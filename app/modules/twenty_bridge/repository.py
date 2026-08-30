from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Integer, case, cast, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ApiKey, RequestLog

_WARMUP_REQUEST_KINDS = ("warmup", "limit_warmup")
_MAX_MODELS_PER_WORKSPACE = 100


@dataclass(frozen=True, slots=True)
class UsageTotals:
    request_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    error_count: int = 0
    total_cost_usd: float = 0.0


@dataclass(frozen=True, slots=True)
class ModelUsage(UsageTotals):
    model: str = ""


@dataclass(frozen=True, slots=True)
class WorkspaceUsage(UsageTotals):
    workspace_id: str = ""
    workspace_name: str = ""
    is_active: bool = False
    last_used_at: datetime | None = None
    models: tuple[ModelUsage, ...] = ()


class TwentyUsageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @staticmethod
    def _usage_columns() -> tuple:
        return (
            func.count(RequestLog.id).label("request_count"),
            func.coalesce(func.sum(RequestLog.input_tokens), 0).label("input_tokens"),
            func.coalesce(
                func.sum(func.coalesce(RequestLog.output_tokens, RequestLog.reasoning_tokens, 0)),
                0,
            ).label("output_tokens"),
            func.coalesce(func.sum(RequestLog.cached_input_tokens), 0).label("cached_input_tokens"),
            func.coalesce(
                func.sum(cast(case((RequestLog.status != "success", 1), else_=0), Integer)),
                0,
            ).label("error_count"),
            func.coalesce(func.sum(RequestLog.cost_usd), 0.0).label("total_cost_usd"),
        )

    @staticmethod
    def _exclude_warmup_clause():
        return or_(
            RequestLog.request_kind.is_(None),
            ~RequestLog.request_kind.in_(_WARMUP_REQUEST_KINDS),
        )

    @staticmethod
    def _window_join_condition(window_started_at: datetime):
        return (
            (RequestLog.api_key_id == ApiKey.id)
            & (RequestLog.requested_at >= window_started_at)
            & TwentyUsageRepository._exclude_warmup_clause()
        )

    async def list_workspace_usage(self, window_started_at: datetime) -> list[WorkspaceUsage]:
        totals_stmt = (
            select(
                ApiKey.id,
                ApiKey.twenty_workspace_id,
                ApiKey.twenty_workspace_name,
                ApiKey.is_active,
                ApiKey.last_used_at,
                *self._usage_columns(),
            )
            .outerjoin(RequestLog, self._window_join_condition(window_started_at))
            .where(ApiKey.twenty_workspace_id.is_not(None))
            .group_by(
                ApiKey.id,
                ApiKey.twenty_workspace_id,
                ApiKey.twenty_workspace_name,
                ApiKey.is_active,
                ApiKey.last_used_at,
            )
            .order_by(ApiKey.twenty_workspace_name.asc(), ApiKey.twenty_workspace_id.asc())
        )
        total_rows = (await self._session.execute(totals_stmt)).all()
        if not total_rows:
            return []

        key_ids = [str(row.id) for row in total_rows]
        model_stmt = (
            select(RequestLog.api_key_id, RequestLog.model, *self._usage_columns())
            .where(
                RequestLog.api_key_id.in_(key_ids),
                RequestLog.requested_at >= window_started_at,
                self._exclude_warmup_clause(),
            )
            .group_by(RequestLog.api_key_id, RequestLog.model)
            .order_by(RequestLog.api_key_id.asc(), func.sum(RequestLog.cost_usd).desc(), RequestLog.model.asc())
        )
        model_rows = (await self._session.execute(model_stmt)).all()
        models_by_key: dict[str, list[ModelUsage]] = {key_id: [] for key_id in key_ids}
        for row in model_rows:
            key_models = models_by_key[str(row.api_key_id)]
            if len(key_models) >= _MAX_MODELS_PER_WORKSPACE:
                continue
            key_models.append(
                ModelUsage(
                    model=str(row.model),
                    request_count=int(row.request_count or 0),
                    input_tokens=int(row.input_tokens or 0),
                    output_tokens=int(row.output_tokens or 0),
                    cached_input_tokens=int(row.cached_input_tokens or 0),
                    error_count=int(row.error_count or 0),
                    total_cost_usd=float(row.total_cost_usd or 0.0),
                )
            )

        return [
            WorkspaceUsage(
                workspace_id=str(row.twenty_workspace_id),
                workspace_name=str(row.twenty_workspace_name or row.twenty_workspace_id),
                is_active=bool(row.is_active),
                last_used_at=row.last_used_at,
                request_count=int(row.request_count or 0),
                input_tokens=int(row.input_tokens or 0),
                output_tokens=int(row.output_tokens or 0),
                cached_input_tokens=int(row.cached_input_tokens or 0),
                error_count=int(row.error_count or 0),
                total_cost_usd=float(row.total_cost_usd or 0.0),
                models=tuple(models_by_key[str(row.id)]),
            )
            for row in total_rows
        ]

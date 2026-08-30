from __future__ import annotations

from datetime import timedelta

from app.core.utils.time import utcnow
from app.modules.twenty_bridge.repository import TwentyUsageRepository, UsageTotals, WorkspaceUsage
from app.modules.twenty_bridge.schemas import (
    TwentyGlobalUsageResponse,
    TwentyModelUsageResponse,
    TwentyUsageTotalsResponse,
    TwentyWorkspaceUsageResponse,
    UsageWindow,
)

_WINDOW_DAYS: dict[UsageWindow, int] = {"1d": 1, "7d": 7, "30d": 30}


def _totals_response(value: UsageTotals) -> TwentyUsageTotalsResponse:
    return TwentyUsageTotalsResponse(
        request_count=value.request_count,
        input_tokens=value.input_tokens,
        output_tokens=value.output_tokens,
        cached_input_tokens=value.cached_input_tokens,
        error_count=value.error_count,
        total_cost_usd=round(value.total_cost_usd, 6),
    )


class TwentyUsageService:
    def __init__(self, repository: TwentyUsageRepository) -> None:
        self._repository = repository

    async def get_global_usage(self, window: UsageWindow) -> TwentyGlobalUsageResponse:
        generated_at = utcnow()
        window_started_at = generated_at - timedelta(days=_WINDOW_DAYS[window])
        workspaces = await self._repository.list_workspace_usage(window_started_at)
        totals = UsageTotals(
            request_count=sum(item.request_count for item in workspaces),
            input_tokens=sum(item.input_tokens for item in workspaces),
            output_tokens=sum(item.output_tokens for item in workspaces),
            cached_input_tokens=sum(item.cached_input_tokens for item in workspaces),
            error_count=sum(item.error_count for item in workspaces),
            total_cost_usd=sum(item.total_cost_usd for item in workspaces),
        )
        return TwentyGlobalUsageResponse(
            generated_at=generated_at,
            window=window,
            window_started_at=window_started_at,
            totals=_totals_response(totals),
            workspaces=[self._workspace_response(item) for item in workspaces],
        )

    @staticmethod
    def _workspace_response(item: WorkspaceUsage) -> TwentyWorkspaceUsageResponse:
        totals = _totals_response(item)
        return TwentyWorkspaceUsageResponse(
            workspace_id=item.workspace_id,
            workspace_name=item.workspace_name,
            is_active=item.is_active,
            last_used_at=item.last_used_at,
            **totals.model_dump(),
            models=[
                TwentyModelUsageResponse(model=model.model, **_totals_response(model).model_dump())
                for model in item.models
            ],
        )

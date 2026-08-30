from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import Field

from app.modules.shared.schemas import DashboardModel

UsageWindow = Literal["1d", "7d", "30d"]


class TwentyUsageTotalsResponse(DashboardModel):
    request_count: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    error_count: int = 0
    total_cost_usd: float = 0.0


class TwentyModelUsageResponse(TwentyUsageTotalsResponse):
    model: str


class TwentyWorkspaceUsageResponse(TwentyUsageTotalsResponse):
    workspace_id: str
    workspace_name: str
    is_active: bool
    last_used_at: datetime | None = None
    models: list[TwentyModelUsageResponse] = Field(default_factory=list)


class TwentyGlobalUsageResponse(DashboardModel):
    generated_at: datetime
    window: UsageWindow
    window_started_at: datetime
    totals: TwentyUsageTotalsResponse
    workspaces: list[TwentyWorkspaceUsageResponse] = Field(default_factory=list)

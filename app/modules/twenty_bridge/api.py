from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.audit.service import AuditService
from app.core.auth.dependencies import set_dashboard_error_format
from app.db.session import get_session
from app.modules.twenty_bridge.auth import require_twenty_usage_bridge
from app.modules.twenty_bridge.repository import TwentyUsageRepository
from app.modules.twenty_bridge.schemas import TwentyGlobalUsageResponse, UsageWindow
from app.modules.twenty_bridge.service import TwentyUsageService

router = APIRouter(
    prefix="/api/integrations/twenty/v1",
    tags=["integrations"],
    dependencies=[Depends(set_dashboard_error_format), Depends(require_twenty_usage_bridge)],
)


@router.get("/workspace-usage", response_model=TwentyGlobalUsageResponse)
async def get_workspace_usage(
    request: Request,
    window: UsageWindow = Query(default="7d"),
    session: AsyncSession = Depends(get_session),
) -> TwentyGlobalUsageResponse:
    result = await TwentyUsageService(TwentyUsageRepository(session)).get_global_usage(window)
    AuditService.log_async(
        "twenty_usage_bridge_read",
        actor_ip=request.client.host if request.client else None,
        details={"window": window, "workspace_count": len(result.workspaces)},
    )
    return result

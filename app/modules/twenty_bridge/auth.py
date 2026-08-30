from __future__ import annotations

import secrets

from fastapi import Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import DashboardAuthError, DashboardNotFoundError
from app.core.rate_limiter.db_rate_limiter import DatabaseRateLimiter
from app.db.session import get_session
from app.modules.twenty_bridge.config import get_twenty_usage_bridge_token

_RATE_LIMITER = DatabaseRateLimiter(max_attempts=120, window_seconds=60, type="twenty_usage_bridge")


async def require_twenty_usage_bridge(
    authorization: str | None = Header(default=None),
    session: AsyncSession = Depends(get_session),
) -> None:
    configured = get_twenty_usage_bridge_token()
    presented = _extract_bearer_token(authorization)
    if configured is None:
        raise DashboardNotFoundError("Not found")
    if presented is None or not secrets.compare_digest(presented, configured):
        raise DashboardAuthError("Invalid integration credential")

    await _RATE_LIMITER.check_and_increment("twenty-owner-app", session)


def _extract_bearer_token(authorization: str | None) -> str | None:
    if authorization is None:
        return None
    scheme, separator, token = authorization.partition(" ")
    if not separator or scheme.lower() != "bearer" or not token.strip():
        return None
    return token.strip()

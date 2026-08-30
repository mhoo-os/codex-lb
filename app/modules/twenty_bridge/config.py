from __future__ import annotations

import os
from collections.abc import Mapping

_TOKEN_ENV_NAME = "CODEX_LB_TWENTY_USAGE_BRIDGE_TOKEN"
_MIN_TOKEN_LENGTH = 32


def get_twenty_usage_bridge_token(environ: Mapping[str, str] | None = None) -> str | None:
    source = os.environ if environ is None else environ
    raw = source.get(_TOKEN_ENV_NAME)
    if raw is None or not raw.strip():
        return None
    token = raw.strip()
    if len(token) < _MIN_TOKEN_LENGTH:
        raise ValueError(f"{_TOKEN_ENV_NAME} must contain at least {_MIN_TOKEN_LENGTH} characters")
    return token


def validate_twenty_usage_bridge_config(environ: Mapping[str, str] | None = None) -> None:
    get_twenty_usage_bridge_token(environ)

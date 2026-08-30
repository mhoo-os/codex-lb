from __future__ import annotations

import pytest

from app.modules.twenty_bridge.config import get_twenty_usage_bridge_token


def test_twenty_usage_bridge_is_disabled_when_secret_is_absent():
    assert get_twenty_usage_bridge_token({}) is None


def test_twenty_usage_bridge_requires_long_distinct_token():
    with pytest.raises(ValueError, match="at least 32 characters"):
        get_twenty_usage_bridge_token({"CODEX_LB_TWENTY_USAGE_BRIDGE_TOKEN": "too-short"})

    assert get_twenty_usage_bridge_token({"CODEX_LB_TWENTY_USAGE_BRIDGE_TOKEN": "x" * 32}) == "x" * 32

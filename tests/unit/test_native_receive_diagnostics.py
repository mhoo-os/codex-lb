from __future__ import annotations

import asyncio
import logging
from typing import Any, cast
from unittest.mock import AsyncMock

import pytest

from app.core.clients.native_egress import NativeEgressProtocolError, NativeEgressTransportError, NativeWebSocketMessage
from app.core.clients.proxy_websocket import NativeUpstreamWebSocket


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "phase",
    [
        "websocket_receive",
        "helper_exit",
        "helper_read",
        "helper_write",
        "shutdown",
        "consumer_backpressure",
        "liveness_timeout",
    ],
)
async def test_receive_failure_logs_only_allowlisted_phase(phase: str, caplog: pytest.LogCaptureFixture) -> None:
    error = NativeEgressTransportError(
        "secret-token and private payload",
        failure_phase=phase,
        headers=(("authorization", "secret-token"),),
        body=b"private payload",
    )
    upstream = AsyncMock()
    upstream.receive.side_effect = error
    with caplog.at_level(logging.WARNING):
        message = await NativeUpstreamWebSocket(cast(Any, upstream)).receive()
    assert message.kind == "error"
    assert message.error == "Upstream websocket receive failed"
    if phase == "liveness_timeout":
        assert message.error_code == "upstream_websocket_liveness_timeout"
    elif phase in {"helper_exit", "helper_read", "helper_write", "shutdown"}:
        assert message.error_code == "proxy_network_unavailable"
    else:
        assert message.error_code is None
    assert f"native_websocket_receive_failed phase={phase}" in caplog.text
    assert "secret-token" not in caplog.text
    assert "private payload" not in caplog.text
    assert all(record.exc_info is None for record in caplog.records)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "error,category",
    [
        (NativeEgressTransportError("secret", failure_phase="private-id\nsecret"), "other"),
        (NativeEgressProtocolError("secret"), "protocol"),
    ],
)
async def test_receive_failure_rejects_untrusted_categories(
    error: Exception, category: str, caplog: pytest.LogCaptureFixture
) -> None:
    upstream = AsyncMock()
    upstream.receive.side_effect = error
    message = await NativeUpstreamWebSocket(cast(Any, upstream)).receive()
    assert message.kind == "error"
    assert f"phase={category}" in caplog.text
    assert "secret" not in caplog.text
    assert "private-id" not in caplog.text


@pytest.mark.asyncio
@pytest.mark.parametrize("code,logged", [(1000, "1000"), (1011, "1011"), (None, "None"), (999, "None"), (5000, "None")])
async def test_close_logs_code_without_reason_and_preserves_message(
    code: int | None, logged: str, caplog: pytest.LogCaptureFixture
) -> None:
    upstream = AsyncMock()
    upstream.receive.return_value = NativeWebSocketMessage(kind="close", close_code=code, close_reason="private reason")
    with caplog.at_level(logging.INFO):
        message = await NativeUpstreamWebSocket(cast(Any, upstream)).receive()
    assert message.kind == "close"
    assert message.close_code == code
    assert message.close_reason == "private reason"
    assert f"native_websocket_closed code={logged}" in caplog.text
    assert "private reason" not in caplog.text


@pytest.mark.asyncio
async def test_data_and_cancellation_emit_no_diagnostic(caplog: pytest.LogCaptureFixture) -> None:
    upstream = AsyncMock()
    upstream.receive.side_effect = [NativeWebSocketMessage(kind="text", text="private frame"), asyncio.CancelledError()]
    adapter = NativeUpstreamWebSocket(cast(Any, upstream))
    with caplog.at_level(logging.INFO):
        assert (await adapter.receive()).text == "private frame"
        with pytest.raises(asyncio.CancelledError):
            await adapter.receive()
    assert not caplog.records

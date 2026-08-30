from __future__ import annotations

from datetime import timedelta

import pytest

import app.modules.twenty_bridge.auth as bridge_auth
from app.core.utils.time import utcnow
from app.db.models import ApiKey, RequestLog
from app.db.session import SessionLocal

pytestmark = pytest.mark.integration

_TOKEN = "twenty-test-bridge-token-that-is-long-enough"


@pytest.fixture
def enabled_bridge(monkeypatch):
    monkeypatch.setattr(
        bridge_auth,
        "get_twenty_usage_bridge_token",
        lambda: _TOKEN,
    )


@pytest.mark.asyncio
async def test_bridge_requires_distinct_bearer_token(async_client, enabled_bridge):
    missing = await async_client.get("/api/integrations/twenty/v1/workspace-usage")
    assert missing.status_code == 401

    invalid = await async_client.get(
        "/api/integrations/twenty/v1/workspace-usage",
        headers={"Authorization": "Bearer wrong"},
    )
    assert invalid.status_code == 401


@pytest.mark.asyncio
async def test_api_key_workspace_binding_is_unique(async_client):
    created = await async_client.post(
        "/api/api-keys/",
        json={
            "name": "mhoo-twenty-workspace",
            "twentyWorkspaceId": "workspace-mhoo",
            "twentyWorkspaceName": "MHOO",
        },
    )
    assert created.status_code == 200
    assert created.json()["twentyWorkspaceId"] == "workspace-mhoo"
    assert created.json()["twentyWorkspaceName"] == "MHOO"

    duplicate = await async_client.post(
        "/api/api-keys/",
        json={
            "name": "duplicate",
            "twentyWorkspaceId": "workspace-mhoo",
        },
    )
    assert duplicate.status_code == 400
    assert duplicate.json()["error"]["code"] == "invalid_api_key_payload"

    orphan_name = await async_client.post(
        "/api/api-keys/",
        json={
            "name": "orphan-name",
            "twentyWorkspaceName": "No immutable id",
        },
    )
    assert orphan_name.status_code == 400


@pytest.mark.asyncio
async def test_bridge_returns_only_bound_workspace_aggregates(async_client, enabled_bridge):
    now = utcnow()
    async with SessionLocal() as session:
        session.add_all(
            [
                ApiKey(
                    id="key-mhoo",
                    name="mhoo-twenty-workspace",
                    key_hash="hash-mhoo",
                    key_prefix="sk-clb-mhoo",
                    twenty_workspace_id="workspace-mhoo",
                    twenty_workspace_name="MHOO",
                    is_active=True,
                    created_at=now,
                ),
                ApiKey(
                    id="key-unbound",
                    name="unbound",
                    key_hash="hash-unbound",
                    key_prefix="sk-clb-unbound",
                    is_active=True,
                    created_at=now,
                ),
            ]
        )
        session.add_all(
            [
                RequestLog(
                    api_key_id="key-mhoo",
                    request_id="req-success",
                    request_kind="normal",
                    requested_at=now - timedelta(hours=1),
                    model="gpt-5.6-sol",
                    input_tokens=100,
                    output_tokens=20,
                    cached_input_tokens=40,
                    cost_usd=0.25,
                    status="success",
                ),
                RequestLog(
                    api_key_id="key-mhoo",
                    request_id="req-error",
                    request_kind="normal",
                    requested_at=now - timedelta(hours=2),
                    model="gpt-5.6-sol",
                    input_tokens=10,
                    output_tokens=0,
                    cached_input_tokens=0,
                    cost_usd=0.01,
                    status="error",
                ),
                RequestLog(
                    api_key_id="key-mhoo",
                    request_id="req-warmup",
                    request_kind="warmup",
                    requested_at=now - timedelta(minutes=5),
                    model="gpt-5.6-sol",
                    input_tokens=999,
                    output_tokens=999,
                    cost_usd=99,
                    status="success",
                ),
                RequestLog(
                    api_key_id="key-unbound",
                    request_id="req-unbound",
                    request_kind="normal",
                    requested_at=now - timedelta(minutes=5),
                    model="gpt-5.6-sol",
                    input_tokens=999,
                    output_tokens=999,
                    cost_usd=99,
                    status="success",
                ),
            ]
        )
        await session.commit()

    response = await async_client.get(
        "/api/integrations/twenty/v1/workspace-usage?window=1d",
        headers={"Authorization": f"Bearer {_TOKEN}"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["window"] == "1d"
    assert payload["totals"] == {
        "requestCount": 2,
        "inputTokens": 110,
        "outputTokens": 20,
        "cachedInputTokens": 40,
        "errorCount": 1,
        "totalCostUsd": 0.26,
    }
    assert len(payload["workspaces"]) == 1
    workspace = payload["workspaces"][0]
    assert workspace["workspaceId"] == "workspace-mhoo"
    assert workspace["workspaceName"] == "MHOO"
    assert workspace["models"][0]["model"] == "gpt-5.6-sol"
    assert "keyPrefix" not in workspace


@pytest.mark.asyncio
async def test_bridge_bounds_model_aggregates_per_workspace(async_client, enabled_bridge):
    now = utcnow()
    async with SessionLocal() as session:
        session.add(
            ApiKey(
                id="key-many-models",
                name="many-models",
                key_hash="hash-many-models",
                key_prefix="sk-clb-many-models",
                twenty_workspace_id="workspace-many-models",
                twenty_workspace_name="Many Models",
                is_active=True,
                created_at=now,
            )
        )
        session.add_all(
            [
                RequestLog(
                    api_key_id="key-many-models",
                    request_id=f"req-model-{index}",
                    request_kind="normal",
                    requested_at=now - timedelta(minutes=5),
                    model=f"model-{index:03d}",
                    input_tokens=1,
                    output_tokens=1,
                    cost_usd=index / 1_000,
                    status="success",
                )
                for index in range(101)
            ]
        )
        await session.commit()

    response = await async_client.get(
        "/api/integrations/twenty/v1/workspace-usage?window=1d",
        headers={"Authorization": f"Bearer {_TOKEN}"},
    )

    assert response.status_code == 200
    workspace = response.json()["workspaces"][0]
    assert workspace["requestCount"] == 101
    assert len(workspace["models"]) == 100
    assert workspace["models"][0]["model"] == "model-100"
    assert workspace["models"][-1]["model"] == "model-001"


@pytest.mark.asyncio
async def test_bridge_is_not_routable_when_disabled(async_client, monkeypatch):
    monkeypatch.setattr(
        bridge_auth,
        "get_twenty_usage_bridge_token",
        lambda: None,
    )
    response = await async_client.get(
        "/api/integrations/twenty/v1/workspace-usage",
        headers={"Authorization": f"Bearer {_TOKEN}"},
    )
    assert response.status_code == 404

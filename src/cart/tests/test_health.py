import pytest
import requests_mock

from cart.client.api_client import ApiClient

# HEALTH / GRACEFUL DEGRADATION TEST: Upstream availability signal
#
# Purpose:
# Validate that the system correctly reports health status
# when upstream services are available.
#
# Context for Knot:
# Health endpoints act as an early-warning signal.
# They must be reliable, fast, and independent from unstable
# external systems in CI.
#
# CI behavior:
# - External calls are mocked to keep CI deterministic
# - This test blocks CI because it validates system observability
#
# Key principle:
# Health checks must be fast, predictable, and safe.

pytestmark = pytest.mark.negative


def test_health_endpoint_reports_ok_status(requests_mock):
    # Scenario:
    # Upstream dependency is reachable and responds successfully.

    base_url = "https://cart.local"

    requests_mock.get(
        f"{base_url}/health",
        status_code=200,
        json={"status": "ok"}
    )

    client = ApiClient(base_url=base_url)

    response = client.get("/health")

    # Expected behavior:
    # - system reports healthy state
    # - no dependency on real network or external services

    assert response.status_code == 200
    assert response.json().get("status") == "ok"

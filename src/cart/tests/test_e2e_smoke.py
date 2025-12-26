import pytest
import requests
from cart.client.api_client import ApiClient

# E2E SMOKE TESTS (API-LEVEL)
# Purpose:
# This file contains minimal end-to-end smoke tests that represent
# critical user-facing journeys without UI automation.
#
# Why API-level E2E:
# UI tests are slow and flaky. These tests validate that the system
# is correctly wired across backend and external merchant boundaries
# while keeping CI fast and deterministic.
#
# Scope:
# - Only happy-path and user-visible failure scenarios
# - No edge cases, retries, or contract validation here
# - All complex behavior is covered by dedicated API and contract tests
#
# CI Policy:
# These tests are allowed to block releases only if a core user flow
# is broken. They are intentionally few, stable, and fast.
#
# Knot context:
# External merchant APIs are unreliable. E2E smoke tests prove that
# the core integration flow works, while resilience is validated separately.

pytestmark = pytest.mark.e2e_smoke


def test_e2e_user_successfully_links_merchant_account(requests_mock):
    # Scenario:
    # User completes the primary merchant linking flow (happy path).

    base_url = "https://cart.local"
    endpoint = "/merchant/connect"

    requests_mock.post(
        f"{base_url}{endpoint}",
        status_code=200,
        json={"status": "connected", "merchantId": "123"}
    )

    client = ApiClient(base_url=base_url)
    response = client.post(endpoint, payload={"merchantId": "123"})

    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "connected"
    assert data.get("merchantId") == "123"


def test_e2e_user_receives_controlled_error_when_merchant_unavailable(requests_mock):
    # Scenario:
    # Merchant API times out. System must degrade gracefully
    # and return a controlled response instead of crashing.

    base_url = "https://cart.local"
    endpoint = "/merchant/connect"

    requests_mock.post(
        f"{base_url}{endpoint}",
        exc=requests.exceptions.Timeout
    )

    client = ApiClient(base_url=base_url)
    response = client.post(endpoint, payload={"merchantId": "123"})

    assert response.status_code == 504
    assert response.json().get("error") == "timeout"

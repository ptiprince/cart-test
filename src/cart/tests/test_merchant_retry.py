import pytest

from cart.client.api_client import ApiClient

# CONTRACT / RESILIENCE TEST: Merchant API retry handling
#
# Purpose:
# Validate that the system retries requests when a merchant API
# temporarily fails and eventually succeeds.
#
# Context for Knot:
# External merchant APIs may experience transient failures (5xx).
# The system must retry safely without duplicating actions or
# corrupting state.
#
# CI behavior:
# - Merchant API is mocked to keep CI deterministic and fast
# - This test blocks CI because it validates retry and recovery logic
#
# Non-blocking behavior:
# - Real merchant stability is monitored separately
# - CI validates our retry policy, not merchant uptime

pytestmark = pytest.mark.contract


def test_merchant_retry_on_temporary_failure(requests_mock):
    # Scenario:
    # Merchant API fails temporarily and then recovers.
    # First request returns 503.
    # Second request returns 200.

    base_url = "https://cart.local"
    endpoint = "/merchant/status"

    requests_mock.get(
        f"{base_url}{endpoint}",
        [
            {"status_code": 503},
            {"status_code": 200, "json": {"status": "ok"}}
        ]
    )

    # Initialize API client with a single retry attempt
    client = ApiClient(base_url=base_url, retries=1)

    response = client.get(endpoint)

    # Expected behavior:
    # - client retries on temporary failure
    # - request eventually succeeds
    # - no duplicate or inconsistent state is created

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

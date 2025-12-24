import pytest

from cart.client.api_client import ApiClient

# CONTRACT / FAILURE TEST: Merchant API timeout handling
#
# Purpose:
# Validate that the system handles external merchant API timeouts
# in a controlled and predictable way.
#
# Context for Knot:
# Merchant APIs are external dependencies and may become slow or unavailable.
# Timeouts must not crash the system or propagate raw exceptions to users.
#
# CI behavior:
# - Merchant API is mocked to keep CI deterministic
# - This test blocks CI because it validates safe failure behavior
#
# Non-blocking behavior:
# - Real merchant latency monitoring belongs to non-blocking checks
#   (monitoring / synthetic probes), not CI

pytestmark = pytest.mark.contract


def test_merchant_timeout_handling(requests_mock):
    # Scenario:
    # Merchant API does not respond and triggers a timeout.

    base_url = "https://cart.local"
    endpoint = "/merchant/status"

    requests_mock.get(
        f"{base_url}{endpoint}",
        # Simulate a network-level timeout from merchant API
        exc=Exception("Timeout")
    )

    client = ApiClient(base_url=base_url)

    response = client.get(endpoint)

    # Expected behavior:
    # - timeout is caught
    # - system returns a controlled error response
    # - no unhandled exception reaches the caller

    assert response.status_code == 504
    assert response.json()["error"] == "timeout"


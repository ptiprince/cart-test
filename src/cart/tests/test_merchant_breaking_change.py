import pytest

from cart.client.api_client import ApiClient

# CONTRACT / BREAKING CHANGE TEST: Merchant API response validation
#
# Purpose:
# Validate system behavior when an external merchant API introduces
# a breaking change by removing a required field from the response.
#
# Context for Knot:
# External merchant APIs are not under our control and may change
# response schemas without notice. Such changes must not crash
# core user flows or corrupt data.
#
# CI behavior:
# - Merchant API is mocked to keep CI fast and deterministic
# - This test blocks CI because it validates our assumptions
#   about merchant response structure
#
# Non-blocking behavior:
# - Real merchant breaking-change detection should run separately
#   (nightly / monitoring pipelines) against live APIs

pytestmark = pytest.mark.contract


def test_merchant_api_breaking_change_missing_field(requests_mock):
    # Scenario:
    # Merchant API responds with HTTP 200 but removes
    # a required field from the payload.

    base_url = "https://cart.local"
    endpoint = "/merchant/data"

    requests_mock.get(
        f"{base_url}{endpoint}",
        status_code=200,
        json={
            # "merchantId" is intentionally missing
            # to simulate a breaking schema change
            "status": "active"
        }
    )

    client = ApiClient(base_url=base_url)

    response = client.get(endpoint)

    # Expected behavior:
    # - client must not crash
    # - response is handled safely
    # - missing required fields are not silently fabricated

    assert response.status_code == 200

    data = response.json()

    assert "merchantId" not in data
    assert data["status"] == "active"


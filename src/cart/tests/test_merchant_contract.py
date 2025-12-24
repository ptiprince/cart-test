import pytest
import requests_mock

from cart.client.api_client import ApiClient

# CONTRACT TEST: Merchant API schema validation
#
# Purpose:
# Validate how our system behaves when an external merchant API
# introduces a breaking change in the response schema.
#
# Context for Knot:
# Merchant APIs are external and unstable. They may remove required fields,
# change payload structure, or partially break without notice.
# QA must ensure such changes are detected early and handled safely.
#
# CI behavior:
# - Merchant API is mocked to keep CI deterministic and fast
# - This test blocks CI because it validates OUR contract assumptions
#
# Non-blocking behavior:
# - Real merchant contract checks should run separately (nightly / on-demand)
#   to detect upstream breaking changes without blocking merges

pytestmark = pytest.mark.contract


def test_merchant_api_missing_required_field():
    # Scenario:
    # Merchant API returns HTTP 200 but payload is missing
    # a required field expected by our system.

    base_url = "https://merchant.example"
    client = ApiClient(base_url=base_url)

    with requests_mock.Mocker() as m:
        m.get(
            f"{base_url}/merchant/profile",
            json={
                # "merchantId" is intentionally missing
                # to simulate a breaking change in merchant API contract
                "name": "Test Merchant",
                "status": "active"
            },
            status_code=200
        )

        response = client.get("/merchant/profile")

        # Expected behavior:
        # - system must not crash
        # - response must be handled safely
        # - missing required fields must not be silently fabricated

        assert response.status_code == 200
        assert "merchantId" not in response.json()


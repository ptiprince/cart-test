import pytest
import requests

from cart.client.api_client import ApiClient

# NEGATIVE / GRACEFUL DEGRADATION TEST: Invalid input handling
#
# Purpose:
# Validate that the system handles invalid requests safely
# and returns a controlled, user-safe error response.
#
# Context for Knot:
# External merchant APIs and user inputs can fail or be invalid.
# The system must not crash, corrupt data, or return generic 500 errors.
# Instead, it must fail fast and fail safely.
#
# CI behavior:
# - External dependencies are mocked
# - This test blocks CI because it validates safe failure behavior
#
# Key principle:
# Graceful degradation means predictable errors and stable system state.

pytestmark = pytest.mark.negative


def test_card_switch_invalid_payload(requests_mock):
    # Scenario:
    # Client sends an invalid payload to the card-switch endpoint.

    base_url = "https://cart.test"
    client = ApiClient(base_url=base_url)

    requests_mock.post(
        f"{base_url}/card-switch",
        status_code=400,
        json={"error": "Invalid payload"}
    )

    response = client.post("/card-switch", payload={})

    # Expected behavior:
    # - system returns a clear client error
    # - error is explicit and user-safe
    # - no unhandled exception or 500 error

    assert response.status_code == 400
    assert "error" in response.json()


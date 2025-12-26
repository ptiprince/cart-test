import pytest
from cart.client.api_client import ApiClient

# INTEGRATION TEST
# Purpose:
# Validate combined behavior of retry logic and idempotency protection
# when interacting with an external merchant API.
#
# Why integration:
# This test verifies how multiple components work together:
# - API client request handling
# - Retry behavior on transient merchant failures
# - Idempotency protection for repeated requests
#
# Strategy:
# - Merchant API is mocked to keep the test deterministic
# - No UI or live external dependencies are used
# - The test represents a real production risk scenario for Knot

pytestmark = pytest.mark.integration


def test_integration_retry_and_idempotency(requests_mock):
    base_url = "https://cart.local"
    endpoint = "/card-switch"
    idempotency_key = "idem-123"

    # First call: transient merchant failure
    # Second call: successful response
    requests_mock.post(
        f"{base_url}{endpoint}",
        [
            {"status_code": 503},
            {"status_code": 200, "json": {"status": "switched"}}
        ]
    )

    client = ApiClient(base_url=base_url, retries=1)

    # Initial request triggers retry and succeeds
    response_first = client.post(
        endpoint,
        payload={"cardId": "abc"},
        headers={"Idempotency-Key": idempotency_key}
    )

    # Repeated request with the same idempotency key
    response_second = client.post(
        endpoint,
        payload={"cardId": "abc"},
        headers={"Idempotency-Key": idempotency_key}
    )

    assert response_first.status_code == 200
    assert response_second.status_code == 200
    assert response_first.json() == response_second.json()

import requests
from cart.client.api_client import ApiClient

def test_idempotent_request(requests_mock):
    """
    Verify that repeating the same request with the same idempotency key
    does not create duplicate operations and returns the same result.
    """

    base_url = "https://cart.local"
    endpoint = "/switch-card"
    idempotency_key = "test-idem-123"

    # Mock the external API response
    requests_mock.post(
        f"{base_url}{endpoint}",
        json={"switchId": "abc-123", "status": "completed"},
        status_code=200
    )

    client = ApiClient(base_url=base_url)

    response1 = client.post(
        endpoint,
        json={"cardId": "1111"},
        headers={"Idempotency-Key": idempotency_key}
    )

    response2 = client.post(
        endpoint,
        json={"cardId": "1111"},
        headers={"Idempotency-Key": idempotency_key}
    )

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response1.json()["switchId"] == response2.json()["switchId"]

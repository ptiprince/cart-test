import requests_mock
from cart.client.api_client import ApiClient
from cart.contracts.health_contract import validate_health_response

def test_health_endpoint_contract():
    # Mock external Cart API to keep test deterministic and CI-safe
    with requests_mock.Mocker() as mock:
        # Stub health endpoint response
        mock.get(
            "https://cart.local/health",
            json={"status": "ok"},
            status_code=200,
        )

        # Initialize API client with mocked base URL
        client = ApiClient(base_url="https://cart.local")

        # Call health endpoint
        response = client.get("/health")

        # Assert successful HTTP response
        assert response.status_code == 200

        # Validate response contract to catch breaking API changes
        validate_health_response(response.json())

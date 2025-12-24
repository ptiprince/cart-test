import pytest

from cart.client.api_client import ApiClient

# CONTRACT / BACKWARD COMPATIBILITY TEST: Merchant API versioning
#
# Purpose:
# Validate that the system correctly handles merchant API versioning
# via response headers and remains backward-compatible when version
# information is missing.
#
# Context for Knot:
# External merchant APIs may introduce new versions, change behavior,
# or omit version headers entirely. The system must not crash or behave
# unpredictably when version metadata changes.
#
# CI behavior:
# - Merchant API is mocked to keep CI deterministic
# - This test blocks CI because it validates our compatibility guarantees
#
# Non-blocking behavior:
# - Live merchant version drift is monitored separately
# - CI focuses on our ability to tolerate version changes safely

pytestmark = pytest.mark.contract


def test_merchant_api_version_header(requests_mock):
    # Scenario:
    # Merchant API responds with an explicit API version header.

    base_url = "https://cart.local"
    endpoint = "/merchant/status"

    requests_mock.get(
        f"{base_url}{endpoint}",
        status_code=200,
        headers={"X-API-Version": "v1"},
        json={"status": "ok"}
    )

    client = ApiClient(base_url=base_url)
    response = client.get(endpoint)

    # Expected behavior:
    # - response is successful
    # - API version header is preserved and accessible

    assert response.status_code == 200
    assert response.headers.get("X-API-Version") == "v1"


def test_merchant_api_missing_version_header(requests_mock):
    # Scenario:
    # Merchant API responds without an API version header.

    base_url = "https://cart.local"
    endpoint = "/merchant/status"

    requests_mock.get(
        f"{base_url}{endpoint}",
        status_code=200,
        json={"status": "ok"}
    )

    client = ApiClient(base_url=base_url)
    response = client.get(endpoint)

    # Expected behavior:
    # - system does not crash
    # - missing version header is tolerated
    # - backward compatibility is preserved

    assert response.status_code == 200
    assert response.headers.get("X-API-Version") is None

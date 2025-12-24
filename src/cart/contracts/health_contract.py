def validate_health_response(body: dict):
    # Validate minimal response contract for health endpoint
    # This protects against breaking API changes

    assert isinstance(body, dict)
    assert "status" in body
    assert body["status"] in ["ok", "healthy"]
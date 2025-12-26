# Cart API Test Automation

This project is an API-first test automation framework designed to validate a Cart-like backend service that integrates with external merchant APIs.
The focus is on reliability, deterministic CI, and safe handling of third-party failures.

Tech stack:
Python 3.11
pytest
requests
requests-mock

Project structure:
src/cart/client/api_client.py
src/cart/tests/
pytest.ini

Test strategy overview:
The test suite is structured by risk and responsibility rather than raw coverage.
API-level tests validate core business logic, error handling, and resilience against unstable external dependencies.

Test types covered:

Smoke tests
Validate basic test wiring and environment readiness.

Health checks
Validate service availability and observability signals.

API contract tests
Validate required fields and response structure from merchant APIs to detect breaking changes early.

Negative tests
Validate safe handling of invalid input and client-side errors.

Idempotency tests
Ensure repeated requests do not create duplicate side effects in critical flows.

Timeout and retry tests
Validate graceful degradation and controlled retries when merchant APIs fail or respond slowly.

E2E smoke tests (API-level)
End-to-end coverage is intentionally minimal and limited to critical user-facing flows.
These tests validate that core user journeys are correctly wired across backend and external merchant boundaries without using UI automation.
All complex logic, retries, and edge cases are validated at the API and contract level to keep CI fast and deterministic.
E2E smoke tests are allowed to block releases only if a core user flow is broken.

CI principles:
Tests are deterministic and designed to provide clear, actionable signals.
Flaky tests and test-level retries are avoided.
Failures indicate real risk and block releases.

Interview focus:
This project demonstrates how QA owns quality outcomes in API-driven systems with unstable external dependencies.

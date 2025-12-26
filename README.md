# Cart API Test Automation

This project is an API-first test automation framework designed to validate a Cart-like backend service that integrates with external merchant APIs.
The focus is reliability, deterministic CI signals, and protection of core user flows from unstable third-party dependencies.

Problem
The biggest risk for systems like Knot is dependency on external merchant APIs.
Failures, schema changes, latency, or partial outages can directly break critical user journeys.
The QA responsibility is to detect these risks early, isolate ownership, and prevent them from reaching users.

Strategy
API-first, risk-based automation focused on external dependencies.
Merchant APIs are treated as unstable by default.
Failures are expected and handled through controlled behavior.
Quality is enforced through explicit contracts, not assumptions.
CI must be fast, deterministic, and actionable.
The goal is confidence in system behavior, not test count.

Test Types Covered

Smoke Tests
Validate basic test wiring and environment readiness.

Health Checks
Validate service availability and observability signals.

API Contract Tests
Validate required fields and response schemas from merchant APIs to detect breaking changes early.

Negative Tests
Validate safe handling of invalid input and client-side errors.

Integration Tests
Validate how multiple system components work together when interacting with merchant APIs.
Integration tests cover combined behavior of retry logic, idempotency protection, and controlled error handling.
All merchant interactions are mocked to keep execution deterministic and CI-friendly.
These tests focus on the highest-risk integration boundaries where most production issues occur.

E2E Smoke Tests (API-level)
End-to-end coverage is intentionally minimal and limited to critical user-facing flows.
These tests validate that core user journeys are correctly wired across backend and external merchant integrations without using UI automation.
All complex logic, retries, edge cases, and merchant instability are validated at the API and contract level.
E2E smoke tests are allowed to block releases only when a core user flow is broken.

CI Quality Gates
CI runs only deterministic tests with mocked merchant APIs.
No live external dependencies are allowed in CI.
Pytest exit code is the single quality gate.
Any failure blocks the merge.

What Does Not Block CI
Live merchant API checks are intentionally excluded from CI.
They are executed separately to observe real upstream behavior.
CI validates system resilience, not merchant uptime.

Tech Stack
Python 3.11
pytest
requests
requests-mock
GitHub Actions

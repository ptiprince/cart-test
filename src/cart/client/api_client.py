from __future__ import annotations

import json as json_lib
import time
from typing import Any, Dict, Optional

import requests
from requests.models import Response


class ApiClient:
    # Minimal HTTP client for API tests.
    # Handles retries and converts timeouts into controlled 504 responses.

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        retries: int = 0,
        retry_backoff_sec: float = 0.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries
        self.retry_backoff_sec = retry_backoff_sec

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def _timeout_response(self) -> Response:
        resp = Response()
        resp.status_code = 504
        resp._content = json_lib.dumps({"error": "timeout"}).encode("utf-8")
        resp.headers["Content-Type"] = "application/json"
        return resp

    def _request(
        self,
        method: str,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        payload: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Response:
        body = json if json is not None else payload
        url = self._url(path)

        attempts = 1 + max(0, int(self.retries))
        last_response: Optional[Response] = None

        for attempt in range(attempts):
            try:
                resp = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=body,
                    timeout=self.timeout,
                )
                last_response = resp

                if resp.status_code in (429, 500, 502, 503, 504) and attempt < attempts - 1:
                    if self.retry_backoff_sec > 0:
                        time.sleep(self.retry_backoff_sec)
                    continue

                return resp

            except Exception:
                if attempt < attempts - 1:
                    if self.retry_backoff_sec > 0:
                        time.sleep(self.retry_backoff_sec)
                    continue
                return self._timeout_response()

        return last_response if last_response is not None else self._timeout_response()

    def get(self, path: str, headers: Optional[Dict[str, str]] = None) -> Response:
        return self._request("GET", path, headers=headers)

    def post(
        self,
        path: str,
        headers: Optional[Dict[str, str]] = None,
        payload: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Response:
        return self._request("POST", path, headers=headers, payload=payload, json=json)

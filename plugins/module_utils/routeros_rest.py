"""Small, dependency-free RouterOS REST API client for collection modules."""

from __future__ import annotations

import base64
import json
import ssl
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class RouterOSRestError(Exception):
    """Raised when a RouterOS REST request cannot be completed."""


class RouterOSRestClient:
    """Minimal JSON client implementing the read-only operations needed by facts."""

    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        timeout: int = 30,
        validate_certs: bool = True,
    ) -> None:
        base = host.rstrip("/")
        self.base_url = base if base.endswith("/rest") else f"{base}/rest"
        self.timeout = timeout
        token = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("ascii")
        self.headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {token}",
        }
        self.context = ssl.create_default_context() if validate_certs else ssl._create_unverified_context()

    def get(self, path: str, query: Optional[Dict[str, Any]] = None) -> Any:
        """Read a RouterOS menu using the REST GET operation."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        if query:
            url = f"{url}?{urlencode(query)}"
        request = Request(url, headers=self.headers, method="GET")
        try:
            with urlopen(request, timeout=self.timeout, context=self.context) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RouterOSRestError(f"RouterOS REST GET {path} failed with HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RouterOSRestError(f"RouterOS REST GET {path} failed: {exc.reason}") from exc
        except OSError as exc:
            raise RouterOSRestError(f"RouterOS REST GET {path} failed: {exc}") from exc

        if not body:
            return []
        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise RouterOSRestError(f"RouterOS REST GET {path} returned invalid JSON: {body[:200]}") from exc

    def post(self, path: str, payload: Dict[str, Any]) -> Any:
        """Run a RouterOS REST POST command with a JSON payload."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {**self.headers, "Content-Type": "application/json"}
        request = Request(
            url,
            headers=headers,
            data=json.dumps(payload).encode("utf-8"),
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout, context=self.context) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RouterOSRestError(f"RouterOS REST POST {path} failed with HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RouterOSRestError(f"RouterOS REST POST {path} failed: {exc.reason}") from exc
        except OSError as exc:
            raise RouterOSRestError(f"RouterOS REST POST {path} failed: {exc}") from exc

        if not body:
            return []
        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise RouterOSRestError(f"RouterOS REST POST {path} returned invalid JSON: {body[:200]}") from exc

    def _write(self, method: str, path: str, payload: Optional[Dict[str, Any]] = None) -> Any:
        """Send a JSON write request to a RouterOS REST resource."""
        url = f"{self.base_url}/{path.lstrip('/')}"
        headers = {**self.headers}
        data = None
        if payload is not None:
            headers["Content-Type"] = "application/json"
            data = json.dumps(payload).encode("utf-8")
        request = Request(
            url,
            headers=headers,
            data=data,
            method=method,
        )
        try:
            with urlopen(request, timeout=self.timeout, context=self.context) as response:
                body = response.read().decode("utf-8")
        except HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            raise RouterOSRestError(f"RouterOS REST {method} {path} failed with HTTP {exc.code}: {detail}") from exc
        except URLError as exc:
            raise RouterOSRestError(f"RouterOS REST {method} {path} failed: {exc.reason}") from exc
        except OSError as exc:
            raise RouterOSRestError(f"RouterOS REST {method} {path} failed: {exc}") from exc

        if not body:
            return []
        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise RouterOSRestError(f"RouterOS REST {method} {path} returned invalid JSON: {body[:200]}") from exc

    def put(self, path: str, payload: Dict[str, Any]) -> Any:
        """Create a RouterOS REST resource."""
        return self._write("PUT", path, payload)

    def patch(self, path: str, payload: Dict[str, Any]) -> Any:
        """Update a RouterOS REST resource."""
        return self._write("PATCH", path, payload)

    def delete(self, path: str) -> Any:
        """Delete a RouterOS REST resource."""
        return self._write("DELETE", path)

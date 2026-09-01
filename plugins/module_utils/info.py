"""Shared read-only implementation for RouterOS REST info modules."""

from __future__ import annotations

from typing import Any, Dict, Optional

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)


def run_info(module: AnsibleModule, path: str, result_key: str, selector: Optional[str] = None) -> None:
    """Read a RouterOS menu and return its records without setting facts."""
    params = module.params
    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"]
    )
    query: Dict[str, Any] = {}
    if selector and params.get("name") is not None:
        query[selector] = params["name"]
    if params.get("object_id") is not None:
        query[".id"] = params["object_id"]
    try:
        data = client.get(path, query=query)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
    if not isinstance(data, list):
        data = [data]
    module.exit_json(changed=False, **{result_key: data})


"""Shared idempotent CRUD implementation for RouterOS REST resources."""

from __future__ import annotations

from typing import Any, Dict

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.resource import reconcile


def run_config(module: AnsibleModule, path: str, identity: Dict[str, Any], payload: Dict[str, Any]) -> None:
    """Reconcile one RouterOS REST resource."""
    p = module.params
    client = RouterOSRestClient(
        host=p["host"],
        username=p["username"],
        password=p["password"],
        timeout=p["timeout"],
        validate_certs=p["validate_certs"],
    )
    try:
        reconcile(module, client, path, identity, payload, p["state"], "resource")
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

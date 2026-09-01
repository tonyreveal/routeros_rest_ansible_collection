"""Shared idempotent REST resource reconciliation helpers."""

from __future__ import annotations

from typing import Any, Dict


def first(value: Any):
    if isinstance(value, list):
        return value[0] if value else None
    return value if isinstance(value, dict) else None


def matches(current: Any, desired: Any) -> bool:
    if isinstance(desired, bool):
        return (str(current).lower() in {"yes", "true"}) == desired
    if isinstance(desired, list):
        return (
            [str(item) for item in current] == [str(item) for item in desired]
            if isinstance(current, list)
            else str(current) == ",".join(desired)
        )
    return str(current) == str(desired)


def reconcile(module, client, path: str, query: Dict[str, Any], desired: Dict[str, Any], state: str, result_key: str):
    existing = first(client.get(path, query=query))
    if state == "absent":
        if existing is None:
            module.exit_json(changed=False, **{result_key: {}, "changed_fields": []})
        resource_id = existing.get(".id")
        if not resource_id:
            module.fail_json(msg=f"RouterOS {path} response did not include .id")
        result = existing if module.check_mode else client.delete(f"{path}/{resource_id}")
        module.exit_json(changed=True, **{result_key: result, "changed_fields": [result_key]})
    if existing is None:
        result = desired if module.check_mode else client.put(path, desired)
        module.exit_json(changed=True, **{result_key: result, "changed_fields": list(desired)})
    resource_id = existing.get(".id")
    if not resource_id:
        module.fail_json(msg=f"RouterOS {path} response did not include .id")
    changes = {key: value for key, value in desired.items() if not matches(existing.get(key, ""), value)}
    if not changes:
        module.exit_json(changed=False, **{result_key: existing, "changed_fields": []})
    result = {**existing, **changes} if module.check_mode else client.patch(f"{path}/{resource_id}", changes)
    module.exit_json(changed=True, **{result_key: result, "changed_fields": list(changes)})

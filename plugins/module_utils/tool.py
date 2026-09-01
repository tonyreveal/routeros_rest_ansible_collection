"""Shared execution helper for RouterOS operational REST tools."""
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

def run_tool(module, path, payload):
    p = module.params
    if module.check_mode:
        module.exit_json(changed=False, skipped=True)
    try:
        result = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]).post(path, payload)
        module.exit_json(changed=False, result=result)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

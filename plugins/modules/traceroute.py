#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: traceroute
short_description: Run a RouterOS traceroute
description:
  - Runs a traceroute through the RouterOS REST API and returns hop information.
  - This is an operational action, so state and idempotency are not applicable.
version_added: '1.0.0'
author:
  - Tony Reveal (https://github.com/tonyreveal)
options:
  host:
    description: RouterOS REST base URL.
    type: str
    required: true
  username:
    description: RouterOS REST username.
    type: str
    required: true
  password:
    description: RouterOS REST password.
    type: str
    required: true
    no_log: true
  address:
    description: Hostname or IP address to trace.
    type: str
    required: true
  max_hops:
    description: Maximum number of hops.
    type: int
    default: 30
  timeout:
    description: HTTP timeout in seconds.
    type: int
    default: 30
  validate_certs:
    description: Validate the RouterOS TLS certificate.
    type: bool
    default: true
requirements:
  - Python 3.
  - RouterOS 7.x with REST API enabled.
  - Ansible 2.16 or newer.
attributes:
  check_mode:
    description: Does not execute traceroute in check mode.
    support: partial
'''


EXAMPLES = r'''
---
- name: Trace a remote endpoint
  mikrotik.routeros_rest.traceroute:
    host: https://router.example.test
    username: admin
    password: secret
    address: 198.51.100.20
  register: trace_result
'''
RETURN = r'''
result:
  description: RouterOS traceroute response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "address": {"type": "str", "required": True}, "max_hops": {"type": "int", "default": 30}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    if p["max_hops"] < 1: module.fail_json(msg="max_hops must be at least 1")
    if module.check_mode: module.exit_json(changed=False, skipped=True)
    try:
        result = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]).post("tool/traceroute", {"address": p["address"], "max-hops": str(p["max_hops"])})
        module.exit_json(changed=False, result=result)
    except RouterOSRestError as exc: module.fail_json(msg=str(exc))

if __name__ == "__main__":
    main()

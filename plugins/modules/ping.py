#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: ping
short_description: Run a RouterOS ping test
description:
  - Runs an ICMP ping test through the RouterOS REST API and returns the RouterOS result.
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
    description: Hostname or IP address to test.
    type: str
    required: true
  count:
    description: Number of echo requests.
    type: int
    default: 5
  size:
    description: ICMP payload size in bytes.
    type: int
    default: 56
  interface:
    description: Optional source interface.
    type: str
  src_address:
    description: Optional source address.
    type: str
  validate_certs:
    description: Validate the RouterOS TLS certificate.
    type: bool
    default: true
  timeout:
    description: HTTP timeout in seconds.
    type: int
    default: 30
requirements:
  - Python 3.
  - RouterOS 7.x with REST API enabled.
  - Ansible 2.16 or newer.
attributes:
  check_mode:
    description: Does not execute the ping in check mode.
    support: partial
'''


EXAMPLES = r'''
---
- name: Ping the default gateway
  mikrotik.routeros_rest.ping:
    host: https://router.example.test
    username: admin
    password: secret
    address: 192.0.2.1
    count: 10
  register: ping_result
'''
RETURN = r'''
result:
  description: RouterOS ping response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "address": {"type": "str", "required": True}, "count": {"type": "int", "default": 5}, "size": {"type": "int", "default": 56}, "interface": {"type": "str"}, "src_address": {"type": "str"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    if p["count"] < 1 or p["size"] < 0:
        module.fail_json(msg="count must be at least 1 and size cannot be negative")
    if module.check_mode:
        module.exit_json(changed=False, skipped=True)
    payload = {"address": p["address"], "count": str(p["count"]), "size": str(p["size"])}
    if p.get("interface"): payload["interface"] = p["interface"]
    if p.get("src_address"): payload["src-address"] = p["src_address"]
    try:
        result = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]).post("ping", payload)
        module.exit_json(changed=False, result=result)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

if __name__ == "__main__":
    main()

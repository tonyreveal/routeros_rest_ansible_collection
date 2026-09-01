#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: ip_scan
short_description: Run a RouterOS IP scan
description:
  - Runs the RouterOS IP scan tool through the REST API and returns discovered hosts.
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
  interface:
    description: Interface on which to scan.
    type: str
    required: true
  address_range:
    description: Optional IPv4 range to scan.
    type: str
  duration:
    description: Scan duration in seconds.
    type: int
    default: 10
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
    description: Does not execute the scan in check mode.
    support: partial
'''


EXAMPLES = r'''
---
- name: Scan the LAN
  mikrotik.routeros_rest.ip_scan:
    host: https://router.example.test
    username: admin
    password: secret
    interface: bridge-lan
    address_range: 192.0.2.0/24
  register: scan_result
'''
RETURN = r'''
result:
  description: RouterOS IP scan response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "interface": {"type": "str", "required": True}, "address_range": {"type": "str"}, "duration": {"type": "int", "default": 10}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    if p["duration"] < 1: module.fail_json(msg="duration must be at least 1")
    if module.check_mode: module.exit_json(changed=False, skipped=True)
    payload = {"interface": p["interface"], "duration": str(p["duration"])}
    if p.get("address_range"): payload["address-range"] = p["address_range"]
    try:
        result = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]).post("tool/ip-scan", payload)
        module.exit_json(changed=False, result=result)
    except RouterOSRestError as exc: module.fail_json(msg=str(exc))

if __name__ == "__main__":
    main()

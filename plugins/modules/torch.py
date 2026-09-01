#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.tool import run_tool

DOCUMENTATION = r'''
---
module: torch
short_description: Run the RouterOS Torch traffic monitor
description:
  - Runs the RouterOS Torch tool through the REST API for an interface.
  - This is an operational action; state and persistent idempotency are not applicable.
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
    description: Interface to monitor.
    type: str
    required: true
  duration:
    description: Capture duration in seconds.
    type: int
    default: 10
  filter:
    description: Optional Torch filter expression.
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
    description: Does not execute Torch in check mode.
    support: partial
'''
EXAMPLES = r'''
---
- name: Capture WAN flows
  mikrotik.routeros_rest.torch:
    host: https://router.example.test
    username: admin
    password: secret
    interface: ether1
    duration: 15
  register: torch_result
'''
RETURN = r'''
result:
  description: RouterOS Torch response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "interface": {"type": "str", "required": True}, "duration": {"type": "int", "default": 10}, "filter": {"type": "str"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    if p["duration"] < 1: module.fail_json(msg="duration must be at least 1")
    payload = {"interface": p["interface"], "duration": str(p["duration"])}
    if p.get("filter"): payload["filter"] = p["filter"]
    run_tool(module, "tool/torch", payload)
if __name__ == "__main__": main()

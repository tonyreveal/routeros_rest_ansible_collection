#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.tool import run_tool

DOCUMENTATION = r'''
---
module: netwatch_test
short_description: Run a RouterOS Netwatch probe
description:
  - Tests reachability of a host through the RouterOS REST API.
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
  address:
    description: IPv4 or IPv6 address to test.
    type: str
    required: true
  timeout:
    description: Probe timeout in seconds.
    type: int
    default: 1
  interval:
    description: Probe interval in seconds.
    type: int
    default: 10
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
    description: Does not execute the probe in check mode.
    support: partial
'''
EXAMPLES = r'''
---
- name: Test an upstream host
  mikrotik.routeros_rest.netwatch_test:
    host: https://router.example.test
    username: admin
    password: secret
    address: 198.51.100.1
  register: netwatch
'''
RETURN = r'''
result:
  description: RouterOS Netwatch probe response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "address": {"type": "str", "required": True}, "timeout": {"type": "int", "default": 1}, "interval": {"type": "int", "default": 10}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    run_tool(module, "tool/netwatch", {"host": p["address"], "timeout": str(p["timeout"]), "interval": str(p["interval"])})
if __name__ == "__main__": main()

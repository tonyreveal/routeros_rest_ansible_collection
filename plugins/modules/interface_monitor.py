#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.tool import run_tool

DOCUMENTATION = r'''
---
module: interface_monitor
short_description: Monitor a RouterOS interface
description:
  - Collects live interface monitoring data through the RouterOS REST API.
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
    description: Monitoring duration in seconds.
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
    description: Does not monitor an interface in check mode.
    support: partial
'''
EXAMPLES = r'''
---
- name: Monitor an interface
  mikrotik.routeros_rest.interface_monitor:
    host: https://router.example.test
    username: admin
    password: secret
    interface: ether1
    duration: 20
  register: interface_stats
'''
RETURN = r'''
result:
  description: RouterOS interface monitoring response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "interface": {"type": "str", "required": True}, "duration": {"type": "int", "default": 10}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    if p["duration"] < 1: module.fail_json(msg="duration must be at least 1")
    run_tool(module, "interface/monitor-traffic", {"interface": p["interface"], "duration": str(p["duration"])})
if __name__ == "__main__": main()

#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: traffic_monitor
short_description: Collect RouterOS interface traffic statistics
description:
  - Collects interface traffic statistics through the RouterOS REST API.
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
    description: Does not collect traffic in check mode.
    support: partial
'''


EXAMPLES = r'''
---
- name: Monitor WAN traffic
  mikrotik.routeros_rest.traffic_monitor:
    host: https://router.example.test
    username: admin
    password: secret
    interface: ether1
    duration: 30
  register: traffic
'''
RETURN = r'''
result:
  description: RouterOS traffic-monitor response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "interface": {"type": "str", "required": True}, "duration": {"type": "int", "default": 10}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    if p["duration"] < 1: module.fail_json(msg="duration must be at least 1")
    if module.check_mode: module.exit_json(changed=False, skipped=True)
    try:
        result = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]).post("interface/monitor-traffic", {"interface": p["interface"], "duration": str(p["duration"])})
        module.exit_json(changed=False, result=result)
    except RouterOSRestError as exc: module.fail_json(msg=str(exc))

if __name__ == "__main__":
    main()

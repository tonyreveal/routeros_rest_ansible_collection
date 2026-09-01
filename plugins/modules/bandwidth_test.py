#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.tool import run_tool

DOCUMENTATION = r'''
---
module: bandwidth_test
short_description: Run a RouterOS bandwidth test
description:
  - Runs the RouterOS bandwidth-test tool through the REST API.
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
    description: Remote RouterOS address.
    type: str
    required: true
  direction:
    description: Test direction.
    type: str
    choices:
      - receive
      - transmit
      - both
    default: both
  duration:
    description: Test duration in seconds.
    type: int
    default: 10
  protocol:
    description: Test protocol.
    type: str
    choices:
      - tcp
      - udp
    default: tcp
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
    description: Does not execute the test in check mode.
    support: partial
'''


EXAMPLES = r'''
---
- name: Test bandwidth to a remote router
  mikrotik.routeros_rest.bandwidth_test:
    host: https://router.example.test
    username: admin
    password: secret
    address: 198.51.100.2
    duration: 30
  register: bandwidth
'''
RETURN = r'''
result:
  description: RouterOS bandwidth-test response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "address": {"type": "str", "required": True}, "direction": {"type": "str", "choices": ["receive", "transmit", "both"], "default": "both"}, "duration": {"type": "int", "default": 10}, "protocol": {"type": "str", "choices": ["tcp", "udp"], "default": "tcp"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    if p["duration"] < 1: module.fail_json(msg="duration must be at least 1")
    run_tool(module, "tool/bandwidth-test", {"address": p["address"], "direction": p["direction"], "duration": str(p["duration"]), "protocol": p["protocol"]})
if __name__ == "__main__": main()

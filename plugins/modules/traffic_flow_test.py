#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.tool import run_tool

DOCUMENTATION = r'''
---
module: traffic_flow_test
short_description: Test RouterOS traffic-flow export
description:
  - Tests traffic-flow export processing through the RouterOS REST API.
  - This is an operational action; persistent state and idempotency are not applicable.
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
  settings:
    description: Traffic-flow test properties.
    type: dict
    required: true
    suboptions:
      interface:
        description: Interface whose traffic is tested.
        type: str
      target:
        description: Traffic-flow target address.
        type: str
      port:
        description: Traffic-flow target port.
        type: int
      protocol:
        description: Export protocol.
        type: str
      duration:
        description: Test duration in seconds.
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
    description: Does not execute a traffic-flow test in check mode.
    support: partial
'''


EXAMPLES = r'''
---
- name: Test traffic-flow export
  mikrotik.routeros_rest.traffic_flow_test:
    host: https://router.example.test
    username: admin
    password: secret
    settings:
      interface: ether1
      target: 198.51.100.20
      port: 2055
      duration: 10
  register: flow_test
'''
RETURN = r'''
result:
  description: RouterOS traffic-flow test response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "settings": {"type": "dict", "required": True}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    run_tool(module, "ip/traffic-flow/test", module.params["settings"])
if __name__ == "__main__": main()

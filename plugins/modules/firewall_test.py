#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.tool import run_tool

DOCUMENTATION = r'''
---
module: firewall_test
short_description: Run a RouterOS firewall packet test
description:
  - Tests how a packet is processed by RouterOS firewall rules through the REST API.
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
    description: Packet-test properties.
    type: dict
    required: true
    suboptions:
      chain:
        description: Firewall chain to test.
        type: str
        required: true
      protocol:
        description: IP protocol.
        type: str
      src_address:
        description: Source address.
        type: str
      dst_address:
        description: Destination address.
        type: str
      src_port:
        description: Source port.
        type: str
      dst_port:
        description: Destination port.
        type: str
      interface:
        description: Input or output interface.
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
    description: Does not execute the firewall test in check mode.
    support: partial
'''


EXAMPLES = r'''
---
- name: Test a forward packet
  mikrotik.routeros_rest.firewall_test:
    host: https://router.example.test
    username: admin
    password: secret
    settings:
      chain: forward
      protocol: tcp
      src_address: 192.0.2.10
      dst_address: 198.51.100.10
      dst_port: '443'
  register: firewall_test
'''
RETURN = r'''
result:
  description: RouterOS firewall-test response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "settings": {"type": "dict", "required": True}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    settings = {key.replace("_", "-"): value for key, value in module.params["settings"].items()}
    run_tool(module, "ip/firewall/connection/print", settings)
if __name__ == "__main__": main()

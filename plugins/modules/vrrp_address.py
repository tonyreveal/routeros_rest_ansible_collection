#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: vrrp_address
short_description: Manage an address assigned to a VRRP interface
description:
  - Creates, updates, or removes an IP address assigned to a VRRP interface through the RouterOS REST API.
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
    description: IPv4 or IPv6 address with prefix length.
    type: str
    required: true
  interface:
    description: VRRP interface receiving the address.
    type: str
    required: true
  network:
    description: Optional network address.
    type: str
  state:
    description: Desired address state.
    type: str
    choices:
      - present
      - absent
    default: present
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
    description: Supports check mode without changing the device.
    support: full
'''


EXAMPLES = r'''
---
- name: Assign the VRRP virtual address
  mikrotik.routeros_rest.vrrp_address:
    host: https://router.example.test
    username: admin
    password: secret
    address: 192.0.2.1/24
    interface: vrrp1
'''
RETURN = r'''
address:
  description: VRRP address record returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True},
        "password": {"type": "str", "required": True, "no_log": True}, "address": {"type": "str", "required": True},
        "interface": {"type": "str", "required": True}, "network": {"type": "str"},
        "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
        "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    values = {"address": p["address"], "interface": p["interface"]}
    if p.get("network") is not None:
        values["network"] = p["network"]
    run_config(module, "ip/address", {"address": p["address"], "interface": p["interface"]}, values)

if __name__ == "__main__":
    main()

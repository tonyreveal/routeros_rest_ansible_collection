#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: ipv6_address_list
short_description: Manage IPv6 firewall address-list entries
description:
  - Creates, updates, or removes an IPv6 firewall address-list entry through the RouterOS REST API.
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
    description: IPv6 address or prefix to place in the list.
    type: str
    required: true
  list:
    description: Address-list name.
    type: str
    required: true
  comment:
    description: Optional comment.
    type: str
  state:
    description: Desired entry state.
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
- name: Add an IPv6 address-list entry
  mikrotik.routeros_rest.ipv6_address_list:
    host: https://router.example.test
    username: admin
    password: secret
    address: 2001:db8:100::/64
    list: trusted-v6
    comment: Trusted network
'''

RETURN = r'''
entry:
  description: The resulting IPv6 address-list entry.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True},
        "password": {"type": "str", "required": True, "no_log": True}, "address": {"type": "str", "required": True},
        "list": {"type": "str", "required": True}, "comment": {"type": "str"},
        "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
        "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    run_config(module, "ipv6/firewall/address-list", {"list": p["list"], "address": p["address"]},
               {"list": p["list"], "address": p["address"], **({"comment": p["comment"]} if p.get("comment") is not None else {})})


if __name__ == "__main__":
    main()

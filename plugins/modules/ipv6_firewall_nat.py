#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: ipv6_firewall_nat
short_description: Manage IPv6 firewall NAT rules
description:
  - Creates, updates, or removes IPv6 firewall NAT rules through the RouterOS REST API.
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
  chain:
    description: NAT chain name.
    type: str
    required: true
  settings:
    description: IPv6 NAT rule properties.
    type: dict
    required: true
    suboptions:
      action:
        description: NAT action.
        type: str
        required: true
      src_address:
        description: Source IPv6 address or prefix.
        type: str
      dst_address:
        description: Destination IPv6 address or prefix.
        type: str
      protocol:
        description: IP protocol.
        type: str
      src_port:
        description: Source port or range.
        type: str
      dst_port:
        description: Destination port or range.
        type: str
      to_address:
        description: Translation IPv6 address.
        type: str
      to_ports:
        description: Translation port or range.
        type: str
      comment:
        description: Optional comment.
        type: str
      disabled:
        description: Whether the rule is disabled.
        type: bool
  state:
    description: Desired rule state.
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
- name: Add an IPv6 destination NAT rule
  mikrotik.routeros_rest.ipv6_firewall_nat:
    host: https://router.example.test
    username: admin
    password: secret
    chain: dstnat
    settings:
      action: dst-nat
      protocol: tcp
      dst_port: '443'
      to_address: 2001:db8::10
      to_ports: '8443'
'''
RETURN = r'''
rule:
  description: IPv6 NAT rule returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "chain": {"type": "str", "required": True}, "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "ipv6/firewall/nat", {"chain": p["chain"], **settings}, {"chain": p["chain"], **settings})

if __name__ == "__main__":
    main()

#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: snmp_trap_target
short_description: Manage RouterOS SNMP trap targets through the REST API
description:
  - Creates, updates, or removes an SNMP trap target.
  - The settings dictionary contains RouterOS trap target properties.
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
  name:
    description: Trap target name or destination identity.
    type: str
    required: true
  settings:
    description: RouterOS SNMP trap target properties.
    type: dict
    required: true
    suboptions:
      address:
        description: Trap receiver address.
        type: str
      port:
        description: Trap receiver port.
        type: int
      version:
        description: SNMP trap version.
        type: str
      community:
        description: SNMP trap community.
        type: str
      disabled:
        description: Whether the target is disabled.
        type: bool
  state:
    description: Desired target state.
    type: str
    choices: [present, absent]
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
"""


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True},
        "username": {"type": "str", "required": True},
        "password": {"type": "str", "required": True, "no_log": True},
        "name": {"type": "str", "required": True},
        "settings": {"type": "dict", "required": True},
        "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
        "validate_certs": {"type": "bool", "default": True},
        "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    run_config(module, "snmp/trap-target", {"name": p["name"]}, {"name": p["name"], **p["settings"]})

if __name__ == "__main__":
    main()

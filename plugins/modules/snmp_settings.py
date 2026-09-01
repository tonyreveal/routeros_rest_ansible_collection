#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: snmp_settings
short_description: Manage global RouterOS SNMP settings through the REST API
description:
  - Reconciles the global RouterOS SNMP service settings.
  - The settings dictionary contains properties of the SNMP singleton.
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
    description: Global RouterOS SNMP properties.
    type: dict
    required: true
    suboptions:
      enabled:
        description: Whether the SNMP service is enabled.
        type: bool
      contact:
        description: SNMP system contact.
        type: str
      location:
        description: SNMP system location.
        type: str
      engine_id:
        description: SNMP engine identifier.
        type: str
      trap_community:
        description: Default SNMP trap community.
        type: str
      trap_version:
        description: SNMP trap version.
        type: str
  state:
    description: Desired settings state.
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
        "settings": {"type": "dict", "required": True},
        "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
        "validate_certs": {"type": "bool", "default": True},
        "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    settings = {key.replace("_", "-"): value for key, value in module.params["settings"].items()}
    run_config(module, "snmp", {}, settings)

if __name__ == "__main__":
    main()

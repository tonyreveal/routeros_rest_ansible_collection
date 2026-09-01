#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: traffic_flow_settings
short_description: Manage global RouterOS traffic-flow settings through the REST API
description:
  - Reconciles the global RouterOS traffic-flow settings.
  - The settings dictionary contains properties of the traffic-flow singleton.
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
    description: Global RouterOS traffic-flow properties.
    type: dict
    required: true
    suboptions:
      enabled:
        description: Whether traffic-flow collection is enabled.
        type: bool
      interfaces:
        description: Interfaces included in flow collection.
        type: list
        elements: str
      active_flow_timeout:
        description: Active flow timeout.
        type: str
      inactive_flow_timeout:
        description: Inactive flow timeout.
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
    run_config(module, "ip/traffic-flow", {}, settings)

if __name__ == "__main__":
    main()

#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: pppoe_server
short_description: Manage RouterOS PPPoE server entries through the REST API
description:
  - Creates, updates, or removes a PPPoE server entry.
  - The settings dictionary contains RouterOS PPPoE server properties.
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
    description: PPPoE server service name.
    type: str
    required: true
  settings:
    description: RouterOS PPPoE server properties.
    type: dict
    required: true
    suboptions:
      interface:
        description: Interface on which the server listens.
        type: str
      service_name:
        description: PPPoE service name.
        type: str
      default_profile:
        description: Default PPP profile.
        type: str
      one_session_per_host:
        description: Whether one session per host is allowed.
        type: bool
      disabled:
        description: Whether the server is disabled.
        type: bool
  state:
    description: Desired server state.
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
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "interface/pppoe-server/server", {"service-name": p["name"]}, {"service-name": p["name"], **settings})

if __name__ == "__main__":
    main()

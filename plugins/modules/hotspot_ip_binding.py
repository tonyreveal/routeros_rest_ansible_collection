#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: hotspot_ip_binding
short_description: Manage RouterOS HotSpot IP bindings
description:
  - Creates, updates, or removes HotSpot IP bindings through the RouterOS REST API.
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
  mac_address:
    description: Client MAC address identifying the binding.
    type: str
    required: true
  settings:
    description: HotSpot IP binding properties.
    type: dict
    required: true
    suboptions:
      address:
        description: Client IP address.
        type: str
      to_address:
        description: Translated client IP address.
        type: str
      server:
        description: HotSpot server name.
        type: str
      type:
        description: Binding type such as regular, bypassed, or blocked.
        type: str
      comment:
        description: Optional comment.
        type: str
      disabled:
        description: Whether the binding is disabled.
        type: bool
  state:
    description: Desired binding state.
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
- name: Bypass HotSpot authentication for a device
  mikrotik.routeros_rest.hotspot_ip_binding:
    host: https://router.example.test
    username: admin
    password: secret
    mac_address: AA:BB:CC:DD:EE:FF
    settings:
      type: bypassed
      address: 192.0.2.50
'''
RETURN = r'''
binding:
  description: HotSpot IP binding returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True},
        "mac_address": {"type": "str", "required": True}, "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
        "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "ip/hotspot/ip-binding", {"mac-address": p["mac_address"]}, {"mac-address": p["mac_address"], **settings})

if __name__ == "__main__":
    main()

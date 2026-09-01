#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: hotspot_user
short_description: Manage a RouterOS HotSpot user
description:
  - Creates, updates, or removes a HotSpot user through the RouterOS REST API.
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
    description: HotSpot username.
    type: str
    required: true
  settings:
    description: HotSpot user properties.
    type: dict
    required: true
    suboptions:
      password:
        description: HotSpot user password.
        type: str
        no_log: true
      profile:
        description: HotSpot user profile.
        type: str
      limit_uptime:
        description: Maximum allowed session time.
        type: str
      server:
        description: HotSpot server name.
        type: str
      address:
        description: Optional client address.
        type: str
      disabled:
        description: Whether the user is disabled.
        type: bool
  state:
    description: Desired user state.
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
- name: Create a HotSpot user
  mikrotik.routeros_rest.hotspot_user:
    host: https://router.example.test
    username: admin
    password: secret
    name: guest1
    settings:
      password: guest-password
      profile: default
'''
RETURN = r'''
user:
  description: HotSpot user record returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True},
        "password": {"type": "str", "required": True, "no_log": True}, "name": {"type": "str", "required": True},
        "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
        "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "ip/hotspot/user", {"name": p["name"]}, {"name": p["name"], **settings})

if __name__ == "__main__":
    main()

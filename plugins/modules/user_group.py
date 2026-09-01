#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: user_group
short_description: Manage RouterOS user groups
description:
  - Creates, updates, or removes RouterOS user groups through the REST API.
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
    description: User group name.
    type: str
    required: true
  settings:
    description: User group properties.
    type: dict
    required: true
    suboptions:
      policy:
        description: Permissions assigned to the group.
        type: list
        elements: str
      skin:
        description: User-interface skin.
        type: str
      comment:
        description: Optional comment.
        type: str
  state:
    description: Desired group state.
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
- name: Create a restricted user group
  mikrotik.routeros_rest.user_group:
    host: https://router.example.test
    username: admin
    password: secret
    name: operators
    settings:
      policy:
        - read
        - write
'''
RETURN = r'''
group:
  description: User group record returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True},
        "name": {"type": "str", "required": True}, "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
        "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    run_config(module, "user/group", {"name": p["name"]}, {"name": p["name"], **p["settings"]})

if __name__ == "__main__":
    main()

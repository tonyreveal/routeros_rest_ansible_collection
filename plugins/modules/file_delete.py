#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: file_delete
short_description: Manage a RouterOS file
description:
  - Ensures a named RouterOS file is present or absent through the REST API.
  - File creation requires a separate upload mechanism; this module is intended primarily for idempotent file removal.
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
    description: RouterOS file name.
    type: str
    required: true
  state:
    description: Desired file state. Present verifies the file exists; absent removes it.
    type: str
    choices:
      - present
      - absent
    default: absent
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
- name: Remove an obsolete RouterOS file
  mikrotik.routeros_rest.file_delete:
    host: https://router.example.test
    username: admin
    password: secret
    name: old-export.rsc
    state: absent
'''
RETURN = r'''
file:
  description: RouterOS file record returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "name": {"type": "str", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "absent"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    run_config(module, "file", {"name": p["name"]}, {"name": p["name"]})

if __name__ == "__main__":
    main()

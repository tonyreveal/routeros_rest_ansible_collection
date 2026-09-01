#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.tool import run_tool

DOCUMENTATION = r'''
---
module: file_copy
short_description: Copy a RouterOS file
description:
  - Copies a RouterOS file using the REST API.
  - This is an imperative operation and is not idempotent.
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
  source:
    description: Existing RouterOS file name.
    type: str
    required: true
  destination:
    description: Destination RouterOS file name.
    type: str
    required: true
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
    description: Does not perform the copy in check mode.
    support: full
'''


EXAMPLES = r'''
---
- name: Copy a RouterOS backup
  mikrotik.routeros_rest.file_copy:
    host: https://router.example.test
    username: admin
    password: secret
    source: backup.backup
    destination: backup-copy.backup
'''
RETURN = r'''
result:
  description: RouterOS REST command response.
  returned: always
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True},
        "username": {"type": "str", "required": True},
        "password": {"type": "str", "required": True, "no_log": True},
        "source": {"type": "str", "required": True},
        "destination": {"type": "str", "required": True},
        "validate_certs": {"type": "bool", "default": True},
        "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    run_tool(module, "file/copy", {"file": module.params["source"], "destination": module.params["destination"]})

if __name__ == "__main__":
    main()

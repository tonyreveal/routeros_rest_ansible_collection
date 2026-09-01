#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.tool import run_tool

DOCUMENTATION = r'''
---
module: script_run
short_description: Run a RouterOS script
description:
  - Runs an existing RouterOS script through the REST API.
  - Running a script is an imperative operation and is not idempotent.
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
    description: Existing script name.
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
    description: Does not run the script in check mode.
    support: full
'''
EXAMPLES = r'''
---
- name: Run a RouterOS maintenance script
  mikrotik.routeros_rest.script_run:
    host: https://router.example.test
    username: admin
    password: secret
    name: nightly-maintenance
'''
RETURN = r'''
result:
  description: RouterOS REST command response.
  returned: always
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True},
        "password": {"type": "str", "required": True, "no_log": True}, "name": {"type": "str", "required": True},
        "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    run_tool(module, "system/script/run", {"number": module.params["name"]})
if __name__ == "__main__":
    main()

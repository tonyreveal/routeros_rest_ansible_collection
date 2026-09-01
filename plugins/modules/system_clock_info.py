#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.info import run_info

DOCUMENTATION = r'''
---
module: system_clock_info
short_description: Gather RouterOS system clock settings
description:
  - Reads RouterOS system clock settings through the REST API.
  - Results are returned in the registered module result and are not Ansible facts.
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
    description: Optional resource filter.
    type: str
  object_id:
    description: Optional RouterOS internal object ID.
    type: str
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
- name: Read RouterOS system clock settings
  mikrotik.routeros_rest.system_clock_info:
    host: https://router.example.test
    username: admin
    password: secret
  register: clock
'''
RETURN = r'''
clock:
  description: RouterOS system clock settings.
  returned: always
  type: list
  elements: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True},
        "username": {"type": "str", "required": True},
        "password": {"type": "str", "required": True, "no_log": True},
        "name": {"type": "str"},
        "object_id": {"type": "str"},
        "validate_certs": {"type": "bool", "default": True},
        "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    run_info(module, "system/clock", "clock", "name")

if __name__ == "__main__":
    main()

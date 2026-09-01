#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: system_clock
short_description: Manage RouterOS clock settings
description:
  - Reconciles RouterOS time zone and clock settings through the REST API.
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
    description: RouterOS clock properties.
    type: dict
    required: true
    suboptions:
      time_zone_name:
        description: IANA or RouterOS time-zone name.
        type: str
      time_zone_autodetect:
        description: Whether the time zone is detected automatically.
        type: bool
      date:
        description: System date in RouterOS format.
        type: str
      time:
        description: System time in RouterOS format.
        type: str
  state:
    description: Desired clock configuration state.
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
- name: Configure the router time zone
  mikrotik.routeros_rest.system_clock:
    host: https://router.example.test
    username: admin
    password: secret
    settings:
      time_zone_name: America/Chicago
      time_zone_autodetect: false
'''
RETURN = r'''
clock:
  description: Clock record returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    settings = {key.replace("_", "-"): value for key, value in module.params["settings"].items()}
    run_config(module, "system/clock", {}, settings)

if __name__ == "__main__":
    main()

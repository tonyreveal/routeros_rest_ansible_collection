#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: wireless_access_list
short_description: Manage RouterOS wireless access-list entries
description:
  - Creates, updates, or removes wireless access-list entries through the RouterOS REST API.
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
    description: Client MAC address.
    type: str
    required: true
  settings:
    description: Wireless access-list properties.
    type: dict
    required: true
    suboptions:
      interface:
        description: Wireless interface to which the entry applies.
        type: str
      signal_range:
        description: Allowed signal range.
        type: str
      authentication:
        description: Whether authentication is required.
        type: bool
      forwarding:
        description: Whether forwarding is allowed.
        type: bool
      comment:
        description: Optional comment.
        type: str
      disabled:
        description: Whether the entry is disabled.
        type: bool
  state:
    description: Desired entry state.
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
- name: Permit a wireless client
  mikrotik.routeros_rest.wireless_access_list:
    host: https://router.example.test
    username: admin
    password: secret
    mac_address: AA:BB:CC:DD:EE:FF
    settings:
      authentication: true
      forwarding: true
'''
RETURN = r'''
entry:
  description: Wireless access-list record returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "mac_address": {"type": "str", "required": True}, "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "interface/wireless/access-list", {"mac-address": p["mac_address"]}, {"mac-address": p["mac_address"], **settings})

if __name__ == "__main__":
    main()

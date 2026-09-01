#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: wireless_security
short_description: Manage RouterOS wireless security profiles
description:
  - Creates, updates, or removes a wireless security profile through the RouterOS REST API.
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
    description: Security profile name.
    type: str
    required: true
  settings:
    description: Wireless security profile properties.
    type: dict
    required: true
    suboptions:
      mode:
        description: Security mode.
        type: str
      authentication_types:
        description: Allowed authentication types.
        type: list
        elements: str
      unicast_ciphers:
        description: Allowed unicast ciphers.
        type: list
        elements: str
      group_ciphers:
        description: Allowed group ciphers.
        type: list
        elements: str
      wpa_pre_shared_key:
        description: WPA pre-shared key.
        type: str
        no_log: true
      wpa2_pre_shared_key:
        description: WPA2 pre-shared key.
        type: str
        no_log: true
      management_protection:
        description: Management-frame protection mode.
        type: str
      supplicant_identity:
        description: Supplicant identity.
        type: str
  state:
    description: Desired profile state.
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
- name: Configure a WPA2 wireless security profile
  mikrotik.routeros_rest.wireless_security:
    host: https://router.example.test
    username: admin
    password: secret
    name: office-secure
    settings:
      mode: dynamic-keys
      authentication_types:
        - wpa2-psk
      wpa2_pre_shared_key: wireless-secret
'''
RETURN = r'''
profile:
  description: Wireless security profile returned after a change.
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
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "interface/wireless/security-profiles", {"name": p["name"]}, {"name": p["name"], **settings})

if __name__ == "__main__":
    main()

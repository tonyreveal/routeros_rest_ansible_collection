#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: lte
short_description: Manage RouterOS LTE interface settings
description:
  - Creates, updates, or removes a RouterOS LTE interface configuration through the REST API.
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
    description: LTE interface name.
    type: str
    required: true
  settings:
    description: LTE interface properties.
    type: dict
    required: true
    suboptions:
      disabled:
        description: Whether the interface is disabled.
        type: bool
      apn_profiles:
        description: APN profile name or list supported by the modem.
        type: str
      allow_roaming:
        description: Whether cellular roaming is allowed.
        type: bool
      network_mode:
        description: Preferred cellular network mode.
        type: str
      pin:
        description: SIM PIN.
        type: str
        no_log: true
      sms_read:
        description: Whether SMS read operations are enabled.
        type: bool
      sms_send:
        description: Whether SMS send operations are enabled.
        type: bool
      mtu:
        description: Interface MTU.
        type: int
  state:
    description: Desired interface state.
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
- name: Configure an LTE interface
  mikrotik.routeros_rest.lte:
    host: https://router.example.test
    username: admin
    password: secret
    name: lte1
    settings:
      allow_roaming: false
      network_mode: LTE
      mtu: 1500
'''
RETURN = r'''
interface:
  description: LTE interface record returned after a change.
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
    run_config(module, "interface/lte", {"name": p["name"]}, {"name": p["name"], **settings})

if __name__ == "__main__":
    main()

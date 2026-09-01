#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: certificate_generate
short_description: Generate a RouterOS certificate key pair
description:
  - Idempotently creates a RouterOS certificate request record with the supplied generation settings.
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
    description: Certificate name.
    type: str
    required: true
  settings:
    description: Certificate generation properties.
    type: dict
    required: true
    suboptions:
      common_name:
        description: Certificate common name.
        type: str
      key_size:
        description: Private-key size.
        type: int
      key_usage:
        description: Certificate key-usage values.
        type: list
        elements: str
      days_valid:
        description: Validity period in days.
        type: int
  state:
    description: Desired certificate request state.
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
- name: Generate a certificate request
  mikrotik.routeros_rest.certificate_generate:
    host: https://router.example.test
    username: admin
    password: secret
    name: router-cert
    settings:
      common_name: router.example.test
      key_size: 2048
      days_valid: 365
'''
RETURN = r'''
certificate:
  description: Certificate record returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "name": {"type": "str", "required": True}, "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "certificate", {"name": p["name"]}, {"name": p["name"], **settings})

if __name__ == "__main__":
    main()

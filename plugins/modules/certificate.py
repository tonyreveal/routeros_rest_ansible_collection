#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: certificate
short_description: Manage RouterOS certificates
description:
  - Creates, updates, or removes a RouterOS certificate record through the REST API.
  - Certificate signing and key material generation can be requested with settings supported by the target RouterOS release.
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
    description: RouterOS certificate properties.
    type: dict
    required: true
    suboptions:
      common_name:
        description: Certificate common name.
        type: str
      country:
        description: Country code.
        type: str
      state:
        description: State or province.
        type: str
      locality:
        description: Locality.
        type: str
      organization:
        description: Organization name.
        type: str
      key_usage:
        description: Certificate key-usage values.
        type: list
        elements: str
      days_valid:
        description: Certificate validity period in days.
        type: int
      trusted:
        description: Whether the certificate is trusted.
        type: bool
      disabled:
        description: Whether the certificate is disabled.
        type: bool
  state:
    description: Desired certificate state.
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
- name: Ensure a trusted certificate record exists
  mikrotik.routeros_rest.certificate:
    host: https://router.example.test
    username: admin
    password: secret
    name: router-cert
    settings:
      common_name: router.example.test
      trusted: true
'''
RETURN = r'''
certificate:
  description: Certificate record returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True},
        "password": {"type": "str", "required": True, "no_log": True}, "name": {"type": "str", "required": True},
        "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
        "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "certificate", {"name": p["name"]}, {"name": p["name"], **settings})

if __name__ == "__main__":
    main()

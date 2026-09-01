#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: radius_incoming
short_description: Manage RouterOS incoming RADIUS settings
description:
  - Reconciles the RouterOS incoming RADIUS service through the REST API.
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
    description: Incoming RADIUS properties.
    type: dict
    required: true
    suboptions:
      accept:
        description: Whether incoming RADIUS requests are accepted.
        type: bool
      port:
        description: UDP port for incoming RADIUS requests.
        type: int
      vrf:
        description: VRF used by the incoming RADIUS service.
        type: str
      secret:
        description: Shared secret for incoming requests.
        type: str
        no_log: true
  state:
    description: Desired incoming RADIUS state.
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
- name: Enable incoming RADIUS
  mikrotik.routeros_rest.radius_incoming:
    host: https://router.example.test
    username: admin
    password: secret
    settings:
      accept: true
      port: 3799
      secret: coa-secret
'''
RETURN = r'''
settings:
  description: Incoming RADIUS settings returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    run_config(module, "radius/incoming", {}, module.params["settings"])

if __name__ == "__main__":
    main()

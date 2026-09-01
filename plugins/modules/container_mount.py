#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: container_mount
short_description: Manage RouterOS container mounts
description:
  - Creates, updates, or removes a RouterOS container mount through the REST API.
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
    description: Mount name.
    type: str
    required: true
  settings:
    description: Container mount properties.
    type: dict
    required: true
    suboptions:
      src:
        description: Host storage path.
        type: str
        required: true
      dst:
        description: Container mount path.
        type: str
        required: true
      comment:
        description: Optional comment.
        type: str
  state:
    description: Desired mount state.
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
  - RouterOS 7.x with REST API and container support enabled.
  - Ansible 2.16 or newer.
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
'''
EXAMPLES = r'''
---
- name: Configure a container mount
  mikrotik.routeros_rest.container_mount:
    host: https://router.example.test
    username: admin
    password: secret
    name: dns-config
    settings:
      src: usb1/containers/dns
      dst: /etc/dns
'''
RETURN = r'''
mount:
  description: Container mount returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "name": {"type": "str", "required": True}, "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    run_config(module, "container/mounts", {"name": p["name"]}, {"name": p["name"], **p["settings"]})
if __name__ == "__main__": main()


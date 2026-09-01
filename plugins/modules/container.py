#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: container
short_description: Manage RouterOS containers
description:
  - Creates, updates, or removes a RouterOS container configuration through the REST API.
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
    description: Container name.
    type: str
    required: true
  settings:
    description: RouterOS container properties.
    type: dict
    required: true
    suboptions:
      remote_image:
        description: Container image URL or reference.
        type: str
      interface:
        description: Container interface name.
        type: str
      root_dir:
        description: Container root directory.
        type: str
      mounts:
        description: Container mount definitions.
        type: list
        elements: str
      envlist:
        description: Environment-list name.
        type: str
      logging:
        description: Whether container logging is enabled.
        type: bool
      start_on_boot:
        description: Whether the container starts on boot.
        type: bool
      disabled:
        description: Whether the container is disabled.
        type: bool
  state:
    description: Desired container state.
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
  - RouterOS 7.x with REST API enabled and container support enabled.
  - Ansible 2.16 or newer.
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
'''


EXAMPLES = r'''
---
- name: Configure a RouterOS container
  mikrotik.routeros_rest.container:
    host: https://router.example.test
    username: admin
    password: secret
    name: dns-container
    settings:
      remote_image: ghcr.io/example/dns:latest
      root_dir: usb1/containers/dns
      start_on_boot: true
'''
RETURN = r'''
container:
  description: Container record returned after a change.
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
    run_config(module, "container", {"name": p["name"]}, {"name": p["name"], **settings})

if __name__ == "__main__":
    main()

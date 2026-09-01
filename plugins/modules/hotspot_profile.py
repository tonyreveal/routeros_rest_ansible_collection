#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r'''
---
module: hotspot_profile
short_description: Manage RouterOS HotSpot profiles
description:
  - Creates, updates, or removes HotSpot user profiles through the RouterOS REST API.
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
    description: HotSpot profile name.
    type: str
    required: true
  settings:
    description: HotSpot profile properties.
    type: dict
    required: true
    suboptions:
      hotspot_address:
        description: HotSpot gateway address.
        type: str
      dns_name:
        description: DNS name presented to clients.
        type: str
      html_directory:
        description: HotSpot HTML directory.
        type: str
      login_by:
        description: Allowed login methods.
        type: list
        elements: str
      use_radius:
        description: Whether RADIUS authentication is used.
        type: bool
      rate_limit:
        description: Default client rate limit.
        type: str
      http_proxy:
        description: Whether the HotSpot HTTP proxy is enabled.
        type: bool
      smtp_server:
        description: SMTP server for redirected SMTP traffic.
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
- name: Configure a HotSpot profile
  mikrotik.routeros_rest.hotspot_profile:
    host: https://router.example.test
    username: admin
    password: secret
    name: office
    settings:
      hotspot_address: 192.0.2.1
      dns_name: hotspot.example.test
      login_by:
        - http-chap
        - https
      use_radius: true
'''
RETURN = r'''
profile:
  description: HotSpot profile record returned after a change.
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
    run_config(module, "ip/hotspot/profile", {"name": p["name"]}, {"name": p["name"], **settings})

if __name__ == "__main__":
    main()

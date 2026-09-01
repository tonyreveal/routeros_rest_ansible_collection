#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: wireguard
short_description: Manage RouterOS WireGuard interfaces through the REST API
description:
  - Creates, updates, or removes a WireGuard interface.
  - The settings dictionary contains RouterOS WireGuard properties.
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
    description: WireGuard interface name.
    type: str
    required: true
  settings:
    description: RouterOS WireGuard properties.
    type: dict
    required: true
    suboptions:
      listen_port:
        description: UDP listen port.
        type: int
      mtu:
        description: WireGuard interface MTU.
        type: int
      private_key:
        description: WireGuard private key.
        type: str
        no_log: true
      comment:
        description: Comment describing the interface.
        type: str
      disabled:
        description: Whether the interface is disabled.
        type: bool
  state:
    description: Desired interface state.
    type: str
    choices: [present, absent]
    default: present
  validate_certs:
    description: Validate the TLS certificate.
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
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.org/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
"""


RETURN = r"""
resource:
  description: Reconciled WireGuard interface.
  returned: always
  type: dict
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "settings": {"type": "dict", "required": True},
            "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "interface/wireguard", {"name": p["name"]}, {"name": p["name"], **settings})


if __name__ == "__main__":
    main()

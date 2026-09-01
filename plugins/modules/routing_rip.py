#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: routing_rip
short_description: Manage RouterOS RIP instances through the REST API
description:
  - Creates, updates, or removes a RouterOS RIP instance.
  - The settings dictionary contains RouterOS RIP instance properties.
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
    description: RIP instance name.
    type: str
    required: true
  settings:
    description: RouterOS RIP instance properties.
    type: dict
    required: true
    suboptions:
      vrf:
        description: VRF used by the RIP instance.
        type: str
      afi:
        description: Address family used by the instance.
        type: str
        choices: [ipv4, ipv6]
      redistribute:
        description: Route sources to redistribute.
        type: list
        elements: str
      in_filter_chain:
        description: Input routing filter chain.
        type: str
      out_filter_chain:
        description: Output routing filter chain.
        type: str
      disabled:
        description: Whether the RIP instance is disabled.
        type: bool
  state:
    description: Desired instance state.
    type: str
    choices: [present, absent]
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
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.org/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
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
    run_config(module, "routing/rip/instance", {"name": p["name"]}, {"name": p["name"], **settings})


if __name__ == "__main__":
    main()

#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: ipsec_profile
short_description: Manage RouterOS IPsec profiles through the REST API
description:
  - Creates, updates, or removes an IPsec profile.
  - The settings dictionary contains RouterOS IPsec profile properties.
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
    description: IPsec profile name.
    type: str
    required: true
  settings:
    description: RouterOS IPsec profile properties.
    type: dict
    required: true
    suboptions:
      hash_algorithm:
        description: IKE hash algorithms.
        type: list
        elements: str
      enc_algorithm:
        description: IKE encryption algorithms.
        type: list
        elements: str
      dh_group:
        description: Diffie-Hellman groups.
        type: list
        elements: str
      lifetime:
        description: IKE lifetime.
        type: str
  state:
    description: Desired profile state.
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
    run_config(module, "ip/ipsec/profile", {"name": p["name"]}, {"name": p["name"], **settings})


if __name__ == "__main__":
    main()

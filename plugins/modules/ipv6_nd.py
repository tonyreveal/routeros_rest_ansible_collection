#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: ipv6_nd
short_description: Manage RouterOS IPv6 Neighbor Discovery settings through the REST API
description:
  - Creates, updates, or removes IPv6 Neighbor Discovery settings.
  - The settings dictionary contains RouterOS Neighbor Discovery properties.
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
  interface:
    description: Interface identity for Neighbor Discovery.
    type: str
    required: true
  settings:
    description: RouterOS Neighbor Discovery properties.
    type: dict
    required: true
    suboptions:
      advertise_mac_address:
        description: Whether router advertisements include the MAC address.
        type: bool
      managed_address_configuration:
        description: Whether hosts should use stateful address configuration.
        type: bool
      other_configuration:
        description: Whether hosts should use stateful configuration for other information.
        type: bool
      ra_interval:
        description: Router advertisement interval.
        type: str
      ra_lifetime:
        description: Router advertisement lifetime.
        type: str
      ra_preference:
        description: Router advertisement preference.
        type: str
      dns:
        description: DNS server addresses advertised to hosts.
        type: list
        elements: str
  state:
    description: Desired resource state.
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


RETURN = r"""
resource:
  description: Reconciled Neighbor Discovery resource.
  returned: always
  type: dict
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "interface": {"type": "str", "required": True},
            "settings": {"type": "dict", "required": True},
            "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "ipv6/nd", {"interface": p["interface"]}, {"interface": p["interface"], **settings})


if __name__ == "__main__":
    main()

#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: dhcp_lease
short_description: Manage RouterOS DHCP leases through the REST API
description:
  - Creates, updates, or removes a DHCP lease.
  - The address identifies the lease and settings contains RouterOS lease properties.
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
  address:
    description: IPv4 address identifying the lease.
    type: str
    required: true
  settings:
    description: RouterOS DHCP lease properties.
    type: dict
    required: true
    suboptions:
      mac_address:
        description: Client MAC address.
        type: str
      server:
        description: DHCP server name serving the lease.
        type: str
      comment:
        description: Comment describing the lease.
        type: str
      client_id:
        description: DHCP client identifier.
        type: str
      host_name:
        description: Client host name.
        type: str
      disabled:
        description: Whether the lease is disabled.
        type: bool
      lease_time:
        description: Lease duration.
        type: str
  state:
    description: Desired lease state.
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
            "address": {"type": "str", "required": True},
            "settings": {"type": "dict", "required": True},
            "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "ip/dhcp-server/lease", {"address": p["address"]}, {"address": p["address"], **settings})


if __name__ == "__main__":
    main()


#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.resource import reconcile

DOCUMENTATION = r"""---
module: dhcp_client
short_description: Manage or gather RouterOS dhcp client information
description:
  - Reads or manages the corresponding RouterOS resource through the REST API.
  - Returns predictable structured data for use in an Ansible playbook.
version_added: '1.0.0'
author:
  - Tony Reveal (https://github.com/tonyreveal)
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
options:
  host:
    type: str
    required: true
  username:
    type: str
    required: true
  password:
    type: str
    required: true
    no_log: true
  interface:
    type: str
    required: true
  add_default_route:
    type: bool
    default: true
  default_route_distance:
    type: int
    default: 1
  use_peer_dns:
    type: bool
    default: true
  use_peer_ntp:
    type: bool
    default: true
  disabled:
    type: bool
    default: false
  state:
    type: str
    choices: [present, absent]
    default: present
  validate_certs:
    type: bool
    default: true
  timeout:
    type: int
    default: 30
requirements: [Python 3, RouterOS 7.x REST API, Ansible 2.16 or newer]
"""


def main():
    m = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "interface": {"type": "str", "required": True},
            "add_default_route": {"type": "bool", "default": True},
            "default_route_distance": {"type": "int", "default": 1},
            "use_peer_dns": {"type": "bool", "default": True},
            "use_peer_ntp": {"type": "bool", "default": True},
            "disabled": {"type": "bool", "default": False},
            "state": {"type": "str", "default": "present", "choices": ["present", "absent"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = m.params
    d = {
        "interface": p["interface"],
        "add-default-route": p["add_default_route"],
        "default-route-distance": p["default_route_distance"],
        "use-peer-dns": p["use_peer_dns"],
        "use-peer-ntp": p["use_peer_ntp"],
        "disabled": p["disabled"],
    }
    try:
        reconcile(
            m,
            RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]),
            "ip/dhcp-client",
            {"interface": p["interface"]},
            d,
            p["state"],
            "client",
        )
    except RouterOSRestError as e:
        m.fail_json(msg=str(e))


if __name__ == "__main__":
    main()


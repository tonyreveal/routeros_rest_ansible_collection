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
module: ospf
short_description: Manage RouterOS OSPF instances through the REST API
description:
  - Creates, updates, or removes an OSPF instance.
  - The instance dictionary contains RouterOS OSPF instance properties.
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
    description: OSPF instance name.
    type: str
    required: true
  instance:
    description: RouterOS OSPF instance properties.
    type: dict
    required: true
    suboptions:
      router_id:
        description: OSPF router ID.
        type: str
      version:
        description: OSPF version.
        type: str
        choices: [2, 3]
      redistribute:
        description: Route sources to redistribute.
        type: list
        elements: str
      in_filter:
        description: Input routing filter chain.
        type: str
      out_filter:
        description: Output routing filter chain.
        type: str
      disabled:
        description: Whether the OSPF instance is disabled.
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
"""


def main():
    m = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "instance": {
                "type": "dict",
                "required": True,
                "options": {
                    "router_id": {"type": "str"},
                    "version": {"type": "str", "choices": ["2", "3"]},
                    "redistribute": {"type": "list", "elements": "str"},
                    "in_filter": {"type": "str"},
                    "out_filter": {"type": "str"},
                    "disabled": {"type": "bool"},
                },
            },
            "state": {"type": "str", "default": "present", "choices": ["present", "absent"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = m.params
    instance = {key.replace("_", "-"): value for key, value in p["instance"].items()}
    d = {"name": p["name"], **instance}
    try:
        reconcile(
            m,
            RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]),
            "routing/ospf/instance",
            {"name": p["name"]},
            d,
            p["state"],
            "instance",
        )
    except RouterOSRestError as e:
        m.fail_json(msg=str(e))


if __name__ == "__main__":
    main()

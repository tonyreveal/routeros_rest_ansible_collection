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
module: bgp
short_description: Manage RouterOS BGP templates through the REST API
description:
  - Creates, updates, or removes a BGP template.
  - The template dictionary contains RouterOS BGP template properties.
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
  name:
    type: str
    required: true
  template:
    description:
      - RouterOS BGP template properties.
      - These fields are sent directly to the RouterOS REST API.
    type: dict
    required: true
    suboptions:
      as:
        description: Local autonomous system number.
        type: int
      router_id:
        description: Router ID used by the BGP template.
        type: str
      routing_table:
        description: Routing table used for BGP routes.
        type: str
      redistribute:
        description: Route sources to redistribute into BGP.
        type: list
        elements: str
      input:
        description: Input routing filter chain.
        type: str
      output:
        description: Output routing filter chain.
        type: str
      disabled:
        description: Whether the BGP template is disabled.
        type: bool
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
            "template": {
                "type": "dict",
                "required": True,
                "options": {
                    "as": {"type": "int"},
                    "router_id": {"type": "str"},
                    "routing_table": {"type": "str"},
                    "redistribute": {"type": "list", "elements": "str"},
                    "input": {"type": "str"},
                    "output": {"type": "str"},
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
    template = {key.replace("_", "-"): value for key, value in p["template"].items()}
    d = {"name": p["name"], **template}
    try:
        reconcile(
            m,
            RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]),
            "routing/bgp/template",
            {"name": p["name"]},
            d,
            p["state"],
            "template",
        )
    except RouterOSRestError as e:
        m.fail_json(msg=str(e))


if __name__ == "__main__":
    main()

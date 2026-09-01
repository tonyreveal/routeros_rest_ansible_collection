#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r"""
---
module: bond_info
short_description: Manage or gather RouterOS bond info information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Reads configured and dynamic bonding interface records from /interface/bonding.
  - Without a selector, returns all bonding interfaces.
  - A name or bond_id selector returns only the matching bonding interface.
  - Returns data directly in the registered module result.
  - The module is read-only and does not create Ansible facts.
version_added: 1.0.0
author:
  - Tony Reveal (https://github.com/tonyreveal)
options:
  host:
    description:
      - RouterOS REST base URL, such as https://192.0.2.1.
      - The module appends /rest when it is not already present.
    type: str
    required: true
  username:
    description:
      - RouterOS user for HTTP Basic Authentication.
    type: str
    required: true
  password:
    description:
      - RouterOS password for HTTP Basic Authentication.
    type: str
    required: true
    no_log: true
  validate_certs:
    description:
      - Validate the TLS certificate presented by the RouterOS www-ssl service.
    type: bool
    default: true
  timeout:
    description:
      - HTTP request timeout in seconds.
    type: int
    default: 30
  name:
    description:
      - Return only the bonding interface with this RouterOS name.
    type: str
  bond_id:
    description:
      - Return only the bonding interface with this RouterOS internal ID, such as '*1'.
    type: str
notes:
  - Use HTTPS and validate_certs=true in production.
  - The REST API requires the www-ssl or www service to be enabled on RouterOS.
  - RouterOS REST API values are commonly returned as strings and are preserved by this module.
requirements:
  - Python 3
  - RouterOS 7.x with REST API enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Gather all RouterOS bonding interfaces
  mikrotik.routeros.bond_info:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
  register: all_bond_result

- name: Gather one bond by name
  mikrotik.routeros.bond_info:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    name: bond-uplink
  register: bond_result

- name: Display bonding interfaces
  ansible.builtin.debug:
    var: bond_result.bonds
...
"""


RETURN = r"""
bonds:
  description: Records returned by the RouterOS /interface/bonding REST endpoint.
  returned: always
  type: list
  elements: dict
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
            "name": {"type": "str"},
            "bond_id": {"type": "str"},
        },
        mutually_exclusive=[["name", "bond_id"]],
        supports_check_mode=True,
    )

    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")

    client = RouterOSRestClient(
        host=params["host"],
        username=params["username"],
        password=params["password"],
        timeout=params["timeout"],
        validate_certs=params["validate_certs"],
    )

    query = {}
    if params.get("name") is not None:
        query["name"] = params["name"]
    if params.get("bond_id") is not None:
        query[".id"] = params["bond_id"]

    try:
        bonds = client.get("interface/bonding", query=query)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    if not isinstance(bonds, list):
        bonds = [bonds]

    module.exit_json(changed=False, bonds=bonds)


if __name__ == "__main__":
    main()

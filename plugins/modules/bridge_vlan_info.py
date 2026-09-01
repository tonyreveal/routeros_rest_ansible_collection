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
module: bridge_vlan_info
short_description: Manage or gather RouterOS bridge vlan info information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Reads the RouterOS /interface/bridge/vlan table.
  - Without filters, returns all bridge VLAN table entries.
  - Filters can select a bridge by name or ID and can select a VLAN ID.
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
  bridge_name:
    description:
      - Return entries associated with this bridge name.
    type: str
  bridge_id:
    description:
      - Return entries associated with the bridge having this RouterOS internal ID.
    type: str
  vlan_id:
    description:
      - Return entries containing this VLAN ID.
    type: int
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
- name: Gather all bridge VLAN table entries
  mikrotik.routeros.bridge_vlan_info:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
  register: all_bridge_vlan_result

- name: Gather VLAN 100 entries from one bridge
  mikrotik.routeros.bridge_vlan_info:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    bridge_name: bridge-lan
    vlan_id: 100
  register: bridge_vlan_result

- name: Display bridge VLAN entries
  ansible.builtin.debug:
    var: bridge_vlan_result.bridge_vlans
...
"""


RETURN = r"""
bridge_vlans:
  description: Records returned by the RouterOS /interface/bridge/vlan REST endpoint.
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
            "bridge_name": {"type": "str"},
            "bridge_id": {"type": "str"},
            "vlan_id": {"type": "int"},
        },
        mutually_exclusive=[["bridge_name", "bridge_id"]],
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

    try:
        bridge_name = params.get("bridge_name")
        if params.get("bridge_id") is not None:
            bridges = client.get("interface/bridge", query={".id": params["bridge_id"]})
            if not isinstance(bridges, list):
                bridges = [bridges]
            if len(bridges) != 1 or not bridges[0].get("name"):
                module.fail_json(msg=f"No unique bridge found for bridge_id {params['bridge_id']}")
            bridge_name = bridges[0]["name"]

        query = {}
        if bridge_name is not None:
            query["bridge"] = bridge_name
        if params.get("vlan_id") is not None:
            query["vlan-ids"] = str(params["vlan_id"])
        bridge_vlans = client.get("interface/bridge/vlan", query=query)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    if not isinstance(bridge_vlans, list):
        bridge_vlans = [bridge_vlans]

    module.exit_json(changed=False, bridge_vlans=bridge_vlans)


if __name__ == "__main__":
    main()

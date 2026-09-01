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
module: bridge_info
short_description: Manage or gather RouterOS bridge info information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Reads defined RouterOS bridge interfaces through the RouterOS REST API.
  - Optionally reads bridge-port membership for each defined bridge.
  - Without a selector, returns all bridges; name or bridge_id selects one bridge.
  - Returns bridge data directly in the registered module result.
  - The module is read-only and does not change the RouterOS device.
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
      - HTTP request timeout in seconds for each REST API request.
    type: int
    default: 30
  include_ports:
    description:
      - Also gather records from /interface/bridge/port.
    type: bool
    default: true
  name:
    description:
      - Return only the bridge with this RouterOS name.
    type: str
    required: false
  bridge_id:
    description:
      - Return only the bridge with this RouterOS internal ID, such as '*1'.
    type: str
    required: false
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
- name: Gather RouterOS bridge information
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Collect bridges and bridge ports
      mikrotik.routeros.bridge_info:
        host: https://192.0.2.1
        username: "{{ vault_routeros_username }}"
        password: "{{ vault_routeros_password }}"
        validate_certs: true
        include_ports: true
        name: bridge-lan
      register: routeros_bridge_facts

    - name: Show defined bridges
      ansible.builtin.debug:
        var: routeros_bridge_facts.bridges
...
"""


RETURN = r"""
bridges:
  description: RouterOS bridge records returned by /interface/bridge.
  returned: always
  type: list
  elements: dict
ports:
  description: RouterOS bridge-port records, or an empty list when include_ports is false.
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
            "include_ports": {"type": "bool", "default": True},
            "name": {"type": "str"},
            "bridge_id": {"type": "str"},
        },
        mutually_exclusive=[["name", "bridge_id"]],
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
        query = {}
        if params.get("name") is not None:
            query["name"] = params["name"]
        if params.get("bridge_id") is not None:
            query[".id"] = params["bridge_id"]
        bridges = client.get("interface/bridge", query=query)
        port_query = {}
        if params.get("name") is not None:
            port_query["bridge"] = params["name"]
        elif params.get("bridge_id") is not None and isinstance(bridges, list) and len(bridges) == 1:
            bridge_name = bridges[0].get("name")
            if bridge_name:
                port_query["bridge"] = bridge_name
        ports = client.get("interface/bridge/port", query=port_query) if params["include_ports"] else []
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    if not isinstance(bridges, list):
        bridges = [bridges]
    if not isinstance(ports, list):
        ports = [ports]

    module.exit_json(
        changed=False,
        bridges=bridges,
        ports=ports,
    )


if __name__ == "__main__":
    main()

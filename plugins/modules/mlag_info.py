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
module: mlag_info
short_description: Manage or gather RouterOS mlag info information
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
description:
  - Returns MLAG-related bridge configuration and status information.
  - Omitting name returns all bridges; supplying name returns one bridge.
  - Results are returned directly in the registered module result, not as Ansible facts.
requirements:
  - Python 3
  - RouterOS 7.22 or newer
  - Ansible 2.16 or newer
options:
  host:
    description: RouterOS REST base URL.
    type: str
    required: true
  username:
    description: RouterOS user for HTTP Basic Authentication.
    type: str
    required: true
  password:
    description: RouterOS password for HTTP Basic Authentication.
    type: str
    required: true
    no_log: true
  name:
    description: Optional bridge name to query.
    type: str
  validate_certs:
    description: Validate the RouterOS TLS certificate.
    type: bool
    default: true
  timeout:
    description: HTTP request timeout in seconds.
    type: int
    default: 30
"""


EXAMPLES = r"""
---
- name: Gather MLAG information
  mikrotik.routeros_rest.mlag_info:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
  register: mlag_state

- name: Display MLAG state
  ansible.builtin.debug:
    var: mlag_state.bridges
...
"""


RETURN = r"""
bridges:
  description: Bridge records containing MLAG configuration and status fields.
  returned: success
  type: list
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
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
        records = client.get("interface/bridge", query={"name": params["name"]} if params.get("name") else None)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
    if not isinstance(records, list):
        records = [records]
    fields = {"name", "mlag-peer-port", "mlag-priority", "mlag-heartbeat", "mlag-state", "mlag-active-role"}
    bridges = [
        {key: value for key, value in record.items() if key in fields} for record in records if isinstance(record, dict)
    ]
    module.exit_json(changed=False, bridges=bridges)


if __name__ == "__main__":
    main()

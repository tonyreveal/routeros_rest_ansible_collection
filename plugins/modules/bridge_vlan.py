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
module: bridge_vlan
short_description: Manage or gather RouterOS bridge vlan information
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
  host: {type: str, required: true}
  username: {type: str, required: true}
  password: {type: str, required: true, no_log: true}
  bridge: {type: str, required: true}
  vlan_ids: {type: str, required: true}
  tagged: {type: list, elements: str, default: []}
  untagged: {type: list, elements: str, default: []}
  state: {type: str, choices: [present, absent], default: present}
  validate_certs: {type: bool, default: true}
  timeout: {type: int, default: 30}
requirements: [Python 3, RouterOS 7.x REST API, Ansible 2.16 or newer]
"""


def main():
    m = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "bridge": {"type": "str", "required": True},
            "vlan_ids": {"type": "str", "required": True},
            "tagged": {"type": "list", "elements": "str", "default": []},
            "untagged": {"type": "list", "elements": "str", "default": []},
            "state": {"type": "str", "default": "present", "choices": ["present", "absent"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = m.params
    d = {"bridge": p["bridge"], "vlan-ids": p["vlan_ids"], "tagged": p["tagged"], "untagged": p["untagged"]}
    try:
        reconcile(
            m,
            RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]),
            "interface/bridge/vlan",
            {"bridge": p["bridge"], "vlan-ids": p["vlan_ids"]},
            d,
            p["state"],
            "vlan",
        )
    except RouterOSRestError as e:
        m.fail_json(msg=str(e))


if __name__ == "__main__":
    main()

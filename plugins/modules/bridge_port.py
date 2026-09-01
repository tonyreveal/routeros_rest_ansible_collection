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
module: bridge_port
short_description: Manage or gather RouterOS bridge port information
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
description: Creates, updates, or removes a bridge port idempotently.
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
  bridge:
    type: str
    required: true
  interface:
    type: str
    required: true
  state:
    type: str
    choices: [present, absent]
    default: present
  pvid:
    type: int
  frame_types:
    type: str
  ingress_filtering:
    type: bool
  edge:
    type: str
  point_to_point:
    type: str
  path_cost:
    type: int
  bpdu_guard:
    type: bool
  restricted_role:
    type: bool
  fast_leave:
    type: bool
  horizon:
    type: int
  mlag_id:
    type: int
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
            "bridge": {"type": "str", "required": True},
            "interface": {"type": "str", "required": True},
            "state": {"type": "str", "default": "present", "choices": ["present", "absent"]},
            "pvid": {"type": "int"},
            "frame_types": {"type": "str"},
            "ingress_filtering": {"type": "bool"},
            "edge": {"type": "str"},
            "point_to_point": {"type": "str"},
            "path_cost": {"type": "int"},
            "bpdu_guard": {"type": "bool"},
            "restricted_role": {"type": "bool"},
            "fast_leave": {"type": "bool"},
            "horizon": {"type": "int"},
            "mlag_id": {"type": "int"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = m.params
    desired = {"bridge": p["bridge"], "interface": p["interface"]}
    mapping = {
        "pvid": "pvid",
        "frame-types": "frame_types",
        "ingress-filtering": "ingress_filtering",
        "edge": "edge",
        "point-to-point": "point_to_point",
        "path-cost": "path_cost",
        "bpdu-guard": "bpdu_guard",
        "restricted-role": "restricted_role",
        "fast-leave": "fast_leave",
        "horizon": "horizon",
        "mlag-id": "mlag_id",
    }
    for key, source in mapping.items():
        if p.get(source) is not None:
            desired[key] = p[source]
    try:
        reconcile(
            m,
            RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]),
            "interface/bridge/port",
            {"bridge": p["bridge"], "interface": p["interface"]},
            desired,
            p["state"],
            "port",
        )
    except RouterOSRestError as e:
        m.fail_json(msg=str(e))


if __name__ == "__main__":
    main()


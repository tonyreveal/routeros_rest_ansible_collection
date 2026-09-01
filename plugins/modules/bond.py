#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.resource import reconcile
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r"""
---
module: bond
short_description: Manage or gather RouterOS bond information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Creates, updates, or removes one RouterOS bonding interface idempotently.
  - Supports LACP, active-backup, balance, and broadcast bonding modes.
  - The module does not create Ansible facts.
version_added: 1.0.0
author:
  - Tony Reveal (https://github.com/tonyreveal)
options:
  host: {type: str, required: true}
  username: {type: str, required: true}
  password: {type: str, required: true, no_log: true}
  name: {description: Bonding interface name., type: str, required: true}
  slaves: {description: Member interfaces., type: list, elements: str, required: true}
  mode:
    description: Bonding mode.
    type: str
    choices: [802.3ad, active-backup, balance-alb, balance-rr, balance-tlb, balance-xor, broadcast]
    default: 802.3ad
  link_monitoring:
    description: Link monitoring method.
    type: str
    choices: [mii, arp, none]
    default: mii
  transmit_hash_policy:
    description: Transmit hash policy.
    type: str
    choices: [layer-2, layer-2-and-3, layer-3-and-4, encap-2-and-3, encap-3-and-4]
    default: layer-2-and-3
  mlag_id: {description: Optional MLAG ID for an MLAG client bond., type: int}
  comment: {description: Optional bond comment., type: str}
  enabled: {description: Enable the bond., type: bool, default: true}
  state: {description: Bond lifecycle state., type: str, choices: [present, absent], default: present}
  validate_certs: {description: Validate TLS certificate., type: bool, default: true}
  timeout: {description: HTTP timeout in seconds., type: int, default: 30}
requirements:
  - Python 3
  - RouterOS 7.x with the www-ssl or www REST service enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Configure an LACP bond for MLAG
  mikrotik.routeros_rest.bond:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    name: client-bond
    slaves:
      - ether3
      - ether4
    mode: 802.3ad
    link_monitoring: mii
    transmit_hash_policy: layer-2-and-3
    mlag_id: 10

- name: Remove a bond
  mikrotik.routeros_rest.bond:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    name: client-bond
    slaves:
      - ether3
    state: absent
...
"""


RETURN = r"""
bond:
  description: RouterOS bonding interface returned after reconciliation.
  returned: success
  type: raw
changed_fields:
  description: Bond fields changed during this invocation.
  returned: success
  type: list
"""


def _normalise_slaves(value):
    if isinstance(value, list):
        values = value
    else:
        values = str(value).split(",")
    return [str(item).strip() for item in values if str(item).strip()]


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "slaves": {"type": "list", "elements": "str", "required": True, "min": 1},
            "mode": {
                "type": "str",
                "default": "802.3ad",
                "choices": [
                    "802.3ad",
                    "active-backup",
                    "balance-alb",
                    "balance-rr",
                    "balance-tlb",
                    "balance-xor",
                    "broadcast",
                ],
            },
            "link_monitoring": {"type": "str", "default": "mii", "choices": ["mii", "arp", "none"]},
            "transmit_hash_policy": {
                "type": "str",
                "default": "layer-2-and-3",
                "choices": ["layer-2", "layer-2-and-3", "layer-3-and-4", "encap-2-and-3", "encap-3-and-4"],
            },
            "mlag_id": {"type": "int"},
            "comment": {"type": "str"},
            "enabled": {"type": "bool", "default": True},
            "state": {"type": "str", "default": "present", "choices": ["present", "absent"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    slaves = list(dict.fromkeys(_normalise_slaves(params["slaves"])))
    if not slaves:
        module.fail_json(msg="slaves must contain at least one interface")
    desired = {
        "name": params["name"],
        "slaves": ",".join(slaves),
        "mode": params["mode"],
        "link-monitoring": params["link_monitoring"],
        "transmit-hash-policy": params["transmit_hash_policy"],
        "disabled": not params["enabled"],
    }
    for key, source in {"mlag-id": "mlag_id", "comment": "comment"}.items():
        if params.get(source) is not None:
            desired[key] = params[source]
    client = RouterOSRestClient(
        host=params["host"],
        username=params["username"],
        password=params["password"],
        timeout=params["timeout"],
        validate_certs=params["validate_certs"],
    )
    try:
        reconcile(module, client, "interface/bonding", {"name": params["name"]}, desired, params["state"], "bond")
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))


if __name__ == "__main__":
    main()

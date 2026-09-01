#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.resource import reconcile

DOCUMENTATION = r'''
---
module: interface_ethernet
short_description: Manage RouterOS Ethernet interface settings
description:
  - Updates settings on an existing Ethernet interface through the RouterOS REST API.
  - Ethernet ports are physical resources and are never deleted by this module.
  - When state is absent, the managed Ethernet settings are reset to their RouterOS defaults.
version_added: '1.0.0'
author:
  - Tony Reveal (https://github.com/tonyreveal)
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
    description: Ethernet interface name.
    type: str
    required: true
  settings:
    description: Ethernet interface properties.
    type: dict
    required: true
    suboptions:
      comment:
        description: Interface comment.
        type: str
      disabled:
        description: Whether the interface is disabled.
        type: bool
      mtu:
        description: Interface MTU.
        type: int
      auto_negotiation:
        description: Whether auto-negotiation is enabled.
        type: bool
      speed:
        description: Configured link speed.
        type: str
      full_duplex:
        description: Whether full duplex is enabled.
        type: bool
      poe_out:
        description: PoE output mode.
        type: str
  state:
    description: Desired interface state. Absent resets managed settings and does not delete the physical port.
    type: str
    choices:
      - present
      - absent
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
notes:
  - The Ethernet interface must already exist.
  - state absent resets the managed settings to RouterOS defaults and never removes the physical port.
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
'''


EXAMPLES = r'''
---
- name: Configure an Ethernet port
  mikrotik.routeros_rest.interface_ethernet:
    host: https://router.example.test
    username: admin
    password: secret
    name: ether1
    settings:
      comment: WAN uplink
      auto_negotiation: true
      mtu: 1500
'''
RETURN = r'''
interface:
  description: Ethernet interface record returned after a change.
  returned: on change
  type: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "name": {"type": "str", "required": True}, "settings": {"type": "dict", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    client = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"])
    defaults = {"comment": "", "disabled": False, "mtu": 1500, "auto-negotiation": True, "speed": "auto", "poe-out": "auto-on"}
    desired = defaults if p["state"] == "absent" else p["settings"]
    try:
        if not client.get("interface/ethernet", {"name": p["name"]}):
            module.fail_json(msg=f"Ethernet interface does not exist: {p['name']}")
        reconcile(module, client, "interface/ethernet", {"name": p["name"]}, {"name": p["name"], **desired}, "present", "interface")
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

if __name__ == "__main__":
    main()

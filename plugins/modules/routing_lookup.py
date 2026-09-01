#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.tool import run_tool

DOCUMENTATION = r'''
---
module: routing_lookup
short_description: Perform a RouterOS route lookup
description:
  - Looks up the active route for a destination through the RouterOS REST API.
  - This is an operational action; persistent state and idempotency are not applicable.
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
  address:
    description: Destination IPv4 or IPv6 address.
    type: str
    required: true
  routing_table:
    description: Optional routing table to query.
    type: str
  vrf:
    description: Optional VRF context.
    type: str
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
attributes:
  check_mode:
    description: Does not perform a route lookup in check mode.
    support: partial
'''


EXAMPLES = r'''
---
- name: Look up the route to a destination
  mikrotik.routeros_rest.routing_lookup:
    host: https://router.example.test
    username: admin
    password: secret
    address: 198.51.100.10
  register: route_lookup
'''
RETURN = r'''
result:
  description: RouterOS route-lookup response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "address": {"type": "str", "required": True}, "routing_table": {"type": "str"}, "vrf": {"type": "str"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    payload = {"address": p["address"]}
    if p.get("routing_table"): payload["routing-table"] = p["routing_table"]
    if p.get("vrf"): payload["vrf"] = p["vrf"]
    run_tool(module, "ip/route/print", payload)
if __name__ == "__main__": main()

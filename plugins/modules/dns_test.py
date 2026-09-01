#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.tool import run_tool

DOCUMENTATION = r'''
---
module: dns_test
short_description: Run a RouterOS DNS test
description:
  - Resolves a DNS name through the RouterOS DNS resolver using the REST API.
  - This is an operational action; state and persistent idempotency are not applicable.
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
    description: DNS name to resolve.
    type: str
    required: true
  type:
    description: DNS record type.
    type: str
    default: A
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
    description: Does not execute the DNS test in check mode.
    support: partial
'''
EXAMPLES = r'''
---
- name: Resolve a name from RouterOS
  mikrotik.routeros_rest.dns_test:
    host: https://router.example.test
    username: admin
    password: secret
    name: www.example.com
  register: dns_result
'''
RETURN = r'''
result:
  description: RouterOS DNS test response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "name": {"type": "str", "required": True}, "type": {"type": "str", "default": "A"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    run_tool(module, "ip/dns-cache/flush", {"name": p["name"], "type": p["type"]})
if __name__ == "__main__": main()

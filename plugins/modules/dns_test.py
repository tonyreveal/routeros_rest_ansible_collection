#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later
# (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (RouterOSRestClient, RouterOSRestError)

DOCUMENTATION = r'''
---
module: dns_test
short_description: Run a RouterOS DNS resolution test
description:
  - Resolves a DNS name from the MikroTik RouterOS device using the
    RouterOS DNS resolver and REST API.
  - The lookup is executed on the RouterOS device using the RouterOS
    C(:resolve) command.
  - This is an operational action; state and persistent idempotency
    are not applicable.
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
    description:
      - Address family to resolve.
      - C(A) performs an IPv4 lookup.
      - C(AAAA) performs an IPv6 lookup.
    type: str
    choices:
      - A
      - AAAA
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
- name: Resolve an IPv4 address from RouterOS
  mikrotik.routeros_rest.dns_test:
    host: https://router.example.test
    username: admin
    password: secret
    name: www.example.com
    type: A
  register: dns_result

- name: Resolve an IPv6 address from RouterOS
  mikrotik.routeros_rest.dns_test:
    host: https://router.example.test
    username: admin
    password: secret
    name: www.example.com
    type: AAAA
  register: dns_result
'''
RETURN = r'''
result:
  description: RouterOS DNS resolution response.
  returned: success
  type: raw
'''


def escape_routeros_string(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')

def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "type": {"type": "str", "choices": ["A", "AAAA"], "default": "A"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )

    p = module.params
    resolve_types = {"A": "ipv4", "AAAA": "ipv6"}
    resolve_type = resolve_types[p["type"]]
    name = escape_routeros_string(p["name"])
    script = (':put [:resolve domain-name="{}" type={}]'.format(name, resolve_type))

    try:
        client = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"])
        result = client.post("execute", {"script": script, "as-string": ""} )
        address = result.get("ret", "").strip()
        if not address:
            module.fail_json(msg="DNS resolution returned no address", name=p["name"], type=p["type"], result=result)
        module.exit_json(changed=False, name=p["name"], type=p["type"], address=address)

    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc), name=p["name"], type=p["type"])

if __name__ == "__main__":
    main()
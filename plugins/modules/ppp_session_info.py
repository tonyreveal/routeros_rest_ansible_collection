#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: ppp_session_info
short_description: Gather active RouterOS PPP sessions
description:
  - Reads active PPP sessions from the RouterOS REST API.
  - Supports filtering by user, service, caller ID, address, and session ID.
  - Results are returned in the registered module result and are not Ansible facts.
  - Connection state details such as uptime, address, caller ID, encoding, and session ID are returned when RouterOS provides them.
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
  user:
    description: Filter by PPP user name.
    type: str
  service:
    description: Filter by PPP service.
    type: str
  caller_id:
    description: Filter by caller ID.
    type: str
  address:
    description: Filter by assigned address.
    type: str
  session_id:
    description: Filter by RouterOS session ID.
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
    description: Supports check mode without changing the device.
    support: full
'''


EXAMPLES = r'''
---
- name: Gather active L2TP sessions for Tony
  mikrotik.routeros_rest.ppp_session_info:
    host: https://router.example.test
    username: admin
    password: secret
    user: tony
    service: l2tp
  register: ppp_sessions
'''
RETURN = r'''
sessions:
  description: Active PPP session records and connection state details.
  returned: always
  type: list
  elements: dict
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True},
        "username": {"type": "str", "required": True},
        "password": {"type": "str", "required": True, "no_log": True},
        "user": {"type": "str"}, "service": {"type": "str"}, "caller_id": {"type": "str"},
        "address": {"type": "str"}, "session_id": {"type": "str"},
        "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    query = {}
    for key in ("user", "service", "caller_id", "address"):
        if p.get(key) is not None:
            query[key.replace("caller_id", "caller-id")] = p[key]
    if p.get("session_id") is not None:
        query[".id"] = p["session_id"]
    client = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"])
    try:
        data = client.get("ppp/active", query)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
    if isinstance(data, dict):
        data = [data]
    module.exit_json(changed=False, sessions=data)

if __name__ == "__main__":
    main()

#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: ppp_session_disconnect
short_description: Disconnect an active PPP session
description:
  - Disconnects a selected active PPP session through the RouterOS REST API.
  - The operation is idempotent because an already absent session requires no action.
  - Use state present to leave the selected session connected and state absent to disconnect it.
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
  session_id:
    description: RouterOS active PPP session internal ID.
    type: str
    required: true
  state:
    description: Desired session state.
    type: str
    choices:
      - present
      - absent
    default: absent
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
    description: Reports whether a disconnect would occur without changing the device.
    support: full
'''


EXAMPLES = r'''
---
- name: Disconnect an active PPP session
  mikrotik.routeros_rest.ppp_session_disconnect:
    host: https://router.example.test
    username: admin
    password: secret
    session_id: '*7'
    state: absent
'''
RETURN = r'''
session_id:
  description: Requested PPP session ID.
  returned: always
  type: str
  sample: '*7'
'''


def main() -> None:
    module = AnsibleModule(argument_spec={
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "session_id": {"type": "str", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "absent"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }, supports_check_mode=True)
    p = module.params
    client = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"])
    try:
        sessions = client.get("ppp/active", {".id": p["session_id"]})
        exists = bool(sessions)
        if p["state"] == "present" or not exists:
            module.exit_json(changed=False, session_id=p["session_id"])
        if module.check_mode:
            module.exit_json(changed=True, session_id=p["session_id"])
        result = client.post("ppp/active/remove", {".id": p["session_id"]})
        module.exit_json(changed=True, session_id=p["session_id"], result=result)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

if __name__ == "__main__":
    main()

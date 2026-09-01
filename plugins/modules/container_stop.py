#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: container_stop
short_description: Stop a RouterOS container
description:
  - Ensures a named RouterOS container is stopped through the REST API.
  - Repeated runs do not stop an already stopped container.
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
    description: Container name.
    type: str
    required: true
  state:
    description: Absent stops the container; present leaves it running.
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
  - RouterOS 7.x with REST API and container support enabled.
  - Ansible 2.16 or newer.
attributes:
  check_mode:
    description: Reports whether a stop operation would occur.
    support: full
'''
EXAMPLES = r'''
---
- name: Stop a container
  mikrotik.routeros_rest.container_stop:
    host: https://router.example.test
    username: admin
    password: secret
    name: dns-container
    state: absent
'''
RETURN = r'''
result:
  description: RouterOS container operation response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "name": {"type": "str", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "absent"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params; client = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"])
    try:
        current = client.get("container", {"name": p["name"]}); current = current[0] if isinstance(current, list) and current else current
        running = isinstance(current, dict) and str(current.get("running", current.get("status", ""))).lower() in {"true", "yes", "running"}
        if p["state"] == "present" or not running: module.exit_json(changed=False, result=current or {})
        if module.check_mode: module.exit_json(changed=True)
        module.exit_json(changed=True, result=client.post("container/stop", {"name": p["name"]}))
    except RouterOSRestError as exc: module.fail_json(msg=str(exc))
if __name__ == "__main__": main()


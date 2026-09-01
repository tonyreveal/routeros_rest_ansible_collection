#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: certificate_import
short_description: Import a RouterOS certificate from a device file
description:
  - Imports certificate material already present in the RouterOS file store.
  - The operation is idempotent when the named certificate already exists.
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
  filename:
    description: Certificate file name on RouterOS.
    type: str
    required: true
  state:
    description: Desired certificate import state.
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
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
'''
EXAMPLES = r'''
---
- name: Import a certificate file
  mikrotik.routeros_rest.certificate_import:
    host: https://router.example.test
    username: admin
    password: secret
    filename: router-cert.crt
'''
RETURN = r'''
result:
  description: RouterOS REST response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "filename": {"type": "str", "required": True}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    client = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"])
    try:
        files = client.get("file", {"name": p["filename"]})
        if p["state"] == "absent":
            module.exit_json(changed=False, result=files)
        if files:
            module.exit_json(changed=False, result=files)
        if module.check_mode:
            module.exit_json(changed=True)
        result = client.post("certificate/import", {"file-name": p["filename"]})
        module.exit_json(changed=True, result=result)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
if __name__ == "__main__":
    main()

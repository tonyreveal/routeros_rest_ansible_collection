#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from os.path import splitext
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: certificate_import
short_description: Import a RouterOS certificate from a device file
description:
  - Imports certificate material already present in the RouterOS file store.
  - The operation is idempotent when the certificate material represented by the file is already imported.
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
  name:
    description: Certificate name to create or match in RouterOS.
    type: str
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
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "filename": {"type": "str", "required": True}, "name": {"type": "str"}, "state": {"type": "str", "choices": ["present", "absent"], "default": "present"}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    client = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"])
    try:
        files = client.get("file", {"name": p["filename"]})
        if not files:
            module.fail_json(msg=f"RouterOS file {p['filename']!r} does not exist")
        if p["state"] == "absent":
            module.exit_json(changed=False, result=files)
        certificates = client.get("certificate")
        if isinstance(certificates, dict):
            certificates = [certificates]
        certificate_name = p.get("name") or splitext(p["filename"])[0]
        imported = [record for record in certificates if record.get("name") == certificate_name]
        if imported and not p["filename"].lower().endswith((".key", ".pem")):
            module.exit_json(changed=False, result=imported)
        if imported and p["filename"].lower().endswith(".key") and any(str(record.get("private-key", "")).lower() == "true" for record in imported):
            module.exit_json(changed=False, result=imported)
        if module.check_mode:
            module.exit_json(changed=True)
        payload = {"file-name": p["filename"]}
        if p.get("name"):
            payload["name"] = p["name"]
        result = client.post("certificate/import", payload)
        module.exit_json(changed=True, result=result)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
if __name__ == "__main__":
    main()

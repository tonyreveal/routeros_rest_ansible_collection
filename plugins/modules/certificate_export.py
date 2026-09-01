#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: certificate_export
short_description: Export a RouterOS certificate to a device file
description:
  - Exports a RouterOS certificate to the device file store through the REST API.
  - Export is intentionally non-idempotent because it creates a new artifact.
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
  certificate:
    description: Certificate name to export.
    type: str
    required: true
  filename:
    description: Destination file name on RouterOS.
    type: str
    required: true
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
    description: Does not perform the export in check mode.
    support: partial
'''
EXAMPLES = r'''
---
- name: Export a certificate
  mikrotik.routeros_rest.certificate_export:
    host: https://router.example.test
    username: admin
    password: secret
    certificate: router-cert
    filename: router-cert.p12
'''
RETURN = r'''
result:
  description: RouterOS REST response.
  returned: success
  type: raw
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "certificate": {"type": "str", "required": True}, "filename": {"type": "str", "required": True}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    if module.check_mode:
        module.exit_json(changed=True)
    try:
        result = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]).post("certificate/export", {"certificate": p["certificate"], "file-name": p["filename"]})
        module.exit_json(changed=True, result=result, filename=p["filename"])
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
if __name__ == "__main__":
    main()

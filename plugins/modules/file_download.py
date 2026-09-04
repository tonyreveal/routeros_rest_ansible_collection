#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import RouterOSRestClient, RouterOSRestError

DOCUMENTATION = r'''
---
module: file_download
short_description: Download a RouterOS file
description:
  - Downloads a RouterOS file through the REST API to a local path.
  - The module is idempotent when the local file already matches the downloaded content.
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
  src:
    description: RouterOS file name.
    type: str
    required: true
  dest:
    description: Local destination path.
    type: path
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
    description: Does not download a file in check mode.
    support: partial
'''
EXAMPLES = r'''
---
- name: Download a RouterOS export
  mikrotik.routeros_rest.file_download:
    host: https://router.example.test
    username: admin
    password: secret
    src: router.rsc
    dest: ./router.rsc
'''
RETURN = r'''
dest:
  description: Local destination path.
  returned: success
  type: path
'''


def main() -> None:
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "src": {"type": "str", "required": True}, "dest": {"type": "path", "required": True}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    p = module.params
    try:
        data = RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]).get("file", {"name": p["src"]})
        if isinstance(data, list):
            records = [record for record in data if isinstance(record, dict)]
            matching = [record for record in records if record.get("name") == p["src"]]
            data = matching[0] if matching else (records[0] if len(records) == 1 else {})
        if not isinstance(data, dict) or data.get("name") != p["src"]:
            module.fail_json(msg=f"RouterOS file does not exist: {p['src']}")
        if "contents" not in data:
            module.fail_json(msg=f"RouterOS did not return contents for file: {p['src']}")
        content = data["contents"]
        if module.check_mode:
            module.exit_json(changed=True, dest=p["dest"])
        old = open(p["dest"], "r", encoding="utf-8").read() if __import__("os").path.exists(p["dest"]) else None
        if old == content:
            module.exit_json(changed=False, dest=p["dest"])
        with open(p["dest"], "w", encoding="utf-8") as handle:
            handle.write(content)
        module.exit_json(changed=True, dest=p["dest"])
    except (OSError, RouterOSRestError) as exc:
        module.fail_json(msg=str(exc))
if __name__ == "__main__":
    main()

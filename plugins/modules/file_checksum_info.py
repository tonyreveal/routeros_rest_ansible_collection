#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

"""Return a checksum for file content exposed by the RouterOS REST API."""

import base64
import hashlib
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r'''
---
module: file_checksum_info
short_description: Calculate a checksum for a RouterOS file
description:
  - Reads a file through the RouterOS REST API and calculates its checksum.
  - The result is returned in the registered module result and is not an Ansible fact.
  - The RouterOS REST response must expose the file content as C(contents),
    optionally encoded as base64 in C(contents-base64).
version_added: '1.0.0'
author:
  - Tony Reveal (https://github.com/tonyreveal)
options:
  host:
    description:
      - RouterOS REST base URL.
    type: str
    required: true
  username:
    description:
      - RouterOS REST username.
    type: str
    required: true
  password:
    description:
      - RouterOS REST password.
    type: str
    required: true
    no_log: true
  name:
    description:
      - RouterOS file name.
    type: str
    required: true
  algorithm:
    description:
      - Checksum algorithm to use.
    type: str
    choices:
      - md5
      - sha1
      - sha256
    default: sha256
  validate_certs:
    description:
      - Validate the RouterOS TLS certificate.
    type: bool
    default: true
  timeout:
    description:
      - HTTP timeout in seconds.
    type: int
    default: 30
requirements:
  - Python 3.
  - RouterOS 7.x with REST API enabled.
  - Ansible 2.16 or newer.
attributes:
  check_mode:
    description:
      - Supports check mode without changing the device.
    support: full
notes:
  - This module is read-only and does not support C(state).
'''


EXAMPLES = r'''
---
- name: Calculate a RouterOS backup checksum
  mikrotik.routeros_rest.file_checksum_info:
    host: https://router.example.test
    username: admin
    password: secret
    name: ansible-backup-20260817-1354.backup
    algorithm: sha256
  register: backup_checksum
'''

RETURN = r'''
filename:
  description: RouterOS file name.
  returned: always
  type: str
algorithm:
  description: Checksum algorithm used.
  returned: always
  type: str
checksum:
  description: Lowercase hexadecimal checksum.
  returned: always
  type: str
file:
  description: RouterOS file record returned by the REST API.
  returned: always
  type: dict
'''


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "algorithm": {"type": "str", "choices": ["md5", "sha1", "sha256"], "default": "sha256"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"],
    )
    try:
        records = client.get("file", {"name": params["name"]})
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
    if isinstance(records, dict):
        records = [records]
    if not records:
        module.fail_json(msg=f"RouterOS file {params['name']!r} was not found")
    record = records[0]
    content = record.get("contents")
    if "contents-base64" in record:
        try:
            content = base64.b64decode(record["contents-base64"])
        except (ValueError, TypeError) as exc:
            module.fail_json(msg=f"RouterOS returned invalid base64 file content: {exc}")
    elif isinstance(content, str):
        content = content.encode("utf-8")
    if not isinstance(content, (bytes, bytearray)):
        module.fail_json(msg="RouterOS REST did not return readable file contents")
    checksum = hashlib.new(params["algorithm"], content).hexdigest()
    module.exit_json(changed=False, filename=params["name"], algorithm=params["algorithm"], checksum=checksum, file=record)


if __name__ == "__main__":
    main()

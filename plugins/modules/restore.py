#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r"""
---
module: restore
short_description: Manage or gather RouterOS restore information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Verifies that a named .backup file exists on the RouterOS device.
  - Starts the RouterOS system backup load operation for the requested file.
  - Supports check mode, in which the file is verified but no restore is started.
  - The restore operation reboots or disrupts the device and is intentionally reported as changed when executed.
  - The module does not create Ansible facts.
version_added: 1.0.0
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
    description: Name of the .backup file in the RouterOS root directory.
    type: str
    required: true
  validate_certs:
    description: Validate the RouterOS www-ssl certificate.
    type: bool
    default: true
  timeout:
    description: HTTP request timeout in seconds.
    type: int
    default: 30
notes:
  - Use HTTPS and validate_certs=true in production.
  - The REST API requires the www-ssl or www service to be enabled on RouterOS.
  - Restoring a backup is disruptive and may cause the REST connection to close.
  - Follow this module with ansible.builtin.wait_for_connection when the device is expected to reboot.
requirements:
  - Python 3
  - RouterOS 7.x with the www-ssl or www REST service enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Restore a RouterOS binary backup
  mikrotik.routeros.restore:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    filename: ansible-backup-20260825-1345.backup

- name: Wait for RouterOS to return after the restore
  ansible.builtin.wait_for_connection:
    timeout: 600
    connect_timeout: 30
    sleep: 10
...
"""


RETURN = r"""
filename:
  description: Backup filename verified before the restore operation.
  returned: always
  type: str
result:
  description: Raw response returned by the RouterOS REST API.
  returned: success
  type: raw
verified:
  description: Whether the requested backup file was found on the device.
  returned: always
  type: bool
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "filename": {"type": "str", "required": True},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    if not params["filename"].lower().endswith(".backup"):
        module.fail_json(msg="filename must identify a RouterOS .backup file")

    client = RouterOSRestClient(
        host=params["host"],
        username=params["username"],
        password=params["password"],
        timeout=params["timeout"],
        validate_certs=params["validate_certs"],
    )

    try:
        files = client.get("file", query={"name": params["filename"]})
        if not isinstance(files, list):
            files = [files]
        matching_files = [
            record for record in files
            if isinstance(record, dict) and record.get("name") == params["filename"]
        ]
        if not matching_files:
            module.fail_json(
                msg=f"RouterOS backup file was not found: {params['filename']}",
                filename=params["filename"],
                verified=False,
            )

        if module.check_mode:
            module.exit_json(
                changed=True,
                filename=params["filename"],
                verified=True,
                result={"check_mode": True, "message": "Backup file exists; restore was not started"},
            )

        result = client.post("system/backup/load", {"name": params["filename"]})
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc), filename=params["filename"], verified=False)

    module.exit_json(
        changed=True,
        filename=params["filename"],
        verified=True,
        result=result,
    )


if __name__ == "__main__":
    main()

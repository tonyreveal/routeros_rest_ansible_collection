#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations

from datetime import datetime, timezone

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r"""
---
module: export
short_description: Manage or gather RouterOS export information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Creates a plain-text RouterOS configuration export through the REST API.
  - The filename is built as prefix-YYYYMMDD-HHMM.rsc using the UTC date and time.
  - Returns the generated filename directly in the registered module result.
  - The module does not create Ansible facts.
version_added: 1.0.0
author:
  - Tony Reveal (https://github.com/tonyreveal)
options:
  host:
    description:
      - RouterOS REST base URL, such as https://192.0.2.1.
      - The module appends /rest when it is not already present.
    type: str
    required: true
  username:
    description:
      - RouterOS user for HTTP Basic Authentication.
    type: str
    required: true
  password:
    description:
      - RouterOS password for HTTP Basic Authentication.
    type: str
    required: true
    no_log: true
  validate_certs:
    description:
      - Validate the TLS certificate presented by the RouterOS www-ssl service.
    type: bool
    default: true
  timeout:
    description:
      - HTTP request timeout in seconds.
    type: int
    default: 30
  filename_prefix:
    description:
      - Safe prefix for the generated export filename.
      - The module appends -YYYYMMDD-HHMM.rsc.
    type: str
    default: ansible-export
notes:
  - Use HTTPS and validate_certs=true in production.
  - The REST API requires the www-ssl or www service to be enabled on RouterOS.
  - The export file remains on the RouterOS device and must be retrieved separately.
requirements:
  - Python 3
  - RouterOS 7.x with REST API enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Export RouterOS configuration
  mikrotik.routeros.export:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    filename_prefix: ansible-export
  register: export_result

- name: Display generated filename
  ansible.builtin.debug:
    var: export_result.filename
...
"""


RETURN = r"""
filename:
  description: Generated export filename including the .rsc extension.
  returned: always
  type: str
  sample: ansible-export-20260825-1345.rsc
result:
  description: Raw response returned by the RouterOS REST API.
  returned: success
  type: raw
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
            "filename_prefix": {
                "type": "str",
                "default": "ansible-export",
            },
        },
        supports_check_mode=False,
    )

    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    if not params["filename_prefix"] or not all(
        character.isalnum() or character in "_-" for character in params["filename_prefix"]
    ):
        module.fail_json(msg="filename_prefix must contain only letters, numbers, underscores, or hyphens")

    filename = f"{params['filename_prefix']}-{datetime.now(timezone.utc):%Y%m%d-%H%M}.rsc"
    client = RouterOSRestClient(
        host=params["host"],
        username=params["username"],
        password=params["password"],
        timeout=params["timeout"],
        validate_certs=params["validate_certs"],
    )

    try:
        result = client.post("export", {"file": filename})
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, filename=filename, result=result)


if __name__ == "__main__":
    main()

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
module: reset
short_description: Reset RouterOS configuration
description:
  - Clears the RouterOS configuration and reboots the device through the REST API.
  - By default, RouterOS restores its factory-default configuration and creates an automatic backup before resetting.
  - This module is intentionally non-idempotent because each successful invocation initiates a configuration reset.
  - The module requires confirm=true to prevent accidental destructive resets.
  - The REST request normally closes the connection because RouterOS reboots immediately after accepting the command.
version_added: 1.0.0
author:
  - Tony Reveal (https://github.com/tonyreveal)
requirements:
  - Python 3
  - RouterOS 7.x with the www-ssl or www REST service enabled
  - Ansible 2.16 or newer
options:
  host:
    description:
      - RouterOS REST base URL, such as https://192.0.2.1.
      - The module appends /rest when it is not already present.
    type: str
    required: true
  username:
    description: RouterOS user for HTTP Basic Authentication.
    type: str
    required: true
  password:
    description: RouterOS password for HTTP Basic Authentication.
    type: str
    required: true
    no_log: true
  confirm:
    description: Confirm that the RouterOS configuration should be cleared and the device rebooted.
    type: bool
    default: false
  keep_users:
    description: Preserve existing RouterOS users during the reset.
    type: bool
    default: false
  no_defaults:
    description: Clear the configuration without loading the factory-default configuration.
    type: bool
    default: false
  skip_backup:
    description: Do not create RouterOS's automatic backup before resetting.
    type: bool
    default: false
  run_after_reset:
    description: RouterOS .rsc file to execute after the reset.
    type: str
  caps_mode:
    description: Run the RouterOS CAPs mode script after resetting.
    type: bool
    default: false
  validate_certs:
    description: Validate the TLS certificate presented by RouterOS.
    type: bool
    default: true
  timeout:
    description: HTTP request timeout in seconds.
    type: int
    default: 30
notes:
  - Use HTTPS and validate_certs=true in production.
  - This operation removes configuration and normally resets the login credentials.
  - Create and download a backup or export before invoking this module.
  - After reset, use ansible.builtin.wait_for_connection or an equivalent recovery workflow.
attributes:
  check_mode:
    description: Reports that a reset would be requested without contacting or changing the device.
    support: full
"""


EXAMPLES = r"""
---
- name: Reset RouterOS to factory defaults
  mikrotik.routeros_rest.reset:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    confirm: true

- name: Clear RouterOS configuration without loading defaults
  mikrotik.routeros_rest.reset:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    confirm: true
    no_defaults: true
    skip_backup: true
...
"""


RETURN = r"""
result:
  description: Response returned by RouterOS before the device reboots, when available.
  returned: success
  type: raw
reset_requested:
  description: Whether the reset request was submitted.
  returned: always
  type: bool
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "confirm": {"type": "bool", "default": False},
            "keep_users": {"type": "bool", "default": False},
            "no_defaults": {"type": "bool", "default": False},
            "skip_backup": {"type": "bool", "default": False},
            "run_after_reset": {"type": "str"},
            "caps_mode": {"type": "bool", "default": False},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params

    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    if not params["confirm"]:
        module.fail_json(msg="confirm must be set to true before resetting RouterOS")
    if params["run_after_reset"] and not params["run_after_reset"].lower().endswith(".rsc"):
        module.fail_json(msg="run_after_reset must specify a RouterOS .rsc file")
    if module.check_mode:
        module.exit_json(changed=True, reset_requested=False, msg="RouterOS reset would be requested")

    payload = {
        "keep-users": "yes" if params["keep_users"] else "no",
        "no-defaults": "yes" if params["no_defaults"] else "no",
        "skip-backup": "yes" if params["skip_backup"] else "no",
        "caps-mode": "yes" if params["caps_mode"] else "no",
    }
    if params["run_after_reset"]:
        payload["run-after-reset"] = params["run_after_reset"]

    client = RouterOSRestClient(
        host=params["host"],
        username=params["username"],
        password=params["password"],
        timeout=params["timeout"],
        validate_certs=params["validate_certs"],
    )
    try:
        result = client.post("system/reset-configuration", payload)
    except RouterOSRestError as exc:
        if any(text in str(exc).lower() for text in ("closed", "reset", "unreachable", "timeout", "reboot")):
            module.exit_json(
                changed=True,
                reset_requested=True,
                result={"message": str(exc), "connection_closed": True},
            )
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, reset_requested=True, result=result)


if __name__ == "__main__":
    main()

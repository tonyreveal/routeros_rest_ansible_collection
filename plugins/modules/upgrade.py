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
module: upgrade
short_description: Manage or gather RouterOS upgrade information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Sets the RouterOS package update channel and starts package installation through REST when an update is available.
  - The default channel is stable; the user can select long-term, testing, or development.
  - Installing a package can reboot or disconnect the device.
  - Does not upgrade RouterBOARD firmware or create Ansible facts.
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
  channel:
    description: RouterOS release channel to use for the upgrade.
    type: str
    default: stable
    choices: [long-term, stable, testing, development]
  validate_certs:
    description: Validate the RouterOS www-ssl certificate.
    type: bool
    default: true
  timeout:
    description: HTTP request timeout in seconds.
    type: int
    default: 30
requirements:
  - Python 3
  - RouterOS 7.x with the www-ssl or www REST service enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Upgrade RouterOS on the stable channel
  mikrotik.routeros.upgrade:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
  register: upgrade_result

- name: Use the testing channel instead
  mikrotik.routeros.upgrade:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    channel: testing
...
"""


RETURN = r"""
channel:
  description: Channel selected for the upgrade.
  returned: always
  type: str
result:
  description: Response from the RouterOS package install command, when available.
  returned: success
  type: raw
changed_reason:
  description: State decision explaining whether a package installation was started.
  returned: always
  type: str
"""


def _record(value):
    """Return the first REST record for singleton RouterOS responses."""
    if isinstance(value, list):
        return value[0] if value else {}
    return value if isinstance(value, dict) else {}


def _update_available(value):
    """Interpret RouterOS update status without depending on response casing."""
    record = _record(value)
    status = str(record.get("status", "")).lower()
    installed = str(record.get("installed-version", ""))
    latest = str(record.get("latest-version", ""))
    if latest and installed and latest != installed:
        return True
    return "new version is available" in status or "update available" in status


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "channel": {
                "type": "str", "default": "stable",
                "choices": ["long-term", "stable", "testing", "development"],
            },
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=False,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")

    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"],
    )
    channel_changed = False
    try:
        settings = _record(client.get("system/package/update"))
        if str(settings.get("channel", "")) != params["channel"]:
            client.post("system/package/update/set", {"channel": params["channel"]})
            channel_changed = True
        result = client.post("system/package/update/check-for-updates", {})
        update_available = _update_available(result)
        if update_available:
            result = client.post("system/package/update/install", {})
            changed_reason = "RouterOS package update started"
        else:
            changed_reason = "RouterOS package is current"
    except RouterOSRestError as exc:
        if not any(text in str(exc).lower() for text in ("closed", "reset", "unreachable", "timeout", "reboot")):
            module.fail_json(msg=str(exc))
        result = {"message": str(exc), "connection_closed": True}
        update_available = True
        changed_reason = "RouterOS package update request accepted before connection closed"
    module.exit_json(
        changed=channel_changed or update_available,
        channel=params["channel"],
        result=result,
        changed_reason=changed_reason,
    )


if __name__ == "__main__":
    main()

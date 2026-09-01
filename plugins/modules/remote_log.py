#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations

import ipaddress

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r"""
---
module: remote_log
short_description: Manage or gather RouterOS remote log information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Configures the built-in RouterOS remote logging action idempotently.
  - The action is named remote and is not deleted when state is absent.
  - state=absent resets the action to its default values, including an empty remote address.
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
  remote_address:
    description: Remote syslog server address. Required even when state is absent; ignored during reset.
    type: str
    required: true
  comment:
    description: Comment assigned to the remote action.
    type: str
    default: ''
  remote_port:
    description: Remote syslog port.
    type: int
    default: 514
  source_address:
    description: Source address used for remote syslog traffic.
    type: str
    default: 0.0.0.0
  remote_log_format:
    description: Remote log format.
    type: str
    choices: [default, bsd-syslog, syslog]
    default: default
  remote_log_protocol:
    description: Remote log transport protocol.
    type: str
    choices: [UDP, TCP, UDP6, TCP6]
    default: UDP
  vrf:
    description: VRF used for remote log traffic.
    type: str
    default: main
  state:
    description: Whether to configure or reset the remote action.
    type: str
    choices: [absent, present]
    default: present
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
- name: Configure remote syslog
  mikrotik.routeros.remote_log:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    remote_address: 192.0.2.50
    remote_port: 514
    remote_log_protocol: UDP
    vrf: main
    comment: Central syslog collector

- name: Reset remote syslog action to defaults
  mikrotik.routeros.remote_log:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    remote_address: 192.0.2.50
    state: absent
...
"""


RETURN = r"""
action:
  description: RouterOS remote action record returned after reconciliation.
  returned: success
  type: raw
changed_fields:
  description: Action fields changed during this invocation.
  returned: success
  type: list
"""


def _first_record(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value if isinstance(value, dict) else None


def _normalise_protocol(value):
    return str(value).upper()


def _matches(current, desired):
    return str(current).lower() == str(desired).lower()


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "remote_address": {"type": "str", "required": True},
            "comment": {"type": "str", "default": ""},
            "remote_port": {"type": "int", "default": 514},
            "source_address": {"type": "str", "default": "0.0.0.0"},
            "remote_log_format": {"type": "str", "default": "default", "choices": ["default", "bsd-syslog", "syslog"]},
            "remote_log_protocol": {"type": "str", "default": "UDP"},
            "vrf": {"type": "str", "default": "main"},
            "state": {"type": "str", "default": "present", "choices": ["absent", "present"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    if not 1 <= params["remote_port"] <= 65535:
        module.fail_json(msg="remote_port must be between 1 and 65535")
    remote_log_protocol = _normalise_protocol(params["remote_log_protocol"])
    if remote_log_protocol not in {"TCP", "UDP", "TCP6", "UDP6"}:
        module.fail_json(msg="remote_log_protocol must be one of TCP, UDP, TCP6, or UDP6")
    try:
        remote_address = ipaddress.ip_address(params["remote_address"])
    except ValueError as exc:
        module.fail_json(msg=f"remote_address must be an IPv4 address; hostnames and IPv6 addresses are not accepted: {exc}")
    if remote_address.version != 4:
        module.fail_json(msg="remote_address must be an IPv4 address; hostnames and IPv6 addresses are not accepted")

    desired = {
        "name": "remote",
        "target": "remote",
        "comment": "",
        "remote": "",
        "remote-port": 514,
        "src-address": "0.0.0.0",
        "remote-log-format": "default",
        "remote-protocol": "udp",
        "vrf": "main",
    }
    if params["state"] == "present":
        desired.update(
            {
                "comment": params["comment"],
                "remote": params["remote_address"],
                "remote-port": params["remote_port"],
                "src-address": params["source_address"],
                "remote-log-format": params["remote_log_format"],
                "remote-protocol": remote_log_protocol.lower(),
                "vrf": params["vrf"],
            }
        )

    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"],
    )
    try:
        existing = _first_record(client.get("system/logging/action", query={"name": "remote"}))
        if existing is None:
            result = desired if module.check_mode else client.put("system/logging/action", desired)
            module.exit_json(changed=True, action=result, changed_fields=list(desired))

        changes = {
            key: value for key, value in desired.items()
            if not _matches(existing.get(key, ""), value)
        }
        if not changes:
            module.exit_json(changed=False, action=existing, changed_fields=[])
        result = {**existing, **changes} if module.check_mode else client.patch(
            f"system/logging/action/{existing['.id']}", changes
        )
    except KeyError as exc:
        module.fail_json(msg=f"RouterOS remote log action response did not include {exc}")
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, action=result, changed_fields=list(changes))


if __name__ == "__main__":
    main()

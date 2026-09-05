#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations

import ipaddress
import re

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r"""
---
module: ntp_client
short_description: Manage or gather RouterOS ntp client information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Configures the RouterOS singleton NTP client idempotently.
  - Requires one or more NTP server hostnames or IP addresses.
  - state=absent resets the NTP client to its defaults instead of deleting it.
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
  servers:
    description: One or more NTP server hostnames or IP addresses.
    type: list
    elements: str
    required: true
  mode:
    description: NTP client operating mode.
    type: str
    choices: [unicast, multicast, manycast, broadcast]
    default: unicast
  vrf:
    description: VRF used by the NTP client.
    type: str
    default: main
  enabled:
    description: Whether the NTP client should be enabled.
    type: bool
    default: true
  state:
    description: Whether to configure or reset the NTP client.
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
- name: Configure the RouterOS NTP client
  mikrotik.routeros.ntp_client:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    servers:
      - time.cloudflare.com
      - 192.0.2.123
    mode: unicast
    vrf: main
    enabled: true

- name: Reset the NTP client to RouterOS defaults
  mikrotik.routeros.ntp_client:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    servers:
      - time.cloudflare.com
    state: absent
...
"""


RETURN = r"""
ntp_client:
  description: RouterOS NTP client settings returned after reconciliation.
  returned: success
  type: raw
changed_fields:
  description: NTP client fields changed during this invocation.
  returned: success
  type: list
"""


HOSTNAME_PATTERN = re.compile(r"^(?=.{1,253}$)([A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)*[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?$")


def _valid_server(server):
    try:
        ipaddress.ip_address(server)
        return True
    except ValueError:
        return bool(HOSTNAME_PATTERN.fullmatch(server))


def _servers(value):
    values = value if isinstance(value, list) else str(value).split(",")
    return [str(item).strip() for item in values if str(item).strip()]


def _bool_matches(current, desired):
    return (str(current).lower() in {"yes", "true"}) == desired


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "servers": {"type": "list", "elements": "str", "required": True, "min": 1},
            "mode": {"type": "str", "default": "unicast", "choices": ["unicast", "multicast", "manycast", "broadcast"]},
            "vrf": {"type": "str", "default": "main"},
            "enabled": {"type": "bool", "default": True},
            "state": {"type": "str", "default": "present", "choices": ["absent", "present"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    servers = list(dict.fromkeys(str(server).strip() for server in params["servers"] if str(server).strip()))
    if not servers:
        module.fail_json(msg="servers must contain at least one hostname or IP address")
    invalid = [server for server in servers if not _valid_server(server)]
    if invalid:
        module.fail_json(msg=f"Invalid NTP server hostname or IP address: {invalid[0]}")

    desired = (
        {"enabled": False, "mode": "unicast", "servers": [], "vrf": "main"}
        if params["state"] == "absent"
        else {"enabled": params["enabled"], "mode": params["mode"], "servers": servers, "vrf": params["vrf"]}
    )
    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"],
    )
    try:
        current = client.get("system/ntp/client")
        if isinstance(current, list):
            current = current[0] if current else {}
        if not isinstance(current, dict):
            module.fail_json(msg="RouterOS NTP client response was not an object")
        changes = {}
        if not _bool_matches(current.get("enabled", "no"), desired["enabled"]):
            changes["enabled"] = desired["enabled"]
        if str(current.get("mode", "")) != desired["mode"]:
            changes["mode"] = desired["mode"]
        if _servers(current.get("servers", "")) != desired["servers"]:
            changes["servers"] = desired["servers"]
        if str(current.get("vrf", "")) != desired["vrf"]:
            changes["vrf"] = desired["vrf"]
        if not changes:
            module.exit_json(changed=False, ntp_client=current, changed_fields=[])
        payload = dict(changes)
        if "servers" in payload:
            payload["servers"] = ",".join(payload["servers"])
        result = {**current, **changes} if module.check_mode else client.post("system/ntp/client/set", payload)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
    module.exit_json(changed=True, ntp_client=result, changed_fields=list(changes))


if __name__ == "__main__":
    main()

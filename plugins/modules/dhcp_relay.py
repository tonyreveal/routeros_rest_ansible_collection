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
module: dhcp_relay
short_description: Manage or gather RouterOS dhcp relay information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Creates, updates, or removes one RouterOS DHCP relay.
  - Requires a relay name, interface, at least one DHCP server address, and local address when present.
  - Supports optional relay-agent information and validates the required remote ID when enabled.
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
  name:
    description: Unique name of the DHCP relay.
    type: str
    required: true
  interface:
    description: Interface on which the relay listens.
    type: str
    required: true
  dhcp_servers:
    description: One or more DHCP server IPv4 or IPv6 addresses.
    type: list
    elements: str
    required: true
  local_address:
    description: Unique IP address used by the DHCP relay.
    type: str
    required: true
  enabled:
    description: Whether the DHCP relay should be enabled.
    type: bool
    default: true
  vrf:
    description: VRF used by the DHCP relay.
    type: str
    default: main
  delay_threshold:
    description: Delay threshold using RouterOS time syntax.
    type: str
    default: 0s
  local_address_as_src_ip:
    description: Use local_address as the source IP for packets sent to DHCP servers.
    type: bool
    default: false
  add_relay_info:
    description: Add DHCP relay agent information according to RFC 3046.
    type: bool
    default: false
  relay_info_remote_id:
    description: Remote ID used when add_relay_info is enabled.
    type: str
  state:
    description: Whether the DHCP relay should exist.
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
- name: Configure a DHCP relay
  mikrotik.routeros.dhcp_relay:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    name: relay-vlan10
    interface: vlan10
    dhcp_servers:
      - 192.0.2.10
      - 192.0.2.11
    local_address: 192.0.2.1
    enabled: true
    vrf: main
    delay_threshold: 0s
    local_address_as_src_ip: true
    add_relay_info: true
    relay_info_remote_id: switch-01

- name: Remove a DHCP relay
  mikrotik.routeros.dhcp_relay:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    name: relay-vlan10
    interface: vlan10
    dhcp_servers:
      - 192.0.2.10
    local_address: 192.0.2.1
    state: absent
...
"""


RETURN = r"""
relay:
  description: RouterOS DHCP relay record returned after reconciliation.
  returned: success
  type: raw
changed_fields:
  description: Fields changed during this invocation.
  returned: success
  type: list
"""


def _first_record(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value if isinstance(value, dict) else None


def _bool_matches(current, desired):
    return (str(current).lower() in {"yes", "true"}) == desired


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "interface": {"type": "str", "required": True},
            "dhcp_servers": {"type": "list", "elements": "str", "required": True, "min": 1},
            "local_address": {"type": "str", "required": True},
            "enabled": {"type": "bool", "default": True},
            "vrf": {"type": "str", "default": "main"},
            "delay_threshold": {"type": "str", "default": "0s"},
            "local_address_as_src_ip": {"type": "bool", "default": False},
            "add_relay_info": {"type": "bool", "default": False},
            "relay_info_remote_id": {"type": "str"},
            "state": {"type": "str", "default": "present", "choices": ["absent", "present"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    if params["state"] == "present" and params["add_relay_info"] and not params.get("relay_info_remote_id"):
        module.fail_json(msg="relay_info_remote_id is required when add_relay_info is true")
    try:
        ipaddress.ip_address(params["local_address"])
        for server in params["dhcp_servers"]:
            ipaddress.ip_address(server)
    except ValueError as exc:
        module.fail_json(msg=f"local_address and dhcp_servers must contain valid IP addresses: {exc}")

    desired = {
        "name": params["name"],
        "interface": params["interface"],
        "dhcp-server": ",".join(dict.fromkeys(params["dhcp_servers"])),
        "local-address": params["local_address"],
        "disabled": not params["enabled"],
        "vrf": params["vrf"],
        "delay-threshold": params["delay_threshold"],
        "local-address-as-src-ip": params["local_address_as_src_ip"],
        "add-relay-info": params["add_relay_info"],
    }
    if params.get("relay_info_remote_id") is not None:
        desired["relay-info-remote-id"] = params["relay_info_remote_id"]

    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"],
    )
    try:
        existing = _first_record(client.get("ip/dhcp-relay", query={"name": params["name"]}))
        if params["state"] == "absent":
            if existing is None:
                module.exit_json(changed=False, relay={}, changed_fields=[])
            resource_id = existing.get(".id")
            if not resource_id:
                module.fail_json(msg="RouterOS DHCP relay response did not include .id")
            result = existing if module.check_mode else client.delete(f"ip/dhcp-relay/{resource_id}")
            module.exit_json(changed=True, relay=result, changed_fields=["relay"])

        if existing is None:
            result = desired if module.check_mode else client.put("ip/dhcp-relay", desired)
            module.exit_json(changed=True, relay=result, changed_fields=list(desired))

        resource_id = existing.get(".id")
        if not resource_id:
            module.fail_json(msg="RouterOS DHCP relay response did not include .id")
        changes = {}
        for key, value in desired.items():
            if key in {"disabled", "local-address-as-src-ip", "add-relay-info"}:
                if not _bool_matches(existing.get(key, "no"), value):
                    changes[key] = value
            elif str(existing.get(key, "")) != str(value):
                changes[key] = value
        if not changes:
            module.exit_json(changed=False, relay=existing, changed_fields=[])
        result = changes if module.check_mode else client.patch(f"ip/dhcp-relay/{resource_id}", changes)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, relay=result, changed_fields=list(changes))


if __name__ == "__main__":
    main()

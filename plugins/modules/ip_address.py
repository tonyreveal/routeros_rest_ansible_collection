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
module: ip_address
short_description: Manage or gather RouterOS ip address information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Creates, updates, or removes one RouterOS IP address entry.
  - Uses the address and interface together as the resource identity.
  - The enabled input is mapped to the RouterOS disabled property.
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
  address:
    description: IP address in CIDR notation, such as 192.0.2.1/24.
    type: str
    required: true
  interface:
    description: RouterOS interface to which the address is assigned.
    type: str
    required: true
  enabled:
    description: Whether the IP address entry should be enabled.
    type: bool
    default: true
  network:
    description: Optional network address associated with the entry.
    type: str
  comment:
    description: Optional comment for the IP address entry.
    type: str
  state:
    description: Whether the IP address entry should exist.
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
- name: Add an enabled address
  mikrotik.routeros.ip_address:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    address: 192.0.2.1/24
    interface: ether1
    enabled: true
    network: 192.0.2.0
    comment: Router management address

- name: Disable an address without removing it
  mikrotik.routeros.ip_address:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    address: 192.0.2.1/24
    interface: ether1
    enabled: false

- name: Remove an address
  mikrotik.routeros.ip_address:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    address: 192.0.2.1/24
    interface: ether1
    state: absent
...
"""


RETURN = r"""
address:
  description: RouterOS IP address record returned after reconciliation.
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


def _routeros_enabled(value):
    return str(value).lower() in {"no", "false"}


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "address": {"type": "str", "required": True},
            "interface": {"type": "str", "required": True},
            "enabled": {"type": "bool", "default": True},
            "network": {"type": "str"},
            "comment": {"type": "str"},
            "state": {"type": "str", "default": "present", "choices": ["absent", "present"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    try:
        ipaddress.ip_interface(params["address"])
        if params.get("network"):
            ipaddress.ip_address(params["network"])
    except ValueError as exc:
        module.fail_json(msg=f"address and network must be valid IP values: {exc}")

    desired = {
        "address": params["address"],
        "interface": params["interface"],
        "disabled": not params["enabled"],
    }
    if params.get("network") is not None:
        desired["network"] = params["network"]
    if params.get("comment") is not None:
        desired["comment"] = params["comment"]

    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"],
    )
    try:
        records = client.get("ip/address", query={"address": params["address"], "interface": params["interface"]})
        existing = _first_record(records)
        if params["state"] == "absent":
            if existing is None:
                module.exit_json(changed=False, address={}, changed_fields=[])
            resource_id = existing.get(".id")
            if not resource_id:
                module.fail_json(msg="RouterOS IP address response did not include .id")
            if not module.check_mode:
                result = client.delete(f"ip/address/{resource_id}")
            else:
                result = existing
            module.exit_json(changed=True, address=result, changed_fields=["address"])

        if existing is None:
            result = desired if module.check_mode else client.put("ip/address", desired)
            module.exit_json(changed=True, address=result, changed_fields=list(desired))

        resource_id = existing.get(".id")
        if not resource_id:
            module.fail_json(msg="RouterOS IP address response did not include .id")
        changes = {}
        for key, value in desired.items():
            if key == "disabled":
                if _routeros_enabled(existing.get(key, "no")) != value:
                    changes[key] = value
            elif str(existing.get(key, "")) != str(value):
                changes[key] = value
        if not changes:
            module.exit_json(changed=False, address=existing, changed_fields=[])
        result = changes if module.check_mode else client.patch(f"ip/address/{resource_id}", changes)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, address=result, changed_fields=list(changes))


if __name__ == "__main__":
    main()

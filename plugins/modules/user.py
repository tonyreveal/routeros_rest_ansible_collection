#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations

import ipaddress
import base64
import hashlib

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r"""
---
module: user
short_description: Manage or gather RouterOS user information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Creates a RouterOS user when the requested username does not exist.
  - Updates the user's group, inactivity settings, and allowed address only when they differ.
  - Deletes the user when state is absent.
  - Maps role values full, read, and write to the RouterOS user groups of the same name.
  - The module does not create Ansible facts.
  - Passwords cannot be read back from RouterOS, so password updates default to creation-only for idempotency.
version_added: 1.0.0
author:
  - Tony Reveal (https://github.com/tonyreveal)
options:
  host:
    description: RouterOS REST base URL.
    type: str
    required: true
  username:
    description: RouterOS REST username used to manage the target user.
    type: str
    required: true
  password:
    description: Password to set for the target user.
    type: str
    required: true
    no_log: true
  name:
    description: Username to create or manage.
    type: str
    required: true
  user_password:
    description: Password for the target RouterOS user.
    type: str
    required: false
    no_log: true
  state:
    description: Whether the user should exist.
    type: str
    choices: [absent, present]
    default: present
  role:
    description: RouterOS user group to assign.
    type: str
    choices: [full, read, write]
    default: read
  inactivity_timeout:
    description: Inactivity timeout using RouterOS time syntax.
    type: str
    default: 10m
  inactivity_policy:
    description: Action taken after the inactivity timeout.
    type: str
    choices: [none, lockscreen, logout]
    default: none
  address:
    description: Optional single allowed source address or network in CIDR notation.
    type: str
  ssh_public_key:
    description: Optional single public SSH key in OpenSSH format.
    type: str
    no_log: true
  update_password:
    description: Whether to update the password for an existing user.
    type: str
    choices: [on_create, always]
    default: on_create
notes:
  - Use HTTPS and validate_certs=true in production.
  - The REST API requires the www-ssl or www service to be enabled on RouterOS.
  - Passwords are sensitive and should come from Ansible Vault or another secret manager.
requirements:
  - Python 3
  - RouterOS 7.x with the www-ssl or www REST service enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Create a read-only RouterOS user
  mikrotik.routeros.user:
    host: https://192.0.2.1
    username: "{{ vault_admin_username }}"
    password: "{{ vault_admin_password }}"
    name: auditor
    user_password: "{{ vault_auditor_password }}"
    role: read
    inactivity_timeout: 10m
    inactivity_policy: none
    address: 192.0.2.0/24
    ssh_public_key: "{{ vault_auditor_ssh_public_key }}"

- name: Rotate an existing user's password
  mikrotik.routeros.user:
    host: https://192.0.2.1
    username: "{{ vault_admin_username }}"
    password: "{{ vault_admin_password }}"
    name: operator
    user_password: "{{ vault_operator_password }}"
    role: write
    update_password: always

- name: Remove a RouterOS user
  mikrotik.routeros.user:
    host: https://192.0.2.1
    username: "{{ vault_admin_username }}"
    password: "{{ vault_admin_password }}"
    name: former-user
    state: absent
...
"""


RETURN = r"""
user:
  description: RouterOS user record returned after creation or update.
  returned: success
  type: raw
changed_fields:
  description: Non-secret fields changed during this invocation.
  returned: success
  type: list
state:
  description: Requested user state.
  returned: always
  type: str
"""


def _first_record(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value if isinstance(value, dict) else None


def _redact_password(value):
    """Prevent an unexpected password field from being returned to Ansible."""
    if isinstance(value, dict):
        return {key: value for key, value in value.items() if key not in {"password", "user_password"}}
    if isinstance(value, list):
        return [_redact_password(item) for item in value]
    return value


def _ssh_key_fingerprint(public_key: str) -> str:
    """Return the OpenSSH SHA256 fingerprint payload for a public key."""
    fields = public_key.split()
    try:
        key_blob = base64.b64decode(fields[1], validate=True)
    except (IndexError, ValueError) as exc:
        raise ValueError("ssh_public_key must be a valid OpenSSH public key") from exc
    return base64.b64encode(hashlib.sha256(key_blob).digest()).decode("ascii").rstrip("=")


def _validate_ssh_public_key(public_key: str) -> str:
    fields = public_key.split()
    if len(fields) < 2 or not fields[0].startswith(("ssh-", "ecdsa-")):
        raise ValueError("ssh_public_key must use OpenSSH public-key format")
    _ssh_key_fingerprint(public_key)
    return fields[1]


def _key_matches(record, public_key: str, fingerprint: str) -> bool:
    return record.get("key") == public_key or record.get("key") == public_key.split()[1] or record.get("fingerprint", "").removeprefix("SHA256:") == fingerprint


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "user_password": {"type": "str", "no_log": True},
            "state": {"type": "str", "default": "present", "choices": ["absent", "present"]},
            "role": {"type": "str", "default": "read", "choices": ["full", "read", "write"]},
            "inactivity_timeout": {"type": "str", "default": "10m"},
            "inactivity_policy": {"type": "str", "default": "none", "choices": ["none", "lockscreen", "logout"]},
            "address": {"type": "str"},
            "ssh_public_key": {"type": "str", "no_log": True},
            "update_password": {"type": "str", "default": "on_create", "choices": ["on_create", "always"], "no_log": True},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    if params["state"] == "present" and not params.get("user_password") and not params.get("ssh_public_key"):
        module.fail_json(msg="user_password is required when state is present unless ssh_public_key is supplied")
    if params["state"] == "absent" and params.get("update_password") == "always":
        module.fail_json(msg="update_password=always cannot be used when state is absent")
    if params.get("address") is not None:
        try:
            ipaddress.ip_network(params["address"], strict=False)
        except ValueError as exc:
            module.fail_json(msg=f"address must be a valid CIDR network: {exc}")
    ssh_public_key = params.get("ssh_public_key")
    if ssh_public_key:
        try:
            _validate_ssh_public_key(ssh_public_key)
            ssh_fingerprint = _ssh_key_fingerprint(ssh_public_key)
        except ValueError as exc:
            module.fail_json(msg=str(exc))

    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"],
    )
    desired = {
        "name": params["name"],
        "group": params["role"],
        "inactivity-timeout": params["inactivity_timeout"],
        "inactivity-policy": params["inactivity_policy"],
    }
    if params.get("address") is not None:
        desired["address"] = params["address"]

    try:
        records = client.get("user", query={"name": params["name"]})
        if not isinstance(records, list):
            records = [records]
        existing = _first_record(records)
        changed_fields = []
        if params["state"] == "absent":
            if existing is None:
                result = {}
                changed = False
            else:
                resource_id = existing.get(".id")
                if not resource_id:
                    module.fail_json(msg="RouterOS user response did not include .id")
                if module.check_mode:
                    result = existing
                else:
                    result = client.delete(f"user/{resource_id}")
                changed_fields = ["user"]
                changed = True
        elif ssh_public_key and existing is None:
            create_payload = {**desired, "password": params["user_password"]}
            result = create_payload if module.check_mode else client.put("user", create_payload)
            changed_fields = list(desired)
            if params["update_password"] == "on_create":
                changed_fields.append("password")
            changed_fields.append("ssh_public_key")
            if not module.check_mode:
                client.put("user/ssh-keys", {"user": params["name"], "key": ssh_public_key})
            changed = True
        elif existing is None:
            create_payload = {**desired, "password": params["user_password"]}
            result = create_payload if module.check_mode else client.put("user", create_payload)
            changed_fields = list(desired)
            if params["update_password"] == "on_create":
                changed_fields.append("password")
            changed = True
        else:
            resource_id = existing.get(".id")
            if not resource_id:
                module.fail_json(msg="RouterOS user response did not include .id")
            updates = {
                key: value for key, value in desired.items()
                if str(existing.get(key, "")) != str(value)
            }
            if params["update_password"] == "always":
                updates["password"] = params["user_password"]
            if updates:
                result = updates if module.check_mode else client.patch(f"user/{resource_id}", updates)
                changed_fields = [key for key in updates if key != "password"]
                if "password" in updates:
                    changed_fields.append("password")
                changed = True
            else:
                result = existing
                changed = False

            if ssh_public_key:
                key_records = client.get("user/ssh-keys", query={"user": params["name"]})
                if not isinstance(key_records, list):
                    key_records = [key_records]
                matching = any(_key_matches(record, ssh_public_key, ssh_fingerprint) for record in key_records if isinstance(record, dict))
                if not matching:
                    if len(key_records) > 1:
                        module.fail_json(msg="RouterOS user has multiple SSH keys; refusing to replace them when only one ssh_public_key is requested")
                    if key_records and not module.check_mode:
                        key_id = key_records[0].get(".id")
                        if not key_id:
                            module.fail_json(msg="RouterOS SSH key response did not include .id")
                        client.delete(f"user/ssh-keys/{key_id}")
                    if not module.check_mode:
                        client.put("user/ssh-keys", {"user": params["name"], "key": ssh_public_key})
                    changed_fields.append("ssh_public_key")
                    changed = True
    except RouterOSRestError as exc:
        if params["state"] == "present" and params["update_password"] == "always" and any(
            text in str(exc).lower()
            for text in ("session closed", "connection closed", "closed", "reset", "reboot")
        ):
            module.exit_json(
                changed=True,
                state=params["state"],
                user={"name": params["name"]},
                changed_fields=["password"],
                msg="RouterOS closed the session after accepting the password change.",
            )
        module.fail_json(msg=str(exc))

    module.exit_json(
        changed=changed,
        state=params["state"],
        user=_redact_password(result),
        changed_fields=changed_fields,
    )


if __name__ == "__main__":
    main()

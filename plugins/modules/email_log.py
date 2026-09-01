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
module: email_log
short_description: Manage or gather RouterOS email log information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Creates or updates a named RouterOS logging action with target email.
  - The target is fixed to email and is not user-configurable.
  - Supports state=absent to remove the named email action.
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
    description: Name of the email logging action.
    type: str
    required: true
  email:
    description: Email address to which logs are sent.
    type: str
    required: true
  cc_email:
    description: Optional CC email address.
    type: str
    default: ''
  comment:
    description: Optional action comment.
    type: str
    default: ''
  start_tls:
    description: Whether the email action uses STARTTLS.
    type: bool
    default: false
  state:
    description: Whether the email logging action should exist.
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
- name: Configure an email logging action
  mikrotik.routeros.email_log:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    name: email-alerts
    email: alerts@example.com
    cc_email: noc@example.com
    comment: Critical system alerts
    start_tls: true

- name: Remove an email logging action
  mikrotik.routeros.email_log:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    name: email-alerts
    email: alerts@example.com
    state: absent
...
"""


RETURN = r"""
action:
  description: RouterOS email action returned after reconciliation.
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


def _bool_matches(current, desired):
    return (str(current).lower() in {"yes", "true"}) == desired


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "email": {"type": "str", "required": True},
            "cc_email": {"type": "str", "default": ""},
            "comment": {"type": "str", "default": ""},
            "start_tls": {"type": "bool", "default": False},
            "state": {"type": "str", "default": "present", "choices": ["absent", "present"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")

    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"],
    )
    try:
        existing = _first_record(client.get("system/logging/action", query={"name": params["name"]}))
        if params["state"] == "absent":
            if existing is None:
                module.exit_json(changed=False, action={}, changed_fields=[])
            resource_id = existing.get(".id")
            if not resource_id:
                module.fail_json(msg="RouterOS email action response did not include .id")
            result = existing if module.check_mode else client.delete(f"system/logging/action/{resource_id}")
            module.exit_json(changed=True, action=result, changed_fields=["action"])

        desired = {
            "name": params["name"],
            "target": "email",
            "email-to": params["email"],
            "email-cc": params["cc_email"],
            "comment": params["comment"],
            "email-start-tls": params["start_tls"],
        }
        if existing is None:
            result = desired if module.check_mode else client.put("system/logging/action", desired)
            module.exit_json(changed=True, action=result, changed_fields=list(desired))

        resource_id = existing.get(".id")
        if not resource_id:
            module.fail_json(msg="RouterOS email action response did not include .id")
        changes = {}
        for key, value in desired.items():
            if key == "email-start-tls":
                if not _bool_matches(existing.get(key, "no"), value):
                    changes[key] = value
            elif str(existing.get(key, "")) != str(value):
                changes[key] = value
        if not changes:
            module.exit_json(changed=False, action=existing, changed_fields=[])
        result = {**existing, **changes} if module.check_mode else client.patch(
            f"system/logging/action/{resource_id}", changes
        )
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, action=result, changed_fields=list(changes))


if __name__ == "__main__":
    main()

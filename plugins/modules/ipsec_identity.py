#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.resource import matches

DOCUMENTATION = r"""
---
module: ipsec_identity
short_description: Manage RouterOS IPsec identities through the REST API
description:
  - Creates, updates, or removes an IPsec identity.
  - The settings dictionary contains RouterOS IPsec identity properties.
version_added: '1.0.0'
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
    description: IPsec identity name.
    type: str
    required: true
  settings:
    description: RouterOS IPsec identity properties.
    type: dict
    required: true
    suboptions:
      peer:
        description: IPsec peer name.
        type: str
        required: true
      auth_method:
        description: Authentication method.
        type: str
      secret:
        description: Pre-shared secret.
        type: str
        no_log: true
      remote_id:
        description: Remote identity matcher.
        type: str
  state:
    description: Desired identity state.
    type: str
    choices: [present, absent]
    default: present
  validate_certs:
    description: Validate the RouterOS TLS certificate.
    type: bool
    default: true
  timeout:
    description: HTTP timeout in seconds.
    type: int
    default: 30
requirements:
  - Python 3.
  - RouterOS 7.x with REST API enabled.
  - Ansible 2.16 or newer.
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.org/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "settings": {"type": "dict", "required": True},
            "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    peer = settings.get("peer")
    if not peer:
        module.fail_json(msg="settings.peer is required for an IPsec identity")

    client = RouterOSRestClient(
        host=p["host"],
        username=p["username"],
        password=p["password"],
        timeout=p["timeout"],
        validate_certs=p["validate_certs"],
    )
    desired = {"peer": peer, "comment": p["name"], **settings}
    try:
        records = client.get("ip/ipsec/identity")
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
    if not isinstance(records, list):
        records = [records]
    remote_id = settings.get("remote-id")
    existing = next(
        (
            record
            for record in records
            if record.get("peer") == peer
            and (
                (remote_id is not None and record.get("remote-id") == remote_id)
                or (remote_id is None and record.get("comment") == p["name"])
            )
        ),
        None,
    )

    if p["state"] == "absent":
        if existing is None:
            module.exit_json(changed=False, identity={}, changed_fields=[])
        identity_id = existing.get(".id")
        if not identity_id:
            module.fail_json(msg="RouterOS IPsec identity response did not include .id")
        result = existing if module.check_mode else client.delete(f"ip/ipsec/identity/{identity_id}")
        module.exit_json(changed=True, identity=result, changed_fields=["identity"])

    if existing is None:
        result = desired if module.check_mode else client.put("ip/ipsec/identity", desired)
        module.exit_json(changed=True, identity=result, changed_fields=list(desired))

    changes = {
        key: value
        for key, value in desired.items()
        if not matches(existing.get(key, ""), value)
    }
    if not changes:
        module.exit_json(changed=False, identity=existing, changed_fields=[])
    identity_id = existing.get(".id")
    if not identity_id:
        module.fail_json(msg="RouterOS IPsec identity response did not include .id")
    result = {**existing, **changes} if module.check_mode else client.patch(
        f"ip/ipsec/identity/{identity_id}", changes
    )
    module.exit_json(changed=True, identity=result, changed_fields=list(changes))


if __name__ == "__main__":
    main()

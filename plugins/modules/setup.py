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
module: setup
short_description: Manage or gather RouterOS setup information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Reads selected RouterOS system and configuration menus using the RouterOS REST API.
  - Returns the data under ansible_facts.routeros_facts.
  - RouterOS REST API must be enabled on the device.
  - REST API responses commonly encode RouterOS values as strings; this module preserves those values.
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
  gather_subset:
    description:
      - Fact groups to collect. Use !group to remove a group from all.
      - The all group collects every supported group.
    type: list
    elements: str
    default:
      - all
    choices:
      - all
      - system
      - identity
      - routerboard
      - packages
      - interfaces
      - ip_addresses
      - routes
      - services
      - "!all"
notes:
  - Use HTTPS and validate_certs=true in production.
  - The REST API requires the www-ssl or www service to be enabled on RouterOS.
  - Fact collection is read-only and is safe to use in check mode.
requirements:
  - Python 3
  - RouterOS 7.x with REST API enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Gather RouterOS facts
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Collect system and interface facts
      mikrotik.routeros.setup:
        host: https://192.0.2.1
        username: "{{ vault_routeros_username }}"
        password: "{{ vault_routeros_password }}"
        validate_certs: true
        gather_subset:
          - system
          - identity
          - interfaces
      register: routeros_device_facts

    - name: Show RouterOS version
      ansible.builtin.debug:
        msg: "{{ routeros_device_facts.ansible_facts.routeros_facts.system[0].version }}"
...
"""


RETURN = r"""
ansible_facts:
  description: Facts collected from RouterOS.
  returned: always
  type: dict
  contains:
    routeros_facts:
      description: Fact groups requested by gather_subset.
      type: dict
      returned: always
      sample:
        system:
          - platform: MikroTik
            version: 7.24
        identity:
          - name: edge-router
"""


FACT_ENDPOINTS = {
    "system": "system/resource",
    "identity": "system/identity",
    "routerboard": "system/routerboard",
    "packages": "system/package",
    "interfaces": "interface",
    "ip_addresses": "ip/address",
    "routes": "ip/route",
    "services": "ip/service",
}


def _selected_subsets(requested: list[str]) -> list[str]:
    """Resolve Ansible-style include/exclude subset names deterministically."""
    all_groups = list(FACT_ENDPOINTS)
    if "all" in requested:
        selected = all_groups.copy()
    else:
        selected = [item for item in requested if not item.startswith("!") and item in FACT_ENDPOINTS]
    for item in requested:
        if item.startswith("!") and item[1:] == "all":
            selected = []
    return selected


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
            "gather_subset": {
                "type": "list",
                "elements": "str",
                "default": ["all"],
            },
        },
        supports_check_mode=True,
    )

    if module.params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")

    selected = _selected_subsets(module.params["gather_subset"])
    client = RouterOSRestClient(
        host=module.params["host"],
        username=module.params["username"],
        password=module.params["password"],
        timeout=module.params["timeout"],
        validate_certs=module.params["validate_certs"],
    )

    facts = {}
    try:
        for subset in selected:
            value = client.get(FACT_ENDPOINTS[subset])
            facts[subset] = value if isinstance(value, list) else [value]
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=False, ansible_facts={"routeros_facts": facts})


if __name__ == "__main__":
    main()

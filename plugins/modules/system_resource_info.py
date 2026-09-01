#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.info import run_info

DOCUMENTATION = r"""
---
module: system_resource_info
short_description: Manage or gather RouterOS system resource info information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Reads system resource records from RouterOS.
  - Returns data in the registered module result and never creates Ansible facts.
  - The module is read-only and idempotent by nature.
version_added: 1.0.0
author:
  - Tony Reveal (https://github.com/tonyreveal)
requirements:
  - Python 3
  - RouterOS 7.x with REST API enabled
  - Ansible 2.16 or newer
options:
  host:
    description: RouterOS REST base URL, such as https://192.0.2.1.
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
  validate_certs:
    description: Validate the TLS certificate presented by RouterOS.
    type: bool
    default: true
  timeout:
    description: HTTP request timeout in seconds.
    type: int
    default: 30
  name:
    description: Optional RouterOS selector value.
    type: str
  object_id:
    description: Optional RouterOS internal object ID, such as '*1'.
    type: str
notes:
  - Use HTTPS and validate_certs=true in production.
  - Register the result to consume the returned information.
"""

EXAMPLES = r"""
---
- name: Gather system resource
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Read system resource
      mikrotik.routeros_rest.system_resource_info:
        host: https://192.0.2.1
        username: "{{ vault_routeros_username }}"
        password: "{{ vault_routeros_password }}"
      register: routeros_system_resource_info

    - name: Show returned data
      ansible.builtin.debug:
        var: routeros_system_resource_info.resource
...
"""

RETURN = r"""
resource:
  description: Records returned by the corresponding RouterOS REST menu.
  returned: always
  type: dict
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
            "name": {"type": "str"},
            "object_id": {"type": "str"},
        },
        mutually_exclusive=[["name", "object_id"]],
        supports_check_mode=True,
    )
    if module.params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    run_info(module, "system/resource", "resource", None)


if __name__ == "__main__":
    main()

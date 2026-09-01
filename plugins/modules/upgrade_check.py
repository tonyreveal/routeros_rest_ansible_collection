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
module: upgrade_check
short_description: Manage or gather RouterOS upgrade check information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Runs the RouterOS package update check-for-updates command through REST.
  - Returns the RouterOS update response directly in the registered result.
  - Does not install packages, reboot the device, or create Ansible facts.
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
- name: Check RouterOS for an available upgrade
  mikrotik.routeros.upgrade_check:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
  register: upgrade_check

- name: Display update response
  ansible.builtin.debug:
    var: upgrade_check.result
...
"""


RETURN = r"""
result:
  description: Raw response from /system/package/update/check-for-updates.
  returned: success
  type: raw
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
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
        result = client.post("system/package/update/check-for-updates", {})
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
    module.exit_json(changed=False, result=result)


if __name__ == "__main__":
    main()

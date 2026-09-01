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
module: ip_address_info
short_description: Manage or gather RouterOS ip address info information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Reads configured and dynamic IPv4 address records from /ip/address.
  - Without a selector, returns all address records; name or address_id selects one record.
  - Returns address data directly in the registered module result.
  - The module is read-only and does not create Ansible facts.
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
  name:
    description:
      - Return only the IP address object with this RouterOS name, when supported by the device.
    type: str
    required: false
  address_id:
    description:
      - Return only the IP address object with this RouterOS internal ID, such as '*1'.
    type: str
    required: false
notes:
  - Use HTTPS and validate_certs=true in production.
  - The REST API requires the www-ssl or www service to be enabled on RouterOS.
  - RouterOS REST API values are commonly returned as strings and are preserved by this module.
requirements:
  - Python 3
  - RouterOS 7.x with REST API enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Gather RouterOS IP address information
  hosts: localhost
  gather_facts: false
  tasks:
    - name: Collect IP addresses
      mikrotik.routeros.ip_address_info:
        host: https://192.0.2.1
        username: "{{ vault_routeros_username }}"
        password: "{{ vault_routeros_password }}"
        validate_certs: true
        address_id: '*1'
      register: routeros_ip_address_result

    - name: Display IP addresses
      ansible.builtin.debug:
        var: routeros_ip_address_result.addresses
...
"""


RETURN = r"""
addresses:
  description: Records returned by the RouterOS /ip/address REST endpoint.
  returned: always
  type: list
  elements: dict
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
            "address_id": {"type": "str"},
        },
        mutually_exclusive=[["name", "address_id"]],
        supports_check_mode=True,
    )

    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")

    client = RouterOSRestClient(
        host=params["host"],
        username=params["username"],
        password=params["password"],
        timeout=params["timeout"],
        validate_certs=params["validate_certs"],
    )

    try:
        query = {}
        if params.get("name") is not None:
            query["name"] = params["name"]
        if params.get("address_id") is not None:
            query[".id"] = params["address_id"]
        addresses = client.get("ip/address", query=query)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    if not isinstance(addresses, list):
        addresses = [addresses]

    module.exit_json(changed=False, addresses=addresses)


if __name__ == "__main__":
    main()

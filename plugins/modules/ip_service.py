#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.resource import reconcile

DOCUMENTATION = r"""
---
module: ip_service
short_description: Manage RouterOS IP services
description:
  - Creates, updates, or removes RouterOS IP service entries through the REST API.
  - Use the C(certificate) option to assign a certificate to certificate-based services such as C(www-ssl).
  - The C(absent) state removes the named service entry.
version_added: '1.0.0'
author:
  - Tony Reveal (https://github.com/tonyreveal)
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description:
      - Supports check mode without changing the device.
    support: full
options:
  host:
    description:
      - RouterOS REST base URL, such as C(https://192.0.2.1).
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
  name:
    description:
      - RouterOS service name, such as C(www-ssl) or C(api-ssl).
    type: str
    required: true
  address:
    description:
      - Source addresses or address ranges from which the service accepts connections.
      - RouterOS receives the list as a comma-separated value.
    type: list
    elements: str
  port:
    description:
      - TCP port used by the service.
    type: int
  certificate:
    description:
      - Certificate name used by certificate-based services such as C(www-ssl).
    type: str
  disabled:
    description:
      - Whether the service is disabled.
    type: bool
    default: false
  state:
    description:
      - Desired service state.
    type: str
    choices:
      - present
      - absent
    default: present
  validate_certs:
    description:
      - Validate the TLS certificate presented by RouterOS.
    type: bool
    default: true
  timeout:
    description:
      - HTTP request timeout in seconds.
    type: int
    default: 30
requirements:
  - Python 3.
  - RouterOS 7.x with REST API enabled.
  - Ansible 2.16 or newer.
notes:
  - Use HTTPS and C(validate_certs=true) in production.
  - The RouterOS REST API must be enabled through the C(www) or C(www-ssl) service.
"""

EXAMPLES = r"""
---
- name: Enable WebFig HTTPS with a certificate
  mikrotik.routeros_rest.ip_service:
    host: https://192.0.2.1
    username: admin
    password: "{{ vault_routeros_password }}"
    name: www-ssl
    address:
      - 0.0.0.0/0
    port: 443
    certificate: router-cert
    disabled: false
    state: present

- name: Remove an unused IP service
  mikrotik.routeros_rest.ip_service:
    host: https://192.0.2.1
    username: admin
    password: "{{ vault_routeros_password }}"
    name: telnet
    state: absent
"""

RETURN = r"""
service:
  description:
    - RouterOS service record returned after reconciliation.
  returned: on change
  type: dict
"""


def main():
    m = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "address": {"type": "list", "elements": "str"},
            "port": {"type": "int"},
            "certificate": {"type": "str"},
            "disabled": {"type": "bool", "default": False},
            "state": {"type": "str", "default": "present", "choices": ["present", "absent"]},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = m.params
    d = {"name": p["name"], "disabled": p["disabled"]}
    for k, s in {"port": "port", "certificate": "certificate"}.items():
        if p.get(s) is not None:
            d[k] = p[s]
    if p.get("address") is not None:
        d["address"] = ",".join(address.strip() for address in p["address"])
    try:
        reconcile(
            m,
            RouterOSRestClient(p["host"], p["username"], p["password"], p["timeout"], p["validate_certs"]),
            "ip/service",
            {"name": p["name"]},
            d,
            p["state"],
            "service",
        )
    except RouterOSRestError as e:
        m.fail_json(msg=str(e))


if __name__ == "__main__":
    main()

#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: dns_static
short_description: Manage RouterOS static DNS records through the REST API
description:
  - Creates, updates, or removes a static DNS record.
  - The name identifies the record and settings contains RouterOS record properties.
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
    description: DNS name for the static record.
    type: str
    required: true
  settings:
    description:
      - RouterOS static DNS record properties.
      - The name is supplied separately and identifies the record.
    type: dict
    required: true
    suboptions:
      address:
        description: IPv4 or IPv6 address returned for A or AAAA records.
        type: str
      cname:
        description: Alias name for a CNAME record.
        type: str
      forward_to:
        description: DNS server address to which matching requests are forwarded.
        type: str
      mx_exchange:
        description: Mail exchange hostname.
        type: str
      ns:
        description: Authoritative name server hostname.
        type: str
      text:
        description: Text value for a TXT record.
        type: str
      srv_port:
        description: TCP or UDP port for an SRV record.
        type: int
        default: 0
      srv_target:
        description: Canonical hostname for an SRV record.
        type: str
      type:
        description: Static DNS record type.
        type: str
        choices: [A, AAAA, CNAME, FWD, MX, NS, NXDOMAIN, SRV, TXT]
        default: A
      address_list:
        description: Firewall address list to populate when the record matches.
        type: str
      comment:
        description: Comment describing the DNS record.
        type: str
      disabled:
        description: Whether the DNS record is disabled.
        type: bool
        default: false
      match_subdomain:
        description: Whether the record also matches subdomains.
        type: bool
        default: false
      mx_preference:
        description: Preference value for an MX record.
        type: int
        default: 0
      regexp:
        description: Case-sensitive regular expression for matching DNS names.
        type: str
      srv_priority:
        description: Priority value for an SRV record.
        type: int
        default: 0
      srv_weight:
        description: Weight value for an SRV record.
        type: int
        default: 0
      ttl:
        description: Maximum time-to-live for cached records.
        type: str
        default: 24h
  state:
    description: Desired record state.
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


EXAMPLES = r"""
---
- name: Create a static DNS record
  mikrotik.routeros_rest.dns_static:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    name: router.example.com
    settings:
      address: 192.0.2.10
      type: A
      ttl: 1h
      comment: Managed by Ansible
    state: present
...
"""

RETURN = r"""
resource:
  description: RouterOS static DNS resource returned after reconciliation.
  returned: always
  type: dict
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "name": {"type": "str", "required": True},
            "settings": {
                "type": "dict",
                "required": True,
                "options": {
                    "address": {"type": "str"},
                    "cname": {"type": "str"},
                    "forward-to": {"type": "str"},
                    "mx-exchange": {"type": "str"},
                    "ns": {"type": "str"},
                    "text": {"type": "str"},
                    "srv-port": {"type": "int", "default": 0},
                    "srv-target": {"type": "str"},
                    "type": {
                        "type": "str",
                        "choices": ["A", "AAAA", "CNAME", "FWD", "MX", "NS", "NXDOMAIN", "SRV", "TXT"],
                        "default": "A",
                    },
                    "address-list": {"type": "str"},
                    "comment": {"type": "str"},
                    "disabled": {"type": "bool", "default": False},
                    "match-subdomain": {"type": "bool", "default": False},
                    "mx-preference": {"type": "int", "default": 0},
                    "regexp": {"type": "str"},
                    "srv-priority": {"type": "int", "default": 0},
                    "srv-weight": {"type": "int", "default": 0},
                    "ttl": {"type": "str", "default": "24h"},
                },
            },
            "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "ip/dns/static", {"name": p["name"]}, {"name": p["name"], **settings})


if __name__ == "__main__":
    main()

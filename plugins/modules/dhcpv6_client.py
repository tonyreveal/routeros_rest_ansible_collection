#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: dhcpv6_client
short_description: Manage RouterOS DHCPv6 clients through the REST API
description:
  - Creates, updates, or removes a DHCPv6 client.
  - The settings dictionary contains RouterOS DHCPv6 client properties.
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
  interface:
    description: Interface identity for the DHCPv6 client.
    type: str
    required: true
  settings:
    description: RouterOS DHCPv6 client properties.
    type: dict
    required: true
    suboptions:
      pool_name:
        description: Name of the delegated prefix pool.
        type: str
      pool_prefix_length:
        description: Prefix length allocated from the delegated pool.
        type: int
      request:
        description: DHCPv6 information requested from the server.
        type: list
        elements: str
      use_peer_dns:
        description: Whether to use DNS servers supplied by the peer.
        type: bool
      add_default_route:
        description: Whether to install a default route.
        type: bool
      disabled:
        description: Whether the client is disabled.
        type: bool
  state:
    description: Desired resource state.
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


RETURN = r"""
resource:
  description: Reconciled DHCPv6 client resource.
  returned: always
  type: dict
"""


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "interface": {"type": "str", "required": True},
            "settings": {"type": "dict", "required": True},
            "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    run_config(module, "ipv6/dhcp-client", {"interface": p["interface"]}, {"interface": p["interface"], **settings})


if __name__ == "__main__":
    main()

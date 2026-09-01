#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: wireguard_peer
short_description: Manage RouterOS WireGuard peers through the REST API
description:
  - Creates, updates, or removes a WireGuard peer.
  - The settings dictionary contains the peer properties accepted by RouterOS.
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
    description: WireGuard interface containing the peer.
    type: str
    required: true
  public_key:
    description: Peer public key used to identify the peer.
    type: str
    required: true
  settings:
    description: WireGuard peer properties.
    type: dict
    required: true
    suboptions:
      allowed_address:
        description: Addresses routed to the peer.
        type: list
        elements: str
      endpoint_address:
        description: Peer endpoint address.
        type: str
      endpoint_port:
        description: Peer endpoint UDP port.
        type: int
      persistent_keepalive:
        description: Persistent keepalive interval.
        type: str
      preshared_key:
        description: Optional preshared key.
        type: str
        no_log: true
      comment:
        description: Comment describing the peer.
        type: str
      disabled:
        description: Whether the peer is disabled.
        type: bool
  state:
    description: Desired peer state.
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
            "interface": {"type": "str", "required": True},
            "public_key": {"type": "str", "required": True},
            "settings": {"type": "dict", "required": True},
            "state": {"type": "str", "choices": ["present", "absent"], "default": "present"},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    p = module.params
    settings = {key.replace("_", "-"): value for key, value in p["settings"].items()}
    payload = {"interface": p["interface"], "public-key": p["public_key"], **settings}
    run_config(module, "interface/wireguard/peers", {"public-key": p["public_key"]}, payload)


if __name__ == "__main__":
    main()

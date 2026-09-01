#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible_collections.mikrotik.routeros_rest.plugins.modules.firewall_filter import main

DOCUMENTATION = r"""
---
module: firewall_raw
short_description: Manage RouterOS IPv4 firewall raw rules through REST
description:
  - Creates, updates, and removes IPv4 firewall raw rules.
version_added: '1.0.0'
author:
  - Tony Reveal (https://github.com/tonyreveal)
options:
  host:
    type: str
    required: true
  username:
    type: str
    required: true
  password:
    type: str
    required: true
    no_log: true
  name:
    type: str
    required: true
  rule:
    type: dict
    required: true
  state:
    type: str
    choices: [present, absent]
    default: present
  validate_certs:
    type: bool
    default: true
  timeout:
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


if __name__ == "__main__":
    main("ip/firewall/raw")

#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config

DOCUMENTATION = r"""
---
module: queue_type
short_description: Manage RouterOS queue types through the REST API
description:
  - Creates, updates, or removes a queue type.
  - The settings dictionary contains RouterOS queue type properties.
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
    description: Queue type name.
    type: str
    required: true
  settings:
    description: RouterOS queue type properties.
    type: dict
    required: true
    suboptions:
      kind:
        description: Queue algorithm.
        type: str
      pcq_rate:
        description: PCQ rate per substream.
        type: str
      pcq_limit:
        description: PCQ queue size per substream.
        type: int
      pcq_classifier:
        description: PCQ classifier fields.
        type: list
        elements: str
      pfifo_limit:
        description: Packet FIFO limit.
        type: int
      red_avg_packet:
        description: RED average packet size.
        type: int
  state:
    description: Desired queue type state.
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
    run_config(module, "queue/type", {"name": p["name"]}, {"name": p["name"], **settings})


if __name__ == "__main__":
    main()

#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.config_resource import run_config


DOCUMENTATION = r"""
---
module: logging_action
short_description: Manage a RouterOS logging action
description:
  - Creates, updates, or removes a RouterOS logging action through the REST API.
version_added: 1.0.0
author:
  - Tony Reveal (https://github.com/tonyreveal)
requirements:
  - Python 3
  - RouterOS 7.x with REST API enabled
  - Ansible 2.16 or newer
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
    description: Logging action name.
    type: str
    required: true
  settings:
    description: Logging action properties.
    type: dict
    required: true
    suboptions:
      target:
        description: Logging target, such as memory, disk, echo, email, or remote.
        type: str
        required: true
      remote:
        description: Remote syslog address.
        type: str
      remote_port:
        description: Remote syslog port.
        type: int
      remote_log_format:
        description: Remote syslog message format.
        type: str
      remote_log_protocol:
        description: Remote syslog transport protocol.
        type: str
      vrf:
        description: VRF used to reach the remote logging server.
        type: str
      disk_file_name:
        description: Disk log file name.
        type: str
      disk_file_count:
        description: Number of retained disk files.
        type: int
      disk_lines_per_file:
        description: Maximum lines per disk file.
        type: int
      bsd_syslog:
        description: Whether BSD syslog format is enabled.
        type: bool
  state:
    description: Desired logging action state.
    type: str
    choices:
      - present
      - absent
    default: present
  validate_certs:
    description: Validate the RouterOS TLS certificate.
    type: bool
    default: true
  timeout:
    description: HTTP timeout in seconds.
    type: int
    default: 30
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
"""


EXAMPLES = r"""
---
- name: Configure a remote logging action
  mikrotik.routeros_rest.logging_action:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    name: remote-log
    settings:
      target: remote
      remote: 192.0.2.52
      remote_port: 514
      remote_log_format: default
      remote_log_protocol: TCP
      vrf: main
...
"""


RETURN = r"""
resource:
  description: RouterOS logging action returned after reconciliation.
  returned: success
  type: raw
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
    params = module.params
    settings = {}
    for key, value in params["settings"].items():
        api_key = {"remote_log_protocol": "remote-protocol"}.get(key, key.replace("_", "-"))
        settings[api_key] = value
    run_config(module, "system/logging/action", {"name": params["name"]}, {"name": params["name"], **settings})


if __name__ == "__main__":
    main()

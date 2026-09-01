#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.info import run_info

DOCUMENTATION = r'''
---
module: sstp_server_info
short_description: Gather SSTP server configuration
description:
  - Retrieves the RouterOS SSTP server configuration through the REST API.
  - The returned data is available in the registered module result and is not
    added to Ansible facts.
author:
  - Tony Reveal
version_added: "1.3.0"
requirements:
  - RouterOS 7 or later with REST API access.
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
    description: Validate the RouterOS TLS certificate.
    type: bool
    default: true
  timeout:
    description: HTTP timeout in seconds.
    type: int
    default: 30
notes:
  - This module is read-only and is effectively idempotent.
attributes:
  check_mode:
    support: full
'''


EXAMPLES = r'''
---
- name: Read SSTP server settings
  mikrotik.routeros_rest.sstp_server_info:
  register: sstp_server
'''

RETURN = r'''
server:
  description: SSTP server configuration records.
  returned: always
  type: list
  elements: dict
'''


def main():
    module = AnsibleModule(argument_spec={"host": {"type": "str", "required": True}, "username": {"type": "str", "required": True}, "password": {"type": "str", "required": True, "no_log": True}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30}}, supports_check_mode=True)
    run_info(module, "/interface/sstp-server/server", "server")


if __name__ == "__main__":
    main()

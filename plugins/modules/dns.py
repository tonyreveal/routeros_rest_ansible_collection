#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations
import ipaddress
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r"""
---
module: dns
short_description: Manage or gather RouterOS dns information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Adds or removes one or more DNS server addresses from the RouterOS DNS server list.
  - Reconciles only the requested server addresses and preserves other configured servers.
  - Configures optional RouterOS DNS settings using the supplied values or documented RouterOS defaults.
  - The module does not create Ansible facts.
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
  servers:
    description: One or more IPv4 or IPv6 DNS server addresses to add or remove.
    type: list
    elements: str
    required: true
  state:
    description: Whether the listed DNS servers should be present or absent.
    type: str
    choices: [absent, present]
    default: present
  allow_remote_requests:
    description: Allow the router to answer DNS requests from remote clients.
    type: bool
    default: false
  vrf:
    description: VRF used for DNS queries.
    type: str
    default: main
  max_udp_packet_size:
    description: Maximum UDP packet size.
    type: int
    default: 4096
  query_server_timeout:
    description: Per-server DNS query timeout using RouterOS time syntax.
    type: str
    default: 2s
  query_total_timeout:
    description: Total DNS query timeout using RouterOS time syntax.
    type: str
    default: 10s
  max_concurrent_queries:
    description: Maximum number of concurrent DNS queries.
    type: int
    default: 100
  max_concurrent_tcp_sessions:
    description: Maximum number of concurrent TCP DNS sessions.
    type: int
    default: 20
  cache_size:
    description: DNS cache size using RouterOS size syntax.
    type: str
    default: 2048KiB
  cache_max_ttl:
    description: Maximum DNS cache TTL using RouterOS time syntax.
    type: str
    default: 1w
  address_list_extra_time:
    description: Additional time for DNS address-list entries using RouterOS time syntax.
    type: str
    default: 0s
  mdns_repeater_interfaces:
    description: Interfaces on which mDNS repeater operates.
    type: list
    elements: str
    default: []
  use_doh_server:
    description: DNS-over-HTTPS server URL; an empty value disables DoH.
    type: str
    default: ''
  validate_certs:
    description: Validate the RouterOS www-ssl certificate.
    type: bool
    default: true
  timeout:
    description: HTTP request timeout in seconds.
    type: int
    default: 30
notes:
  - Use HTTPS and validate_certs=true in production.
  - The REST API requires the www-ssl or www service to be enabled on RouterOS.
  - RouterOS defaults can vary by RouterOS release; explicitly set values when exact policy is required.
requirements:
  - Python 3
  - RouterOS 7.x with the www-ssl or www REST service enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Configure RouterOS DNS
  mikrotik.routeros.dns:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    servers:
      - 1.1.1.1
      - 2606:4700:4700::1111
    state: present
    allow_remote_requests: true
    vrf: main
    use_doh_server: https://cloudflare-dns.com/dns-query

- name: Remove a DNS server without changing other DNS servers
  mikrotik.routeros.dns:
    host: https://192.0.2.1
    username: "{{ vault_routeros_username }}"
    password: "{{ vault_routeros_password }}"
    servers:
      - 1.1.1.1
    state: absent
...
"""


RETURN = r"""
dns:
  description: DNS settings returned after reconciliation.
  returned: success
  type: raw
changed_fields:
  description: DNS fields changed during this invocation.
  returned: success
  type: list
"""


def _normalise_servers(value):
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    return [item.strip() for item in str(value).split(",") if item.strip()]


def _same_value(current, desired):
    if isinstance(desired, bool):
        return str(current).lower() in {"yes", "true"} if desired else str(current).lower() in {"no", "false"}
    return str(current).lower() == str(desired).lower()


def _validate_servers(module, servers):
    for server in servers:
        try:
            ipaddress.ip_address(server)
        except ValueError as exc:
            module.fail_json(msg=f"servers must contain valid IP addresses: {exc}")


def main() -> None:
    module = AnsibleModule(
        argument_spec={
            "host": {"type": "str", "required": True},
            "username": {"type": "str", "required": True},
            "password": {"type": "str", "required": True, "no_log": True},
            "servers": {"type": "list", "elements": "str", "required": True, "min": 1},
            "state": {"type": "str", "default": "present", "choices": ["absent", "present"]},
            "allow_remote_requests": {"type": "bool", "default": False},
            "vrf": {"type": "str", "default": "main"},
            "max_udp_packet_size": {"type": "int", "default": 4096},
            "query_server_timeout": {"type": "str", "default": "2s"},
            "query_total_timeout": {"type": "str", "default": "10s"},
            "max_concurrent_queries": {"type": "int", "default": 100},
            "max_concurrent_tcp_sessions": {"type": "int", "default": 20},
            "cache_size": {"type": "str", "default": "2048KiB"},
            "cache_max_ttl": {"type": "str", "default": "1w"},
            "address_list_extra_time": {"type": "str", "default": "0s"},
            "mdns_repeater_interfaces": {"type": "list", "elements": "str", "default": []},
            "use_doh_server": {"type": "str", "default": ""},
            "validate_certs": {"type": "bool", "default": True},
            "timeout": {"type": "int", "default": 30},
        },
        supports_check_mode=True,
    )
    params = module.params
    if params["timeout"] <= 0:
        module.fail_json(msg="timeout must be greater than zero")
    if params["max_udp_packet_size"] <= 0 or params["max_concurrent_queries"] <= 0 or params["max_concurrent_tcp_sessions"] <= 0:
        module.fail_json(msg="DNS numeric limits must be greater than zero")

    requested_servers = list(dict.fromkeys(params["servers"]))
    _validate_servers(module, requested_servers)
    client = RouterOSRestClient(
        host=params["host"], username=params["username"], password=params["password"],
        timeout=params["timeout"], validate_certs=params["validate_certs"],
    )
    desired = {
        "allow-remote-requests": params["allow_remote_requests"],
        "vrf": params["vrf"],
        "max-udp-packet-size": params["max_udp_packet_size"],
        "query-server-timeout": params["query_server_timeout"],
        "query-total-timeout": params["query_total_timeout"],
        "max-concurrent-queries": params["max_concurrent_queries"],
        "max-concurrent-tcp-sessions": params["max_concurrent_tcp_sessions"],
        "cache-size": params["cache_size"],
        "cache-max-ttl": params["cache_max_ttl"],
        "address-list-extra-time": params["address_list_extra_time"],
        "mdns-repeat-ifaces": params["mdns_repeater_interfaces"],
        "use-doh-server": params["use_doh_server"],
    }

    try:
        current = client.get("ip/dns")
        if isinstance(current, list):
            current = current[0] if current else {}
        if not isinstance(current, dict):
            module.fail_json(msg="RouterOS DNS response was not an object")

        current_servers = _normalise_servers(current.get("servers"))
        if params["state"] == "present":
            new_servers = current_servers + [server for server in requested_servers if server not in current_servers]
        else:
            new_servers = [server for server in current_servers if server not in requested_servers]

        changes = {}
        if new_servers != current_servers:
            changes["servers"] = ",".join(new_servers)
        for key, value in desired.items():
            current_value = current.get(key)
            if key == "mdns-repeat-ifaces":
                current_value = _normalise_servers(current_value)
                value = _normalise_servers(value)
            if not _same_value(current_value, value):
                changes[key] = value

        if not changes:
            module.exit_json(changed=False, dns=current, changed_fields=[])
        if module.check_mode:
            result = {**current, **changes}
        else:
            result = client.post("ip/dns/set", changes)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))

    module.exit_json(changed=True, dns=result, changed_fields=list(changes))


if __name__ == "__main__":
    main()

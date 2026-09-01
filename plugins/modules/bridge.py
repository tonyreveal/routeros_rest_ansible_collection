#!/usr/bin/python
# Copyright: Tony Reveal
# GNU General Public License v3.0 or later (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.html)

from __future__ import annotations
import ipaddress
import re
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.mikrotik.routeros_rest.plugins.module_utils.routeros_rest import (
    RouterOSRestClient,
    RouterOSRestError,
)

DOCUMENTATION = r"""
---
module: bridge
short_description: Manage or gather RouterOS bridge information
seealso:
  - name: RouterOS REST API documentation
    link: https://help.mikrotik.com/docs/display/ROS/REST+API
attributes:
  check_mode:
    description: Supports check mode without changing the device.
    support: full
description:
  - Creates, updates, or removes one RouterOS bridge interface.
  - Supports bridge, VLAN filtering, STP, MLAG, and IGMP/MLD snooping settings.
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
  name:
    description: Bridge name.
    type: str
    required: true
  enabled:
    description: Enable the bridge.
    type: bool
    default: true
  comment:
    description: Bridge comment.
    type: str
  mtu:
    description: Bridge MTU.
    type: int
  arp:
    description: ARP behavior.
    type: str
    choices: [disabled, enabled, local-proxy-arp, proxy-arp, reply-only]
    default: enabled
  arp_timeout:
    description: ARP timeout.
    type: str
  admin_mac_address:
    description: Administrative MAC address.
    type: str
  ageing_time:
    description: MAC ageing time.
    type: str
  max_learned_entries:
    description: Maximum learned entries.
    type: raw
  dhcp_snooping:
    description: Enable DHCP snooping.
    type: bool
  dhcpv6_snooping:
    description: Enable DHCPv6 snooping.
    type: bool
  ra_guard:
    description: Enable Router Advertisement guard.
    type: bool
  fast_forward:
    description: Enable fast forwarding.
    type: bool
  vlan_filtering:
    description: Enable VLAN filtering.
    type: bool
    default: false
  pvid:
    description: Bridge PVID; required when VLAN filtering is enabled.
    type: int
  ether_type:
    description: VLAN EtherType.
    type: str
    choices: ['0x88a8', '0x8100', '0x9100']
    default: '0x8100'
  frame_types:
    description: Accepted frame types.
    type: str
    choices: [admit-all, admit-only-untagged-and-priority-tagged, admit-only-vlan-tagged]
    default: admit-all
  ingress_filtering:
    description: Enable ingress filtering.
    type: bool
    default: true
  mvrp:
    description: Enable MVRP.
    type: bool
    default: false
  mlag_peer_port:
    description: MLAG peer port; required when MLAG settings are supplied.
    type: str
  mlag_priority:
    description: MLAG election priority.
    type: int
    default: 128
  mlag_heartbeat:
    description: MLAG heartbeat interval.
    type: str
    default: 00:00:05
  stp_protocol_mode:
    description: Spanning Tree protocol mode.
    type: str
    choices: [none, stp, rstp, mstp]
    default: rstp
  stp_priority:
    description: STP bridge priority.
    type: raw
    default: '0x8000'
  port_cost_mode:
    description: Port cost mode.
    type: str
    choices: [short, long]
    default: long
  max_message_age:
    description: Maximum message age.
    type: str
    default: 00:00:20
  forward_delay:
    description: Forward delay.
    type: str
    default: 00:00:15
  transmit_hold_count:
    description: Transmit hold count.
    type: int
    default: 6
  max_hops:
    description: Maximum MSTP hops.
    type: int
    default: 20
  igmp_snooping:
    description: Enable IGMP/MLD snooping.
    type: bool
    default: false
  igmp_version:
    description: IGMP version.
    type: int
    choices: [2, 3]
    default: 2
  mld_version:
    description: MLD version.
    type: int
    choices: [1, 2]
    default: 1
  multicast_router:
    description: Multicast router mode.
    type: str
    choices: [disabled, permanent, temporary-query]
    default: temporary-query
  multicast_carrier:
    description: Enable multicast carrier.
    type: bool
    default: false
  querier_uses_bridge_address:
    description: Use the bridge address for IGMP queries.
    type: bool
    default: false
  startup_query_count:
    description: Startup query count.
    type: int
    default: 2
  last_member_query_count:
    description: Last-member query count.
    type: int
    default: 2
  last_member_interval:
    description: Last-member interval.
    type: str
    default: '1.00'
  membership_interval:
    description: Membership interval.
    type: str
    default: '260.00'
  querier_interval:
    description: Querier interval.
    type: str
    default: '255.00'
  query_interval:
    description: Query interval.
    type: str
    default: '125.00'
  query_response_interval:
    description: Query response interval.
    type: str
    default: '10.00'
  startup_query_interval:
    description: Startup query interval.
    type: str
    default: '31.25'
  state:
    description: Bridge lifecycle state.
    type: str
    choices: [absent, present]
    default: present
  validate_certs:
    description: Validate TLS certificate.
    type: bool
    default: true
  timeout:
    description: HTTP timeout in seconds.
    type: int
    default: 30
requirements:
  - Python 3
  - RouterOS 7.x with REST enabled
  - Ansible 2.16 or newer
"""


EXAMPLES = r"""
---
- name: Create a VLAN-aware bridge
  mikrotik.routeros_rest.bridge:
    host: https://192.0.2.1
    username: "{{ routeros_username }}"
    password: "{{ routeros_password }}"
    name: bridge1
    vlan_filtering: true
    pvid: 1
    stp_protocol_mode: rstp
...
"""


RETURN = r"""
bridge:
  description: RouterOS bridge record returned after reconciliation.
  returned: success
  type: raw
changed_fields:
  description: Bridge fields changed during this invocation.
  returned: success
  type: list
"""


def _first(value):
    if isinstance(value, list):
        return value[0] if value else None
    return value if isinstance(value, dict) else None


def _bool_match(current, desired):
    return (str(current).lower() in {"yes", "true"}) == desired


def _valid_mac(value):
    return bool(re.fullmatch(r"(?i)([0-9a-f]{2}:){5}[0-9a-f]{2}", value))


def main():
    spec = {
        "host": {"type": "str", "required": True}, "username": {"type": "str", "required": True},
        "password": {"type": "str", "required": True, "no_log": True}, "name": {"type": "str", "required": True},
        "enabled": {"type": "bool", "default": True}, "comment": {"type": "str"}, "mtu": {"type": "int"},
        "arp": {"type": "str", "default": "enabled", "choices": ["disabled", "enabled", "local-proxy-arp", "proxy-arp", "reply-only"]},
        "arp_timeout": {"type": "str"}, "admin_mac_address": {"type": "str"}, "ageing_time": {"type": "str"},
        "max_learned_entries": {"type": "raw"}, "dhcp_snooping": {"type": "bool"}, "dhcpv6_snooping": {"type": "bool"},
        "ra_guard": {"type": "bool"}, "fast_forward": {"type": "bool"}, "vlan_filtering": {"type": "bool", "default": False},
        "pvid": {"type": "int"}, "ether_type": {"type": "str", "default": "0x8100", "choices": ["0x88a8", "0x8100", "0x9100"]},
        "frame_types": {"type": "str", "default": "admit-all", "choices": ["admit-all", "admit-only-untagged-and-priority-tagged", "admit-only-vlan-tagged"]},
        "ingress_filtering": {"type": "bool", "default": True}, "mvrp": {"type": "bool", "default": False},
        "mlag_peer_port": {"type": "str"}, "mlag_priority": {"type": "int", "default": 128}, "mlag_heartbeat": {"type": "str", "default": "00:00:05"},
        "stp_protocol_mode": {"type": "str", "default": "rstp", "choices": ["none", "stp", "rstp", "mstp"]}, "stp_priority": {"type": "raw", "default": "0x8000"},
        "port_cost_mode": {"type": "str", "default": "long", "choices": ["short", "long"]}, "max_message_age": {"type": "str", "default": "00:00:20"},
        "forward_delay": {"type": "str", "default": "00:00:15"}, "transmit_hold_count": {"type": "int", "default": 6}, "max_hops": {"type": "int", "default": 20},
        "igmp_snooping": {"type": "bool", "default": False}, "igmp_version": {"type": "int", "default": 2, "choices": [2, 3]}, "mld_version": {"type": "int", "default": 1, "choices": [1, 2]},
        "multicast_router": {"type": "str", "default": "temporary-query", "choices": ["disabled", "permanent", "temporary-query"]}, "multicast_carrier": {"type": "bool", "default": False},
        "querier_uses_bridge_address": {"type": "bool", "default": False}, "startup_query_count": {"type": "int", "default": 2}, "last_member_query_count": {"type": "int", "default": 2},
        "last_member_interval": {"type": "str", "default": "1.00"}, "membership_interval": {"type": "str", "default": "260.00"}, "querier_interval": {"type": "str", "default": "255.00"},
        "query_interval": {"type": "str", "default": "125.00"}, "query_response_interval": {"type": "str", "default": "10.00"}, "startup_query_interval": {"type": "str", "default": "31.25"},
        "state": {"type": "str", "default": "present", "choices": ["absent", "present"]}, "validate_certs": {"type": "bool", "default": True}, "timeout": {"type": "int", "default": 30},
    }
    module = AnsibleModule(argument_spec=spec, supports_check_mode=True)
    p = module.params
    if p["timeout"] <= 0: module.fail_json(msg="timeout must be greater than zero")
    if p["vlan_filtering"] and p.get("pvid") is None: module.fail_json(msg="pvid is required when vlan_filtering is true")
    if p.get("pvid") is not None and not 1 <= p["pvid"] <= 4094: module.fail_json(msg="pvid must be between 1 and 4094")
    if p.get("admin_mac_address") and not _valid_mac(p["admin_mac_address"]): module.fail_json(msg="admin_mac_address must be a valid MAC address")
    if p.get("mlag_peer_port") is None and (p["mlag_priority"] != 128 or p["mlag_heartbeat"] != "00:00:05"): module.fail_json(msg="mlag_peer_port is required when MLAG settings are supplied")
    if p["max_hops"] < 6 or p["max_hops"] > 40: module.fail_json(msg="max_hops must be between 6 and 40")

    desired = {"name": p["name"], "disabled": not p["enabled"], "arp": p["arp"], "vlan-filtering": p["vlan_filtering"], "ether-type": p["ether_type"], "frame-types": p["frame_types"], "ingress-filtering": p["ingress_filtering"], "mvrp": p["mvrp"], "protocol-mode": p["stp_protocol_mode"], "priority": p["stp_priority"], "port-cost-mode": p["port_cost_mode"], "max-message-age": p["max_message_age"], "forward-delay": p["forward_delay"], "transmit-hold-count": p["transmit_hold_count"], "max-hops": p["max_hops"], "igmp-snooping": p["igmp_snooping"], "igmp-version": p["igmp_version"], "mld-version": p["mld_version"], "multicast-router": p["multicast_router"], "multicast-carrier": p["multicast_carrier"], "querier-uses-bridge-address": p["querier_uses_bridge_address"], "startup-query-count": p["startup_query_count"], "last-member-query-count": p["last_member_query_count"], "last-member-interval": p["last_member_interval"], "membership-interval": p["membership_interval"], "querier-interval": p["querier_interval"], "query-interval": p["query_interval"], "query-response-interval": p["query_response_interval"], "startup-query-interval": p["startup_query_interval"]}
    optional = {"comment": "comment", "mtu": "mtu", "arp-timeout": "arp_timeout", "admin-mac": "admin_mac_address", "ageing-time": "ageing_time", "max-learned-entries": "max_learned_entries", "dhcp-snooping": "dhcp_snooping", "dhcpv6-snooping": "dhcpv6_snooping", "ra-guard": "ra_guard", "fast-forward": "fast_forward", "pvid": "pvid", "mlag-peer-port": "mlag_peer_port", "mlag-priority": "mlag_priority", "mlag-heartbeat": "mlag_heartbeat"}
    for key, source in optional.items():
        if p.get(source) is not None: desired[key] = p[source]
    client = RouterOSRestClient(host=p["host"], username=p["username"], password=p["password"], timeout=p["timeout"], validate_certs=p["validate_certs"])
    try:
        existing = _first(client.get("interface/bridge", query={"name": p["name"]}))
        if p["state"] == "absent":
            if existing is None: module.exit_json(changed=False, bridge={}, changed_fields=[])
            if not existing.get(".id"): module.fail_json(msg="RouterOS bridge response did not include .id")
            result = existing if module.check_mode else client.delete(f"interface/bridge/{existing['.id']}")
            module.exit_json(changed=True, bridge=result, changed_fields=["bridge"])
        if existing is None:
            result = desired if module.check_mode else client.put("interface/bridge", desired)
            module.exit_json(changed=True, bridge=result, changed_fields=list(desired))
        if not existing.get(".id"): module.fail_json(msg="RouterOS bridge response did not include .id")
        changes = {}
        for key, value in desired.items():
            if key in {"disabled", "vlan-filtering", "ingress-filtering", "mvrp", "igmp-snooping", "multicast-carrier", "querier-uses-bridge-address", "dhcp-snooping", "dhcpv6-snooping", "ra-guard", "fast-forward"}:
                if not _bool_match(existing.get(key, "no"), bool(value)): changes[key] = value
            elif str(existing.get(key, "")) != str(value): changes[key] = value
        if not changes: module.exit_json(changed=False, bridge=existing, changed_fields=[])
        result = {**existing, **changes} if module.check_mode else client.patch(f"interface/bridge/{existing['.id']}", changes)
    except RouterOSRestError as exc:
        module.fail_json(msg=str(exc))
    module.exit_json(changed=True, bridge=result, changed_fields=list(changes))


if __name__ == "__main__":
    main()

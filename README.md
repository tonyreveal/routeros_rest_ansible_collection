# Ansible Collection - mikrotik.routeros_rest

The `mikrotik.routeros_rest` collection provides Ansible modules for managing
and inspecting MikroTik RouterOS devices through the RouterOS REST API.

## Description

The collection provides focused REST modules for the complete RouterOS device
lifecycle. It can configure switching and interfaces, bridges, VLANs, bonds,
MLAG, wireless, LTE, VRFs, IP addressing, DHCP, DNS, routing protocols,
firewall policies, NAT, VPNs, tunnels, VRRP, HotSpot, PPP, RADIUS, SNMP,
traffic flow, logging, users, certificates, containers, and system settings.

The collection also supports package and RouterBOARD upgrades, backups,
exports, restores, imports, file operations, and controlled reboots. Read-only
information modules inspect supported RouterOS resources, sessions, modem and
wireless state, storage, licensing, and system environment. Operational tool
modules provide ping, traceroute, route lookup, scanning, packet capture,
traffic monitoring, bandwidth, firewall, cable, Netwatch, DNS, wireless, and
modem diagnostics. Information modules return registered results directly;
only `mikrotik.routeros_rest.setup` returns RouterOS data as Ansible facts.

## Requirements

- Ansible Core 2.16 or newer is recommended.
- Python 3 in the execution environment.
- RouterOS 7.x with the `www-ssl` or `www` REST service enabled.
- A RouterOS account with permissions for the requested operations.
- HTTPS and appropriate certificate validation in production.

The modules use Python’s standard library and require no additional Python
packages or Ansible collection dependencies.

## Installation

### Red Hat Ansible Automation Platform

Red Hat customers should install certified content from Ansible Automation Hub
using their organization’s approved content source.

### Ansible Galaxy or source repository

Install from Ansible Galaxy:

```bash
ansible-galaxy collection install mikrotik.routeros_rest
```

In `requirements.yml`:

```yaml
collections:
  - name: mikrotik.routeros_rest
```

Install a requirements file with:

```bash
ansible-galaxy collection install -r requirements.yml
```

Install a specific version or upgrade with:

```bash
ansible-galaxy collection install mikrotik.routeros_rest:==1.0.0
ansible-galaxy collection install mikrotik.routeros_rest --upgrade
```

See [using Ansible collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html)
for more information.

## Use cases

- Configure bridges, bridge ports, VLANs, bonded interfaces, MLAG state,
  Ethernet, wireless, LTE, VRFs, interface lists, and IP services.
- Configure IPv4 and IPv6 addressing, static routes, routing tables, policy
  routing, OSPF, BGP, RIP, routing filters, and connection tracking.
- Configure IPv4 and IPv6 firewall filter, mangle, raw, NAT, and address-list
  resources.
- Configure DHCP clients, pools, networks, servers, relays, DHCP leases,
  DHCPv6 clients, pools, networks, and servers.
- Configure DNS, static DNS records, NTP, system identity, system clock,
  RADIUS, SNMP, traffic flow, logging, watchdog, and neighbor discovery.
- Configure users, user groups, SSH keys, HotSpot servers, profiles, users,
  bindings, and PPP profiles, secrets, and server services.
- Configure WireGuard, IPsec, GRE, EoIP, IPIP, SIT, VXLAN, L2TP, SSTP, PPPoE,
  VRRP, and related server, peer, identity, policy, and proposal resources.
- Configure certificates, RouterOS containers, file operations, backups,
  exports, imports, restores, RouterOS package upgrades, RouterBOARD upgrades,
  and reboots.
- Gather read-only information for all supported resources, including active
  sessions, wireless registrations, LTE modem diagnostics, certificates,
  storage, license, RouterOS environment, and system state.
- Run operational diagnostics including ping, traceroute, IP, ARP, MAC, and
  wireless scans; bandwidth tests; Torch; packet capture; interface and
  traffic monitoring; firewall and traffic-flow tests; Netwatch probes;
  Ethernet cable tests; route lookups; DNS tests; and modem AT commands.

## Modules

Configuration modules are listed alphabetically:

- `address_list` — Manage or configure address list.
- `backup` — Manage or configure backup.
- `bgp` — Manage or configure bgp.
- `bgp_connection` — Manage or configure bgp connection.
- `bond` — Manage or configure bond.
- `bridge` — Manage or configure bridge.
- `bridge_port` — Manage or configure bridge port.
- `bridge_vlan` — Manage or configure bridge vlan.
- `certificate` — Manage or configure certificate.
- `certificate_export` — Manage or configure certificate export.
- `certificate_generate` — Manage or configure certificate generate.
- `certificate_import` — Manage or configure certificate import.
- `certificate_revoke` — Manage or configure certificate revoke.
- `certificate_sign` — Manage or configure certificate sign.
- `connection_tracking` — Manage or configure connection tracking.
- `container` — Manage or configure container.
- `container_environment` — Manage RouterOS container environment variables.
- `container_mount` — Manage RouterOS container mounts.
- `container_start` — Start a RouterOS container.
- `container_stop` — Stop a RouterOS container.
- `dhcp_client` — Manage or configure dhcp client.
- `dhcp_lease` — Manage or configure dhcp lease.
- `dhcp_network` — Manage or configure dhcp network.
- `dhcp_pool` — Manage or configure dhcp pool.
- `dhcp_relay` — Manage or configure dhcp relay.
- `dhcp_server` — Manage or configure dhcp server.
- `dhcpv6_client` — Manage or configure dhcpv6 client.
- `dhcpv6_network` — Manage or configure dhcpv6 network.
- `dhcpv6_pool` — Manage or configure dhcpv6 pool.
- `dhcpv6_server` — Manage or configure dhcpv6 server.
- `dns` — Manage or configure dns.
- `dns_static` — Manage or configure dns static.
- `email_log` — Manage or configure email log.
- `eoip` — Manage or configure eoip.
- `export` — Manage or configure export.
- `file_copy` — Copy a RouterOS file.
- `file_delete` — Manage or configure file delete.
- `file_download` — Manage or configure file download.
- `file_move` — Move a RouterOS file.
- `file_upload` — Manage or configure file upload.
- `firewall_filter` — Manage or configure firewall filter.
- `firewall_mangle` — Manage or configure firewall mangle.
- `firewall_nat` — Manage or configure firewall nat.
- `firewall_raw` — Manage or configure firewall raw.
- `gre` — Manage or configure gre.
- `hotspot_ip_binding` — Manage or configure hotspot ip binding.
- `hotspot_profile` — Manage or configure hotspot profile.
- `hotspot_server` — Manage or configure hotspot server.
- `hotspot_user` — Manage or configure hotspot user.
- `import` — Manage or configure import.
- `interface` — Manage or configure interface.
- `interface_ethernet` — Manage or configure interface ethernet.
- `interface_list` — Manage or configure interface list.
- `ip_address` — Manage or configure ip address.
- `ip_service` — Manage or configure ip service.
- `ipip` — Manage or configure ipip.
- `ipsec` — Manage or configure ipsec.
- `ipsec_identity` — Manage or configure ipsec identity.
- `ipsec_policy` — Manage or configure ipsec policy.
- `ipsec_profile` — Manage or configure ipsec profile.
- `ipsec_proposal` — Manage or configure ipsec proposal.
- `ipv6_address` — Manage or configure ipv6 address.
- `ipv6_address_list` — Manage or configure ipv6 address list.
- `ipv6_firewall` — Manage or configure ipv6 firewall.
- `ipv6_firewall_nat` — Manage or configure ipv6 firewall nat.
- `ipv6_nd` — Manage or configure ipv6 nd.
- `ipv6_route` — Manage or configure ipv6 route.
- `l2tp` — Manage or configure l2tp.
- `l2tp_server` — Manage or configure l2tp server.
- `logging_rule` — Manage or configure logging rule.
- `logging_action` — Manage or configure logging actions.
- `lte` — Manage or configure lte.
- `neighbor_discovery` — Manage or configure neighbor discovery.
- `ntp_client` — Manage or configure ntp client.
- `ospf` — Manage or configure ospf.
- `ospf_interface` — Manage or configure ospf interface.
- `ppp_profile` — Manage or configure ppp profile.
- `ppp_secret` — Manage or configure ppp secret.
- `ppp_session_disconnect` — Manage or configure ppp session disconnect.
- `pppoe` — Manage or configure pppoe.
- `pppoe_server` — Manage or configure pppoe server.
- `qos_queue` — Manage or configure qos queue.
- `queue_tree` — Manage or configure queue tree.
- `queue_type` — Manage or configure queue type.
- `radius` — Manage or configure radius.
- `radius_incoming` — Manage or configure radius incoming.
- `reboot` — Manage or configure reboot.
- `remote_log` — Manage or configure remote log.
- `restore` — Manage or configure restore.
- `route` — Manage or configure route.
- `routerboard_upgrade` — Manage or configure routerboard upgrade.
- `routing_filter` — Manage or configure routing filter.
- `routing_filter_chain` — Manage or configure routing filter chain.
- `routing_rip` — Manage or configure routing rip.
- `routing_rule` — Manage or configure routing rule.
- `routing_table` — Manage or configure routing table.
- `scheduler` — Manage or configure scheduler.
- `script` — Manage or configure script.
- `setup` — Manage or configure setup.
- `sit` — Manage or configure sit.
- `snmp` — Manage or configure snmp.
- `snmp_settings` — Manage or configure snmp settings.
- `snmp_trap_target` — Manage or configure snmp trap target.
- `sstp` — Manage or configure sstp.
- `sstp_server` — Manage or configure sstp server.
- `system_clock` — Manage or configure system clock.
- `system_identity` — Manage or configure system identity.
- `traffic_flow` — Manage or configure traffic flow.
- `traffic_flow_settings` — Manage or configure traffic flow settings.
- `upgrade` — Manage or configure upgrade.
- `upgrade_check` — Manage or configure upgrade check.
- `user` — Manage or configure user.
- `user_group` — Manage or configure user group.
- `vlan` — Manage or configure vlan.
- `vrf` — Manage or configure vrf.
- `vrrp` — Manage or configure vrrp.
- `vrrp_address` — Manage or configure vrrp address.
- `vxlan` — Manage or configure vxlan.
- `watchdog` — Manage or configure watchdog.
- `wireguard` — Manage or configure wireguard.
- `wireguard_peer` — Manage or configure wireguard peer.
- `wireless` — Manage or configure wireless.
- `wireless_access_list` — Manage or configure wireless access list.
- `wireless_security` — Manage or configure wireless security.

Tools modules are listed alphabetically. These are operational actions; state is not applicable:

- `arp_scan` — Run a RouterOS ARP scan.
- `bandwidth_test` — Run a RouterOS bandwidth test.
- `cable_test` — Run a RouterOS Ethernet cable test.
- `dns_test` — Run a RouterOS DNS test.
- `firewall_test` — Run a RouterOS firewall packet test.
- `interface_monitor` — Monitor a RouterOS interface.
- `interface_reset` — Reset a RouterOS interface.
- `ip_scan` — Run a RouterOS IP scan.
- `mac_scan` — Run a RouterOS MAC scan.
- `modem_at_command` — Execute an AT command on a RouterOS modem.
- `netwatch_test` — Run a RouterOS Netwatch probe.
- `packet_capture` — Run a RouterOS packet capture.
- `packet_capture_stop` — Stop a RouterOS packet capture.
- `ping` — Run a RouterOS ping test.
- `routing_lookup` — Perform a RouterOS route lookup.
- `scheduler_run` — Run a RouterOS scheduler entry.
- `script_run` — Run a RouterOS script.
- `service_restart` — Restart a RouterOS service.
- `torch` — Run the RouterOS Torch traffic monitor.
- `traffic_flow_test` — Test RouterOS traffic-flow export.
- `traffic_monitor` — Collect interface traffic statistics.
- `traceroute` — Run a RouterOS traceroute.
- `wireless_scan` — Run a RouterOS wireless scan.

Information modules are listed alphabetically. They are read-only, return registered module data, and do not create Ansible facts.  There may be some overlap with ansible_facts collected by the setup modulule, but these individual *_info modules are for targeted inspection.

- `address_list_info` — Gather address list information.
- `bandwidth_test_info` — Gather bandwidth-test results.
- `bgp_connection_info` — Gather bgp connection information.
- `bgp_info` — Gather bgp information.
- `bond_info` — Gather bond information.
- `bridge_info` — Gather bridge information.
- `bridge_vlan_info` — Gather bridge vlan information.
- `cable_test_info` — Gather Ethernet cable-test results.
- `certificate_info` — Gather certificate information.
- `certificate_revoke_info` — Gather certificate revocation information.
- `connection_tracking_info` — Gather connection tracking information.
- `container_info` — Gather container information.
- `dhcp_lease_info` — Gather dhcp lease information.
- `dhcp_server_info` — Gather dhcp server information.
- `dhcpv6_client_info` — Gather dhcpv6 client information.
- `dhcpv6_lease_info` — Gather DHCPv6 lease information.
- `dhcpv6_server_info` — Gather dhcpv6 server information.
- `dns_info` — Gather dns information.
- `dns_static_info` — Gather dns static information.
- `eoip_info` — Gather eoip information.
- `file_checksum_info` — Calculate a checksum for a RouterOS file.
- `file_info` — Gather file information.
- `firewall_counter_info` — Gather firewall rule counters.
- `firewall_filter_info` — Gather firewall filter information.
- `firewall_mangle_info` — Gather firewall mangle information.
- `firewall_nat_info` — Gather firewall nat information.
- `firewall_raw_info` — Gather firewall raw information.
- `gre_info` — Gather gre information.
- `hotspot_active_info` — Gather hotspot active information.
- `hotspot_cookie_info` — Gather hotspot cookie information.
- `hotspot_host_info` — Gather hotspot host information.
- `hotspot_info` — Gather hotspot information.
- `hotspot_ip_binding_info` — Gather hotspot ip binding information.
- `hotspot_profile_info` — Gather hotspot profile information.
- `hotspot_service_info` — Gather hotspot service information.
- `hotspot_user_info` — Gather hotspot user information.
- `interface_counter_info` — Gather interface traffic counters.
- `interface_ethernet_info` — Gather interface ethernet information.
- `interface_info` — Gather interface information.
- `interface_list_info` — Gather interface list information.
- `ip_address_info` — Gather ip address information.
- `ip_service_info` — Gather ip service information.
- `ipip_info` — Gather ipip information.
- `ipsec_identity_info` — Gather ipsec identity information.
- `ipsec_info` — Gather ipsec information.
- `ipsec_policy_info` — Gather ipsec policy information.
- `ipsec_profile_info` — Gather ipsec profile information.
- `ipsec_proposal_info` — Gather ipsec proposal information.
- `ipv6_address_info` — Gather ipv6 address information.
- `ipv6_address_list_info` — Gather ipv6 address list information.
- `ipv6_firewall_info` — Gather ipv6 firewall information.
- `ipv6_firewall_nat_info` — Gather IPv6 firewall NAT information.
- `ipv6_nd_info` — Gather ipv6 nd information.
- `ipv6_route_info` — Gather ipv6 route information.
- `l2tp_info` — Gather l2tp information.
- `l2tp_server_info` — Gather l2tp server information.
- `logging_info` — Gather logging information.
- `logging_action_info` — Gather logging action information.
- `lte_info` — Gather lte information.
- `modem_at_command_info` — Gather modem AT-command results.
- `mlag_info` — Gather mlag information.
- `neighbor_discovery_info` — Gather neighbor discovery information.
- `ntp_info` — Gather ntp information.
- `ospf_info` — Gather ospf information.
- `ospf_neighbor_info` — Gather ospf neighbor information.
- `ppp_profile_info` — Gather ppp profile information.
- `ppp_secret_info` — Gather ppp secret information.
- `ppp_session_info` — Gather active PPP sessions and connection state.
- `pppoe_info` — Gather pppoe information.
- `pppoe_server_info` — Gather pppoe server information.
- `qos_queue_info` — Gather qos queue information.
- `queue_tree_info` — Gather queue tree information.
- `queue_type_info` — Gather queue type information.
- `radius_incoming_info` — Gather incoming RADIUS settings.
- `radius_info` — Gather radius information.
- `route_info` — Gather route information.
- `route_cache_info` — Gather route cache information.
- `routerboard_info` — Gather routerboard information.
- `routeros_environment_info` — Gather routeros environment information.
- `routing_filter_chain_info` — Gather routing filter chain information.
- `routing_filter_info` — Gather routing filter information.
- `routing_rip_info` — Gather routing rip information.
- `scheduler_info` — Gather scheduler information.
- `script_info` — Gather script information.
- `sit_info` — Gather sit information.
- `snmp_info` — Gather snmp information.
- `snmp_trap_target_info` — Gather snmp trap target information.
- `sstp_info` — Gather sstp information.
- `sstp_server_info` — Gather sstp server information.
- `storage_info` — Gather storage information.
- `system_clock_info` — Gather RouterOS system clock settings.
- `system_identity_info` — Gather RouterOS system identity.
- `system_license_info` — Gather system license information.
- `system_package_info` — Gather system package information.
- `system_resource_info` — Gather system resource information.
- `torch_info` — Gather Torch traffic information.
- `traffic_flow_info` — Gather traffic flow information.
- `traffic_flow_settings_info` — Gather traffic flow settings information.
- `user_group_info` — Gather user group information.
- `user_info` — Gather user information.
- `vlan_info` — Gather vlan information.
- `vrf_info` — Gather vrf information.
- `vrrp_info` — Gather vrrp information.
- `vxlan_info` — Gather vxlan information.
- `watchdog_info` — Gather watchdog information.
- `wireguard_info` — Gather wireguard information.
- `wireguard_peer_info` — Gather wireguard peer information.
- `wireless_access_list_info` — Gather wireless access list information.
- `wireless_channel_info` — Gather wireless channel information.
- `wireless_info` — Gather wireless information.
- `wireless_registration_info` — Gather wireless registration information.
- `wireless_scan_info` — Gather wireless scan results.
- `wireless_security_info` — Gather wireless security information.

All modules accept REST connection parameters including `host`, `username`,
`password`, `validate_certs`, and `timeout`, as described in their embedded
module documentation.

The `interface_ethernet` module manages settings on existing physical Ethernet
ports. Its `state: absent` value resets the settings managed by the module to
RouterOS defaults; it does not delete or disable the physical port.

The `interface` module follows the same model for generic interface settings.
Its `state: absent` value resets the managed comment, MTU, and enabled state to
generic RouterOS defaults; it does not delete the interface. Use the dedicated
resource module, such as `vlan`, `bridge`, `bond`, or a tunnel module, when a
virtual interface must be created or removed.

## Testing

Complete testing of all modules in this collection is incomplete due to
limited time and insuffient hardware.  Basic functionality in all modules
should function as expected.  If you experience issues or limited functionality
please open an issue in this collections GitHub repository.

Testing has been performed against RouterOS versions 7.23.3 and newer.
Python syntax validation is performed for the modules. Live integration tests
require a RouterOS device with REST enabled and suitable credentials.

Package upgrades, firmware upgrades, reboots, restores, and imports are
disruptive. Use `ansible.builtin.wait_for_connection` when appropriate.

## Contributing

Contributions and issue reports are welcome through the project repository and
issue tracker. Include the RouterOS and Ansible versions, inputs, and sanitized
error output when reporting a problem.

## Support

This third-party collection is maintained by Tony Reveal.  Open any issues
in this collections repository at:
https://github.com/tonyreveal/routeros_rest_ansible_collection/issues
Red Hat customers using certified content can open support cases through the
**Create issue** button in Ansible Automation Hub when the collection is
available there. Community assistance may also be available through the
[Ansible Forum](https://forum.ansible.com/).

## Release notes and roadmap

Release notes are published with collection releases. A separate public
roadmap is not currently available.

## Related information

- [MikroTik RouterOS REST API documentation](https://manual.mikrotik.com/docs/developers/rest-api)
- [MikroTik RouterOS documentation](https://help.mikrotik.com/docs/)
- [Ansible collections documentation](https://docs.ansible.com/ansible/latest/collections/index.html)

## License information

This collection is licensed under the
[GNU General Public License v3.0 or later](https://www.gnu.org/licenses/gpl-3.0.html).

## Author

Tony Reveal — [https://github.com/tonyreveal](https://github.com/tonyreveal)

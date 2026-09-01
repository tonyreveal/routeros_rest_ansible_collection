# Changelog

All notable changes to this collection are documented here.

## Current functionality summary

The collection now covers configuration and read-only inspection for RouterOS
switching, routing, IPv4 and IPv6 firewalling, DHCP and DNS, VPN and tunnels,
wireless and LTE, HotSpot and PPP, RADIUS and monitoring, certificates and
containers, system administration, backups and file operations. It also
provides operational tools for network reachability, route, scan, traffic,
firewall, packet-capture, cable, Netwatch, and modem diagnostics.

## [1.0.0] - 2026-08-31

### Added

- Added idempotent RouterOS container start and stop controls, container mount
  and environment management, and read-only file checksum inspection.

### Changed

- Removed redundant `firewall_connection_tracking_rule` in favor of
  `connection_tracking`.
- Removed redundant `ppp_active_info` in favor of the more capable filtered
  `ppp_session_info` module.
- Removed redundant `lte_modem_info`; LTE interface and modem information is
  provided by `lte_info`.
- Added RouterOS file move and copy operations, script and scheduler execution,
  service restart and interface reset tools, and filtered active PPP session
  information with connection state details.

- Added idempotent REST modules for DHCPv6 clients, IPv6 Neighbor Discovery,
  DHCP leases, firewall address-list entries, and static DNS records.
- Added `address_list_info` for read-only address-list inspection.
- Added idempotent REST modules for VRRP, IPsec peers, routing filters, SNMP
  communities, and traffic-flow export targets.
- Added core router modules for DHCPv6 servers and read-only information
  modules for WireGuard, DHCPv6 clients and servers, IPv6 Neighbor Discovery,
  static DNS, and routing filters.
- Added idempotent RIP and connection-tracking modules, plus read-only
  information modules for RIP, connection tracking, SNMP, traffic flow, and
  VRRP.
- Added operational and security modules for simple queues, scheduler
  entries, RouterOS scripts, watchdog settings, and neighbor discovery,
  including corresponding read-only information modules.
- Added idempotent IPsec profile and policy modules with corresponding
  read-only information modules.
- Added idempotent IPsec identity and GRE tunnel modules with corresponding
  read-only information modules.
- Added OSPF interface-template, routing-filter-chain, and queue-type modules,
  including read-only routing-filter-chain and queue-type information modules.
- Added queue-tree inspection, global SNMP settings, SNMP trap targets, and
  global traffic-flow settings modules with read-only trap-target and
  traffic-flow information modules.
- Added idempotent EoIP, IPIP, and SIT tunnel modules with corresponding
  read-only information modules.
- Added idempotent VXLAN, L2TP, SSTP, and PPPoE tunnel modules with
  corresponding read-only information modules.
- Added WireGuard peer, IPsec proposal, DHCPv6 pool, and DHCPv6 network
  modules, including read-only information modules for WireGuard peers and
  IPsec proposals.
- Added BGP connection, OSPF neighbor information, queue tree, and IPv4 raw
  firewall information modules.
- Added idempotent PPP profile and secret management, L2TP, SSTP, and PPPoE
  server configuration, plus read-only active-session and server information
  modules.
- Added idempotent REST modules for bridge ports, bridge VLAN entries, VLAN
  interfaces, interface lists, firewall filter/NAT/mangle/raw rules, DHCP
  servers, DHCP pools, DHCP networks, static routes, and common interfaces.
- Added shared resource reconciliation helpers for consistent check-mode and
  state handling.
- Added `bond` for idempotent bonded-interface configuration, including MLAG
  client bond support.
- Added `mlag_info` for read-only MLAG bridge configuration and state reporting.
- Added router configuration modules for DHCP clients, routing tables, VRFs,
  policy routing, IP services, OSPF, BGP, IPv6 addresses, IPv6 routes, and
  IPv6 firewall rules.
- Added read-only REST info modules for interfaces, routes, IPv6 routes and
  addresses, IPv4 and IPv6 firewall rules, DHCP leases and servers, system
  resources and packages, RouterBOARD state, users, IP services, DNS, NTP,
  logging, interface lists, VRFs, OSPF, and BGP.
- Added IPv6 firewall address-list management and read-only information.
- Added read-only PPP profile and secret information modules.
- Added certificate, RADIUS, and VRRP address management modules, with
  certificate and RADIUS information modules.
- Added HotSpot server and user management, LTE information, wireless
  configuration and information, container management and information, and
  user-group management and information modules.
- Added HotSpot profile and IP-binding management, active-session and resource
  information modules, and idempotent LTE interface configuration.
- Added wireless security profile management and registration information,
  certificate lifecycle configuration modules, and RouterOS file inspection
  and removal modules.
- Added certificate import, export, and revocation, RouterOS file upload and
  download, wireless access-list management, and wireless channel information.
- Added HotSpot user, cookie, host, and service information modules, LTE modem
  diagnostics, and idempotent PPP session disconnection.
- Added operational diagnostic modules for ping, traceroute, IP scanning, and
  interface traffic monitoring.
- Added packet capture, Netwatch probing, Ethernet cable testing, and modem AT
  command tool modules.
- Added wireless scanning, routing lookup, firewall testing, and traffic-flow
  testing tool modules.
- Added information modules for bandwidth tests, Torch, wireless scans, cable
  tests, modem commands, route cache, firewall counters, and interface
  counters, plus packet-capture stop control.
- Added bandwidth testing, Torch monitoring, MAC scanning, DNS testing,
  interface monitoring, and ARP scanning tool modules.
- Added incoming RADIUS, system identity, and system clock configuration, plus
  RouterOS license and storage information modules.
- Added Ethernet interface configuration and information, global connection
  tracking controls, IPv6 firewall NAT rules, and RouterOS environment
  information.
- Added high-priority information modules for IPv6 NAT, system identity and
  clock, incoming RADIUS, DHCPv6 leases, and certificate revocation, plus
  generic logging-action management and inspection.
- Refined `interface_ethernet` to update existing physical ports only; its
  `state: absent` behavior now resets managed settings instead of deleting a
  port.

### Updated

- Verified the bridge module performs state comparison before creating or
  updating bridge interfaces.

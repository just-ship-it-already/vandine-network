# Network Engineering Lab - rafael.vandine.us

A production-grade network engineering showcase featuring multi-site infrastructure with advanced routing, monitoring, and security capabilities.

## Live Demo
Visit: rafael.vandine.us

## Features

### Infrastructure Components
- **Palo Alto PA-220** - Next-generation firewall with IPS/IDS, URL filtering, and threat prevention
- **Cloudflare Integration** - Global edge network with 275+ PoPs, currently connected via LAX datacenter
- **Dynamic DNS** - Automatic failover with 60-second TTL updates
- **IPsec VPN** - Site-to-site connectivity with AES-256-GCM encryption
- **VLAN Segmentation** - Isolated development networks (10.200.1.0/24 and 10.201.1.0/24)
- **NordVPN Backup** - Redundant routing path (185.80.114.80)

### Performance & Monitoring
- **Real-time Metrics** - Live bandwidth, latency, and session monitoring
- **iperf3 Testing** - Dedicated performance testing infrastructure
- **Prometheus + Grafana** - Comprehensive monitoring stack
- **Route Comparison** - Interactive testing between Cloudflare and direct routes

### Key Capabilities
- Multi-site connectivity with automatic failover
- Hardware-accelerated inter-VLAN routing
- Zero-trust security architecture
- 99.9% uptime SLA
- Sub-20ms latency via Cloudflare edge
- 950+ Mbps throughput capacity

## Network Topology

    Internet --> rafael.vandine.us (DDNS) --> Cloudflare Workers (LAX)
         |
    PA-220 Firewall
         |
    VLAN Segregation
    ├── VLAN 200: 10.200.1.0/24 (Primary)
    └── VLAN 201: 10.201.1.0/24 (Secondary)

## Technology Stack

- **Security**: Palo Alto PA-220 NGFW
- **CDN/Edge**: Cloudflare Workers & Argo
- **VPN**: IPsec IKEv2 with PFS
- **Web Server**: nginx 1.22.1
- **Monitoring**: Prometheus + Grafana
- **Performance**: iperf3
- **Containerization**: Docker & Docker Compose

## Performance Metrics

| Route Type | Latency | Throughput | Packet Loss |
|------------|---------|------------|-------------|
| Cloudflare Argo | 18ms | 948 Mbps | 0.01% |
| Direct ISP | 35ms | 756 Mbps | 0.1% |
| IPsec Tunnel | 22ms | 856 Mbps | 0% |
| NordVPN Backup | 45ms | 520 Mbps | 0.05% |

## Interactive Features

- **Real-time Edge Detection**: Auto-detect your Cloudflare edge location
- **Route Testing**: Compare performance between Cloudflare and direct routes
- **Live Monitoring**: Real-time bandwidth and latency updates
- **Performance Visualization**: Interactive metrics and charts

## Security Features

- Zero-trust network architecture
- Multi-layer security (DDoS, WAF, NGFW)
- IPsec encryption for site-to-site VPN
- VLAN isolation for network segmentation
- Real-time threat detection and response

## License

MIT License

---

Built for network engineers by network engineers

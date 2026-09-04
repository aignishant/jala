"""Project Jala - the ID decomposition and day map, and the check that keeps them honest.

Run as `./m plan` (or `uv run python scripts/plan_check.py`). Two jobs:

1. **Verify.** Every declared concept ID is closed exactly once, day numbers are contiguous
   from 0, and no day closes an ID that was never declared. The plan's day count is printed
   as an *output* of this check.
2. **Emit.** Regenerate the plan's SS8-22 and S23 tables, so no table in
   `docs/00_MASTER_PLAN.md` is ever retyped by hand.


Principle 19: the day count is *derived*. This script is where it is
derived, so that the number in the frontmatter is an output rather than a claim.
"""

from collections import Counter
from dataclasses import dataclass, field

# --- The curricula -------------------------------------------------------------------
# prefix -> (name, [concept, ...])  The index in the list + 1 is the ID number.

CURRICULA: dict[str, tuple[str, list[str]]] = {
    "FOUND": ("Foundations & the model", [
        "What a network is - two machines, one wire, and the problem of whose turn it is",
        "Layering as an engineering decision - what a layer buys and what it costs",
        "OSI's seven layers vs the Internet's four - which one is real, which one is vocabulary",
        "Encapsulation and decapsulation - the envelope inside the envelope",
        "The header - why every protocol starts with fixed fields, and how you read one",
        "Four names for one machine - MAC, IP, port, hostname, and what resolves what",
        "Frame, packet, segment, datagram, message - using the five words correctly",
        "Circuit switching vs packet switching - the argument the Internet won, and its cost",
        "The end-to-end principle, and every place the Internet now violates it",
        "How a protocol becomes real - IETF, RFCs, IEEE, W3C, and the standards process",
        "Reading a spec - MUST/SHOULD/MAY, ABNF, and the packet diagram convention",
        "The five tools that see different things - ip, ss, tcpdump, dig, curl",
        "A capture is the ground truth - reading one pcap end to end, byte by byte",
        "The lab - network namespaces, veth pairs and bridges: an internet on one laptop",
    ]),
    "PHY": ("The physical layer & signalling", [
        "Bits on a wire - voltage, time, and why both ends need the same clock",
        "Bandwidth, bit rate, baud and the Shannon limit",
        "Line coding - NRZ, Manchester, 4B/5B, 8b/10b, and why raw NRZ fails",
        "Clock recovery, DC balance, and the danger of a long run of zeros",
        "Latency decomposed - propagation, transmission, queueing, processing",
        "The bandwidth-delay product - the pipe you have to keep full",
        "Media - copper, multimode and single-mode fibre; the distance/rate trade",
        "Multiplexing - FDM, TDM, WDM, OFDM as one idea in four costumes",
        "Errors on the wire - BER, attenuation, crosstalk, and what noise does to a bit",
        "Error detection - parity, the Internet checksum, and CRC-32, all built",
        "Error correction - Hamming distance and FEC; when to correct, when to resend",
        "The physical layer you can touch - NICs, transceivers, link training, the cable plant",
    ]),
    "LINK": ("The link layer & switching", [
        "The framing problem - where does a frame start, and where does it stop",
        "Framing methods - length fields, sentinels, byte stuffing, bit stuffing",
        "The Ethernet frame field by field, built by hand and put on the wire",
        "MAC addresses - the OUI, broadcast, multicast, and the locally administered bit",
        "The FCS - your CRC-32 checked against the one in a real capture",
        "Shared media and collisions - CSMA/CD, and why it is history worth knowing",
        "Collision domain vs broadcast domain - the distinction that killed the hub",
        "The learning switch, built - the MAC table, flooding, and ageing",
        "Duplex, autonegotiation, and the duplex mismatch that halves your throughput",
        "VLANs and the 802.1Q tag - one wire, many broadcast domains",
        "Trunks, access ports, and the native-VLAN trap",
        "The loop and the broadcast storm - a redundant cable that kills a LAN",
        "Spanning Tree - root election, port roles, and what convergence costs",
        "Link aggregation - LACP, and the hash that decides which cable your flow takes",
        "ARP, built - request, reply, the cache, and the gratuitous announcement",
        "ARP spoofing, and the fact that a LAN has no authentication at all",
        "MTU and jumbo frames - a link-layer number that causes network-layer pain",
        "Point-to-point links - PPP, and framing when there is nobody to address",
        "DHCP - DORA, leases, options, and the rogue server on the guest network",
        "The link layer under a hypervisor - tap, bridge, veth, macvlan",
        "IPv6 Neighbor Discovery - ARP's replacement, plus RA, SLAAC and DAD",
        "Inside the switch - store-and-forward vs cut-through, buffers, head-of-line blocking",
    ]),
    "NET": ("The network layer & addressing", [
        "Why a second address - the LAN does not scale, and the internetwork problem",
        "The IPv4 header field by field - built, parsed, and checked against a capture",
        "The IPv4 address - the dotted quad, and what the network/host split actually means",
        "Classful addressing, and the reason it had to be abandoned",
        "Masks and prefix length - the arithmetic, done in binary, by hand",
        "Subnetting and VLSM - carving a /24 into the subnets a building needs",
        "CIDR, supernetting and aggregation - how the routing table stays finite",
        "Special-purpose addresses - RFC 1918, loopback, link-local, multicast, broadcast",
        "The forwarding decision - longest prefix match, built",
        "The routing table on a real machine - `ip route` read line by line",
        "The default gateway - what the first hop knows that you do not",
        "TTL and the hop limit - the field that ends a loop nobody noticed",
        "The header checksum - computed by hand, and why IPv6 deleted it",
        "Fragmentation and reassembly - the ID, offset and MF fields, built",
        "Path MTU discovery and the PMTU black hole - the handshake works, the transfer hangs",
        "ICMP - echo, unreachable, time-exceeded, redirect; the network's error channel",
        "ping and traceroute, both written from scratch, then diffed against the real ones",
        "NAT - the translation table, the port rewrite, and everything it breaks",
        "NAT traversal - STUN, TURN, ICE and hole punching",
        "IPv6 - the address, the header, and the list of things that were removed",
        "IPv6 addressing in practice - link-local, ULA, SLAAC, and the /64 convention",
        "ICMPv6 is not optional - and the firewall rule that silently breaks IPv6",
        "Dual stack and Happy Eyeballs - the broken v6 path you never noticed",
        "Transition mechanisms - NAT64/DNS64, 464XLAT and tunnels",
    ]),
    "ROUTE": ("Routing", [
        "Routing vs forwarding - the control plane and the data plane, separated",
        "Static routes, and the cases where they are still the right answer",
        "The forwarding table as a longest-prefix trie, built and benchmarked",
        "Administrative distance - choosing between two protocols that both have an answer",
        "Distance vector - Bellman-Ford, built and run on your own topology",
        "Count-to-infinity, reproduced on purpose; split horizon and poison reverse",
        "RIP as the worked example - timers, hop limit, and why it faded",
        "Link state - flooding the database, then Dijkstra, both built",
        "OSPF - areas, LSA types, DR/BDR election, and forming an adjacency",
        "OSPF convergence - what actually happens in the seconds after a cable is pulled",
        "Interior vs exterior - why one Internet needs two kinds of routing protocol",
        "Autonomous systems, ASNs, and the commercial shape of the Internet",
        "BGP as path vector - and why policy beats shortest path",
        "The BGP session - OPEN, UPDATE, KEEPALIVE, NOTIFICATION; a speaker you write",
        "BGP path attributes and the decision process, evaluated in order",
        "BGP policy - local preference, AS-path prepending, MED, communities",
        "Route leaks and hijacks - the day a prefix vanished, and what RPKI/ROV does",
        "Multicast routing and IGMP",
    ]),
    "TRANS": ("Transport & TCP", [
        "What transport adds - process to process, and the port number",
        "The five-tuple - how a packet finds one process among hundreds",
        "UDP - the header, the optional checksum, and the honesty of no guarantees",
        "A UDP echo server and client, built, then made to lose packets on purpose",
        "When UDP is the right answer - DNS, games, media, and QUIC",
        "Reliability from first principles - stop-and-wait, ARQ, and sequence numbers",
        "Duplicates, delays and wrap-around - the problems sequence numbers create",
        "Sliding windows - go-back-N and selective repeat, both built",
        "The TCP header field by field, built by hand",
        "The three-way handshake, and what a SYN cookie defends against",
        "The TCP state machine - all eleven states, drawn and implemented",
        "Teardown, half-close, and why TIME_WAIT has to last as long as it does",
        "TIME_WAIT accumulation and ephemeral port exhaustion, reproduced",
        "Sequence and acknowledgement numbers - the byte stream, and the numbers under it",
        "TCP is a byte stream, not a message queue - the partial-read bug",
        "Framing on top of TCP - length prefixes, delimiters, and the parser you must write",
        "Retransmission - the RTT estimator, Karn's algorithm and the RTO, implemented",
        "Fast retransmit and fast recovery - what three duplicate ACKs mean",
        "SACK - the retransmission you did not need to send",
        "Flow control - the receive window, the zero window, and the persist timer",
        "Silly window syndrome, Nagle, delayed ACK, and the interaction that adds 40 ms",
        "TCP options - MSS, window scale, timestamps, SACK-permitted",
        "Keepalives, half-open connections, and the peer that went away without saying so",
        "close, shutdown and SO_LINGER - what the socket API actually does to a connection",
    ]),
    "CONG": ("Congestion control & queueing", [
        "Congestion control vs flow control - two windows, one sender, different problems",
        "The congestion collapse of 1986, and the algorithm that ended it",
        "AIMD - why additive increase and multiplicative decrease converge to fairness",
        "Slow start and congestion avoidance - the two phases, drawn from your own trace",
        "Tahoe, Reno and NewReno, implemented on the stack you wrote",
        "CUBIC - the window function, and the long-fat-pipe problem it solves",
        "Delay-based control - Vegas, and the road the Internet did not take",
        "BBR - modelling the bottleneck instead of waiting for loss",
        "The queueing theory you actually need - utilisation, Little's law, and the knee",
        "Bufferbloat - excellent throughput and terrible latency, measured on your own link",
        "Active queue management - RED, CoDel and FQ-CoDel; dropping early on purpose",
        "ECN - marking instead of dropping, and why deployment took twenty years",
        "Fairness - RTT unfairness, and what TCP-friendly actually means",
        "Measuring a congestion controller honestly - repetitions, spread, and the noise band",
    ]),
    "SOCK": ("The socket API & concurrency", [
        "The socket API syscall by syscall - socket, bind, listen, accept, connect",
        "The backlog - the SYN queue, the accept queue, and what 'connection refused' means",
        "Blocking I/O and thread-per-connection, built and measured",
        "The C10K problem - the exact point where thread-per-connection stops",
        "Non-blocking sockets, EAGAIN, and the partial write",
        "select, poll and epoll - readiness, and the O(n) that was the whole bug",
        "The event loop, built from `selectors`, then compared against `asyncio`",
        "Readiness vs completion - io_uring and IOCP",
        "The socket options that matter - SO_REUSEADDR, SO_REUSEPORT, TCP_NODELAY, buffers",
        "Buffers and backpressure - the kernel's queue, your queue, and who says stop",
        "Timeouts and cancellation - the connection that hangs forever",
        "Connection pooling and keep-alive - what a handshake costs, measured",
    ]),
    "DNS": ("Naming & DNS", [
        "Why names exist - and the hosts file that stopped scaling in the 1980s",
        "The namespace - root, TLD, authoritative servers, and delegation as a tree",
        "Stub, recursive, iterative - who asks whom, and who caches",
        "The DNS message format, built and parsed by hand, including name compression",
        "The record types you must know - A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, SRV",
        "Caching and TTLs - the answer that never touched the network",
        "An iterative resolver, written from the root down, with a cache",
        "Negative caching, NXDOMAIN, and the wildcard that answers everything",
        "UDP, truncation, TCP fallback and EDNS(0) - how DNS outgrew 512 bytes",
        "DNSSEC - the chain of trust, and why deployment is genuinely hard",
        "DoT, DoH and DoQ - privacy for the user, blindness for the operator",
        "DNS in operations - split horizon, low-TTL failover, and the outage caused by a name",
    ]),
    "APP": ("Application protocols", [
        "Client-server, peer-to-peer, and what a protocol specification must actually pin down",
        "URIs and URLs - scheme, authority, path, query, fragment, and percent-encoding",
        "HTTP/1.1 - the request line, the headers, the body, parsed by hand",
        "An HTTP/1.1 server written on a raw socket",
        "Methods, status codes, safety and idempotency",
        "Content-Length, chunked transfer encoding, and content negotiation",
        "Request smuggling - the desync that lives between Content-Length and Transfer-Encoding",
        "Persistent connections, pipelining, and head-of-line blocking",
        "HTTP caching - freshness, validators, and the four caches between you and the origin",
        "Cookies and sessions - state bolted onto a stateless protocol",
        "The same-origin policy and CORS - the browser's own network model",
        "HTTP/2 - binary framing, streams, multiplexing and HPACK",
        "HTTP/3 and QUIC - streams over UDP, 0-RTT, and connection migration",
        "WebSocket - the upgrade, the frame format, and ping/pong",
        "Server-sent events and long polling - choosing among three ways to push",
        "REST, RPC and gRPC - the API shapes that sit on HTTP",
        "SMTP and store-and-forward - the protocol that assumes the other end is down",
        "IMAP, MIME, and SPF/DKIM/DMARC - why mail delivery is a reputation system",
        "FTP and its two connections - the protocol that taught firewalls to inspect payloads",
        "Real-time media - RTP, RTCP, WebRTC, and the jitter buffer",
    ]),
    "SEC": ("Security, TLS & trust", [
        "The network threat model - who can read, who can change, who can pretend to be you",
        "The lab ethics rule - your traffic, your namespaces, and the law",
        "Passive attacks - sniffing a shared medium, a mirror port, and an ARP-spoofed switch",
        "Active attacks - spoofing, replay, on-path and off-path injection",
        "Cryptographic primitives, used and never written - hash, MAC, AEAD, KDF, signature",
        "Symmetric vs asymmetric, and Diffie-Hellman drawn as a picture",
        "What TLS promises, and the four things it does not",
        "The TLS 1.3 handshake, message by message, read out of your own capture",
        "Key exchange, the key schedule, and the transcript hash",
        "X.509 certificates - the chain, the name checks, and the fields that matter",
        "The public-key infrastructure - roots, intermediates, revocation, OCSP stapling",
        "Certificate Transparency, pinning, and what happens after a misissuance",
        "A TLS client that verifies properly - and the one flag that turns it all off",
        "Mutual TLS and client certificates",
        "SSH - the protocol, host keys, and trust on first use",
        "VPNs - IPsec as an idea, and a WireGuard-shaped tunnel built over UDP",
        "Firewalls - stateless filters, stateful inspection, and nftables rules read as code",
        "NAT is not a firewall - the accidental security everyone relies on",
        "DDoS - volumetric, protocol and application-layer; amplification and reflection",
        "Scanning and reconnaissance, seen from the defender's side",
        "Segmentation and zero trust - the perimeter that stopped existing",
        "The capture that contained a password - handling evidence safely",
    ]),
    "WIRE": ("Wireless & mobility", [
        "The wireless channel - attenuation, interference, multipath, and why it is not a cable",
        "The 802.11 MAC - CSMA/CA, the hidden terminal, and RTS/CTS",
        "Beacons, scanning, association and roaming",
        "Wi-Fi generations - what MIMO, wider channels and OFDMA actually changed",
        "Wi-Fi security - WPA2, WPA3, the four-way handshake, and the open network",
        "Why the Wi-Fi is slow - airtime fairness, rate adaptation, and one distant client",
        "Cellular architecture - radio access network, core, and the bearer",
        "Mobility and handover - keeping an address while the radio changes",
        "Bluetooth and BLE - low power, short range, different assumptions",
        "TCP over a wireless link - loss that is not congestion, and what that costs",
    ]),
    "DC": ("Datacenter, cloud & overlays", [
        "The datacenter problem - east-west traffic, and why the three-tier tree failed",
        "Leaf-spine and Clos - the topology, and the oversubscription arithmetic",
        "ECMP and flow hashing - and the elephant flow that ruins a perfect plan",
        "Incast - many senders, one receiver, and TCP's worst case",
        "Overlays - VXLAN, the VTEP, and the tenant that believes it owns a LAN",
        "Geneve, GRE and IP-in-IP - the encapsulation zoo and the MTU it costs you",
        "SDN - the control plane pulled out of the box, with OpenFlow as the worked example",
        "Software forwarding - eBPF/XDP and DPDK",
        "The load balancer - L4 vs L7, direct server return, and connection affinity",
        "Health checks and draining - the balancer that kept sending to a dead backend",
        "Anycast - one address in many places, and the arithmetic behind a CDN footprint",
        "CDNs - caching at the edge, and the request that cannot be cached",
        "Container networking, built by hand - netns, veth, bridge, and one address",
        "Kubernetes networking - the pod model, CNI, Services, and kube-proxy",
        "The service mesh and the sidecar - what it buys and what each hop costs",
        "Cloud primitives - VPCs, subnets, security groups and route tables",
        "Peering, transit and internet exchanges - who pays whom, and why it shows in traceroute",
        "The cost and blast radius of a network design, worked as arithmetic",
    ]),
    "PERF": ("Performance, measurement & capture", [
        "What to measure - latency, throughput, jitter, loss, availability",
        "Latency is a distribution - p50, p95, p99, and the tail that users feel",
        "Throughput, goodput and bandwidth - three numbers people use as one",
        "The measurement harness - repetitions, seeds, warm-up, and reporting the spread",
        "The benchmark that measured slow start - a result that was an artefact",
        "tc netem - building delay, loss, reordering and rate limits on purpose",
        "Capturing correctly - the filter, the snaplen, the capture point, and what you miss",
        "The pcap and pcapng file formats, parsed by hand",
        "Following a stream - reading time, sequence and window out of a capture",
        "Diagnosing from a capture - RST, retransmission, zero window, dup ACK, reordering",
        "Active and passive measurement - and the free public vantage points",
        "Flow telemetry - NetFlow, IPFIX, sFlow, and the sampling error nobody mentions",
        "The four signals - traffic, errors, saturation, latency",
        "Reporting a network result honestly - topology, seed, spread, and the caveat",
    ]),
    "OPS": ("Operations, troubleshooting & discipline", [
        "The repo as the network's memory - ledgers, ADRs and reproducible topologies",
        "Address planning - the document that prevents next year's outage",
        "Configuration as code - idempotent topology scripts you can run twice",
        "The troubleshooting method - bottom-up, top-down, and divide-and-conquer",
        "The five questions to ask before touching anything",
        "'It's the network' - proving that it is not, with evidence rather than opinion",
        "Monitoring - what deserves an alert, and what only deserves a graph",
        "Change windows, rollback, and the config change that locked you out",
        "The incident - timeline, communication, and a postmortem worth reading",
        "Capacity planning from measured data rather than from vendor sizing",
        "An IPv6 rollout, run as a change-management exercise",
        "The runbook and the design document - written down, not remembered",
    ]),
}


@dataclass
class Day:
    n: int
    title: str
    ids: list[str] = field(default_factory=list)


@dataclass
class Phase:
    n: int
    name: str
    gate: str
    days: list[Day] = field(default_factory=list)


def d(n: int, title: str, *ids: str) -> Day:
    return Day(n, title, list(ids))


PHASES: list[Phase] = [
    Phase(0, "Foundry: the lab, the skeleton, the driver",
          "`./m check` green; `./m lab up two-host` pings; no key and no capture in git", [
        d(0, "Toolchain, skeleton and the `./m` driver - one owner for the environment, a repo "
             "that cannot commit a private key or a capture, and a gate that refuses a "
             "half-finished day"),
    ]),
    Phase(1, "The ground: what a network is",
          "`./m lab up two-host` builds two namespaces that ping, and you can name every "
          "header in the capture of that ping", [
        d(1, "Bootstrap & the map - the repo as Jala's memory, the six ledgers, `scripts/trace.py`, "
             "and the ethics rule that governs every packet you will send",
          "OPS-01"),
        d(2, "What a network is, and why it is built in layers", "FOUND-01", "FOUND-02"),
        d(3, "OSI vs the Internet model, and the envelope inside the envelope",
          "FOUND-03", "FOUND-04"),
        d(4, "Headers, addresses and the five words - frame, packet, segment, datagram, message",
          "FOUND-05", "FOUND-06", "FOUND-07"),
        d(5, "Circuit switching, packet switching, and the end-to-end principle",
          "FOUND-08", "FOUND-09"),
        d(6, "How a protocol becomes real - the RFC, and how to read one",
          "FOUND-10", "FOUND-11"),
        d(7, "The five tools that each see something different", "FOUND-12"),
        d(8, "Your first capture, read byte by byte", "FOUND-13"),
        d(9, "The lab - an internet on one laptop, from `ip netns` up", "FOUND-14"),
    ]),
    Phase(2, "The wire: signals, errors and the numbers under everything",
          "Your CRC-32 matches the FCS of a frame captured in the lab, and you can state the "
          "bandwidth-delay product of your own loopback", [
        d(10, "Bits, clocks and the Shannon limit", "PHY-01", "PHY-02"),
        d(11, "Line coding and clock recovery - why the wire never carries your bits raw",
          "PHY-03", "PHY-04"),
        d(12, "Latency decomposed, and the bandwidth-delay product", "PHY-05", "PHY-06"),
        d(13, "Media and multiplexing - copper, fibre, and one idea in four costumes",
          "PHY-07", "PHY-08"),
        d(14, "Errors on the wire, and the three ways to detect them", "PHY-09", "PHY-10"),
        d(15, "Correcting instead of resending - Hamming distance and FEC", "PHY-11"),
        d(16, "The physical layer you can touch - NICs, transceivers and the cable plant",
          "PHY-12"),
    ]),
    Phase(3, "The frame: the link layer, built",
          "Your learning switch forwards correctly on a four-host topology, your ARP responder "
          "answers a real `ping`, and you can explain the broadcast storm you caused", [
        d(17, "The framing problem, and four ways to solve it", "LINK-01", "LINK-02"),
        d(18, "The Ethernet frame, built by hand and checked against a capture",
          "LINK-03", "LINK-04", "LINK-05"),
        d(19, "Collisions, hubs, and the two kinds of domain", "LINK-06", "LINK-07"),
        d(20, "The learning switch, built", "LINK-08"),
        d(21, "Inside the switch - forwarding modes, buffers, and the duplex mismatch",
          "LINK-09", "LINK-22"),
        d(22, "VLANs and the 802.1Q tag", "LINK-10", "LINK-11"),
        d(23, "The loop, the broadcast storm, and Spanning Tree", "LINK-12", "LINK-13"),
        d(24, "Link aggregation, and the hash that picks your cable", "LINK-14"),
        d(25, "ARP, built - and the LAN's complete absence of authentication",
          "LINK-15", "LINK-16"),
        d(26, "MTU - a link-layer number that causes network-layer pain", "LINK-17"),
        d(27, "Point-to-point links and DHCP", "LINK-18", "LINK-19"),
        d(28, "The link layer under a hypervisor - tap, bridge, veth, macvlan", "LINK-20"),
        d(29, "IPv6 Neighbor Discovery - ARP's replacement, and SLAAC", "LINK-21"),
    ]),
    Phase(4, "The packet: addressing and the network layer",
          "Your IPv4 stack answers `ping` from an unmodified host, forwards between two "
          "namespaces, and reassembles a fragmented datagram", [
        d(30, "Why a second address, and the IPv4 header built by hand", "NET-01", "NET-02"),
        d(31, "The IPv4 address, and the classful era it grew out of", "NET-03", "NET-04"),
        d(32, "Masks, prefix length and subnetting, done in binary", "NET-05", "NET-06"),
        d(33, "CIDR, aggregation, and the addresses that are not yours to use",
          "NET-07", "NET-08"),
        d(34, "Longest prefix match, built - and a real routing table read line by line",
          "NET-09", "NET-10"),
        d(35, "The first hop, and the field that ends a loop", "NET-11", "NET-12"),
        d(36, "The checksum and fragmentation - two things IPv6 changed its mind about",
          "NET-13", "NET-14"),
        d(37, "The PMTU black hole - the handshake succeeds and the transfer hangs", "NET-15"),
        d(38, "ICMP, and writing `ping` and `traceroute` from scratch", "NET-16", "NET-17"),
        d(39, "NAT, built - and everything it breaks", "NET-18", "NET-19"),
        d(40, "IPv6 - the address, the header, and the list of deletions",
          "NET-20", "NET-21"),
        d(41, "ICMPv6 is not optional", "NET-22"),
        d(42, "Dual stack, Happy Eyeballs, and the broken v6 path nobody noticed", "NET-23"),
        d(43, "Transition mechanisms - NAT64, 464XLAT and tunnels", "NET-24"),
    ]),
    Phase(5, "Routing: how a packet finds a path it was never told about",
          "Distance vector and link state both converge on your six-router topology, and your "
          "BGP speaker exchanges a prefix with a second speaker and applies a policy", [
        d(44, "Control plane and data plane, and the static route", "ROUTE-01", "ROUTE-02"),
        d(45, "The forwarding trie, and choosing between two protocols that disagree",
          "ROUTE-03", "ROUTE-04"),
        d(46, "Distance vector, built", "ROUTE-05"),
        d(47, "Count-to-infinity, reproduced - split horizon, poison reverse, and RIP",
          "ROUTE-06", "ROUTE-07"),
        d(48, "Link state - flooding a database, then Dijkstra", "ROUTE-08"),
        d(49, "OSPF - areas, adjacencies, and what convergence actually costs",
          "ROUTE-09", "ROUTE-10"),
        d(50, "Interior and exterior - autonomous systems and the shape of the Internet",
          "ROUTE-11", "ROUTE-12"),
        d(51, "BGP - path vector, and a speaker you write", "ROUTE-13", "ROUTE-14"),
        d(52, "The BGP decision process, and policy as the real routing metric",
          "ROUTE-15", "ROUTE-16"),
        d(53, "Route leaks and hijacks - and what RPKI can and cannot fix", "ROUTE-17"),
        d(54, "Multicast and IGMP", "ROUTE-18"),
    ]),
    Phase(6, "Transport: TCP, built",
          "Your TCP completes a handshake with an unmodified `curl`, transfers a file "
          "correctly under 5% loss, and closes without leaving a half-open connection", [
        d(55, "Ports and the five-tuple - how a packet finds one process",
          "TRANS-01", "TRANS-02"),
        d(56, "UDP, built - and made to lose packets on purpose", "TRANS-03", "TRANS-04"),
        d(57, "When UDP is the right answer", "TRANS-05"),
        d(58, "Reliability from first principles - stop-and-wait, and what sequence numbers cost",
          "TRANS-06", "TRANS-07"),
        d(59, "Sliding windows - go-back-N and selective repeat, both built", "TRANS-08"),
        d(60, "The TCP header and the three-way handshake", "TRANS-09", "TRANS-10"),
        d(61, "The TCP state machine - eleven states, implemented", "TRANS-11"),
        d(62, "Teardown, TIME_WAIT, and the port exhaustion it causes",
          "TRANS-12", "TRANS-13"),
        d(63, "The byte stream - and the partial read that corrupts your protocol",
          "TRANS-14", "TRANS-15"),
        d(64, "Framing on top of TCP - the parser you have to write anyway", "TRANS-16"),
        d(65, "Retransmission - the RTT estimator, Karn's algorithm, and fast recovery",
          "TRANS-17", "TRANS-18"),
        d(66, "SACK and flow control - the window that says stop", "TRANS-19", "TRANS-20"),
        d(67, "Nagle meets delayed ACK - the 40 milliseconds nobody ordered",
          "TRANS-21", "TRANS-22"),
        d(68, "Keepalives, half-open connections, and what `close` really does",
          "TRANS-23", "TRANS-24"),
    ]),
    Phase(7, "Congestion: sharing a link nobody owns",
          "Your Reno and CUBIC implementations produce the expected sawtooth under netem, "
          "reported over five seeds with the spread, not the best run", [
        d(69, "Congestion control vs flow control, and the collapse of 1986",
          "CONG-01", "CONG-02"),
        d(70, "AIMD, slow start and congestion avoidance", "CONG-03", "CONG-04"),
        d(71, "Tahoe, Reno and NewReno, implemented on your own stack", "CONG-05"),
        d(72, "CUBIC, and the delay-based road not taken", "CONG-06", "CONG-07"),
        d(73, "BBR - modelling the bottleneck instead of waiting for loss", "CONG-08"),
        d(74, "Queues, Little's law, and the bufferbloat on your own link",
          "CONG-09", "CONG-10"),
        d(75, "Active queue management and ECN - dropping early on purpose",
          "CONG-11", "CONG-12"),
        d(76, "Fairness, and measuring a congestion controller honestly",
          "CONG-13", "CONG-14"),
    ]),
    Phase(8, "The socket API: where your program meets the stack",
          "Your event-loop server holds ten thousand idle connections on one thread, and you "
          "can state the memory cost per connection from measurement", [
        d(77, "The socket API syscall by syscall, and the backlog", "SOCK-01", "SOCK-02"),
        d(78, "Thread per connection, and exactly where it stops", "SOCK-03", "SOCK-04"),
        d(79, "Non-blocking sockets, and the readiness APIs", "SOCK-05", "SOCK-06"),
        d(80, "The event loop, built - then compared against `asyncio`", "SOCK-07"),
        d(81, "Completion-based I/O, and the socket options that matter",
          "SOCK-08", "SOCK-09"),
        d(82, "Buffers, backpressure, timeouts and cancellation", "SOCK-10", "SOCK-11"),
        d(83, "Connection pooling - what a handshake costs, measured", "SOCK-12"),
    ]),
    Phase(9, "Names: DNS, and the answer that never touched the network",
          "Your resolver answers from the root for a name it has never seen, and the second "
          "query is served from cache with the TTL counted down correctly", [
        d(84, "Why names exist, and the delegation tree", "DNS-01", "DNS-02"),
        d(85, "Who asks whom, and the DNS message parsed by hand", "DNS-03", "DNS-04"),
        d(86, "The record types, and what each one is actually for", "DNS-05"),
        d(87, "Caching and TTLs - the answer that never touched the network", "DNS-06"),
        d(88, "An iterative resolver, written from the root down", "DNS-07", "DNS-08"),
        d(89, "Truncation, EDNS(0), and the chain of trust", "DNS-09", "DNS-10"),
        d(90, "Encrypted DNS, and the outage caused by a name", "DNS-11", "DNS-12"),
    ]),
    Phase(10, "Applications: the protocols people actually speak",
           "Your HTTP/1.1 server serves an unmodified browser correctly, including keep-alive "
           "and chunked encoding, and rejects a smuggling attempt", [
        d(91, "Client, server, and what a specification has to pin down", "APP-01", "APP-02"),
        d(92, "HTTP/1.1, parsed by hand and served from a raw socket", "APP-03", "APP-04"),
        d(93, "Methods, status codes, and the two ways to say how long a body is",
           "APP-05", "APP-06"),
        d(94, "Request smuggling - the desync between two length fields", "APP-07"),
        d(95, "Keep-alive, head-of-line blocking, and the four caches in the path",
           "APP-08", "APP-09"),
        d(96, "Cookies, sessions, and the browser's own network model", "APP-10", "APP-11"),
        d(97, "HTTP/2 - binary framing, multiplexing and HPACK", "APP-12"),
        d(98, "HTTP/3 and QUIC - streams over UDP", "APP-13"),
        d(99, "WebSocket, server-sent events, and long polling", "APP-14", "APP-15"),
        d(100, "REST, RPC and gRPC", "APP-16"),
        d(101, "Mail - SMTP, and why delivery is a reputation system", "APP-17", "APP-18"),
        d(102, "FTP's two connections, and real-time media", "APP-19", "APP-20"),
    ]),
    Phase(11, "Security: the network assumes nothing and trusts nobody",
           "Your TLS client verifies a real chain, rejects a self-signed certificate and a "
           "name mismatch, and your WireGuard-shaped tunnel carries traffic between namespaces", [
        d(103, "The threat model, and the ethics rule that governs everything after it",
           "SEC-01", "SEC-02"),
        d(104, "Passive and active attacks, reproduced in your own lab", "SEC-03", "SEC-04"),
        d(105, "The primitives you use and never write", "SEC-05", "SEC-06"),
        d(106, "What TLS promises, and the 1.3 handshake read from your own capture",
           "SEC-07", "SEC-08"),
        d(107, "Key exchange, the key schedule and the transcript hash", "SEC-09"),
        d(108, "Certificates and the PKI - chains, names and revocation",
           "SEC-10", "SEC-11"),
        d(109, "Certificate Transparency, pinning, and life after a misissuance", "SEC-12"),
        d(110, "A TLS client that verifies - and the flag that turns it all off", "SEC-13"),
        d(111, "Mutual TLS, and SSH's trust on first use", "SEC-14", "SEC-15"),
        d(112, "A tunnel of your own - IPsec as an idea, WireGuard as a build", "SEC-16"),
        d(113, "Firewalls, and the reason NAT is not one", "SEC-17", "SEC-18"),
        d(114, "DDoS and reconnaissance, seen from the defender's side", "SEC-19", "SEC-20"),
        d(115, "Segmentation, zero trust, and the capture that contained a password",
           "SEC-21", "SEC-22"),
    ]),
    Phase(12, "Wireless: the link that is not a cable",
           "You can explain, from a measurement, why adding one distant client slowed every "
           "other client on the same access point", [
        d(116, "The channel, and the MAC that has to share it", "WIRE-01", "WIRE-02"),
        d(117, "Beacons, association, roaming, and what each generation actually changed",
           "WIRE-03", "WIRE-04"),
        d(118, "Wi-Fi security and the four-way handshake", "WIRE-05"),
        d(119, "Why the Wi-Fi is slow - airtime, and the one distant client", "WIRE-06"),
        d(120, "Cellular architecture and mobility", "WIRE-07", "WIRE-08"),
        d(121, "Short-range radios, and TCP over a lossy link", "WIRE-09", "WIRE-10"),
    ]),
    Phase(13, "Datacenter and cloud: networks built for machines, not people",
           "A leaf-spine topology in namespaces with ECMP, a VXLAN overlay between two "
           "tenants, and the oversubscription arithmetic written down", [
        d(122, "East-west traffic, leaf-spine, and the oversubscription arithmetic",
           "DC-01", "DC-02"),
        d(123, "ECMP, elephant flows and incast", "DC-03", "DC-04"),
        d(124, "Overlays - VXLAN, and the MTU that encapsulation costs you",
           "DC-05", "DC-06"),
        d(125, "SDN, and forwarding in software", "DC-07", "DC-08"),
        d(126, "The load balancer, and the health check that lied", "DC-09", "DC-10"),
        d(127, "Anycast and the CDN", "DC-11", "DC-12"),
        d(128, "Container networking, built by hand", "DC-13"),
        d(129, "Kubernetes networking - the pod model and what CNI actually does", "DC-14"),
        d(130, "The service mesh, and what each extra hop costs", "DC-15"),
        d(131, "Cloud primitives, peering and transit", "DC-16", "DC-17"),
        d(132, "The cost and blast radius of a design, as arithmetic", "DC-18"),
    ]),
    Phase(14, "Measurement: numbers you are allowed to quote",
           "Every claim in your report carries a topology, a seed, a repetition count and a "
           "spread; the contamination-by-warm-cache check is clean", [
        d(133, "What to measure, and why latency is a distribution", "PERF-01", "PERF-02"),
        d(134, "Throughput, goodput, and a harness that reports the spread",
           "PERF-03", "PERF-04"),
        d(135, "The benchmark that measured slow start", "PERF-05"),
        d(136, "netem, and capturing without lying to yourself", "PERF-06", "PERF-07"),
        d(137, "The pcap format parsed by hand, and following a stream",
           "PERF-08", "PERF-09"),
        d(138, "Diagnosis from a capture alone", "PERF-10"),
        d(139, "Active, passive and sampled measurement", "PERF-11", "PERF-12"),
        d(140, "The four signals, and reporting a result honestly", "PERF-13", "PERF-14"),
    ]),
    Phase(15, "Operations: the network as something someone has to run",
           "The whole lab rebuilds from committed scripts on a clean machine, and your "
           "runbook lets a stranger diagnose an injected fault", [
        d(141, "The address plan - the document that prevents next year's outage", "OPS-02"),
        d(142, "Configuration as code - a topology you can run twice", "OPS-03"),
        d(143, "The troubleshooting method, and the five questions", "OPS-04", "OPS-05"),
        d(144, "'It's the network' - proving it is not", "OPS-06"),
        d(145, "Monitoring, change windows, and the config that locked you out",
           "OPS-07", "OPS-08"),
        d(146, "The incident, the postmortem, and capacity planning", "OPS-09", "OPS-10"),
        d(147, "An IPv6 rollout, and the documents you leave behind",
           "OPS-11", "OPS-12"),
    ]),
    Phase(16, "Capstone: the whole path, cold",
           "A stranger clones the repo, rebuilds the lab, reproduces every headline number, "
           "and diagnoses five injected faults from evidence alone", [
        d(148, "The cold rebuild - destroy the lab and bring the whole internet back from "
               "committed scripts"),
        d(149, "One request, every layer - a browser to your own server, annotated from a "
               "single capture"),
        d(150, "The fault injection audit - five deliberate breakages, diagnosed from "
               "evidence alone"),
        d(151, "The design document - a network for a stated requirement, with the "
               "arithmetic, the threat model and the runbook"),
    ]),
]


def verify() -> None:
    declared = {f"{p}-{i + 1:02d}" for p, (_, cs) in CURRICULA.items() for i in range(len(cs))}
    used: Counter[str] = Counter()
    days: list[Day] = [day for ph in PHASES for day in ph.days]

    for day in days:
        used.update(day.ids)

    problems: list[str] = []

    dupes = [i for i, c in used.items() if c > 1]
    if dupes:
        problems.append(f"IDs used more than once: {sorted(dupes)}")

    unknown = sorted(set(used) - declared)
    if unknown:
        problems.append(f"IDs used but never declared: {unknown}")

    missing = sorted(declared - set(used))
    if missing:
        problems.append(f"IDs declared but never closed: {missing}")

    numbers = [day.n for day in days]
    if numbers != list(range(0, len(numbers))):
        problems.append("day numbers are not contiguous from 0")

    total_ids = sum(len(cs) for _, cs in CURRICULA.values())
    print(f"curricula      : {len(CURRICULA)}")
    print(f"concept IDs    : {total_ids}")
    print(f"days           : {len(days)}  (Day 0 + Days 1-{max(numbers)})")
    print(f"phases         : {len(PHASES)}")
    print(f"IDs per day    : {total_ids / (len(days) - 1):.2f} (excluding Day 0)")
    print()
    for prefix, (name, cs) in CURRICULA.items():
        print(f"  {prefix:<6} {len(cs):>3}  {name}")
    print()
    if problems:
        for p in problems:
            print("PROBLEM:", p)
        raise SystemExit(1)
    print("OK - every declared ID is closed exactly once.")




# --- table emission ---------------------------------------------------------------



# Days whose title takes a marker in the map. 💥 = the deliberate-failure part is the day's
# centre of gravity. 🅿️ = the day is parked/awareness-level. 🔍 = build first, compare after.
BURST = {21, 23, 25, 37, 42, 47, 53, 62, 63, 67, 74, 78, 87, 94, 104, 110, 115, 119,
         123, 126, 135, 144, 150}
PARKED = {16, 43, 54, 120, 121}
COMPARE = {18, 20, 34, 38, 80, 88, 92, 128, 137}

# Per-ID markers, applied in the curriculum tables.
ID_MARKS = {
    "PHY-12": "🅿️", "ROUTE-07": "🅿️", "ROUTE-18": "🅿️", "NET-24": "🅿️",
    "SOCK-08": "🅿️", "APP-19": "🅿️", "WIRE-07": "🅿️", "WIRE-09": "🅿️",
    "DC-08": "🅿️", "DC-11": "🅿️",
    "LINK-09": "💥", "LINK-12": "💥", "NET-15": "💥", "ROUTE-06": "💥",
    "ROUTE-17": "💥", "TRANS-13": "💥", "TRANS-15": "💥", "TRANS-21": "💥",
    "CONG-10": "💥", "DNS-06": "💥", "APP-07": "💥", "SEC-13": "💥", "SEC-22": "💥",
    "WIRE-06": "💥", "DC-04": "💥", "DC-10": "💥", "PERF-05": "💥", "OPS-06": "💥",
    "SOCK-07": "🔍", "LINK-15": "🔍", "NET-17": "🔍", "DNS-07": "🔍",
}


def closes_on() -> dict[str, int]:
    return {i: day.n for ph in PHASES for day in ph.days for i in day.ids}


def curriculum_tables() -> str:
    where = closes_on()
    out: list[str] = []
    section = 8
    for prefix, (name, concepts) in CURRICULA.items():
        last = f"{prefix}-{len(concepts):02d}"
        out.append(f"## {section} · Curriculum `{prefix}` — {name} "
                   f"({prefix}-01..{last.split('-')[1]})\n")
        out.append("| ID | Concept | Closes on |")
        out.append("| --- | --- | --- |")
        for i, concept in enumerate(concepts, start=1):
            cid = f"{prefix}-{i:02d}"
            mark = ID_MARKS.get(cid, "")
            text = f"{mark} {concept}" if mark else concept
            out.append(f"| `{cid}` | {text} | {where[cid]} |")
        out.append("")
        section += 1
    return "\n".join(out)


def phase_table() -> str:
    out = ["| Phase | Days | Theme | Gate |", "| --- | --- | --- | --- |"]
    for ph in PHASES:
        ns = [d.n for d in ph.days]
        span = f"{ns[0]}" if len(ns) == 1 else f"{ns[0]}–{ns[-1]}"
        bold = "**" if ph.n == 0 else ""
        out.append(f"| {bold}{ph.n}{bold} | {bold}{span}{bold} | {bold}{ph.name}{bold} "
                   f"| {ph.gate} |")
    return "\n".join(out)


def day_map() -> str:
    out: list[str] = []
    for ph in PHASES:
        ns = [d.n for d in ph.days]
        span = f"Day {ns[0]}" if len(ns) == 1 else f"Days {ns[0]}–{ns[-1]}"
        out.append(f"#### Phase {ph.n} — {ph.name.split(':')[0]} ({span})\n")
        out.append("| Day | Title | IDs closed |")
        out.append("| --- | --- | --- |")
        for day in ph.days:
            marks = "".join(m for m, s in (("💥", BURST), ("🅿️", PARKED), ("🔍", COMPARE))
                            if day.n in s)
            title = f"{marks} {day.title}" if marks else day.title
            ids = ", ".join(f"`{i}`" for i in day.ids) or "—"
            out.append(f"| {day.n} | {title} | {ids} |")
        out.append("")
    return "\n".join(out)


def emit_tables() -> None:
    def dash(t: str) -> str:
        return t.replace(" - ", " — ")

    with open("tables_curricula.md", "w") as fh:
        fh.write(dash(curriculum_tables()))
    with open("tables_phases.md", "w") as fh:
        fh.write(dash(phase_table()))
    with open("tables_daymap.md", "w") as fh:
        fh.write(dash(day_map()))
    print("wrote tables_curricula.md, tables_phases.md, tables_daymap.md")


if __name__ == "__main__":
    verify()
    emit_tables()

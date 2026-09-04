---
plan: jala
version: "v1.0.0"
curricula: 15
ids: 248
days: 152
phases: 17
doc_architecture: "hub + parts/ (see §24)"
day_count_is: "derived, not chosen (see §23.0)"
created: "2026-08-27"
amended: "2026-08-27"
---

# 🕸️ MASTER PLAN v1.0.0 — Project **Jāla**
## Computer networks from the wire up — frames · addresses · routing · TCP · TLS · the running network

> **Jāla** (Sanskrit जाल) means *a net*: the mesh, the web, the thing made entirely of knots and the
> gaps between them. That is the right image. A network is not a cable and not a protocol; it is a
> set of agreements about what the knots do when a message arrives, and every one of those
> agreements is something you can build.
>
> 📌 **Purpose:** the single source of truth. Every later document points back here.
>
> **You build the stack.** Not a diagram of a stack — the frame, the ARP responder, the IPv4
> forwarder, the TCP state machine, the congestion controller, the DNS resolver, the HTTP server,
> the routing protocols, the tunnel. Each one hand-rolled first and *then* compared against the
> kernel, `scapy`, `dnspython` or `curl`, so that the tools everybody uses become conveniences you
> can read rather than mysteries you invoke.
>
> ⚠️ **Zero budget is a hard constraint, not an aspiration.** No lab hardware, no cloud account, no
> paid VPS, no switch, no router, no second machine. Every day runs inside network namespaces on one
> laptop. If a day cannot be done that way it is redesigned until it can, or it is explicitly parked
> 🅿️ as reading **with the arithmetic worked**. See §4.
>
> ⚠️ **And one constraint no other curriculum needs.** A model that trains badly wastes your
> afternoon. A packet sent badly reaches somebody else's machine. §4.2 is a rule about other
> people's networks, and it is not optional.

---

## 📑 Table of Contents

| §  | Section |
| --- | --- |
| 1  | 🎬 The Vision — one stack, fifteen threads |
| 2  | 🧭 Core Principles — rules we never break |
| 3  | 🏗️ The Artifact — what Jāla actually is |
| 4  | 🧪 Lab & Budget Policy — the $0 constraint, and the ethics rule |
| 5  | ⚙️ The Stack — tools, versions, specs, verification |
| 6  | 💥 The Five Silent Failures — how networks go wrong quietly |
| 7  | 🧶 The Fifteen Curricula & the ID scheme |
| 8  | 🧱 Curriculum FOUND — Foundations & the model |
| 9  | 〰️ Curriculum PHY — The physical layer & signalling |
| 10 | 🔗 Curriculum LINK — The link layer & switching |
| 11 | 📮 Curriculum NET — The network layer & addressing |
| 12 | 🗺️ Curriculum ROUTE — Routing |
| 13 | 🚚 Curriculum TRANS — Transport & TCP |
| 14 | 🌊 Curriculum CONG — Congestion control & queueing |
| 15 | 🔌 Curriculum SOCK — The socket API & concurrency |
| 16 | 🏷️ Curriculum DNS — Naming & DNS |
| 17 | 💬 Curriculum APP — Application protocols |
| 18 | 🔐 Curriculum SEC — Security, TLS & trust |
| 19 | 📡 Curriculum WIRE — Wireless & mobility |
| 20 | 🏢 Curriculum DC — Datacenter, cloud & overlays |
| 21 | 📊 Curriculum PERF — Performance, measurement & capture |
| 22 | 🛠️ Curriculum OPS — Operations, troubleshooting & discipline |
| 23 | 🗓️ The Day Map (day → IDs closed) |
| 24 | 📐 The Depth Contract — how a day is written |
| 25 | 🚦 Phase Gates & the Freshness Check |
| 26 | 📒 Ledgers & Traceability |
| 27 | ✍️ The Style Guide |
| 28 | 📝 Amendment record |

---

## 1 · 🎬 The Vision — one stack, fifteen threads

By the final day you will have **built a working network stack in user space, run a small internet
on your own laptop, and measured it honestly** — and you will be able to defend every number in it.
You will have written the frame, the ARP responder, the IPv4 forwarder, the TCP state machine, three
congestion controllers, a distance-vector protocol, a link-state protocol, a BGP speaker, a DNS
resolver, an HTTP/1.1 server, a TLS client that actually verifies, and a tunnel — and you will have
broken each of them on purpose.

Three commitments shape everything:

1. **One artifact, not disconnected exercises.** Every concept lands as a change to Jāla. The
   checksum you write on Day 14 verifies the frame you build on Day 18, which carries the IPv4
   packet you forward on Day 34, which carries the TCP segment whose retransmission timer you tune
   on Day 65 — and which fails on Day 37 because a tunnel you have not built yet will one day take
   twenty bytes off your MTU.
2. **The repo is the memory, not the chat.** Ledgers plus day documents mean any capable CLI agent
   can pick up exactly where the last one stopped — and more importantly, **every measurement is
   reproducible from a committed topology script and a seed.**
3. **Measured beats quoted.** "TCP slow start doubles the window each RTT" is a sentence from a
   textbook. A graph of *your* congestion window, produced by *your* sender, over a link where *you*
   set the delay to 40 ms and the loss to 1%, across five seeds, with the spread shown — that is a
   result. This curriculum is built out of the second kind (Principle 8).

### 1.1 Stated non-goals (decisions, not blind spots)

| Excluded | Why |
| --- | --- |
| Vendor certification tracks and their configuration syntax | A vendor's CLI is a dialect. This plan teaches the protocol the dialect configures; you can read any vendor's manual afterwards, and none of them will teach you what a `SYN` costs. |
| Writing cryptographic primitives | **Never.** You use a reviewed library and learn to reason about what it guarantees (§2, Principle 3). A hand-rolled cipher in a teaching repo is a liability that outlives the lesson. |
| Kernel and driver development, NIC offload internals | `EFF`-style systems work with its own curriculum. §10 and §20 teach what checksum offload and XDP *do* and where they change what you observe; writing the driver is a different course. 🅿️ awareness only. |
| Radio-frequency engineering and antenna design | §19 teaches the wireless channel as it affects packets. Link budgets and antenna patterns are a physics course. |
| Formal queueing theory beyond the working set | §14 teaches utilisation, Little's law and the knee of the curve, because those change what you build. The M/M/1 derivations are cited, not taught. |
| Paid labs, cloud accounts, physical hardware | The $0 constraint (§4) is absolute. |
| Attacking anything you do not own | Not a scoping decision — a legal and ethical one (§4.2). |

---

## 2 · 🧭 Core Principles — rules we never break

1. **Doc-first.** The day document is written before any code; the code follows the doc.
2. **One day, one commit.** Traceable, append-only history.
3. **Build first, compare after — except cryptography, which you never build.** Hand-roll the
   mechanism once — the checksum, the switch, the forwarder, the TCP state machine, the resolver,
   the parser — *then* open the tool that does it and diff your understanding against theirs. A
   library you have re-implemented is a convenience; one you have only imported is a mystery with a
   nice API. **The single exception is cryptography.** You will use `cryptography`'s primitives to
   drive a TLS handshake and a tunnel, and you will read the specification closely enough to say
   what each primitive guarantees — but you will not write AES, or a curve, or an HMAC, at any
   point, for any reason. The exception is stated as a principle because "build it to understand it"
   is right everywhere else in this plan, and the one place it is dangerously wrong needs to be
   named rather than assumed.
4. **Every concept is load-bearing.** If removing it would not change Jāla or change how you would
   defend Jāla, it does not get a day.
5. **Simple language plus a concrete example, always.** If a concept cannot be explained simply with
   an example, it is not understood yet (§27 enforces this).
6. **Never invent a version.** Package versions, tool versions, kernel features: looked up live, or
   a `TODO` containing **the exact lookup command**. Every pin gets a dated row in
   `docs/PACKAGES.md`.
7. **Never invent an API — and never invent a header field, a flag, a default or a bit offset.**
   Every library symbol is verified against that library's docs or source **for the version actually
   pinned**. Every wire-format detail is verified against **the specification, read on the day it is
   used**, and the document names the RFC and the section. A header diagram remembered from a
   lecture slide is how a byte offset goes wrong, and a byte offset that is wrong produces a packet
   that is silently ignored rather than an error.
8. **Never invent a number.** Every empirical claim carries its provenance: either *"measured here,
   on `<topology>`, `<netem settings>`, seed `<n>`, `<n>` repetitions, `<hardware>`, `<date>`"* or
   *"specified in RFC NNNN §N"* or *"reported in `<paper>`, `<venue>`, `<year>`"*. A default timer
   value, an MTU, a header size, a "typical" RTT or a throughput figure recalled from memory is a
   rumour, and rumours are how network arguments are won by the wrong person.
9. **Topologies, configs and scripts are committed. Captures and keys never are.** Every measurement
   is reproducible from what is in git. `docs/MEASUREMENTS.md` is the ledger; a measurement without
   a topology, a seed, a repetition count and a hardware line did not happen. **A capture is
   evidence, not source** — it can contain credentials, and it is regenerated, never committed
   (§26).
10. **Fail honestly.** A topology that would not converge is reported as not converging. A
    throughput number that got worse after your "optimisation" says so. This applies to you as much
    as to the code.
11. **Every day ends with at least one check that can go RED.**
12. **Reproduce the fault before you fix it.** You may not claim a fix for a failure you cannot
    cause on demand. This is the network equivalent of a failing test: if you cannot make the
    connection hang, you do not know why it hung, and the thing you changed is a coincidence with
    good timing. Every day that diagnoses something also *injects* it.
13. **Blast radius before capability.** Every new power — a raw socket, a spoofed source address, a
    scan, a flood, a tunnel, a served port — arrives together with its containment story. **Your
    traffic stays inside your own namespaces; the public internet is read-only** (§4.2). This is not
    a style preference. It is the difference between a lab and an incident report with your name on
    it.
14. **If reality changes, the plan is amended first.** An RFC obsoleted, a tool's flag removed, a
    kernel default changed → versioned addendum + `docs/CHANGELOG_PLAN.md` → *then* code. Never
    silently adapt; stop and say so.
15. **Zero budget is a feature.** You cannot buy a second router, so you will build one. You cannot
    rent a 200 ms transatlantic link, so you will create one with `tc netem` and know exactly what
    you configured. A student with a rack of real hardware never learns what a topology *is*; you
    will, because yours is a script (§4).
16. **Depth over density.** A day is a hub plus one document per subtopic (§24), never one long
    page. A wall of text is not depth — it is depth's disguise.
17. **No clocks.** A day is a unit of subject, not a unit of time. Never write a time estimate, a
    duration, an "estimated hours" field or a suggested pace — anywhere. A topic is finished when it
    is understood, however many sittings that takes. **Never trim an explanation because a day is
    getting long; split it into another part instead.**
18. **Assume no prior knowledge, finish at production.** Open where someone who has never met the
    idea can stand, define every term on first use — *including terms from earlier days, with a link
    back* — and carry it through to the real-system version: what changes at scale, what an operator
    does differently from the tutorial version, what a reviewer says, what an interviewer probes.
19. **The day count is derived, not chosen.** 152 days is an *output* of decomposing 248 concepts
    into idea-sized units — not a target anyone picked, and not a schedule. When content demands a
    day be split, it is split by ADR and the count changes. **A round number would have been a
    warning sign** (§23.0).
20. **Wire formats are stated, never inferred.** Any part that introduces or parses a header carries
    a **`## Wire format`** table: byte offset, bit width, field name, the value in *this* example,
    and what it means. More protocol bugs are offset and endianness bugs than logic bugs, and a
    document that leaves the reader to count bytes has taught them something they cannot debug.

> Principles 3, 8, 9, 12, 13 and 20 are the ones this curriculum adds to ordinary engineering
> discipline, because networks fail *quietly* (§6) and because networking mistakes leave your
> machine. They are made concrete by **§24, the depth contract**, and enforced mechanically by
> `scripts/depth_check.py` (`./m depth N`).

---

## 3 · 🏗️ The Artifact — what Jāla actually is

**Jāla is a user-space network stack you write, running over a TUN/TAP device, plus the virtual
internet you run it on, plus the measurements that prove it works.**

What exists when the plan is finished:

- **A link layer you wrote** — Ethernet framing, CRC-32 checked against a real capture, a learning
  switch with a MAC table and ageing, VLAN tagging, and an ARP responder that answers an unmodified
  `ping` from a neighbouring namespace.
- **A network layer you wrote** — the IPv4 header built and parsed by hand, longest-prefix-match
  forwarding over a trie, TTL handling, checksum, fragmentation and reassembly, ICMP, and a NAT with
  a real translation table. Plus IPv6, and the ICMPv6 rule that breaks it when a firewall is too
  keen.
- **Routing protocols you wrote** — distance vector (and the count-to-infinity you caused on
  purpose), link state with Dijkstra over a flooded database, and a BGP speaker that opens a
  session, exchanges a prefix, applies a local-preference policy and withdraws cleanly.
- **A TCP you wrote** — the full eleven-state machine, sequence and acknowledgement handling, the
  RTT estimator with Karn's algorithm, retransmission, fast recovery, SACK, flow control, and the
  options. It completes a handshake with an unmodified `curl` and transfers a file correctly under
  5% loss.
- **Three congestion controllers you wrote** — Reno, CUBIC and a delay-based controller, each
  producing its own characteristic trace under `tc netem`, reported across seeds with the spread.
- **A resolver you wrote** — DNS messages parsed by hand including name compression, iterative
  resolution from the root, a cache that counts TTLs down correctly, and negative caching.
- **An HTTP/1.1 server and client you wrote** — on a raw socket, with keep-alive and chunked
  encoding, serving an unmodified browser, and rejecting a request-smuggling attempt because you
  understand where the desync comes from.
- **A TLS client you wrote** — driving the 1.3 handshake with primitives from a reviewed library
  (never your own), validating a real certificate chain, and rejecting a name mismatch, an expired
  certificate and a self-signed one.
- **A tunnel you wrote** — a WireGuard-shaped encrypted tunnel over UDP between two namespaces, with
  the MTU arithmetic worked out rather than guessed.
- **A virtual internet** — `lab/` topology scripts that build hosts, switches, routers, a NAT, a
  firewall and a leaf-spine fabric out of `ip netns`, `veth` and `tc netem`, from nothing, twice,
  identically.
- **A measurement harness** — your own `ping`, `traceroute`, throughput tool and pcap parser, plus a
  runner that repeats, seeds, warms up and reports p50/p95/p99 and the spread.
- **A design document and a runbook** — the network you would build for a stated requirement, with
  the arithmetic, the threat model, the failure modes and the diagnosis procedure. Written because
  `OPS-12` requires it, not because a form asked.

**Repo layout (established Day 0, grown daily):**

```
jala/
├── m                       # the driver — ./m check | depth | lab | cap | start | done  (Day 0)
├── Makefile                # a two-line shim so `make check` still reaches ./m check
├── CLAUDE.md               # standing instructions for the driver agent                 (Day 0)
├── README.md               # what this is, and how a stranger runs it
├── pyproject.toml          # uv-managed; every pin dated in docs/PACKAGES.md
├── uv.lock                 # the exact transitive tree; committed
│
├── days/                   # 📚 THE TEACHING — one folder per day
│   ├── README.md           #    how to read a day
│   └── day-NNN-<slug>/     #    the number is the identity, the slug says what it teaches
│       ├── LESSON.md       #    the hub: story, part map, setup, build brief, check, ledger
│       ├── CHECKLIST.md    #    the definition of done; ./m done NNN refuses until ticked
│       ├── parts/          #    one document per subtopic — the actual teaching
│       │   ├── 01-<slug>/1.1-<slug>.md …
│       │   └── 02-<slug>/2.1-<slug>.md …
│       └── lab/            #    the learner's own scratch code for that day
│
├── jala/                   # the stack — you write every line, from the docs
│   ├── wire/               #   framing, checksums, CRC, hexdump, the header codecs
│   ├── stack/              #   arp, ipv4, ipv6, icmp, udp, tcp — over a TUN/TAP device
│   ├── route/              #   the LPM trie, distance vector, link state, the BGP speaker
│   ├── resolve/            #   the DNS message codec and the iterative resolver
│   ├── app/                #   the HTTP/1.1 server and client, the framing parsers
│   ├── crypt/              #   the TLS 1.3 client and the tunnel — primitives imported, never written
│   └── probe/              #   ping, traceroute, the pcap parser, the measurement harness
├── lab/                    # topology scripts: netns, veth, bridges, netem. Committed. Idempotent.
├── scripts/                # repo tooling: depth_check.py · tracker.py · trace.py
├── tests/                  # pytest; deterministic, no root, no external network
└── docs/
    ├── 00_MASTER_PLAN.md          # this file
    ├── CURRICULUM_INDEX.md        # generated: ID → day
    ├── TRACKER.md · TRACEABILITY.md          # generated
    ├── PROGRESS.md · PACKAGES.md · SPECS.md · TOPOLOGIES.md · CAPTURES.md
    ├── MEASUREMENTS.md · CHANGELOG_PLAN.md
    └── adr/                       # architecture decision records
```

> ⚠️ **Nothing under `jala/` or `tests/` is pre-written.** Every line is printed in a day document
> and typed by the learner (`days/README.md`, rule 1). You cannot debug a retransmission storm on
> Day 65 that you never typed on Day 60.
>
> ⚠️ **`.gitignore` blocks `*.pcap`, `*.pcapng`, `captures/`, `*.pem`, `*.key`, `keys/`.**
> Principle 9, and it has two separate reasons. A capture is **evidence**: it is regenerated from a
> committed topology, and it may contain a session cookie, a password on a plaintext protocol, or a
> colleague's traffic. A private key in git history is unremovable and permanently compromised —
> including the throwaway one you generated for a lab, because "throwaway" is a claim about
> intention, not about who cloned the repo.

---

## 4 · 🧪 Lab & Budget Policy — the $0 constraint, and the ethics rule

### 4.1 The four tiers

**The rule: no day in this plan may require a payment, a billing account, a second machine, or a
single piece of network hardware.** Everything runs on one of four tiers, and every day states which
it is on.

| Tier | What it is | What it runs |
| --- | --- | --- |
| **L0 — one host, user space** | The default. No root beyond a TUN device, no namespaces. | Header codecs, checksums, parsers, the pcap reader, protocol state machines driven by test vectors, arithmetic. The majority of days start here. |
| **L1 — the virtual lab** | Linux network namespaces, `veth` pairs, bridges and `tc netem` on the same laptop. Multiple "machines" for free. | Switching, routing, forwarding, NAT, firewalls, TCP against a real peer, congestion control under configured delay and loss, leaf-spine fabrics, overlays. |
| **L2 — the public internet, read-only** | `dig`, `traceroute`, `curl`, public looking glasses, public BGP route collectors, public measurement platforms. | Observing the real Internet: a real delegation chain, a real AS path, a real certificate chain, a real RTT to another continent. **Read-only. See §4.2.** |
| **L3 — 🅿️ parked** | Cannot be done at $0 or cannot be done legally. | Real BGP peering with an ASN and address space, carrier optics, 100G NICs, a cellular core, a globally distributed anycast deployment. Taught as reading, **with the arithmetic worked**, so the thing you did not run is still a thing you can size. |

The rules that follow from it:

- **Every L1 day is a script, not a sequence of instructions.** A topology you built by typing
  fourteen commands is a topology you cannot rebuild. `lab/<name>.sh` is committed, idempotent, and
  runs twice without complaint (`OPS-03`).
- **Every L1 day states its topology in the hub** and in each part that runs something: the
  namespaces, the links, the addresses, the netem settings. A measurement without a topology is an
  anecdote (§24.4, the `## Topology` section).
- **Linux is required for L1, and it is free.** Native Linux, WSL2 on Windows, or a free Linux VM on
  macOS. Namespaces are a Linux feature; macOS and Windows have no equivalent, and this plan says so
  rather than pretending. Day 0 sets this up and states exactly what each host operating system can
  and cannot do.
- **Never write code that silently requires root.** Where a day needs a capability, the document
  says which one, why, and what the unprivileged version demonstrates instead.
- **Budgets are denominated in namespaces, links and configured delay** — never in dollars, and
  never in time. A day's hub states its tier; `L0` is an answer and must be stated.

### 4.2 🛑 The ethics rule — the one that has nothing to do with money

Every other curriculum's worst case is a wasted evening. This one's worst case is a criminal
offence, and pretending otherwise would be a failure of the plan rather than a matter of taste.

**Rules that hold on every day, without exception:**

1. **Traffic you generate stays inside your own namespaces.** Every scan, flood, spoof, injection,
   replay, deauthentication and man-in-the-middle exercise in this plan runs against machines you
   created with `ip netns add` sixty seconds earlier and will delete afterwards.
2. **The public internet is read-only, and gently.** `dig`, `traceroute`, `curl`, a looking glass, a
   public route collector — a handful of requests, at human speed, to services that publish
   themselves for exactly this. Never a scan, never a flood, never an automated sweep, never a
   protocol violation aimed at somebody else's host.
3. **Your employer's network and your university's network are not your lab.** They belong to
   somebody who has not agreed. A packet capture on a shared network collects other people's
   traffic, which is a privacy question before it is a technical one.
4. **A capture is evidence and is handled as such** (`SEC-22`). It may contain credentials. It is
   never committed, never shared without redaction, and deleted when the day is done.
5. **In many jurisdictions, port-scanning a host you do not own is a crime**, regardless of intent
   and regardless of whether anything broke. This plan does not offer a legal opinion, and neither
   should you: it tells you where the line is drawn safely, which is inside `ip netns`.

`SEC-02` is the day that teaches this properly — the threat model, the law as a shape rather than a
citation, and how professional testing gets its authorisation in writing. **It sits at the front of
the security phase because everything after it is a technique that is fine in a namespace and a
serious matter anywhere else.** Every part in this plan that teaches an attack states, in its
`## Topology` section, the namespaces it runs in.

---

## 5 · ⚙️ The Stack — tools, versions, specs, verification

- **Language:** Python **3.12** (`uv`-managed). Exact `==` pins in `pyproject.toml`; `uv.lock`
  committed; a dated row in `docs/PACKAGES.md` for every install. Python is the right choice here
  precisely because it is slow: a stack you can read at 40 megabits is a better teacher than one you
  cannot read at 40 gigabits, and where speed is the lesson, §21 measures the gap instead of hiding
  it.
- **System tools** arrive from the distribution, never from a download: `ip` (iproute2), `ss`,
  `tcpdump`, `tshark`, `dig`, `curl`, `nft`, `tc`, `socat`, `openssl`. Wireshark's GUI is used for
  reading captures and is never required by a check.
- **Python libraries arrive on the day they are first used, never up front** — and after the
  hand-rolled version exists (Principle 3). The comparison days are exactly where `scapy`,
  `dnspython`, `httpx`, `cryptography` and the plotting library enter, each *after* your own version
  works.
- **`cryptography` is the one exception to "build first"** (Principle 3). It arrives on the day the
  TLS phase starts, and it arrives as a primitive provider, not as a black box: the day names the
  algorithm, the RFC section that specifies its use, and what the primitive guarantees.
- **Version verification is per-day and live** (Principle 6). No version in this plan is written from
  memory; every day's hub §8 names what was actually fetched and when.

### 5.1 Specifications are pinned the way packages are

A protocol specification is a dependency, and it moves. TCP's specification is no longer the document
everybody cites from memory: **RFC 9293 (August 2022) obsoletes RFC 793** and folds in decades of
scattered updates. CUBIC's is no longer RFC 8312: **RFC 9438 (August 2023) obsoletes it** and moves
CUBIC to Standards Track. *(Both checked at `rfc-editor.org`, 2026-08-27.)* A curriculum that quotes
section numbers from the superseded document sends its reader to text that has been replaced.

So specs get the same discipline as packages:

- **Every RFC is resolved live on the day it is used**, at `https://www.rfc-editor.org/rfc/rfcNNNN`,
  and the day confirms on the info page that it is **not marked "Obsoleted by"**. If it is, the day
  reads the successor and **amends the plan first** (Principle 14).
- **Every citation names the section**, never just the number. "RFC 9293" is a shelf; "RFC 9293
  §3.1" is a sentence you can be held to.
- **Every spec read gets a dated row in `docs/SPECS.md`**: number, title, status, obsoletes/obsoleted
  by, sections read, date, day.
- **IEEE standards are cited by number and year** (802.3, 802.1Q, 802.11) with the same rule, and
  the plan notes where the document is paywalled and what the freely available substitute is.
- Where behaviour is *implementation-defined* rather than specified — a default timer, a queue
  length, a backlog cap — the day **reads it off the running system** and says which system, which
  kernel version, and when. A default is not a fact about the protocol; it is a fact about a build.

---

## 6 · 💥 The Five Silent Failures

Ordinary software fails loudly: a stack trace, a 500, a red test. **Networks fail quietly** — the
connection establishes, the page loads, the benchmark prints a number, and the thing you believe you
proved is not the thing that happened. These five will each cost you a week if you have not been
taught to look for them, and **every day document that touches one must name it in words** (§24.4.1).

| # | Trap | What you see | What is actually happening |
| --- | --- | --- | --- |
| 1 | **The cache answered, not the network** | Your fix works. Your colleague's identical machine still fails. | An ARP entry, a DNS answer, a warm TCP connection or a browser's connection pool served the request without touching the thing you changed. You tested a path that was never exercised. Cold-start every test. `LINK-15`, `DNS-06`, `SOCK-12`. |
| 2 | **The MTU black hole** | The connection opens instantly. The transfer hangs at a few kilobytes, forever, with no error. | Small packets fit; a full-size one does not, and the ICMP "fragmentation needed" that would have said so is blocked by a firewall being helpful. Nothing errors, nothing logs, and it only happens over one path. `NET-15`, `DC-06`, `SEC-16`. |
| 3 | **TCP is a byte stream, not a message queue** | Works perfectly on loopback with small messages. Corrupts under load, or over a real link, or when the payload crosses one particular size. | Your code assumed one `send` equals one `recv`. TCP guarantees ordered bytes and nothing else: it will split your message, or deliver two of them in one read. The bug is in the *reader*, and it appears the day latency changes. `TRANS-15`, `TRANS-16`, `APP-06`. |
| 4 | **Averaged away** | Version B is 12% faster. Ship it. | One run each, no warm-up, mean latency reported, the transfer shorter than slow start. The difference is inside the noise band, or it is an artefact of the measurement window. `PERF-02`, `PERF-05`, `CONG-14`. |
| 5 | **The middlebox rewrote it** | Perfect in the lab, broken in production — or vice versa. | A NAT rewrote a port, a stateful firewall dropped an idle flow after its own timeout, a proxy re-terminated the TLS session, a load balancer changed the source address. Your two-namespace lab has none of these; production has four. `NET-18`, `SEC-18`, `DC-09`. |

> Any day document that touches one of these areas must say which trap it is avoiding, and how the
> reader would detect it. A reader who has been following tutorials needs to be **told**, not
> protected.

---

## 7 · 🧶 The Fifteen Curricula & the ID scheme

Every concept in the plan has an ID. A day **closes** an ID when the concept is built into (or
demonstrably exercised against) Jāla and the day's gates are green. `docs/TRACEABILITY.md` is
regenerated from the day hubs by `scripts/trace.py`; **any open ID from a completed phase is a bug.**

The curricula are grouped into five books. The books are for navigation; the ID prefix is the
identity.

### Book I — The wire: what a link is

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Foundations | `FOUND` | 14 | Layering, encapsulation, the five words, reading a spec, reading a capture, building the lab |
| Physical | `PHY` | 12 | Bits, clocks, coding, latency, the bandwidth-delay product, errors and how to detect them |
| Link | `LINK` | 22 | Framing → Ethernet → switching → VLANs → STP → ARP → MTU → DHCP → neighbour discovery |

### Book II — The internetwork: addresses and paths

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Network | `NET` | 24 | IPv4 built, subnetting, CIDR, forwarding, fragmentation, ICMP, NAT, IPv6, dual stack |
| Routing | `ROUTE` | 18 | Static → distance vector → link state → OSPF → autonomous systems → BGP → hijacks |

### Book III — The conversation: transport

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Transport | `TRANS` | 24 | Ports, UDP, reliability from first principles, the TCP state machine, timers, options |
| Congestion | `CONG` | 14 | AIMD, Reno, CUBIC, BBR, queues, bufferbloat, AQM, ECN, measuring honestly |
| Sockets | `SOCK` | 12 | The syscalls, the backlog, C10K, readiness APIs, the event loop, backpressure |

### Book IV — The services: names, applications, trust

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Naming | `DNS` | 12 | The delegation tree, the message format, an iterative resolver, TTLs, DNSSEC, encrypted DNS |
| Applications | `APP` | 20 | HTTP/1.1 built, smuggling, caching, HTTP/2, QUIC, WebSocket, gRPC, mail, media |
| Security | `SEC` | 22 | Threat model, the ethics rule, attacks reproduced, TLS 1.3, PKI, tunnels, firewalls, DDoS |

### Book V — Real networks

| Curriculum | Prefix | Count | Thread |
| --- | --- | --- | --- |
| Wireless | `WIRE` | 10 | The channel, the 802.11 MAC, association, Wi-Fi security, airtime, cellular, mobility |
| Datacenter | `DC` | 18 | Leaf-spine, ECMP, incast, overlays, SDN, load balancing, anycast, containers, Kubernetes |
| Performance | `PERF` | 14 | What to measure, distributions, the harness, netem, capture, diagnosis, telemetry |
| Operations | `OPS` | 12 | The repo as memory, address plans, config as code, the method, incidents, runbooks |

**Total: 248 concept IDs across 15 curricula.**

> 🅿️ Some IDs are **parked** (awareness-level): you learn the map and the arithmetic, you do not
> build the thing — either because it cannot be done at $0 (§4, L3) or because it is a different
> discipline. A parked ID still gets a full part with a story, a mechanism and a production section.
> What it does not get is a build step. Parked IDs close normally.

The per-ID topics are stated in §§8–22. The **authoritative day→ID assignment is §23**, and a day
document closes **exactly** the IDs §23 assigns it — no more, no fewer.

---

## 8 · 🧱 Curriculum `FOUND` — Foundations & the model (FOUND-01..14)

Everything the rest of the plan assumes, built rather than asserted. No prior networking is
presumed; what is presumed is that you can read Python and open a terminal. The phase ends with a
virtual internet running on your own laptop, which every later phase uses.

| ID | Concept | Closes on |
| --- | --- | --- |
| `FOUND-01` | What a network is — two machines, one wire, and the problem of whose turn it is | 2 |
| `FOUND-02` | Layering as an engineering decision — what a layer buys and what it costs | 2 |
| `FOUND-03` | OSI's seven layers vs the Internet's four — which one is real, which one is vocabulary | 3 |
| `FOUND-04` | Encapsulation and decapsulation — the envelope inside the envelope | 3 |
| `FOUND-05` | The header — why every protocol starts with fixed fields, and how you read one | 4 |
| `FOUND-06` | Four names for one machine — MAC, IP, port, hostname, and what resolves what | 4 |
| `FOUND-07` | Frame, packet, segment, datagram, message — using the five words correctly | 4 |
| `FOUND-08` | Circuit switching vs packet switching — the argument the Internet won, and its cost | 5 |
| `FOUND-09` | The end-to-end principle, and every place the Internet now violates it | 5 |
| `FOUND-10` | How a protocol becomes real — IETF, RFCs, IEEE, W3C, and the standards process | 6 |
| `FOUND-11` | Reading a spec — MUST/SHOULD/MAY, ABNF, and the packet diagram convention | 6 |
| `FOUND-12` | The five tools that see different things — ip, ss, tcpdump, dig, curl | 7 |
| `FOUND-13` | A capture is the ground truth — reading one pcap end to end, byte by byte | 8 |
| `FOUND-14` | The lab — network namespaces, veth pairs and bridges: an internet on one laptop | 9 |

---

## 9 · 〰️ Curriculum `PHY` — The physical layer & signalling (PHY-01..12)

The layer nobody lets you touch, taught anyway — because the numbers that constrain every layer
above it are set here. You will not build a transceiver. You will build the checksum and the CRC,
and you will be able to say what a bandwidth-delay product means for the buffer you size on Day 74.

| ID | Concept | Closes on |
| --- | --- | --- |
| `PHY-01` | Bits on a wire — voltage, time, and why both ends need the same clock | 10 |
| `PHY-02` | Bandwidth, bit rate, baud and the Shannon limit | 10 |
| `PHY-03` | Line coding — NRZ, Manchester, 4B/5B, 8b/10b, and why raw NRZ fails | 11 |
| `PHY-04` | Clock recovery, DC balance, and the danger of a long run of zeros | 11 |
| `PHY-05` | Latency decomposed — propagation, transmission, queueing, processing | 12 |
| `PHY-06` | The bandwidth-delay product — the pipe you have to keep full | 12 |
| `PHY-07` | Media — copper, multimode and single-mode fibre; the distance/rate trade | 13 |
| `PHY-08` | Multiplexing — FDM, TDM, WDM, OFDM as one idea in four costumes | 13 |
| `PHY-09` | Errors on the wire — BER, attenuation, crosstalk, and what noise does to a bit | 14 |
| `PHY-10` | Error detection — parity, the Internet checksum, and CRC-32, all built | 14 |
| `PHY-11` | Error correction — Hamming distance and FEC; when to correct, when to resend | 15 |
| `PHY-12` | 🅿️ The physical layer you can touch — NICs, transceivers, link training, the cable plant | 16 |

---

## 10 · 🔗 Curriculum `LINK` — The link layer & switching (LINK-01..22)

One wire, several machines, and the question of whose turn it is. This is where addresses first
appear, where the first device you build lives, and where the LAN's total absence of authentication
becomes something you can demonstrate rather than something you have been warned about.

| ID | Concept | Closes on |
| --- | --- | --- |
| `LINK-01` | The framing problem — where does a frame start, and where does it stop | 17 |
| `LINK-02` | Framing methods — length fields, sentinels, byte stuffing, bit stuffing | 17 |
| `LINK-03` | The Ethernet frame field by field, built by hand and put on the wire | 18 |
| `LINK-04` | MAC addresses — the OUI, broadcast, multicast, and the locally administered bit | 18 |
| `LINK-05` | The FCS — your CRC-32 checked against the one in a real capture | 18 |
| `LINK-06` | Shared media and collisions — CSMA/CD, and why it is history worth knowing | 19 |
| `LINK-07` | Collision domain vs broadcast domain — the distinction that killed the hub | 19 |
| `LINK-08` | The learning switch, built — the MAC table, flooding, and ageing | 20 |
| `LINK-09` | 💥 Duplex, autonegotiation, and the duplex mismatch that halves your throughput | 21 |
| `LINK-10` | VLANs and the 802.1Q tag — one wire, many broadcast domains | 22 |
| `LINK-11` | Trunks, access ports, and the native-VLAN trap | 22 |
| `LINK-12` | 💥 The loop and the broadcast storm — a redundant cable that kills a LAN | 23 |
| `LINK-13` | Spanning Tree — root election, port roles, and what convergence costs | 23 |
| `LINK-14` | Link aggregation — LACP, and the hash that decides which cable your flow takes | 24 |
| `LINK-15` | 🔍 ARP, built — request, reply, the cache, and the gratuitous announcement | 25 |
| `LINK-16` | ARP spoofing, and the fact that a LAN has no authentication at all | 25 |
| `LINK-17` | MTU and jumbo frames — a link-layer number that causes network-layer pain | 26 |
| `LINK-18` | Point-to-point links — PPP, and framing when there is nobody to address | 27 |
| `LINK-19` | DHCP — DORA, leases, options, and the rogue server on the guest network | 27 |
| `LINK-20` | The link layer under a hypervisor — tap, bridge, veth, macvlan | 28 |
| `LINK-21` | IPv6 Neighbor Discovery — ARP's replacement, plus RA, SLAAC and DAD | 29 |
| `LINK-22` | Inside the switch — store-and-forward vs cut-through, buffers, head-of-line blocking | 21 |

---

## 11 · 📮 Curriculum `NET` — The network layer & addressing (NET-01..24)

The layer that made an internet possible: one address space over any link technology, and a
forwarding decision small enough to make at every hop. Silent Failure #2 lives here, and so does the
single most useful diagnostic skill in the plan — reading a routing table out loud.

| ID | Concept | Closes on |
| --- | --- | --- |
| `NET-01` | Why a second address — the LAN does not scale, and the internetwork problem | 30 |
| `NET-02` | The IPv4 header field by field — built, parsed, and checked against a capture | 30 |
| `NET-03` | The IPv4 address — the dotted quad, and what the network/host split actually means | 31 |
| `NET-04` | Classful addressing, and the reason it had to be abandoned | 31 |
| `NET-05` | Masks and prefix length — the arithmetic, done in binary, by hand | 32 |
| `NET-06` | Subnetting and VLSM — carving a /24 into the subnets a building needs | 32 |
| `NET-07` | CIDR, supernetting and aggregation — how the routing table stays finite | 33 |
| `NET-08` | Special-purpose addresses — RFC 1918, loopback, link-local, multicast, broadcast | 33 |
| `NET-09` | The forwarding decision — longest prefix match, built | 34 |
| `NET-10` | The routing table on a real machine — `ip route` read line by line | 34 |
| `NET-11` | The default gateway — what the first hop knows that you do not | 35 |
| `NET-12` | TTL and the hop limit — the field that ends a loop nobody noticed | 35 |
| `NET-13` | The header checksum — computed by hand, and why IPv6 deleted it | 36 |
| `NET-14` | Fragmentation and reassembly — the ID, offset and MF fields, built | 36 |
| `NET-15` | 💥 Path MTU discovery and the PMTU black hole — the handshake works, the transfer hangs | 37 |
| `NET-16` | ICMP — echo, unreachable, time-exceeded, redirect; the network's error channel | 38 |
| `NET-17` | 🔍 ping and traceroute, both written from scratch, then diffed against the real ones | 38 |
| `NET-18` | NAT — the translation table, the port rewrite, and everything it breaks | 39 |
| `NET-19` | NAT traversal — STUN, TURN, ICE and hole punching | 39 |
| `NET-20` | IPv6 — the address, the header, and the list of things that were removed | 40 |
| `NET-21` | IPv6 addressing in practice — link-local, ULA, SLAAC, and the /64 convention | 40 |
| `NET-22` | ICMPv6 is not optional — and the firewall rule that silently breaks IPv6 | 41 |
| `NET-23` | Dual stack and Happy Eyeballs — the broken v6 path you never noticed | 42 |
| `NET-24` | 🅿️ Transition mechanisms — NAT64/DNS64, 464XLAT and tunnels | 43 |

---

## 12 · 🗺️ Curriculum `ROUTE` — Routing (ROUTE-01..18)

How a packet reaches a network nobody told your router about. The arc is deliberately historical:
you build distance vector and feel it fail, then link state, then the path-vector protocol that runs
the actual Internet — and by then "why is BGP like this?" has an answer instead of a shrug.

| ID | Concept | Closes on |
| --- | --- | --- |
| `ROUTE-01` | Routing vs forwarding — the control plane and the data plane, separated | 44 |
| `ROUTE-02` | Static routes, and the cases where they are still the right answer | 44 |
| `ROUTE-03` | The forwarding table as a longest-prefix trie, built and benchmarked | 45 |
| `ROUTE-04` | Administrative distance — choosing between two protocols that both have an answer | 45 |
| `ROUTE-05` | Distance vector — Bellman-Ford, built and run on your own topology | 46 |
| `ROUTE-06` | 💥 Count-to-infinity, reproduced on purpose; split horizon and poison reverse | 47 |
| `ROUTE-07` | 🅿️ RIP as the worked example — timers, hop limit, and why it faded | 47 |
| `ROUTE-08` | Link state — flooding the database, then Dijkstra, both built | 48 |
| `ROUTE-09` | OSPF — areas, LSA types, DR/BDR election, and forming an adjacency | 49 |
| `ROUTE-10` | OSPF convergence — what actually happens in the seconds after a cable is pulled | 49 |
| `ROUTE-11` | Interior vs exterior — why one Internet needs two kinds of routing protocol | 50 |
| `ROUTE-12` | Autonomous systems, ASNs, and the commercial shape of the Internet | 50 |
| `ROUTE-13` | BGP as path vector — and why policy beats shortest path | 51 |
| `ROUTE-14` | The BGP session — OPEN, UPDATE, KEEPALIVE, NOTIFICATION; a speaker you write | 51 |
| `ROUTE-15` | BGP path attributes and the decision process, evaluated in order | 52 |
| `ROUTE-16` | BGP policy — local preference, AS-path prepending, MED, communities | 52 |
| `ROUTE-17` | 💥 Route leaks and hijacks — the day a prefix vanished, and what RPKI/ROV does | 53 |
| `ROUTE-18` | 🅿️ Multicast routing and IGMP | 54 |

---

## 13 · 🚚 Curriculum `TRANS` — Transport & TCP (TRANS-01..24)

The largest thread alongside `NET`. You will build reliability from nothing — stop-and-wait, then
windows, then the real state machine — because a reader who meets TCP as a list of features learns
trivia, and a reader who meets it after writing selective repeat learns a design. Silent Failure #3
lives here.

| ID | Concept | Closes on |
| --- | --- | --- |
| `TRANS-01` | What transport adds — process to process, and the port number | 55 |
| `TRANS-02` | The five-tuple — how a packet finds one process among hundreds | 55 |
| `TRANS-03` | UDP — the header, the optional checksum, and the honesty of no guarantees | 56 |
| `TRANS-04` | A UDP echo server and client, built, then made to lose packets on purpose | 56 |
| `TRANS-05` | When UDP is the right answer — DNS, games, media, and QUIC | 57 |
| `TRANS-06` | Reliability from first principles — stop-and-wait, ARQ, and sequence numbers | 58 |
| `TRANS-07` | Duplicates, delays and wrap-around — the problems sequence numbers create | 58 |
| `TRANS-08` | Sliding windows — go-back-N and selective repeat, both built | 59 |
| `TRANS-09` | The TCP header field by field, built by hand | 60 |
| `TRANS-10` | The three-way handshake, and what a SYN cookie defends against | 60 |
| `TRANS-11` | The TCP state machine — all eleven states, drawn and implemented | 61 |
| `TRANS-12` | Teardown, half-close, and why TIME_WAIT has to last as long as it does | 62 |
| `TRANS-13` | 💥 TIME_WAIT accumulation and ephemeral port exhaustion, reproduced | 62 |
| `TRANS-14` | Sequence and acknowledgement numbers — the byte stream, and the numbers under it | 63 |
| `TRANS-15` | 💥 TCP is a byte stream, not a message queue — the partial-read bug | 63 |
| `TRANS-16` | Framing on top of TCP — length prefixes, delimiters, and the parser you must write | 64 |
| `TRANS-17` | Retransmission — the RTT estimator, Karn's algorithm and the RTO, implemented | 65 |
| `TRANS-18` | Fast retransmit and fast recovery — what three duplicate ACKs mean | 65 |
| `TRANS-19` | SACK — the retransmission you did not need to send | 66 |
| `TRANS-20` | Flow control — the receive window, the zero window, and the persist timer | 66 |
| `TRANS-21` | 💥 Silly window syndrome, Nagle, delayed ACK, and the interaction that adds 40 ms | 67 |
| `TRANS-22` | TCP options — MSS, window scale, timestamps, SACK-permitted | 67 |
| `TRANS-23` | Keepalives, half-open connections, and the peer that went away without saying so | 68 |
| `TRANS-24` | close, shutdown and SO_LINGER — what the socket API actually does to a connection | 68 |

---

## 14 · 🌊 Curriculum `CONG` — Congestion control & queueing (CONG-01..14)

The part of TCP that is not about your connection at all. It is about a shared resource nobody owns,
and about the fact that the polite algorithm and the fast algorithm are not the same algorithm.
Silent Failure #4 lives here, and this is the phase where the measurement discipline becomes
mandatory rather than advisory.

| ID | Concept | Closes on |
| --- | --- | --- |
| `CONG-01` | Congestion control vs flow control — two windows, one sender, different problems | 69 |
| `CONG-02` | The congestion collapse of 1986, and the algorithm that ended it | 69 |
| `CONG-03` | AIMD — why additive increase and multiplicative decrease converge to fairness | 70 |
| `CONG-04` | Slow start and congestion avoidance — the two phases, drawn from your own trace | 70 |
| `CONG-05` | Tahoe, Reno and NewReno, implemented on the stack you wrote | 71 |
| `CONG-06` | CUBIC — the window function, and the long-fat-pipe problem it solves | 72 |
| `CONG-07` | Delay-based control — Vegas, and the road the Internet did not take | 72 |
| `CONG-08` | BBR — modelling the bottleneck instead of waiting for loss | 73 |
| `CONG-09` | The queueing theory you actually need — utilisation, Little's law, and the knee | 74 |
| `CONG-10` | 💥 Bufferbloat — excellent throughput and terrible latency, measured on your own link | 74 |
| `CONG-11` | Active queue management — RED, CoDel and FQ-CoDel; dropping early on purpose | 75 |
| `CONG-12` | ECN — marking instead of dropping, and why deployment took twenty years | 75 |
| `CONG-13` | Fairness — RTT unfairness, and what TCP-friendly actually means | 76 |
| `CONG-14` | Measuring a congestion controller honestly — repetitions, spread, and the noise band | 76 |

---

## 15 · 🔌 Curriculum `SOCK` — The socket API & concurrency (SOCK-01..12)

Where your program meets the stack you just wrote. Everything here is the API you have already been
using, explained from the other side — and the point where "why is this server slow?" stops being a
protocol question and becomes a concurrency question.

| ID | Concept | Closes on |
| --- | --- | --- |
| `SOCK-01` | The socket API syscall by syscall — socket, bind, listen, accept, connect | 77 |
| `SOCK-02` | The backlog — the SYN queue, the accept queue, and what 'connection refused' means | 77 |
| `SOCK-03` | Blocking I/O and thread-per-connection, built and measured | 78 |
| `SOCK-04` | The C10K problem — the exact point where thread-per-connection stops | 78 |
| `SOCK-05` | Non-blocking sockets, EAGAIN, and the partial write | 79 |
| `SOCK-06` | select, poll and epoll — readiness, and the O(n) that was the whole bug | 79 |
| `SOCK-07` | 🔍 The event loop, built from `selectors`, then compared against `asyncio` | 80 |
| `SOCK-08` | 🅿️ Readiness vs completion — io_uring and IOCP | 81 |
| `SOCK-09` | The socket options that matter — SO_REUSEADDR, SO_REUSEPORT, TCP_NODELAY, buffers | 81 |
| `SOCK-10` | Buffers and backpressure — the kernel's queue, your queue, and who says stop | 82 |
| `SOCK-11` | Timeouts and cancellation — the connection that hangs forever | 82 |
| `SOCK-12` | Connection pooling and keep-alive — what a handshake costs, measured | 83 |

---

## 16 · 🏷️ Curriculum `DNS` — Naming & DNS (DNS-01..12)

The system that turns a name into an address, and the most common single point of failure in
modern infrastructure. Silent Failure #1 lives here: DNS is caches all the way down, and a cache is
an answer that never touched the network you are trying to debug.

| ID | Concept | Closes on |
| --- | --- | --- |
| `DNS-01` | Why names exist — and the hosts file that stopped scaling in the 1980s | 84 |
| `DNS-02` | The namespace — root, TLD, authoritative servers, and delegation as a tree | 84 |
| `DNS-03` | Stub, recursive, iterative — who asks whom, and who caches | 85 |
| `DNS-04` | The DNS message format, built and parsed by hand, including name compression | 85 |
| `DNS-05` | The record types you must know — A, AAAA, CNAME, MX, TXT, NS, SOA, PTR, SRV | 86 |
| `DNS-06` | 💥 Caching and TTLs — the answer that never touched the network | 87 |
| `DNS-07` | 🔍 An iterative resolver, written from the root down, with a cache | 88 |
| `DNS-08` | Negative caching, NXDOMAIN, and the wildcard that answers everything | 88 |
| `DNS-09` | UDP, truncation, TCP fallback and EDNS(0) — how DNS outgrew 512 bytes | 89 |
| `DNS-10` | DNSSEC — the chain of trust, and why deployment is genuinely hard | 89 |
| `DNS-11` | DoT, DoH and DoQ — privacy for the user, blindness for the operator | 90 |
| `DNS-12` | DNS in operations — split horizon, low-TTL failover, and the outage caused by a name | 90 |

---

## 17 · 💬 Curriculum `APP` — Application protocols (APP-01..20)

The protocols people actually speak, starting with the one you can type by hand and ending with the
ones you cannot. HTTP gets the most room because it is the one you will read in a capture for the
rest of your career, and because its two ways of stating a body length produce one of the most
instructive vulnerabilities in the field.

| ID | Concept | Closes on |
| --- | --- | --- |
| `APP-01` | Client-server, peer-to-peer, and what a protocol specification must actually pin down | 91 |
| `APP-02` | URIs and URLs — scheme, authority, path, query, fragment, and percent-encoding | 91 |
| `APP-03` | HTTP/1.1 — the request line, the headers, the body, parsed by hand | 92 |
| `APP-04` | An HTTP/1.1 server written on a raw socket | 92 |
| `APP-05` | Methods, status codes, safety and idempotency | 93 |
| `APP-06` | Content-Length, chunked transfer encoding, and content negotiation | 93 |
| `APP-07` | 💥 Request smuggling — the desync that lives between Content-Length and Transfer-Encoding | 94 |
| `APP-08` | Persistent connections, pipelining, and head-of-line blocking | 95 |
| `APP-09` | HTTP caching — freshness, validators, and the four caches between you and the origin | 95 |
| `APP-10` | Cookies and sessions — state bolted onto a stateless protocol | 96 |
| `APP-11` | The same-origin policy and CORS — the browser's own network model | 96 |
| `APP-12` | HTTP/2 — binary framing, streams, multiplexing and HPACK | 97 |
| `APP-13` | HTTP/3 and QUIC — streams over UDP, 0-RTT, and connection migration | 98 |
| `APP-14` | WebSocket — the upgrade, the frame format, and ping/pong | 99 |
| `APP-15` | Server-sent events and long polling — choosing among three ways to push | 99 |
| `APP-16` | REST, RPC and gRPC — the API shapes that sit on HTTP | 100 |
| `APP-17` | SMTP and store-and-forward — the protocol that assumes the other end is down | 101 |
| `APP-18` | IMAP, MIME, and SPF/DKIM/DMARC — why mail delivery is a reputation system | 101 |
| `APP-19` | 🅿️ FTP and its two connections — the protocol that taught firewalls to inspect payloads | 102 |
| `APP-20` | Real-time media — RTP, RTCP, WebRTC, and the jitter buffer | 102 |

---

## 18 · 🔐 Curriculum `SEC` — Security, TLS & trust (SEC-01..22)

The network was designed to move packets between people who trusted each other, and then it was
connected to everybody. This curriculum starts with the threat model and the ethics rule (§4.2), and
every attack in it runs inside namespaces you created. **You never write cryptography** (Principle
3); you learn to reason about what a reviewed implementation gives you.

| ID | Concept | Closes on |
| --- | --- | --- |
| `SEC-01` | The network threat model — who can read, who can change, who can pretend to be you | 103 |
| `SEC-02` | The lab ethics rule — your traffic, your namespaces, and the law | 103 |
| `SEC-03` | Passive attacks — sniffing a shared medium, a mirror port, and an ARP-spoofed switch | 104 |
| `SEC-04` | Active attacks — spoofing, replay, on-path and off-path injection | 104 |
| `SEC-05` | Cryptographic primitives, used and never written — hash, MAC, AEAD, KDF, signature | 105 |
| `SEC-06` | Symmetric vs asymmetric, and Diffie-Hellman drawn as a picture | 105 |
| `SEC-07` | What TLS promises, and the four things it does not | 106 |
| `SEC-08` | The TLS 1.3 handshake, message by message, read out of your own capture | 106 |
| `SEC-09` | Key exchange, the key schedule, and the transcript hash | 107 |
| `SEC-10` | X.509 certificates — the chain, the name checks, and the fields that matter | 108 |
| `SEC-11` | The public-key infrastructure — roots, intermediates, revocation, OCSP stapling | 108 |
| `SEC-12` | Certificate Transparency, pinning, and what happens after a misissuance | 109 |
| `SEC-13` | 💥 A TLS client that verifies properly — and the one flag that turns it all off | 110 |
| `SEC-14` | Mutual TLS and client certificates | 111 |
| `SEC-15` | SSH — the protocol, host keys, and trust on first use | 111 |
| `SEC-16` | VPNs — IPsec as an idea, and a WireGuard-shaped tunnel built over UDP | 112 |
| `SEC-17` | Firewalls — stateless filters, stateful inspection, and nftables rules read as code | 113 |
| `SEC-18` | NAT is not a firewall — the accidental security everyone relies on | 113 |
| `SEC-19` | DDoS — volumetric, protocol and application-layer; amplification and reflection | 114 |
| `SEC-20` | Scanning and reconnaissance, seen from the defender's side | 114 |
| `SEC-21` | Segmentation and zero trust — the perimeter that stopped existing | 115 |
| `SEC-22` | 💥 The capture that contained a password — handling evidence safely | 115 |

---

## 19 · 📡 Curriculum `WIRE` — Wireless & mobility (WIRE-01..10)

Everything above assumed a cable. Remove the cable and the assumptions break in ways that are
visible from the transport layer: loss that is not congestion, capacity that depends on the worst
client, and a medium anybody nearby can hear.

| ID | Concept | Closes on |
| --- | --- | --- |
| `WIRE-01` | The wireless channel — attenuation, interference, multipath, and why it is not a cable | 116 |
| `WIRE-02` | The 802.11 MAC — CSMA/CA, the hidden terminal, and RTS/CTS | 116 |
| `WIRE-03` | Beacons, scanning, association and roaming | 117 |
| `WIRE-04` | Wi-Fi generations — what MIMO, wider channels and OFDMA actually changed | 117 |
| `WIRE-05` | Wi-Fi security — WPA2, WPA3, the four-way handshake, and the open network | 118 |
| `WIRE-06` | 💥 Why the Wi-Fi is slow — airtime fairness, rate adaptation, and one distant client | 119 |
| `WIRE-07` | 🅿️ Cellular architecture — radio access network, core, and the bearer | 120 |
| `WIRE-08` | Mobility and handover — keeping an address while the radio changes | 120 |
| `WIRE-09` | 🅿️ Bluetooth and BLE — low power, short range, different assumptions | 121 |
| `WIRE-10` | TCP over a wireless link — loss that is not congestion, and what that costs | 121 |

---

## 20 · 🏢 Curriculum `DC` — Datacenter, cloud & overlays (DC-01..18)

Networks built for machines rather than people: predictable, oversubscribed on purpose, and full of
overlays that quietly cost you MTU. This is where the arithmetic you learned in §11 and §14 stops
being an exercise and starts being the design document.

| ID | Concept | Closes on |
| --- | --- | --- |
| `DC-01` | The datacenter problem — east-west traffic, and why the three-tier tree failed | 122 |
| `DC-02` | Leaf-spine and Clos — the topology, and the oversubscription arithmetic | 122 |
| `DC-03` | ECMP and flow hashing — and the elephant flow that ruins a perfect plan | 123 |
| `DC-04` | 💥 Incast — many senders, one receiver, and TCP's worst case | 123 |
| `DC-05` | Overlays — VXLAN, the VTEP, and the tenant that believes it owns a LAN | 124 |
| `DC-06` | Geneve, GRE and IP-in-IP — the encapsulation zoo and the MTU it costs you | 124 |
| `DC-07` | SDN — the control plane pulled out of the box, with OpenFlow as the worked example | 125 |
| `DC-08` | 🅿️ Software forwarding — eBPF/XDP and DPDK | 125 |
| `DC-09` | The load balancer — L4 vs L7, direct server return, and connection affinity | 126 |
| `DC-10` | 💥 Health checks and draining — the balancer that kept sending to a dead backend | 126 |
| `DC-11` | 🅿️ Anycast — one address in many places, and the arithmetic behind a CDN footprint | 127 |
| `DC-12` | CDNs — caching at the edge, and the request that cannot be cached | 127 |
| `DC-13` | Container networking, built by hand — netns, veth, bridge, and one address | 128 |
| `DC-14` | Kubernetes networking — the pod model, CNI, Services, and kube-proxy | 129 |
| `DC-15` | The service mesh and the sidecar — what it buys and what each hop costs | 130 |
| `DC-16` | Cloud primitives — VPCs, subnets, security groups and route tables | 131 |
| `DC-17` | Peering, transit and internet exchanges — who pays whom, and why it shows in traceroute | 131 |
| `DC-18` | The cost and blast radius of a network design, worked as arithmetic | 132 |

---

## 21 · 📊 Curriculum `PERF` — Performance, measurement & capture (PERF-01..14)

The curriculum that makes Principle 8 possible. Everything else in the plan produces claims; this is
where a claim becomes a number you are allowed to say out loud. Silent Failures #4 and #1 are both
checked here, mechanically.

| ID | Concept | Closes on |
| --- | --- | --- |
| `PERF-01` | What to measure — latency, throughput, jitter, loss, availability | 133 |
| `PERF-02` | Latency is a distribution — p50, p95, p99, and the tail that users feel | 133 |
| `PERF-03` | Throughput, goodput and bandwidth — three numbers people use as one | 134 |
| `PERF-04` | The measurement harness — repetitions, seeds, warm-up, and reporting the spread | 134 |
| `PERF-05` | 💥 The benchmark that measured slow start — a result that was an artefact | 135 |
| `PERF-06` | tc netem — building delay, loss, reordering and rate limits on purpose | 136 |
| `PERF-07` | Capturing correctly — the filter, the snaplen, the capture point, and what you miss | 136 |
| `PERF-08` | The pcap and pcapng file formats, parsed by hand | 137 |
| `PERF-09` | Following a stream — reading time, sequence and window out of a capture | 137 |
| `PERF-10` | Diagnosing from a capture — RST, retransmission, zero window, dup ACK, reordering | 138 |
| `PERF-11` | Active and passive measurement — and the free public vantage points | 139 |
| `PERF-12` | Flow telemetry — NetFlow, IPFIX, sFlow, and the sampling error nobody mentions | 139 |
| `PERF-13` | The four signals — traffic, errors, saturation, latency | 140 |
| `PERF-14` | Reporting a network result honestly — topology, seed, spread, and the caveat | 140 |

---

## 22 · 🛠️ Curriculum `OPS` — Operations, troubleshooting & discipline (OPS-01..12)

A network is not a project that finishes; it is something somebody has to run at three in the
morning. This curriculum is the discipline that makes that possible — the ledgers, the address plan,
the method, and the two documents you leave behind for whoever is on call next.

| ID | Concept | Closes on |
| --- | --- | --- |
| `OPS-01` | The repo as the network's memory — ledgers, ADRs and reproducible topologies | 1 |
| `OPS-02` | Address planning — the document that prevents next year's outage | 141 |
| `OPS-03` | Configuration as code — idempotent topology scripts you can run twice | 142 |
| `OPS-04` | The troubleshooting method — bottom-up, top-down, and divide-and-conquer | 143 |
| `OPS-05` | The five questions to ask before touching anything | 143 |
| `OPS-06` | 💥 'It's the network' — proving that it is not, with evidence rather than opinion | 144 |
| `OPS-07` | Monitoring — what deserves an alert, and what only deserves a graph | 145 |
| `OPS-08` | Change windows, rollback, and the config change that locked you out | 145 |
| `OPS-09` | The incident — timeline, communication, and a postmortem worth reading | 146 |
| `OPS-10` | Capacity planning from measured data rather than from vendor sizing | 146 |
| `OPS-11` | An IPv6 rollout, run as a change-management exercise | 147 |
| `OPS-12` | The runbook and the design document — written down, not remembered | 147 |

---

## 23 · 🗓️ The Day Map (day → IDs closed)

### 23.0 Why there are 152 days and not 100

**Nobody chose 152.** The number is what came out of taking 248 concepts and splitting them at idea
boundaries until each day held one coherent unit of subject (Principle 19). It is an *output*, and
it is quoted here only so the tracker has something to count against. It was produced by a script
that refuses to run if any ID is closed twice or never — the derivation is mechanical, not editorial.

This matters because the alternative — picking a round target first — silently corrupts everything
downstream. A plan that commits to "100 days" must then compress TCP into three days and routing
into two, and the compression always lands on the same victim: the explanation. The reason so many
networking courses leave a graduate who can recite the seven layers but cannot read a capture is
that the recitation fits in the slot and the capture does not.

Three consequences you should hold on to:

1. **A day is not a session.** Day 20 might be one evening; Day 61 might be four. Both are the day
   being done properly (Principle 17). `./m done N` is gated on a ticked checklist and green checks,
   never on elapsed time.
2. **Days are not equal in size.** Day 61 closes one ID because the TCP state machine is the single
   hardest thing in the plan and deserves a day with nothing else in it. Day 4 closes three because
   *frame*, *packet* and *segment* are one mental model wearing three words, and separating them
   would teach the vocabulary without the idea.
3. **The count changes when content demands it.** If a day turns out to hold two ideas, it is split
   — by ADR, with `docs/CHANGELOG_PLAN.md` updated, and the total moves. That is the plan working as
   designed, not the plan failing.

### 23.1 The 17 phases


| Phase | Days | Theme | Gate |
| --- | --- | --- | --- |
| **0** | **0** | **Foundry: the lab, the skeleton, the driver** | `./m check` green; `./m lab up two-host` pings; no key and no capture in git |
| 1 | 1–9 | The ground: what a network is | `./m lab up two-host` builds two namespaces that ping, and you can name every header in the capture of that ping |
| 2 | 10–16 | The wire: signals, errors and the numbers under everything | Your CRC-32 matches the FCS of a frame captured in the lab, and you can state the bandwidth-delay product of your own loopback |
| 3 | 17–29 | The frame: the link layer, built | Your learning switch forwards correctly on a four-host topology, your ARP responder answers a real `ping`, and you can explain the broadcast storm you caused |
| 4 | 30–43 | The packet: addressing and the network layer | Your IPv4 stack answers `ping` from an unmodified host, forwards between two namespaces, and reassembles a fragmented datagram |
| 5 | 44–54 | Routing: how a packet finds a path it was never told about | Distance vector and link state both converge on your six-router topology, and your BGP speaker exchanges a prefix with a second speaker and applies a policy |
| 6 | 55–68 | Transport: TCP, built | Your TCP completes a handshake with an unmodified `curl`, transfers a file correctly under 5% loss, and closes without leaving a half-open connection |
| 7 | 69–76 | Congestion: sharing a link nobody owns | Your Reno and CUBIC implementations produce the expected sawtooth under netem, reported over five seeds with the spread, not the best run |
| 8 | 77–83 | The socket API: where your program meets the stack | Your event-loop server holds ten thousand idle connections on one thread, and you can state the memory cost per connection from measurement |
| 9 | 84–90 | Names: DNS, and the answer that never touched the network | Your resolver answers from the root for a name it has never seen, and the second query is served from cache with the TTL counted down correctly |
| 10 | 91–102 | Applications: the protocols people actually speak | Your HTTP/1.1 server serves an unmodified browser correctly, including keep-alive and chunked encoding, and rejects a smuggling attempt |
| 11 | 103–115 | Security: the network assumes nothing and trusts nobody | Your TLS client verifies a real chain, rejects a self-signed certificate and a name mismatch, and your WireGuard-shaped tunnel carries traffic between namespaces |
| 12 | 116–121 | Wireless: the link that is not a cable | You can explain, from a measurement, why adding one distant client slowed every other client on the same access point |
| 13 | 122–132 | Datacenter and cloud: networks built for machines, not people | A leaf-spine topology in namespaces with ECMP, a VXLAN overlay between two tenants, and the oversubscription arithmetic written down |
| 14 | 133–140 | Measurement: numbers you are allowed to quote | Every claim in your report carries a topology, a seed, a repetition count and a spread; the contamination-by-warm-cache check is clean |
| 15 | 141–147 | Operations: the network as something someone has to run | The whole lab rebuilds from committed scripts on a clean machine, and your runbook lets a stranger diagnose an injected fault |
| 16 | 148–151 | Capstone: the whole path, cold | A stranger clones the repo, rebuilds the lab, reproduces every headline number, and diagnoses five injected faults from evidence alone |

**Every phase gate includes the freshness check (§25).**

### 23.2 The map

> The authoritative day→ID assignment. Day documents close **exactly** these IDs — no more, no
> fewer. 💥 = the day's deliberate-failure part is the day's centre of gravity. 🅿️ = the day
> contains parked, awareness-level material. 🔍 = a "build first, compare after" day (Principle 3):
> the hand-rolled version already exists and today you open the tool.


#### Phase 0 — Foundry (Day 0)

| Day | Title | IDs closed |
| --- | --- | --- |
| 0 | Toolchain, skeleton and the `./m` driver — one owner for the environment, a repo that cannot commit a private key or a capture, and a gate that refuses a half-finished day | — |

#### Phase 1 — The ground (Days 1–9)

| Day | Title | IDs closed |
| --- | --- | --- |
| 1 | Bootstrap & the map — the repo as Jala's memory, the six ledgers, `scripts/trace.py`, and the ethics rule that governs every packet you will send | `OPS-01` |
| 2 | What a network is, and why it is built in layers | `FOUND-01`, `FOUND-02` |
| 3 | OSI vs the Internet model, and the envelope inside the envelope | `FOUND-03`, `FOUND-04` |
| 4 | Headers, addresses and the five words — frame, packet, segment, datagram, message | `FOUND-05`, `FOUND-06`, `FOUND-07` |
| 5 | Circuit switching, packet switching, and the end-to-end principle | `FOUND-08`, `FOUND-09` |
| 6 | How a protocol becomes real — the RFC, and how to read one | `FOUND-10`, `FOUND-11` |
| 7 | The five tools that each see something different | `FOUND-12` |
| 8 | Your first capture, read byte by byte | `FOUND-13` |
| 9 | The lab — an internet on one laptop, from `ip netns` up | `FOUND-14` |

#### Phase 2 — The wire (Days 10–16)

| Day | Title | IDs closed |
| --- | --- | --- |
| 10 | Bits, clocks and the Shannon limit | `PHY-01`, `PHY-02` |
| 11 | Line coding and clock recovery — why the wire never carries your bits raw | `PHY-03`, `PHY-04` |
| 12 | Latency decomposed, and the bandwidth-delay product | `PHY-05`, `PHY-06` |
| 13 | Media and multiplexing — copper, fibre, and one idea in four costumes | `PHY-07`, `PHY-08` |
| 14 | Errors on the wire, and the three ways to detect them | `PHY-09`, `PHY-10` |
| 15 | Correcting instead of resending — Hamming distance and FEC | `PHY-11` |
| 16 | 🅿️ The physical layer you can touch — NICs, transceivers and the cable plant | `PHY-12` |

#### Phase 3 — The frame (Days 17–29)

| Day | Title | IDs closed |
| --- | --- | --- |
| 17 | The framing problem, and four ways to solve it | `LINK-01`, `LINK-02` |
| 18 | 🔍 The Ethernet frame, built by hand and checked against a capture | `LINK-03`, `LINK-04`, `LINK-05` |
| 19 | Collisions, hubs, and the two kinds of domain | `LINK-06`, `LINK-07` |
| 20 | 🔍 The learning switch, built | `LINK-08` |
| 21 | 💥 Inside the switch — forwarding modes, buffers, and the duplex mismatch | `LINK-09`, `LINK-22` |
| 22 | VLANs and the 802.1Q tag | `LINK-10`, `LINK-11` |
| 23 | 💥 The loop, the broadcast storm, and Spanning Tree | `LINK-12`, `LINK-13` |
| 24 | Link aggregation, and the hash that picks your cable | `LINK-14` |
| 25 | 💥 ARP, built — and the LAN's complete absence of authentication | `LINK-15`, `LINK-16` |
| 26 | MTU — a link-layer number that causes network-layer pain | `LINK-17` |
| 27 | Point-to-point links and DHCP | `LINK-18`, `LINK-19` |
| 28 | The link layer under a hypervisor — tap, bridge, veth, macvlan | `LINK-20` |
| 29 | IPv6 Neighbor Discovery — ARP's replacement, and SLAAC | `LINK-21` |

#### Phase 4 — The packet (Days 30–43)

| Day | Title | IDs closed |
| --- | --- | --- |
| 30 | Why a second address, and the IPv4 header built by hand | `NET-01`, `NET-02` |
| 31 | The IPv4 address, and the classful era it grew out of | `NET-03`, `NET-04` |
| 32 | Masks, prefix length and subnetting, done in binary | `NET-05`, `NET-06` |
| 33 | CIDR, aggregation, and the addresses that are not yours to use | `NET-07`, `NET-08` |
| 34 | 🔍 Longest prefix match, built — and a real routing table read line by line | `NET-09`, `NET-10` |
| 35 | The first hop, and the field that ends a loop | `NET-11`, `NET-12` |
| 36 | The checksum and fragmentation — two things IPv6 changed its mind about | `NET-13`, `NET-14` |
| 37 | 💥 The PMTU black hole — the handshake succeeds and the transfer hangs | `NET-15` |
| 38 | 🔍 ICMP, and writing `ping` and `traceroute` from scratch | `NET-16`, `NET-17` |
| 39 | NAT, built — and everything it breaks | `NET-18`, `NET-19` |
| 40 | IPv6 — the address, the header, and the list of deletions | `NET-20`, `NET-21` |
| 41 | ICMPv6 is not optional | `NET-22` |
| 42 | 💥 Dual stack, Happy Eyeballs, and the broken v6 path nobody noticed | `NET-23` |
| 43 | 🅿️ Transition mechanisms — NAT64, 464XLAT and tunnels | `NET-24` |

#### Phase 5 — Routing (Days 44–54)

| Day | Title | IDs closed |
| --- | --- | --- |
| 44 | Control plane and data plane, and the static route | `ROUTE-01`, `ROUTE-02` |
| 45 | The forwarding trie, and choosing between two protocols that disagree | `ROUTE-03`, `ROUTE-04` |
| 46 | Distance vector, built | `ROUTE-05` |
| 47 | 💥 Count-to-infinity, reproduced — split horizon, poison reverse, and RIP | `ROUTE-06`, `ROUTE-07` |
| 48 | Link state — flooding a database, then Dijkstra | `ROUTE-08` |
| 49 | OSPF — areas, adjacencies, and what convergence actually costs | `ROUTE-09`, `ROUTE-10` |
| 50 | Interior and exterior — autonomous systems and the shape of the Internet | `ROUTE-11`, `ROUTE-12` |
| 51 | BGP — path vector, and a speaker you write | `ROUTE-13`, `ROUTE-14` |
| 52 | The BGP decision process, and policy as the real routing metric | `ROUTE-15`, `ROUTE-16` |
| 53 | 💥 Route leaks and hijacks — and what RPKI can and cannot fix | `ROUTE-17` |
| 54 | 🅿️ Multicast and IGMP | `ROUTE-18` |

#### Phase 6 — Transport (Days 55–68)

| Day | Title | IDs closed |
| --- | --- | --- |
| 55 | Ports and the five-tuple — how a packet finds one process | `TRANS-01`, `TRANS-02` |
| 56 | UDP, built — and made to lose packets on purpose | `TRANS-03`, `TRANS-04` |
| 57 | When UDP is the right answer | `TRANS-05` |
| 58 | Reliability from first principles — stop-and-wait, and what sequence numbers cost | `TRANS-06`, `TRANS-07` |
| 59 | Sliding windows — go-back-N and selective repeat, both built | `TRANS-08` |
| 60 | The TCP header and the three-way handshake | `TRANS-09`, `TRANS-10` |
| 61 | The TCP state machine — eleven states, implemented | `TRANS-11` |
| 62 | 💥 Teardown, TIME_WAIT, and the port exhaustion it causes | `TRANS-12`, `TRANS-13` |
| 63 | 💥 The byte stream — and the partial read that corrupts your protocol | `TRANS-14`, `TRANS-15` |
| 64 | Framing on top of TCP — the parser you have to write anyway | `TRANS-16` |
| 65 | Retransmission — the RTT estimator, Karn's algorithm, and fast recovery | `TRANS-17`, `TRANS-18` |
| 66 | SACK and flow control — the window that says stop | `TRANS-19`, `TRANS-20` |
| 67 | 💥 Nagle meets delayed ACK — the 40 milliseconds nobody ordered | `TRANS-21`, `TRANS-22` |
| 68 | Keepalives, half-open connections, and what `close` really does | `TRANS-23`, `TRANS-24` |

#### Phase 7 — Congestion (Days 69–76)

| Day | Title | IDs closed |
| --- | --- | --- |
| 69 | Congestion control vs flow control, and the collapse of 1986 | `CONG-01`, `CONG-02` |
| 70 | AIMD, slow start and congestion avoidance | `CONG-03`, `CONG-04` |
| 71 | Tahoe, Reno and NewReno, implemented on your own stack | `CONG-05` |
| 72 | CUBIC, and the delay-based road not taken | `CONG-06`, `CONG-07` |
| 73 | BBR — modelling the bottleneck instead of waiting for loss | `CONG-08` |
| 74 | 💥 Queues, Little's law, and the bufferbloat on your own link | `CONG-09`, `CONG-10` |
| 75 | Active queue management and ECN — dropping early on purpose | `CONG-11`, `CONG-12` |
| 76 | Fairness, and measuring a congestion controller honestly | `CONG-13`, `CONG-14` |

#### Phase 8 — The socket API (Days 77–83)

| Day | Title | IDs closed |
| --- | --- | --- |
| 77 | The socket API syscall by syscall, and the backlog | `SOCK-01`, `SOCK-02` |
| 78 | 💥 Thread per connection, and exactly where it stops | `SOCK-03`, `SOCK-04` |
| 79 | Non-blocking sockets, and the readiness APIs | `SOCK-05`, `SOCK-06` |
| 80 | 🔍 The event loop, built — then compared against `asyncio` | `SOCK-07` |
| 81 | Completion-based I/O, and the socket options that matter | `SOCK-08`, `SOCK-09` |
| 82 | Buffers, backpressure, timeouts and cancellation | `SOCK-10`, `SOCK-11` |
| 83 | Connection pooling — what a handshake costs, measured | `SOCK-12` |

#### Phase 9 — Names (Days 84–90)

| Day | Title | IDs closed |
| --- | --- | --- |
| 84 | Why names exist, and the delegation tree | `DNS-01`, `DNS-02` |
| 85 | Who asks whom, and the DNS message parsed by hand | `DNS-03`, `DNS-04` |
| 86 | The record types, and what each one is actually for | `DNS-05` |
| 87 | 💥 Caching and TTLs — the answer that never touched the network | `DNS-06` |
| 88 | 🔍 An iterative resolver, written from the root down | `DNS-07`, `DNS-08` |
| 89 | Truncation, EDNS(0), and the chain of trust | `DNS-09`, `DNS-10` |
| 90 | Encrypted DNS, and the outage caused by a name | `DNS-11`, `DNS-12` |

#### Phase 10 — Applications (Days 91–102)

| Day | Title | IDs closed |
| --- | --- | --- |
| 91 | Client, server, and what a specification has to pin down | `APP-01`, `APP-02` |
| 92 | 🔍 HTTP/1.1, parsed by hand and served from a raw socket | `APP-03`, `APP-04` |
| 93 | Methods, status codes, and the two ways to say how long a body is | `APP-05`, `APP-06` |
| 94 | 💥 Request smuggling — the desync between two length fields | `APP-07` |
| 95 | Keep-alive, head-of-line blocking, and the four caches in the path | `APP-08`, `APP-09` |
| 96 | Cookies, sessions, and the browser's own network model | `APP-10`, `APP-11` |
| 97 | HTTP/2 — binary framing, multiplexing and HPACK | `APP-12` |
| 98 | HTTP/3 and QUIC — streams over UDP | `APP-13` |
| 99 | WebSocket, server-sent events, and long polling | `APP-14`, `APP-15` |
| 100 | REST, RPC and gRPC | `APP-16` |
| 101 | Mail — SMTP, and why delivery is a reputation system | `APP-17`, `APP-18` |
| 102 | FTP's two connections, and real-time media | `APP-19`, `APP-20` |

#### Phase 11 — Security (Days 103–115)

| Day | Title | IDs closed |
| --- | --- | --- |
| 103 | The threat model, and the ethics rule that governs everything after it | `SEC-01`, `SEC-02` |
| 104 | 💥 Passive and active attacks, reproduced in your own lab | `SEC-03`, `SEC-04` |
| 105 | The primitives you use and never write | `SEC-05`, `SEC-06` |
| 106 | What TLS promises, and the 1.3 handshake read from your own capture | `SEC-07`, `SEC-08` |
| 107 | Key exchange, the key schedule and the transcript hash | `SEC-09` |
| 108 | Certificates and the PKI — chains, names and revocation | `SEC-10`, `SEC-11` |
| 109 | Certificate Transparency, pinning, and life after a misissuance | `SEC-12` |
| 110 | 💥 A TLS client that verifies — and the flag that turns it all off | `SEC-13` |
| 111 | Mutual TLS, and SSH's trust on first use | `SEC-14`, `SEC-15` |
| 112 | A tunnel of your own — IPsec as an idea, WireGuard as a build | `SEC-16` |
| 113 | Firewalls, and the reason NAT is not one | `SEC-17`, `SEC-18` |
| 114 | DDoS and reconnaissance, seen from the defender's side | `SEC-19`, `SEC-20` |
| 115 | 💥 Segmentation, zero trust, and the capture that contained a password | `SEC-21`, `SEC-22` |

#### Phase 12 — Wireless (Days 116–121)

| Day | Title | IDs closed |
| --- | --- | --- |
| 116 | The channel, and the MAC that has to share it | `WIRE-01`, `WIRE-02` |
| 117 | Beacons, association, roaming, and what each generation actually changed | `WIRE-03`, `WIRE-04` |
| 118 | Wi-Fi security and the four-way handshake | `WIRE-05` |
| 119 | 💥 Why the Wi-Fi is slow — airtime, and the one distant client | `WIRE-06` |
| 120 | 🅿️ Cellular architecture and mobility | `WIRE-07`, `WIRE-08` |
| 121 | 🅿️ Short-range radios, and TCP over a lossy link | `WIRE-09`, `WIRE-10` |

#### Phase 13 — Datacenter and cloud (Days 122–132)

| Day | Title | IDs closed |
| --- | --- | --- |
| 122 | East-west traffic, leaf-spine, and the oversubscription arithmetic | `DC-01`, `DC-02` |
| 123 | 💥 ECMP, elephant flows and incast | `DC-03`, `DC-04` |
| 124 | Overlays — VXLAN, and the MTU that encapsulation costs you | `DC-05`, `DC-06` |
| 125 | SDN, and forwarding in software | `DC-07`, `DC-08` |
| 126 | 💥 The load balancer, and the health check that lied | `DC-09`, `DC-10` |
| 127 | Anycast and the CDN | `DC-11`, `DC-12` |
| 128 | 🔍 Container networking, built by hand | `DC-13` |
| 129 | Kubernetes networking — the pod model and what CNI actually does | `DC-14` |
| 130 | The service mesh, and what each extra hop costs | `DC-15` |
| 131 | Cloud primitives, peering and transit | `DC-16`, `DC-17` |
| 132 | The cost and blast radius of a design, as arithmetic | `DC-18` |

#### Phase 14 — Measurement (Days 133–140)

| Day | Title | IDs closed |
| --- | --- | --- |
| 133 | What to measure, and why latency is a distribution | `PERF-01`, `PERF-02` |
| 134 | Throughput, goodput, and a harness that reports the spread | `PERF-03`, `PERF-04` |
| 135 | 💥 The benchmark that measured slow start | `PERF-05` |
| 136 | netem, and capturing without lying to yourself | `PERF-06`, `PERF-07` |
| 137 | 🔍 The pcap format parsed by hand, and following a stream | `PERF-08`, `PERF-09` |
| 138 | Diagnosis from a capture alone | `PERF-10` |
| 139 | Active, passive and sampled measurement | `PERF-11`, `PERF-12` |
| 140 | The four signals, and reporting a result honestly | `PERF-13`, `PERF-14` |

#### Phase 15 — Operations (Days 141–147)

| Day | Title | IDs closed |
| --- | --- | --- |
| 141 | The address plan — the document that prevents next year's outage | `OPS-02` |
| 142 | Configuration as code — a topology you can run twice | `OPS-03` |
| 143 | The troubleshooting method, and the five questions | `OPS-04`, `OPS-05` |
| 144 | 💥 'It's the network' — proving it is not | `OPS-06` |
| 145 | Monitoring, change windows, and the config that locked you out | `OPS-07`, `OPS-08` |
| 146 | The incident, the postmortem, and capacity planning | `OPS-09`, `OPS-10` |
| 147 | An IPv6 rollout, and the documents you leave behind | `OPS-11`, `OPS-12` |

#### Phase 16 — Capstone (Days 148–151)

| Day | Title | IDs closed |
| --- | --- | --- |
| 148 | The cold rebuild — destroy the lab and bring the whole internet back from committed scripts | — |
| 149 | One request, every layer — a browser to your own server, annotated from a single capture | — |
| 150 | 💥 The fault injection audit — five deliberate breakages, diagnosed from evidence alone | — |
| 151 | The design document — a network for a stated requirement, with the arithmetic, the threat model and the runbook | — |

> **Day 0 and the capstone close no IDs, and both do so by design.** Day 0 is the machine, the
> skeleton and the driver, which are preconditions for the curriculum rather than part of it. Days
> 148–151 exercise everything and introduce nothing. That is what keeps `TRACEABILITY.md` valid — no
> ID is assigned to a day that teaches no new concept, so an open ID is always a real gap rather
> than a bookkeeping artefact.
>
> **The Day 0 / Day 1 boundary, stated so it cannot drift.** Day 0 builds a repo that could belong
> to *any* Python project, plus the one thing that makes it a networking repo: a working Linux with
> namespaces, and a `.gitignore` that blocks **captures and keys**. Day 1 makes that repo **Jāla's**:
> the seven ledgers, `trace.py`/`tracker.py`, the address plan the whole lab will use, and the
> ethics rule (§4.2) written into `CLAUDE.md` before a single packet is sent. `.gitignore` is touched
> on both days for two genuinely different reasons, and each day says which.

---

## 24 · 📐 The Depth Contract — how a day is written

> **Why this section exists.** The default failure mode of a technical curriculum is a long page per
> topic. It looks thorough. It is not: a reader cannot revisit *one* idea without re-reading four,
> there is no artifact that distinguishes a thinly-covered subtopic from a missing one, and a time
> estimate at the top silently authorises the worst edit in technical writing — cutting the
> explanation because the document is getting long.
>
> A day here is **one hub plus one document per subtopic**, every document written from zero prior
> knowledge through to how the idea behaves in a real network. This section states exactly what
> "covered properly" means, so it can be reviewed by reading and partly checked by a script. It is
> Principles 16, 17, 18 and 20 made concrete.

### 24.1 The four commitments

**One idea per document.** A subtopic that cannot be read alone, understood without scrolling past a
different subtopic, and explained back out loud is not one subtopic — it is several, badly stacked.
If a document needs the word "also" to introduce its second half, it is two documents.

**No clocks.** Nothing in a day folder carries a time estimate, an "estimated hours" field, a "this
should take 90 minutes", or a suggested pace. **Content is never trimmed to fit a schedule**, and a
day is never declared finished because a duration elapsed.

> **What "no clocks" does *not* ban — and this matters more here than anywhere.** Networking is made
> of durations. A measured RTT, a retransmission timeout in milliseconds, a `TIME_WAIT` of twice the
> maximum segment lifetime, a p99, a hold timer, a netem setting of `delay 40ms 5ms` — every one of
> those is *data* and must be written, with its source. The ban is on estimates aimed at the reader's schedule: anything that
> tells them how fast they ought to be going, and thereby licenses trimming the explanation.
> `./m depth` distinguishes the two, and a false positive on a measured duration is a bug in the
> checker, not a reason to delete the number.

**Zero to production, in one document.** Each part starts where a reader who has never heard of the
idea can stand, and ends where a working professional stands: how the idea appears in a real
network, what an operator does differently from the tutorial version, what fails at scale, and what
a reviewer or an interviewer will probe.

**Every number has a provenance.** Any empirical claim in any part is either *measured here* — with
topology, netem settings, seed, repetitions, hardware and date — or *specified* with an RFC number
and section, or *cited* to a named paper. Never recalled (Principle 8).

### 24.2 The folder shape

```
days/day-NNN-<day-slug>/
├── LESSON.md          # the hub — orientation, story, part map, build brief, check, ledger
├── CHECKLIST.md       # the definition of done; ./m done NNN refuses to commit until ticked
├── parts/             # THE TEACHING — one document per subtopic
│   ├── 01-<slug>/     # section 1 — two digits, zero-padded, then what the section is about
│   │   ├── 1.1-<slug>.md
│   │   └── 1.2-<slug>.md
│   ├── 02-<slug>/
│   │   └── 2.1-<slug>.md
│   └── 03-<slug>/
│       └── 3.1-<slug>.md
└── lab/               # created by ./m scaffold NNN; the learner's own scratch code
```

`parts/` is mandatory. **A day with no `parts/` directory is, by definition, not written** — the
tracker reports it as pending and the phase gate cannot go green.

**Day numbers are three digits, zero-padded** — `day-037-pmtu-black-hole`, `day-151-design-document`.
The plan runs past 99, and `day-9` sorting after `day-100` in every file listing is a papercut paid
152 times.

**Every folder name carries its subject.** A number alone is an address, not an answer:

| Folder | Shape | Slug from | Length |
| --- | --- | --- | --- |
| the day | `day-NNN-<slug>` | the hub's `title` frontmatter, minus articles | 1–4 words |
| a section | `NN-<slug>` | the section's heading in the hub's §2 map | 1–3 words |

**The number is the identity; the slug is a label on it.** Every tool resolves a day by number and
accepts whatever slug follows, so a folder can be renamed to a better slug at any time without
breaking `./m`, `depth_check.py`, `tracker.py` or `trace.py`.

**Every part lives inside its section's folder**, and the folder number must agree with the number
before the dot: `parts/02-arp/2.3-<slug>.md` is correct; `parts/02-arp/3.1-<slug>.md` is a bug the
depth check rejects. **Links between parts are relative**: a sibling is `1.2-<slug>.md`; another
section is `../01-<slug>/1.5-<slug>.md`; the hub is `../../LESSON.md`.

### 24.3 The numbering rule — what `1.1` and `2.3` mean

Part numbers are **`<section>.<subtopic>`**, both scoped to the day.

- The **section** groups subtopics that share one mental model — usually one curriculum ID, one
  layer, one stage of a packet's journey, or one phase of a protocol exchange.
- The **subtopic** is the reading order inside that section. It starts at `1`, never `0`, and has no
  gaps.

The hub's §2 map declares what each section *is*. A typical two-ID day:

| Section | Means | Example subtopics |
| --- | --- | --- |
| **1.x** | the day's first ID | `1.1` what it is · `1.2` the wire format · `1.3` how it behaves |
| **2.x** | the day's second ID | `2.1` … `2.2` … |
| **3.x** | the synthesis — the two IDs meeting | `3.1` the failure visible only when both are true |

A protocol day uses sections as *stages of the exchange*: `1.x` the header, `2.x` the state machine,
`3.x` the timers, `4.x` the failure surface. A routing day uses them as *convergence phases*. A
measurement day uses them as *the harness, the run, the reading*. **The grouping must be stated in
the hub;** an unexplained numbering is a bug.

### 24.4 What a part document must contain

Every file in `parts/` carries all twelve of these, **in this order**. Three of them — *Wire format*,
*Topology* and *Line by line* — are conditional; the other nine are unconditional.

| # | Section | The rule |
| --- | --- | --- |
| 1 | **frontmatter** | `day`, `part`, `title`, `ids`, `level`, `tier`, `prerequisites`, `prev`, `next`. Machine-read. **No duration field of any kind** (Principle 17). |
| 2 | **One-line answer** | The subtopic's claim in a single sentence, before anything else. A reader who reads only this line has learned something true. |
| 3 | **The story** | A concrete scene before any abstraction: a person, a machine, a failure, a decision. It comes **first**, in plain words, with **no jargon at all**. It must pass all four of §27.1's story tests — **everyday · plain · concrete · honest**. |
| 4 | **The idea in plain language** | The concept itself, assuming the reader has never met it. Every term defined the first time it appears — **including terms from earlier days**, with a link to the part that introduced them. No code. |
| 5 | **Why Jāla needs it** | The concrete later day that breaks without this. *"You meet this again on Day 124, where a VXLAN header takes bytes off the MTU and the transfer hangs exactly the way it hung today"* is the shape. Never "this is important". |
| 6 | **The mechanism** | How it actually works: the runnable code, the exchange written out, or the diagram. Nothing skipped as "obvious". Mermaid whenever the concept is spatial, sequential, or a state machine — which, in this field, is most of them. |
| 7 | **Wire format** ⟵ *conditional* | **Required whenever the part introduces, builds or parses a header, a frame, a message or a record.** A table with one row per field: byte offset, bit width, field name, the value in *this* example (hex and decoded), and what it means. Plus the byte order, stated explicitly. More protocol bugs are offset and endianness bugs than logic bugs, and a wrong offset produces a packet that is *silently discarded*, not an exception (Principle 20). A part with no wire format omits this section and `./m depth` does not ask for it. |
| 8 | **Topology** ⟵ *conditional* | **Required whenever the part runs something in the lab (tier L1 or L2).** The namespaces, the links, the addresses, the netem settings, and the exact `lab/<name>.sh` that builds it. A Mermaid diagram plus the address table. **A measurement without a topology is an anecdote** (Principle 9), and a reader who cannot rebuild your topology cannot reproduce your result. |
| 9 | **Line by line** ⟵ *conditional* | Every non-obvious token of every code block, explained — and *why it is that line and not another*. Written as a `**Line by line:**` list **immediately after each code block**. Blocks showing error output, a bare check command, a capture excerpt or a diagram are exempt. **An unexplained line is a bug in the doc.** |
| 10 | **When it breaks** | The **real** error text, reproduced verbatim — the `Destination Host Unreachable`, the `Connection reset by peer`, the `EAGAIN`, the `certificate verify failed`, the packet that simply never arrives. What it says, what it actually means, and the smallest fix. For this field it also covers the *silent* breakages (§6): what the wrong-but-running version looks like, and the check that catches it. |
| 11 | **In production** | Where this idea shows up in a real network and what changes there: what an operator runs instead of the teaching version, what degrades at scale, the failure that only appears with real traffic, the review comment, and the question an interviewer asks to find out whether you have actually debugged one. **Not optional. This is the section that makes the document professional rather than introductory.** |
| 12 | **Check yourself** | One command the reader can run right now — **which prints a number, not just a pass** — plus one question they must answer **out loud** without scrolling up. |

Four further rules that have no section of their own:

- **The one-idea test.** If a part needs "also" to introduce its second half, split it.
- **The standalone test.** A part must be readable cold. If it depends on an earlier idea, **name
  that part and link it** — never assume the reader remembers Day 26 on Day 124.
- **The no-shortcut test.** "For now, just accept that" is banned unless it links forward to the part
  that explains it. **A deferred explanation must have an address.**
- **The provenance test.** Every number in the part is measured-here, specified in a named RFC
  section, or cited. No exceptions.

#### 24.4.1 Jāla's six additional part rules

These come from Principles 3, 6, 7, 8, 12 and 13, and apply on top of the twelve sections:

1. **Never invent a wire-format detail.** Any part that shows a header names the RFC or IEEE
   standard **and the section**, resolved live that day, next to the table: *"Fields and offsets per
   RFC 9293 §3.1, read 2026-08-27."* The row lands in `docs/SPECS.md` the same day, including
   whether the document is obsoleted.
2. **Never invent a default.** A timer, a buffer size, a backlog cap or a queue length is **read off
   the running system** — `sysctl`, `ss -i`, `ip route show`, `tc -s qdisc` — and the part says which
   system and which kernel version. A default is a fact about a build, not about a protocol.
3. **Never invent a number.** Measured-here (topology, netem settings, seed, repetitions, hardware,
   date) or specified (RFC + section) or cited (paper, venue, year).
4. **Name the silent failure.** Any part touching one of the five (§6) says which one it is avoiding
   and how the reader would detect it.
5. **State the tier and the blast radius.** Any part that sends a packet states its tier — L0, L1,
   L2 or 🅿️ L3 — and, if it generates traffic, **names the namespaces it stays inside** (§4.2). A
   part that teaches an attack and does not name its containment is not finished.
6. **Reproduce before you repair.** Any part that fixes a failure must first *cause* it, in the lab,
   with the command that causes it printed (Principle 12).

### 24.5 What the hub (`LESSON.md`) must contain

The hub is **orientation and assembly, never the teaching itself**. It carries no `Line by line:`
walkthrough, no `Wire format` table and no `Topology` diagram — those live in the parts. Required, in
this order:

1. **frontmatter** — `day`, `phase`, `phase_name`, `title`, `ids`, `principles`, `kind`,
   `plan_version`, `parts` (the count), `tier`, `topology`, `generated`, `status`, `lab_scaffolded`,
   `commit`.
2. **yesterday / today / tomorrow** — one line each, as a blockquote. No time estimate.
3. **`## §1 Where we are`** — the day's whole idea as a scene and an analogy, in plain language,
   before any code and before any jargon.
4. **`## §2 The map`** — a table of every part: number, linked title, what it answers, its `level`
   and its `tier`. Grouped by section, with **one line saying what each section means for this day**.
   **No minutes column, ever.**
5. **`## §3 Setup — run this`** — every `mkdir`, `touch`, `uv add <pkg>==<exact>`, `sudo apt install`
   and `lab/<name>.sh` the day needs, pinned, with the version verified that day.
6. **`## §4 Build brief`** — the files to create, with `TODO(me)` markers left **unsolved**.
7. **`## §5 The check that must be able to fail`** — the check that is RED before the TODOs are done
   (Principle 11). For a networking day this is usually a packet that does not arrive, and the hub
   says what "does not arrive" looks like on the wire.
8. **`## §6 Lab budget`** — the tier (L0/L1/L2/L3), the topology name, the namespace and link count,
   and the netem settings. `L0` is an answer; state it.
9. **`## §7 Traps`** — the mistakes that eat an evening, including the named Silent Failure (§6) if
   the day touches one.
10. **`## §8 Verify before you code`** — the live URLs actually fetched on the day of writing: the
    RFC info pages (and whether each is obsoleted), the tool man pages, the library doc pages
    (Principles 6, 7, 8).
11. **`## §9 Say it in an interview`** — one paragraph, spoken voice, honest, tied to what was built
    and to a number you measured.
12. **`## §10 Done when`** — pointer to `CHECKLIST.md`. Defined by understanding and green checks,
    **never by elapsed time**.
13. **`## §11 Ledger & commit`** — the verbatim snippets that end every day: the `PROGRESS.md` row,
    any `PACKAGES.md` / `SPECS.md` / `TOPOLOGIES.md` / `CAPTURES.md` / `MEASUREMENTS.md` rows, and
    the commit message `day NNN: <title> — closes <IDs>`. **The hub ends with these.**

### 24.6 The `level` field — how a day climbs

| `level` | The reader at the end of this part |
| --- | --- |
| `foundation` | Knows what the thing *is* and could define it to someone else without using the word itself. |
| `working` | Can implement or use it correctly on their own problem, and recognises its failure signature in a capture. |
| `production` | Knows what changes in a real network — scale, buffering, middleboxes, operations — and can defend the choice with arithmetic. |

A day that is all `foundation` is a tutorial. A day that opens at `production` has skipped the
reader. Most days run `foundation → working → production`.

### 24.7 Symbols and conventions used curriculum-wide

Any part introducing a new symbol defines it. These are used consistently and never redefined:

| Symbol | Means | Unit |
| --- | --- | --- |
| `MTU` | maximum transmission unit — largest payload a link will carry | bytes |
| `MSS` | maximum segment size — largest TCP payload, `MTU` minus headers | bytes |
| `RTT` | round-trip time, measured | milliseconds |
| `RTO` | retransmission timeout, computed from `RTT` | milliseconds |
| `BDP` | bandwidth-delay product, `bandwidth × RTT` | bytes |
| `cwnd` | congestion window — what the sender believes the network will take | bytes or segments, stated |
| `rwnd` | receive window — what the receiver has room for | bytes |
| `ssthresh` | slow-start threshold | same unit as `cwnd` |
| `TTL` | time to live (IPv4) / hop limit (IPv6) | hops |

**Byte offsets are decimal and zero-based.** Every wire-format table states its byte order
explicitly; "network byte order" is written out as **big-endian** on first use in every part, because
the phrase is exactly the kind of jargon that hides a bug.

### 24.8 How finely to split

Split by **idea boundaries, never by length or by pace**. A part is finished when its one idea is
fully explained — *including its production face* — and not before.

| Day kind | Split by |
| --- | --- |
| `setup` | one tool, one file, or one command per part |
| `concept` | one claim per part, each with its evidence |
| `format` | one header per part: the fields → the encoding → the edge case → the malformed one |
| `build` (1 ID) | mechanism → wire format → behaviour → edge case → failure mode → production use |
| `build` (2–3 IDs) | one section per ID, plus a synthesis section where they meet |
| `protocol` | one phase of the exchange per part: open → transfer → close → timers → failure |
| `compare` 🔍 | one dimension of difference per part (correctness, speed, what it handles that yours does not, what it hides) |
| `measure` | one stage per part: topology → harness → run → read → what the number does not say |
| `diagnose` | one symptom per part, each ending in the evidence that identifies it |
| `capstone` | one component per part, in build order |

There is deliberately **no target part count and no target length**. If a subject needs five parts it
gets five; if it needs twenty-four it gets twenty-four. The only wrong answers are a part that
carries two ideas and a part that stops before production.

**Every day carries at least one part whose subject is a deliberate failure** — and in this
curriculum that part *injects* the failure rather than describing it (Principle 12). Breaking the
thing on purpose, at `production` level, is the whole point of that document.

### 24.9 What "in depth" is not

The failure modes this contract exists to prevent, stated so they can be caught in review:

- **Splitting without deepening.** Cutting one long page into six shorter ones changes nothing. Each
  part must **gain** the story, the wire format, the topology, the failure text, the production face
  and the check it never had.
- **Summary in place of explanation.** *"The checksum is then verified"* is a caption. *"The receiver
  sums the same sixteen-bit words including the checksum field itself, and a correct packet gives
  `0xffff`, because adding a number to its own one's-complement is always all ones — which is why the
  sender can compute the field with the same routine that verifies it"* is an explanation.
- **Stopping at loopback.** A part that shows a socket working on `127.0.0.1` and never says what
  changes over a link with 40 ms of delay and 1% loss has taught half the subject. **Loopback has no
  MTU problem, no reordering, no middlebox and effectively no latency** — it is a debugger, not a
  network.
- **Assuming the previous day.** Each part names its prerequisite and links it. 152 days is long
  enough that Day 26 is genuinely forgotten by Day 124.
- **Mechanism without failure.** Every mechanism has a matching *When it breaks* with the **actual**
  error string — and, for this field, the *silent* failure too, shown as the wrong output.
- **Numbers without provenance.** "TCP's default initial window is usually 10 segments" is a rumour.
  "`ss -i` reports `cwnd:<n>` on the first ACK of this connection, on kernel `<version>`, checked
  `<date>`" is a fact about a system you can name — and the `<n>` is filled in by running it, not by
  remembering it.
- **Wire formats left to the reader.** If a part shows a header and does not give offsets, it has
  created a bug it will not be around to fix.
- **A topology described in prose.** "Two hosts connected through a router" is not a topology. A
  committed script that builds it is.
- **Trimming to fit.** Cutting an explanation because the day "is getting long" is the one edit this
  format forbids outright. **Split it into another part instead.**
- **Solved reps.** `TODO(me)` stays `TODO(me)`.

### 24.10 Enforcement

`scripts/depth_check.py`, run as `./m depth [NNN]`, is the machine-readable half of this contract.
It fails on:

- a missing `parts/` directory;
- a day folder that is not `day-NNN-<slug>` with a three-digit number and a slug;
- a part loose in `parts/` instead of inside a section folder;
- a section folder that is not two zero-padded digits plus a slug;
- a part whose section folder disagrees with the number in its filename;
- a filename that does not match `<section>.<subtopic>-<slug>.md`;
- a gap in the section or subtopic numbering;
- any of the nine unconditional part sections missing or out of contract order;
- a code block with no `Line by line:` walkthrough following it;
- a part that shows a header, a field name and an offset but carries no `## Wire format` section;
- a part declaring tier `L1` or `L2` that carries no `## Topology` section;
- a part that generates traffic without naming its namespaces (§4.2);
- a `level` outside `foundation` · `working` · `production`, or a `tier` outside `L0` · `L1` · `L2` ·
  `L3`;
- **any reader-directed time estimate anywhere in a day folder** (Principle 17) — an "estimated
  hours" field, a `duration:` key, a "should take about 40 minutes", a "quick detour", a suggested
  pace. **A measured duration in a result, a timer value, or a netem setting is data and passes**;
- a hub that carries teaching, or whose §2 map does not link every part on disk;
- a `parts:` frontmatter count that disagrees with the directory;
- a missing `CHECKLIST.md`.

What it **cannot** check is whether an explanation is any good. That is what §24.9 is for, and it is
reviewed by reading. `docs/TRACKER.md` reports the part count of every written day, so a thin day is
visible from the progress table alone.

`scripts/trace.py` is the ID-level check: it reads each `days/day-NNN-<slug>/LESSON.md` against §23
and regenerates `docs/TRACEABILITY.md`. **An open ID in a completed phase is a bug.**

---

## 25 · 🚦 Phase Gates & the Freshness Check

A phase is **green** only when:

1. Every day in the phase has its row in `docs/PROGRESS.md` with gates green.
2. `scripts/trace.py` shows **no open IDs** from this or any earlier phase.
3. `./m check` passes on the whole repo — lint, format, tests, **and the §24 depth contract for
   every written day**.
4. Every day in the phase has a `parts/` directory. A day with no `parts/` is not written (§24.2), so
   a phase containing one cannot be green.
5. **Every topology used in the phase rebuilds from its committed script on a torn-down lab.**
   `./m lab down && ./m lab up <name>` twice, with the second run producing no error — an idempotent
   script is the only kind that is worth committing (`OPS-03`).
6. Every measurement performed in the phase has a row in `docs/MEASUREMENTS.md` carrying the
   topology, the netem settings, the seed, the repetition count and a hardware line (Principle 9).
   **A measurement without a row did not happen**, and a measurement of one repetition is Silent
   Failure #4 with a table around it.
7. Every specification read in the phase has a row in `docs/SPECS.md` with its status, and **none of
   them is marked obsoleted** by a document the plan does not know about.
8. **No capture and no key is in git.** `git log --all --name-only | grep -E '\.(pcap|pcapng|pem|key)$'`
   returns nothing. This is checked every phase, not once, because the day it fails is the day it
   became permanent.
9. The **freshness check** passes:
   - Pinned specifications — has an RFC been obsoleted? Has an errata been filed against one you
     quoted? Obsoleted spec → amend first.
   - Pinned libraries and system tools — has a breaking release landed? Has a flag been removed?
   - Kernel defaults the phase relied on — re-read them; a distribution upgrade silently changes
     experiments (§5.1).
   - Any public resource the phase uses — a looking glass, a route collector, a measurement platform
     — still free, still reachable, still permitting what §4.2 allows.
10. Any deviation is recorded: an ADR for structural changes, `docs/CHANGELOG_PLAN.md` for plan text.

**Never** skip a day, merge two days, or reorder days without an ADR.

> A gate is never passed because time ran out (Principle 17). `./m done N` is gated on a ticked
> `CHECKLIST.md` and green checks, and on nothing else.

---

## 26 · 📒 Ledgers & Traceability

All ledgers live in `docs/`.

| File | Nature | Rule |
| --- | --- | --- |
| `docs/PROGRESS.md` | Append-only | One row per completed day; **the last row is where we are.** |
| `docs/PACKAGES.md` | Append-only | Every install: package or system tool, version, date, day, why. No invented versions (Principle 6). |
| `docs/SPECS.md` | Append-only | Every specification **before** it is quoted: number, title, status, obsoletes / obsoleted-by, sections read, date resolved, day. |
| `docs/TOPOLOGIES.md` | Append-only | Every lab topology: name, script path, namespace count, link count, address plan, netem settings, day introduced. A topology named in a measurement must have a row. |
| `docs/CAPTURES.md` | Append-only | Every capture: filename, topology, capture point, filter, snaplen, tool and version, date, day, and **whether it has been checked for credentials** (`SEC-22`). The capture itself is gitignored; its provenance is not. |
| `docs/MEASUREMENTS.md` | Append-only | Every measurement: id, day, topology, netem settings, seed, repetitions, tool and version, hardware, the result **with its spread**, and the outcome (**including "no significant difference"** — Principle 10). |
| `docs/CHANGELOG_PLAN.md` | Append-only | Every amendment to this plan (Principle 14). |
| `docs/TRACEABILITY.md` | Regenerated | `scripts/trace.py` scans every day hub against §23; an open ID in a completed phase is a bug. |
| `docs/TRACKER.md` | Regenerated | `scripts/tracker.py` reports what is written, **how many parts each day has**, and what is pending. |
| `docs/CURRICULUM_INDEX.md` | Regenerated | The ID → day cross-table read out of §23. Answers *"where do I learn `TRANS-17`?"* |

**Seven ledgers are written by hand and three are regenerated — do not confuse them.**
`TRACEABILITY.md`, `TRACKER.md` and `CURRICULUM_INDEX.md` are outputs; editing them by hand only
means the next `./m check` silently overwrites you. The other seven are append-only history, written
by the day you are finishing — every day document ends with the exact rows to paste (§24.5).

> **`MEASUREMENTS.md` and `TOPOLOGIES.md` are the two ledgers this curriculum has that an ordinary
> project does not**, and they exist for the same reason. Six weeks after a run, the only difference
> between a result and an anecdote is a row saying which topology it ran on, what delay and loss were
> configured, which seed, how many repetitions, and what the spread was. **A throughput number
> without a topology is not a weak result. It is not a result.**

ADRs are `docs/adr/ADR-NNNN-*.md`.

---

## 27 · ✍️ The Style Guide

§24 says what a day must *contain*. This section says how it must *read*.

### 27.1 The register

1. **Storytelling is the default, not a flourish.** A scene before an abstraction, every time. The
   story section of a part carries **no jargon at all** — a person, a machine, an afternoon lost. A
   reader remembers the office where every video call froze at exactly the same point in the day long
   after they have forgotten the phrase "buffer occupancy".
2. **Simple language first.** Plain words → concrete example → *only then* the terminology. If a
   twelve-year-old could not follow the first sentence, rewrite the first sentence. This is not
   dumbing down; it is putting the definition after the thing it defines.
3. **Define every term on first use — including your own terms from earlier days.** 152 days is long
   enough that Day 26 is genuinely forgotten by Day 124. Link the part that introduced it. "As we saw
   earlier" is not a link.
4. **Second person, present tense, active voice.** "You take the first 20 bytes, and the version and
   header-length nibbles come out of the first one." Not "the header is then parsed".
5. **No person names, no course or creator brand names.** This curriculum is self-contained and
   promotes nobody: never name an instructor, author, channel, academy, bootcamp or training company
   — in a lesson, a checklist, a docstring or a commit message. Naming the **tools and standards** you
   actually use is required and unaffected (`tcpdump`, Wireshark, `scapy`, iproute2, nftables), as is
   **citing an RFC by number and section** or a paper by title and venue — a citation is provenance
   (Principle 8), not a brand. **An algorithm named after its author is its name** (Nagle's algorithm,
   Karn's algorithm, Dijkstra, Bellman–Ford) and is written normally.
6. **The story must be a scene the reader has actually lived.** Four tests, and a story that fails
   any of them is rewritten, not defended:
   - **Everyday.** A kitchen, a shop, a bus, a phone, a queue, a bill, a lift, a shared kitchen tap.
     *Not* a trade the reader has never practised. A metaphor the reader has to learn before it can
     teach is a second lesson, not a hook.
   - **Plain.** No word a twelve-year-old would have to look up, and no sentence they would have to
     read twice. Short sentences. Common words. The terminology belongs in section 4, not here.
   - **Concrete.** Real objects and real numbers — *fourteen people in the queue*, *a 90-second wait*,
     *three lifts and one of them locked* — never "some traffic" or "a quantity".
   - **Honest.** A thing that genuinely happens, with the failure it genuinely causes. A setup built
     backwards from the lesson reads as contrived, and a reader who notices the contrivance stops
     trusting the section that follows it.
7. **Grammar and punctuation are part of the contract.** Full stops, commas, apostrophes and hyphens,
   correct and consistent, in every section — prose, tables, code comments, checklist boxes and commit
   messages alike. Use the em dash for an aside, the comma for a pause, the semicolon rarely and the
   exclamation mark never.

### 27.2 The scene format

For failures and motivations, use the four-beat scene:

> 🎬 **The scene:** what you are doing.
> 😬 **The naive fix:** what everyone tries.
> 💥 **Why it fails:** the mechanism — not the symptom.
> 💡 **The insight:** the principle that survives after the details are forgotten.

### 27.3 Code, packets, topologies and commands

8. **Every command is given in full.** `sudo ip netns add h1`, `uv add scapy==<exact>`, the capture
   command with its filter, the check command. A reader should never have to infer "and now
   presumably I create the namespace".
9. **Every code block is followed by `**Line by line:**`** — every non-obvious token, and *why it is
   that line and not another*. **An unexplained line is a bug in the doc.**
10. **Every packet is shown as bytes at least once.** A hexdump with the fields annotated, next to the
    `## Wire format` table (§24.4). A protocol you have only seen as a Wireshark tree is a protocol you
    cannot write.
11. **Every capture excerpt names how it was produced** — the command, the filter, the capture point,
    the topology — and gets its row in `docs/CAPTURES.md`.
12. **Every diagram of a topology is Mermaid, and matches a committed script.** A drawing that does
    not correspond to a `lab/<name>.sh` is decoration.
13. **Mermaid whenever the concept is spatial, sequential, or a state machine** — the three-way
    handshake, the TCP state machine, a packet's path through four namespaces, a BGP session opening,
    a queue filling. In this field that is most concepts, and a sequence diagram is usually worth more
    than the paragraph it replaces.
14. **Every mechanism has a matching failure with the real error text**, reproduced verbatim.
    Paraphrasing an error is worse than omitting it — the reader searches for the string. For silent
    failures, show the *wrong capture* instead: the retransmission that keeps happening, the window
    that stays at zero, the SYN with no reply.
15. **`TODO(me)` stays unsolved.** The doc teaches; it never does the reps.

### 27.4 Facts

16. **No invented facts.** Versions, header offsets, flag values, timer defaults, RFC section numbers,
    measured throughput: looked up live and dated, or explicitly `TODO`'d **with the exact lookup
    command**. Principles 6, 7 and 8 wearing their writing hat.
17. **Cite specifications by number and section**, and say whether you checked it is current: *"RFC
    9293 §3.1, checked 2026-08-27, not obsoleted"*. A claim attributed to "the RFC" is not a citation,
    and a claim attributed to a *superseded* RFC is a citation to a document that has been replaced.
18. **Tables for enumerable facts, prose for reasoning.** Never a table of one row.
19. **Emoji section markers, consistent not decorative** — 🎬 🎯 📚 🛠️ 💥 🎤 ✅ 💡 🅿️ 🔍 📌 ⚠️ 📐 🛑.
20. **🅿️ = parked**: awareness-level, interview-ready, deliberately not built (§4, L3). A parked ID
    still gets a part with a story, a mechanism and a production section; what it does not get is a
    build step. **The arithmetic is still worked** — you must be able to size the thing you did not
    run.
21. **🔍 = compare**: a "build first, compare after" day (Principle 3). The hand-rolled version already
    exists; today you open the tool and diff your understanding against theirs. A compare part must
    state at least one thing the tool does that yours does not, and **why**.
22. **🛑 = the ethics rule** (§4.2). Any part that generates traffic which would be hostile outside a
    namespace carries this marker in the hub's §2 map, and names its namespaces in `## Topology`.
23. **The interview paragraph is honest.** An answer you could actually defend, tied to what you built
    and to a number you measured. A war story with a capture in it beats an adjective.

### 27.5 The two things that are never written

24. **Never a clock.** Not "estimated hours", not "this takes an evening", not "quick", not "a short
    detour". `./m depth` fails the day on any of them (Principle 17). A *measured* duration is data
    and is required (§24.1).
25. **Never a trim.** If the day is getting long, it gets another part (§24.8). Cutting an explanation
    to fit is the one edit this format forbids outright.

### 27.6 The ritual

26. **Every day ends the same way** — the checklist, then the ledger rows, then the commit message
    `day NNN: <title> — closes <IDs>`. The sameness is the point: the repo is the memory, not the
    chat, and a stranger — or a different CLI agent six months from now — has to be able to pick up
    from the last row of `docs/PROGRESS.md` alone.

---

## 28 · 📝 Amendment record

| Version | Change |
| --- | --- |
| **v1.0.0** | Initial plan. 15 curricula, 248 IDs, 152 days (Day 0 + Days 1–151), 17 phases. Establishes the twenty principles (§2) including the **cryptography carve-out** to "build first, compare after" (P3), **reproduce the fault before you fix it** (P12) and **wire formats are stated, never inferred** (P20); the five silent failures (§6); the hub + `parts/` documentation architecture with the twelve-section part contract including the mandatory **Wire format** and **Topology** tables (§24); the four-tier $0 lab policy and the **ethics rule** (§4); and the seven hand-written / three generated ledgers including `SPECS.md`, `TOPOLOGIES.md`, `CAPTURES.md` and `MEASUREMENTS.md` (§26). |

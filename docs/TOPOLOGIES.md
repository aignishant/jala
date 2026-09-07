# 🕸️ TOPOLOGIES — every lab topology, and the script that rebuilds it

**Append-only.** A topology described in prose is not a topology (§24.9). *"Two hosts
connected through a router"* is a sentence. A topology is a **committed, idempotent
script** — `./m lab up <name>` run twice produces no error — plus a row here.

**A measurement whose topology has no row did not happen** (P9). `docs/MEASUREMENTS.md`
names a topology by the `Name` column below and by nothing else.

**Reuse before you invent.** Before adding a topology, read this table: a near-identical
second topology is two things to maintain and one more way for two results to stop being
comparable.

| Name | Script | Namespaces | Links | Address plan | netem | Day |
| --- | --- | --- | --- | --- | --- | --- |

No topology exists yet. Namespaces are `FOUND-14`, which the plan closes on **Day 9**; the
first script lands there. Day 0 only verifies whether this machine can host one at all —
see
[`days/day-000-toolchain-skeleton-driver/parts/04-the-linux-door/4.1-namespaces-need-linux.md`](../days/day-000-toolchain-skeleton-driver/parts/04-the-linux-door/4.1-namespaces-need-linux.md).

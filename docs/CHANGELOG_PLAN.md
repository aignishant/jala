# 📝 CHANGELOG_PLAN — every amendment to the master plan

**Append-only** (P14). If reality changes — an RFC obsoleted, a tool's flag removed, a
kernel default changed, a day that turns out to hold two ideas — **the plan is amended
first, here**, and only then does the code follow. Never silently adapt.

Structural changes get an ADR in [`adr/`](adr/); the plain text of the plan changes here.

---

## Open — raised on Day 0, not yet applied

Two conflicts surfaced while building the Day 0 toolchain. Both are recorded **before**
being worked around, which is the whole of P14.

### A-001 · Phase 0's gate cannot be met by Phase 0

**The plan says** (§23.1) Phase 0's gate is *"`./m check` green; `./m lab up two-host`
pings; no key and no capture in git"*. Phase 0 contains exactly one day — Day 0 — whose
subject is the toolchain, the skeleton and the driver.

**The conflict.** `two-host` is a namespace topology. Namespaces are `FOUND-14`, which
§23.2 closes on **Day 9**, and the ethics rule that governs every packet the lab sends is
Day 1. Day 0 cannot build `two-host` without pulling nine days of material out of order,
and §25 forbids reordering days without an ADR. Phase 1's gate *already* requires
`two-host` to ping, so the requirement is not lost by moving it — it is duplicated today.

**Proposed.** Phase 0's gate becomes *"`./m check` green; `./m lab` reports whether this
machine has network namespaces; no key and no capture in git."* The **door** is verified on
Day 0; the **topology** arrives with Phase 1. Needs an ADR, because it changes a phase gate.

**Status:** open. `./m lab` reports namespace availability and refuses to invent a topology
it was never given.

### A-002 · `./m check` cannot contain the lab rebuild

**`CLAUDE.md` says** `./m check` is *"ruff + format + pytest + depth + trace + lab rebuild"*.

**The conflict.** A lab rebuild needs root **and** Linux. Putting it inside `check` makes
the gate that guards every commit unrunnable on a laptop without `sudo`, and impossible on
macOS or Windows — the platforms §4 explicitly says to be honest about rather than pretend
around. It would also turn "I am not on Linux today" into a red build on a commit that
changed one markdown file.

**Proposed.** The rebuild is `./m lab verify <topology>`, run at a phase gate (§25 item 5)
rather than on every commit. `check` asks *"is this correct?"*; `lab verify` asks *"does
this topology still rebuild from its script?"*. Different questions, different frequencies.

**Status:** implemented in `./m` as `lab verify`. `CLAUDE.md`'s command list still needs the
matching edit.

---

## Applied

| Version | Date | Change | Why |
| --- | --- | --- | --- |
| v1.0.0 | 2026-08-27 | Initial plan — 15 curricula, 248 concept IDs, 152 days, 17 phases. | — |

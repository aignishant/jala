# Day 1 — definition of done

`./m done 1` refuses to commit while any box below is unticked. That refusal is the whole
point ([Day 0, 3.3](../day-000-toolchain-skeleton-driver/parts/03-the-driver/3.3-the-done-gate.md))
— and so is **not ticking a box you did not do**. The gate cannot tell.

**Status: this day is written, not done.** Every box below is unticked, which is the honest
state — `docs/PROGRESS.md` has no row for Day 1 and `OPS-01` is still **open**
([3.1](parts/03-traceability/3.1-the-id-scheme-and-what-closed-means.md)).

**Demo command — the whole day in one line:**

```bash
./m plan && ./m trace && ./m check && git log --oneline -1
```

---

## The parts — read, run, answer

One box per document in `parts/`. Tick it when you have read it, run its **Check yourself**
command, and answered its out-loud question *without scrolling back up*.

### Section 1 — the repo as memory

- [ ] [1.1 The repo as the network's memory](parts/01-repo-as-memory/1.1-the-repo-as-the-networks-memory.md)
- [ ] [1.2 Written by hand, or regenerated](parts/01-repo-as-memory/1.2-written-by-hand-or-regenerated.md)

### Section 2 — the six ledgers

- [ ] [2.1 `PROGRESS.md` — the row that says a day happened](parts/02-the-six-ledgers/2.1-progress-the-row-that-says-a-day-happened.md)
- [ ] [2.2 `PACKAGES.md` — never invent a version](parts/02-the-six-ledgers/2.2-packages-never-invent-a-version.md)
- [ ] [2.3 `SPECS.md` — read it before you quote it](parts/02-the-six-ledgers/2.3-specs-read-it-before-you-quote-it.md)
- [ ] [2.4 `TOPOLOGIES.md` — a script, not a sentence](parts/02-the-six-ledgers/2.4-topologies-a-script-not-a-sentence.md)
- [ ] [2.5 `CAPTURES.md` — the provenance, never the bytes](parts/02-the-six-ledgers/2.5-captures-the-provenance-never-the-bytes.md)
- [ ] [2.6 `MEASUREMENTS.md` — what turns a number into a result](parts/02-the-six-ledgers/2.6-measurements-what-turns-a-number-into-a-result.md)

### Section 3 — traceability

- [ ] [3.1 The ID scheme, and what "closed" means](parts/03-traceability/3.1-the-id-scheme-and-what-closed-means.md)
- [ ] [3.2 `scripts/trace.py`](parts/03-traceability/3.2-scripts-trace-py.md)
- [ ] 💥 [3.3 An open ID in a completed phase is a bug](parts/03-traceability/3.3-an-open-id-is-a-bug.md)

### Section 4 — 🛑 the rule that comes before every other rule

- [ ] 🛑 [4.1 The rule before every rule](parts/04-the-ethics-rule/4.1-the-rule-before-every-rule.md)
- [ ] [4.2 Naming your containment](parts/04-the-ethics-rule/4.2-naming-your-containment.md)
- [ ] 🅿️ [4.3 The line, and the arithmetic](parts/04-the-ethics-rule/4.3-the-line-and-the-arithmetic.md)

---

## The ledgers — understood, not just present

- [ ] Can name all **seven** append-only ledgers and all **four** generated projections, and
      say which command regenerates each projection
- [ ] Ran `./m tracker` then `git status --porcelain docs/ days/INDEX.md` — **empty**, so no
      projection has drifted from its sources
- [ ] Understand why `>` instead of `>>` on a ledger destroys the history, and have checked
      that every append in this day's commands uses `>>`
- [ ] Can state, for `docs/MEASUREMENTS.md`, the four columns people leave out and the
      specific failure attached to each
- [ ] Can explain why `docs/CAPTURES.md` records the provenance and never the bytes, and name
      the column that distinguishes a filtered capture from a stalled connection

---

## Specifications — resolved live, not recalled (P7)

- [ ] Ran `curl -sL https://www.rfc-editor.org/info/rfc793 | grep -i -A2 'obsoleted by'` and
      read that TCP is now **RFC 9293**
- [ ] Confirmed RFC 9293 has **no** "Obsoleted by" line — the difference is the whole check
- [ ] Confirmed RFC 8312 → **RFC 9438** (CUBIC), and RFC 7230 → **RFC 9110** (HTTP)
- [ ] Understand why fetching `rfc793.txt` and reading it carefully **cannot** tell you it has
      been superseded
- [ ] Understand why omitting `-L` produces a **false all-clear**, and that the absence of a
      warning and the absence of a fetch look identical
- [ ] The five `docs/SPECS.md` rows from the hub's §11 are appended, marked *status only* —
      none is quoted for a field offset yet

---

## Build brief — `scripts/trace.py` is yours

- [ ] **`scripts/trace.py`** created, reading its three inputs from **three independent
      sources**: the day map, each hub's `ids:` frontmatter, and `docs/PROGRESS.md`
- [ ] It decides "complete" from the **progress ledger**, never from the day folder existing
- [ ] It reports **matched**, **mismatched**, **open** and **closed**
- [ ] It regenerates `docs/TRACEABILITY.md`, and that file carries the do-not-edit header
- [ ] It exits **non-zero** on a mismatch and on an open ID from a completed phase
- [ ] `./m trace` no longer prints the `WARN … not written yet` line
- [ ] **`tests/test_trace.py`** created with `test_open_id_in_completed_phase_is_a_bug`
- [ ] That test drives `compare()` with hand-built dicts — **no filesystem, no network**
      (plan §5: unprivileged, deterministic, offline)

---

## The check that must be able to fail (P11, P12)

- [ ] Watched `tests/test_trace.py` go **RED** with `NotImplementedError` before implementing
      anything
- [ ] **Injection 1 — the hole:** removed `FOUND-12` from Day 7, ran `./m plan`, saw
      `PROBLEM: IDs declared but never closed: ['FOUND-12']`, restored on the same run
- [ ] **Injection 2 — the duplicate:** added `FOUND-12` to Day 8 as well, saw
      `PROBLEM: IDs used more than once: ['FOUND-12']`, restored
- [ ] **Injection 3 — the typo:** transposed `FOUND-12` to `FOUND-21`, saw **two** problems
      that are one bug, restored
- [ ] `cp scripts/plan_check.py scripts/plan_check.py.bak` was run **before** each injection,
      and the `.bak` was removed afterwards
- [ ] **Verified the restore:** `./m plan` ends `OK - every declared ID is closed exactly
      once.` — a restore you did not check is a restore you are assuming
- [ ] Can say what a green traceability report **cannot** tell you about a day

---

## 🛑 The ethics rule (§4.2, P13)

- [ ] Can state all **five** rules of §4.2 without looking
- [ ] Can name the four words — `ip netns exec h1` — that separate a contained exercise from
      an incident, and explain why the terminal output is identical either way
- [ ] Understand why there can be **no technical check** for this, and what this repository
      uses instead: the declared tier and the named namespaces, written **before** the command
- [ ] Can explain what a complete `## Topology` section carries and the **two** obligations it
      satisfies at once
- [ ] Can explain why the *technique* of an attack is practised here and only the *target* is
      parked

---

## Lab budget and traffic

- [ ] Tier recorded as **L0** overall, with **2.3 at L2** (reading published RFC info pages)
      and **4.3 at L3** (parked)
- [ ] Namespaces: **0** · links: **0** · netem: **none** · topology: **none**
- [ ] **Every packet this day generated stayed where it should:** the only traffic is a handful
      of hand-typed requests to `rfc-editor.org` and `datatracker.ietf.org` — published
      document servers, read-only and gently (§4.2 rule 2). Nothing was scanned, probed or
      swept.
- [ ] No capture and no key was added to git —
      `git status --porcelain | grep -E '\.(pcap|pcapng|pem|key)$'` returns nothing

---

## Silent failures (§6) — which ones this day names

- [ ] **#1, the cache answered, not the network** — named in
      [2.6](parts/02-the-six-ledgers/2.6-measurements-what-turns-a-number-into-a-result.md) as
      the `dig` benchmark whose second query never leaves the machine. **The check:** flush and
      retest cold.
- [ ] **#4, averaged away** — named in
      [2.6](parts/02-the-six-ledgers/2.6-measurements-what-turns-a-number-into-a-result.md).
      **The check:** five seeds minimum, warm-up discarded, p50/p95/p99 **with the spread**,
      never the best run.
- [ ] Neither could contaminate a result today, because **Day 1 measures nothing** — and no
      number was invented so a ledger would look started (P8, P10)

---

## Ledgers (plan §26)

- [ ] `docs/PROGRESS.md` — the Day 1 row appended, verbatim from the hub's §11
- [ ] `docs/SPECS.md` — five rows, each with its status resolved live on a stated date
- [ ] `docs/PACKAGES.md` — **no rows**; nothing was installed today
- [ ] `docs/TOPOLOGIES.md` — **no rows**; the first topology is Day 9
- [ ] `docs/CAPTURES.md` — **no rows**; no capture was taken
- [ ] `docs/MEASUREMENTS.md` — **no rows**; Day 1 makes no empirical claim
- [ ] `docs/CHANGELOG_PLAN.md` — **A-001** and **A-002** still open, still needing ADRs

---

## Budget

- [ ] Cost today: **$0**

---

## Commit

- [ ] `git status --porcelain` **read** before staging, not after
- [ ] `./m check` is green, **including `./m trace`**
- [ ] `./m done 1` run, and it committed rather than refused
- [ ] `git status --porcelain | wc -l` is **0** afterwards — a clean tree

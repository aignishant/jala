---
name: day-jala
description: Generate the hub, the parts/ sub-documents, the lab scaffold and the checklist for a given day of the Jāla plan
argument-hint: [day-number]
---

# Generate Day $ARGUMENTS of the Jāla plan (v1.0.0 — hub + `parts/`)

> **Read `docs/00_MASTER_PLAN.md` §24 before writing a single line, and §6 and §4.2 before writing a
> single line of code.** §24 is the depth contract this skill implements; §6 is the five silent
> failures that make networks go wrong quietly; §4.2 is the ethics rule that governs every packet
> this curriculum sends. This skill is the procedure; the plan is the standard.

## The five commitments (§24.1 and §4.2 — everything below follows from these)

1. **One idea per document.** If it needs "also" to introduce its second half, it is two documents.
2. **No clocks.** Never write a time estimate, a duration, an "estimated hours" field, or a pace —
   not in frontmatter, not in prose, not in the checklist. **A *measured* duration is data and is
   required**: an RTT, an RTO, a `TIME_WAIT`, a p99, a netem setting. **Never trim an explanation
   because the day is getting long — split it into another part instead.**
3. **Zero to production, in one document.** Open where a reader who has never heard of the idea can
   stand. End where a professional stands: what an operator runs instead, what breaks at scale, what
   a reviewer says, what an interviewer probes. **Loopback is not a network** — a part that stops at
   `127.0.0.1` has taught half the subject.
4. **Every number has a provenance.** Measured here — with topology, netem settings, seed,
   repetitions, hardware and date — or specified with an RFC number and section, or cited to a named
   paper. **Never recalled.** This is the rule you are most likely to break.
5. **🛑 Every packet stays home.** Anything hostile or high-volume runs inside namespaces created for
   the purpose. The public internet is read-only and gentle. A part that teaches an attack and does
   not name its containment is not finished.

---

## Step 1 — gather

1. Read the plan: **§2** (the twenty principles), **§4** (the four lab tiers and the ethics rule),
   **§6** (the five silent failures), **§23** (the day map — the authoritative ID list for day
   $ARGUMENTS), **§24** (the depth contract), **§27** (the style guide). Collect every ID slotted to
   day $ARGUMENTS, the phase theme, and the gate that phase feeds.
2. Read `docs/PROGRESS.md`. **Confirm $ARGUMENTS is exactly one more than the last row.** If it is
   not, say so and stop — do not generate out of order (plan §25: never skip, merge or reorder a day
   without an ADR).
3. Read `docs/TRACEABILITY.md`. Any open ID from a completed phase is a bug — report it, don't paper
   over it.
4. Read the previous day's `days/day-NNN-<slug>/LESSON.md` and `CHECKLIST.md`. If the checklist has
   unticked boxes, warn me and ask before proceeding. **Build on the code the previous days told the
   learner to write in `jala/` — never duplicate it, never rewrite it.** By Day 34 there is a
   forwarder; by Day 61 there is a TCP state machine. A day that re-derives what already exists has
   wasted the learner's typing.
5. Read the ledgers that bind this day: `docs/PACKAGES.md` for what is pinned, `docs/SPECS.md` for
   which RFCs have already been read and at what status, `docs/TOPOLOGIES.md` for which topologies
   already exist — **reuse a topology rather than inventing a near-identical one** — and
   `docs/MEASUREMENTS.md` for what has already been measured on them.

## Step 2 — verify reality before you write (Principles 6, 7, 8, 14)

6. **Never invent a wire-format detail.** For every header the day shows, open the specification
   live, at `https://www.rfc-editor.org/rfc/rfcNNNN` (or the info page,
   `https://www.rfc-editor.org/info/rfcNNNN`), and:
   - confirm it is **not marked "Obsoleted by"** — TCP is RFC 9293, not 793; CUBIC is RFC 9438, not
     8312; HTTP/1.1 messaging is RFC 9112 and its semantics are RFC 9110, which between them replaced
     RFC 7230. A curriculum quoting section numbers from a superseded
     document sends its reader to replaced text;
   - read the section that actually specifies the fields, and cite it by number;
   - write the row into `docs/SPECS.md`: number, title, status, obsoletes/obsoleted-by, sections
     read, date, day.
   If the spec disagrees with the plan, **stop and propose an amendment** — do not silently adapt.
7. **Never invent a default.** A timer, a buffer size, a backlog cap, an initial window, a queue
   length: **read it off the running system** — `sysctl net.ipv4.tcp_*`, `ss -i`, `ip route show`,
   `tc -s qdisc show`, `cat /proc/sys/...` — and record which system and which kernel version. A
   default is a fact about a build, not about a protocol, and it changes between distributions.
8. **Never invent a version.** For every package the day installs, read the version live
   (`curl -s https://pypi.org/pypi/<pkg>/json`, or `uv pip compile` for a resolved answer); for every
   system tool, `<tool> --version`. Record package, version and date in `docs/PACKAGES.md`. If a
   lookup fails, leave a `TODO(<exact command>)` — never a guess.
9. **Never invent a number.** This is the one that matters most here.
   - A header size, an MTU, a "typical" RTT, a throughput figure, a convergence time, a timer value,
     a percentage of traffic — **none of these may be written from memory.**
   - Either **measure it** in the day (and the part states topology, netem settings, seed,
     repetitions, hardware, date), or **specify it** (RFC + section, fetched), or **cite it** (paper
     title, venue, year), or leave `TODO(measure: <the exact command>)`.
   - If you catch yourself writing "typically", "usually", "around", or "on the order of" in front of
     a number, stop: that is a rumour with a hedge in front of it.
10. **Confirm the tier and the containment.** Decide whether the day is L0 (one host, user space), L1
    (namespaces), L2 (public internet, read-only) or contains L3 🅿️ material. If any step needs root
    or a namespace, **the day must say which capability, why, and what the unprivileged version
    demonstrates instead.** If any step generates traffic, **name the namespaces** it stays inside.
    A day that silently requires root, or that would send a packet to somebody else's machine, is a
    broken day.

## Step 3 — plan the split (do this before writing prose)

11. List the day's subtopics. Group them into **sections** that share one mental model — usually one
    section per curriculum ID, per layer, per stage of a packet's journey, or per phase of a protocol
    exchange. State the grouping; an unexplained numbering is a bug.
12. Split by **idea boundaries, never by length or pace** (§24.8). There is no target part count.
    - `format` days: one header per part — the fields → the encoding → the edge case → the malformed
      one
    - `build` days: mechanism → wire format → behaviour → edge case → failure mode → production use
    - `protocol` days: one phase of the exchange per part — open → transfer → close → timers →
      failure
    - `compare` 🔍 days: one dimension of difference per part
    - `measure` days: topology → harness → run → read → what the number does not say
    - `diagnose` days: one symptom per part, each ending in the evidence that identifies it
    - `concept` days: one claim per part, each with its evidence
13. **Every day gets at least one part whose subject is a deliberate failure** — and that part
    **injects** the failure rather than describing it (Principle 12). Print the command that causes
    it. Usually at `production` level.
14. Assign each part a `level` — `foundation` (knows what it is), `working` (can implement it, and
    recognises its signature in a capture), `production` (knows what changes in a real network, and
    can defend it with arithmetic) — and a `tier` (`L0`/`L1`/`L2`/`L3`). A day should climb.
15. Apply the **one-idea test**, the **standalone test**, the **no-shortcut test** and the
    **provenance test** to each planned part *before* writing.
16. **Print the planned part list to me before writing.** If it looks thin, I will say so.

## Step 4 — write the parts (`days/day-NNN-<slug>/parts/<NN>-<slug>/<section>.<sub>-<slug>.md`)

> **Name the day folder `days/day-NNN-<slug>/`** — the number **zero-padded to three digits** (the
> plan runs to 151), then a kebab-case slug of 1–4 words taken from the hub's `title` with articles
> dropped: `days/day-037-pmtu-black-hole/`. A number alone is an address, not an answer. The number
> stays the identity — `./m`, `depth_check.py`, `tracker.py` and `trace.py` all resolve a day by
> number and accept any slug — so a folder can be renamed at any time. `./m depth` rejects a bare
> `days/day-037/` and rejects a two-digit `day-37-…`.

17. **One folder per section**, two zero-padded digits **then a kebab-case slug of 1–3 words saying
    what the section is about** — `parts/01-arp-request/`, `parts/03-the-cache/`. Take the slug from
    the section's heading in the hub's §2 map. A bare `parts/01/` is rejected. Every part lives inside
    its section's folder, and the folder number must match the number before the dot in the filename.
18. One file per subtopic, named `<section>.<subtopic>-<kebab-slug>.md`. The slug says what the part
    *teaches*, never where it sits. Numbering starts at `1` and has no gaps.
19. **Links are relative to the part's own folder**: a sibling is `1.2-<slug>.md`; another section is
    `../01-<slug>/1.5-<slug>.md`; the hub is `../../LESSON.md`. `prev` and `next` use the same form.
    The hub's §2 map links the full path from the day folder.
20. Every part carries all twelve sections of §24.4, **in this order** (three are conditional):
    - **frontmatter** — `day`, `part`, `title`, `ids`, `level`, `tier`, `prerequisites`, `prev`,
      `next`. **No duration field of any kind.**
    - **One-line answer** — the claim in one sentence, before anything else.
    - **The story** — a concrete scene first: a person, a machine, a failure, a decision. **No jargon
      at all** in this section. It must pass all four story tests of plan §27.1 item 6, and a story
      that fails one is rewritten, not defended:
      - **Everyday.** A kitchen, a shop, a bus, a phone, a queue, a bill, a lift, a shared tap, a
        block of flats with one letterbox. **Never a trade the reader has not practised** — no
        compositors, watchmakers, actuaries, hauliers, telegraph clerks or ships' navigators. If the
        metaphor has to be learned before it can teach, it is a second lesson, not a hook.
      - **Plain.** No word a twelve-year-old would look up; no sentence they would read twice.
      - **Concrete.** Real objects and real numbers — *fourteen people in the queue*, *a 90-second
        wait*, *three lifts and one of them locked* — never "some traffic" or "a quantity".
      - **Honest.** A thing that genuinely happens, with the failure it genuinely causes. A scene
        built backwards from the lesson reads as contrived and costs the reader's trust in the
        section after it.

      Write in the second person (*you*) or with a plain role noun (*the person on the help desk*).
      **Never invent a name, and never guess a pronoun** — plan §27.1 item 5 bans names, and
      they/them is the default for anyone whose pronouns are not stated.

      **Check the whole day for callbacks after writing a story.** Later sections routinely reuse the
      story's nouns. A rewritten story with stale callbacks downstream is worse than the original.
    - **The idea in plain language** — the concept assuming zero prior knowledge; every term defined
      on first use, **including terms from earlier days**, with a link to the part that introduced
      them. No code.
    - **Why Jāla needs it** — the concrete later day that breaks without this. Never "this is
      important".
    - **The mechanism** — how it actually works: runnable code, the exchange written out, or the
      diagram. Nothing skipped as "obvious".
    - **Wire format** ⟵ *required whenever a header, frame, message or record is introduced or
      parsed.* A table: byte offset (decimal, zero-based) · bit width · field name · **the value in
      this example, in hex and decoded** · what it means. **State the byte order explicitly**, written
      out as *big-endian* rather than as "network byte order". Show the bytes at least once as an
      annotated hexdump. Omit the section only if the part genuinely has no wire format.
    - **Topology** ⟵ *required whenever the part runs something at tier L1 or L2.* The namespaces,
      the links, the addresses, the netem settings, and the exact `lab/<name>.sh` that builds it — as
      a Mermaid diagram plus an address table. **Name the namespaces the traffic stays inside**
      (§4.2). A measurement without a topology is an anecdote. Reuse an existing topology from
      `docs/TOPOLOGIES.md` where one fits; if you add one, write its row.
    - **Line by line** — a `**Line by line:**` list **immediately after each code block**: every
      non-obvious token, and *why that line and not another*. Omit only if the part has no code
      needing a walkthrough.
    - **When it breaks** — the **real** error text verbatim (`Destination Host Unreachable`,
      `Connection reset by peer`, `certificate verify failed`, `EAGAIN`), what it means, the smallest
      fix. And for this field: **the silent version too** — the packet that never arrives, the
      retransmission that keeps happening, the window that stays at zero — shown as a capture
      excerpt, plus the check that catches it (§6).
    - **In production** — the real-network version: what an operator runs instead of the teaching
      version, what degrades at scale, the failure that only shows with real traffic and real
      middleboxes, the review comment, and the interview question that finds out whether you have
      actually debugged one. **Not optional.**
    - **Check yourself** — one command to run now **that prints a number, not just a pass**, and one
      question to answer out loud.
21. Apply **Jāla's six additional part rules** (§24.4.1): name the RFC and section checked, and the
    date · read every default off the running system and name the kernel · every number measured-here
    or specified or cited · **name the silent failure** the part is avoiding and how the reader
    detects it · **state the tier and the namespaces** · **reproduce before you repair**.
22. Mermaid diagram whenever the concept is spatial, sequential, or a state machine — the three-way
    handshake, the TCP state machine, a packet's path through four namespaces, a BGP session opening,
    a queue filling, the resolver walking down from the root. In this field that is most concepts.
23. **Offset and byte-order comments in every code block**:
    `total_len = int.from_bytes(buf[2:4], "big")  # bytes 2-3: total length, big-endian`. The
    `Wire format` table is the summary; the comments are the working. **Never a bare
    `struct.unpack("H", …)`** — the result depends on the machine.

## Step 5 — write the hub (`days/day-NNN-<slug>/LESSON.md`)

24. The hub orients and assembles; **it never teaches**. No `Line by line:`, no `Wire format` table
    and no `Topology` diagram in the hub. Required sections, in order (§24.5):
    - YAML frontmatter (`day`, `phase`, `phase_name`, `title`, `ids`, `principles`, `kind`,
      `plan_version: "v1.0.0"`, `parts`, `tier`, `topology`, `generated`, `status`,
      `lab_scaffolded`, `commit`)
    - a **yesterday / today / tomorrow** blockquote — no time estimate
    - `## §1 Where we are` — a scene and an analogy, plain language, NO code, NO jargon
    - `## §2 The map` — a table of every part: number, linked title
      (`parts/01-<slug>/1.1-<slug>.md`), what it answers, `level`, `tier`, grouped by section with one
      line saying what each *section* means. Mark 🛑 on any part whose traffic would be hostile
      outside a namespace. **No minutes column, ever.**
    - `## §3 Setup — run this` — every `mkdir`, `touch`, `uv add <pkg>==<exact>`, `sudo apt install`
      and `./m lab up <name>` the day needs, pinned and verified that day
    - `## §4 Build brief` — files to create, with `TODO(me)` markers left unsolved
    - `## §5 The check that must be able to fail` — the check that is RED before the TODOs are done,
      and **what "RED" looks like on the wire** for this day
    - `## §6 Lab budget` — the tier (L0/L1/L2/L3), the topology name, the namespace and link count,
      the netem settings. `L0` is an answer; state it.
    - `## §7 Traps` — the mistakes that eat an evening, including the named Silent Failure (§6)
    - `## §8 Verify before you code` — the live URLs actually fetched: **every RFC info page, with
      its status and the date you opened it**, the tool man pages, the library doc pages. Never from
      memory.
    - `## §9 Say it in an interview` — one paragraph, spoken voice, tied to a number you measured
    - `## §10 Done when` — pointer to `CHECKLIST.md`, defined by understanding and green checks
    - `## §11 Ledger & commit` — the verbatim `PROGRESS.md` row, any `PACKAGES.md`, `SPECS.md`,
      `TOPOLOGIES.md`, `CAPTURES.md` and `MEASUREMENTS.md` rows, and the commit message
      `day NNN: <title> — closes <IDs>`. **The hub ends here.**

## Step 6 — the checklist (`days/day-NNN-<slug>/CHECKLIST.md`)

25. Demo command, setup boxes, **one box per part document** (read it, run its check-yourself, answer
    its out-loud question), build-brief boxes, a test box per test **including at least one "break it,
    watch it go red, fix it"**, the lab budget, the ledger rows pasted, and the commit box. No time
    estimates.
26. **On any day that runs something in the lab, the checklist must include:**
    - [ ] The topology was torn down and rebuilt from its script, twice, cleanly (`OPS-03`)
    - [ ] Every packet this day generated stayed inside namespaces I created (§4.2)
    - [ ] The `docs/MEASUREMENTS.md` row is written: topology, netem, seed, repetitions, hardware,
          result **with the spread**, outcome
    - [ ] Which of the five silent failures (§6) this result could have hit, and how I ruled it out
    - [ ] No capture and no key was added to git:
          `git status --porcelain | grep -E '\.(pcap|pcapng|pem|key)$'` returns nothing

## Step 7 — verify

27. Run `./m depth $ARGUMENTS`. **Fix every failure; never hand-wave past one.**
28. Run `./m trace` — the day's IDs must match §23 exactly, no more and no fewer.
29. Run `./m lab up <topology> && ./m lab down` if the day introduced a topology; then run `up`
    twice to prove idempotence.
30. Run `./m tracker`.

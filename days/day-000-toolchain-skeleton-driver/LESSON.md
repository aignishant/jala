---
day: 0
phase: 0
phase_name: "Foundry"
title: "Toolchain, skeleton and the ./m driver"
ids: []
principles: ["P1 doc-first", "P2 one day one commit", "P6 never invent a version", "P9 captures and keys never committed", "P10 fail honestly", "P11 a check that can go RED", "P16 depth over density", "P17 no clocks", "P18 zero to production"]
kind: setup
plan: jala
plan_version: "v1.0.0"
parts: 18
tier: L0
topology: none
generated: "2026-09-07"
status: complete
lab_scaffolded: false
commit: "day 000: complete"
---

# Day 0 — toolchain, skeleton and the `./m` driver

**Phase 0 · Foundry** · This day closes **no curriculum IDs**. It exists so that Day 1 can
start with work instead of with installation.

> **Yesterday:** nothing.
> **Today:** one owner for the environment, a repository that cannot commit a private key or
> a packet capture, a driver that refuses a half-finished day, and an honest answer about
> whether this machine can host the lab.
> **Tomorrow:** the six ledgers, `scripts/trace.py`, and the ethics rule that governs every
> packet you will send — Day 1 closes `OPS-01`.

> **Read this hub first**, then work through `parts/` in order. There is no time estimate on
> this day or any other: a day is a unit of subject, not of hours (P17). The definition of
> done is the checklist, not the clock.

---

## §1 Where we are

There is a version of this project where you install things when you need them. On Day 18 you
need `scapy`, so you install `scapy`. On Day 107 you need `cryptography`, so you install that.

That version fails somewhere around Day 40, and here is exactly how. You will have three
Python installations on this machine — one from an installer, one that came with an editor,
one from a tool you tried once. `pip install` will put a package into one of them. Running
your code will use a different one. You will spend an evening on an import error for a package
you can see in your file explorer, and nothing will be broken: two words on the same keyboard
will simply be pointing at two different machines that share a disk.

That evening is not bad luck. It is what happens when **nothing owns the environment** — when
"which Python is this?" is answered by an accumulated list of folders that every installer you
have ever run has appended itself to.

There is a second version of that story, and it is the one this curriculum has to worry about
more. On Day 8 you take your first packet capture. On Day 107 you generate a private key. Both
of those land in your project folder next to everything else, and both of them are permanent
the moment they are committed — because a repository's history is append-only, and deleting a
file tomorrow does not remove it from yesterday. A capture is a recording of real traffic; it
can carry a session cookie, an internal hostname, a password. The rule has to exist **before**
the first capture does, because a rule written on Day 8 is written next to a file you already
have.

So today is the boring day, and it is three sentences:

- **One tool owns the environment.** `uv` installs the interpreter, creates the environment,
  resolves and locks every package, and runs your code inside it. You will never type `pip`
  here.
- **One repository holds the memory, and refuses two things.** A skeleton where the location
  of a file is a claim about what it is, and a `.gitignore` written before a key or a capture
  has ever existed.
- **One script owns the routine.** `./m start 4`, `./m check`, `./m done 4` — and `done`
  physically refuses while a checkbox is unticked, a check is red, or a capture is staged.

And one honest answer, which is the fourth thing and is specific to this subject. The lab this
curriculum runs on is built from **Linux network namespaces**, and they do not exist on
Windows or macOS. Today you run the command that fails and write down what this machine can
actually do. "Not available" is a correct answer and blocks nothing until Day 9.

```mermaid
flowchart LR
    S1["§1 the tools<br/>who owns the environment"] --> S2["§2 the skeleton<br/>what each folder claims"]
    S2 --> S3["§3 the driver<br/>the script that refuses"]
    S3 --> S4["§4 the Linux door<br/>can this machine host L1?"]
    S4 --> S5["§5 closing<br/>a check that can go red"]
    style S1 fill:#1f6feb,color:#fff
    style S4 fill:#d29922,color:#000
    style S5 fill:#238636,color:#fff
```

---

## §2 The map

**What the section numbers mean today.** This is a `setup` day, so §24.8 splits it by *one
tool, one file, or one command per part*. The five sections are the four owners above plus the
close: **1.x** the tools that own the environment, **2.x** the skeleton on disk, **3.x** the
driver that owns the routine, **4.x** the lab door and the tier vocabulary, **5.x** the check
and the commit.

Read them in order — each part names its prerequisites and builds on the one before.

### Section 1 — the tools that own things

| Part | What it answers | Level | Tier |
| --- | --- | --- | --- |
| [1.1 Why one tool must own the environment](parts/01-toolchain/1.1-why-one-tool-owns-the-environment.md) | Why does `pip install X` succeed and `import X` still fail? | `foundation` | L0 |
| [1.2 Git, and the shell every command is written in](parts/01-toolchain/1.2-git-and-the-shell.md) | What does a commit actually contain, and why is every command here bash? | `foundation` | L0 |
| [1.3 `uv`, the one binary](parts/01-toolchain/1.3-uv-the-one-binary.md) | What four jobs does `uv` replace, and why is it not a Python package? | `working` | L0 |
| [1.4 Python 3.12, and why not the newest](parts/01-toolchain/1.4-python-3-12-and-not-the-newest.md) | Why is being one release behind the right call? | `working` | L0 |
| [1.5 The editor, and the interpreter trap](parts/01-toolchain/1.5-the-editor-and-the-interpreter-trap.md) | Why does the editor disagree with the terminal, and which one is right? | `working` | L0 |

### Section 2 — the skeleton on disk

| Part | What it answers | Level | Tier |
| --- | --- | --- | --- |
| [2.1 The folder skeleton](parts/02-skeleton/2.1-the-folder-skeleton.md) | What claim does each folder make, and what does being wrong look like? | `foundation` | L0 |
| [2.2 `.gitignore`, before anything secret exists](parts/02-skeleton/2.2-gitignore-before-secrets-exist.md) | Why write it now, and why does deleting a leaked key not remove it? | `production` | L0 |
| [2.3 `git init`, and what a repository is](parts/02-skeleton/2.3-git-init-and-what-a-repo-is.md) | What is inside `.git`, and what is a branch really? | `foundation` | L0 |
| [2.4 `pyproject.toml` and the lockfile](parts/02-skeleton/2.4-pyproject-and-the-lockfile.md) | What is the difference between intent and resolution, and why commit both? | `working` | L0 |
| [2.5 The `.venv` you never activate](parts/02-skeleton/2.5-the-venv-you-never-activate.md) | What does `activate` actually do, and why does this project skip it? | `working` | L0 |

### Section 3 — the driver that owns the routine

| Part | What it answers | Level | Tier |
| --- | --- | --- | --- |
| [3.1 `set -euo pipefail`](parts/03-the-driver/3.1-set-euo-pipefail.md) | Which three ways does bash report success after failing, and how do you stop it? | `production` | L0 |
| [3.2 The `case` dispatcher](parts/03-the-driver/3.2-the-case-dispatcher.md) | How do a dozen routines live in one file, and why one entry point? | `working` | L0 |
| [3.3 The `done` gate](parts/03-the-driver/3.3-the-done-gate.md) | Why does a refusal work where a reminder does not — and what can it never check? | `production` | L0 |
| [3.4 The depth contract, made mechanical](parts/03-the-driver/3.4-the-depth-contract-made-mechanical.md) | What can a script check about a day, and what must a person read? | `production` | L0 |

### Section 4 — the Linux door, and where packets are allowed to go

| Part | What it answers | Level | Tier |
| --- | --- | --- | --- |
| 💥 [4.1 Namespaces need Linux](parts/04-the-linux-door/4.1-namespaces-need-linux.md) | Can this machine host the lab — and what exactly does it say when it cannot? | `production` | L0 |
| [4.2 The four tiers, and why Day 0 is L0](parts/04-the-linux-door/4.2-the-four-tiers.md) | What do L0, L1, L2 and L3 commit you to, and where do the packets go? | `foundation` | L0 |

**💥 4.1 is this day's deliberate-failure part** (§24.8). It does not describe the failure — it
**causes** it, with the command printed, which is what P12 requires of every day that
diagnoses anything.

### Section 5 — closing the day

| Part | What it answers | Level | Tier |
| --- | --- | --- | --- |
| [5.1 The check that must be able to go red](parts/05-first-commit/5.1-the-check-that-can-go-red.md) | Why is a test that has never failed worth nothing? | `production` | L0 |
| [5.2 The first commit, and reading a clean tree](parts/05-first-commit/5.2-the-first-commit.md) | What do you check in the last moment before a commit becomes permanent? | `working` | L0 |

---

## §3 Setup — run this

Every command below is explained in the part named beside it. **Do not paste this section
blind** — it is the summary, not the lesson. Work through the parts; this exists so the day
can be re-run from scratch later without re-reading.

All commands are **Git Bash** on Windows, or your normal terminal on macOS and Linux.

```bash
# --- section 1: the tools (parts 1.1-1.5) ---
# Install Git from https://git-scm.com/download/win, then in Git Bash:
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global core.autocrlf input        # ./m breaks without this — part 1.2

curl -LsSf https://astral.sh/uv/install.sh | sh
# close Git Bash, reopen it — PATH is read once, at shell start — then:
uv python install 3.12

code --install-extension ms-python.python
code --install-extension charliermarsh.ruff

# --- section 2: the skeleton (parts 2.1-2.5) ---
mkdir -p jala/{wire,stack,route,resolve,app,crypt,probe} lab scripts tests days docs/adr .vscode

# .gitignore FIRST — before git init, before any key or capture exists (part 2.2)
# .vscode/settings.json — see part 1.5 for the four settings and why each one matters

git init
uv sync                                        # writes .venv and uv.lock — part 2.4

# --- section 3: the driver (parts 3.1-3.4) ---
# write ./m — the full script is built up across parts 3.1, 3.2 and 3.3
chmod +x m
git update-index --add --chmod=+x m            # the bit must be committed — part 3.2

# --- section 4: the Linux door (parts 4.1-4.2) ---
./m lab up two-host                            # this WILL fail today. Read what it says.

# --- section 5: closing (parts 5.1-5.2) ---
# write tests/test_setup.py from the §4 skeleton, leave the TODO(me) bodies unsolved
uv run python -m pytest tests/test_setup.py -v  # three RED — that is correct
git status --porcelain                          # READ this before staging
./m done 0
```

Packages pinned today, with the version **read live from the index on 2026-09-07** (P6) and a
dated row in [`../../docs/PACKAGES.md`](../../docs/PACKAGES.md):

| Package | Version | Group | Why today |
| --- | --- | --- | --- |
| `ruff` | `==0.16.6` | dev | linter + formatter; the first two gates of `./m check` — [2.4](parts/02-skeleton/2.4-pyproject-and-the-lockfile.md) |
| `pytest` | `==9.1.1` | dev | P11 needs a runner for the check that can go RED — [5.1](parts/05-first-commit/5.1-the-check-that-can-go-red.md) |

**There are no runtime dependencies, and that is the point.** `scapy`, `dnspython` and
`cryptography` each arrive on the day they are first used, after the hand-rolled version
exists (P3).

---

## §4 Build brief

Four files are yours to write. The parts give you every command and every concept; the
`TODO(me)` markers are deliberately unsolved.

**1. `m`** — the daily driver. Parts [3.1](parts/03-the-driver/3.1-set-euo-pipefail.md),
[3.2](parts/03-the-driver/3.2-the-case-dispatcher.md) and
[3.3](parts/03-the-driver/3.3-the-done-gate.md) build it up. **Type it; do not copy it.** You
will edit this file a dozen times over 152 days, and you cannot edit what you have never read.

**2. `.gitignore`** — part [2.2](parts/02-skeleton/2.2-gitignore-before-secrets-exist.md) has
every line and the reason for each. Write it **before** `git init`.

**3. `README.md`** — a short description of what this repository is, in your own words.

**4. `tests/test_setup.py`** — the check that must be able to fail. Create it with the
skeleton from [5.1](parts/05-first-commit/5.1-the-check-that-can-go-red.md), then fill in the
three `TODO(me)` bodies yourself:

- `test_pins_are_exact` — every dependency uses `==`, not a range (P6)
- `test_secrets_and_captures_are_ignored` — `.env`, `*.pem`, `*.key`, `*.pcap` and
  `captures/` are all covered, and `!.env.example` re-includes the example (P9)
- `test_daily_driver_is_strict` — `m` exists, starts with a bash shebang, and contains
  `set -euo pipefail`

---

## §5 The check that must be able to fail

The three tests above are **red right now** — each raises `NotImplementedError`. That is the
correct starting state (P11): a test that has never been red has never proved anything.

```bash
uv run python -m pytest tests/test_setup.py -v
```

**What RED looks like today** is three `NotImplementedError` lines and
`3 failed`. There is no wire to look at yet — that begins on Day 8 — so today's red is a
traceback rather than a packet that never arrives.

Then implement the bodies until they pass. Then — **and this is the box people skip** — break
each one on purpose and watch it go red again:

- Change `ruff==0.16.6` to `ruff>=0.16.6`. `test_pins_are_exact` must fail. Change it back.
- Comment out the `*.pcap` line in `.gitignore`. `test_secrets_and_captures_are_ignored` must
  fail. Restore it.
- Remove `set -euo pipefail` from `m`. `test_daily_driver_is_strict` must fail. Put it back.

A test that does not go red when you break the thing it guards is not a test. It is a comment
that takes longer to run.

**And one more failure to cause deliberately** — the day's 💥 part
([4.1](parts/04-the-linux-door/4.1-namespaces-need-linux.md)):

```bash
./m lab up two-host
```

Read what it prints and record the answer in the checklist. On a machine without a Linux
kernel it reports that namespaces are unavailable and exits 1 — which is the honest state, and
blocks nothing until Day 9.

---

## §6 Lab budget

| | |
| --- | --- |
| **Tier** | **L0** — one host, user space. Stated, because `L0` is an answer (§4.1). |
| **Topology** | none. The first is `two-host`, on Day 9 (`FOUND-14`). |
| **Namespaces** | 0 |
| **Links** | 0 |
| **netem** | none |
| **Traffic generated** | none. Today fetches an installer and a package index over the public internet — a named resource, read-only and gently — and puts no packet on any wire to observe or affect another machine. |
| **Cost** | $0, as on all 152 days |

`./m lab` reports whether this machine can reach L1 at all. On the machine this day was
written on, it cannot: Git Bash on Windows 11 has no Linux kernel, and WSL is not installed.
Recorded rather than worked around (P10).

---

## §7 Traps

- **Running these commands in PowerShell.** `mkdir -p`, brace expansion, `touch`, heredocs and
  `chmod` are bash. In PowerShell they either error or do something subtly different —
  [1.2](parts/01-toolchain/1.2-git-and-the-shell.md).
- **Not reopening the terminal after installing `uv`.** A shell reads `PATH` once, at start.
  This is the most common "the installer lied to me" moment and it appears three times in this
  day — [1.1](parts/01-toolchain/1.1-why-one-tool-owns-the-environment.md).
- **Typing `pip install` out of habit.** It installs into whichever interpreter that `pip`
  belongs to, and writes nothing down —
  [1.1](parts/01-toolchain/1.1-why-one-tool-owns-the-environment.md).
- **Writing `.gitignore` after `git init` and after the first `.env`.** The ordering is not
  stylistic: an ignore rule does nothing to an already-tracked file, and a committed secret is
  disclosed rather than hidden —
  [2.2](parts/02-skeleton/2.2-gitignore-before-secrets-exist.md).
- **Committing `pyproject.toml` without `uv.lock`.** The two must move together, or your
  machine and CI build different environments from the same commit —
  [2.4](parts/02-skeleton/2.4-pyproject-and-the-lockfile.md).
- **Trusting a green test run from the editor's run button.** 🅢 **This is Silent Failure #1 —
  *the cache answered, not the network*** — in its shell-shaped form: the run succeeded, and it
  was not the run you thought. Read pytest's `platform` header line, every time, and check the
  interpreter and version match your terminal —
  [1.5](parts/01-toolchain/1.5-the-editor-and-the-interpreter-trap.md).
- **Forgetting `chmod +x m`, or forgetting to commit the bit.** Permissions belong to the file,
  not the name — [3.2](parts/03-the-driver/3.2-the-case-dispatcher.md).
- **`CRLF` line endings on `m`.** The error says `bad interpreter: No such file or directory`
  about a file that exists, because the kernel is looking for `env\r` —
  [1.2](parts/01-toolchain/1.2-git-and-the-shell.md).
- **Running `git add -A` without reading `git status --porcelain` first.** Five seconds, every
  time — [5.2](parts/05-first-commit/5.2-the-first-commit.md).
- **Ticking a box you did not do.** The gate cannot tell, which is exactly why it is worth
  nothing if you do — [3.3](parts/03-the-driver/3.3-the-done-gate.md).

---

## §8 Verify before you code

This day was written **2026-09-07**, and every version below was read live on that date (P6,
P7). Tool interfaces move; check these before you start, and if something has changed, **amend
the plan rather than working around it** (P14).

| Source | Checked | What was confirmed |
| --- | --- | --- |
| <https://docs.astral.sh/uv/> | 2026-09-07 | `uv init`, `uv add`, `uv sync`, `uv python install`, `uv run` still take these flags |
| <https://pypi.org/pypi/ruff/json> | 2026-09-07 | latest is `0.16.6` |
| <https://pypi.org/pypi/pytest/json> | 2026-09-07 | latest is `9.1.1` |
| <https://git-scm.com/download/win> | 2026-09-07 | the current Git for Windows installer, which supplies Git Bash |
| <https://docs.astral.sh/ruff/> | 2026-09-07 | `ruff check` and `ruff format --check` interfaces |
| <https://docs.pytest.org/> | 2026-09-07 | marker syntax for `-m "not root"`, and exit code 5 = no tests collected |
| local | 2026-09-07 | `git 2.54.0.windows.1`, `uv 0.12.3`, `bash 5.3.9(1)`, Python `3.12.12` under `uv` |
| local | 2026-09-07 | `wsl.exe --status` reports WSL is not installed; `command -v ip` finds nothing |

**No RFC is cited today**, and [`../../docs/SPECS.md`](../../docs/SPECS.md) is deliberately
empty. Day 0 installs tools and writes a driver; inventing a citation to look thorough is
exactly the failure P7 exists to stop.

---

## §9 Say it in an interview

> "The repository is `uv`-managed on a pinned Python 3.12, with a lockfile committed beside
> the project file, so any machine rebuilds the identical environment — every transitive
> version, with hashes. There's a three-command daily loop, and `done` physically refuses to
> commit while a checkbox is unticked, a check is red, or a `.pcap` or `.pem` is staged. That
> last one matters more than it sounds: a capture is a recording of real traffic and a
> repository's history is append-only, so a capture committed once is disclosed, not hidden —
> the repo holds what *reproduces* a capture and never the capture. And the setup day is
> honest about what the machine can't do: it runs `./m lab up` deliberately, gets
> `no network namespaces on this machine`, and records that the lab is blocked until WSL is
> installed. Writing down a capability you don't have is worth more than writing down the one
> you wish you had."

---

## §10 Done when

Every box in [`CHECKLIST.md`](CHECKLIST.md) is ticked and `./m check` is green — not when a
particular amount of effort has been spent. Then:

```bash
./m done 0
```

Day 1 builds the six ledgers and `scripts/trace.py`, and states the ethics rule that governs
every packet the next 151 days will send. It closes `OPS-01`. Run `./m status` and read
[`../../docs/TRACKER.md`](../../docs/TRACKER.md) to see how far the plan has been written out.

---

## §11 Ledger & commit

**`docs/PROGRESS.md`** — append this row verbatim:

```text
| 0 | Toolchain, skeleton and the `./m` driver | — | 18 | check green · depth green · plan green · no key or capture in git | 2026-09-07 | `day 000: complete` |
```

**`docs/PACKAGES.md`** — the rows added today (versions read live on 2026-09-07):

```text
| `ruff` | `==0.16.6` | 2026-09-07 | 0 | linter + formatter; the first two gates of `./m check` (dev group) |
| `pytest` | `==9.1.1` | 2026-09-07 | 0 | P11 needs a runner for the check that can go RED (dev group) |
| `git` | 2.54.0.windows.1 | 2026-09-07 | 0 | the repo is the memory (P2) |
| `uv` | 0.12.3 | 2026-09-07 | 0 | one owner for the environment |
| `bash` | 5.3.9(1)-release | 2026-09-07 | 0 | `./m` is a bash script; Git Bash supplies it on Windows |
| `python` | 3.12.12 (under `uv`) | 2026-09-07 | 0 | the interpreter `uv` installed and pinned |
```

**`docs/SPECS.md`** — no rows. No specification was read today, and none is invented (P7).

**`docs/TOPOLOGIES.md`** — no rows. No topology exists; the first is `two-host` on Day 9.

**`docs/CAPTURES.md`** — no rows. No capture was taken.

**`docs/MEASUREMENTS.md`** — no rows. Day 0 produces no empirical claim, and does not invent
one so the table looks started (P8, P10).

**`docs/CHANGELOG_PLAN.md`** — two amendments raised today and **not** silently worked around
(P14): **A-001**, Phase 0's gate requires `./m lab up two-host` to ping, which Day 0 cannot
satisfy because namespaces are `FOUND-14` on Day 9; and **A-002**, `CLAUDE.md` puts the lab
rebuild inside `./m check`, which needs root and Linux and would make the commit gate
unrunnable on the machine it guards. Both are open, both need an ADR.

**The commit** — written by `./m done 0`:

```text
day 000: complete
```

Day 0 closes no curriculum IDs, so the message carries no `closes` clause. From Day 1 the
format is `day NNN: <title> — closes <IDs>`.

# Day 0 — definition of done

`./m done 0` refuses to commit while any box below is unticked. That refusal is the whole
point (part [3.3](parts/03-the-driver/3.3-the-done-gate.md)) — and so is **not ticking a box
you did not do**. The gate cannot tell. Nothing here is a time estimate; a box is ticked when
the thing is true.

**Demo command — the whole day in one line:**

```bash
./m check && ./m lab && git log --oneline -1
```

---

## The parts — read, run, answer

One box per document in `parts/`. Tick it when you have read it, run its **Check yourself**
command, and answered its out-loud question *without scrolling back up*.

### Section 1 — the tools that own things

- [x] [1.1 Why one tool must own the environment](parts/01-toolchain/1.1-why-one-tool-owns-the-environment.md)
- [x] [1.2 Git, and the shell every command is written in](parts/01-toolchain/1.2-git-and-the-shell.md)
- [x] [1.3 `uv`, the one binary](parts/01-toolchain/1.3-uv-the-one-binary.md)
- [x] [1.4 Python 3.12, and why not the newest](parts/01-toolchain/1.4-python-3-12-and-not-the-newest.md)
- [x] [1.5 The editor, and the interpreter trap](parts/01-toolchain/1.5-the-editor-and-the-interpreter-trap.md)

### Section 2 — the skeleton on disk

- [x] [2.1 The folder skeleton](parts/02-skeleton/2.1-the-folder-skeleton.md)
- [x] [2.2 `.gitignore`, before anything secret exists](parts/02-skeleton/2.2-gitignore-before-secrets-exist.md)
- [x] [2.3 `git init`, and what a repository is](parts/02-skeleton/2.3-git-init-and-what-a-repo-is.md)
- [x] [2.4 `pyproject.toml` and the lockfile](parts/02-skeleton/2.4-pyproject-and-the-lockfile.md)
- [x] [2.5 The `.venv` you never activate](parts/02-skeleton/2.5-the-venv-you-never-activate.md)

### Section 3 — the driver that owns the routine

- [x] [3.1 `set -euo pipefail`](parts/03-the-driver/3.1-set-euo-pipefail.md)
- [x] [3.2 The `case` dispatcher](parts/03-the-driver/3.2-the-case-dispatcher.md)
- [x] [3.3 The `done` gate](parts/03-the-driver/3.3-the-done-gate.md)
- [x] [3.4 The depth contract, made mechanical](parts/03-the-driver/3.4-the-depth-contract-made-mechanical.md)

### Section 4 — the Linux door, and where packets are allowed to go

- [x] 💥 [4.1 Namespaces need Linux](parts/04-the-linux-door/4.1-namespaces-need-linux.md)
- [x] [4.2 The four tiers, and why Day 0 is L0](parts/04-the-linux-door/4.2-the-four-tiers.md)

### Section 5 — closing the day

- [x] [5.1 The check that must be able to go red](parts/05-first-commit/5.1-the-check-that-can-go-red.md)
- [x] [5.2 The first commit, and reading a clean tree](parts/05-first-commit/5.2-the-first-commit.md)

---

## Setup — verified on disk

Each of these is checkable by a command, and each was checked.

- [x] Git configured — `user.name`, `user.email`, `init.defaultBranch main`,
      `core.autocrlf input` (`git config --global --list`)
- [x] `uv` installed and on `PATH` in a **reopened** shell — `uv --version` reports `0.12.3`
- [x] Python 3.12 installed under `uv`, and `requires-python = "==3.12.*"` in
      `pyproject.toml` — `uv run python -V` reports `3.12.12`
- [x] Skeleton exists: `jala/{wire,stack,route,resolve,app,crypt,probe}`, `lab/`, `scripts/`,
      `tests/`, `days/`, `docs/adr/`, `.vscode/`
- [x] `.gitignore` written **before** `git init`, and it covers `.env`, `.env.*`, `*.pem`,
      `*.key`, `keys/`, `captures/`, `*.pcap`, `*.pcapng` — with `!.env.example` re-included
- [x] `git check-ignore -v .env captures/x.pcap keys/server.key` names a rule for all three
- [x] `git init` done; the repository is on `main`
- [x] `pyproject.toml` **and** `uv.lock` both exist and are committed together
- [x] Every dependency pinned with `==`: `ruff==0.16.6`, `pytest==9.1.1` — both in the `dev`
      group, both with a dated row in [`../../docs/PACKAGES.md`](../../docs/PACKAGES.md)
- [x] Runtime `dependencies = []`, deliberately — packages arrive on the day first used (P3)
- [x] `.venv/` is ignored and **never activated** — every command goes through `uv run`
- [x] `.vscode/settings.json` points at `${workspaceFolder}/.venv`, and the editor's
      interpreter string matches `uv run python -c "import sys; print(sys.executable)"`

---

## Build brief — the four files that are yours

- [x] **`m`** exists, starts with `#!/usr/bin/env bash`, and is in strict mode
      (`set -euo pipefail`)
- [x] **`m`** is executable **and the bit is committed** — `git ls-files -s m` shows mode
      `100755`, not `100644`
- [x] **`m`** dispatches `start · brief · parts · scaffold · plan · depth · trace · tracker ·
      lab · cap · check · status · done`, and a bare `./m` prints usage rather than failing
- [x] **`.gitignore`** written in the order part 2.2 gives, before `git init`
- [x] **`README.md`** written in your own words
- [x] **`tests/test_setup.py`** created from the §4 skeleton
- [x] `test_pins_are_exact` — `TODO(me)` body implemented, test passes
- [x] `test_secrets_and_captures_are_ignored` — `TODO(me)` body implemented, test passes
- [x] `test_daily_driver_is_strict` — `TODO(me)` body implemented, test passes

---

## The check that must be able to fail (P11)

- [x] Ran `uv run python -m pytest tests/test_setup.py -v` and watched all three go **RED**
      with `NotImplementedError` before implementing anything
- [x] **Broke `test_pins_are_exact` on purpose:** changed `ruff==` to `ruff>=`, watched it go
      red, changed it back
- [x] **Broke `test_secrets_and_captures_are_ignored` on purpose:** commented out the `*.pcap`
      line, watched it go red, restored it
- [x] **Broke `test_daily_driver_is_strict` on purpose:** removed `set -euo pipefail` from
      `m`, watched it go red, put it back
- [x] `./m check` is green — ruff, ruff format, lesson blocks, plan, pytest, depth
- [x] `./m depth 0` is green on its own

---

## The deliberate failure (P12) and the lab budget

- [x] **Caused the failure rather than reading about it:** ran `./m lab up two-host` and read
      the output
- [x] Recorded honestly what this machine reports. **On the machine this day was written on:**
      `FAIL no network namespaces on this machine.` — Git Bash on Windows 11, `MINGW64_NT`,
      no Linux kernel, `wsl.exe --status` says WSL is not installed. **L1 is blocked until
      WSL2 is installed; Days 0–8 are unaffected.**
- [x] `./m lab` reports namespace availability in one line
- [x] Tier for today recorded as **L0** in the hub's §6, with topology `none`, 0 namespaces,
      0 links, no netem
- [x] **Every packet this day generated stayed where it should:** today generates none. It
      fetched an installer and a package index — a named resource, read-only and gently — and
      put no packet on any wire to observe or affect another machine (§4.2)

---

## Silent failures (§6) — which one this day could have hit

- [x] **#1, the cache answered, not the network** — in its Day 0 form: a green test run
      produced by the editor's interpreter rather than the project's. **Ruled out by** reading
      pytest's `platform` header line and confirming it matches
      `uv run python -c "import sys; print(sys.executable)"` — part 1.5
- [x] Confirmed `uv run python -m pytest -q` does not silently report success on **zero**
      collected tests — pytest exits 5, and `./m check` says so out loud rather than passing

---

## Ledgers (plan §26)

- [x] [`docs/PROGRESS.md`](../../docs/PROGRESS.md) — the Day 0 row appended, verbatim from
      the hub's §11
- [x] [`docs/PACKAGES.md`](../../docs/PACKAGES.md) — six rows, each with the date the version
      was **read live** (P6)
- [x] [`docs/SPECS.md`](../../docs/SPECS.md) — **no rows**, and that is correct: no
      specification was read today and none was invented (P7)
- [x] [`docs/TOPOLOGIES.md`](../../docs/TOPOLOGIES.md) — no rows; the first topology is Day 9
- [x] [`docs/CAPTURES.md`](../../docs/CAPTURES.md) — no rows; no capture was taken
- [x] [`docs/MEASUREMENTS.md`](../../docs/MEASUREMENTS.md) — no rows; Day 0 makes no empirical
      claim and does not invent one (P8, P10)
- [x] [`docs/CHANGELOG_PLAN.md`](../../docs/CHANGELOG_PLAN.md) — **A-001** and **A-002**
      raised rather than silently worked around (P14)

---

## Budget

- [x] Namespaces: **0** · links: **0** · netem: **none** · tier: **L0**
- [x] Cost today: **$0**, as on all 152 days

---

## Commit

- [x] `git status --porcelain` **read** before staging, not after
- [x] No capture and no key is staged —
      `git status --porcelain | grep -E '\.(pcap|pcapng|pem|key)$'` returns nothing
- [x] `./m done 0` run, and it committed rather than refused
- [x] `git status --porcelain | wc -l` is **0** afterwards — a clean tree

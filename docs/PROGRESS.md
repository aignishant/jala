# 📈 PROGRESS — one row per completed day

**Append-only. The last row is where we are.** (plan §26)

A row is written by `./m done N`, after the checklist is fully ticked and `./m check` is
green — never because a day felt finished. `scripts/tracker.py` reads this file to decide
which days count as complete, and `/day-jala N` refuses to generate day N unless the last
row here is day N-1.

**The `Commit` column records the commit *message*, not its hash.** The row is written by the
same command that makes the commit, so the hash does not exist yet when the row is written —
and adding it afterwards needs an amend, which changes the hash again. The message is fixed by
`./m done N` and is a stable handle: `git log --grep='^day 000'` resolves it to a hash.

| Day | Title | IDs closed | Parts | Gates | Date | Commit |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | Toolchain, skeleton and the `./m` driver | — | 18 | check green · depth green · plan green · no key or capture in git | 2026-09-07 | `day 000: complete` |

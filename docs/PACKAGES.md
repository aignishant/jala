# 📦 PACKAGES — every install, with the date it was looked up

**Append-only.** Every package and every system tool, with the exact version, the date the
version was **read live** (never recalled — P6), the day that installed it, and why that day
needed it.

A package is added **on the day it is first used**, and — except for cryptography — only
**after** the hand-rolled version exists (P3). `scapy` does not arrive before the Ethernet
frame has been built by hand; `dnspython` does not arrive before the resolver does.

**The lookup commands**, so a row is never a guess:

```bash
curl -s https://pypi.org/pypi/<pkg>/json \
  | python -c "import sys,json;print(json.load(sys.stdin)['info']['version'])"
<tool> --version          # for a system tool from the distribution
```

## Python packages

| Package | Version | Looked up | Day | Why this day needed it |
| --- | --- | --- | --- | --- |
| `ruff` | `==0.16.6` | 2026-09-07 | 0 | linter + formatter; the first two gates of `./m check` (dev group) |
| `pytest` | `==9.1.1` | 2026-09-07 | 0 | P11 needs a runner for the check that can go RED (dev group) |

There are **no runtime dependencies yet**, and that is the point. `jala/` is written by hand
from the day documents; the first runtime pin arrives on the day a library is first compared
against something already built (P3).

## System tools — from the distribution, never a download (plan §5)

| Tool | Version | Read on | Day | Why |
| --- | --- | --- | --- | --- |
| `git` | 2.54.0.windows.1 | 2026-09-07 | 0 | the repo is the memory (P2) |
| `uv` | 0.12.3 | 2026-09-07 | 0 | one owner for the environment |
| `bash` | 5.3.9(1)-release | 2026-09-07 | 0 | `./m` is a bash script; Git Bash supplies it on Windows |
| `python` | 3.12.12 (under `uv`) | 2026-09-07 | 0 | the interpreter `uv` installed and pinned |

**Not yet installed, and named here so the gap is visible rather than forgotten:** `ip`
(iproute2), `ss`, `tcpdump`, `tshark`, `dig`, `nft`, `tc`, `socat`. Every one of them is
Linux-only and arrives with the lab. See
[`days/day-000-toolchain-skeleton-driver/parts/04-the-linux-door/4.1-namespaces-need-linux.md`](../days/day-000-toolchain-skeleton-driver/parts/04-the-linux-door/4.1-namespaces-need-linux.md).

#!/usr/bin/env python
"""Parse every Python code block in every lesson, and fail on one that does not compile.

Why this is a separate gate. `ruff format` reaches into Python fences inside Markdown, but
it **fails open** on a block it cannot parse: an unparseable block is simply skipped, and a
lesson with a syntax error in it is green everywhere in the repository. That is the exact
shape of a silent failure, so it gets its own check that fails CLOSED.

This compiles; it never executes. A block that is deliberately incomplete — a fragment, a
`TODO(me)` skeleton, a snippet with an ellipsis — marks itself with the info string
`python-fragment` and is skipped, so the day can still show a shape without pretending it
is a whole program.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SEARCH = ["days", "docs"]

FENCE = re.compile(r"^(\s*)```(\S*)\s*$")
COMPILED_LANGS = {"python", "py"}


def blocks(path: Path) -> list[tuple[int, str, str]]:
    """(start line, language, body) for every fenced block in one document."""
    out: list[tuple[int, str, str]] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        m = FENCE.match(lines[i])
        if not m:
            i += 1
            continue
        indent, lang = m.group(1), m.group(2).lower()
        start = i + 1
        body: list[str] = []
        i += 1
        while i < len(lines) and not FENCE.match(lines[i]):
            body.append(lines[i][len(indent) :] if lines[i].startswith(indent) else lines[i])
            i += 1
        out.append((start, lang, "\n".join(body)))
        i += 1
    return out


def main() -> int:
    problems: list[str] = []
    checked = 0
    skipped = 0

    for top in SEARCH:
        base = ROOT / top
        if not base.is_dir():
            continue
        for md in sorted(base.rglob("*.md")):
            for start, lang, body in blocks(md):
                if lang == "python-fragment":
                    skipped += 1
                    continue
                if lang not in COMPILED_LANGS or not body.strip():
                    continue
                checked += 1
                try:
                    compile(body, f"{md.name}:{start}", "exec")
                except SyntaxError as exc:
                    rel = md.relative_to(ROOT).as_posix()
                    line = start + (exc.lineno or 1) - 1
                    problems.append(
                        f"  FAIL {rel}:{line}\n"
                        f"       python block does not compile: {exc.msg}\n"
                        f"       If the block is a deliberate fragment, fence it as "
                        f"```python-fragment"
                    )

    for p in problems:
        print(p)
    if problems:
        print(f"\nFAIL lesson blocks: {len(problems)} of {checked} python block(s) do not compile")
        return 1
    print(f"OK lesson blocks: {checked} python block(s) compile ({skipped} fragment(s) skipped)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

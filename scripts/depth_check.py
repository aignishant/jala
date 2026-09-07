#!/usr/bin/env python
"""The machine-readable half of the depth contract (plan §24.10).

Run as `./m depth [NNN]` - one day, or every written day. It fails on everything §24.10
lists: a missing `parts/`, a misnamed folder, a numbering gap, a missing or misordered part
section, an unexplained code block, a header with no wire format, an L1 part with no
topology, traffic with no named namespaces, a bad `level` or `tier`, a reader-directed time
estimate, a hub that teaches, and a missing checklist.

What it cannot check is whether an explanation is any good. That is §24.9, and it is
reviewed by reading.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DAYS = ROOT / "days"

# --- the contract ---------------------------------------------------------------------

# §24.4: the nine unconditional part sections, in contract order. Frontmatter is the tenth
# and is checked separately because it is not a heading.
PART_SECTIONS: list[str] = [
    "One-line answer",
    "The story",
    "The idea in plain language",
    "Why Jāla needs it",
    "The mechanism",
    "When it breaks",
    "In production",
    "Check yourself",
]

# The two conditional sections, and where they are allowed to sit in the order above.
# Wire format and Topology follow "The mechanism"; both are optional.
CONDITIONAL_AFTER_MECHANISM = ["Wire format", "Topology"]

# §24.5: the hub's required sections, in order.
HUB_SECTIONS: list[str] = [
    "§1 Where we are",
    "§2 The map",
    "§3 Setup — run this",
    "§4 Build brief",
    "§5 The check that must be able to fail",
    "§6 Lab budget",
    "§7 Traps",
    "§8 Verify before you code",
    "§9 Say it in an interview",
    "§10 Done when",
    "§11 Ledger & commit",
]

PART_FRONTMATTER_KEYS = [
    "day",
    "part",
    "title",
    "ids",
    "level",
    "tier",
    "prerequisites",
    "prev",
    "next",
]
HUB_FRONTMATTER_KEYS = [
    "day",
    "phase",
    "phase_name",
    "title",
    "ids",
    "principles",
    "kind",
    "plan_version",
    "parts",
    "tier",
    "topology",
    "generated",
    "status",
    "lab_scaffolded",
    "commit",
]

LEVELS = {"foundation", "working", "production"}
TIERS = {"L0", "L1", "L2", "L3"}

# Fence languages that carry code a reader must have walked through. Everything else -
# text, mermaid, console output, a capture excerpt, a diagram - is exempt by §24.4 rule 9.
CODE_LANGS = {"bash", "sh", "shell", "python", "py", "c"}

# §24.4 rule 9 exempts "error output, a bare check command, a capture excerpt or a
# diagram". Those live in these two sections, so blocks inside them need no walkthrough.
WALKTHROUGH_EXEMPT_SECTIONS = {"When it breaks", "Check yourself"}

# §24.10: any reader-directed time estimate, anywhere in a day folder. These patterns are
# deliberately aimed at estimates pointed at the reader's schedule - "should take about an
# hour", "a quick 20-minute detour", "duration: 2h". A MEASURED duration is data and is
# required by this curriculum (an RTT, an RTO, a TIME_WAIT, a netem setting, a p99), so
# nothing here matches a bare number with a time unit. A false positive on a measured
# duration is a bug in this checker, not a reason to delete the number (§24.1).
CLOCK_PATTERNS: list[tuple[str, str]] = [
    (
        r"^\s*(?:duration|estimated_hours|est_hours|time_estimate|pace|effort)\s*:",
        "a duration key in frontmatter",
    ),
    (
        r"\b(?:should|will|might|may|can)\s+take\s+(?:you\s+)?(?:about|around|roughly|approx\w*|~)?\s*\d",
        "a 'should take N' estimate",
    ),
    (
        r"\btakes?\s+(?:about|around|roughly|approx\w*)\s+\d+\s*(?:min|hour|hr|day|week)",
        "a 'takes about N' estimate",
    ),
    (
        r"\b(?:spend|allow|budget|set aside|give it)\s+(?:about\s+)?\d+"
        r"\s*[-\s]?(?:min|hour|hr|day|week)",
        "a 'spend N minutes' instruction",
    ),
    (
        r"\b\d+\s*-\s*(?:minute|hour)\s+(?:read|detour|exercise|lesson|session|sitting)\b",
        "an 'N-minute read' label",
    ),
    (
        r"\b(?:quick|brief|short)\s+(?:detour|aside|read|look)\b",
        "a 'quick detour' - a pace signal (§24.10)",
    ),
    (
        r"\bin\s+(?:about|around|roughly)\s+\d+\s*(?:minutes?|hours?)\b",
        "an 'in about N minutes' estimate",
    ),
    # "per day" alone is NOT a clock: "one day, one commit" (P2) and "one commit per day"
    # are statements about the unit of work, not about the reader's schedule. Only a
    # quantity of TIME per day is a pace - "two hours per day" tells the reader how fast to
    # go, which is the thing P17 bans.
    (
        r"\b\d+(?:\.\d+)?\s*(?:hours?|hrs?|minutes?|mins?)\s+(?:per|a|each)\s+day\b",
        "a daily pace in hours",
    ),
]

# Commands that put a packet on a wire. §4.2: every part that generates traffic names the
# namespaces it stays inside.
#
# Two lists, because the plan draws the line in two different places. PROBE commands measure
# or interrogate somebody else's machine - they are the ones §4.2 is actually about, and they
# have no business in an L0 part at all, because L0 is one host in user space. FETCH commands
# retrieve a named resource; §4.2 permits them explicitly at L2, "read-only and gently", and
# `curl -LsSf <installer> | sh` on a setup day is not probing anyone.
#
# Both lists are matched against CODE BLOCKS ONLY, never prose. A part is supposed to be able
# to discuss a ping without being accused of sending one; what matters is what the reader is
# instructed to run.
PROBE_COMMANDS = [
    r"\bping6?\b",
    r"\btraceroute6?\b",
    r"\btracepath\b",
    r"\biperf3?\b",
    r"\bhping3?\b",
    r"\bnmap\b",
    r"\barping\b",
    r"\bnping\b",
    r"\bmtr\b",
    r"\bsendp?\(",
    r"\bsr1?\(",
    r"\bsrp1?\(",
]

FETCH_COMMANDS = [
    r"\bcurl\b",
    r"\bwget\b",
    r"\bdig\b",
    r"\bnslookup\b",
    r"\bncat\b",
    r"\bsocat\b",
]

# A part that shows a header talks about offsets and field widths. If it does that and has
# no `## Wire format`, §24.10 says it has created a bug it will not be around to fix.
HEADER_HINTS = [
    r"\bbyte\s+offset\b",
    r"\boffsets?\s+\d",
    r"\bbytes?\s+\d+\s*[-–]\s*\d+\b",
    r"\bbig-endian\b",
    r"\blittle-endian\b",
    r"\bheader\s+field\b",
    r"\bint\.from_bytes\(",
    r"\bstruct\.unpack\(",
]


@dataclass
class Problem:
    path: Path
    detail: str
    line: int | None = None

    def __str__(self) -> str:
        where = f"{self.path.relative_to(ROOT).as_posix()}"
        if self.line is not None:
            where += f":{self.line}"
        return f"  FAIL {where}\n       {self.detail}"


@dataclass
class Doc:
    """A markdown document, split once into the pieces every rule needs."""

    path: Path
    text: str
    frontmatter: dict[str, str] = field(default_factory=dict)
    body_start: int = 0

    @classmethod
    def load(cls, path: Path) -> Doc:
        text = path.read_text(encoding="utf-8")
        doc = cls(path=path, text=text)
        lines = text.splitlines()

        # YAML frontmatter: a --- fence on line 1, closed by the next --- .
        if lines and lines[0].strip() == "---":
            for i, line in enumerate(lines[1:], start=1):
                if line.strip() == "---":
                    doc.body_start = i + 1
                    break
                if ":" in line and not line.startswith((" ", "\t", "-")):
                    key, _, value = line.partition(":")
                    doc.frontmatter[key.strip()] = value.strip()
        return doc

    def h2s(self) -> list[str]:
        """Level-2 headings, in order - the sections the contract names."""
        out: list[str] = []
        in_fence = False
        for line in self.text.splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            m = re.match(r"^##\s+(.*)$", line)
            if m:
                out.append(m.group(1).strip())
        return out

    def code_blocks(self) -> list[tuple[int, str, str, str]]:
        """(start line, language, body, enclosing ## section) for every fenced block."""
        out: list[tuple[int, str, str, str]] = []
        lines = self.text.splitlines()
        section = ""
        i = 0
        while i < len(lines):
            line = lines[i]
            m = re.match(r"^##\s+(.*)$", line)
            if m:
                section = m.group(1).strip()
            fence = re.match(r"^\s*```(\w*)", line)
            if fence:
                lang = fence.group(1).lower()
                start = i + 1
                body: list[str] = []
                i += 1
                while i < len(lines) and not lines[i].lstrip().startswith("```"):
                    body.append(lines[i])
                    i += 1
                out.append((start, lang, "\n".join(body), section))
            i += 1
        return out

    def prose(self) -> str:
        """Everything outside fenced code blocks - what the clock rule reads."""
        out: list[str] = []
        in_fence = False
        for line in self.text.splitlines():
            if line.lstrip().startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                out.append(line)
        return "\n".join(out)


# --- the individual rules -------------------------------------------------------------


def check_clocks(doc: Doc, problems: list[Problem]) -> None:
    """§24.10: no reader-directed time estimate anywhere in a day folder (P17)."""
    in_fence = False
    for n, line in enumerate(doc.text.splitlines(), start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for pattern, why in CLOCK_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                problems.append(Problem(doc.path, f"clock (P17): {why} - {line.strip()!r}", n))


def check_frontmatter(doc: Doc, keys: list[str], problems: list[Problem]) -> None:
    if not doc.frontmatter:
        problems.append(Problem(doc.path, "no YAML frontmatter"))
        return
    missing = [k for k in keys if k not in doc.frontmatter]
    if missing:
        problems.append(Problem(doc.path, f"frontmatter missing keys: {missing}"))


def check_part_sections(doc: Doc, problems: list[Problem]) -> None:
    """§24.10: the nine unconditional sections, present and in contract order."""
    found = doc.h2s()
    missing = [s for s in PART_SECTIONS if s not in found]
    if missing:
        problems.append(Problem(doc.path, f"missing required section(s): {missing}"))
        return

    positions = [found.index(s) for s in PART_SECTIONS]
    if positions != sorted(positions):
        out_of_order = [s for s in found if s in PART_SECTIONS]
        problems.append(
            Problem(
                doc.path,
                f"sections out of contract order.\n       contract: {PART_SECTIONS}\n"
                f"       found:    {out_of_order}",
            )
        )

    # The two conditional sections sit between "The mechanism" and "When it breaks".
    mech, breaks = found.index("The mechanism"), found.index("When it breaks")
    for cond in CONDITIONAL_AFTER_MECHANISM:
        if cond in found and not (mech < found.index(cond) < breaks):
            problems.append(
                Problem(
                    doc.path,
                    f"'{cond}' must sit between 'The mechanism' and 'When it breaks' (§24.4)",
                )
            )


def check_level_and_tier(doc: Doc, problems: list[Problem]) -> str:
    level = doc.frontmatter.get("level", "").strip().strip("\"'")
    tier = doc.frontmatter.get("tier", "").strip().strip("\"'")
    if level and level not in LEVELS:
        problems.append(Problem(doc.path, f"level {level!r} is not one of {sorted(LEVELS)}"))
    if tier and tier not in TIERS:
        problems.append(Problem(doc.path, f"tier {tier!r} is not one of {sorted(TIERS)}"))
    return tier


def check_walkthroughs(doc: Doc, problems: list[Problem]) -> None:
    """§24.10: a code block with no `Line by line:` walkthrough following it."""
    lines = doc.text.splitlines()
    for start, lang, body, section in doc.code_blocks():
        if lang not in CODE_LANGS:
            continue
        if section in WALKTHROUGH_EXEMPT_SECTIONS:
            continue
        if not body.strip():
            continue
        # Find the closing fence, then look at the next handful of non-blank lines.
        i = start
        while i < len(lines) and not lines[i].lstrip().startswith("```"):
            i += 1
        window = "\n".join(lines[i + 1 : i + 8])
        if "Line by line:" not in window:
            problems.append(
                Problem(
                    doc.path,
                    f"a {lang} block in '{section or '(no section)'}' has no "
                    f"`**Line by line:**` walkthrough after it (§24.4 rule 9)",
                    start,
                )
            )


def check_wire_format(doc: Doc, problems: list[Problem]) -> None:
    """§24.10: a part that shows a header but carries no `## Wire format`."""
    if "Wire format" in doc.h2s():
        return
    prose = doc.prose()
    hits = [p for p in HEADER_HINTS if re.search(p, prose, re.IGNORECASE)]
    # Two independent hints, so a passing mention of "big-endian" is not enough to demand
    # a whole table. A part that really parses a header trips several of these.
    if len(hits) >= 2:
        problems.append(
            Problem(
                doc.path,
                f"shows header/offset detail ({hits[:3]}) but has no `## Wire format` "
                f"section (§24.4 item 7, P20)",
            )
        )


def check_topology(doc: Doc, tier: str, problems: list[Problem]) -> None:
    """§24.10: an L1/L2 part with no `## Topology`, and traffic with no namespaces."""
    has_topology = "Topology" in doc.h2s()
    if tier in {"L1", "L2"} and not has_topology:
        problems.append(
            Problem(doc.path, f"tier {tier} but no `## Topology` section (§24.4 item 8, P9)")
        )

    # Code blocks only. A part may discuss a ping in prose without being accused of
    # sending one; what §4.2 governs is what the reader is instructed to run.
    #
    # Markdown table rows are dropped even inside a code block. A ledger row appended with
    # a heredoc - "| M-001 | 72 | two-host | ... | iperf3 3.16 | ..." - names a tool as
    # DATA, recording what was once run; it does not run anything. Reading those as
    # commands accuses every MEASUREMENTS.md and CAPTURES.md example of generating traffic.
    runnable = "\n".join(
        line
        for _, lang, body, _ in doc.code_blocks()
        if lang in CODE_LANGS or lang == ""
        for line in body.splitlines()
        if not line.lstrip().startswith("|")
    )
    probes = sorted({p for p in PROBE_COMMANDS if re.search(p, runnable)})
    fetches = sorted({p for p in FETCH_COMMANDS if re.search(p, runnable)})

    if probes and tier == "L0":
        problems.append(
            Problem(
                doc.path,
                f"tier L0 but a code block runs a probe ({probes[:3]}). L0 is one host in "
                f"user space - either the tier is wrong or the packet is (§4.1)",
            )
        )
    if (probes or fetches) and tier == "L1" and "netns" not in doc.text:
        problems.append(
            Problem(
                doc.path,
                f"generates traffic ({(probes + fetches)[:3]}) at tier L1 but never names a "
                f"namespace. Every part that generates traffic names its namespaces (§4.2)",
            )
        )


def check_relative_links(doc: Doc, problems: list[Problem]) -> None:
    """A dead relative link is what catches a half-finished rename."""
    for m in re.finditer(r"\[[^\]]*\]\(([^)#\s]+\.md)(?:#[^)]*)?\)", doc.text):
        target = m.group(1)
        if target.startswith(("http://", "https://", "/")):
            continue
        line = doc.text[: m.start()].count("\n") + 1
        if not (doc.path.parent / target).resolve().exists():
            problems.append(Problem(doc.path, f"dead relative link: {target}", line))


def check_hub_does_not_teach(doc: Doc, problems: list[Problem]) -> None:
    """§24.5: the hub carries no walkthrough, no wire-format table, no topology diagram."""
    # Headings are read from the parsed heading list, not by substring search: a hub's §2
    # map legitimately *names* `## Wire format` and `## Topology` inside a table cell when
    # describing what a part contains, and accusing it of carrying the section would teach
    # authors to stop naming the contract in the map.
    for banned, why in (
        ("Wire format", "a `## Wire format` table"),
        ("Topology", "a `## Topology` diagram"),
    ):
        if banned in doc.h2s():
            problems.append(
                Problem(doc.path, f"the hub carries {why} - that belongs in a part (§24.5)")
            )
    # A walkthrough has no heading, so this one stays a substring check.
    if "Line by line:" in doc.text:
        problems.append(
            Problem(
                doc.path,
                "the hub carries a `Line by line:` walkthrough - that belongs in a part (§24.5)",
            )
        )


# --- walking a day --------------------------------------------------------------------


def check_day(day_dir: Path, problems: list[Problem]) -> int:
    """Check one day folder. Returns the number of parts found."""
    name = day_dir.name
    if not re.fullmatch(r"day-\d{3}-[a-z0-9]+(?:-[a-z0-9]+)*", name):
        problems.append(
            Problem(
                day_dir,
                f"day folder must be day-NNN-<slug>, three digits and a kebab slug "
                f"(§24.2) - got {name!r}",
            )
        )

    lesson = day_dir / "LESSON.md"
    checklist = day_dir / "CHECKLIST.md"
    parts_dir = day_dir / "parts"

    if not lesson.exists():
        problems.append(Problem(day_dir, "no LESSON.md"))
        return 0
    if not checklist.exists():
        problems.append(Problem(day_dir, "no CHECKLIST.md (§24.10)"))
    if not parts_dir.is_dir():
        problems.append(
            Problem(day_dir, "no parts/ directory - a day without one is not written (§24.2)")
        )
        return 0

    # The checklist is a day-folder document, so the clock rule applies to it too.
    if checklist.exists():
        check_clocks(Doc.load(checklist), problems)

    # --- the hub ---
    hub = Doc.load(lesson)
    check_frontmatter(hub, HUB_FRONTMATTER_KEYS, problems)
    check_clocks(hub, problems)
    check_hub_does_not_teach(hub, problems)
    check_relative_links(hub, problems)

    hub_h2 = hub.h2s()
    missing = [s for s in HUB_SECTIONS if s not in hub_h2]
    if missing:
        problems.append(Problem(lesson, f"hub missing section(s): {missing} (§24.5)"))
    else:
        pos = [hub_h2.index(s) for s in HUB_SECTIONS]
        if pos != sorted(pos):
            problems.append(Problem(lesson, "hub sections are out of contract order (§24.5)"))

    # --- section folders ---
    section_dirs = sorted(d for d in parts_dir.iterdir() if d.is_dir())
    loose = [f for f in parts_dir.iterdir() if f.is_file() and f.suffix == ".md"]
    for f in loose:
        problems.append(
            Problem(f, "a part is loose in parts/ instead of inside a section folder (§24.2)")
        )

    seen_sections: list[int] = []
    part_files: list[Path] = []

    for sd in section_dirs:
        m = re.fullmatch(r"(\d{2})-[a-z0-9]+(?:-[a-z0-9]+)*", sd.name)
        if not m:
            problems.append(
                Problem(
                    sd,
                    f"section folder must be NN-<slug>, two zero-padded digits and a "
                    f"kebab slug (§24.2) - got {sd.name!r}",
                )
            )
            continue
        section_no = int(m.group(1))
        seen_sections.append(section_no)

        files = sorted(f for f in sd.iterdir() if f.suffix == ".md")
        subtopics: list[int] = []
        for f in files:
            fm = re.fullmatch(r"(\d+)\.(\d+)-[a-z0-9]+(?:-[a-z0-9]+)*\.md", f.name)
            if not fm:
                problems.append(
                    Problem(f, "filename must be <section>.<subtopic>-<slug>.md (§24.10)")
                )
                continue
            if int(fm.group(1)) != section_no:
                problems.append(
                    Problem(
                        f,
                        f"lives in section folder {section_no:02d} but its number says "
                        f"section {fm.group(1)} (§24.2)",
                    )
                )
            subtopics.append(int(fm.group(2)))
            part_files.append(f)

        if subtopics and sorted(subtopics) != list(range(1, len(subtopics) + 1)):
            problems.append(
                Problem(
                    sd,
                    f"subtopic numbering must start at 1 with no gaps (§24.3) - "
                    f"got {sorted(subtopics)}",
                )
            )

    if seen_sections and sorted(seen_sections) != list(range(1, len(seen_sections) + 1)):
        problems.append(
            Problem(
                parts_dir,
                f"section numbering must start at 1 with no gaps (§24.3) - "
                f"got {sorted(seen_sections)}",
            )
        )

    # --- each part ---
    for f in sorted(part_files):
        doc = Doc.load(f)
        check_frontmatter(doc, PART_FRONTMATTER_KEYS, problems)
        check_clocks(doc, problems)
        check_part_sections(doc, problems)
        tier = check_level_and_tier(doc, problems)
        check_walkthroughs(doc, problems)
        check_wire_format(doc, problems)
        check_topology(doc, tier, problems)
        check_relative_links(doc, problems)

    # --- the hub's map must link every part on disk, and the count must agree ---
    for f in part_files:
        rel = f.relative_to(day_dir).as_posix()
        if rel not in hub.text:
            problems.append(Problem(lesson, f"hub §2 map does not link {rel} (§24.10)"))

    declared = hub.frontmatter.get("parts", "").strip().strip("\"'")
    if declared.isdigit() and int(declared) != len(part_files):
        problems.append(
            Problem(
                lesson,
                f"frontmatter says parts: {declared} but {len(part_files)} are on disk (§24.10)",
            )
        )

    return len(part_files)


def main() -> int:
    if not DAYS.is_dir():
        print("no days/ directory yet - nothing to check")
        return 0

    wanted = sys.argv[1] if len(sys.argv) > 1 else None
    day_dirs = sorted(d for d in DAYS.iterdir() if d.is_dir() and d.name.startswith("day-"))
    if wanted is not None:
        n = f"{int(wanted):03d}"
        day_dirs = [d for d in day_dirs if d.name.startswith(f"day-{n}")]
        if not day_dirs:
            print(f"FAIL no day folder for day {int(wanted)}")
            return 1

    if not day_dirs:
        print("no days written yet - nothing to check")
        return 0

    problems: list[Problem] = []
    total_parts = 0
    for d in day_dirs:
        total_parts += check_day(d, problems)

    for p in problems:
        print(p)

    if problems:
        print(f"\nFAIL depth contract: {len(problems)} problem(s) across {len(day_dirs)} day(s)")
        return 1

    print(f"OK depth contract: {len(day_dirs)} day(s), {total_parts} parts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

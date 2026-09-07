#!/usr/bin/env bash
# Project Jala daily driver. `make` is not used here (plan §5) - this is the one entry point.
#
# Three commands carry the routine for 152 days: ./m start N, ./m check, ./m done N.
# Everything else exists so those three can stay honest.
set -euo pipefail

cd "$(dirname "$0")"

DAY="${2:-}"
pad() { printf "%03d" "$1"; }

# Day folders are days/day-NNN-<slug> (plan §24.2), so the slug is free text and the NUMBER
# is the only stable handle - glob on it. That is what lets a folder be renamed to a better
# slug without breaking ./m, depth_check.py, tracker.py or trace.py.
daydir() {
  local n d
  n="$(pad "$1")"
  for d in days/day-"$n"-*; do
    [ -d "$d" ] && { echo "$d"; return; }
  done
  echo ""
}

# The lab is Linux-only: network namespaces have no macOS or Windows equivalent, and the
# plan says to say so rather than pretend (§4). This answers "can this machine do L1 at all".
have_netns() { command -v ip >/dev/null 2>&1 && ip netns list >/dev/null 2>&1; }

case "${1:-help}" in
  start)
    [ -z "$DAY" ] && { echo "usage: ./m start <day>"; exit 1; }
    D="$(daydir "$DAY")"
    [ -n "$D" ] || { echo "no lesson written yet for day $DAY"; exit 1; }
    echo "-> open $D/LESSON.md"
    ;;

  brief)
    # The day's working set, projected out of the plan instead of read from it whole.
    # A projection may replace a lookup; it may never replace a judgement. Plan §24, §6
    # and §4.2 are still read in full before writing a day.
    [ -z "$DAY" ] && { echo "usage: ./m brief <day>"; exit 1; }
    uv run python scripts/day_brief.py "$DAY"
    ;;

  parts)
    [ -z "$DAY" ] && { echo "usage: ./m parts <day>"; exit 1; }
    D="$(daydir "$DAY")"
    [ -n "$D" ] || { echo "no lesson written yet for day $DAY"; exit 1; }
    for S in "$D"/parts/*/; do
      [ -d "$S" ] || continue
      echo "$(basename "$S")"
      for F in "$S"*.md; do [ -f "$F" ] && echo "    $(basename "$F")"; done
    done
    ;;

  scaffold)
    [ -z "$DAY" ] && { echo "usage: ./m scaffold <day>"; exit 1; }
    D="$(daydir "$DAY")"
    [ -n "$D" ] || {
      echo "no folder for day $DAY yet - write the day first (/day-jala $DAY)."
      echo "day folders are days/day-$(pad "$DAY")-<slug>, never bare days/day-$(pad "$DAY")."
      exit 1
    }
    mkdir -p "$D/lab"
    echo "-> created $D/lab"
    ;;

  plan)
    # P19: the day count is DERIVED. This is where it is derived, so the number in the
    # plan's frontmatter is an output rather than a claim. --emit also rewrites the
    # generated tables; the bare check never writes anything.
    uv run python scripts/plan_check.py "${2:-}"
    ;;

  depth)
    if [ -n "$DAY" ]; then uv run python scripts/depth_check.py "$DAY"
    else uv run python scripts/depth_check.py; fi
    ;;

  trace)
    # scripts/trace.py is Day 1's build brief - the learner writes it. Until then this
    # says so out loud rather than passing silently, because a check that quietly does
    # nothing is worth less than no check (P10).
    if [ -f scripts/trace.py ]; then
      uv run python scripts/trace.py
    else
      echo "WARN scripts/trace.py not written yet - it is Day 1's build brief (OPS-01)"
    fi
    ;;

  tracker)
    uv run python scripts/tracker.py
    # Both files are projections of the same tree, so they are regenerated together.
    # Letting one be refreshed without the other is how a generated file starts lying.
    uv run python scripts/parts_index.py
    ;;

  lab)
    # L1 - the virtual lab. Every topology is a committed, idempotent script with a row in
    # docs/TOPOLOGIES.md (plan §4). "up" run twice must be clean; that is the whole test.
    SUB="${2:-}"; NAME="${3:-}"
    case "$SUB" in
      up)
        [ -z "$NAME" ] && { echo "usage: ./m lab up <topology>"; exit 1; }
        # Namespaces first, then the script. "this machine cannot host L1 at all" is the
        # more fundamental fact, and reporting the missing script first would send a reader
        # off to write a topology they still could not run (P10 - fail honestly).
        have_netns || { echo "FAIL no network namespaces on this machine."
                        echo "     L1 needs Linux. Native Linux, WSL2 on Windows, or a Linux VM."
                        echo "     macOS and Windows have no namespace equivalent (plan §4)."; exit 1; }
        [ -f "lab/$NAME.sh" ] || { echo "FAIL no lab/$NAME.sh - a topology built by typing"
                                   echo "     fourteen commands is one you cannot rebuild (§4)"; exit 1; }
        bash "lab/$NAME.sh"
        ;;
      down)
        have_netns || { echo "FAIL no network namespaces on this machine (plan §4)"; exit 1; }
        # Only namespaces this repo created. Never a blanket delete.
        if [ -f lab/down.sh ]; then bash lab/down.sh
        else echo "FAIL no lab/down.sh yet - it arrives with the first topology (Day 9)"; exit 1; fi
        ;;
      verify)
        # The idempotence proof (OPS-03), and the reason it is NOT part of ./m check:
        # it needs root and it needs Linux. Wiring it into `check` would make the gate that
        # guards every commit unrunnable on the machine it is meant to guard - and would
        # turn "I am on a laptop without sudo" into a red build. They answer different
        # questions: `check` asks "is this correct", `lab verify` asks "does this topology
        # still rebuild from its script".
        [ -z "$NAME" ] && { echo "usage: ./m lab verify <topology>"; exit 1; }
        "$0" lab down || true
        "$0" lab up "$NAME"
        "$0" lab up "$NAME"
        echo "OK $NAME rebuilt twice with no error - it is idempotent (OPS-03)"
        ;;
      *)
        echo "usage: ./m lab <up|down|verify> [topology]"
        have_netns && echo "  namespaces: available" || echo "  namespaces: NOT available (L1 blocked)"
        ;;
    esac
    ;;

  cap)
    # Captures are regenerated, never committed (P9). This writes into captures/, which is
    # gitignored; the provenance row goes in docs/CAPTURES.md by hand, same day.
    TOPO="${2:-}"; IFACE="${3:-}"; NAME="${4:-}"
    [ -z "$NAME" ] && { echo "usage: ./m cap <topology> <iface> <name>"; exit 1; }
    have_netns || { echo "FAIL no network namespaces on this machine (plan §4)"; exit 1; }
    mkdir -p captures
    echo "-> capturing on $IFACE in netns $TOPO into captures/$NAME.pcap"
    echo "   remember the docs/CAPTURES.md row, including the credential check (SEC-22)"
    ip netns exec "$TOPO" tcpdump -i "$IFACE" -w "captures/$NAME.pcap" -s 0
    ;;

  check)
    # Order matters. The three gates that READ code without running it come first, cheapest
    # first, because nothing should execute until everything has been read.
    uv run ruff check .
    uv run ruff format --check .
    uv run python scripts/check_blocks.py
    uv run python scripts/plan_check.py

    # pytest exits 5 when it collected nothing. Until the first day writes a test that is
    # the honest state of the repo, not a failure - but it is said out loud, because a
    # silently empty test run is exactly how P11 rots. Every other exit code is fatal.
    set +e
    uv run python -m pytest -q -m "not root"
    PYTEST=$?
    set -e
    if [ "$PYTEST" -eq 5 ]; then
      echo "WARN pytest collected no tests yet (P11: every day ends with a check that can go RED)"
    elif [ "$PYTEST" -ne 0 ]; then
      exit "$PYTEST"
    fi

    uv run python scripts/depth_check.py
    "$0" trace
    echo "OK all green"
    ;;

  status)
    uv run python scripts/tracker.py --summary
    ;;

  done)
    [ -z "$DAY" ] && { echo "usage: ./m done <day>"; exit 1; }
    D="$(daydir "$DAY")"
    [ -n "$D" ] || { echo "no day folder for $DAY"; exit 1; }
    C="$D/CHECKLIST.md"
    if grep -q '^- \[ \]' "$C"; then
      echo "FAIL unticked boxes remain in $C"
      grep -n '^- \[ \]' "$C"
      exit 1
    fi
    # P9, checked on every single day and not once a phase, because the day it fails is
    # the day it became permanent.
    if git status --porcelain | grep -Eq '\.(pcap|pcapng|pem|key)$'; then
      echo "FAIL a capture or a key is staged. Never (P9):"
      git status --porcelain | grep -E '\.(pcap|pcapng|pem|key)$'
      exit 1
    fi
    "$0" check
    "$0" tracker
    git add -A && git commit -m "day $(pad "$DAY"): complete"
    echo "OK day $DAY committed"
    ;;

  *)
    cat <<'USAGE'
usage: ./m <command> [args]

  start N            point at day N's lesson
  brief N            print day N's working set - its IDs, phase, gate, and the ledger tails
  parts N            list day N's sections and their part documents
  scaffold N         create the lab/ folder inside day N's folder

  plan [--emit]      verify the ID decomposition; the day count is an OUTPUT (P19)
  depth [N]          run the depth contract over day N, or every written day
  trace              regenerate docs/TRACEABILITY.md (Day 1 writes scripts/trace.py)
  tracker            regenerate docs/TRACKER.md, docs/CURRICULUM_INDEX.md, days/INDEX.md

  lab up <topo>      build a topology from its committed script
  lab down           tear down the namespaces this repo created
  lab verify <topo>  down, up, up - the idempotence proof (OPS-03). Needs root + Linux.
  cap <topo> <if> <n>  capture on a link. Captures are gitignored; provenance is not (P9).

  check              ruff + format + lesson blocks + plan + offline pytest + depth + trace
  status             one-line progress
  done N             refuse unless the checklist is ticked and check is green, then commit
USAGE
    ;;
esac

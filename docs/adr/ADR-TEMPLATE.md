# ADR-NNNN — <the decision, as a short statement>

- **Status:** proposed | accepted | superseded by ADR-NNNN
- **Date:** YYYY-MM-DD
- **Day:** the day number this arose on
- **Affects:** the plan sections, ledgers or scripts this changes

## Context

What is actually true that made this a decision rather than a default. Name the constraint:
an RFC that was obsoleted, a kernel default that changed, a day that turned out to hold two
ideas, a tool that removed a flag. **Cite it** — an RFC number and section, a `sysctl` read
off a named kernel, a release note. P14 exists because the alternative is a plan that
quietly stops describing the repository.

## Decision

One paragraph, in the present tense, saying what is now the case.

## Consequences

What this costs, not only what it buys. Include the day count if it moved — P19 says 152 is
an **output**, so a day that splits moves the number and that is the plan working, not the
plan failing.

- **Ledgers to update:** `docs/CHANGELOG_PLAN.md` always; others as they apply.
- **Days already written that this invalidates:** list them, or say "none".

## Alternatives considered

Each with the reason it lost. An ADR whose alternatives section is empty is a decision that
was never actually made.

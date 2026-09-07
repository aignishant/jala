"""Day 0: prove the setup is real, rather than assumed.

Three claims made on Day 0, each checkable by reading a file. All three are L0 - no
namespace, no socket, no network - which is plan §5's constraint (tests are unprivileged,
deterministic and offline) satisfied on the first day rather than promised for later.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _dependency_specs(text: str) -> list[str]:
    """Every quoted dependency specification in pyproject.toml.

    The specs are the quoted strings inside the `dependencies` list and inside each list
    in `[dependency-groups]`. Parsing the TOML properly would need a dependency, and on
    Day 0 there is not one - so this reads the two list literals directly.
    """
    specs: list[str] = []
    for block in re.findall(
        r"^\s*(?:dependencies|dev)\s*=\s*\[(.*?)]", text, re.DOTALL | re.MULTILINE
    ):
        specs.extend(re.findall(r'"([^"]+)"', block))
    return specs


def test_pins_are_exact() -> None:
    """Every dependency uses == and not a range (P6)."""
    text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    specs = _dependency_specs(text)

    # The dev group must be populated; an empty runtime `dependencies` list is deliberate
    # on Day 0 (packages arrive on the day they are first used, P3), so the assertion is
    # that we found the specs we do have - not that there are many.
    assert specs, "no dependency specifications found in pyproject.toml"

    for spec in specs:
        assert "==" in spec, f"{spec} is not an exact pin (P6: never invent a version)"
        for loose in (">=", "<=", "~=", "^", ">", "<"):
            bare = spec.replace("==", "")
            assert loose not in bare, f"{spec} carries a range operator {loose!r}"


def test_secrets_and_captures_are_ignored() -> None:
    """.env, keys and captures are ignored BEFORE they exist (P9).

    The repository holds what *reproduces* a capture, never the capture - so this checks
    the networking-specific half as seriously as the credential half.
    """
    text = (ROOT / ".gitignore").read_text(encoding="utf-8")
    rules = {line.strip() for line in text.splitlines() if line.strip()}

    for required in (
        ".env",
        ".env.*",
        "*.pem",
        "*.key",
        "keys/",
        "captures/",
        "*.pcap",
        "*.pcapng",
    ):
        assert required in rules, f".gitignore has no rule for {required} (P9)"

    assert "!.env.example" in rules, ".env.example must be re-included so the shape is committed"

    # Order matters: a `!` rule only re-includes if it comes AFTER the rule that excluded
    # it. A .gitignore listing them the other way round is silently wrong.
    lines = [line.strip() for line in text.splitlines()]
    assert lines.index(".env") < lines.index("!.env.example"), (
        "!.env.example must come after .env, or it does not re-include anything"
    )


def test_daily_driver_is_strict() -> None:
    """./m exists, is bash, and is in strict mode (part 3.1)."""
    m = ROOT / "m"
    assert m.exists(), "./m does not exist - it is Day 0's build brief"

    text = m.read_text(encoding="utf-8")
    lines = text.splitlines()

    assert lines[0].startswith("#!"), "./m has no shebang"
    assert "bash" in lines[0], f"./m is not a bash script: {lines[0]!r}"

    # A CRLF line ending here produces `bad interpreter: No such file or directory` about
    # a file that plainly exists, because the kernel looks for `env\r` (part 1.2).
    assert "\r" not in text, "./m has CRLF line endings - the shebang will not resolve"

    # Match the line, not the substring. A commented-out `# set -euo pipefail` contains
    # the text and does nothing at all - and a substring check passes it, which is a hole
    # this test had until the deliberate break in part 5.1 exposed it.
    strict = any(line.strip() == "set -euo pipefail" for line in lines[:10])
    assert strict, (
        "./m is not in strict mode - without it a failed gate does not stop the script "
        "and `check` can print OK after a failure (part 3.1)"
    )

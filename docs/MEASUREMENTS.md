# 📊 MEASUREMENTS — every number this curriculum is allowed to quote

**Append-only.** A number with no row here is a rumour (P8). Every row carries the topology,
the netem settings, the **seed**, the **repetition count**, the tool and its version, a
hardware line, and the result **with its spread**.

**One run is not a measurement.** Five seeds minimum, warm-up discarded, transfer longer
than slow start, and p50 / p95 / p99 reported with the spread — never the best run. That is
Silent Failure #4 (§6), and a single-repetition row is that failure with a table around it.

**"No significant difference" is a result and gets a row** (P10). An optimisation that made
throughput worse says so, in this table, in the same words it would have used if it had won.

**Before writing a row, name which of the five silent failures you ruled out and how.** A
throughput number taken from a warm cache, over loopback, through a middlebox that rewrote
the flow, is a number about none of the things you think it is about.

| ID | Day | Topology | netem | Seed | Reps | Tool + version | Hardware | Result (with spread) | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

Nothing has been measured yet. Day 0 installs tools and writes a driver; it produces no
empirical claim, and it does not invent one so this table can look started.

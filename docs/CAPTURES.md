# 🎣 CAPTURES — the provenance, never the bytes

**Append-only.** `*.pcap`, `*.pcapng` and `captures/` are gitignored. **The repo holds what
*reproduces* a capture, never the capture itself** (P9) — so every row carries enough to
regenerate it, and every row records whether it has been **checked for credentials**
(`SEC-22`).

A capture of your own lab holds your own traffic. A capture taken anywhere else holds
somebody else's. That is why the credential column is not optional and why the answer is
never assumed: a capture of an HTTP exchange from before TLS existed carries the password in
plain text, and a capture is forever once it is committed.

| File | Topology | Capture point | Filter | Snaplen | Tool + version | Date | Day | Credential-checked |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

No capture has been taken yet. `./m cap <topology> <iface> <name>` writes into the ignored
`captures/` directory and prints the reminder that the row above is written by hand, the
same day.

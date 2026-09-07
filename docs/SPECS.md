# 📜 SPECS — every specification, read before it was quoted

**Append-only.** A row goes in **before** the spec is quoted in a day, never after (P7).

Every row records whether the document is **obsoleted**, because a citation to a superseded
RFC points a reader at replaced text. The info page shows an "Obsoleted by" line when it
applies:

```bash
curl -s https://www.rfc-editor.org/info/rfcNNNN     # status + obsoleted-by
curl -s https://www.rfc-editor.org/rfc/rfcNNNN.txt  # the document itself
```

**The three that catch people out.** TCP is **RFC 9293**, not 793. CUBIC is **RFC 9438**,
not 8312. HTTP/1.1 is **RFC 9112** (messaging) plus **RFC 9110** (semantics), which between
them replaced RFC 7230. A day quoting a section number from the superseded document sends
its reader to text that no longer says what the day claims.

| Number | Title | Status | Obsoletes / obsoleted by | Sections read | Resolved | Day |
| --- | --- | --- | --- | --- | --- | --- |

No specification has been read yet. Day 0 quotes none — it installs tools and writes a
driver, and inventing a citation to look thorough is exactly the failure P7 exists to stop.
The first rows arrive in Phase 1.

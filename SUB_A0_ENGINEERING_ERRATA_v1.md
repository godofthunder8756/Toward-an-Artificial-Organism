# SUB-A0 engineering errata v1

2026-10-02. Additive correction; original execution source, manifest, traces,
checkpoints and results are preserved.

## Trace hash semantics on Windows

The original runner records `trace_sha256` while emitting UTF-8 JSON rows with
LF newlines, BEFORE Python's text writer translates newlines. On Windows the
saved files contain CRLF. Consequently the recorded hash is the **LF-normalized
trace-content hash**, not the SHA-256 of physical on-disk bytes.

The first independent byte-hash audit failed on this distinction. Inspection
confirmed 1,024 CRLF rows per file; replacing CRLF by LF reproduces every
original recorded hash. Fresh graph replay also reproduces the LF hashes.
This is a provenance/format-definition defect, not a mismatch of predictions,
writes, scores or traces. It was investigated before interpreting the audit.

The additive [auditor](sub_a0_v1/audit.py) explicitly verifies the original
LF-normalized hashes and separately records physical byte hashes. Its
[regressions](sub_a0_v1/test_audit.py) distinguish newline translation from
actual content corruption. No saved file is normalized or overwritten.
Future execution formats should explicitly label byte versus canonical
content hashes and avoid platform-dependent writer translation.

## Scope

No scientific endpoint, seed, fault dose, learning budget or stopping rule
changes. No fit is repeated. Seed 1 remains NOT_RUN under the prospective
no-write STOP. Original source hashes remain replayable.

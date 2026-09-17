# AC75 results v1: erase-on-relinquish makes the reconciled closure world-accommodating

2026-09-17. Final seeds 2900–2903 (4 seeds × 2 histories = 8 individuals per condition), hashed protocol
`AC75_PROTOCOL_v1.md`, 16,384 ticks. Engineering seeds (0–2) excluded. **All eight predeclared gates pass.**

## Gate outcomes

| gate | statement | result |
| --- | --- | --- |
| G1 | `erase` survives a permanent move in all 8 | **PASS** (8/8) |
| G2 | `erase` survives a temporary outage (two transitions) in all 8 | **PASS** (8/8) |
| G3 | `erase` re-acquires the moved route and holds both in all 8 | **PASS** (8/8, `route1` correct, `demand=[42,0]`) |
| G4 | `erase` register intact in all 8 (perm and temp) | **PASS** (8/8, `[F,F,F,F]`) |
| G5 | `restore` (no erase) fails under change | **PASS** (8/8 dead under both perm and temp) |
| G6 | repair stays load-bearing (`erase_no_repair` dies) | **PASS** (8/8, deaths 403–792) |
| G7 | inert without change (`erase` ≡ `restore`, zero relinquishments) | **PASS** (exact `state_hash` equality) |
| G8 | completeness and determinism | **PASS** (96 rows; re-run exact) |

## The measured arms (8 individuals per condition)

| arm | perm | temp | none |
| --- | --- | --- | --- |
| `erase` | survive 8/8, both routes 8/8, register intact | survive 8/8, both routes 8/8 | survive 8/8, both routes 8/8, 0 relinquish |
| `restore` | **die 8/8** (8439–8449) | **die 8/8** (8439–8449) | survive 8/8, both routes 8/8, 0 relinquish |
| `erase_no_repair` | die 8/8 (403–792) | die 8/8 | die 8/8 |
| `restore_no_repair` | die 8/8 (403–792) | die 8/8 | die 8/8 |

The `erase` arm is the only configuration that survives *and* holds both routes through a post-development
change; the no-erase rival dies 8/8 under both a permanent move and a temporary outage. The temporary
outage is the sharpest test: the organism relinquishes and re-acquires **twice** (mean 2.0
relinquishments), and still ends with both routes held.

## What the result is, and what it is not

**Establishes:** a single mechanism change — erase the entry on relinquishment — closes the
AC74 cascade. The reconciled closure (AC71's majority read + load-bearing repair, joined to AC16's
deposit-open + restore rule) is **world-accommodating** over the declared transition family: it preserves
and reconstructs its acquired function through permanent and temporary environmental change, keeps its
body and decision state intact, stays inert in the unchanged world, and keeps the repair loop causally
necessary. This is the first result in the line where the closure survives *change* at the long horizon,
not just a fixed world.

**The mechanism is legitimate, not a rescue:** the erase is triggered only by the organism's own
relinquishment decision (its own failure streak), writes through its own vulnerable program bank, and
books the entry as expired exactly as the frozen decay law does — no privileged information, no external
rescue, no new conservation violation. It generalizes across the transition family (perm and temp), which
is the test for a mechanism rather than a case-specific patch.

**Does not establish:** autopoiesis (the controller is still externally supplied and only maintained, not
produced — see `DEPENDENCY_AUDIT_v1.md`); generality beyond the two-route, one-move, graded-yield world;
anything about consciousness. The endpoint is behavioural and economic (survival + route holding), not a
claim about the controller's own production.

## Verification

`audit_ac75.py` passes (96 rows, 12 source hashes no drift, all eight gates recomputed without
simulating); `replay_ac75.py` **6/6 exact**; `test_ac75.py` 5 tests green; full AC core suite **306 tests
pass**. Verification tools are deliberately not hashed (AC17's rule).

## Artifacts

`ac75.py`, `AC75_PROTOCOL_v1.md`, `ac75_results_v1/`, `test_ac75.py`, `audit_ac75.py`, `replay_ac75.py`.
Related: `AC74_ENGINEERING_v1.md` (the cascade), `AC75_ENGINEERING_v1.md` (the diagnostic panel),
`AC71_RESULTS_v1.md` (the fixed-world closure), `DEPENDENCY_AUDIT_v1.md` (the structural gap this does
*not* close).

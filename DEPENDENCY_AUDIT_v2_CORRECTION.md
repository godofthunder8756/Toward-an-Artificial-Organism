# Dependency audit v2 — correction (K2, charter v2 reclassification)

2026-09-22. This corrects `DEPENDENCY_AUDIT_v2.md` against `DEFINITIONS_CHARTER_v2.md`.
It is a derived, definitional correction — no study was re-run, no frozen row, hash, or
ledger was touched. It supersedes v2's §5 (evidence matrix) and §7 (gap list) only; the
inventory (§2) and the code trace (Sources) remain valid.

## What was wrong in v2

v2's §5 asserted C2 (production/replacement) for C5 (pointer), C6 (coordination state),
C7 (route memory) and C8 (decision memory) by listing their update/repair operations
(`write_pointer` + `reg_pointer`; `write_ctrl` + timer + `reg_ctrl`; deposit + renew;
`_drop`/`_restore`/`gray_streak_write` + bank-0 repair). None of those is "re-made from
other maintained state" — the charter's own C2 definition. That was assertion, not
verification (the exact failure the K2 card names). Charter v2 corrects the classification:
C5/C6/C7/C8 are **maintained state** (internalized, vulnerable, paid-maintained), not
**components** (constraints whose realization turns over).

## Corrected evidence matrix (§5 replacement)

Components (C2/C3/C4/C5 apply):

| Component | C1 existence | C2 production/replacement | C3 within-network dep. | C4 content boundary | C5 on a cycle |
| --- | --- | --- | --- | --- | --- |
| C1 W | `life[:16]` | action 6 births (turnover) | live W parent (autocatalytic) + program C9 | inherited endowment, replaced endogenously | yes (C4→C9→W→C4; W→W) |
| C2 C | `life[16:20]` | action 7 births | live W parent + program C9 | inherited, replaced | yes (C9→C→energy→C9; W→C→energy→W) |
| C3 B | `boundary[20]` | action 8 births, B_expiry | live W anchor + program C9 | inherited, replaced | yes (W→B→W via retention) |
| C4 description | bank-1 slots | succession copy→verify→switch→remove | W (catalysis) + pointer C5 + coordinator C6 + own content | content inherited (permitted) | yes (C4→C9→W→C4) |
| C9 program | `traces[0,:126]` | derived from C4 (reconstruction) | C4 + W | content inherited (C4) | yes (C4→C9) |

Maintained state (S1–S4 apply; C2 does NOT — no turnover is claimed or required):

| Item | Realized by | Operations (update/repair) | Clause |
| --- | --- | --- | --- |
| C5 pointer | `traces[1,520:522]` | `write_pointer`/`commit_switch` (update); `reg_pointer` (repair) | S1–S4 |
| C6 coordination | `traces[1,522:540]` | `write_ctrl` MODE, `reset_timer`/`increment_timer`, `write_rip` (update); `reg_ctrl` (repair) | S1–S4 |
| C7 route memory | `mem.Memory` | deposit (content acquisition), renewal (refresh) | S1–S4 (+ acquisition) |
| C8 decision memory | dead-rule free bits | `_drop`/`_restore` (register update), `gray_streak_write` (counter update); bank-0 repair | S1–S4 |

**Network re-verified.** The five components form a single strongly-connected
mutual-constraint network (details in `CLOSURE_CRITERION_CONSISTENCY_v1.md` §3): C4→C9→W→C4;
C9→C→(energy)→C9; W→B→W (retention). No external root inside the substrate convention. The
network criterion is satisfied; the *verdict* remains K3's to issue and remains conditional
on J1 (substrate classification) and J4 (retention vs spatial unity).

## Corrected gap list (§7 replacement)

1. **J1** — unchanged and decisive: `advance()` and `prog.choose` are supplied; if
   organism-specific functions, the criterion fails on them. v2 sharpens it: this now
   concerns the *mechanism* only; the coordinator *state* (C6) and pointer (C5) are
   maintained state, not components.
2. **J2/J3** — unchanged ("format-level" is asserted, not demonstrated; content-supply
   boundary is a judgment).
3. **Decision-state economics** — unchanged and *reclassified*: it is now explicitly a
   **state-integrity** robustness limit (S1–S4), not a production/closure gap. The
   allowance-42 rule's seed-dependence bounds the level-(b) decision claim; it does not bear
   on whether any component is produced.
4. **J5 (observation layer)** — unchanged; bears on levels (c)/(d), not closure.

v2's residual gaps that depended on counting C5/C6/C8 as produced components are withdrawn:
there was never a production edge to verify for them, so there is no production gap. The
honest statement is that their status is **maintained state**, established by S1–S4, and that
their *mechanisms* (`advance()`, `prog.choose`, and the deposit/decision logic) are the
supplied/process side of the J1/J3 boundary — not a separate failure.

## Supplied operations: they supply DIFFERENT amounts of organization (SCOPE item)

Two fixed functions are supplied as substrate (J1), and the ledger must not treat them as
one category — they supply different amounts of organization:

- **`prog.choose` (a rule interpreter).** A fixed ISA: reads the mutable 126-bit program bank,
  matches a rule word's mask against the observation, returns the action; falls through to
  action 9 (`ac5_program.py:33-41`). It supplies the *semantics of rule-matching* and nothing
  else. The *content* — which action follows which observation — lives entirely in the derived
  program (C9), which the organism re-builds from C4. A passive interpreter is the closest
  analog to a law (like the decode format); its concession to "substrate" is small.
- **`advance()` (a prescribed succession procedure).** A fixed sequence machine:
  copy → verify → switch → remove (`ac95.py:607-725`), including the *verify gate* (switch
  only after the successor decodes syntactically valid AND matches the source). It supplies a
  *specific multi-step procedure with a built-in correctness check*, not a generic primitive.
  Its concession to "substrate" is larger: the verify gate is precisely the kind of
  always-available functional service the AC90 review flagged. This is why J1's decisive
  question bites hardest on `advance()`, less on `prog.choose`.

Both remain supplied substrate under the accepted convention (the ledger records, does not
resolve, J1). But a verdict that treats them as equally "format-level" would be understating
the concession `advance()` represents.

## Charter discrepancies (carried, now fixed in charter v2)

- C5 offset `[520,521]` (not AC86's 312–313) — fixed in charter v2 §7b.
- C6 shape MODE + W-funded timer + RIP (not MODE/LAST) — fixed in charter v2 §7b.
- C8 = two sub-states (register + Gray streak) — fixed in charter v2 §7b.

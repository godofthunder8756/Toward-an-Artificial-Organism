# AC107 results v1 — the maintained cause-estimate confirms on discrimination, but the causal-role and survival-advantage do not transfer (K6)

2026-09-22. Frozen confirmatory run of the K5 mechanism (`ac107.py`, engineering seeds 0-7,
`AC107_ENGINEERING_v1.md`) on the untouched final family **6000-6007** (8 seeds × 2 histories =
16 individuals), 240 rows, protocol `AC107_PROTOCOL_v1.md` (hashed in `pre_run_snapshot.json`
before any final seed ran). Audit (`audit_ac107.py`) re-derives the gates and source hashes from
the saved table without simulating; replay (`replay_ac107.py`) reproduces 15 sampled rows and the
first-row determinism re-run exactly.

Verdict: **partial confirmation.** The four questions are answered separately below. Q1
(discrimination) and Q3 (storage maintenance) confirm; Q2 (content causal) and Q4 (comparative
advantage) do not transfer to the fresh family.

---

## 1. Q1 — the estimate discriminates the relevant causes: CONFIRMED

- `cut`: e reads E_machinery (0) at the window end in **16/16** individuals (entry bound at cut
  start, so the cut was experienced).
- `move`: e reads E_world (1) at the first drop in **16/16** individuals.
- post-intervention mistakes: **0** across all 32 individuals.

The discriminator is a direct consequence of the K4-identifiable observation triple, and it
transfers to the untouched family unchanged. This is the strongest result of the freeze.

## 2. Q2 — the estimate's content causally influences decisions: NOT ESTABLISHED on finals

The read-only `scramble` (writes intact, read forced E_world) does **relinquish in `cut` where the
candidate holds** — seeds 6001 and 6006 (4 individuals: scramble relinquishes ≥1, candidate holds
0) — so the read of the maintained bit is *behaviourally* causal.

But the **survival** consequence did not transfer: `scramble` survives `cut` **16/16** (as does
`r2`), so G2's death clause is **vacuously false**. On engineering seed 4 (priority `[3,0,2,1]`,
the renewal-last corner) r2's in-window relinquishment was fatal; none of the final seeds
6000-6007 has that priority (final priorities: `[3,2,1,0] [2,1,3,0] [0,3,1,2] [3,0,1,2]
[3,2,1,0] [2,0,3,1] [0,2,3,1] [0,1,2,3]`), so on the fresh family a mid-cut relinquishment is
recoverable (the route is still valid; a blind re-bind re-acquires it). The cut bites r2's
behaviour (relinquishes on 6001/6002/6006) but not its survival.

G2 (as prespecified, requiring a scramble death) **FAILS**; the behavioural causality is recorded
as a separate measurement, not a moved gate.

## 3. Q3 — maintaining its storage sustains that function: CONFIRMED (storage-content sense)

- G3 state sufficiency: observer-discard per-tick byte-identical on the candidate in `cut` for
  **16/16** — the estimate value is read from the vulnerable maintained state, not host state.
- G4 no-cause identity: candidate == r2 (`state_hash`) in `no_cause` for **16/16** — the estimate
  is inert absent a cause, so its maintenance does not perturb the organism when unused.
- Vulnerable-storage audit: the estimate bit lives in the sticky program damage stream, is written
  by the paid W-gated `bel_write`, and is excluded from `reg_from_active`.

Scope note (carried from the protocol, not hidden): the maintenance is a **single paid write** at
cause-onset (measured `bel_writes == 7`, one attempt), and the decision window (96 ticks) is short
relative to the sticky damage rate, so an ongoing-repair loop is **not exercised** (the AC13 wall).
"Maintenance sustains function" holds in the sense that the function depends on the maintained
storage's *content*; ongoing *repair* of that storage is not load-bearing here and is not claimed.

## 4. Q4 — the advantage survives credible rivals: PARTIAL, seed-bounded

Survival, per arm and condition, finals 6000-6007 (16 individuals each):

| arm | cut (E_machinery) | move (E_world) |
|---|---|---|
| candidate | 16/16 | **14/16** (dies 6002) |
| r2 (streak 6) | 16/16 (relinquishes on 6001/6002/6006, survives) | 16/16 |
| r4 (counter 24) | 16/16 | **10/16** (dies 6002, 6003, 6007) |
| r1 (reactive) | 16/16 | 16/16 |
| scramble | 16/16 | (≡ r2) |

- **Cut:** no survival advantage — r2 survives 16/16, so the candidate's hold buys no survival
  difference on this family (only a relinquish-churn avoidance: candidate 0 vs r2 3 seeds).
- **Move:** real but seed-bounded advantage. The candidate survives where r4 dies on 6003 and 6007
  (drop-fast beats hold-too-long), but on **6002 both die** — the candidate correctly reads
  E_world, drops at 8235, re-acquires at 8241, and still collapses at 8441, while r4 holds and dies
  at 8447. Only r1 (drop at the first failure) survives 6002. So on 6002 the correct decision
  (drop) is made, but at the frozen streak threshold 6 it is too slow; the economy had already
  fixed the outcome (the AC83/AC74 pattern, in the weaker "too late" form).

G5 **FAILS**: the r2-cut death clause is vacuous (r2_cut deaths = []) and the candidate's own
move-survival is seed-bounded (14/16, with a both-die seed).

## 5. Gates (recorded, not moved)

| gate | result |
|---|---|
| G1 discrimination | **PASS** |
| G2 content causal (scramble death) | FAIL (vacuous; behavioural causality present) |
| G3 state sufficiency | **PASS** |
| G4 no-cause identity | **PASS** |
| G5 comparative advantage | FAIL (vacuous cut + seed-bounded move) |
| G6 completeness/determinism | **PASS** (240 rows, determinism re-run) |
| G7 rival distinctness | **PASS** |

## 6. Claim discipline

- The strongest wording earned: "**a maintained one-bit cause-estimate, updated from the organism's
  own (bound, used_held, productive) history, discriminates the two causes at decision times with
  zero mistakes on an untouched seed family, and the discrimination depends on the maintained
  storage's content (state sufficiency, no-cause identity).**"
- The estimate's **survival value is not established on the fresh family**: the read-cut does not
  produce a survival difference, and the route-move advantage is seed-bounded (a both-die seed).
- No level-(d) claim, no metacognition claim, no autopoiesis claim. Seeds are the replication unit;
  engineering seeds 0-7 are excluded from this sample (AC39, in the unfavourable direction here).

## 7. What this hands downstream

- **K8 (reliability monitoring):** the estimate is *too accurate to vary* — 0 mistakes on finals.
  K8's prerequisite ("meaningful variation in accuracy") is not met by this mechanism; the estimate
  has no errors for a reliability state to predict. The K8 worker should assess this explicitly
  (block with reopening conditions unless a mechanism change introduces error variance).
- **K7 (cognitive-organizational coupling):** the mechanism is real and maintained, so the two
  coupling directions can be tested, but the representation's survival-value is seed-bounded —
  coupling claims must not rest on a survival contrast that only bites on priority-corner seeds.
- **K9 (synthesis):** the maintained-representation result is a *representational-function +
  storage-maintenance* positive with a *survival-advantage* negative on fresh data; neither the
  "estimate is causally load-bearing" nor the "estimate beats rivals" claim transfers.

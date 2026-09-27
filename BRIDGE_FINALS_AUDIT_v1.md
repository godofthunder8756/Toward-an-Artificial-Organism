# N12 — Independent audit and adversarial reduction of the N11 bridge finals

2026-09-26. Deliverable of the N12 card (t_db7e0b42): *does the saved data
survive an independent audit and adversarial reduction?* No retraining, no
re-freezing — this is a read-only audit of `bridge/finals_v1/` plus a
first-principles attempt to reduce the one positive result to a rival.

The audit is reproducible: `PYTHONPATH=. OPENBLAS_NUM_THREADS=1
.venv-bridge/bin/python -B bridge/audit_finals_v1.py` re-runs every check
below and exits 0 (14/14 PASS). That script is a verification tool, not part
of the frozen source set; it reimplements the sign-flip test independently of
`bridge/exact_stats.py`.

---

## 0. Verdict

**The saved data survives the audit; the positive result survives reduction
only as a necessary-condition claim about the substrate, and the allocation
half is fully reducible — exactly as N11 recorded.** The conclusion N11 froze
("explicit maintained V was unnecessary in this task") is independently
confirmed; nothing in the audit licenses a stronger or a resurrected claim.

One headline, unchanged by this audit: **active paid persistence is confirmed**
— future-task information depends on a representation whose retention is paid
per tick, and is unrecoverable without it. That claim is *narrow* (a
necessary-condition / free-permanence fact) and survives every reduction
attempted. It is **not** a claim that the candidate's learned *allocation* is
causal or unique, and the audit finds the allocation half is reducible to a
3-line sufficient-statistic rule.

---

## 1. Audit (saved-data integrity)

| Item | Result |
| --- | --- |
| Coverage | 192 rows = 16 arms x 12 seeds, one row per (seed, arm) cell, no missing/extra cells |
| Seeds | 2000-2011 (N=12), disjoint from engineering {0,1,2} |
| Arm counts | 16 arms: candidate, no_maintenance, free_memory, oracle, arm9_d, arm9_nod, arm10_P_rb, arm7_reward, arm8_multi, fixed_p{1,2,4,8,16,32,64} |
| Parameter hashes | All 13 frozen sources intact (sha256 snapshot == on-disk), verification tools correctly excluded |
| Checkpoint provenance | 48 checkpoints = 4 trained arms x 12 seeds, no gaps; spot reload (candidate + arm10, seed 2000) reproduces the recorded rows field-for-field (survival 0.008646 exact) |
| Independence unit | Seeds are the replication unit (N=12 in the sign-flip test); 2048 eval episodes per seed are repeated measures aggregated to a mean |
| Raw-to-summary | All four sign-flip p-values re-derive exactly: G-N1 = 2/2^12 = 0.000488, G3b = 2/2^10 = 0.001953 (2 ties dropped), N3c = 0.6445 (5 pos/7 neg), d_t-read = 1.0 (12 ties) |
| Interventions | W-intervention (force-hold -> probe 1.0, force-drop -> chance) and V-intervention (A's P(refresh) depends on V's code, mean |dP| = 0.19/0.15) present and consistent |
| Teacher leakage | None into the allocation: V reads only (v_prev, h_prev, (E,d)); A reads only (v, s); reward reaches S_pol only (G3c: g_joint == g_alone). V **is** teacher-supervised on (E,d) — that is the N6 collapse, disclosed, not leakage into A |
| Cue leakage | None: S_pol reads (W, x_t) only (S4), x_t is i.i.d. and c-independent, cue enters only at t=0 via the W write |
| Resource accounting | Well-defined ledger: earn 0.2/correct tick, spend 0.1 proc + 1.0 refresh, budget 2.0, death at E <= 0. Candidate over-spends ~3.5x the oracle (refresh 0.22 vs 0.062) for the same cue |

Two findings the audit adds (details in §3):

- **F1 — the `free_memory` arm is redundant with `no_maintenance`.** Both run
  `action_never`; `free_memory` additionally sets `write_cue=False`. Either way
  the slot reads 0 at the probe, so both record exactly 0.000 slot survival in
  every seed (verified identical to 1e-12). The arm as *measured* does not test
  "hidden recurrent memory" — it runs no GRU at all. The free-permanence claim
  in fact rests on the **S4 architecture** (S_pol reads only (W, x_t), x_t
  c-independent), which is real and verifiable in code but is a *structural*
  fact, not something the `free_memory` arm measures. The claim is sound; the
  control is a no-op relative to `no_maintenance`.

- **F2 — N1 (paid persistence) is not unique to the candidate.** Fixed
  schedules `fixed_p8`/`fixed_p16` (state-blind) and the reward-only arm 7 all
  hold the cue through paid refresh (stable slot 1.0). N1's correct, irreducible
  content is the *necessary-condition* statement — without paid maintenance the
  cue is unrecoverable (no_maintenance and free_memory both 0.000) — which is a
  substrate+architecture fact. It is **not** evidence that the candidate's
  learned behavior is causal or distinctive.

---

## 2. Adversarial reduction

The one positive result is N1 (candidate 0.978 vs no_maintenance 0.000,
p at floor). Each reduction attempted in turn:

1. **Ordinary RL (arm 7, probe-reward RL, same capacity).** Holds the cue
   (slot 1.0) but over-refreshes (0.505) and dies (survival 0.05). It does
   **not** reproduce the candidate (which survives at 0.815). The candidate is
   not "just ordinary RL" — but note arm 7 *also* achieves paid persistence, so
   N1 alone does not separate the candidate from ordinary RL; the separation is
   survival/conservation (N3b), which fails strict dominance.

2. **Supervised integrity prediction.** **CONFIRMED reducible.** V is
   teacher-forced by L_V on the measured (E_t, d_t); V's integrity bit is a
   learned re-encoding of the readable age `d_t` (I_t = f(d_t), N6). The
   candidate's "internal state" carries no information beyond the observable.

3. **Direct control policy / sufficient statistic (arm 9_d).** **CONFIRMED
   reducible, above the candidate.** The 3-line threshold rule
   `refresh iff s=stable and E>=E_crit and d>=L-1` attains the oracle (op 1.0)
   in every seed, strictly above the candidate (op 0.895, median gap -0.026).
   The candidate's entire allocation is reproduced by a hand-coded rule on the
   raw observable.

4. **Fixed schedule (state-blind family).** Every level scores op 0.5 (holds in
   both regimes or neither); the candidate is regime-dependent (op 0.895) in
   10/12 seeds. So the *regime-conditional* allocation is not reducible to a
   fixed level — but it **is** reducible to arm 9_d, and the candidate does not
   strictly dominate (2/12 collapse to over-refresh and die, AC39/AC68).

5. **Hidden recurrent memory (free_memory).** Ruled out **structurally** (S4 +
   c-independence), not by the measurement (F1).

6. **Parameter-count advantage.** Arms 7/8/10 share the candidate's GRU body and
   optimizer budget; the candidate demonstrates no advantage over P_rb/arm 9_d
   anyway, so no parameter-count confound can be invoked to save it.

7. **Optimization advantage.** Same Adam, same budget and objective family for
   the trained rivals; arm 9_d needs no optimization at all and wins. No
   optimization advantage.

8. **Reward shaping / task-clock exploitation.** G3c (reward adds zero gradient
   to A), G3d (homeostatic cost survival-blind), and the clock/generalization
   control (announce +/-8, delay 48, horizon 80 -> slot survival 0.97-1.00) all
   pass. One disclosed knife-edge: arm9_nod's phase-0 clock coincides with the
   countdown deadline, so the d_t-read necessity measures 0.0 — the age read's
   necessity is fragile (a phase-aligned fixed clock reproduces it), which is
   itself the N6 point that d_t is a readable counter, not a latent.

9. **Sufficient statistic (already covered, item 3).**

10. **Supervised integrity prediction / direct control (already covered).**

**No positive interpretation is invented.** Every positive component is either
(1) the substrate-level necessary condition of paid persistence, or (2) reducible
to a rival that reads the same raw bookkeeping. The audit confirms the recorded
conclusion verbatim: explicit maintained V was unnecessary in this task.

---

## 3. What this hands N13

- The frozen data is auditable and reproducible (`bridge/audit_finals_v1.py`,
  14/14 checks). Source hashes, checkpoint provenance, seeds, arm counts, and
  statistics are all independently verifiable.
- The only load-bearing positive is **N1: active paid persistence** (necessary
  condition, free-permanence), correctly bounded. It is a substrate/architecture
  result, not a learned-behaviour result.
- The allocation half (N3a/N3b/N3c) is **not** supported and is reducible to
  the (s,E,d) sufficient statistic — the N6/N7 identifiability collapse,
  confirmed empirically rather than assumed.
- Two audit findings to carry: (F1) `free_memory` is measurement-redundant with
  `no_maintenance`; the free-permanence claim is structural (S4), and any future
  "hidden recurrent memory" control must actually run the recurrence with W
  zeroed rather than a no-GRU fixed policy. (F2) paid persistence is shared by
  state-blind fixed schedules; do not later cite N1 as evidence the *learned
  allocator* is load-bearing — it is not, and nothing here says it is.

Claim ceiling: active paid persistence confirmed; no inferred-integrity,
autopoiesis, subjectivity, or consciousness claim is made, implied, or
supported by this data.

# Phase-III independent audit + adversarial reduction — G14

2026-09-27. Deliverable for the G14 card (t_97f6430a): *do the raw artifacts
reproduce the results, and do the reductions (A–F) survive?* This is an
independent re-derivation of the G13 frozen finals
(`phase3_results_finals_v1`) — I recomputed the frozen artifacts from scratch and
did not rely on the G13 worker's own cross-check.

Verdict up front: **the results reproduce byte-for-byte and the frozen
statistical plan is applied correctly, but the reductions substantially bound
the claim.** The candidate is the *worst* of six arms on raw inference accuracy;
its content is a scalar sufficient statistic that the fixed analytic rival (R4)
matches for free; and the one genuinely measured, discriminating advantage over
the strongest non-shared rival is narrow (coordination + maintenance economy vs
R1). The causal/identity gates are largely satisfied *by construction*, not by a
measured behavioral contrast against the rivals.

---

## Part 1 — Recomputation and verification

All recomputation used the frozen `.venv-bridge` interpreter, CPU-only
(`CUDA_VISIBLE_DEVICES=`), from the repo root.

### 1.1 What reproduces (verified independently)

- **Source hashes.** sha256 of all eleven frozen sources (`phase3/config.py`,
  `task.py`, `model.py`, `specialists.py`, `arms.py`, `train.py`,
  `interventions.py`, `novel_consumer.py`, `leakage.py`, `runner.py`) and
  `ACI_PHASE3_PROTOCOL_v1.md` match `pre_run_snapshot.json` exactly. **No
  post-final edit to any frozen code or the protocol.**
- **State hash.** `sha256(sorted rows)` recomputed = recorded
  `6327948ce71fd2badfbbc9182239dfcadfa02d5fa3ae23e2ed403303ca6beff1` (match).
- **Coverage.** 72 rows = 6 arms × 12 seeds {100…111}, no missing arm/seed
  (planned-denominator complete).
- **Seed partition.** Engineering 0–7 and finals 100–111 are disjoint (config
  §11); the finals dir contains only 100–111. Correct.
- **Replay.** Seeds 100, 107, 111 re-trained from scratch and re-evaluated:
  all three **BYTE-IDENTICAL** to the frozen rows on every frozen endpoint
  (probe/clean acc, incoherence, π-cut, S_conf/S_bias, ceiling). Determinism
  (`seed_all`, `torch.use_deterministic_algorithms`) holds.
- **Statistical units.** The model seed is the replication unit (N = 12). Each
  seed trains a *fresh* six-arm model and evaluates on its own 1024 balanced-A/B
  episodes; the sign-flip runs on paired per-seed differences with ties
  excluded (N_eff = 12, no ties), floor 2/2^12 = 0.00049. Correct — the "N model
  seeds, not 2N" discipline (§10.1) is respected.
- **Manifold geometry.** Exactly six realizable triples (four sign + two
  magnitude contradictions); θ ≤ a by construction (`theta_value` clamps).
- **Parameter parity (conclusion holds).** Candidate encoder 393, R1 3×103 =
  309, R4/R5 = 0, R2/R3 far larger. No rival is given less than the candidate.

### 1.2 Deviations and defects found

These do not falsify the frozen run, but they bound what the gates actually
establish.

**(a) The reported R2/R3 parameter counts are wrong (overstated).**
`phase3/config.py:242` computes R2 heads as `3 * (d_h + 1) * 3 = 153`, but the
actual `r2_heads` (phase3/train.py:127–133) are `Linear(21,2)+Linear(17,3)+
Linear(19,2)` = 138. Actual R2 total = 1104 + 138 = **1242**, not 1257; R3 =
3312 + 138 = **3450**, not 3465. The helper overstates each by 15. Direction is
conservative (overstates the *rival's* capacity), so the parity conclusion is
unaffected, but the numbers printed in the summary are not the numbers in the
modules.

**(b) The analysis layer was patched post-hoc (not the frozen rows).**
`endpoints.json` is *not* in the frozen snapshot (only sources + protocol are
hashed). Two scratch scripts patched it in place after the run: `_fix_i5.py`
(the original I5 "stale" coherence compared against the wrong predicted value
`w[probe_entry-5]` instead of the injected `w[probe_entry-1]`) and
`_fix_targets.py` (corrected `n_refresh_targets`). The frozen `rows.jsonl` is
untouched and its hash is unaffected — but the I5 gate verdict as delivered was
produced by an in-place rewrite, not the original analysis pass. Disclosed in
the scripts, not in the summary.

**(c) F1 decode uses a within-seed split, not the frozen decoder discipline.**
`phase3/analyze_finals.py:163–166` calls `decode_accuracy(h_probe, z)` which
trains the logistic decoder on the first 512 and evaluates on the last 512 of
the *same seed's* episodes. Protocol §10.7 freezes "decoder trains on
engineering 0–7, evaluates on finals 100–111, never the reverse." This is a
literal deviation. Direction is conservative (same-seed split-half is a
*stronger* leak detector than cross-seed), so it does not inflate the claim —
but it is not what the protocol froze.

**(d) I4 (the load-bearing SHARED behavioral discriminator) is under-implemented.**
`phase3/interventions.py:109–120` — `private_copy_divergence` **ignores its
`consumer` argument** and returns `mean |W_ongoing − W_frozen|` over the
accumulation phase. It is one scalar about how much W moves after the
substitution tick (≈1.09), reported identically for spol/splan/sreg because all
three read the *same* W. Protocol §9.3.2 (and G9's binding handoff) requires
two things: the privatized consumer's output equals S_i(frozen copy) *exactly*,
and the i-vs-j divergence equals the accumulated evidence. The implementation
delivers neither the privatized-output equality nor a candidate-vs-R5 contrast;
it delivers one trajectory statistic, three times.

**(e) I3 (consumer-cut) is not run on finals at all.** It exists only as a unit
test (`test_interventions.py:71`) asserting W is a pure function of the token
stream — a reproducibility check, not the §9.3.1 "disable one consumer, W +
survivors byte-identical" measurement.

**(f) I1/I2/I5 pass by construction, run only on the candidate.** The
specialists are *fixed functions* of W (`apply_specialists`,
phase3/arms.py:261). Overwriting W and re-applying the functions necessarily
traces the injected value (I1/I5 "coherent"), and cutting W for one consumer
necessarily drops it to its no-W baseline with survivors byte-identical (I2).
These are wiring checks — real, but they do not measure a behavioral contrast
against R1/R5, which is the only place they could discriminate SHARED from
private. The single-write-reach test (`interventions.py:59–71`) is source-level
(shape `[-1]==3` vs not), which the protocol itself concedes is "never a
sufficient behavioral proof" (§9.3.4).

**(g) F1 is near-tautological given δ = 1.0.** The h-leak term
(`phase3/arms.py:176–178`) multiplies the GRU state by `1 − δ = 0` on every
unrefreshed step, so under π-cut the hidden state is zeroed each step and h_t in
the probe depends only on the current (neutral t3) token. Decode-at-chance is
guaranteed structurally. This is a disclosed design choice (README: "the
workspace h_t leaks at rate δ"), but it means H1.4 does not *test* free
recurrence — it removes the pathway. The real MAINTAINED content is carried
entirely by the π-cut decay (H1.3), which is genuine and clean: 0.9632 → 0.5000
(p = 0.00049, 12/12 seeds).

**(h) R1's "final energy" is a per-copy readout, not a total.** The energy
ledger (`phase3/arms.py:199–210`) sums only `refresh[:, t, 0]`, so R1's
`final_energy_mean` (30.4) matches the candidate's while R1 actually spends 3×
(98304 vs 32768 refresh events). The headline economy (1 vs 3 targets) is
captured correctly by `total_refresh_events`; the final-energy column is
misleading for R1.

---

## Part 2 — The six reductions

Measured from the frozen finals (per-arm mean over 12 seeds):

| arm | probe_acc | clean_acc | incoherence | refresh events | trainable params |
| --- | --- | --- | --- | --- | --- |
| candidate | **0.9632** | 0.9639 | 0.000 | 32768 | 393 |
| r1 (private) | 0.9634 | 0.9631 | 0.0140 | 98304 | 309 |
| r4 (analytic) | 0.9645 | 0.9645 | 0.000 | 0 | 0 |
| r5 (copies) | 0.9645 | 0.9645 | 0.000 | 0 | 0 |
| r2 (monolith) | 0.9643 | 0.9645 | 0.0038 | 0 | 1242 |
| r3 (history) | 0.9648 | 0.9652 | 0.0129 | 0 | 3450 |

The candidate is the **lowest-accuracy arm** on raw inference.

**A — "W is just a counter."** Largely **succeeds** on content. W *is* the
scalar sufficient statistic S_H = Σλ(x_i), quantized — a counter. The analytic
rival R4 computes the exact counter with the supplied λ and ties/beats the
candidate on every accuracy endpoint (0.9645 vs 0.9632) at zero maintenance
cost (0 refresh events vs 32768). The learned encoder adds nothing to accuracy
over the fixed counter. What the candidate adds is that the counter is *learned*
(λ not supplied) and *paid-maintained* — and the data show both properties are a
pure cost on this task, not an advantage. Bound: the "maintained hidden-state
content" (H1) face is fully explained by a fixed counter; the candidate's
distinctive content contribution over R4 is nil, and its maintenance is a
liability R4 does not carry.

**B — "Sharing unnecessary; private copies work."** **Partially refuted, but the
margin is small and one-sided.** R1 matches the candidate on probe accuracy
(0.9634 vs 0.9632), so sharing is *not* necessary for accuracy. But sharing is
load-bearing for exactly two measured things: coordination (candidate
incoherence 0.000 vs R1 0.0140, p = 0.00049, 12/12 seeds) and maintenance
economy (1 vs 3 refresh targets). This is the one genuine, discriminating,
behavioral advantage the candidate has. It is real but small (mean incoherence
0.014, max 0.074), and R1's incoherence does not measurably hurt R1's task
accuracy — so the *cost* of not sharing is a coordination/economy tax, not an
inference failure.

**C — "Monolithic RNN does everything equally well."** **Succeeds** on the task.
R2 (0.9643) beats the candidate with ~3× the parameters (1242 vs 393), no W, no
π, no shared state. R2 has no W to scramble/cut/stale, so the candidate's
modularity claim vs R2 is interpretability/intervention-only, not a performance
claim. Protocol §13 already predicted R2 as the "most likely clean winner" — on
raw inference it is.

**D — "New consumer is ordinary representation transfer."** **Succeeds — it is
stronger than transfer.** S_conf = sigmoid(W) and S_bias = W > θ_bias are fixed
analytic functions of W. A consumer that is a fixed function of a sufficient
statistic requires zero training by definition; there is nothing transferred and
nothing learned. H5's "reuse without retraining" is satisfied trivially, and the
protocol §9.5 concedes the new consumers are experimenter-supplied. H5 is a
consistency check, not evidence of an organizational property.

**E — "W interventions merely damage the network globally."** **Mis-framed, and
the gates are vacuous as causal evidence.** The interventions do not damage the
network; they overwrite a scalar W and re-apply fixed functions. They pass by
construction (see 1.2f), run only on the candidate, and are undefined for
R2/R3 (no W). So the interventions establish "the specialists are functions of
W" (a wiring fact), not a causal role a rival fails to realize. Against the one
rival family where they could discriminate (R1 private copies), the behavioral
part (I4/I5) is not actually measured (1.2d).

**F — "Different specialists are one objective split into heads."** **Partially
succeeds as a framing.** The three specialists are three fixed functions of one
scalar with genuinely distinct invariance classes (S_pol odd, S_plan
sign-and-magnitude, S_reg even) — verified by the I1 differential-scramble
signature and by construction. But they are experimenter-supplied fixed
functions, not learned or emerged distinct consumers; the "three non-collapsing
classes" is a design fact, not an organizational achievement. The reduction is
not literally right (S_plan/S_reg do not predict z), but its force — distinctness
is by fiat, not demonstrated — stands.

---

## Part 3 — Bound on the claim

The frozen statistical plan is applied correctly and the artifacts are sound;
that part of G13 stands. What the reductions bound is the *claim*:

The candidate does **not** outperform any rival on inference. Its content is a
counter, matched for free by R4/R5. The causal (H2), same-content (H3), and
reuse (H5) predicates are satisfied by construction (fixed functions of one
scalar W), and the two load-bearing behavioral discriminators named by G9 (I4
private-copy divergence, I5 global-vs-local error) are either not measured as a
rival contrast (I4) or measured only on the candidate (I5).

What survives, honestly bounded, is roughly:

> A maintained scalar representation can serve multiple fixed, objective-distinct
> consumers with **perfect structural coordination at 1× maintenance cost**,
> where the private-copy rival incurs nonzero incoherence at 3× cost — while not
> outperforming any rival on inference, and while the fixed sufficient-statistic
> rival does the same content work for free.

That is a level-(b) wiring/coordination fact, consistent with the protocol's
already-modest ceiling, but narrower than "SHARED ∧ CAUSAL ∧ DISTINCT ∧
AVAILABLE ∧ MAINTAINED are each causally load-bearing": CAUSAL and DISTINCT are
load-bearing only against a rival they were never behaviorally tested against,
and MAINTAINED is carried by the π-cut decay alone (genuine) plus a
near-tautological F1.

**Recommendations for any successor (G15):** (1) implement I4 as the actual
private-copy-substitution behavior — freeze a copy for one consumer, assert its
output equals S_i(copy) and diverges from the shared consumer's output, and run
the same on R5 — before claiming SHARED is behaviorally discriminated; (2) run
I1/I2/I5 on R1 and R5, not just the candidate, so the shared-vs-private contrast
is measured rather than asserted; (3) fix `parameter_counts` to read the actual
module shapes; (4) either re-run F1 under the frozen disjoint-seed decoder
discipline or explicitly re-scope it given δ = 1.0 makes it structural; (5) do
not claim the candidate "matches" R4 on accuracy as an achievement — it *trails*
R4 while paying for the privilege.

---

*Audit scripts: `_g14_audit.py` (hash/coverage/parameter/manifold re-derivation)
and `_g14_replay.py` (from-scratch replay of seeds 100/107/111 → byte-identical).*

# AC117 (M6) — Estimator-monitoring feasibility harness: results and verdict

2026-09-25. Confirmatory results for the M6 card (t_4e030ff7). Protocol frozen in
`AC117_PROTOCOL_v1.md` (hashed into `ac117_results_v1/pre_run_snapshot.json`). Engineering
seeds 0-7 (240 rows, disclosed and excluded); finals seeds 6800-6815 (480 rows, 32 individuals),
run once after the protocol hash. Clean control 64/64 (all five arms byte-identical in `no_cause`
and `move`).

## One-sentence verdict

The monitor mechanism works — its direction knowledge (the retained write-value) is a real,
causally-effective, load-bearing maintenance state — but it earns the support it earns on CONTROL
(which direction to repair), not on PREDICTION (the transient `ones>=4` policy already predicts
wrongness perfectly), and its value is representational, not economic.

## The two findings that shape everything

**(1) At the frozen ambient damage rate, the harness is vacuous — action 2 already maintains e.**
The M5 design's premise (case 3: a single estimate bit flips to wrong while the obs-bit-2 reflex
is silent) does NOT arise at ambient 1e-4. AC110 rule 1 was read as "e's own flip cannot trigger
its repair", but it overlooks that obs bit 2 fires on OTHER program corruption and action 2's
whole-bank majority-restore then restores e as a side effect — fast enough that e's ones-count
never reaches the 4-of-7 majority threshold (base rate 0/8096 post-window ticks; monitor == reflex
on bel_wrong_ever for every seed). This is the M5 section-8.3 non-vacuity failure, and it is why
the declared study runs at BEL_DAMAGE = 0.01 (the section-8.3 prescription). The monitor's added
value is therefore CONDITIONAL on a damage regime where action 2 is insufficient — which the
frozen ambient world does not produce.

**(2) Under sticky-SET (0->1) damage, direction is inert for prediction and only marginally
load-bearing for control.** Because damage only ever sets toward 1, the majority-read of e is
already the correct direction: "ones>=4" IS "wrong" under cut, and a fast state-blind
majority-restore (fixed_duty at short period) prevents the flip without ever needing to know the
direction. The retained write-value adds nothing to the READOUT, and its control value is a
robustness/efficiency margin, not a categorical capability.

## H1 — PREDICTION (scored on the fixed_duty trajectory, cut, post-window [8288, 16384))

Pooled over 32 fixed_duty individuals, 259,072 post-window ticks. Wrong fraction = 0.4462
(fixed_duty at K=12 is bimodal, so e drifts on ~2/3 of individuals and the base rate is moderate).

| readout | AUC | Brier | ECE | false-alarm | miss |
|---|---|---|---|---|---|
| monitor | 0.9858 | 0.0415 | 0.0758 | 0.025 | 0.000 |
| reflex (obs bit 2) | 0.4995 | 0.4468 | 0.4468 | 0.002 | 0.999 |
| direct (ones>=4) | 1.0000 | 0.0000 | 0.0000 | 0.000 | 0.000 |
| history (corruption counter) | 0.4998 | 0.4465 | 0.4465 | 0.001 | 1.000 |

Case counts (post-window): case 1 (ones=3) = 566; case 3 (ones>=4, obs bit 2 silent) = 115,514;
case 4 (repair_at_risk, ones<=3) = 3,530. The monitor's false alarms are EXACTLY the case-4
leading-indicator events (3,530) — at ones=3 without resource stress it reads reliable (P-G1), and
it catches every case-3 flip the reflex misses (P-G2).

Gates: P-G1 (read convention) PASS; P-G2 (case-3 catch over reflex) PASS; P-G3 (case-4 leading
indicator + move decoupling) PASS; P-G4 (referent separation: under move m reads reliable
throughout, direct reads unreliable 1.000) PASS; **P-G5 (calibration) FAIL against direct**;
**P-G6 (discrimination) FAIL against direct**.

P-G5/P-G6 fail because the transient `direct` rival (ones>=4, no retained direction) IS a perfect
predictor of wrongness under cut — it is literally the substrate damage count, and it is the SAME
signal the monitor reads. The monitor's only additions over direct are the retained direction
(inert for the readout under cut, where last_write==0 always) and the case-4 leading indicator
(a declared false alarm that only adds 3,530 false positives). So the monitor's distinguishing
content does NOT make it a better predictor; it makes it a *directional repairer*.

## H2 — CONTROL (cut; pairwise monitor vs rivals, 32 individuals)

| arm | bel_wrong_ever (mean) | e correct (all 32) | erepair writes | income (post) | route-1 retention |
|---|---|---|---|---|---|
| monitor | 26.6 | YES | 408 | 19,044 | 1.00 |
| fixed_duty (K=12) | 3,638.9 | NO (bimodal, ~1/3) | 268 | 18,808 | 1.00 |
| reflex | 8,016.6 | NO | 0 | 18,476 | 1.00 |
| direct | 8,016.6 | NO | 3 | 18,478 | 1.00 |
| history | 7,996.1 | NO | 4 | 18,478 | 1.00 |

The monitor keeps e correct in every individual (bel_wrong_ever 7-81, all in-window staleness);
the reflex/direct/history let e drift in every individual (~8,000 of ~8,096 post-window ticks
wrong); fixed_duty is bimodal (correct on ~1/3, drifted on ~2/3). The monitor's ~408 directional
repair writes achieve what no rival's policy does: direct cements the flip (its majority-restore
writes the minority toward the wrong majority), history cements on its corruption threshold, and
reflex never targets e.

Sign-flip (per-seed differences): monitor vs reflex/direct/history, wrong_ever p = 0.00000 (32/32
negative = monitor better); income p = 0.00000 (32/32 positive). monitor vs fixed_duty: wrong_ever
p = 0.00000 (26/26), income p = 0.00018 (24/28 positive, 4 negative).

Gates: C-G1 (clean control, 64/64 byte-identity) PASS; C-G2 (utility: dominance) PASS (income
32/32 over reflex/direct/history, 24/28 over fixed_duty; retention tied 1.00); C-G3 (content
inertness: fixed_duty does NOT reproduce monitor) PASS; C-G4 (causal role, engineering) PASS —
`scramble_m` (force m's readout reliable) removes the targeted repair and e drifts exactly like
reflex (erepair 432->0, wrong 29->8,111); `scramble_e` (force e's decision read) changes the
decision (relinquishments 0->2 in cut) while the maintenance mechanism is unchanged.

## The economic result (AC116's lesson re-entering)

Keeping e correct is REAL but economically marginal. Route-1 retention is 1.00 for every arm
(no one drops the route post-window, so e's drift is decision-irrelevant for the hold-vs-drop
gate, exactly AC110's finding). The only income consequence is ~+568 units (3%) from proactive
renewal firing while e reads 0 — a small, income-visible but not load-bearing margin. The
monitor's value is the representational state e itself, not the downstream economy.

## Feasibility verdict

SUPPORT for the mechanism, with two sharp bounds:

- The monitor maintains a genuine second-order state — the retained write-value in a distinct
  vulnerable locus — that causally drives directional repair of the first-order estimate's
  damage (C-G2/G3/G4 all pass, and scramble_m/scramble_e separate the two directions).
- The DIRECTION knowledge is load-bearing for CONTROL, not for PREDICTION: the transient
  `ones>=4` policy predicts wrongness perfectly (P-G5/P-G6 fail against it), because under
  sticky-SET damage the substrate damage count already IS the wrongness signal. What the
  direction buys is *which way to repair*, and it buys that only in a damage regime where the
  shared action-2 baseline fails — which the frozen ambient world does not produce.

Claim ceiling honored: no "metacognitive" unqualified, no staleness claim, no level-(e) wording.
A negative result bounds THIS design (the M5 harness) and THIS target (the damage component of
e's correctness in the AC110 cut world).

SOURCES: `ac117.py`, `AC117_PROTOCOL_v1.md`, `ac110.py`, `ac107.py`, `ac106.py`,
`ac99_d2.py`, `ac95.py`, `ac12.py`, `ac96.py`, `ac4.py`, `ac9.py`, `ac5_program.py`, `ac100.py`
(+ the full declared set in the protocol).

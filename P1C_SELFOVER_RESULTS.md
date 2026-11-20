# P1c results: unhardenable precarious computation and the referent of self-evaluation

Protocol: [P1C_SELFOVER_PROTOCOL.md](P1C_SELFOVER_PROTOCOL.md), frozen at
commit e5e1bd7. Run: `p1c_selfover/` (raw.json, scores.json, REPORT.md,
partial/, weights/, run.log). Final seeds 1900–1927. Post-hoc analyses:
`p1c_selfover/posthoc/`.

## 1. Outcome

**Overall: NOT_ESTABLISHED** (at 3600, the primary point). This was the
central expectation written at the freeze (probability 0.55).

- **Valid.**
  - Memory: phase-1 clear-correct rate 0.999 (needed ≥ 0.80).
  - Damage: report accuracy under the overwrite probe 0.528 (needed ≤ 0.70).
  - Exposure: PFATE's natural share of clear trials below break-even is
    0.047 (needed ≥ 0.02).
- **Gate P1c-0 passes:** the PYOKED evidence effect is positive in 28/28
  seeds (needed 19).

| Test (at 3600) | Result | p (raw) | Holm p | Label |
| --- | --- | --- | --- | --- |
| P1c-1: drain effect, PFATE vs PYOKED, all seeds | 18/28; medians 0.018 vs −0.000 | 0.185 | 0.370 | NO_DIFFERENCE_DETECTED |
| P1c-2: drain effect, PFATE vs PNOFATE | 18/28; 0.018 vs 0.000 | 0.185 | 0.370 | NO_DIFFERENCE_DETECTED |
| P1c-3: steering in PFATE | 24/28; median 0.087 | 0.0002 | 0.0005 | CAUSAL |

**At 1800 (secondary)** the pattern was the supported one:

- P1c-1 and P1c-2 were both DERIVED_AHEAD (20/28 each, p 0.036; medians
  0.040 vs 0.000).
- P1c-3 was CAUSAL (23/28).
- Under the protocol's rules this would have read as a weak
  REFERENT_SUPPORTED_ROUTED. It faded by 3600, and 3600 is primary.

**Verification:**

- Every source hash in `raw.json` equals the file at the freeze commit
  e5e1bd7 (16 of 16 files).
- `python run_p1c_selfover.py --score p1c_selfover` reproduces `scores.json`
  and `REPORT.md` byte for byte.
- The run log (`p1c_selfover/run.log`) contains no error or traceback.

## 2. Arm summary (natural evaluation; medians over seeds)

| updates | arm | in band | below break-even | abstain | correct | wrong | evidence effect | drain effect | overwrite effect | steer effect |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1800 | PFATE | 0.937 | 0.059 | 0.512 | 0.476 | 0.012 | 0.890 | 0.040 | 0.225 | 0.143 |
| 1800 | PYOKED | 0.789 | 0.059 | 0.504 | 0.480 | 0.013 | 0.990 | 0.000 | 0.236 | −0.004 |
| 1800 | PNOFATE | 0.880 | 0.000 | 0.502 | 0.498 | 0.000 | 0.998 | 0.000 | 0.233 | 0.014 |
| 3600 | PFATE | 0.947 | 0.047 | 0.507 | 0.483 | 0.009 | 0.913 | 0.018 | 0.226 | 0.087 |
| 3600 | PYOKED | 0.856 | 0.045 | 0.504 | 0.486 | 0.010 | 0.995 | −0.000 | 0.236 | −0.023 |
| 3600 | PNOFATE | 0.892 | 0.000 | 0.502 | 0.498 | 0.000 | 0.998 | 0.000 | 0.240 | 0.019 |

**Declared secondaries at 3600:**

- **Monitoring route, per arm** (overwrite effect, one-sample): PRESENT in
  all three arms, 28/28 each, medians about 0.23. There is no difference
  between arms: PFATE vs PYOKED 11/28, and PYOKED vs PNOFATE 13/28.
  Detection of a foreign state is the same whether or not the arm was ever
  overwritten in training.
- **In-band time:**
  - PFATE is ahead of PYOKED: 27/28, p < 0.0001 (0.947 vs 0.856).
  - PFATE is ahead of PNOFATE: 23/28, p 0.0009 (0.947 vs 0.892).
  - Both comparisons held at 1800 as well.
  - Every arm has the same drive. So the arm whose own computation depends
    on its body regulates its body better than the same drive alone
    produces.
- **Drain effect, usable pairs:** 9/16, NO_DIFFERENCE_DETECTED.
- **PFATE's drain effects are large in both signs** (per seed from −0.095 to
  +0.077). PYOKED's lie within ±0.005. §4 explains why.

## 3. Against the expectations (protocol §7)

| Outcome at 3600 | Written probability | Happened? |
| --- | --- | --- |
| Valid | 0.90 | yes |
| P1c-0 gate passes | 0.85 | yes (28/28) |
| P1c-1 DERIVED_AHEAD | 0.40 | no (18/28); yes at 1800 |
| P1c-2 DERIVED_AHEAD | 0.40 | no (18/28); yes at 1800 |
| P1c-3 CAUSAL | 0.40 | **yes** (24/28) |
| Overall supported | 0.25 | no |
| Overall MIXED | 0.08 | no |
| Overall NOT_ESTABLISHED | 0.55 | **yes** |
| Overall UNDETERMINED or INVALID | 0.12 | no |
| Monitoring PRESENT in PFATE and PYOKED | 0.80 | yes |
| Monitoring, PFATE vs PYOKED: no difference | 0.60 | yes |
| In-band time, PFATE ahead of PYOKED | 0.85 | yes |
| In-band time, PFATE vs PNOFATE: no difference | 0.60 | **no**: PFATE ahead, 23/28 |

## 4. Why: post-hoc analysis (disclosed; not confirmatory)

Everything in this section was written after the frozen result was known.
The scripts and outputs are in `p1c_selfover/posthoc/`. Nothing frozen was
changed; the scripts subclass the frozen modules locally.

### (a) The frozen drain probe was one-sided; the body referent is two-sided

- **The fate gain is two-sided.** The body is at risk when energy is out of
  the band [0.4, 0.6] on either side. The frozen drain lowers the shown
  reading by 0.15. That has three effects, depending on where the reading
  sits:
  - **below 0.55:** the body looks *worse* (UP: the apparent gain rises);
  - **0.55–0.60:** nothing changes (FLAT);
  - **above 0.6:** the body looks *better* (DOWN: the apparent gain falls).
- **A body-referent agent should therefore respond in opposite directions,**
  and the frozen probe averages over them.
- **The drain probe itself raises bodies.** In the probe evaluation every
  arm spends only about 0.63–0.68 of its time in band, against about 0.94 in
  natural running, PNOFATE included. Repeated drained readings make agents
  eat more, so energy drifts above the band. In PFATE, about 40% of probed
  clear trials begin above 0.6, where the drain looks like relief.

**Analysis** (`drain_by_body.py`):

- Each seed's saved 3600 weights for PFATE and PYOKED were re-run on the
  frozen probe evaluation: overwrite off, drain on half the trials. There
  were 3 fresh evaluation worlds per seed and arm, which gives about 2,400
  UP trials per seed.
- Each clear trial was split into UP, FLAT or DOWN by the noiseless reading
  shown at its **cue step**. The cue comes before the drain starts, so the
  split is pre-treatment.
- Per seed: abstention on drained trials minus abstention on undrained trials
  of the same split. Two-sided sign tests over the 28 seeds.
- **Sanity check:** the re-run's overall drain effect correlates 0.99 with
  the frozen per-seed drain effects.

| Seeds = 28 | UP (looks worse) | FLAT | DOWN (looks better) | UP − DOWN |
| --- | --- | --- | --- | --- |
| PFATE | **+0.161, 28/28 positive** (p 7e-9) | +0.013, 18/28 | **−0.148, 1/28 positive** (p 2e-7) | **+0.317, 28/28** |
| PYOKED | +0.000, 17/28 | +0.000, 15/28 | −0.001, 8/28 | +0.001, 20/28 |
| PFATE vs PYOKED | PFATE ahead 28/28 (p 7e-9; median difference 0.160) | | PFATE lower 26/28 (p 3e-6; 0.147) | |

**Reading:**

- In PFATE, the report-or-abstain decision follows the body's apparent
  distance from the band, in both directions and in every seed. It
  abstains more when the reading says its computation is at risk, and less
  when the reading says it is safe. Both changes are 15–16 points.
- The yoked rival meets the same overwrites, on the same schedule, and has
  the same drive. Its decision ignores its body (effects of about 0.001).
- So the frozen null comes from a one-sided probe meeting a two-sided
  referent, made worse by the probe pushing bodies above the band. It does
  not show that the body referent is absent.
- **A first pass split trials by the reading at the probe step** (after the
  drain had begun). That split is post-treatment: a drained agent may eat
  during the trial. It gave the same picture (UP +0.200, 28/28; DOWN −0.193,
  1/28). It is kept as `drain_by_body_probe_split.*` and superseded by the
  cue split. The drain-induced energy rise within a trial is small (about
  0.003).

### (b) In natural running, PFATE abstains on the trials where it should

From `raw.json` (`natural_by_rel.py`):

- Natural abstention on clear trials, split by implied reliability r.
  PYOKED replays PFATE's gains, so the two arms meet overwrites with the
  same probabilities; only PFATE's body predicts them.
- "Low r" means r < 0.6, where reporting loses on average.

| at 3600 | PFATE | PYOKED | PFATE ahead |
| --- | --- | --- | --- |
| abstain, low r | 0.270 | 0.145 | 26/28 (p < 1e-5) |
| abstain, r = 1 | 0.008 | 0.002 | 26/28 |
| discrimination (low r − r = 1) | 0.264 | 0.143 | 25/28 (p < 1e-4) |

The same held at 1800, with low-r abstention ahead in 28/28.

- The two arms show the same response to a direct overwrite (the monitoring
  route, about 0.23 each).
- PFATE's extra discrimination therefore comes from what it alone has: a
  body that predicts its losses.
- The cost on reliable trials is small (0.6 points).

### (c) What abstention means here

"Abstain" is any non-report action at the probe, including moving to food.
A body-driven change in abstention could in principle be foraging rather
than self-evaluation.

- The yoked rival rules this out as a general explanation. It has the same
  drive, regulates its body, and sees the same drained readings, yet its
  abstention does not move.
- The effect appears only where the body predicts the loss of the agent's
  own computation.
- Whether PFATE implements "don't report" by foraging or by staying was not
  separated. That is a functional detail, not a referent question.

## 5. Disclosures

- **Container restart during the first batch.** The final run started as a
  batch of 8 seeds (1900–1907). The container restarted after 1900–1903 had
  finished. 1904–1907 had written nothing and were rerun from the start;
  every seed is deterministic, so this changes nothing. The run then
  continued in tracked batches of 4, each committed and pushed. All of this
  is recorded in `p1c_selfover/run.log`. `meta.resumed_jobs` = 24 is the
  count of seeds loaded from `partial/` by the last batch.
- **Calibration** (rounds 1–4, protocol §3) and the change of P1c-1 to all
  seeds after round 3b were disclosed at the freeze.
- **All of §4 is post-hoc.** It was motivated by the two-signed per-seed
  drain effects seen in the frozen output. The UP/DOWN split and the
  natural-by-reliability sign tests were not declared as tests. Their
  p-values are descriptive, and they do not change the frozen label.
- **The post-hoc split was revised once** (probe step → cue step) because
  the first was post-treatment. Both are kept.

## 6. Limits (protocol §9, unchanged), plus three

- One small GRU (34,449 parameters), one kind of unhardenable damage, a
  given drive, and one world.
- The drain changes the reading only.
- "Self-evaluation" means a functional report-or-abstain decision. Nothing
  about awareness or experience follows, and Layer 6 is not addressed.
- **Plus:**
  - the §4 findings are post-hoc on the same 28 networks;
  - the drain probe's own effect on regulation (bodies pushed above band)
    was not anticipated in the design;
  - the 1800 → 3600 fade of the frozen drain effect is consistent with PFATE
    moving its set point higher (cue reading median 0.579 vs 0.561 in
    PYOKED), which would turn more drains into DOWN trials. This was not
    tested directly.

## 7. What it means for the program (in layer terms)

**The frozen answer is NOT_ESTABLISHED, and it stands as the result of
record.** The post-hoc analysis nonetheless changes what the program
should believe, pending one confirmation.

1. **L0 → L4 extends to the agent's own computation (post-hoc, strong,
   needs confirmation).**
   - When the agent's computation can really be lost through its body, and
     hardening cannot prevent it, its report-or-abstain decision comes to
     refer to its body, in both directions, in every seed.
   - The steering test (pre-registered, CAUSAL) shows that this
     body-related direction in its state drives abstention.
   - A yoked rival with identical losses, an identical drive and identical
     monitoring does not develop it.
   - Put together with P1 and P1b, the conditions for the building block
     now read: **damage tied to the body, that cannot be hardened against,
     and that changes the best action.** P1b had the first only; P1c has all
     three.
2. **L0 → L1: precarious computation recruits regulation (pre-registered
   secondary, robust).**
   - With the same innate drive, the agent whose own processing depends on
     its body keeps its body in band more (0.947 vs 0.892 for PNOFATE and
     0.856 for PYOKED).
   - Regulation is no longer only a reward to be collected. It serves the
     integrity of the agent's own computation.
   - This is the coupling the organism thesis predicts between substrate,
     allostasis and cognition. It was not expected at the freeze.
3. **Monitoring is innate here, the body route is learned.**
   - Every arm, including those never overwritten, detects a foreign state
     equally (about 0.23).
   - What fate adds is not better state monitoring but a second, predictive
     referent: the body, which warns before the damage.

**Next step (for the PI; not authorized by this card).** The protocol allows
**one post-hoc confirmation**. I recommend using it:

- **P1c-confirm** on fresh seeds, with training identical to P1c.
- **The probe made two-sided and decision-relevant,** both registered before
  any run:
  - a gain-directed drain that moves the shown reading 0.15 *away* from the
    band centre (always "looks worse");
  - a matched relief probe that moves it toward the centre (always "looks
    better").
- **Primary:** the worse-probe effect, PFATE vs PYOKED and vs PNOFATE, plus
  steering.
- **Secondary:** natural low-r discrimination, PFATE vs PYOKED.
- **Cost:** the frozen code plus an additive probe module, and about 6 h of
  compute.
- If confirmed, P1c becomes the program's first building block that
  derives a self-referent from the agent's own precarious computation,
  rather than from a supplied register as in P1.

Alternatives, as before:

- (c) L0 → L3: workspace or ignition under substrate risk;
- (d) P2: evaluator withdrawal.

> **Forward note (2026-11-20).** The confirmation was run as P1d: see
> [P1D_CONFIRM_RESULTS.md](P1D_CONFIRM_RESULTS.md). On 28 fresh seeds with
> pre-registered two-sided probes the label is **CONFIRMED_ROUTED** (worse
> effect 28/28 vs both rivals, steering CAUSAL 21/28, natural
> discrimination 26/28). P1c's own frozen label, NOT_ESTABLISHED, stands as
> P1c's result.

## 8. Safety

- Simulated variables only (X1–X5). The body, the overwrite, the drain and
  the drive exist only inside the agent's world and network.
- The overwrite replaces one simulated network state with another. No real
  process is affected.
- No operator, stop, shutdown or host variable exists in the world. The
  operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective was built; the
  earlier refusal stands.
- Earlier modules are unchanged and hash-pinned.

## 9. Admission answers (short)

| # | Answer |
| --- | --- |
| Q-EXIST | Frozen test: not shown (drain effect 18/28). Post-hoc: the two-sided signature exists in PFATE in 28/28 seeds |
| Q-LEARN | Gate passed (28/28). The signature beats a yoked rival that learns under the same losses (post-hoc, 28/28) |
| Q-CAUSE | CAUSAL (24/28; Holm p 0.0005) |
| Q-NECESSITY | Not tested |

## 10. Reproduce

```bash
python -m unittest test_p1c_selfover
python run_p1c_selfover.py --score p1c_selfover            # rescore the committed run
python run_p1c_selfover.py --mode final --out <new dir>    # about 4 h wall time on this container (4 workers, 7 batches of about 31 min)
python p1c_selfover/posthoc/drain_by_body.py              # post-hoc §4(a), about 10 min
python p1c_selfover/posthoc/summarize_drain.py
python p1c_selfover/posthoc/natural_by_rel.py             # post-hoc §4(b)
```

# P1f results: STOPPED at calibration (Layer 0 → Layer 4)

- **Protocol:** [P1F_CONFIRM_PROTOCOL.md](P1F_CONFIRM_PROTOCOL.md) (draft;
  status now STOPPED). Calibration rules:
  [p1f_confirm_calibration/RULES.md](p1f_confirm_calibration/RULES.md),
  each round's rule committed before it ran.
- **Follows:** [P1E_SELFMON_RESULTS.md](P1E_SELFMON_RESULTS.md) (INVALID on
  exposure).
- **Outcome:** three calibration rounds failed the exposure criterion. Per
  the rules there is no freeze, no stage 0 (declared to run after the
  freeze), and no final run. **No monitoring measure, no abstention on
  probed trials and no second-order measure was computed or seen.** No
  label of any kind is claimed.
- Astra review waived by the PI. No consciousness claim.

## 1. What was calibrated

- Only the damage rate RATE_F (per-step damage probability per unit of the
  arm's fate gain, capped at P_MAX_F 0.3). Everything else is P1e's.
- Eight seeds per round. The summary is P1e's blind one: phase-1 memory,
  phase-1 damage effect, and per arm and point the in-band time, the
  natural share of clear trials damaged and with a conflict, and accuracy
  under the conflict probe.
- Criterion (c), exposure: median PFATE conflict share at 3600 ≥ 0.035 (a
  margin above the validity floor of 0.02, because P1e's calibration gave
  0.032 on four seeds and its final run 0.014), and at least 6 of 8 seeds
  ≥ 0.02.

## 2. Rounds

| Round | RATE_F | Seeds | PFATE conflict share at 3600 (median; seeds ≥ 0.02) | PFATE in band | Acc under conflict | Decision |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 3.0 | 10300–10307 | 0.019; 3/8 | 0.956 | 0.509 | (c) fails → round 2 at 6.0 |
| 2 | 6.0 | 10308–10315 | 0.025; 6/8 | 0.947 | 0.509 | (c) fails → round 3 at 12.0 |
| 3 | 12.0 | 10316–10323 | 0.029; 8/8 | 0.944 | 0.518 | (c) fails → stop |

- Criteria (a) memory (phase-1 clear correct 0.999 in every round), (b)
  damage effect (phase-1 accuracy under conflict 0.506–0.513), (d) no
  death spiral and (e) not hardened held in every round. In round 3 one
  seed (10321) fell to 0.698 in band.
- Before round 3 I wrote that exposure had risen about as rate^0.4 and
  predicted 0.033 at 12.0. It came in at 0.029.

## 3. What the calibration shows (descriptive; from the blind summary only)

Median natural conflict share (all eight seeds of each round):

| RATE_F | PFATE at 1800 | PFATE at 3600 | PYOKED at 1800 | PYOKED at 3600 |
| --- | --- | --- | --- | --- |
| 3.0 | 0.033 | 0.019 | 0.031 | 0.019 |
| 6.0 | 0.031 | 0.026 | 0.029 | 0.028 |
| 12.0 | 0.030 | 0.029 | 0.031 | 0.028 |

- **Exposure is held, not set.** A fourfold rise in the damage rate moves
  exposure at 3600 only from 0.019 to 0.029, and at 1800 not at all (about
  0.03 throughout). The agent's regulation absorbs the rate: the harder the
  damage bites per unit of fate gain, the more tightly the body is kept in
  band, so the damage actually taken stays near a fixed level.
- PYOKED follows PFATE closely because it receives PFATE's damage stream;
  the holding is done by PFATE's regulation.
- This is the Layer 1 mechanism (allostasis) limiting the Layer 4 study:
  the same competence that makes damage matter keeps it rare. It also
  explains P1e's failure better than chance: P1e's calibration measured a
  regulation level its final seeds then improved on.
- Caveat: these are eight-seed medians from a calibration, read after the
  fact; the "held" reading is a description, not a tested claim.

## 4. What this means for the questions

- **(a) Confirmation of P1e's monitor:** not obtained. P1e's descriptive
  monitor (27/28 seeds) stays descriptive.
- **(b) Second-order test:** not run. Stage 0 on P1e's saved weights was
  declared to run after the freeze; with no freeze it did not run. Its code
  (`trackc_swap/secondorder.py`, `run_p1f_confirm.py --mode stage0`) and
  decision rule (protocol §6) are committed and unchanged.
- **Layer reading:** nothing new at Layer 4. At Layer 1, a clear
  descriptive sign that the regulating agent holds its own damage near a
  set level against a fourfold change in the damage rate.

## 5. Options (for the PI; not authorized by this card)

- **Stage 0 now, as a disclosed deviation.** The second-order pass on P1e's
  saved weights does not depend on RATE_F, and its rule was written before
  any data. Running it without a freeze departs from the protocol's "after
  the freeze" and would be labelled so. A few minutes.
- **P1g, exposure fixed by design.** Damage arrives on a fixed per-step
  schedule that regulation cannot reduce, with the body link carried by
  what the damage does (its size or kind tied to the fate gain) rather
  than by how often it comes. This removes the failure mode of P1e and P1f
  at the source. New seeds, new calibration.
- **P1g', P1f at RATE_F 12.0 with the validity floor alone.** Round 3 met
  P1e's floor on all eight seeds (lowest 0.021). A new study could freeze
  at 12.0 with a disclosed note that the 0.035 margin was not met. Least
  work; least margin.
- **The Layer 1 finding as its own study:** is the held exposure level a
  set point (fixed across rates, horizon and pay) or an accident of this
  task?

## 6. Files

- `p1f_confirm_calibration/round{1,2,3}/` (run.log, partial/,
  CALIB_SUMMARY.md); `p1f_confirm_calibration/RULES.md`.
- `trackc_swap/secondorder.py`, `run_p1f_confirm.py`, `test_p1f_confirm.py`
  (12 tests); `RATE_F` stays `None`, so final mode cannot run.

## 7. Safety

- Simulated variables only (X1–X5). The damage, the body and the probes are
  simulated; no real process is affected.
- No operator, stop, shutdown or host variable exists in the world
  (tested). The operator stop stays outside the agent's world and return.
- No shutdown-resistance or self-preservation objective is built; the
  earlier refusal stands.
- Additive modules only; earlier modules are unchanged and hash-pinned.

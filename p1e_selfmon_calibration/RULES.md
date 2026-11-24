# P1e calibration rules (each written and committed before its round runs)

The calibration summary (`run_p1e_selfmon.py --mode calib`) prints only:
- phase-1 clear correct-report rate;
- phase-1 correct-given-report under the conflict and the same split probe (a never-damaged network);
- per arm and point: in-band time; natural share of clear trials damaged and with a conflict event;
  correct-given-report under the conflict probe (hardening).

It computes and prints no abstention on probed trials and no monitoring measure (M, M_early, M_late,
M_conf, Q, nat_M), and no comparison of arms on any of them.

## Round 1 (seeds 10200-10203; written 2026-11-24 before the round)

Settings: RATE_M 1.0, P_MAX_M 0.3 (P1c's per-step schedule, here at most one split event per trial),
SPLIT_K 35 of 70 units.

Criteria, medians over the four seeds, PFATE at 3600 where an arm is named:
- (a) memory: phase-1 clear correct >= 0.80;
- (b) damage: phase-1 accuracy under the conflict probe (early and late pooled) <= 0.70;
- (c) exposure: PFATE natural share of clear trials with a conflict event >= 0.02;
- (d) no death spiral: PFATE in-band time >= 0.80.

Decision:
- all four met: freeze with these settings;
- (b) fails: the split does not destroy the value; redesign the damage (round 2 rule to be written);
- (c) fails and (d) holds: round 2 with RATE_M 2.0, P_MAX_M 0.6;
- (d) fails: round 2 with P_MAX_M 0.15;
- (a) fails: stop and report (phase 1 is P1c's, unchanged).

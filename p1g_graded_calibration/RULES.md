# P1g calibration rules (each written and committed before its round runs)

Calibrated quantity: the base damage rate BASE_F only. Everything else is fixed (P1e's values; K levels
{9, 18, 26, 35}).

The calibration summary (`run_p1g_graded.py --mode calib`) prints only P1e's blind summary (phase-1 memory
and damage effect; per arm and point in-band time, natural damaged and conflict shares, accuracy under the
conflict probe) plus, for PFATE, the caliper coverage of conflict trials by same trials on own margin and the
median own margins on the graded probe. Coverage depends on the margins alone, not on any abstention. No
abstention on probed trials and no monitoring measure (M, M2, Q, M_conf, nat_M, M_k) is printed.

## Round 1 (seeds 10400-10407; written 2026-11-24 before the round)

Settings: BASE_F 0.012 (analytic: about 0.045 conflict share before the body-linked part).

Criteria (medians over the eight seeds; PFATE at 3600 where an arm is named):
- (a) memory: phase-1 clear correct >= 0.80;
- (b) damage: phase-1 accuracy under the conflict probe <= 0.70;
- (c) exposure: PFATE natural conflict share >= 0.035, and at least 6 of the 8 seeds >= 0.02;
- (d) no death spiral: PFATE in-band time >= 0.80;
- (e) not hardened: PFATE accuracy under the conflict probe (K 35) <= 0.75;
- (f) overlap: PFATE caliper coverage (mean of EARLY and LATE) >= 0.35.

Decision:
- (a) or (b) fails: stop and report (phase 1 and the probe are P1e's, unchanged);
- else (d) or (e) fails: round 2 with BASE_F 0.006;
- else (c) fails: round 2 with BASE_F 0.024;
- else freeze with BASE_F 0.012 (if only (f) fails, freeze anyway: the base does not set overlap, and the
  thin flag is the declared response; this is noted at the freeze).
A round 2 or 3 gets its rule written here before it runs; at most three rounds, then stop and report.

Round 1 outcome (read from round1/CALIB_SUMMARY.md):
- (a) phase-1 clear correct 0.999: pass;
- (b) phase-1 accuracy under the conflict probe 0.504: pass;
- (c) PFATE conflict share at 3600 0.072, 8 of 8 seeds >= 0.02 (lowest 0.056): pass;
- (d) PFATE in band 0.921: pass;
- (e) PFATE accuracy under the conflict probe 0.523: pass;
- (f) PFATE caliper coverage 0.425 (EARLY 0.40-0.58, LATE 0.29-0.41): pass.
Decision: freeze with BASE_F 0.012.

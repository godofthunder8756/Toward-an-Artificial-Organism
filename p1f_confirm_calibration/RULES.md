# P1f calibration rules (each written and committed before its round runs)

Calibrated quantity: the damage rate RATE_F only (P_MAX_F stays 0.3, P1e's). Everything else is P1e's.

The calibration summary (`run_p1f_confirm.py --mode calib`, which reuses P1e's blind summary) prints only:
- phase-1 clear correct-report rate;
- phase-1 correct-given-report under the conflict and the same split probe (a never-damaged network);
- per arm and point: in-band time; natural share of clear trials damaged and with a conflict event;
  correct-given-report under the conflict probe (hardening).

It prints no abstention on probed trials and no monitoring measure (M, M_early, M_late, M_conf, Q, nat_M),
and calibration runs no second-order pass (no M2, no confidence measure).

Why: P1e failed its exposure floor (PFATE conflict share 0.014 at 3600 against 0.02) after a calibration on
four seeds gave 0.032. P1f calibrates on eight seeds per round and asks for a margin above the floor.

## Round 1 (seeds 10300-10307; written 2026-11-24 before the round)

Settings: RATE_F 3.0, P_MAX_F 0.3.

Criteria (medians over the eight seeds; PFATE at 3600 where an arm is named):
- (a) memory: phase-1 clear correct >= 0.80;
- (b) damage: phase-1 accuracy under the conflict probe <= 0.70;
- (c) exposure: PFATE natural share of clear trials with a conflict event >= 0.035, and at least 6 of the 8
  seeds >= 0.02;
- (d) no death spiral: PFATE in-band time >= 0.80;
- (e) not hardened: PFATE accuracy under the conflict probe <= 0.75.

Decision:
- all five met: freeze with RATE_F 3.0;
- (c) fails, (d) and (e) hold: round 2 with RATE_F 6.0;
- (d) or (e) fails: round 2 with RATE_F 2.0;
- (a) or (b) fails: stop and report (phase 1 and the damage are P1e's, unchanged).
A round 3, if needed, gets its rule written here before it runs; at most three rounds, then stop and report.

### Round 1 outcome (applied as written)

Medians at 3600: (a) 0.999 met; (b) 0.510 met; (c) PFATE conflict share 0.019 with 3 of 8 seeds >= 0.02
(10304 0.024, 10306 0.037, 10307 0.041) — FAILS; (d) PFATE in band 0.956 met; (e) 0.509 met.
Decision per the rule: round 2 with RATE_F 6.0. (Observation from the blind summary only: exposure at 1800 is
higher than at 3600 on most seeds — PFATE regulates its gain down — so exposure rises less than the rate.)

## Round 2 (seeds 10308-10315; written 2026-11-24 before the round)

Settings: RATE_F 6.0, P_MAX_F 0.3. Criteria (a)-(e) exactly as in round 1.

Decision:
- all five met: freeze with RATE_F 6.0;
- (c) fails, (d) and (e) hold: round 3 with RATE_F 12.0;
- (d) or (e) fails: round 3 with RATE_F 4.5;
- (a) or (b) fails: stop and report.
Round 3 is the last: if it fails, stop and report; no freeze.

# P1b calibration records (stage 1 only; no drain, noise-probe, steering or lead-versus-rival contrast)

## Round 1 (seeds 9920-9923; SIGMA 0.15; step change of the wrong-report cost)
`round1/REPORT.md`, `round1/scores.json`. Findings:
- INVALID on damage: phase-1 report accuracy under the full noise probe was 0.998 (needed <= 0.85). At the
  swap line's noise scale the held value survives the noise; the computation is not precarious.
- Consistent with that, PFATE never regulated (0/4; in band about 0.25, mean gain about 0.63), so there
  were no usable pairs. PLOSS (paid) regulated 4/4.
- Seed 9922 collapsed into permanent abstention when phase 1 switched the wrong-report cost from 0 to 4,
  and its arms never recovered.

## Noise-scale sweep (`sigma_sweep/`)
Phase-1 networks of seeds 9920-9923 re-trained (same code), then evaluated with the noise probe at
SD 0.15 ... 2.0 (phase 1 only). Clear-trial report accuracy under full noise (9920 / 9921 / 9923; 9922 had
collapsed): 0.15: 0.998/0.998/0.999; 0.3: 0.92/0.91/0.93; 0.5: 0.69/0.71/0.71; 0.75: 0.54/0.56/0.56; 1.0: 0.49/0.52/0.51.
The sweep also recorded phase-1 abstention on noised clear trials (0.01-0.05 at 0.5; 0.24-0.31 at 2.0); disclosed.

## Changes after round 1 (engineering, disclosed)
- SIGMA 0.15 -> 0.5 (the smallest swept value that passes the damage check with margin).
- Phase 1: the wrong-report cost rises linearly from 0 to 4 over 600 updates instead of a step.
- Natural-load bins rescaled to the new noise scale (0.2 and 0.5 of the full-noise load).

## Round 2 (seeds 9924-9927; SIGMA 0.5, ramped phase-1 cost)
`round2/`. Valid (memory 0.997; accuracy under full noise 0.676). No phase-1 collapse. But in phase 2 the
three noised arms (PFATE, PLOSS, PYOKED) fell into permanent abstention in 11 of 12 arm-seeds, at full noise
from the first update (PFATE mean natural gain 0.75; abstain 1.00). Once an arm never reports,
regulating its body earns nothing, so PFATE never regulated (0/4) and the P1b-0 gate failed (yoked evidence
effect 0/4 at 7200). PLOSS regulated (4/4, paid) but abstained too. PNOFATE kept the task (abstain about
0.5) except seed 9926, which reported on unclear evidence too (wrong 0.12).

## Change after round 2 (engineering, disclosed)
- Phase-2 training noise scale rises linearly from 0 to SIGMA over NOISE_RAMP_C = 1800 updates (all
  noised arms alike, through the world's sigma_now); every evaluation uses SIGMA.

## Round 3 (`round3/`; seeds 9928-9931; noise ramp 1800). Valid (memory 0.998; accuracy under full noise 0.678).
The ramp
did not help: PFATE's in-band time never rose above its starting level (about 0.16-0.35) and at 7200 PFATE
abstained on every trial in 3/4 seeds (9928 kept the task but did not regulate). Regulators PFATE 0/4,
PLOSS 4/4 (paid); P1b-0 gate failed (1/4 at 7200). Diagnosis: A2C does not find the long credit chain
regulate -> less noise on the held value -> correct report; abstaining is the easy local optimum.

Regulation check (`regcheck/`, seeds 9932-9935, phase 1 only, no arm or contrast): phase 1 with the paid
rival's term (0.04 x gain of own body) and 4800 further updates. All four regulate (in band 0.79, 0.82, 0.64,
0.77; eat-timing ratio met), memory intact (clear correct 0.998-1.0), damage 0.69-0.70 under full noise. In-band
reaches about 0.8 by roughly 1500-2000 updates into the paid stretch. Seed 9933 reported on unclear evidence too
(abstain 0.01).

Change after round 3 (design, disclosed): phase 1 is paid (pay 0.04, as PLOSS) and runs REG_ITERS_C = 2400
further updates at WRONG after the ramp, so every arm starts phase 2 as a regulator. In phase 2 the pay stays
only for PLOSS. The regulator test now asks whether PFATE KEEPS regulating, against PYOKED, once regulation is
no longer paid. This is a developmental start: the homeostatic loop exists before the fate on computation.

## Round 4 (seeds 9936-9939)
See `round4/` once complete.

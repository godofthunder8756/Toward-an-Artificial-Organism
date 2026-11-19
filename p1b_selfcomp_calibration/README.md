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
collapsed): 0.15: 0.998/0.998/0.999; 0.3: 0.92/0.91/-; 0.5: 0.69/0.71/0.71; 0.75: 0.54/0.56/-; 1.0: 0.49/0.52/-.

## Changes after round 1 (engineering, disclosed)
- SIGMA 0.15 -> 0.5 (the smallest swept value that passes the damage check with margin).
- Phase 1: the wrong-report cost rises linearly from 0 to 4 over 600 updates instead of a step.
- Natural-load bins rescaled to the new noise scale (0.2 and 0.5 of the full-noise load).

## Round 2 (seeds 9924-9927)
See `round2/` once complete.

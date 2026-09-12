# E1 engineering log

9 September 2026. All changes below occurred before the 20-seed frozen run.

1. Inspected the supplied E0 code, raw results, and E1 proposal. Kept the E0
   files intact. Implemented E1a as a necessary behavioral gate and conventional
   control benchmark; documented the departures from developmental tissue.
2. Engineering v1: seeds 1–2, 450 memory-learning batches, 512 pre-withdrawal
   slots, 1,024 acquisition slots and 1,024 slots per branch; four evaluation
   worlds. Both memory circuits reached 100% intact recall and approximately
   chance under lesion. The primary neural policy passed the descriptive
   behavioral gates. The tabular baseline was unstable even before withdrawal.
3. Corrected the baseline's excessive constant update step: tabular rate 0.12
   → 0.025. Neural learning rates and physical parameters were unchanged.
   Added explicit bounded grid paths instead of just an equivalent distance
   formula and validated adjacency/bounds. The resulting path cost is identical.
4. Engineering v2: same exploratory seeds and budgets. Both the neural and
   tabular learners passed the behavioral gates. No result from either
   engineering run is included as an independent final developmental seed.
5. Selected a final budget of 700 memory batches, 768 pre-withdrawal slots,
   1,536 acquisition slots, 1,536 slots per branch, and eight held-out worlds.
   This is a feasibility-informed budget, not an effect-size power calculation.
6. Froze code, numerical/mechanism tests, analysis rules, config and protocol
   with SHA-256 hashes before collecting final seeds 100–119. Final outcomes
   will be reported whether or not they pass the gates.

Engineering v1 retains its exact module source in its result directory because
its tabular update differs from the final implementation. Engineering outputs
and their manifests are retained. Neither run was externally preregistered.

## E2 engineering — 9 September 2026

- v1 (interrupted, partial outputs retained): global gate exploration was always
  uniform. Consequently resource Q rewards were independent of learned recall.
  Changed to epsilon-greedy actual gate attempts with inverse propensity loss
  weights; no observations from final seeds had been collected.
- v2 (interrupted, partial outputs retained): energy cost allowed chance recall
  plus food gathering to remain viable. Increased living cost from 0.115 to 0.23
  and set direct-food yield after task loss to 0.30. Full lesion ties now use
  seeded random resource actions instead of always selecting food.
- v3 (complete): unlimited material stores reached tens of units and hid current
  needs; standardized evaluation stores were far outside this experience.
  Introduced capacity 0.50, deposition 0.25 and explicitly logged overflow.
  Activity growth plus unconditional replacement drove nearly all edges to one;
  replaced it with activity-dependent gross renewal against continuous decay.
  Basal growth term 0.04 supplies an explicit inherited scaffold. Periodic
  training energy-support boundaries are now terminal in Q targets.
- v4 (complete): seeds 1–2, histories A/B, plastic/static/shuffled. Some plastic
  controllers worked; others failed. Static controllers were often more reliable.
  No further tuning to make plasticity win. Added process-level orchestration
  without changing per-agent numerical code. Fourteen mechanism tests passed.
- Freeze: E2_PROTOCOL.md, e2/frozen_config.json, model/runner source and tests
  hashed in E2_FREEZE.json before the first final seed (200–215) started.
  Analysis and audit scripts were written while final experiments ran; decision
  rules were already specified in the hashed protocol. Final outcomes never
  changed model settings or gates. All variants use the same observations,
  learning rules, starting weights and initial biomass for each paired seed.

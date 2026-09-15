# RESUME_RESEARCH — addendum: state after AC33–AC41

Everything below was done in one long session on 2026-09-15. Read this with the main body above; the
earlier AC1–AC32 sections remain as they were.

## Two claims now pass, both frozen, both with all eight pre-declared gates

| study | claim | endpoint | result |
| --- | --- | --- | --- |
| **AC33** | release-your-order-and-search-again re-acquires the new regime's level | sites retained (ordering) | 8/8 gates; capable worst **12.33**, incapable best 11.25 |
| **AC36** | the same, where maintenance is unaffordable in full | population retained (maintenance) | 8/8 gates; capable worst **6.67**, incapable best 5.67 |

Both have `PROTOCOL` + `RESULTS` files, frozen result dirs, provenance snapshots, recomputed-gate audits
and cross-process replays. Do **not** re-run either; both protocols say so explicitly.

## Five prerequisite stops — every one decided before a final seed was spent

| study | why it stopped |
| --- | --- |
| **AC31** | design falsified by its own engineering (unpaired comparison, noise ≈ margin) |
| **AC35** | self-funded endpoint could not resolve orders (spread 1.00 vs noise 0.30); production scales with population and equalizes |
| **AC37** | drain mechanism worked at short horizons (ratio 22) but failed at study scale (7.16 < 10) |
| **AC39** | effect size 2.45 < 3 while the exact test gave p = 0.0001; ratio unstable across seed subsets |
| **AC41** | endpoint degenerate (occupancy a structural constant, 21) and effect-size requirement mis-scaled |

No protocol exists for any of them and none should. Each has an `*_ENGINEERING_v1.md`. Their tests assert
the recorded failure so it cannot be quietly relaxed.

## Other results since AC33

- **AC34**: the binary alive/dead endpoint is horizon-unstable (same config: 0.40 at 400 ticks, 0.00 at
  800). Rejected as an endpoint; graded retention recommended instead.
- **AC38**: the inherited validity criterion measured the wrong quantity. Pairing buys no meaningful
  variance reduction in this endpoint (factor ≈ 1 either side). Introduce the exact **sign-flip test** on
  paired individuals: AC33 and AC36 hit the floor (p = 0.0005 at n = 12 — every individual favouring the
  capable arm); AC32's contrast was equally significant, so AC32 failed on gate *shape*, not contrast.
  **Power floor 2/2ⁿ: n = 4 gives 0.125 and can never be significant — every engineering pass used 4.**
- **AC40**: the split criterion — resolvability, effect size, stability, headroom. Found that all four
  contrasts are resolved at the exact test; that **headroom was missing from every earlier criterion**
  (AC39's maintained arm sat at exactly 4096 ticks, 100% saturated); and that **my own stability metric
  does not discriminate** (it flags both passing studies and the failing one).
- **AC19-M**: the maintenance half from AC19 is **diagnosed and closed**. The cut arms die 0/4 even with
  the register damage rate at zero, so **corruption is excluded**; the route is that an emptying register
  stops driving activity (live arm active 16384 ticks vs 6156; conversions, births and spending roughly
  halve). Reconciled with AC14: the state's **integrity** is not load-bearing, its **occupancy** is.

## Standing process rules (all learned the hard way this session)

1. **Prerequisite before protocol, always.** Measure that the endpoint resolves the contrast, with power
   stated (`n ≥ 8`), before writing anything. Cheap failures beat frozen ones.
2. **Never move a bar.** Four studies prove it is possible to stop cleanly instead.
3. **Pre-flight the hash set**: parse the protocol's `SOURCES (declared):` line and assert it equals what
   the runner hashes, before the first final seed (AC32 declared 5, hashed 4).
4. **Do not hash verification tools** into a study's snapshot (AC17's lesson) — editing them creates
   self-inflicted drift.
5. **Run the suite, READ the result, then commit.** Three commits this session landed on a red suite
   (`739d401`, `67c4445`, `0ac641a` — the last with a SyntaxError) because a patch and a commit were
   issued in one sequence without checking in between. This rule is the fix.
6. **When a measurement surprises you, apply your own check to data whose answer you already know.**
   That is how the AC29 half-chance metric, AC38's ratio rule, AC40's stability metric and AC41's
   mis-scaled requirement were caught. All four were my own instruments, not the science.

## The next step, and it is well-posed

AC41's stop leaves two clean routes, both cheap because the AC40 four-check framework now rejects bad
endpoints before they consume a study:

1. **An occupancy-family endpoint with genuine variation** — a *duration* (how long the register stays
   occupied) rather than a *level* (which was a structural constant), with its effect-size requirement
   measured in that endpoint's own units, not copied from another ledger.
2. **The activity endpoint with saturation fixed by censoring** — time-to-first-drop, which has headroom
   by construction because it is a duration, and which re-tests AC41's falsified bimodality prediction
   (the bimodality belongs to *activity*, not to the repair cut).

Either way: framework first, prediction stated in advance, `n ≥ 8`, corruption absent so AC14's integrity
channel is off by construction. Beyond that, the broader-developmental-function arc (AC20–AC28: 9.49
effective bits of order structure) has the machinery to be extended further, and the AC19 line is now
closed rather than open.

## Since AC41: a third verified claim (AC42, AC43)

**AC42** (`ac42_endpoints.py`, `AC42_ENDPOINTS_v1.md`) — surveyed all 15 scalar quantities `ac19.run`
exposes, at 16 individuals per arm, against variance / headroom / resolution / impaired-fraction. Result:
**7 usable endpoints, 5 of them metabolic and bimodal at 88% impaired** (`spent_e`, `spent_m`,
`memory_writes`, `converted`, `W_birth`). The survey's own checks **reject both endpoints that failed
before** — `ledger.active` (live sd exactly 0) and `register_replicas_set_total` (constant 21). Two open
questions settled: (1) AC41's falsified prediction is **resolved, not merely refuted** — the bimodality
belongs to the *metabolic* family, not to activity as such and not to occupancy (wrong about *where*,
right about *whether*); (2) the shortlist carries effect sizes in each endpoint's **own** units (208–4218),
so no requirement need be copied from another ledger — AC41's specific error. `productivity_kept` is an
**inverted** signal (cut arm scores higher) and needs interpreting before use.

**AC43** (`ac43_capability.py`, `AC43_PROTOCOL_v1.md`, `ac43_results_v1/`, verified) — the first frozen
study of the AC19 maintenance line, and it **passes all seven declared gates**:

| gate | measured | bar |
| --- | --- | --- |
| G1 resolvability | p = 0.000105, n = 16 | 0.01 |
| G2 effect size (endpoint units) | median Δ = **161** births | 150 |
| G3 impaired fraction | **0.875** | 0.75 |
| G4 heterogeneity present | 0 < 0.875 < 1 | — |
| G5 protected variant > cut | median > 0 | 0 |
| G6 completeness | 16/16, none substituted | — |
| G7 determinism | two re-runs exact | — |

Claim: repair-maintained register occupancy produces more W births than its absence, **corruption absent**
(`reg_rate = 0.0`, AC14's channel off by construction). Endpoint `ledger.W_birth`, chosen from AC42's
survey. Finals: **seeds 8–15 × 2 histories, disjoint from the engineering seeds 0–7**. capable 366.1 vs
cut 222.0. **Verified**: `audit_ac43.py` PASS (gates recomputed independently, 4 registered source hashes
re-checked), `replay_ac43.py` PASS (fresh process, exact), `test_ac43.py` 12 tests OK.

**Two corrections AC43's own audit forced, both recorded in commits:**
- Prediction 3 ("no individual is expected to be hurt") is **FALSIFIED**: min difference is **−11**, one
  of sixteen individuals is hurt. The gate set deliberately never excluded that (the claim is an aggregate
  with stated heterogeneity), but the prose in `6cb0c05` overstated it and the audit caught it.
- The bimodality prediction **held on fresh seeds** (0.875 vs AC42's 0.88) — AC39's prediction, falsified
  by AC41 for occupancy, relocated by AC42 to metabolism, confirmed by AC43 on seeds that played no part
  in locating it.

**How to reproduce the check:** `.venv/bin/python -B ac43_capability.py finals` will fail — `mkdir(
exist_ok=False)` refuses to clobber the frozen directory. That is intended. Run `audit_ac43.py` and
`replay_ac43.py` instead.

**Three verified frozen claims now stand**: AC33 (re-acquisition), AC36 (maintenance under an insufficient
income), AC43 (repair capability, corruption absent) — each with a protocol registered before its first
final seed, fresh seeds, an independent auditor and a cross-process replay. Plus five prerequisite stops
(AC31, AC35, AC37, AC39, AC41), AC34's rejected endpoint, and **six corrections logged against my own
instruments and prose** — the last two by an audit written specifically to catch exactly that.

## Still untouched, and honestly stated

- **Self-sufficiency in a world that resolves orders** — AC35 and AC37 both stopped; the AC37 drain
  mechanism works at short horizons and needs an endpoint whose noise does not grow faster than its spread.
- **Nothing in this line claims experience, understanding, or life, and none of it is offered as evidence
  toward them.** The endpoints are sites retained, populations retained, and distinguishable rule orders.
  "Maintenance" means sites retained under a cost. The claim discipline in the project README stands.

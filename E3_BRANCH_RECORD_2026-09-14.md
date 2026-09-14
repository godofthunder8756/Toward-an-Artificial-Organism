---
title: E3 side-branch lineage and design-freeze line-ending erratum
description: Where the 2026-09-14 maintenance-allocation toy sits relative to E3, and why verify_e3_design.py fails on this checkout
ms.date: 2026-09-14
---

## 1. Design-freeze erratum: `NEW_AGENT_GUIDE.md` hash mismatch

### Observation

On this checkout, `python -B verify_e3_design.py` exits 1:

```text
NEW_AGENT_GUIDE.md: bytes mismatch (expected 20529, found 20960)
NEW_AGENT_GUIDE.md: sha256 mismatch
```

`test_e3_inputs.TestE3Inputs.test_23_no_generator_worker_imports_or_freeze_changes`
fails for the same reason. The rest of the E3 suite passed: 443 tests,
1 failure, 4 skipped.

### Cause: line endings, not content

- The working-tree file has 431 CRLF line endings. Converting them to LF gives
  exactly 20,529 bytes, and its SHA-256 equals the frozen value
  `895deb5a…c99b26`.
- The repository has one commit (`ca97560 Init`). It stores all 23 manifest
  files with LF endings (`git ls-files --eol` reports `i/lf w/crlf`). This
  checkout has `core.autocrlf=true` and no `.gitattributes`.
- Checked against all 23 manifest entries:
  - 22 entries match the CRLF working-tree bytes. 1 does not.
  - 1 entry, `NEW_AGENT_GUIDE.md`, matches the committed LF blob. 22 do not.
- The v0.11 snapshot was therefore hashed on Windows when 22 files had CRLF
  endings and the guide alone had LF endings.

The content of all 23 frozen files matches the snapshot, apart from line
endings. The earlier statement in `E3_REVISED_HYPOTHESIS_v1.md`, "The guide
was edited after that snapshot", is wrong and is retracted there.

### Consequence

The verifier's result depends on the checkout's line-ending conversion, not
only on content:

- A Windows checkout with `autocrlf=true` fails 1 of 23 entries.
- An LF checkout (Linux, macOS, or `autocrlf=false`) would fail 22 of 23.

Under either convention, neither the verifier nor `test_23` can currently pass
for all files. Anyone who reruns the audit should read a failure in light of
this erratum rather than as evidence of edited content.

### What was done

Nothing frozen was changed:

- `E3_DESIGN_FREEZE_v0_11.json`, `verify_e3_design.py` and `test_e3_inputs.py`
  are unmodified.
- The v0.11 hash, byte count and manifest SHA-256 are preserved.
- No file was re-encoded to force a pass.

### Decision left open for the next freeze

This record doesn't choose among these options:

- Record a line-ending normalization rule in future manifests, for example
  hashing LF-normalized text, and keep v0.11 as a historical Windows-EOL
  snapshot explained by this erratum.
- Add a `.gitattributes` rule that pins frozen documents' checkout bytes.
  This changes working-tree bytes, so it has to be paired with a new manifest
  version, never with edits to v0.11.

## 2. Lineage of the side branch

### Where it comes from

1. `E3_INTEGRATION_DECISION_v0_11.md` refuted the universal financial
   interpretation of H2. Fixed repetition covers full conditioning plus
   maximal correction for at most 33 material units, under g=36. The decision
   set current confirmatory H2 to NO-GO. Its next permitted stage 1 asks for a
   revised discriminating question before any further engineering.
2. `E3_REVISED_HYPOTHESIS_v1.md` proposed such a question. It kept H2's
   subject, allocating scarce maintenance among memories whose usefulness
   changes, but replaced "does scarcity force abandonment" with "does an
   uncertainty-aware allocator outperform a recency allocator on returning
   memories". It is in H2's lineage. It is not a new E3 frontier, and it
   doesn't replace the v0.11 design.
3. `e3_fep_engineering_seed.py` (v1) and `e3_fep_engineering_seed_v2.py`
   test that question in a standalone toy:
   - a binary repetition code
   - majority decode
   - repair toward the current majority

   The toy shares no code, tariffs, codecs or state layout with the frozen
   `e3/` package. Nothing it shows transfers to claims about `e3/`.

### Status

This is an exploratory side branch:

- No freeze.
- No confirmatory sample.
- No prospectively defined minimum useful advantage.

Results are estimates, not gate outcomes. The FEP, active-inference and
autopoiesis vocabulary in `E3_REVISED_HYPOTHESIS_v1.md` motivated the design
only. The toy doesn't implement any of those theories, and its results
neither support nor undermine them.

### Relation to "E3k/E3l"

A research note from 2026-09-14 describes an established frontier labeled
E3k/E3l: a planner anticipates deterioration when supplied its rate, but the
individual struggles to learn that rate. No artifact with those labels or
that finding exists in this workspace. A search covered this repository, all
local and remote branches, and the sibling repository. This branch cannot be
reconciled with that work until the materials are added.

One conditional observation, if that finding stands: the precision allocator
uses a hand-set staleness bonus (`ucb_c * sqrt(ticks_since_query)`). The
experimenter supplies it; the individual doesn't learn it. A positive result
for it would sit on the "rate supplied" side of that finding. It would not
show that an individual learns deterioration.

## 3. Audit of the toy (2026-09-14)

Produced by `audit_e3_fep_seed.py` in `e3_fep_seed_results/v2/audit.json`.
All outputs from v1 runs 1–4 are preserved unmodified in
`e3_fep_seed_results/v1/`.

- **A. Refactor equivalence.** v2 in `--legacy-shared-rng` mode reproduces v1
  exactly: 12 runs, 4 policies × 3 seeds, 800 ticks. Fields compared: overall,
  post-return and steady accuracy with their counts, and repair counts.
- **B. Random-stream pairing.** v1 was not paired. Scrub draws shared one
  generator with relevance transitions, queries and corruption.
  - Environments diverged from the no-repair reference by tick 1–10.
  - About 93.5% of query ticks differed, which is chance-level agreement.
  - Total corruption flips differed by policy.

  v1 runs 3 and 4 therefore compared policies on effectively independent
  worlds. v2 draws environment and policy randomness from separate streams.
  Its digests, flips and query sequences are identical across all seven
  policies for every audited seed.
- **C. Repair in isolation.** The test covered every bit pattern for widths
  3–8 and both truth values, repaired to a fixed point with no further damage.
  - **Violations:** none. Every pattern reaches a fixed point within n
    repairs, independent of which bad bit is chosen.
  - **Odd widths:** below threshold (fewer than n/2 wrong bits), repair fully
    restores the trace at a cost equal to the number of wrong bits. Above
    threshold, it locks in the wrong value.
  - **Even widths:** at an exact tie, the outcome depends on truth, because
    the decoder's tie rule (`sum*2 >= len`) always decodes 1. The result is
    100% restored for truth 1 and 0% for truth 0. v1's configurations used
    widths 8 and 6.
  - **Decode:** repair never changed a decode outcome. It only restores
    redundancy against future damage. This is the constraint already recorded
    in `E3_RESEARCH_HANDOFF_v0_1.md`.

Conclusion so far: the substrate behaves as a majority code is specified to,
with one implementation asymmetry at even-width ties. Below-threshold damage
is recoverable at progressively greater cost. Beyond-threshold damage is not
recoverable without new information.

## 4. Budget feasibility (2026-09-14)

### Design

`e3_fep_engineering_seed_v2.py` ran with split random streams, and environment
digests were verified identical across all policies. The run used 16 seeds,
6,000 ticks and seven policies:

- `none`
- `random`
- `uniform`
- `recency`
- `precision`
- `oracle`
- `ample`, meaning every damaged cue is fully repaired every tick with no
  budget limit and no truth access.

It covered v1's two configurations plus odd-width diagnostics that remove the
tie rule. Results are in `e3_fep_seed_results/v2/`.

Intervals are descriptive bootstrap intervals over seeds, applied to paired
within-seed differences. No minimum useful advantage was defined before these
runs, so nothing below is a gate outcome.

### Post-return recall

| Config (budget, width, flip p) | none | recency | precision | uniform | ample | oracle* |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| default 5, 8, 0.03 | 0.519 | 0.786 | 0.801 | 0.821 | 0.939 | 0.999 |
| default 5, 7, 0.03 (no ties) | 0.493 | 0.842 | 0.846 | 0.840 | 0.919 | 0.999 |
| stress 3, 6, 0.04 | 0.518 | 0.546 | 0.539 | 0.540 | 0.632 | 0.956 |
| stress 3, 5, 0.04 (no ties) | 0.507 | 0.497 | 0.509 | 0.493 | 0.577 | 0.968 |

\*Invalid as a ceiling. See the oracle finding below.

### Paired precision − recency, post-return recall

| Config | Mean difference | 95% interval | Seeds positive/negative |
| --- | ---: | --- | --- |
| default, width 8 | +0.015 | [−0.018, +0.049] | 11/5 |
| default, width 7 | +0.004 | [−0.025, +0.035] | 8/8 |
| stress, width 6 | −0.007 | [−0.022, +0.008] | 7/9 |
| stress, width 5 | +0.012 | [−0.010, +0.032] | 9/6 |

There is no evidence of an advantage for precision in any configuration.

For reference, v0.11 already uses a 0.05 adaptive-gate magnitude. Every
interval's upper bound falls below it; default width 8 is borderline at
+0.049. This comparison was chosen after seeing the data. It is not a test.

### Findings

1. **The "oracle" leaks the answer through its timing.** It repairs only cues
   whose current majority equals truth. Two facts together mean timing is a
   channel for truth:

   - Audit C shows that repair never changes a decode.
   - Repair never reads truth.

   A cue with a lost majority is left to drift until noise happens to restore
   the correct majority. Only then is it repaired and locked in. Evidence for
   this mechanism:

   - Under stress, the budget-3 oracle reaches 0.956 with 17,825 repairs.
     Unlimited truth-blind repair reaches 0.632 with 22,931 repairs.
   - The oracle made zero harmful repairs.

   A scheduler conditioned on truth is therefore not a maintenance ceiling in
   this substrate: it relearns the answer through selection. A valid
   scheduling ceiling may use only truth-independent privileged information,
   such as the true relevance state, future queries and flip-event exposure.
   It may not use truth or any stored past consensus, which would reintroduce
   a template. That oracle has not been run.
2. **Under stress, maintenance is nearly impossible here, not just badly
   scheduled.** Unlimited, immediate, truth-blind repair reaches only 0.632 at
   width 6 and 0.577 at width 5, near the 0.5 floor. Budgeted policies reach
   0.49–0.55.

   Proposed mechanism, consistent with the numbers but not separately tested:
   - At width 5 and p=0.04, a single tick flips three or more bits in about
     6.4×10⁻⁴ of cue-ticks.
   - Any repair that uses only the current trace then locks in the wrong
     majority.
   - With symmetric noise, lock-out and lock-back rates are equal. Every
     truth-blind policy therefore relaxes toward 0.5 over roughly 800 ticks,
     well inside a 6,000-tick run.

   Consequence: the stress configuration cannot discriminate allocators.
   Recall is also a transient that depends on run length, not a steady state.
3. **At the default budget, the budget rarely binds, so allocation mostly
   doesn't matter.**
   - Budgeted policies used about 3.76 repairs per tick against a budget of 5.
   - Unlimited repair used 3.83.
   - At default width 8, repairs per hot cue-tick and per cold cue-tick are
     equal (0.236 versus 0.235) for random, uniform and recency. Recency is not
     concentrating effort, because whenever the budget covers every damaged
     cue, ordering is irrelevant.

   The per-tick binding fraction was not instrumented. Mean repairs per tick
   is only a proxy. Truth-blind budgeted policies still trail unlimited repair
   by 0.08–0.15. A likely contributor is the one-bit-per-cue-per-tick limit.
   That is not measured.
4. **Hot-cue errors are inherited from dormancy.** For every budgeted
   truth-blind policy, the wrong-majority fraction on hot cues matches the
   fraction lost at return; at default width 8 both are about 0.18–0.22. About
   20% of repairs at default, and 45–49% under stress, reinforce an
   already-wrong majority. "Steady" failures are mostly losses that occurred
   before the cue became active, not failures of maintenance while active.
5. **The even-width tie rule distorted v1's configurations.** At default
   width 8, recency's recall is 0.577 for truth-0 cues and 0.949 for truth-1
   cues. At width 7 the two are symmetric: 0.854 and 0.832.

### Answer to "world, controller, or interpretation"

Neither v1 configuration could test the allocation question:

- In the default configuration, scarcity rarely binds.
- In the stress configuration, the world defeats even unlimited truth-blind
  repair.

The run was also unpaired, and one control leaks truth. The negative
allocator result stands only in this narrow form: no advantage was observed
in configurations that could not have shown one. It does not tell us whether
recoverability-based allocation helps.

### Not yet done (superseded by section 5)

- Run a truth-independent scheduling oracle.
- Instrument the per-tick budget-binding fraction.
- Choose a configuration that is scarce but feasible, where the budget binds
  and unlimited truth-blind repair stays well above floor. This must be
  selected on control policies only, before any allocator comparison.
- Decide the tie rule: change it to be unbiased, or keep odd widths only.
  This changes world rules, so it needs an explicit decision.

## 5. Allocation study v1: stopped at phase 1; exploratory follow-up

### Protocol outcome

`E3_ALLOCATION_PROTOCOL_v1.md` was written before configuration selection.
It had been audited (`audit_e3_allocation.py`: v3 reproduces v2 exactly, one
environment per seed, truth-blind decisions invariant under truth relabelling,
loss model matches Monte Carlo, learned rate within 1%).

Phase 1 ran the controls only, on engineering seeds 0–7, over 27
configurations. **No configuration passed, so per protocol no allocator
comparison was run and no freeze was made.** Every configuration failed
criterion 4 (headroom): `blind_oracle` never beat max(`uniform`, `random`) by
0.08, and its headroom ranged from −0.102 to +0.038.

Provenance for the stopped study, as LF-normalized SHA-256:

| File | SHA-256 |
| --- | --- |
| `E3_ALLOCATION_PROTOCOL_v1.md` | `8efea85b…3ca9cd` |
| `e3_fep_engineering_seed_v3.py` | `1f384f8f…c46ed4` |
| `e3_allocation_study.py` | `435453f4…ce7338bc` |
| `audit_e3_allocation.py` | `e622df2a…03e3db` |
| `phase1_controls.json` | `dd081b3f…069a93e37` |
| `selected_configs.json` (`selected: []`) | `d96f2195…68c9a5` |

A gap in the selection criteria surfaced here. Criteria 1 and 3 together
("unlimited repair feasible" and "budget binds") do not imply that the
scarce budget is feasible. At width 7/p 0.02/budget 2 and width 9/p 0.03/
budget 2, every budgeted control stays near 0.5 while `ample` is at 0.99–1.0.

### Exploratory diagnostics (not prespecified)

**1. Diagnostic of the ceiling failure**
(`explore_e3_phase1_diagnostic.py`, controls only, seeds 0–7).

The hypothesis that `blind_oracle` abandons dormant cues is not supported
where it matters. At width 9/p 0.02/budget 3 its repairs are split evenly
(0.172 per hot cue-tick, 0.170 per cold), yet it scores 0.728 against
`uniform`'s 0.831. It lets more cues reach the failure threshold: 0.279 are
lost at return (uniform 0.167), and 0.288 of its repairs are harmful (uniform
0.164).

**2. Ceiling search in the unchanged world**
(`explore_e3_ceiling_search.py`, seeds 8–15).

The harness was first validated: it reproduces v3's `uniform` and
`blind_oracle` exactly, with identical recall and every repair decision.
Seven truth-blind schedulers were then compared, paired against `uniform` on
overall recall, with descriptive 95% intervals:

| Scheduler | w9/p.02/b3 | w9/p.03/b3 | w9/p.03/b4 |
| --- | --- | --- | --- |
| `deepest_then_stale` (largest minority count first) | +0.179 [+0.122, +0.235], 8/8 | +0.054 [+0.017, +0.089], 7/8 | +0.257 [+0.193, +0.322], 8/8 |
| `blind_oracle` | −0.052 | −0.018 | −0.065 |
| `hot_then_stale` (true relevance first) | −0.056 | −0.006 | −0.049 |
| `deadline_then_stale` (true next query within 20 ticks first) | −0.050 | +0.006 | −0.047 |
| `shallowest_then_stale` | −0.215 | −0.001 | −0.086 |
| `deadline_then_shallowest` | −0.159 | +0.010 | −0.070 |

`deepest_then_stale` reaches 0.994 at w9/p.02/b3 (unlimited repair: 1.000).
It uses only the minority count of its own trace, which the agent can
observe, plus its own repair history. It is an agent-observable policy, not a
privileged ceiling. Every scheduler that prioritizes relevance or imminent
queries is worse than ignoring relevance, even with true future query times.

### Interpretation (exploratory)

- In this world, the useful allocation signal is closeness to irreversible
  loss: observable damage depth, the recoverability half of the restated
  claim. Relevance weighting, the consequence half as implemented, hurts.
- A plausible reason: relevance is symmetric, so every memory has the same
  long-run value, dormant memories return, and lock-in makes loss permanent.
  Preventing threshold crossings everywhere therefore beats protecting what is
  needed next. This explanation is unverified.
- It also explains the ceiling failure: `blind_oracle` weights its loss model
  by near-term query probability.
- The effects are large and consistent across seeds. They were found after
  trying several schedulers on seen configurations, so they need confirmation
  on fresh seeds under a prospective protocol (see
  `E3_ALLOCATION_PROTOCOL_v2.md`).
- Whether consequence information helps when memories differ in lasting
  importance, for example becoming permanently obsolete, is untested. It would
  require a world-rule change.

## 6. Allocation study v2: confirmatory result (seeds 200–231)

### How the run was conducted

- **Protocol:** `E3_ALLOCATION_PROTOCOL_v2.md`.
- **Freeze:** `E3_ALLOCATION_FREEZE_v2.json`, created 2026-09-14T20:56:40Z,
  covering 9 files with LF-normalized SHA-256 `3ffa8ac67d2e2118…`. The final
  phase verified every hash before running.
- **Pre-freeze audit** (`audit_e3_allocation_v4.py`):
  - v4 reproduces v3 exactly (40 runs).
  - `depth_first` makes the same decisions as the explored scheduler.
  - Truth-blind policies are invariant under truth relabelling.
- **Configurations**, selected by rule from existing phase-1 control data:
  width 9/p 0.02/budget 3 and width 9/p 0.03/budget 4. Both were exploratory
  configurations; this is disclosed in the protocol.
- **Validity:** both configurations passed every check, with environments
  paired.

### Prespecified outcome

**Overall status: supported in this toy.**

| Config | `depth_first` − `recency` overall recall | 97.5% interval | Seeds positive | Decision |
| --- | ---: | --- | ---: | --- |
| w9/p.02/b3 | +0.334 | [+0.308, +0.365] | 32/32 | useful advantage |
| w9/p.03/b4 | +0.343 | [+0.314, +0.373] | 32/32 | useful advantage |

### Secondary results (descriptive, 95%)

| Paired difference | w9/p.02/b3 | w9/p.03/b4 |
| --- | --- | --- |
| `depth_first` − `uniform` | +0.178 [+0.148, +0.208] | +0.302 [+0.282, +0.324] |
| `depth_then_recency` − `depth_first` | +0.008 [+0.002, +0.016] | −0.009 [−0.031, +0.013] |
| `depth_first` − `recov_supplied` | +0.029 [+0.016, +0.041] | +0.170 [+0.145, +0.196] |
| `depth_first` − `ample` | −0.013 [−0.020, −0.006] | −0.104 [−0.119, −0.087] |
| `blind_oracle` − `uniform` | −0.145 [−0.182, −0.109] | −0.040 [−0.065, −0.015] |
| `recov_supplied` − `recency` | +0.305 [+0.279, +0.335] | +0.173 [+0.149, +0.198] |
| `recov_learned` − `recov_supplied` | +0.002 [−0.009, +0.013] | −0.009 [−0.032, +0.014] |
| `precision` − `recency` | +0.035 [−0.001, +0.075] | −0.018 [−0.048, +0.011] |

### Mean overall recall by policy

| Policy | w9/p.02/b3 | w9/p.03/b4 |
| --- | ---: | ---: |
| `none` | 0.500 | 0.504 |
| `recency` | 0.652 | 0.548 |
| `blind_oracle` | 0.663 | 0.550 |
| `precision` | 0.687 | 0.530 |
| `random` | 0.796 | 0.571 |
| `uniform` | 0.808 | 0.589 |
| `recov_supplied` | 0.957 | 0.721 |
| `recov_learned` | 0.959 | 0.712 |
| `depth_first` | 0.986 | 0.891 |
| `depth_then_recency` | 0.994 | 0.883 |
| `ample` | 0.998 | 0.995 |

`truth_oracle` scores 1.000 and 0.999 but is excluded as a leak.

### Reading, per section 9 of the protocol

- **Recoverability half: confirmed in this toy.** Triage by observable
  closeness to irreversible loss beats triage by recent activity by about 0.33
  recall, in every seed. It is a conventional most-endangered-first scrubbing
  rule. It shows nothing beyond ordinary error correction: no self-modelling,
  anticipation or organismal property.
- **Consequence half.** Adding recent activity as a tie-break within a depth
  class gives +0.008 in one configuration and nothing detectable in the
  other. That is below the 0.03 MUA, so it is near zero in magnitude.
- **Recent-activity allocation is harmful under binding scarcity**
  (descriptive). `recency` falls below round-robin in both configurations
  (0.652 vs 0.808; 0.548 vs 0.589).
- **Not prespecified as a contrast, and worth noting.** `recov_supplied`, the
  myopic loss model driven by *inferred, smoothed* relevance, is strong
  (0.957). `blind_oracle` uses the same model with *exact* future query times
  and is weak (0.663). A plausible explanation is that exact, sparse query
  timing gives zero value to cues with no query inside the horizon. The model
  also ignores later repairs, so foresight concentrates effort badly, while a
  smooth expectation behaves more like damage-depth weighting. This is
  unverified.
- **Rate learning:** as expected from audit E, there is no detectable cost of
  learning the corruption rate when damage is directly observable.

### What this does for the project

- It strengthens the conventional rival that E3 must beat. `NEW_AGENT_GUIDE.md`
  already requires "a standard error-correcting representation plus ordinary
  reinforcement learning" as a rival. This branch shows that the rival should
  include observable-damage triage, not recency. In this toy, recency
  underperforms even round-robin, and a candidate compared only against it
  would look much better than it is.
- The consequence half of the restated claim remains untested in a world where
  it could matter. With symmetric relevance, every memory has equal lasting
  value.

### End-of-session fields

| Field | Record |
| --- | --- |
| Question tested | Does allocating scarce repair by observable damage depth preserve more recall than allocating by recent activity? Secondary: does adding consequence information help? |
| Mechanism implemented | Binary-trace toy v4, with 12 policies including damage-depth, recoverability-model, oracle and control allocators. Nothing in `e3/` was touched. |
| Externally supplied objectives/rules | Simulator laws, corruption and relevance processes, and the query generator. Chain rates are supplied to `recov_*`; the corruption rate is supplied to `recov_supplied` and `blind_oracle`. |
| Engineering changes made | Six. v1 bugs found: inverted bonus, `hash()` seeds, shared RNG stream, even-width tie bias. The ceilings changed from the truth oracle (leak) to the blind oracle (weak) to damage-depth as a candidate. Every version is preserved. |
| Frozen sample and gates | Protocol v1 stopped at phase 1 with no freeze. Protocol v2 froze 9 files, used 32 fresh seeds, a 0.03 MUA and Bonferroni intervals. |
| Primary results | `depth_first` − `recency`: +0.334 and +0.343, 32/32 seeds in each configuration, useful advantage in both, overall status supported. |
| Simplest sufficient rival | The finding *is* the conventional rival: ECC-style most-endangered-first scrubbing. |
| Failures and negative results | Exploratory claims retracted. Protocol v1 stopped with no feasible configuration. Both oracle ceilings failed, one by leaking truth and one by underperforming round-robin. Consequence information added about zero. `precision` showed no advantage. The design-freeze verifier depends on line endings. |
| What this establishes | In this toy with symmetric relevance, observable-damage triage beats recent-activity triage by a large margin. Recent-activity allocation is worse than round-robin under binding scarcity. |
| What this does not establish | Anything about `e3/`, novelty beyond conventional ECC, learned relevance, unobservable rate learning, FEP, autopoiesis, autonomy or consciousness. |
| Files created or changed | All new and untracked. No tracked file was modified. See `git status`. |
| Verification completed | Four audits (equivalence, pairing, repair isolation, truth relabelling, loss model against Monte Carlo); freeze verification; a validated exploratory harness. |
| Next falsifiable question | In a world where some memories become permanently obsolete, does adding consequence information to damage-depth triage raise recall, and does the allocator stop paying for obsolete memories while staying viable? This needs a world-rule change and a new protocol. |

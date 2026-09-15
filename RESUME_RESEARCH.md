# Resume guide: Toward an Artificial Organism

## Current stopping point

The latest completed study is **AC10, the integrated constituent ablations**
(`AC10_RESULTS_v1.md`, `ac10_results_v1/results.json`, 72 rows, seeds 1300–1303).
It closes the requirement that stood open since AC1–AC4: every produced
constituent is now ablated **inside** the integrated AC9 body, and the enclosure's
function is separated from its matter.

Main results, all nine prespecified gates passing:

- Removing **W production** leaves no entry ever allocated (0/8) and kills all
  eight individuals at 248–252.
- Removing **C production** confines conversion to the inherited endowment (zero
  assay conversion) and kills all eight at 200–232.
- Removing **B production** exports constituents in 8/8 and loses both routes at
  195–279; activity still reaches 0.355 by random fallback, so survival is not a
  proxy for organization.
- **Forced retention with zero enclosure matter** (`no_B_retention`) and
  **external B supply** (`B_rescue`) both hold routes 8/8, completion 8/8 and
  zero export. The enclosure's causal contribution is retention, not mass.
- Suppressing W or B production only **after** development still destroys the
  acquired routes (599–609 and 647–857): the requirement is continuous
  maintenance, not a one-time acquisition.

Before it, the frozen baseline is **AC9 controls v3** (`AC9_CONTROLS_RESULTS_v3.md`):
acquired functional organization is maintenance-dependent where it is physically
located, with relocation, inert-burden, protected-copy and oracle controls all
run. AC9 v1 is preserved as a negative result and v2 as the first-stage pass.

## Exact resume commands

Any Python 3.12 with NumPy suffices. On this host the project has its own venv
(3.12.3 / NumPy 2.5.3); the default system `python3` has no NumPy:

```bash
cd ~/projects/Toward-an-Artificial-Organism
export OPENBLAS_NUM_THREADS=1

# AC10: tests, frozen-table audit, sampled exact replays, and a 14 s full rerun
.venv/bin/python -B -m unittest test_ac10
.venv/bin/python -B audit_ac10.py        # uses the frozen table, does not rerun
.venv/bin/python -B replay_ac10.py       # 11 sampled conditions, exact
.venv/bin/python -B ac10.py              # refuses to overwrite ac10_results_v1

# AC9 controls v3 remains frozen and audited
.venv/bin/python -B audit_ac9_controls_v3.py
```

Every runner uses `mkdir(exist_ok=False)`, so a re-run raises rather than
overwriting frozen results. Changed experiments need a new versioned protocol and
a new results directory; the v3 and AC10 directories are frozen.

Regression suite before extending anything:

```bash
.venv/bin/python -B -m unittest test_ac1 test_ac2 test_ac3 test_ac4 \
  test_ac4_transport test_ac5 test_ac5_program test_ac6 test_ac7 test_ac8 \
  test_ac9 test_ac9_memory test_ac10      # 77 tests, about 6 s
```

The docs' original commands (`py -3.12-arm64 -B ...`, `C:\Users\ahern\...`) are
the author's Windows machine, not this host.

## What to do next

## Current state (AC20–AC28): the broader-developmental-function line

The older open item — "a broader developmental function than the present four routing classes and
two unknown bits" — was worked from AC20 to AC28, and it produced a sharper problem than it started
with, correcting the framing by measurement twice:

- **AC24 (effective bits).** The frozen controller's four rule positions are worth **1.00 effective
  bit**, not the 4.58 of its permutation count: exactly one W region is active per individual
  (`activation` ties a region to the individual's history) and observation bit 5 is never set, so
  two positions can never fire. 24 permutations collapse to 2 behaviours. `AC24_FUNCTIONAL_v1.md`.
  The word "bank" had been doing three jobs — site group, trace bank, rule position — and the
  distinction is what the surprise hinged on.
- **AC25/AC26/AC27 (what makes an order learnable).** Order information comes only from
  confrontation. Singletons alone give **0.00 bits** however many signals are live. AC25 claimed
  pairwise co-occurrence suffices; **AC26 falsified that** — a world with all 15 pairs co-occurring
  reaches **680 of 720** orders, because a word is read by first match and a third signal pre-empts
  the comparison. The corrected criterion is an **exact pair witness** for every pair, and AC27
  shows 15 deliberate presentations suffice (107,774× sooner than letting coprime oscillators drift
  into every combination).
- **AC28 (chemistry).** Six W regions, one rule position each, signals derived from body state,
  births at the frozen price, conservation asserted every tick. The criterion is met (720 classes)
  and the controls reproduce 0.00 and 1.00 bits on the same measurement. The order is still supplied
  by the harness — **nothing has been acquired, stored or retained**, and the demand is imposed
  rather than emergent.

**Next target:** acquisition and retention over this six-position order — the AC16/AC18 shape, but
over 9.49 effective bits rather than a nominal 4.58 — then a protocol declaring the scale, the demand
schedule, and the two endpoints (random-fallback survival; acquired-function retention) separately,
before any final seed. Read `AC28_REGIONS_v1.md` first; `AC24_FUNCTIONAL_v1.md` explains why the
earlier "4.58 bits" framing was wrong.

### Older open items (kept for the record)

1. **The next target, and the strongest remaining claim**: test whether the
   controller can *acquire* the need to allocate or relinquish maintenance
   resources under an intervention chosen **after** development, with no
   protected copy and no externally fixed correct state.
   **AC11 attempted this and was falsified by its own pre-run engineering
   controls — do not run `AC11_PROTOCOL_v1.md` as written; read
   `AC11_DESIGN_CONTROLS_v2.md` first.** A state-blind fixed duty cycle (4/6)
   matches or beats every configuration of the adaptive arm (3/6 at thresholds
   N=2,4,8,16), so the outcome is reachable without an acquired decision. Two
   measured causes: renewal is **region-granular** while the usefulness boundary
   is per-key, which makes the optimal maintenance level intermediate and
   constant; and blind access at 1/4 success cannot fund even a reduced
   metabolism, so relinquishment only changes *when* the organism dies. The
   frozen economy and the AC11 regime each satisfy one requirement and violate
   the other.
   **Prerequisite before re-attempting**: (i) an allocation primitive whose
   granularity matches the usefulness boundary — **built and verified**
   (`ac12_memory.renew_alloc`; the register in the frozen program's dead rule
   reproduces the frozen rows exactly when all slots are maintained —
   `AC12_DESIGN_CONTROLS_v1.md`); (ii) an intervention that does **not zero the
   organism's income** — **now designed and calibrated**: make the affected port
   *unreliable* (a channel drawn per contact, so a stored value earns exactly what
   blind search earns) and drop the material yield at the same intervention. In the
   calibrated world (ports 4, yields 64 → 12 at tick 1024) `allocate` completes 6/6
   with phase-1 productivity 1.000 and phase-2 renewal writes 393 against
   `preserve` 5/6 with 662, `no_learning` 463, `fixed_schedule` 491, and
   `relinquish` 0/6 at 0.277 — see `AC13_CALIBRATION_v1.md`; (iii) a measured
   economy where the route is worth keeping while valid and useless maintenance
   still competes with the metabolism (solved: Y1=64, Y2=12; Y2=8 puts the drop's
   own payment on a knife edge and is excluded); (iv) rivals at the same
   granularity (implemented: spending-matched schedule, random, sham-write,
   protected); (v) the decision in vulnerable, paid, repairable state (unchanged).
   **Next step was `AC13_PROTOCOL_v1.md` — it is now UNFROZEN AND FALSIFIED:**
   the calibration's 41% saving did not replicate (12 fresh engineering
   individuals: mean −9.3%, range −311% to +99.8%; `preserve` matches the learner
   in 10 of 12). See `AC13_REPLICATION_v1.md`. **Structural limit, supported by
   three independent measurements (AC11, AC12, AC13):** with a single-bit resource
   port whose blind fallback is uniform over the same candidate set, the value of a
   stored route is either decisive *because fatal* (a wrong stored value zeroes
   income) or negligible (a stored value earns exactly what blind search earns), so
   the maintenance decision has no consequence between "forced by starvation" and
   "irrelevant". Do not design another learner for this line until an access-law
   primitive exists. Two candidates, each needing its own primitive and protocol:
   a **graded access law** (being wrong costs a fraction of the yield rather than
   all of it) and a **wider access channel with non-uniform fallback** (a stored
   value carries more usable information than a blind attempt can reach).
   **AC18 v1 is FROZEN AND ITS CLAIM PASSES — all eight predeclared gates** —
   `AC18_PROTOCOL_v1.md`, `AC18_RESULTS_v1.md`, `ac18_results_v1/`, seeds 2500-2503. The gate
   is a **separation of worst cases**: G1 learner's worst individual **1.000** (all 8), G2
   one-way's worst **0.429**, plus G3 (keeping arms exactly 0.000, no re-binding tick), G4
   (kept channel 1.000), G5 (three exact equalities), G6 (`restore_only` barred —
   structural), G7 (no blind rival reaches 0.90), G8 (all declared arms complete). Learner
   invariant at 1.000 vs one-way 0.429-0.800 and crude-relinquish 0.444-0.714: both rivals
   re-bind but neither holds. **Necessity confirmed on three seed families:** drop-only binds
   but cannot hold, restore-only never frees the key so the frozen deposit gate bars it
   (exactly 0.000, no re-binding), both directions together hold in every individual — so the
   two-way rule is necessary and sufficient in this machinery. **This closes the open item**
   (acquire the need to allocate/relinquish under a post-development intervention, no
   protected copy, no externally fixed correct state) subject to: behavioural/economic not
   survival-level; **not** generalized to both-channels-moving worlds (excluded by measurement
   in AC17's engineering, where the crude arm reaches 0.93); no optimality claim; nothing
   about consciousness/experience/autopoiesis. Verified by audit (all eight gates recomputed
   without simulating, 18 hashes, no drift), replay **8/8 exact**, 15 AC18 tests, **149 tests**
   in the full suite, and everything hashed up front. **Gate-shape lesson for any successor:**
   classify the claim first — "cannot hold" → separation of minima (AC18, passes); "worse on
   average" → a justified margin (AC16, falsified by 0.006); "better everywhere" → dominance
   exempting the ceiling (AC17, unsatisfiable as declared). Both earlier falsifications stand
   permanently.
   **Next frontier (the older open item):** a broader developmental function than the present
   four routing classes and two unknown bits, keeping random-fallback survival and
   acquired-function retention as separate endpoints.
   **AC17 v1 remains FROZEN AND FALSIFIED on an unsatisfiable gate** (`AC17_PROTOCOL_v1.md`,
   `AC17_RESULTS_v1.md`, `AC17_ENGINEERING_v1.md`, `ac17_results_single_v1/`, seeds 2300-2303).
   G1 PASS (learner 1.000 in **8/8**), G3 PASS (keeping arms exactly 0.000, no re-binding tick,
   every individual), G4 PASS, G5 PASS (three exact equalities), G6 PASS, G7 PASS, G8 PASS;
   **G2 FAIL** because strict per-individual dominance is **unsatisfiable at the ceiling** — on
   2 of 8 individuals one-way also reached 1.000. The claim's true shape is a **separation of
   worst cases**: learner minimum 1.000 vs one-way minimum 0.462, i.e. one-way cannot
   *guarantee* holding while the learner can; that gate was not declared in advance so it is
   not this study's result. **AC17's new knowledge is structural:** `restore_only` scores
   exactly 0.000 with no re-binding (predicted from the frozen deposit gate), so with AC16's
   drop-only result **both directions are necessary and neither suffices alone**. A third
   claim (both channels moving) was killed in engineering — the crude always-relinquish arm
   reaches 0.93 there vs the learner's 0.75 — and the world is excluded rather than reframed.
   **Next (AC18):** declare a **separation of minima** gate (learner min ≥0.90 AND one-way min
   <0.90) plus G3-G8 unchanged, on fresh seeds, protocol hashed first. **Two consecutive
   falsifications were by gate shape, so derive gates from the claim's logic: a "cannot hold"
   claim is a worst-case statement.** Do not re-run AC16 or AC17 with better-chosen gates.
   **AC16 remains FROZEN AND FALSIFIED** on its mean-margin gate (mechanism intact: keeping
   0.000 ×8 / one-way 0.636-0.889 / two-way 1.000 ×8).
   **AC16 v1 remains FROZEN AND FALSIFIED on its mean-margin gate** (`AC16_PROTOCOL_v1.md`,
   `AC16_RESULTS_v1.md`, `ac16_results_v1/`, seeds 2100-2103).
   First, the mechanical answer to what AC15 left open: the frozen deposit path is gated on
   `grow` and the frozen runner stops growth at t=512, before AC15's t=1024 intervention —
   **AC15 had re-acquisition switched off**, which is why its learner never bound a correct
   route. AC16 opens that window and adds a **restore** primitive symmetric with the drop
   (relinquish on a failure streak, restore maintenance on a productive contact, both paid
   per replica, same vulnerable bank). Result: **G1 PASS** (learner holds a correct route at
   **1.000 in all 8 individuals**), **G2 FAIL** (+0.2437 vs the predeclared +0.25), **G3
   PASS** (keeping arms exactly 0.000, never a re-binding tick), **G4 PASS**, **G5 PASS**
   (all three consistency equalities exact, `restore_disabled` == one-way `allocate`),
   **G6 FAIL** (`relinquish` dies 4/8 — not in the falsification list), **G7 PASS**. The
   protocol's own clause falsifies the claim on G2, and the protocol and threshold were
   **not** amended. The categorical pattern is exactly as predicted and is a three-way
   separation: keeping arms **cannot re-bind at all** (the frozen gate needs
   `selected is None` — structural control, no scaffold), one-way relinquishment **binds but
   cannot hold** (0.636-0.889), two-way **holds at 1.000 ×8**. The learner strictly dominates
   one-way in **8/8 individuals** (+0.111 to +0.364); only the mean margin missed.
   **Next version (AC17):** declare *dominance and categorical* gates in advance on fresh
   seeds — learner ≥0.90 in **every** individual, every keeping arm exactly 0.000 with no
   re-binding tick, strict per-individual dominance over one-way — and no margin over a
   partially-succeeding rival. Do **not** re-run AC16 with a better-chosen threshold.
   **AC15 remains FROZEN AND PASSED** (`AC15_PROTOCOL_v1.md`, `AC15_RESULTS_v1.md`,
   `ac15_results_v1/`, seeds 1900-1903, 64 rows, all five prespecified gates PASS).
   After an unannounced post-development move of **one** channel (asymmetric: material
   goes stale, fuel stays valid — moving both makes "drop everything" optimal and cannot
   discriminate), the learner relinquishes the stale route and keeps the valid one:
   kept 1.000, moved 0.398, mean **0.699** versus `preserve` 0.500 and `relinquish` 0.439,
   with every individual relinquishing exactly one slot and none dying (64/64). No
   state-blind rival reaches it (all fixed duties 1-8 and random p∈{0.25,0.5,0.75} sit at
   exactly 0.5000). G3 holds exactly: duty 1/1 and an unreachable streak reproduce
   `preserve` including the state hash. Verified by `audit_ac15.py` (coverage,
   invariants, hashes, gates recomputed) and `replay_ac15.py` (**6/6 exact**), plus 13
   tests. Two honest limits: **no blind rival ever lets the stale entry lapse** (these
   arms choose whether to *renew*, and renewal stays frequent enough that the 64-tick
   entry never expires), so G2 is real but weak; and the learner's own threshold makes no
   difference (0.6989 for streaks 2/4/6/8) — the learner beats every rival at every
   setting, so no selection was needed. **Not established: re-acquisition** — the learner
   relinquishes the stale route, it does not learn a correct new one (moved 0.398 ≈ blind
   search ~1/2, not better), and every keeping arm showed productivity 0.000 afterwards.
   That stronger claim is the next target. **Deviation disclosed:** the first final run
   used seeds 1800-1803 because the runner still held a placeholder seed family; the
   protocol was NOT amended, the deviating run is preserved at
   `ac15_deviation_seeds1800_v1/`, and the corrected run stands. Both seed families give
   the same verdict, which is a robustness check the protocol did not require.
   Note the stated limit of the whole line: what replicates is the decision
   *machinery* (outcome-driven, paid, vulnerable, correctly targeted); what does not
   replicate is a distinct economic consequence for it.
   Carried forward: the lineage's optimum level of memory maintenance is
   intermediate, not all-or-nothing — which explains AC6's "no net material
   saving" and why the AC9 v1→v2 stored rule-order change mattered so much.
2. **Framework-aligned and independent of the blocked allocation line: test
   whether the organism's own decision state is a maintained constraint whose
   degradation propagates into its own decisions — closure, not a chain.**
   The machinery is in place and verified (the allocation register lives inside
   `traces[0,:126]`, is flipped by the same damage stream, and is repaired only by
   the paid bank-0 repair, gated by core W, which the program itself produces).
   **v2 done, negative and not close (`AC14_CLOSURE_v1.md`).** Making the register
   genuinely at risk via a declared read convention (relinquished when ≥
   `REGISTER_THRESHOLD` replicas are set: 4 = majority, 1 = a single designated
   replica) and re-running `closed` vs `no_repair` at both conventions: at 1-of-7 the
   register *does* read wrong, first at the **same tick** with and without the repair
   loop (77, 798, 216), and cutting the loop changes nothing — identical final
   register state, occupancy, contacts and survival. At 4-of-7 the register never
   reads wrong in any arm. **The decision state's integrity is not maintained by the
 loop that repairs the bank it lives in**; its dominant dynamics are the organism's
 own writes and a self-reversing (XOR) damage stream. Why the wrong read has no
 consequence (corrected — an earlier reading of `demand` as "one entry, half the
 register inert" was wrong): `demand()` counts live cells per region and a live slot
 is 3 bits × 7 replicas = 21 cells, so [42,0] means **two live entries in region 0**,
 governed by exactly the register bits that read wrong. The real reason is that the
 register is **sampled only when a renewal action (3/4) is chosen, and the damage is
 transient** — the first damaged read lands at 77/798/216 and self-reverses, so a
 wrong state rarely coincides with a renewal opportunity, which is why contacts are
 *identical* to the tick in both arms rather than merely similar.
 **Requirements before retrying:** (1) **persistent corruption of the register** —
 either a higher program-bank damage rate (order 1e-3–1e-2 per replica per tick, so
 several replicas of one bit are set at once and the read survives to the next
 renewal; the read threshold and the rate must be chosen together and declared), or
 a non-self-reversing damage model for the program bank (a flip that stays flipped
 until repaired) — the more interesting option because it makes repair load-bearing
 by construction and needs its own protocol; (2) the single-replica read convention,
 now implemented as `REGISTER_THRESHOLD` in `ac12.py` (default 4 = majority).
   One datum still **unexplained and not used for any claim**: at tick 36 from
   identical initial states the live arm records `spent_m=4, writes=4` while the
   protected arm records neither, though `_drop` writes all seven replicas at once
   and no drops are logged; next diagnostic is to instrument `_drop` with its
   `place`, `n` and `cap` per invocation.
3. Add a broader developmental function than the present four routing classes and
   two unknown bits, keeping random-fallback survival and acquired-function
   retention as separate endpoints.
3. Preserve exact replays, source hashes, ledgers and negative controls. Any
   successful result must survive protected-memory, relocation, inert-burden and
   read-disabled comparisons.

Useful standing facts: activity is a poor proxy for organization (AC10 shows
three arms acting long after route loss); `policy_accuracy` of the program bank
does not discriminate at the current horizon and flip rate; eight independent
individuals per study is the working sample size.

Do not resume the stopped E3 v0.11 experiment or reinterpret the current results
as proof of full autopoiesis. The next breakthrough must show that the system's
own maintained organization changes its maintenance decisions under
counterfactual damage or scarcity, with no protected copy or externally fixed
correct state.

# M5 — Frozen harness design, analysis plan, and run budget (estimator-monitoring feasibility comparison)

2026-09-25. Design deliverable for the M5 card (t_7e673e39). Predecessor: M4
(t_6145d172, `M4_MONITOR_INPUT_AUDIT_v1.md`), which returned the identifiability verdict M5 is
conditioned on. This document **commits the harness design + analysis plan + run budget BEFORE
evaluation**. It runs nothing, freezes nothing, re-hashes nothing, and edits no frozen artifact.
M6 implements and carries the scientific claims; M5 freezes the design those claims are gated on.

One sentence up front: **the harness tests the M3 monitor `m` against the scoped referent — the
DAMAGE component of "the decoded first-order estimate `e` is wrong" — in the AC110 cut world's
post-window damage regime, with two separated hypotheses (PREDICTION: `m`'s readout tracks
wrongness; CONTROL: consuming `m` improves repair scheduling), five rivals (fixed-duty, the
obs-bit-2 reflex, a transient direct policy, a history-based predictor, and `m` itself), and a
prespecified split of 8 engineering seeds + 16 final seeds.**

---

## 1. Scoped referent and regime (what M4 hands over, restated as constraints)

M4's verdict: the referent "P(decoded `e` is wrong)" splits by observability. Only the
**damage-induced** component is identifiable; the **staleness** component is unidentifiable; and
the **pure primary decision window [8192, 8288) has no error variance** (the discriminator writes
`e` before the consumption reads it, so `e` is ceiling-accurate there). Three consequences bind
this design:

1. **The referent is `e`'s wrongness from storage damage only**: the estimate's majority flips to
   the wrong value after a write, under the frozen sticky-SET stream (`b.traces[0,:126] |= core_flips`,
   1e-4 per replica per tick). Acquired value 1 = E_world; under cut the discriminator writes 0 =
   E_machinery; a flip 0→1 is therefore toward error. "Last write was 0 AND `ones ≥ 4`" is the full
   observable damage-wrongness condition (`ones = traces[0, bel_off].sum()`, the DIRECTIONED count).
2. **The regime is the cut condition, post-window [8288, 16384).** There the discriminator has
   finished (no open in-window contact to re-fire), `e` is latched at 0, and the ambient stream
   degrades it toward 1 — exactly the AC110 G4 drift (maintained holds 16/16, no_repair drifts 8/16
   on finals 6200–6207). This is where `e` is *sometimes wrong for implementation reasons*, so a
   monitor has variance to predict. `move` is the P1 decoupling control (e is acquired 1 and
   sticky-SET is a no-op: e is correct and can never be wrong). `no_cause` is the clean control.
3. **The staleness component (case 2 of M4 §3) is recorded as an unavoidable miss, never scored as
   a gate.** It is observationally identical to "intact and correct"; no permitted observation can
   separate it (the separator is the cause, which is evaluator-only).

## 2. The four discriminating cases (the target events; M4 §3, re-stated as harness invariants)

Each is a `(bookkeeping → truth)` point the harness must produce and the monitor must resolve.
All are read off the substrate, never host logs.

| case | substrate state | truth (`e` vs cause) | correct monitor readout | the rival it discriminates against |
|---|---|---|---|---|
| 1 — damaged-but-correct | `ones=3`, decoded 0, majority intact | CORRECT | **reliable** (no false alarm at the still-correct boundary) | pins the READ convention/threshold |
| 2 — intact-but-stale | storage untouched (`ones` = written value) | WRONG | **unavoidable MISS** (record, do not score) | none — structural blind spot |
| 3 — wrong, reflex-silent | `ones=4`, majority flipped, obs bit 2 silent (single bit contributes `min(4,3)=3 < 4`) | WRONG | **unreliable** (the catch) | the obs-bit-2 reflex (misses it) |
| 4 — correct-but-short | resource stress fires (W<2 / material≤64 / fuel≤8 / cap would refuse), `ones ≤ 3` | CORRECT (now) | **unreliable as LEADING indicator** (declared false alarm vs current wrongness) | pins the resource-signal mapping |

Non-vacuity: the harness MUST be verified in engineering to produce cases 1, 3, 4 at a measurable
base rate (case 3 in particular is the low-base-rate single-bit event). If the ambient rate yields
case 3 too rarely to score, the fix is a longer horizon or a disclosed elevated BEL_DAMAGE (an
engineering diagnostic in ac110.py, NOT a frozen-law change) — never a silent acceptance of an
empty cell. State the base rate and the read threshold together (AC14/AC69).

## 3. The candidate monitor `m`

**Substrate.** A stored, maintained state in a locus DISTINCT from `bel_off` (the estimate's dead-rule
action bit) and from the AC116 counter's free bits — a dead-rule free-bit set or recipe-bank (bank 1)
free bits. Requirements: majority-read (≥4/7), W-gated paid writes, IN the damage stream (vulnerable),
and re-derived from substrate at scoring time (observer-discard survives — never read from the runner's
host-side `bel_events`/`bel_refused`/`bel_minority` fields).

**Inputs (M4's corrected list).** (1) the DIRECTIONED per-bit count `ones` at `bel_off` — not the
collapsed `bel_minority = min(ones, 7−ones)`, which is non-monotone (0,1,2,3,3,2,1,0) and zero at the
most-wrong state (`ones=7`); (2) the RETAINED write-value (last `bel_write` value, 0/1), a paid
maintained record — the direction knowledge that breaks the `ones ≥ 4` ambiguity; (3) the SHARED frozen
signals: obs bit 2 (whole-bank corruption, `min(ones,7−ones).sum() ≥ 4` over 126 bits) and the resource
signals (W count `available(b)[:4]`, fuel/material starvation bits obs 0/1/6/7). The `repair_at_risk`
predicate (the case-4 leading indicator) is DERIVED from these resource signals (W<2 / obs bit 6,
material ≤ 64 / obs bit 1, fuel ≤ 8 / obs bit 0, or `_cap = min(32, 8·W, energy, material)` would refuse
the needed write), not read as a separate counter (M4 §2b).

**Readout.** A coarse ordinal reliability judgment `r ∈ {0,1,2,3}` (0 = certainly correct, 3 = certainly
wrong), plus its categorical threshold {reliable (`r<2`), unreliable (`r≥2`)}. The categorical rule:

```
unreliable  iff  (last_write == 0 AND ones >= 4)          # damage-wrongness (case 3)
              OR (last_write == 0 AND repair_at_risk)     # leading indicator (case 4)
reliable    otherwise                                     # incl. move (last_write == 1, ones == 7)
```

where `repair_at_risk` is the resource-stress predicate DERIVED from the shared resource signals
(W<2 / obs bit 6, material ≤ 64 / obs bit 1, fuel ≤ 8 / obs bit 0, or `_cap` would refuse the needed
write) — a leading indicator that repair is about to fail, NOT a second counter (M4 §2b). The graded
`r` is the coarsened directioned count: `r = min(3, ones)` when `last_write == 0`, `r = 0` when
`last_write == 1`, with case 4 contributing a declared `r = 3` even when `ones ≤ 3`. Gradedness is
an implementation detail (M3 §3); the referent is fixed by the categorical rule, not the granularity.

**Control action (H2).** When `m` reads unreliable, schedule a **targeted paid repair of `bel_off` to
the retained last-written value** (write the flipped replicas back to 0), W-gated by `_cap`. This is a
per-bit write primitive (bounded by `min(32, 8·W, energy, material)`), NOT action 2's whole-bank
majority-restore — because a single estimate bit contributes at most 3 minority replicas and can NEVER
trigger obs bit 2's whole-bank threshold (AC110 rule 1 / AC76). The monitor's causal role is the
MAINTENANCE direction only (when to spend a repair write, scheduling of `e`'s repair/renewal); it never
feeds the hold-vs-drop decision, which is `e`'s job.

## 4. The rival set (strong rivals, not strawmen)

All arms share the first-order machinery — the C2 occluded-`used_held` gate (q=0.5), the discriminator
that writes `e` on open contacts, and the frozen streak/hold consumption. Arms differ ONLY in the
maintenance policy of `e` (and, for the monitor, in whether they store `m`). The shared-vs-private split
(M4 §1): inputs 2/5 (obs bit 2, resource signals) are SHARED; inputs 1/4 (directioned count, retained
write-value) are CANDIDATE-PRIVATE.

| arm | readout (H1) | maintenance policy (H2) | what it isolates |
|---|---|---|---|
| `monitor` | `m` (directioned count + retained write-value + shared) | repair `e` when `m` reads unreliable | the candidate |
| `fixed_duty` | — (state-blind) | repair `e` on a FIXED schedule, spend-matched to `monitor` | content inertness (P5) |
| `reflex` | "unreliable iff obs bit 2 fires" | obs bit 2 → whole-bank repair (action 2) only | the existing watchdog (null) |
| `direct` | "unreliable iff `ones ≥ 4`" (transient, no retained write-value) | repair `e` when it reads unreliable, toward the current majority (a no-op) | the value of retention/direction |
| `history` | a counter over the shared bookkeeping history (e.g. corruption-event count since last repair) | repair `e` when the counter crosses a threshold | "any history" vs "e-specific readout" |

Design notes that make these genuine:

- **`fixed_duty` is SPEND-MATCHED.** Its repair period `K` is tuned on the ENGINEERING cohort so its
  total `e`-repair write count ≈ the `monitor` arm's, so a utility advantage cannot be bought by
  unbounded extra spend (AC11's lesson, at the maintenance layer). Report the matched spend explicitly.
- **`direct` has no direction, by construction.** It reads `ones ≥ 4` (majority flipped) but does not
  retain the write-value, so it cannot tell "drifted toward 1 under cut (wrong)" from "acquired 1 under
  move (correct)". It false-alarms throughout the move world (P1) and cannot repair toward the right
  value (repairing toward the majority is a no-op; repairing toward 0 would corrupt `e` under move).
  This is the monitor's discriminating content, isolated as a rival rather than folded into the monitor.
- **`history` is state-blind to `e`.** It accumulates a generic corruption/failure history but does not
  read `e`'s own replicas or write-value (C2's r4 lesson: "any history helps" vs "attributed history helps").
- **`reflex` is the correct null.** It has inputs 2/5 (shared) and lacks 1/4 (candidate-private), so it
  CANNOT catch case 3 (single-bit miss). P5 is non-vacuous because the reflex genuinely lacks the
  estimate-specific content.

**The ε-estimator arm is OMITTED, deliberately.** The ε-estimator (C0/C4) estimates the residual yield
ε — a first-order CHANNEL-QUALITY parameter that addresses the STALENESS/quality confound. M4 scoped the
referent to the DAMAGE component, which ε does not address. Adding it would be an irrelevant arm for the
appearance of completeness, which the card forbids. It is recorded as out-of-scope, not forgotten.

**Causal-role controls (engineering-level, P4).** `scramble_m` (force `m`'s read to reliable → repair
never fires) and `scramble_e` (force `e`'s read → decision changes, maintenance unchanged), on the
AC116 `scramble` pattern (split the read: true value for the update, force only the decision read).

## 5. The two hypotheses, separated

**H1 — PREDICTION ("`m` tracks estimate/decision error at relevant times").** Scored on the `fixed_duty`
trajectory (repair held at the fixed schedule, so `e` is ALLOWED to drift and the four cases arise). At
every decision tick (a channel-1 contact, `t ≥ 8192`), record the four readouts {`monitor`, `reflex`,
`direct`, `history`} computed from the SAME per-tick bookkeeping, and the evaluator truth
`decoded e(t) != cause(t)`. The `(readout, truth)` series is the prediction evidence. The four readouts
are functions of one trajectory, so this costs one run per (seed, history, condition), not four.

**H2 — CONTROL ("consuming `m` improves checking/maintenance decisions relative to rivals").** The five
full arms (`monitor`, `fixed_duty`, `reflex`, `direct`, `history`), each consuming its maintenance policy,
compared pairwise (monitor vs each rival) on utility and cost endpoints.

Why the two are separate: `m`'s control action removes the wrongness its readout predicts. Scoring the
readout on the control-active trajectory would compress the informative cells (case 3, 4) into single-tick
transients. Scoring on the `fixed_duty` trajectory decouples readout from control and guarantees the cases
arise. H1 and H2 are then independent: H1 is about the READOUT, H2 about the POLICY.

## 6. Metrics (utility and resource cost measured separately)

**H1 — prediction.** (a) *Calibration*: binned reliability diagram of the graded `r` vs observed
`P(e wrong | r)`, summarized by expected calibration error (ECE). (b) *Proper scoring*: Brier score of
the candidate's declared `r → p_wrong` mapping (treat the categorical latch as `p ∈ {0, 1}` where the
graded form exists, or score the graded `r/3`); log-loss where the graded form is defined. (c) *Error
discrimination*: AUC of `r` against the truth, plus the categorical 2×2 type-2 table (hit / false alarm /
miss / correct rejection) with false-alarm rate and miss rate. (d) *Case-level*: the four cases of §2
resolved per-case (case 2 recorded as a miss, excluded from any pass/fail).

**H2 — control.** (a) *Utility*: per-seed post-window route-1 retention (fraction of ticks in
[8288, 16384) with route-1 bound) and post-window channel-1 income; first acquire/loss times. (b) *Cost*:
total writes, `reg_writes`, the targeted `e`-repair writes, `m`'s own write + repair writes,
`proactive_writes`, energy/material spent — reported as a SEPARATE table, never folded into the utility
number. (c) *Viability*: `completed`, `first_dead`, reported as a bimodality-aware LOWER bound (AC68),
never a gate.

## 7. Gates (prespecified; engineering informs endpoints, not outcomes)

H1 (prediction) gates — all on the pooled readout-truth series, cut condition, finals:

- **P-G1 (case-1 read convention).** At `ones=3` (damaged, still correct), `m` reads reliable — no false
  alarm at the still-correct boundary. (Pins the threshold; a monitor flagging `minority>0` fails here.)
- **P-G2 (case-3 catch over the reflex).** At `ones=4` with obs bit 2 silent, `m` reads unreliable and
  `reflex` reads reliable (the reflex misses the single-bit flip). This is `m`'s discriminating value.
- **P-G3 (case-4 leading indicator + move decoupling).** Under cut with `repair_at_risk` (resource
  stress) and `ones ≤ 3`, `m` reads unreliable (declared false alarm vs current wrongness); under move,
  the same resource signals fire while `e` is correct-and-inert, and `m` reads reliable.
- **P-G4 (P1 referent separation).** Under move, `m` reads reliable throughout, while `reflex` reads
  unreliable whenever obs bit 2 fires (on other corruption) and `direct` reads unreliable (ones=7≥4).
  `m` is decoupled from both; if `m` tracks them, its referent is damage, not correctness → falsified.
- **P-G5 (calibration/proper scoring).** `m`'s ECE ≤ each rival's, and its Brier score ≤ each rival's.
- **P-G6 (discrimination).** `m`'s AUC > each rival's AUC.

H2 (control) gates — pairwise monitor vs each rival, finals:

- **C-G1 (intervention validity / clean control).** In `no_cause` and `move`, all five arms are
  byte-identical (`state_hash`) — the maintenance policies are inert where `e` is 1 (sticky-SET no-op)
  and there is no cause. (AC110 G1/G5 pattern.)
- **C-G2 (utility).** Per-seed post-window route-1 retention (and income) of `monitor` ≥ each rival's,
  tested by the paired exact sign-flip on per-seed differences (see §9 for the resolvable floor).
  Categorical, so gated on per-individual dominance or separation of minima — NOT a mean margin
  (AC16/AC17).
- **C-G3 (content inertness, P5).** The spend-matched `fixed_duty` rival does NOT reproduce `monitor`'s
  maintenance behaviour (they differ on repair scheduling and/or the utility endpoint). If it does,
  `m`'s stored content is inert → falsified (AC109 one level up).
- **C-G4 (causal role, P4; engineering).** `scramble_m` changes repair/renewal behaviour while the
  hold-vs-drop decision is unchanged; `scramble_e` changes the decision while maintenance is unchanged.

Reported, not gated: survival (bimodality-aware lower bound), resource cost (separate table), the
case-2 staleness miss, and the move-world completion/survival (a route-move consequence, not a monitor
effect — AC110 G5).

## 8. Non-vacuity / anti-scaffold checks (engineering, before the protocol)

1. **Repair reachability (the card's "verify the repair can change the error outcome").** Instrument the
   `monitor` arm's targeted repair: confirm it FIRES on `bel_off` within the decision window after a
   damage flip and flips `e` back to correct within a bounded number of ticks, and that this changes a
   downstream decision (proactive renewal resumes / the entry does not lapse). A repair primitive that
   cannot be reached or cannot change `e`'s wrongness is a non-starter (AC110 rule 1; AC91's timing flaw).
2. **Observer-discard / re-derive-from-substrate.** Assert every monitor input is a function of
   `traces[0]`/`traces[1]`/the frozen observe, and that zeroing the host-side log fields leaves every
   arm byte-identical (AC95-D4). No `bel_events`/`bel_refused`/`bel_minority` host fields may feed `m`.
3. **Four-case base-rate check.** Measure the per-tick frequency of cases 1, 3, 4 on the engineering
   `fixed_duty` trajectory; record it. If case 3 is too rare to score, declare the elevated-damage
   diagnostic (with the rate and read threshold stated together) or a longer horizon — do not proceed
   with an empty cell.
4. **Spend-match verification.** Confirm the tuned `fixed_duty` `K` produces total `e`-repair spend
   within a declared tolerance of `monitor`'s, on the engineering cohort, before the finals.

## 9. Evaluation split, run budget, and statistical resolution

**Replication unit.** The seed. `history ∈ {0,1}` is a within-seed secondary measure: the deterministic
arms (monitor/fixed_duty/reflex/direct/history, all non-coin-driven) produce byte-identical histories
(the step's activation is `[True,True]`, mapping is seed-derived), so N seeds = N independent units and
the 2 histories are correlated duplicates (the AC116/R1 finding). Any arm with a per-history RNG (e.g. a
coin in `fixed_duty`/`direct`) must derive it deterministically from `(seed, history)` and disclose it;
no statistic may treat the 2 histories as independent.

**Split.** Engineering: seeds 0–7 (16 individuals), all arms × all 3 conditions, plus the causal-role and
non-vacuity checks. Disclosed here, EXCLUDED from the finals, used only to (a) verify the four cases
arise, (b) tune the `fixed_duty` `K` (spend-match) and the `direct`/`history` thresholds, (c) inform gate
shapes. Finals: a fresh disjoint family of 16 seeds (proposed 6800–6815, 32 individuals; confirmed
disjoint from AC107 6000s, AC108 6100s, AC110 6200s, AC111 6300s, AC115/AC116 6600s at freeze time).
Run ONCE after the M6 protocol is hashed.

**Run budget (rows).** Each row ≈ 3.7 s on this host (measured on ac110.py this session).

| pass | arms | conditions | seeds × histories | rows | est. time |
|---|---|---|---|---|---|
| engineering (screening + checks) | 5 arms + 2 causal-role + diagnostics | 3 (cut/move/no_cause) | 8 × 2 | ≈ 320 | ≈ 20 min |
| finals (confirmatory) | 5 arms | 3 | 16 × 2 | 480 | ≈ 30 min |
| (H1 readouts ride the `fixed_duty` trajectory — no extra rows) | — | — | — | 0 | — |

Total ≈ 800 rows, ≈ 50–55 min wall + overhead. This is the finite budget; no post-hoc extension.

**Statistical resolution (checked BEFORE running).** The H2 utility gate is the paired exact sign-flip
on per-seed differences. Two-sided p for k nonzero same-sign differences of n effective is
`2 · (1/2)^n_eff`. At n=8 all-positive this is `2/256 = 0.0078`; but ties shrink `n_eff` — AC116 had
5 positive + 3 tied, so `n_eff = 5` and p = `2/32 = 0.0625` (the SMALLEST attainable at effective n=5,
per M2). To escape that floor the finals use **16 seeds**: all-positive gives `2/65536 ≈ 3.1e-5`; 12 of
16 positive (4 tied) gives `≈ 0.0005`. The discriminating seeds are the ~half where the drift matters
(AC110 G4: drift 8/16), so 16 finals give headroom the 8-seed AC116 ceiling lacked. The gate is stated
as dominance/separation-of-minima, not a mean margin, so it is not knife-edge at the ceiling (AC17).

H1 gates are within-run scorings over the pooled `(readout, truth)` series; with 16 seeds × 2 histories
× ~8000 post-window ticks each, the base rates are estimated to engineering precision and the AUC/ECE
comparisons are dominated by systematic (calibration) error, not sampling noise. The case-3 base rate is
the binding resolution constraint and is checked in §8.3.

## 10. Claim ceiling and falsification scope

**If every gate passes**, the strongest wording the result earns: the organism maintains a second-order
state whose referent is the **damage component** of its first-order estimate's correctness, computed from
its maintenance bookkeeping (directioned count + retained write-value + shared signals), dissociable from
the estimate by selective damage (P-G4), calibrated and discriminating against shared-bookkeeping rivals
(P-G5/G6), and causally effective on maintenance (C-G2/G3/G4) — **meets candidate indicator HOT-2 at
degree Y**. Not licensed: "metacognitive" unqualified, "monitors its own reliability" (the undefined
label), any claim about the staleness component, any level-(e) wording.

**A negative result is precise:** `m` is falsified if (a) the spend-matched `fixed_duty` reproduces its
maintenance behaviour (P5 — content inert), or (b) its readout is matched by the transient `direct` policy
(retention is inert) and does not beat it, or (c) its readout tracks damage/obs-bit-2 rather than
correctness (P-G4 — the referent collapses to the substrate). That concerns THIS design and THIS target;
it does not close the reliability tier "for real" (C0's over-reach, corrected in C1).

## 11. What this hands to M6

M6 implements, on the AC110/AC116 world: `m` in a distinct maintained locus with the §3 inputs; the four
readouts and five control arms of §4; the two separated hypotheses of §5; the §6 metrics; the §7 gates;
the §8 non-vacuity checks; the §9 split/budget. M6 writes the hashed protocol (source list + this design
doc) and runs engineering then finals. The referent, once, for the record: **the damage component of the
first-order estimate `e`'s correctness.**

## Sources

`ac110.py` (damage stream `:357`, GatedEstimator discriminator `:145–162`, evaluator scoring
`:341,399–410`), `ac107.py` (`bel_off`/`bel_read`/`bel_write` `:102–126`, Estimator consumption
`:243–302`), `ac116.py` (arms/finals, `scramble`/`no_write`), `ac9.py` (`observe` `:52–67`, obs bit 2
`:56`), `ac95.py` (`_cap` `:336`, `maintain`, `resolve_offsets`), `ac106.py` (ReadCut, `bel_minority`),
`M3_MONITOR_TARGET_v1.md`, `M4_MONITOR_INPUT_AUDIT_v1.md`, `AC110_PROTOCOL_v1.md`,
`references/ac110.md`, `references/ac116.md`, `references/m4-monitor-identifiability.md`,
`references/c4-uncertainty.md`. This document is derived and is NOT hashed into any study's
`pre_run_snapshot.json`.

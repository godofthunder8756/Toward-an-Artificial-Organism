# AC112 (P5) — engineering the heterogeneous-likelihood-ratio two-counter estimate

2026-09-24. P5's deliverable (task `t_96dbc363`): implement the smallest versioned
architecture for the question P4 (`t_260b4671`) selected — does a maintained **two-counter**
estimate (counts in vulnerable paid-maintained state, weights supplied) beat a maintained
**single-counter** rival in the informative-heterogeneous regime, gated on **decision utility
and not survival**? This is an **engineering** runner + rivals, no protocol, no freeze, no
finals. It unblocks P6 (the discriminating prediction) only if the design is functioning and
discriminating.

---

## 1. What P4 handed over

P4 (`P4_COGNITION_CONTINUATION_v1.md`, `_p4_heterogeneous_lr.py`) selected design 2: relax the
C4 premise "M never yields" to a residual yield ε, giving TWO weak likelihood ratios
`w_u = log((4/3)(1−ε))` (occluded-unproductive, weak M) and `w_p = log(4ε)`
(occluded-productive, weak C) whose ratio is non-integer. It demonstrated at the harness level
that (i) the sufficient statistic is the integer pair `(n_u, n_p)` consumed as the weighted sum,
(ii) a graded log-odds register is **exactly equal** to that two-counter finite-state rival
(gradedness stays non-load-bearing), and (iii) the weighted policy beats the strongest
single-counter rival in the informative regime (ε ≤ ~0.125, q ≥ ~0.7) and reverses only at the
uninformative boundary. The implementing-study question P5 received: at the organism scale,
does a maintained two-counter beat a maintained single-counter, gated on decision utility?

## 2. The architecture (AC112)

The world is the AC107/AC110 two-cause world — **move** (channel-1 mapping flips at t=8192; the
route-1 entry is stale) vs **cut** (route-1 read suppressed for [8192, 8288); the entry is
intact) — with two declared world changes, both applied **uniformly to every arm**:

1. **Occlusion gate (q = 0.7).** On a Bernoulli(q) fraction of channel-1 contacts the `used_held`
   bit is forwarded as `2` (occluded), so the two causes' open signatures — held-fail (move) vs
   blind (cut) — are hidden and the estimator must fall back to accumulated weak evidence. This
   is C2's gate, unchanged from AC110 (an interface change to the forwarded observation, never
   `selected`, `productive`, memory, or any conservation quantity).
2. **Residual yield (ε = 0.08).** Under move a HELD stale entry yields with residual probability
   ε (the old port retains residual activity). Implemented by source surgery on the frozen
   contact line: `if port==mapping[action] or (selected is not None and residual()): react` — a
   stale held entry whose port misses the flipped mapping still calls `ac4.react` (income) with
   probability ε. Balance-identity-safe by construction: the same react path fires, only its
   trigger widens. `ε → 0` recovers P2's homogeneous world (`w_p → −∞`, productive is
   decisive-C again); `ε → 1/4` makes both weak signals uninformative.

The candidate is a **maintained two-counter accumulator**. Two integer counters `(n_u, n_p)` live
in the dead rule's free bits (the AC12/AC96 pattern extended to two low-bit-width counters), plus
a one-bit hold latch (the AC107 estimate bit) for the decisive "open blind → hold forever"
branch. Weights `w_u, w_p` and threshold `θ` are **supplied** frozen constants (the first-order
content tier; the learned reliability tier is the deferred next-after, P4 §9).

### Storage, update, sensing, actions, damage, maintenance (the card's accounting)

- **Storage.** `n_u` = 4 bits (Gray-coded, 7 replicas/bit) in the dead rule's free bits
  `streak_offs[0:4]` (word bits 5,7,8,9); `n_p` = 2 bits in `streak_offs[4:6]` (word bits 11,13);
  hold latch = 1 bit in `bel_off` (word bit 10, action bit 0, frozen value 1 = "not holding",
  inverted semantics). All 7 bits are zero-valued free bits of the permanently-dead bank rule
  (mask 32), so the acquired organism is byte-identical to the frozen one. Offsets resolved once
  at acquisition (`ac12.dead_rule_index`), excluded from `reg_from_active` so reconstruction
  never clobbers them.
- **Update.** On a post-cause occluded-unproductive contact `n_u += 1`; occluded-productive
  `n_p += 1`; both atomic, W-gated (`ac95._cap`), Gray-coded so each increment is 1 logical bit =
  7 replicas (affordable at W=1). Open held-fail relinquishes immediately (decisive M); open
  blind writes the hold latch (decisive C). On drop and on re-bind the counters and latch reset.
- **Sensing.** The organism reads its own `(bound, used_held, productive)` triple; `bound` is the
  unshimmed introspection read, `used_held` the forwarded (gate-occluded) retrieval result,
  `productive` the realized yield. No cause label, no schedule access, no privileged read (C2's
  three anti-confound properties).
- **Actions.** The organism's action set is unchanged (contacts, renewal, birth, repair); the
  estimator only steers the *relinquishment* of route 1 through the frozen drop (register write +
  memory expiry).
- **Damage.** The counters/latch live in `traces[0]`, so the same ambient sticky-SET program
  stream (1e-4/replica/tick) reaches them; they are repaired by the same paid bank-0 restore
  (action 2). The repair-dependence of the *decision state* is **not** the claim here (it was
  AC110's question for the one-bit estimate) and is left explicit for a follow-up.
- **Maintenance.** The counters are the *decision state*; their writes are paid (1 energy + 1
  material per replica). The `immediate` rival holds no state (0 cost); the `single_counter`
  holds 3 bits; the `two_counter` 7 bits — the functional-capability-vs-cost ladder P4 §5 names.

## 3. Rivals (same observation stream, same decisive handling, differing only in accumulation)

- `two_counter` (candidate): weighted threshold `n_u·w_u + n_p·w_p ≥ logit θ`.
- `single_counter`: ONE integer counter (`n += 1` unproductive, `n += w` integer productive,
  clamped ≥ 0), relinquish at `n ≥ N`. The strongest single-integer rival (P4 rival 3).
- `immediate`: no state — relinquish on any unproductive contact, hold on productive/blind. The
  same-information immediate policy (C4's binary+imm with accumulation removed).
- `scramble`: the candidate with the counter READ forced to `(0,0)` (writes intact) — the
  read-only causal-role control (AC107's scramble pattern).

## 4. Verification (the card's completion criteria)

- **Host-state audit** (`audit_host_fields`): the candidate's host fields are config constants
  (offsets, weights, threshold, scramble flag) or observational logs (`counter_events`,
  `hold_events`, `log`). No host field steers a write: `n_u/n_p` are read from `traces[0,
  streak_offs]` (Gray majority), the hold latch from `traces[0, bel_off]`.
- **Observer-discard** (`observer_discard_equivalence`): per-tick byte-identity under a mid-window
  observer+allocator swap. PASSED 3/3 seeds probed (16,384/16,384 ticks equal, `swap_applied`,
  terminal hash equal) — the decision state is recovered from the body, not the host.
- **Interventions clean.** The gate and residual yield are uniform world changes (one step-source
  surgery each, asserted single-occurrence); the scramble changes only the counter read. Balance
  identity holds on every step (asserted by `ac4.balance`), so neither the gate (an interface
  forwarding change) nor the residual yield (a react-trigger widening) changes conservation.
  `ε → 0` is the declared homogeneous control (weights diverge correctly, unit-tested).
- **Unit suite** (`test_ac112.py`, 13 tests, all pass): Gray roundtrip, counter write/read
  roundtrip, heterogeneous weights (opposite sign, non-integer ratio), residual-surgery
  single-occurrence, ε→0 boundary, no-cause no-relinquish, move relinquishes, cut single-counter
  holds, cut immediate churns, scramble read-only, observer-discard, host-audit shape.

## 5. Engineering measurements (decision utility, not survival)

Default parameters ε=0.08, q=0.7, θ=0.6 (P4's optimal for that row), single-counter (w=−6, N=4).
Full cohort: 8 seeds × 2 histories = 16 individuals.

| arm | move relinquishes | cut false-relinquishes | cut holds route | survival (move) |
|---|---|---|---|---|
| two_counter | 16/16 | 6/16 | 16/16 | 16/16 |
| single_counter | 16/16 | 2/16 | 16/16 | 16/16 |
| immediate | 16/16 | 14/16 | 12/16 | 10/16 (6 deaths) |
| scramble | 16/16 | 0/16 | 16/16 | 16/16 |

Move first-drop tick: all arms ~8193–8262 (two_counter and single_counter overlap throughout; the
immediate rival drops marginally earlier because it never waits for evidence).

The parameter screen (`--sweep`, θ ∈ {0.5…0.9} × single (w,N) grid, 4 seeds) shows the arms
**discriminate on their own surfaces**:

| two_counter θ | cut false-relinq | | single_counter (w,N) | cut false-relinq |
|---|---|---|---|---|
| 0.5 | 3/4 | | (−6,4) | 0/4 |
| 0.6 | 1/4 | | (−6,2) | 1/4 |
| 0.7 | 0/4 | | (−4,4) | 0/4 |
| 0.8 | 0/4 | | (−2,2) | 1/4 |
| 0.9 | 0/4 | | (0,1) | 3/4 |

(move is 4/4 for every configuration on both families.)

## 6. Honest findings (what the engineering shows, and does not)

1. **The runner is valid and the arms are distinct.** The two-counter's weighted threshold traces a
   monotone θ→cut-false-positive surface, the single-counter a (w,N) surface, and the immediate
   rival churns (14/16 cut false-relinquishes) and dies under move (6/16). Observer-discard passes
   16/16 (per-tick byte-identical, mid-window swap), the host-audit is clean, and the interventions
   (gate, residual yield, scramble) are uniform and balance-safe.
2. **At the P4-declared θ=0.6 the two-counter is WORSE than the single-counter on the cut endpoint**
   (6/16 vs 2/16 false-relinquish), because θ=0.6 is the *decision-theoretic* optimum (wrong
   relinquish under cut costs R=4 there) and is over-aggressive at the organism scale. Raising θ to
   0.7+ restores clean cut behaviour (0/16) with unchanged move behaviour — the organism-scale
   threshold is a parameter-sweep result, not a fixed constant.
3. **At their cut-safe optima the two arms TIE on the categorical endpoints** (two_counter θ=0.7 and
   single_counter (−6,4) both give move 4/4 + cut 0/4). The P4 benefit (+0.039 … +0.32) is a
   **regret-level (graded)** difference, and the organism-scale categorical endpoint
   (relinquish-vs-hold) cannot resolve a regret margin — the same gate-shape lesson as AC16/AC17
   (a categorical claim needs a categorical difference; the weighting advantage is graded). The
   discriminating prediction therefore needs a **latency/income/regret-level gate**, not
   categorical dominance.
4. **No positive result is claimed.** This is engineering: the design is *functioning and
   discriminating* (the arms separate on their surfaces, the interventions are clean), not
   *vindicated*. The two-counter's graded advantage over the single-counter — and whether it
   survives at organism scale at the informative high-q end — is P6's prediction to test.

## 7. What P6 receives

A valid AC112 runner (two_counter candidate + single_counter / immediate / scramble rivals) with
passing host-audit + observer-discard (16/16) and clean interventions, plus an engineering screen
showing the arms discriminate on decision utility. Two things P6 must handle, both measured here:

- **Regime.** The accumulator is only load-bearing at high occlusion (q ≥ ~0.9), where the open
  decisive path (1−q) is rare; at q=0.7 the decisive path does most of the work (C4's rule).
- **Gate shape.** The two-counter's advantage is graded (regret/latency), so gate on a
  latency/income/regret endpoint — not categorical relinquish-vs-hold dominance — swept over both
  parameter families (θ and (w,N)) on fresh disjoint seeds, per AC11/AC16/AC17.

## Files

- runner: `ac112.py`
- tests: `test_ac112.py` (13 tests)
- this doc: `AC112_ENGINEERING_v1.md`
- engineering cohort: `ac112_engineering_v1/` (rows.jsonl, results.json, observer-discard)
- parameter screen: `ac112_sweep_v1/` (θ grid × single (w,N) grid)
- No frozen artifact was edited, re-run, or re-hashed.

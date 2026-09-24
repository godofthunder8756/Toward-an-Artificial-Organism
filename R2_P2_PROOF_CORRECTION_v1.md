# R2 — corrected P2 equivalence proof, AC112/113 scaffolding disclosure, and the four distinctions

2026-09-24. Corrects the reasoning in `C4_P2_EQUIVALENCE_v1.md` §3 (and its echo in
`_c4_p2_equivalence.py` docstrings), discloses the AC112/113 operational scaffolding as
limitations, and draws the four distinctions the task body requires. No frozen artifact is
edited or re-run and nothing is re-hashed: `ac112.py`, `ac113.py`, and the frozen
`AC113_PROTOCOL_v1.md`/`AC113_RESULTS_v1.md` are untouched. This note supersedes
`C4_P2_EQUIVALENCE_v1.md` §3 and the framing of its §4 check (2), while **preserving the
central result and every measured number in that document**.

Supporting verification (non-frozen, new): `_r2_exact_boundary.py`.

---

## Headline (adopted)

The central P2 result stands — **the graded posterior is exactly an integer ambiguous-failure
counter under matched decisive-observation handling** — and it is in fact *stronger* than the
original document proved: the equivalence does not depend on the grid avoiding boundaries,
because the matching `>=` convention makes `N = ceil(logit(θ)/LR)` exact for every θ. The
original *reasoning* ("LR irrational and θ rational ⇒ logit(θ)/LR never an integer") is
**false**, and is replaced by an explicit-equality threshold mapping plus a numerical,
grid-specific boundary check. The AC112/113 estimate's causal role, informative value, and
maintenance dependence are each narrower than a surface reading of "the organism maintains a
cause estimate" would claim; those bounds are stated in §6–§7.

---

## 1. The false claim and its counterexample

`C4_P2_EQUIVALENCE_v1.md` §3 argued:

> `LR = log(4/3)` is irrational and every grid `θ` is rational, so `logit(θ)/LR` is never an
> integer.

This is false. The exact-boundary condition is

    logit(θ) / LR = k   (integer)

which, exponentiating (`logit(θ) = log(θ/(1−θ))`), is equivalent to

    θ/(1−θ) = (4/3)^k   ⟺   θ = (4/3)^k / (1 + (4/3)^k),

a **rational** number for every integer k. The sequence is θ = 1/2 (k=0), 4/7 (k=1), 16/25
(k=2), 3/7 (k=−1), … — all rational. In particular, for k = 1:

    θ = 4/7  ⇒  logit(4/7) = log((4/7)/(3/7)) = log(4/3) = LR exactly,

so `logit(θ)/LR = 1`, an exact integer — the very counterexample the original proof denied.

The original §3 was therefore wrong in its *reasoning*, not in its conclusion. What actually
carries the proof is the explicit equality handling below plus a numerical check that the
specific grid used does not put any other point on a boundary (which is true for reasons of
arithmetic coincidence, not irrationality).

## 2. Corrected threshold mapping (explicit equality, unconditional)

In the finite branch the graded accumulator takes exactly the values `L = n·LR` (after n
occluded-unproductive contacts, from prior `L_0 = 0`), and the decision is `L >= logit(θ)`.
The integer counter with threshold N decides `n >= N`. With N = ceil(logit(θ)/LR), the two
coincide on every admissible history for **every** θ, integer boundary or not:

- **Non-boundary case** `logit(θ)/LR ∉ ℤ`: write `k = floor(logit(θ)/LR)`. Then
  `n·LR >= logit(θ)` ⟺ `n >= logit(θ)/LR` ⟺ `n >= k+1 = ceil(logit(θ)/LR) = N`. Exact.
- **Boundary case** `logit(θ)/LR = k ∈ ℤ`: `n·LR >= logit(θ) = k·LR` ⟺ `n >= k`, and
  `N = ceil(k) = k`, so `n >= k` ⟺ `n >= N`. The `>=` on both sides aligns the exact boundary;
  **no special case is required.** (Verified exhaustively for θ = 0.5 → N = 0 and θ = 4/7 →
  N = 1, zero mismatches over the full 6-symbol alphabet, horizons 1–7 — see §4.)

The decisive branches (`open held` → +∞ act now; `open blind`/`occluded-productive` → −∞ hold
forever) are matched term-for-term exactly as in the original §2. The corrected statement of
§3 is therefore: **the float log-odds carries no information the integer counter lacks**, and
the equivalence is a *representation* fact (constant LR ⇒ L is a scaled, translated count)
that does not require any gap argument.

## 3. Numerical-boundary handling over the used grid

The tuning comparison still needs the grid to map to a well-defined integer threshold, and it
does — but the justification is a numerical fact about the grid, not rationality:

- The used grid is `{0.5, 0.52, 0.55, 0.58, 0.6, 0.62, 0.66, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95}`.
  The exact-boundary condition `θ/(1−θ) = (4/3)^k` is satisfied **only** by `θ = 0.5`
  (k = 0, logit = 0 = 0·LR). Every other grid point has a non-integer ratio.
- The nearest **non-zero** distance from `logit(θ)/LR` to an integer is **0.0296** at
  `θ = 0.85` (≈ 8.5e-3 in log-odds), against a float accumulation error of ~1.8e-14 after 96
  adds — a margin of >1e9. No grid θ sits within float noise of a boundary it is not exactly on.
- `θ = 0.5`'s exact boundary is handled by the `>=` convention (`graded(0.5) == int(0)` on
  every history, confirmed exhaustively), so it does not perturb the mapping.

The mapping `{0.5,…,0.95} → N ∈ {0,1,1,2,2,2,3,3,4,5,7,8,11}` and the nine distinct thresholds
`{0,1,2,3,4,5,7,8,11}` reported in `C4_P2_EQUIVALENCE_v1.md` §4 are **unchanged** — only the
reasoning that licenses them is corrected.

## 4. The exact-boundary verification artifact

`_r2_exact_boundary.py` (run: `.venv/bin/python -B _r2_exact_boundary.py`) checks, exactly and
numerically:

1. `logit(4/7) == log(4/3) == LR` (float equality) and `logit(4/7)/LR == 1.0`.
2. The general rational solution: `logit(θ)/LR == k` to 1e-12 for `θ = (4/3)^k/(1+(4/3)^k)`,
   `k ∈ {−5,…,5}` — the exact boundaries are countably infinite and rational.
3. The used-grid scan: the only exact boundary in the grid is `θ = 0.5`.
4. `graded(θ) == int(ceil(logit(θ)/LR))` exhaustively on the exact-boundary thetas
   `θ ∈ {0.5, 4/7}`, horizons 1–7, full 6-symbol alphabet (zero mismatches).
5. The numerical margin: min non-zero gap 0.0296 at `θ = 0.85`, >1e9 above float noise.

All checks pass. The original executable equivalence (`_c4_p2_equivalence.py`, whose false
docstring lines are corrected in place) still passes unchanged, confirming the central result
is preserved.

## 5. What is preserved

Everything else in `C4_P2_EQUIVALENCE_v1.md` stands, verbatim:

- The exhaustive and random equivalence (graded == int == binary+imm(full) on every admissible
  history) — §4 checks 3 and 4.
- The regret attribution (the `binary+imm (as-is)` column is strictly worse; the dominance is
  a rival defect, not a property of gradedness) — §4 check 4 and §5.
- The one-observation defect (occluded-productive is decisive-C; `binary+imm` resets instead) —
  §5.
- The P4 consequence (the first-order claim licenses an integer counter, not a graded register;
  the reliability tier is deferred) — §6.

The *reasoning* in §3 and the *framing* of §4 check (2) are what change.

---

## 6. AC112/113 operational scaffolding (disclosed limitations)

The maintained two-counter estimate (AC112 engineering, AC113 frozen) demonstrates a specific,
narrow capability. The following are **supplied** (host-provided), not acquired, maintained, or
estimated by the organism. They are limitations of the demonstrated mechanism, not properties
to inherit into the frozen study.

1. **Supplied timing — `self.now < CUT_TICK`.** `ac112.py:312, 383, 426` guard the estimator's
   `outcome()` with `if key != 1 or self.now < CUT_TICK: return`, so the update/decide path is
   inert before the host-supplied intervention tick (`CUT_TICK = MOVE_TICK = 8192`, imported
   from `ac107`; `ac112.py:76-77`). The *when* of the cause is supplied; the organism does not
   acquire the timing, and nothing in AC112/113 shows it would detect an unannounced cause at an
   unannounced time.

2. **Supplied location — channel-1 specialization.** The same guard's `key != 1` means only
   channel 1 moves/cuts/occludes; channel 0 is structurally inert (`ac12.MOVE_KEYS = (1,)`,
   `ac113.py:92`). *Which* channel fails is a supplied world fact. The estimate is specialized
   to the one channel that changes; a move of channel 0 (or a second channel) is outside what
   AC112/113 exercised.

3. **Supplied likelihoods and cause assumptions.** The weights `w_u = log((4/3)(1−ε))`,
   `w_p = log(4ε)` (`ac112.py:102-106`), the threshold θ (`ac112.py:85`, `ac113.py:60`), the
   residual yield ε (`ac112.py:84`, `ac113.py:48-49`), and the occlusion q (`ac112.py:83`,
   `ac113.py:47`) are declared world constants, baked into `_decide`
   (`n_u·w_u + n_p·w_p >= logit(θ)`, `ac112.py:300`). The organism does **not** estimate these;
   they are the first-order content tier. The two-cause structure itself (move = channel-1
   mapping flip; cut = route-1 read suppression) is supplied. This is precisely the boundary P7
   deferred on: an *estimated* reliability tier (learned ε / `P_YIELD`) is not implemented.

4. **What observer-discard does and does not establish.** `observer_discard_equivalence`
   (`ac112.py:629-653`) replaces the succession observer and the `alloc` object (clearing its
   observational host logs) at a swap tick and verifies the trajectory is byte-identical at
   every tick. This establishes that the estimator's **decision state lives in the maintained
   substrate** (counters at `traces[0, streak_offs]`, hold latch at `traces[0, bel_off]`) and
   that the host `alloc` object carries only configuration + observational logs, not steering
   state — i.e. the state is *located where it is claimed to be*. It does **not** establish:
   (a) that the estimate is *informative* (that requires host scoring against the true cause);
   (b) that the organism *uses* the estimate for anything beyond the frozen program's action
   stream; or (c) that the estimate is *maintained or repairable* — the repair-dependence of
   the decision state was explicitly out of AC113's scope (AC110's question;
   `AC113_RESULTS_v1.md` §"Not established").

5. **Two further scaffolds, already resolved as substrate (J1), not re-derived here:** the
   rule-interpreter `prog.choose` (`ac9.py:84`) and the succession coordinator `advance()`
   (`ac89/91/92`) are format-level supplied machinery accepted as substrate (BASELINE_v3 §3).
   They are listed for completeness of the scaffold inventory; neither is a cognition-track
   claim.

None of this is removed; AC112/113 keep their scaffolding and their frozen record. The point is
that downstream documents must carry these as limitations, not attribute "the organism estimates
its cause and times its own response" to a study whose timing, location, likelihoods, and cause
structure were all supplied.

---

## 7. The four distinctions

1. **Behaviorally causal state ≠ demonstrated informative estimate.** The scramble control
   (`ac112.py:46-47`, read-forced `(0,0)`) shows the counter *read* causally drives the drop:
   at θ = 0.6 the candidate false-relinquishes under cut where the scramble holds (AC113 rule 2).
   That is *causality of the state in the decision*, not *accuracy of the estimate about the
   cause*. A state can be causal yet harmful (the aggressive θ\* = 0.5 content triggers a drop
   that starves the organism — the 2/16 collapse tail), and it can be accurate yet not useful
   (P4's +0.03…+0.32 regret is below organism-scale resolution). "The register causally drives
   the decision" must never be read as "the register carries a demonstrated accurate estimate."

2. **Sufficient integer representation ≠ absence of uncertainty.** P2 shows the first-order
   posterior is *representationally* an integer counter (sufficient statistic = the count under
   constant LR). That bounds the *register* (no continuous log-odds needed); it does not remove
   the organism's uncertainty (occlusion hides the cause signature), nor does it eliminate the
   need to acquire, update, and maintain the estimate, nor does it touch the deferred
   second-order tier (estimated ε / `P_YIELD`, C4 §11). And it is a *model* fact — a stipulated
   constant `P_YIELD = 1/4` supplying `LR = log(4/3)` — not a demonstration that the organism's
   real evidence stream is constant-LR.

3. **One failed immediate rival ≠ a proof that all memoryless policies fail.** The `immediate`
   (no-state) arm dies under move (6/16 at q = 0.9; AC112 rule 6) because its churn
   (drop + blind re-bind + drop) is not self-sustaining. That documents *one* memoryless
   policy's failure mode. It is not a theorem over the class of memoryless policies: the
   `scramble` arm (counters read as `(0,0)`, writes intact) survives and holds in many
   conditions, and the minimal-state single counter ties the two-counter. "Some maintained state
   is necessary" is only as strong as the specific rivals actually implemented (immediate,
   scramble, single-counter).

4. **Acquisition/update dependence ≠ ongoing repair dependence.** AC108 established the decision
   state's *acquisition/update* is coupled to maintenance (the paid acquisition/update write;
   adaptation reversal 16/16, survival reversal 12/16 — behavioural, not
   viability-advantageous). AC110 established *repair* dependence in the window (repair
   load-bearing for post-window storage protection, G4 8/16). These are different claims:
   acquisition/update = the state is *built and changed* through paid machinery; repair = the
   state's *persistence against damage* requires paid repair. AC113's frozen record states the
   repair-dependence of the decision state was explicitly out of scope (AC110's question;
   `AC113_RESULTS_v1.md` §"Not established"), and the estimate's maintenance rides the shared
   program repair (`reg_writes ~2170`) as in AC110. So neither dependence is
   *re-demonstrated* in AC112/113; each is established in its own architecture (AC108 for
   acquisition/update, AC110 for repair), and the counter bits under a *live* reconstruction
   remain a unit-level assertion (P7), not a study.

---

## 8. Errata (derived claims updated consistently)

- **`C4_P2_EQUIVALENCE_v1.md` §3** — superseded by §2 above. Its §4 check (2) framing
  ("no θ sits within float noise of a boundary" *because* of irrationality) is corrected to the
  explicit-equality + grid-specific statement in §3 above. The central result and all measured
  numbers are unchanged. (Not edited in place; this note supersedes it, per R1's convention of
  not rewriting the historical record.)
- **`_c4_p2_equivalence.py`** — docstring false claim ("logit(theta) never equals an integer
  multiple of the irrational LR", module docstring + `regret_int` docstring) corrected in place.
  This is an exploratory `_`-prefixed script, not in any frozen source-hash set, so the edit
  causes no hash drift. The script's checks still pass.
- **`BASELINE_v3.md` §2 R2 flag** — the defect it names is now corrected by this note; the flag
  remains accurate as the point-in-time record and is not edited.
- **Out of scope, noted for clarity:** `P4_COGNITION_CONTINUATION_v1.md` lines 91-92 and 246-247
  state a *different* irrationality claim — `w_u/w_p` irrational ⇒ the two-counter threshold
  "never coincides with an integer-weighted boundary" (a two-counter vs single-counter
  statement, not the P2 single-counter increment claim). That claim is untouched here; its
  organism-scale consequence is already recorded as AC113 F1 (non-load-bearing) and re-analyzed
  in R1.

---

## 9. Claim discipline

This is a proof repair and a scope disclosure, not a new organism result. It does not re-run,
re-hash, or re-interpret any frozen study; it narrows the first-order cognition claim to its
supported form (a maintained integer counter with supplied weights/threshold/timing/location
suffices; informative value and maintenance-dependence are established only in their
respective, narrower studies). No autopoiesis, "wants", "metacognitive", or "conscious"
language is introduced or licensed here.

## Files

- corrected proof + scaffolding + distinctions: `R2_P2_PROOF_CORRECTION_v1.md` (this file)
- new exact-boundary verification: `_r2_exact_boundary.py`
  (`.venv/bin/python -B _r2_exact_boundary.py`)
- corrected in place (non-frozen docstrings): `_c4_p2_equivalence.py`

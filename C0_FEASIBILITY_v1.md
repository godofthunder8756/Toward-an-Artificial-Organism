# C0 — feasibility verdict: the "reliability continuation" collapses to first-order inference

2026-09-24. Task `t_8dd15ab9`. Feasibility analysis in the AC113 economics, in the lineage of
C2/C4/P2/P4 (identifiability-before-organism-run). Decision-theoretic demonstration
`_c0_reliability_identifiability.py` (run; output below). **No organism-scale run, no seeds, no
freeze** — and, per the card, none is authorized: the outcome is a feasibility verdict, and the
verdict is that no identifiable probe exists.

---

## 1. The question, restated

The card asks whether there is an identifiable, economics-consistent probe that separates three
things:

- **(a)** learning an *environment / observation-channel parameter* — the residual yield ε, the
  occlusion rate q, or the blind-fallback rate P_YIELD (equivalently, the likelihood weights
  w_u, w_p);
- **(b)** *first-order uncertainty about a cause* — the graded posterior P(cause = move | history),
  which P2/P4 established is an integer counter (homogeneous LR) / a two-counter (heterogeneous
  LR);
- **(c)** *monitoring the reliability of the organism's own estimate* — a purported second-order
  state about how trustworthy the first-order estimate is.

The card's warning is the load-bearing constraint: *"do NOT label an epsilon estimate second-order
cognition merely because it parameterizes another computation."* The verdict below is that this
warning, taken literally, closes the track.

---

## 2. The frozen economics (what the probe would have to live in)

AC113's world: two causes, **move** (channel-1 mapping flips at t=8192; the held entry is stale)
and **cut** (route-1 read suppressed for 96 ticks; the entry is intact), plus two declared world
changes applied uniformly to every arm — the C2 occlusion gate (q, occluding `used_held` on a
Bernoulli(q) fraction of channel-1 contacts) and a residual yield ε (a stale held entry under move
yields with probability ε instead of never). Per channel-1 contact the organism observes
`(bound, used_held ∈ {0,1,2}, productive)`; `bound`/`used_held` are its own introspection and the
shimmed retrieval, `productive` is the income outcome. YIELD_M = YIELD_F = 64 per productive
contact; blind fallback under cut yields uniformly over PORTS=4 (so 1/4).

The likelihood structure (P4 §2, frozen):

| observation | possible under | log-LR toward move |
|---|---|---|
| open `held` | M only | +∞ (decisive M) |
| open `blind` | C only | −∞ (decisive C) |
| occluded, unproductive | both | w_u = log((4/3)(1−ε)) |
| occluded, productive | both | w_p = log(4ε) |

The sufficient statistic for the cause is the integer pair (n_u, n_p) consumed as
L = n_u·w_u + n_p·w_p (P4 §3); the weights w_u, w_p and the threshold θ are **supplied** frozen
constants (AC112/113 scaffolding, R2 §6). The two-counter candidate is exactly this sufficient
statistic; AC113 froze F1 (no demonstrated advantage over the single counter, corrected by R1 to
seed-level p ≈ 0.71/0.63).

The deferred item this card reframes is P4 §9's "reliability tier": make ε (or P_YIELD) *vary
across distinguishable conditions* and ask whether an *estimated* weight "restores the
discriminating weighting that a supplied weight gives here."

---

## 3. The five pre-probe items, answered

The card requires these to be specified **before** any probe. Each is answered; each answer
contributes to the collapse.

**(1) What observations identify changing evidence quality, without hidden labels?**

Only the stream `(bound, used_held ∈ {0,1,2}, productive)`. The occlusion rate q is directly
observed (`used_held = 2` is a visible event), so q is trivially countable — but q is fixed in the
frozen world. The residual yield ε is **not** directly observed: it enters the likelihood only
*conditional on the latent cause*,

  P(productive | occluded, cause=move) = ε,  P(productive | occluded, cause=cut) = 1/4,

so the marginal rate the organism can actually observe is

  r = P(productive | occluded) = P(move)·ε + P(cut)·(1/4).

The demonstration shows a continuum of (ε, P(move)) pairs — (0.02, 0.435), (0.08, 0.588),
(0.125, 0.80) — all producing the *identical* observed rate r = 0.15. There is no label-free
observation that tags "evidence quality changed": a change in ε is observationally equivalent to
a change in the first-order cause-belief, and the two are only disambiguated once the cause is
resolved (the open decisive contacts). Estimating ε is therefore *entangled with*, not upstream
of, the first-order inference.

**(2) Does the proposed monitor predict first-order errors beyond the strongest first-order
policy?**

No. The strongest first-order policy is the two-counter, which realizes the sufficient statistic
(n_u, n_p) with the correct weights — Bayes-optimal for the occluded world. Its errors (a false
relinquish under cut from accumulated weak-M; a late drop under move) are the *irreducible*
posterior uncertainty given the occluded evidence. A "reliability" state can only be:

- a function of (n_u, n_p) — e.g. confidence = tanh(|L|/2) — which is a *re-encoding* of the
  first-order state and predicts nothing the state does not already contain; or
- an estimate of ε (the channel's diagnostic value), which is (a) — a first-order world
  parameter — and whose value is needed *inside* the first-order likelihood, not alongside it.

Either way the monitor adds no error-predicting power beyond (a) + (b). (Demonstration F2, F3.)

**(3) A context-sensitive rival receiving the same observations?**

The card's requirement is that the rival not be "a fixed parameter known to be wrong" — it must
receive the same stream and adapt. The context-sensitive rival receiving the same stream **is**
the first-order policy (single-counter / two-counter), or an ε-estimator (a). There is no third
rival category: any arm that "monitors reliability" is, by (2), either an ε-estimator (a rival
that learns the environment parameter) or a re-parameterization of the counter (a rival that
infers the cause). The rival structure degenerates — which is itself the finding (the card
anticipates this: "a context-sensitive rival solving the task is a legitimate result").

**(4) Interventions separating estimated content from estimated reliability?**

C4's rule 7 gives the two single-flag interventions — scramble-content-keep-reliability and
scramble-reliability-keep-content. They do not separate (a) from (c), for the reason (2) exposes:

- An ε-estimate (a) is *invariant* to scrambling the cause estimate: it tracks the world's ε, not
  the estimate, so "keep-reliability" cannot be implemented distinctly from "keep-ε".
- A reliability state that *responds* to content scrambling (flips to "unreliable" when the
  estimate is scrambled) responds exactly as first-order re-inference (b) does — the new
  observations no longer match the latched estimate, which *is* the posterior shifting.

So "scramble reliability but keep content" has no referent other than "keep the supplied ε" (a)
or "keep the posterior" (b). There is no third state to scramble.

**(5) The narrow claim the probe could support?**

None of the form "the organism monitors the reliability of its own estimate." The only narrow
claims that survive are first-order: "the organism learns and maintains an estimate of the
channel parameter ε" (a), and "the organism infers the cause from weighted evidence" (b). The
second-order reading is a *label* applied to one of these, not a distinct mechanism.

---

## 4. The collapse, stated precisely

Three cases, each terminating in (a) or (b):

1. **"Reliability" = the channel's diagnostic value (ε / P_YIELD / q).** Then it is (a) — a
   first-order estimate of a world parameter. The word "reliability" is a re-description of the
   parameter, not a second-order fact. This is exactly the card's warning: ε parameterizes the
   first-order computation, so calling it "second-order cognition" is the labeling error.

2. **"Reliability" = the estimate's own confidence / distance-to-threshold.** Then it is a
   function of the sufficient statistic (n_u, n_p), hence (b). P2's lesson at one level up: a
   graded confidence register is a lossy re-encoding of the counter and carries nothing the
   counter lacks.

3. **"Reliability" = is my substrate/machinery intact?** This *is* genuinely self-referential and
   distinct from both — but it is AC110's question (repair dependence), not an estimate-reliability
   question, and AC110 already answered it: repair is not load-bearing for the estimate's
   correctness/use in the decision window (reacquisition carries it). A machinery-integrity state
   is a maintenance/substrate claim, not a cognition claim.

The deeper structure behind all three: in a faithful Bayesian agent the "reliability of my own
estimate" **is** the posterior (its spread), and the "evidence quality" **is** a likelihood
parameter. There is no third referent. The circularity completes the collapse — ε is needed
*inside* the first-order likelihood, but ε is identifiable only *after* the first-order cause
inference resolves which contacts are "under move." Joint inference over (cause, ε) is one
first-order hierarchical computation, not "first-order inference plus a separate second-order
monitor." The "second-order" language describes the *level* of a parameter in a hierarchy, not a
distinct cognitive mechanism.

---

## 5. Verdict

**Not identifiable.** No economics-consistent, label-free probe distinguishes (a), (b), and (c)
as three mechanisms. (c) collapses to (a) (if it is the channel parameter ε) or to (b) (if it is a
function of the sufficient statistic), and the third self-referential reading is the already-answered
substrate question (AC110). The five pre-probe items do **not** yield an identifiable comparison,
so per the card no probe is run and no organism-scale study is proposed.

**Consequence for the reliability continuation:** it is closed as a *second-order cognition*
track. The residue is a first-order question — can the organism *acquire and maintain* a graded
estimate of ε when ε varies across distinguishable conditions, and does that estimate improve
weighting over a supplied/stale weight? That is an acquisition/maintenance question about a world
parameter (a), *not* a reliability/cognition question, and it is gated on the same
economics-vs-cost discipline as AC113 (which already showed the supplied-weight two-counter does
not beat the single counter). It should be framed, if pursued at all, as "the organism estimates a
channel parameter," never as "the organism monitors its own reliability."

**What would make (c) identifiable (reopening conditions) — and why each is closed here:**

- A first-order estimate that is *sometimes wrong*: satisfied (occlusion). K8's prerequisite is met.
- Wrongness *predictable from observations the first-order state does not condition on*: this is
  where (c) must live, and it is unsatisfiable — any observation that predicts the estimate's
  error is either already in the sufficient statistic (then (c) = (b)) or is the world's ε (then
  (c) = (a)).
- A *self* referent distinct from the world: unsatisfiable as an observable — the "self vs world"
  boundary is a host-side label, not something the organism's stream or behavior can mark.

These three, taken together, say the reliability tier has no empirical content beyond first-order
inference under the AC113 economics; the block is structural, not a tuning miss.

---

## 6. Claim discipline

This is a feasibility verdict, not a study and not a falsification of anything previously claimed.
It does **not** assert the organism "cannot" do anything; it asserts that "monitoring the
reliability of one's own estimate" is not a *separable mechanism* from "learning ε" and "inferring
the cause" under a label-free criterion, so no probe can distinguish them. It licenses no
autopoiesis, "wants", "metacognitive", or consciousness language — and, per the card, it must not
be read as authorizing an organism-scale reliability study (none is authorized). It narrows P4 §9's
"reliability tier" from a *second-order cognition* target to a *first-order parameter-learning*
target, which is the correction the card's warning requires.

---

## 7. Demonstration output (`_c0_reliability_identifiability.py`, run)

    F1 -- eps is identifiable only conditional on the latent cause
      blind fallback P(prod|cut) = 0.2500
        (eps=0.020, P(cause=move)=0.4348) -> r = 0.1500
        (eps=0.080, P(cause=move)=0.5882) -> r = 0.1500
        (eps=0.125, P(cause=move)=0.8000) -> r = 0.1500
      all three (eps, cause-belief) pairs produce the IDENTICAL observed stream r.

    F2 -- 'reliability'/'confidence' is a pure function of the sufficient statistic
      eps=0.08: w_u=0.2043, w_p=-1.1394
      confidence(n_u,n_p) = tanh(|L|/2), L = n_u*w_u + n_p*w_p  -- deterministic in (n_u,n_p).

    F3 -- the only predictor of first-order errors is the true eps (a world parameter)
      true eps=0.08, supplied stale eps'=0.02
        under move, drift with true weights: +0.0968; with stale weights: +0.0440 (bias -0.0528)
      => a 'reliability monitor' that predicts these errors IS an eps-estimator = (a).

    All identifiability checks pass: the 'reliability tier' collapses to (a) or (b).

---

## 8. Files

- verdict: `C0_FEASIBILITY_v1.md` (this file)
- demonstration: `_c0_reliability_identifiability.py`
  (`.venv/bin/python -B _c0_reliability_identifiability.py`)
- no frozen artifact, runner, protocol, or hash edited, re-run, or re-hashed.

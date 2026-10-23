# Prospective reachable-alias audit: draft (additive, pre-enumeration)

Status: PROTOCOL DRAFT ONLY. Prepared Oct 20, 2026 (America/New_York). Nothing here was
run. The 256-history enumeration is not approved. Whether aliases exist is UNKNOWN and was
deliberately not computed. No numerical gate of `ACI_NEXT_EXPERIMENT_DECISION_v1.md` (DEC)
is changed. Algebra references point to `filter_algebra.md` (FA).

## 1. Why the audit is needed

- DEC L119-121 already says: "For a stronger marginal-only necessity claim, demand exact
  reachable aliases or an explicit finite-precision/stability/control-class proof. An
  off-support state clamp alone is not such a proof."
- DEC L113-114 disclaims "that any nonlinear two-marginal readout cannot encode history
  via precision".
- CON (`ACI_RESEARCH_CONSTITUTION_v3.md`) L53-58 and L60-63 require separating causal
  use from necessity and matching rivals on information.

Gates (ii)/(iii) compare the oracle with the bilinear PRODUCT readout of exact marginals
(FA section 6). The reachable set at each stage is finite (at most 2^k histories). If no
two reachable histories share exact marginals while differing in c, then SOME function of
the exact marginals recovers c, and therefore recovers XOR, exactly. A pass of (ii)/(iii)
would then defeat only the product decoder, not "marginals". Astra raised this
(`/workspace/astra_consult_1.md` L5). The audit makes the distinction checkable and
prospective.

## 2. Definitions to freeze

- **Stage k** (k = 1..8): the post-reading-k belief b_k(h), before any transition
  (DEC L54-56). The pre-reading (post-transition) belief is a deterministic invertible
  function of b_k: the transition is diagonal with nonzero factors (FA 3c). So it adds no
  separate alias class.
- **Reachable set** R_k = { b_k(h) : h in {0,1}^k }. All prefixes have positive
  probability (DEC L63).
- **Marginal map** M(b) = (m_x, m_y). Exact rational equality only (precision regime P0,
  section 4).
- **Reachable XOR/covariance alias at stage k:** h != h' in {0,1}^k with
  M(b_k(h)) == M(b_k(h')) and c_k(h) != c_k(h').
- **Continuation alias at stage k < 8:** h != h' with equal M but a different predictive
  law for some future reading or terminal query.
  - Lemma A1: for k < 8, a continuation alias at stage k is equivalent to a covariance
    alias at stage k.
    - Proof (=>): the predictive law is a function of b_k = Psi^{-1}(m_x, m_y, c).
    - Proof (<=): suppose M is equal and kappa differs. The transition preserves equal
      mu and unequal kappa, because its factors are nonzero. At the next reading of
      variable v, the other marginal moves by eta o kappa/D with equal D (FA 3a/3b). The
      other marginal then differs, so the predictive probability of the next reading of
      the other variable differs; if k+1 = 8, the terminal XOR forecast differs instead.
  - At k = 8, "continuation" means the terminal XOR query, so the two notions coincide.
- **Benign merge:** equal M and equal c. Then the beliefs are identical by FA Lemma 1.
  This is not an alias.
- **Off-manifold clamped state:** any belief produced by intervention (for example the
  zero-covariance clamp of DEC L92-95, or arm 2's product). It is legal (FA section 6)
  but generally not in R_k. **A clamped state can never serve as an alias witness.** Both
  members of a witness pair must be naturally reachable posteriors of actual histories.

### Candidate mechanism (stated without evaluation)

The model is invariant under flipping all X-reading outcomes:
(mu_x, mu_y, kappa) -> (-mu_x, mu_y, -kappa), with P(h) preserved. The same holds for Y.
This symmetry produces an exact XOR alias precisely when some reachable state has
mu_x = 0 (respectively mu_y = 0) and kappa != 0. The partner history then has identical
marginals and the XOR forecast 1 - q.

Whether such exact cancellations occur, and whether non-symmetric "accidental" equalities
occur, is not known and must not be pre-computed. The audit must report which mechanism
produced each witness.

## 3. Two audit targets, kept separate

| Target | Question | Stages audited | Timing regime |
|---|---|---|---|
| **T-PROJ** (terminal oracle projection) | Is there any function g with g(M(b_8)) = q_joint on R_8? | k = 8 only | stage known |
| **T-CLOSE** (autonomous filter closure) | Is there a stage-indexed marginal-only filter m_{k+1} = F_k(m_k, o_{k+1}), with readout g, that is exact on all reachable histories? | k = 1..8 | see section 4 |

- Lemma A2 (with a clock): T-CLOSE holds iff there is no covariance alias at any stage
  k = 1..8. The proof is Lemma A1 plus the lookup construction of F_k on R_k.
- T-PROJ can hold while T-CLOSE fails. An alias at an early stage can make the
  autonomous update ambiguous even though the terminal marginals happen to separate the
  histories.
- If either holds via a lookup, the realizing decoder is a reachable-set table. It must
  be charged entries and precision exactly like arm 5 (DEC L76, L128-129). Sufficiency of
  the information is not economy of the mechanism.

## 4. Timing and precision assumptions (declare, do not tune)

- **Clock regimes:**
  - **K1:** the retained state is given the stage index k and the reading modality. The
    stage-indexed F_k and g_k above are allowed.
  - **K2 (no clock):** the decoder sees only M. Pairs (h at stage k, h' at stage k') with
    k != k' must then also be audited. A cross-stage alias implicates missing time/modality
    information, not missing correlation. It must be reported separately and never counted
    as a covariance witness.
- **Precision:**
  - **P0:** exact rationals, the only regime that can produce an exact alias verdict.
  - Any finite-precision statement, such as near-aliases or decoder Lipschitz/stability
    bounds, is a DIFFERENT claim class (DEC L119-120). This draft adds no tolerance
    threshold, because doing so would create a new gate.
  - At most, record as a descriptive, non-gating quantity, per stage, the minimum
    distance ||M(h) - M(h')||_inf over pairs with c(h) != c(h'). Also record the exact
    numerator/denominator bit-lengths. These are labelled "descriptive; licenses nothing".

## 5. Proposed frozen wording (additive; to be appended via a new versioned file)

Proposed file: `ACI_TWO_STREAM_ALIAS_AUDIT_ADDENDUM_v1.md`. It is additive per CON
L91-94 and handoff governance (`/workspace/aci_handoff.md` L27). The text below is a draft
for Aidan's approval and has not been committed:

> **Reachable-alias audit (additive, non-gating).** This addendum leaves every admission
> signature, threshold, generator parameter, horizon and arm of
> ACI_NEXT_EXPERIMENT_DECISION_v1 unchanged. It adds no PASS/FAIL condition for world
> admission.
>
> When the approved enumeration runs, the same exact rational posteriors, cross-checked
> by the independent replay, are used to report, for each stage k = 1..8 and under exact
> rational equality:
>
> (a) the number of reachable covariance-alias pairs: distinct histories with identical
> exact (P(X=1), P(Y=1)) and different Cov(X,Y);
>
> (b) for each pair, the stage, both histories, both covariances, and whether the pair is
> generated by the X-flip or Y-flip outcome symmetry or is accidental;
>
> (c) separately, cross-stage marginal coincidences (no-clock regime), never pooled with (a);
>
> (d) the verdicts T-PROJ (stage-8 aliases absent?) and T-CLOSE (aliases absent at all
> stages?).
>
> States produced by covariance clamping or factorized projection are not reachable and
> are excluded as witnesses. The audit specification, alias definition and reporting
> format are frozen before enumeration. No result of the audit may be used to alter the
> world, the gates, or the claim wording of gates (i)-(iv) after the fact. It may only
> select among the pre-written interpretation rows below.

## 6. What each outcome licenses (pre-written interpretation rows)

The admission PASS/FAIL comes from gates (i)-(iv) alone. The alias outcome only selects
the claim ceiling attached to (ii)/(iii).

| Outcome | Licenses | Does NOT license |
|---|---|---|
| **A0: no aliases at any stage (T-PROJ and T-CLOSE true, K1, P0)** | "In this world, exact marginals determine the XOR forecast and an exact stage-indexed marginal filter exists on the reachable set. Gates (ii)/(iii) measure only the information discarded by the product readout." | Any claim that marginals are insufficient. Any claim that a third coordinate is necessary. Any claim that the product failure shows integration is required. |
| **A1: terminal aliases (T-PROJ false)** | "The exact pair (P(X), P(Y)) is informationally insufficient for the terminal XOR forecast on reachable histories, under exact arithmetic with stage known." This is a Q-EXIST-level fact about this world (CON L49). | Neural necessity of 3 coordinates (DEC L113). Q-LEARN, Q-CAUSE or workspace/C3 claims. Generalization to other worlds or noise. Necessity under other encodings: a learner need not store marginals at all. |
| **A2: aliases only at intermediate stages (T-PROJ true, T-CLOSE false)** | "A marginal-only state cannot be updated autonomously and exactly; joint information must be retained during filtering, even though the terminal marginals happen to separate the histories." | That terminal XOR prediction needs more than marginals. Anything beyond retained-state closure for this world. |
| **A3: only cross-stage coincidences (K2)** | "A clockless marginal state confounds stages; time/modality information is needed." | Anything about correlation. |
| **Replay disagreement** | INVALID: halt and report (CON L117-119). | Any alias verdict. |

For every row, the claim ceiling of DEC L106-117 still binds. Nothing here advances C2/C3
beyond PARTIAL, touches the O-axis, resolves A6, or unblocks A8 (also Astra L3; handoff L17).

## 7. Interaction with the admission analysis (why this matters)

From FA:
- (iv) is a theorem.
- (i) passes by a sign argument.
- (ii)/(iii) both read the law of terminal |c_h| from a product readout.

Under outcome A0, a full PASS of DEC would add, beyond algebra already in hand, only
"terminal |c_h| clears two thresholds". That is a headroom property of the benchmark,
which is the purpose DEC L41-44 states, not evidence about integration. The audit prevents
that headroom from being reported as necessity.

A stronger rival is still missing: an autonomous mean-field (assumed-density) factorized
filter, which would also show X/Y excess (FA Lemma 4). Adding it as a sixth arm would be
an apparatus change and needs its own human approval. It is noted, not proposed here as
frozen.

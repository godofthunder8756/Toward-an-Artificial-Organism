# Two-stream world: exact joint filter algebra (symbolic only)

Status: ANALYTIC DERIVATION / PROTOCOL DRAFT. Prepared Oct 20, 2026 (America/New_York).
HARD LIMIT honoured: the 256-history enumeration is NOT approved. No history was
enumerated. No admission-gate value, Brier risk, intervention mass or clamp statistic
was computed, numerically or symbolically. No solver was run. Everything below is
general algebra over an arbitrary belief state, plus substitution of the frozen generator
parameters into the update coefficients. Repo is read-only at HEAD 32cfbe6 (per
/workspace/aci_handoff.md L2); nothing in it was modified.

Sources: world and gates `ACI_NEXT_EXPERIMENT_DECISION_v1.md` (hereafter DEC) L46-104;
governance `ACI_RESEARCH_CONSTITUTION_v3.md` (hereafter CON); Astra hypotheses
`/workspace/astra_consult_1.md` L4-7 (treated as claims to check, not authority).

---

## 0. Frozen world, as read from DEC L48-63

- Hidden (X,Y) in {0,1}^2, initially uniform (DEC L48-49).
- Transition: independent C~Bern(g), Dx~Bern(dx), Dy~Bern(dy); X'=X^C^Dx, Y'=Y^C^Dy
  with g=1/5, dx=1/50, dy=1/40 (DEC L51-53).
- Eight readings alternating X and Y, each through an independent BSC(e), e=1/5.
  Observe at state t, then transition; no transition after reading 8 (DEC L54-56).
- Terminal queries: X, Y, XOR(X,Y) (DEC L57-58).

Ambiguity to freeze (not a gate change): DEC says "alternate X and Y" but does not
say which comes first. Below I write the order as X,Y,X,Y,X,Y,X,Y (reading 8 = Y),
but every formula is written for a generic X-reading or Y-reading, so it holds either way.
The order affects which marginal the current-only arm sees. **It should be written into
the frozen manifest.**

## 1. Coordinates

Spin variables: s = 1-2X, t = 1-2Y, in {+1,-1}. Observation spin: o = 1-2O.
Any distribution p on {0,1}^2 is fully described by its Walsh moments:

    mu_x = E[s] = 1-2 m_x,   mu_y = E[t] = 1-2 m_y,   rho = E[st],
    p(s,t) = (1 + mu_x s + mu_y t + rho s t) / 4.

where m_x = P(X=1), m_y = P(Y=1). Define the (marginals, covariance) coordinates

    c     = Cov(X,Y) = p11 - m_x m_y
    kappa = rho - mu_x mu_y = Cov(s,t) = 4c.

(Check: rho = 1-2m_x-2m_y+4p11 and mu_x mu_y = 1-2m_x-2m_y+4m_x m_y, so their
difference is 4(p11-m_x m_y).)

Constants (generator substitution only):

    a   = E[(-1)^C]  = 1-2g  = 3/5
    b_x = E[(-1)^Dx] = 1-2dx = 24/25
    b_y = E[(-1)^Dy] = 1-2dy = 19/20
    eta = 1-2e       = 3/5,     1-eta^2 = 4e(1-e) = 16/25
    1-a^2 = 4g(1-g) = 16/25

## 2. Lemma 1 (chart). (m_x, m_y, c) is a bijective chart of the 4-state simplex

Inverse map:

    p11 = m_x m_y + c
    p10 = m_x(1-m_y) - c
    p01 = (1-m_x) m_y - c
    p00 = (1-m_x)(1-m_y) + c

The image of the simplex is exactly the set where all four entries are >= 0. This is the
Frechet box:

    max(-m_x m_y, -(1-m_x)(1-m_y)) <= c <= min(m_x(1-m_y), (1-m_x) m_y),

which implies |c| <= 1/4. The map p -> (m_x, m_y, c) is a polynomial bijection with a
polynomial inverse. The simplex has 3 free parameters, and (m_x, m_y, c) are 3 numbers.

**Consequence:** "marginals plus one covariance statistic" is not a compression of the
joint filter. It IS the joint filter in different coordinates.

## 3. Exact update law

### 3a. Observation of X with spin o (likelihood P(o|s) = (1+eta o s)/2)

Let D = 1 + eta o mu_x. Note that D = 2 P(O=o | h), twice the predictive probability.

    mu_x' = (mu_x + eta o) / D
    mu_y' = (mu_y + eta o rho) / D  = mu_y + eta o kappa / D
    rho'  = (rho + eta o mu_y) / D
    kappa'= (1-eta^2) kappa / D^2

Proof of the kappa line: kappa' = rho' - mu_x' mu_y', and multiplying through by D^2
with o^2 = 1 gives

    (rho+eta o mu_y)(1+eta o mu_x) - (mu_x+eta o)(mu_y+eta o rho)
      = rho + eta^2 mu_x mu_y - mu_x mu_y - eta^2 rho = (1-eta^2)(rho - mu_x mu_y).

In (m, c) coordinates, writing P1 = P(O=1|h) = e + eta m_x and P0 = 1-P1:

    O=1: m_x' = (1-e) m_x / P1,   m_y' = m_y + eta c / P1,   c' = e(1-e) c / P1^2
    O=0: m_x' = e m_x / P0,       m_y' = m_y - eta c / P0,   c' = e(1-e) c / P0^2

(Direct check for O=1: P(Y=1,O=1) = (1-e)p11 + e p01 = m_y P1 + eta c.)

### 3b. Observation of Y

This is the same as 3a with the roles of x and y swapped:

    mu_y' = (mu_y + eta o)/D,   mu_x' = mu_x + eta o kappa/D,   kappa' = (1-eta^2) kappa/D^2

with D = 1 + eta o mu_y.

### 3c. Transition

The noise is independent of the state, and (-1)^C appears squared in st. So:

    mu_x' = a b_x mu_x,   mu_y' = a b_y mu_y,   rho' = b_x b_y rho
    kappa' = b_x b_y [ kappa + (1-a^2) mu_x mu_y ]

In (m, c) coordinates:

    m_x' = 1/2 + a b_x (m_x - 1/2)
    m_y' = 1/2 + a b_y (m_y - 1/2)
    c'   = b_x b_y [ c + (1-a^2)(m_x - 1/2)(m_y - 1/2) ]

The Walsh basis diagonalises the transition. The common flip contracts each marginal by
a = 3/5 per step but leaves parity untouched; parity decays only through private flips
(b_x b_y). This is the structural source of any XOR headroom.

### 3d. Structural lemmas (general, no history evaluated)

- **L2 (observations never create covariance).** By 3a/3b, kappa' is proportional to kappa.
  A product belief stays a product under any reading, because the likelihood depends on
  one coordinate only. Readings can rescale |c| by e(1-e)/P(o)^2. That factor lies in
  [1/4, 4], because P(o) lies in [e, 1-e].
- **L3 (transitions create covariance from the product of marginal means).** By 3c, the
  new covariance is b_x b_y (1-a^2) mu_x mu_y. From the uniform start, mu_y = 0 until the
  first Y reading. So the transition after reading 1 creates no covariance, and the first
  nonzero c can appear only after the second transition. No magnitude is claimed.
- **L4 (marginal-only updates do not close).** By 3a/3b, a reading of one variable moves
  the other marginal by eta o kappa/D. The exact marginal update therefore needs c. A
  marginal-only state is not an autonomous filter in this world unless c is recoverable
  from it (see alias_check.md).

## 4. Theorem: sufficiency and closure of (marginals, covariance)

Claim: (m_x, m_y, c) is an exactly sufficient statistic of the history for every terminal
query and every continuation prediction. It also closes under the update law.

Proof: the Bayes posterior b_t(h) is sufficient for (X_t, Y_t) and for all future
observations (standard HMM filtering). By Lemma 1, b_t <-> (m_x, m_y, c) is a bijection.
Sufficiency transfers. Closure: Phi_o(b) is the Bayes update. Then
Psi o Phi_o o Psi^{-1} is an explicit rational map, written out in section 3. QED.

This is a proof over the whole simplex, not over histories. It covers every reachable
and every off-manifold legal state.

**Implication for DEC signature (iv)** (DEC L96-98, "marginals plus covariance match the
full joint filter's forecasts and update law"): it is a theorem, not an empirical
outcome. It cannot fail except through an implementation bug, and it carries zero
evidential weight about the world. The "small ordinary joint statistic" asked about in
DEC L38-39 is the full posterior. The workstream draft `/workspace/aci_decision_package_v1.md`
L14, L83 and L112 reaches the same conclusion independently.

## 5. Astra's identities: verified in general algebra

Forecasts: q_joint = P(X xor Y = 1 | h) = p10 + p01 = m_x + m_y - 2 p11 = (1 - rho)/2.
The factorized forecast from the SAME exact marginals (DEC L72-73) is
q_fact = m_x + m_y - 2 m_x m_y = (1 - mu_x mu_y)/2.

    q_fact - q_joint = 2 (p11 - m_x m_y) = 2c = kappa/2.          [VERIFIED]

Brier: for a binary target Z with posterior mean q* = E[Z|h] and any forecast q that is
a function of h,

    E[(q - Z)^2 | h] = (q - q*)^2 + q*(1-q*).

So the per-history excess is (q_fact - q_joint)^2 = 4c_h^2. Hence

    Delta R_XOR = E_h[ 4 c_h^2 ]   (expectation under P(h))          [VERIFIED, with conditions]

Conditions under which the identity holds:
1. Single-component binary Brier (q-Z)^2. This matches repo precedent `_m6_analyze.py`
   L29-31. A two-class Brier sum gives 8E[c^2]. DEC L81/L90 does not state the
   convention. Freeze it explicitly; this clarifies a convention and does not change the
   1/1000 threshold.
2. The factorized arm is the terminal projection of the oracle's exact marginals. If
   arm 2 were an autonomous factorized (mean-field / assumed-density) filter that projects
   after each step, its marginals would also drift (Lemma 4), so the X/Y excesses would be
   nonzero and Delta R_XOR would not be 4E[c^2].
3. c is the terminal (post-reading-8) covariance, and there is no final transition
   (DEC L55-56).

The X and Y Brier excess of arm 2 is identically 0, by construction.

## 6. Which admission conditions are algebraically coupled

The DEC L86-98 signatures in these coordinates:

| Gate | Restated exactly | Status from algebra |
|---|---|---|
| (i) history | current-only Brier > oracle Brier | **Sign settled a priori (PASS)** (see 6a). |
| (ii) joint headroom | E_h[4 c_h^2] >= 1/1000, i.e. E[c^2] >= 1/4000 | Functional of the law of c_h; not computed |
| (iii) selective content | P_h(\|c_h\| >= 1/40) >= 1/4 (because \|Delta q\| = 2\|c\| >= 1/20); "X/Y unchanged" | Same random variable as (ii); the X/Y clause is a tautology |
| (iv) strong reduction | (m,c) reproduces the joint forecasts and update | **Theorem** (section 4); identity check only |

**(ii) and (iii) are coupled.** The zero-covariance substitution of (iii) is literally the
factorized arm of (ii): p11 -> m_x m_y. Both gates are functionals of the single scalar
random variable |c_h| under P(h). (ii) is its second moment; (iii) is an upper-tail mass
condition. Neither implies the other at the frozen thresholds (threshold logic only, no
world values):

- (iii) holding implies E[4c^2] >= (1/4)·4·(1/40)^2 = 1/1600, which is less than 1/1000.
  So (iii) does not imply (ii).
- (ii) can hold with mass concentrated on fewer than 1/4 of histories, since |c| <= 1/4
  allows E[4c^2] up to 1/4. So (ii) does not imply (iii).

Passing both is therefore two views of one omitted quantity, not two independent pieces
of evidence. Both certify only that the product readout of exact marginals discards
XOR-relevant information. Neither certifies that marginal information is insufficient
(see alias_check.md).

The "X/Y forecasts unchanged" and "legal simplex" parts of (iii) hold automatically for
the zero clamp: the product m_x m_y always satisfies the Frechet box. The clamped state is
legal but, in general, NOT a reachable posterior. It is an off-manifold diagnostic
(DEC L99-100, L119-120).

### 6a. Gate (i) holds by structural necessity (sign only; no value computed)

Under the generator, uniform is invariant (XOR translation is a group action), so
X_8 is independent of Y_8. A current-only rival that sees only reading 8 (a Y reading)
must forecast P(X=1) = 1/2. Its X-excess is E_h[(m_x(h) - 1/2)^2], which is strictly
positive iff mu_x,8 != 0 on some history.

Proof that this happens:
1. For any 6-prefix, the two extensions at reading 7 (an X reading) give
   mu_x = (mu + eta o)/(1 + eta o mu). Both values cannot be zero, because that would need
   mu = -eta and mu = +eta.
2. The transition multiplies that mu by a b_x != 0.
3. At reading 8, mu_x,8 = (mu_x' + eta o rho')/D. Both values are zero only if
   mu_x' = rho' = 0, which contradicts step 2.

All histories have positive probability (DEC L63), so the X-excess is strictly positive.
Gate (i) therefore cannot fail; it carries no information about this world beyond
"readings are informative and marginals do not fully mix in one step". If reading 8 is an
X reading, the mirror argument applies to Y.

## 7. Independent rational replay method (SPEC ONLY: run only after human approval)

The goal is two code paths that share no filtering logic and agree with exact equality.

**Path A, the primary forward filter.** A 4-vector of `fractions.Fraction` over states
(00,01,10,11). The transition matrix T is built from the generator: T[z->z'] = sum over
(C,Dx,Dy) in {0,1}^3 of the noise probability times [z' = z xor (C^Dx, C^Dy)]. The
observation step multiplies by diag(L) and normalizes. Readout: m_x, m_y, p11, q_joint,
c. Arms 2 and 3 are derived from Path A's posterior.

**Path B, the independent latent-path enumeration (no recursion, no normalization during
the pass).** Use integer weights only:
- Scale the noise weights to integers: C uses (4,1)/5, Dx uses (49,1)/50, Dy uses (39,1)/40,
  and BSC uses (4,1)/5.
- For every latent trajectory z_1..z_8 in 4^8 = 65,536 paths, compute the integer weight
  w(z) = prior x product of integer transition weights. The prior is 1 per start state
  over a common denominator of 4.
- For each of the 256 histories h, accumulate the integer joint weight W(h, z_8) =
  sum over z of w(z) x prod_t (4 if o_t matches its variable else 1).
- Only at the end form P(h) and P(z_8 | h) as exact Fractions, using a single global
  denominator 4 · (5·50·40)^7 · 5^8.
- Compute the transition weights from the (C,Dx,Dy) enumeration in a separately written
  function. Do not import Path A's matrix.

**Path C, an optional third check: the moment recursion** of section 3 (mu_x, mu_y, kappa)
in Fractions. It catches errors in the derivation itself.

Mandatory exact assertions. No floats anywhere: assert `type(x) is Fraction` or int, and
ban `float()`/`numpy` imports in both modules.
1. sum_h P(h) = 1 exactly, and P(h) > 0 for all 256 histories.
2. Path A posterior == Path B posterior for every h. Compare all four entries with `==`.
3. Chart round trip: Psi^{-1}(Psi(b)) == b. The Frechet box holds for every reachable c
   and for every clamp.
4. Identity checks for every h: q_fact - q_joint == 2c. Also
   sum_h P(h)(q_fact - q_joint)^2 == 4 sum_h P(h) c^2.
5. Symmetry checks: flipping all X-reading outcomes maps (mu_x, mu_y, kappa) to
   (-mu_x, mu_y, -kappa) and preserves P(h). Do the same for Y.
6. If Path C is run, it must match A and B exactly.
7. Record per history the numerator and denominator bit-lengths, to charge
   storage/precision for arm 5 (DEC L76, L128-129).

Provenance: separate authors or at least separate files, written before either is run.
The manifest hash is frozen before execution (DEC L101-103, L126-131; CON L117-119).
Any disagreement means INVALID/halt. It never means "pick the plausible one".

## 8. Summary of findings

1. (m_x, m_y, c) is a chart of the full posterior, so signature (iv) is a theorem.
2. Astra's identities hold, conditional on a single-component Brier and a terminal-
   projection factorized arm.
3. (ii) and (iii) both measure the law of one scalar, |c_h|, and the X/Y clause of (iii)
   is automatic.
4. (i) is guaranteed to pass by a sign argument.
5. The only world-informative content of the admission package is the distribution of
   terminal |c_h| against two thresholds. The meaningful rivals (an autonomous mean-field
   filter, and marginal-only nonlinear decoders) are not in the apparatus. See alias_check.md.

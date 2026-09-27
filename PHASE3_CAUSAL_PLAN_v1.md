# Phase-III causal plan v1 — the five frozen interventions (I1–I5) that establish W is causally load-bearing per consumer

2026-09-27. Deliverable for the G5 card (t_7913d287): *what are the frozen interventions
(I1–I5) that establish W is causally load-bearing for each consumer?* Category B/F —
**design / formalization; do not execute.**

This is a **derived document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It specifies the five interventions —
their surgical definition, their per-consumer prediction, and their per-arm application —
so that G10 can implement them as frozen arms on the six architectures that G4 fixed and
the three specialists that G3 fixed. It does **not** define the coordination condition
(that is G6's), the novel-consumer/sample-efficiency measures (G7's), or the z-leakage
audit (G8's); it defines only the causal load-bearing tests those cards read from.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is a consciousness claim. (2) Seeds are
the replication unit; every signature is a planned-denominator readout reported per seed
family, never a per-family guarantee (AC39/AC68). (3) Every intervention cuts exactly
one link and holds everything else fixed — the Q4 §7 "cut the link, not the neighbour"
contract — and is paired with the rival or degenerate arm that must fail (P6, AC109
rule 1). (4) The G0 demotions bind: V is absent, the maintenance rule A is fixed/reactive
(verdict D), no learned allocator, and no intervention re-introduces either. (5) This is
a causal plan about **W's role for its consumers** (the CAUSAL / SHARED /
FUNCTIONALLY_DISTINCT / AVAILABLE half of H_share), not about persistence (MAINTAINED);
the persistence intervention is inherited from G2 and is cross-referenced, not re-specified.

---

## 0. The one-paragraph answer

The five frozen interventions are the smallest set that turns "the specialists' outputs
correlate with W" into "W's *content* is the cause of each specialist's output, and the
three outputs co-vary *because* they read the same W." **I1 (W-scramble)** overwrites W
with a chosen value w★, holding the observation, parameters, other inputs, and the
recurrent state fixed — the differential-scramble test: the three specialists change in
three *content-specific, functionally different* ways, each predicted by that
specialist's function of W (sign / two-sided threshold / even magnitude-gate). **I2
(W-cut)** removes W from *one specialist at a time* — the per-consumer independence test:
that specialist falls to its exact no-W baseline while the others are byte-unchanged, so
W is load-bearing *for each consumer separately*, not merely for the trio. **I3
(consumer-cut)** disables *one specialist* and leaves W and the others running — the
independence-of-consumers test: W's content trajectory and the surviving consumers'
outputs are byte-unchanged, so W is a genuine shared substrate, not one consumer's
private state that the others eavesdrop on. **I4 (private-copy substitution)** swaps W
for *one* specialist with a private copy equal to W at substitution time and then frozen —
the literal-shared-state test: that specialist's output diverges from the others' exactly
as the ongoing W moves away from the frozen copy, so coordination rides the *identity* of
the shared variable, not merely its momentary value. **I5 (stale/incorrect W)** injects a
*controlled error* into W — the content-vehicle test: the error propagates *coherently*,
each specialist applying its own function to the same wrong W, so the three outputs are
mutually consistent with one (wrong) belief rather than three independent corruptions. The
passing bar for every intervention is stated here and inherited by G10: **the observed
signature must equal the signature W's content predicts** — an exact function of the
injected value, not a non-zero change. A correlated output change that does not match the
predicted function of W is a falsification, not a pass.

---

## 1. Label reconciliation (the I1–I5 numbering changed; this is now canonical)

The G-series documents up to G4 used a two-intervention vocabulary inherited from Q4:
**I1 = cut π** (N1/MAINTAINED) and **I2 = scramble W** (N2/CAUSAL). The G5 card renumbers
the label space for the causal plan and adds three new interventions. To prevent the
AC14-class error (an arm name that does not match the arm actually cut), the mapping is
fixed here and is binding on G6, G9 and G10:

| This plan (G5, canonical) | Prior label (Q4 / G0–G4) | What it is | Predicate served |
| --- | --- | --- | --- |
| **I1 — W-scramble** | I2 (scramble W) | overwrite W, hold all else fixed | CAUSAL + FUNCTIONALLY_DISTINCT |
| **I2 — W-cut** | *(new)* | remove W from one consumer at a time | CAUSAL per consumer |
| **I3 — consumer-cut** | *(new)* | disable one consumer, leave W + others | SHARED (W independent of any one consumer) |
| **I4 — private-copy substitution** | *(new)* | swap W for one consumer with a frozen private copy | SHARED (identity vs value) |
| **I5 — stale/incorrect W** | *(new)* | inject a controlled error into W | CAUSAL as a content-vehicle |

The prior **I1 (cut π)** — the N1/MAINTAINED persistence intervention — is **not** one of
this plan's five. It is already fully specified in G2 §3.2 and G1 §2.5 (cut π's refresh of
W, hold W's value and the sensors fixed, measure the decay time-course and the behavioural
co-decay), and it is inherited by G10 unchanged from there. This plan references it only
where the two must not be conflated (I2 and I4 both leave π running; cutting π is a
different intervention that G2 owns). Nothing here re-specifies or weakens the
MAINTAINED test.

---

## 2. The five interventions at a glance

| # | Name | Alter (what, not what) | Hold fixed | Per-consumer prediction (candidate) | The rival / degenerate arm it exposes |
| --- | --- | --- | --- | --- | --- |
| I1 | W-scramble | W ← w★ (a chosen value) | x_t, parameters, recurrent state, π, contexts u_i | S_pol: sign follows w★; S_plan: threshold-crossing follows w★; S_reg: |w★|-gate follows |w★| — three *different* effects | R2/R3 have no W to scramble |
| I2 | W-cut | W ← neutral, for consumer i only | W for j≠i, x_t, π, contexts | consumer i → its no-W baseline (chance / abstain / release); j≠i byte-unchanged | R2/R3 have no W to cut |
| I3 | consumer-cut | freeze/remove S_i's output | W, π, encoder, consumers j≠i | W trajectory and S_j outputs byte-unchanged | (diagnostic: W must not be S_i's private state) |
| I4 | private-copy substitution | S_i reads a frozen private copy W_i instead of W | W (keeps updating), π, consumers j≠i | S_i tracks the frozen copy; diverges from S_j as W moves | R1/R5 are the all-consumer limit of I4 |
| I5 | stale/incorrect W | W ← a controlled wrong value | x_t, π, contexts | all three apply their own function to the *same* wrong W — coherent error | R1/R5 make the error local, not global |

The predicate each serves is stated in §4–§8; the central quality bar all five share is
§9; the pre-declared gates are §10; endpoints and seeds are §11.

---

## 3. The shared surgical discipline (what "intervene" means in this plan)

Five rules make these interventions *causal* rather than correlational, and each is
binding on G10's implementation:

1. **Cut exactly one link.** Each intervention changes W (or one consumer's access to W,
   or one consumer's existence) and nothing else. The token stream x_1..H, the encoder's
   parameters, the specialists' weights, the paid refresh π, the fixed/reactive rule A,
   and every consumer's private context u_i are held at their intact-run values. A change
   that also perturbs the token stream or a specialist's weights is a different experiment
   and is not one of I1–I5.
2. **Measure the decisive signatures in the probe window.** In the probe (G2 §1.3) every
   token is neutral, so x_t carries zero information about z; W is the *only* carrier of z
   there. This is what makes a scrambled/cut/erroneous W have a *total*, unambiguous
   effect, and what makes the "W is the cause" reading clean (AC109: storage is inert
   where the observation is decisive — so the causal claim is made where the observation
   is *not*). The accumulation-phase variants ("then restore") are run as the companion
   that pins content-tracking (G3 §5), but the load-bearing contrast is the probe.
3. **Every episode completes the horizon.** The task is a discrimination endpoint, not a
   survival endpoint (G2 §1.4): no intervention terminates the episode, so the causal
   readout is a planned-denominator accuracy/consistency per seed, with no termination
   bimodality to condition on. This is the structural fact that keeps I1–I5 clean, and it
   is why none of them trips the organism line's "intervention zeroes the income" wall
   (AC11/12/13): the system is not starved by any of the five.
4. **The tie-break at the cut is a fixed convention, not part of the claim.** When W is
   set to the neutral value (I2) or to 0 (I1 with w★ = 0), S_pol's forced-choice rule
   "ẑ = A iff W > 0" hits its tie. The design fixes one convention (W ≤ 0 → B, stated at
   implementation) and holds it across every arm; the claim is that S_pol's accuracy
   collapses to chance (its output no longer tracks z), never about which side of the tie
   it lands on.
5. **Byte-identity at the intact boundary is the license.** Every intervention is compared
   against a control run in which the same arm runs *unintervened* on the same seed; the
   only permitted difference is the one link the intervention cuts. Where a prediction is
   "unchanged," it must be **byte-identical** (same output string, same W trajectory, same
   ledger), not merely similar (P7's composition license; AC83's method). Where a
   prediction is "changed," the change must be the exact function of the injected content
   (§9).

---

## 4. I1 — W-scramble (CAUSAL + FUNCTIONALLY_DISTINCT)

- **Alter.** Overwrite W with a chosen value w★ ∈ [−6, +6] (the b-bit quantized range,
  G2 §4.2), at the probe entry (t = H−K+1), and hold it there. Do not touch x_t, the
  encoder, the specialists' weights, π, A, or any consumer's context. The recurrent state
  is held at its intact-run value; only the W slot's *content* is replaced.
- **Hold fixed.** Everything except W's value: the token stream, all parameters, π's
  refresh, A, and u_pol = x_t, u_plan = cost, u_reg = (E, d, s).
- **Per-consumer prediction (the differential-scramble signature).** For each injected
  w★, the three outputs are the three specialists' functions of W applied to w★, and they
  differ *in kind* (G3 §3.2, §5):

  | w★ | S_pol (odd) | S_plan (sign+mag) | S_reg (even) |
  | --- | --- | --- | --- |
  | +large (≥ +a) | ẑ = A | commit-A | preserve |
  | −large (≤ −b) | ẑ = B | commit-B | preserve |
  | 0 (neutral) | chance (forced choice, no signal) | postpone | release |
  | +small (0 < w★ < a) | ẑ = A (sign only) | postpone (magnitude below boundary) | release iff |w★| < θ |

  The signature is a **function of w★**, not a direction: sweeping w★ from −6 to +6 traces
  the sign-equivariance of S_pol, the two-sided threshold of S_plan, and the even
  magnitude-gate of S_reg. This is the G1 §2.3 differential-scramble test at the level of
  three consumers, and it is what the two-linear-heads rival cannot reproduce (its heads
  are all odd and co-vary on sign flips, G3 §1).
- **Per-arm application.**
  - **CANDIDATE:** one write to the one W reaches all three → the full differential
    signature, from one scramble. Passes SHARED (single-write reaches all, G1 §2.1-c),
    CAUSAL (all three change), DISTINCT (three different effects).
  - **R4:** scramble the broadcast S_t → the *same* three effects (the readouts are the
    candidate's own). R4 passes CAUSAL + SHARED + DISTINCT here; it differs from the
    candidate only on the maintained/organizational endpoints, not on this scramble
    (G4 §4). The I1 signature alone cannot separate candidate from R4 — and must not be
    expected to; the separation is I5's local-vs-global error and G2's π-cut, not I1.
  - **R1:** scrambling W_1 changes only S_pol; scrambling W_2 only S_plan; W_3 only S_reg.
    The three effects are each reachable, but only by **three separate writes** — a single
    write reaches exactly one consumer, so R1 **fails the single-write test** (G1 §2.1-c).
    This is the SHARED contrast, isolated.
  - **R5:** identical to R1 (three free copies, one write reaches one consumer). Fails
    single-write.
  - **R2:** no W slot exists; there is nothing to scramble. Degenerate — and that is the
    point: R2's h_t is a full hidden vector, not a b-bit maintained latent, so it has no
    W whose content could be selectively overwritten. I1 is inapplicable to R2.
  - **R3:** no W slot; the "content" is the raw history. Degenerate for the same reason.
- **What I1 discriminates.** Candidate/R4 (shared) from R1/R5 (unshared) via the
  single-write identity; and it exposes R2/R3 as lacking any latent to scramble. It is the
  one intervention that tests FUNCTIONALLY_DISTINCT directly (the three different
  effects), so it is the load-bearing arm for the G1 §2.3 predicate.

---

## 5. I2 — W-cut (CAUSAL per consumer)

- **Alter.** Replace consumer i's input with the neutral value (W ← 0) **for i only**;
  consumers j≠i continue to read the intact W. Run once per consumer (three sub-arms:
  cut-S_pol, cut-S_plan, cut-S_reg). π, the encoder, and the W slot itself are untouched —
  W keeps accumulating and being maintained for the other consumers.
- **Hold fixed.** W's actual value for j≠i, x_t, all parameters, π, A, every context.
- **Per-consumer prediction.** Consumer i falls to its exact no-W baseline; the others are
  **byte-unchanged**:
  - **cut-S_pol:** S_pol's accuracy → 0.500 in the probe (no signal survives; its forced
    choice no longer tracks z). S_plan and S_reg read the intact W and are unchanged.
  - **cut-S_plan:** S_plan postpones forever (|W| = 0 < a, b) → commitment rate 0, abstain
    payoff. S_pol and S_reg unchanged.
  - **cut-S_reg:** S_reg releases (|W| = 0 < θ). S_pol and S_plan unchanged.
  This pins CAUSAL *independently per consumer* (G1 §2.2-b): each consumer's output is a
  function of W alone, so removing W for that consumer alone changes only that consumer.
  It is the dual of the sever-history test (G3 §6 gate 5): sever-history holds W and cuts
  the history (AVAILABLE); W-cut holds the history and cuts W (CAUSAL). Together they
  show the consumer uses W *and nothing but W*.
- **Per-arm application.**
  - **CANDIDATE:** the clean per-consumer signature above. Each sub-arm is load-bearing
    for one consumer.
  - **R1:** cutting W_i reproduces the same per-consumer signature (each W_i is its
    specialist's content source). I2 does **not** separate candidate from R1 — both show
    per-consumer load-bearing — which is correct and expected; the separation is I1/I4.
  - **R4:** cutting S_t for i reproduces the signature. No separation.
  - **R5:** cutting copy i reproduces the signature. No separation.
  - **R2:** there is no W to cut. "Remove h_t from head i" is a different intervention
    (h_t is the shared RNN state, jointly computed, not a per-consumer latent); it is not
    I2 and is not run under this label. Degenerate.
  - **R3:** there is no W to cut. "Remove the history from reader i" is a different
    channel. Degenerate.
- **What I2 discriminates.** Nothing among the latent-bearing arms — deliberately. Its
  function is (a) to establish CAUSAL per consumer for the candidate with byte-identity
  on the survivors, and (b) to expose R2/R3 as arms that have no W whose removal is the
  intervention under test. The per-consumer independence it proves is what makes the
  "shared content is independently load-bearing per consumer" reading of N2 real, not a
  pooled claim.

---

## 6. I3 — consumer-cut (SHARED: W is independent of any one consumer)

- **Alter.** Disable one specialist — freeze its output at its intact-run value (or remove
  it from the wiring) — and leave W, π, the encoder, and the other two specialists running
  on the same seed. Run once per specialist (three sub-arms).
- **Hold fixed.** W's accumulation and maintenance, the token stream, the other
  specialists' inputs and weights, π, A.
- **Per-consumer prediction.** W's content trajectory and the surviving consumers'
  outputs are **byte-identical** to the intact run. The disabled specialist's output is
  frozen. This shows W's lifecycle — the encoder's acquisition writes and π's refresh
  under the fixed/reactive rule A — is driven by `(s, E, d)` and the token stream, **not
  by any consumer's output**: W is a genuine shared substrate, not S_pol's private state
  that S_plan and S_reg happen to read.
- **Per-arm application.**
  - **CANDIDATE:** the byte-identity prediction above. A failure (W changes when S_pol is
    disabled) would mean W is coupled to S_pol — a SHARED failure, falsifying the claim.
  - **R1:** disabling S_pol leaves W_2/W_3 and their consumers untouched by construction;
    whether π_1 continues to maintain W_1 is a wiring detail to be fixed at
    implementation (the honest contrast is economic: R1 carries three maintenance burdens,
    the candidate one — G7's endpoint). I3 passes trivially for R1 and does not separate.
  - **R4/R5:** pass trivially (a free register has no consumer-dependent lifecycle).
  - **R2:** "disable one head" is ill-defined (the three heads are jointly parameterized
    off one h_t); treated as degenerate, with the caveat that R2's heads are not separable
    consumers in the sense I3 needs.
  - **R3:** disabling one reader leaves the history and the other readers unchanged;
    passes trivially.
- **What I3 discriminates.** It is diagnostic on the candidate, not a rival separator: it
  verifies the *independence* of W from any single consumer, which is the "not a private
  component" half of SHARED. Its load-bearing value is the byte-identity gate — if W's
  trajectory is not byte-identical under a consumer cut, the candidate's W is revealed as
  a consumer's private state and H_share fails regardless of what I1/I4 show.

---

## 7. I4 — private-copy substitution (SHARED: identity vs value)

- **Alter.** For consumer i, substitute a private representation W_i that is set **equal
  to W at substitution time** (t = H−K+1, probe entry) and then **frozen** — it receives
  no further acquisition writes. Consumers j≠i continue to read the ongoing shared W. Run
  once per specialist. (For R1/R5 this is a no-op: they already hold private copies — see
  per-arm.)
- **Hold fixed.** The shared W (which keeps updating), π, the token stream, the other
  consumers' inputs, all parameters.
- **Per-consumer prediction.** Consumer i's output now equals S_i(W_i = frozen value), and
  it **diverges** from S_j(W_t = ongoing) exactly as the ongoing W moves away from the
  frozen value. In the probe, W does not move (the tokens are neutral, λ = 0), so the
  divergence is zero *there* — the honest place to measure I4 is the **accumulation
  phase**, where W keeps accumulating while the private copy sits still: consumer i tracks
  the stale frozen belief while consumers j≠i track the current one, and the gap between
  them is exactly the accumulated evidence since substitution. If consumer i's output were
  identical whether it read the shared W or the frozen copy, then sharing is inert *for i*
  — it never needed the ongoing updates, only the momentary value. The divergence is the
  signature that coordination rides the **identity** of the shared variable, not its
  momentary value (G1 §2.1-b: same content ≠ shared content).
- **Per-arm application.**
  - **CANDIDATE:** the localized divergence test above. This is the single-consumer probe
    of "does sharing matter," and it is what I4 is for.
  - **R4:** the same test on S_t (the free register keeps updating; the private copy
    freezes). Divergence in the accumulation phase; the candidate-vs-R4 separation is not
    here but on the maintained/economic endpoints (R4 has no π, G2 §4.1).
  - **R1:** I4 is *already* R1's topology — each specialist reads a private copy. The
    relationship is exact: **R1 = I4 applied to all three consumers at once.** So I4 on
    the candidate is the localized version of the full R1 rival, and the honest reading of
    the candidate-vs-R1 contrast is "does privatizing *one* consumer cost anything that
    privatizing *all three* (R1) does not."
  - **R5:** the same as R1 (three frozen fixed copies); R5 = I4-all with fixed content.
  - **R2/R3:** no shared W; inapplicable (there is no shared variable to substitute away
    from).
- **What I4 discriminates.** Candidate (and R4) from R1/R5: it isolates the *identity* of
  the shared variable as the load-bearing thing, per consumer. It is the causal plan's
  contribution to the "coordination requires LITERAL shared state" question that G6 then
  turns into a measurable coordination condition — I4 supplies the per-consumer
  load-bearing fact, G6 supplies the cross-consumer condition.

---

## 8. I5 — stale/incorrect W (CAUSAL as a content-vehicle)

- **Alter.** Inject a *controlled error* into W at the probe entry, then hold it. Two
  error models, run separately: **(a) wrong-sign** — W ← −w_true with |w_true| large (a
  confident, opposite belief); **(b) stale** — W ← W_{t−Δ} (the value Δ steps earlier,
  the "failed to update" error). (The magnitude-collapsed error W ← W/k is G3's canonical
  magnitude-shrink perturbation, already covered under I1's w★ sweep, and is not a
  separate I5 arm.)
- **Hold fixed.** x_t, all parameters, π, A, every context. Only W's content is wrong.
- **Per-consumer prediction (the coherence signature).** Each specialist applies its own
  function to the *same* wrong W, so the three outputs are **mutually consistent with one
  (wrong) belief** — not three independent corruptions:
  - **wrong-sign (truth A, W ← −3):** S_pol → ẑ = B (wrong, confident); S_plan → commit-B
    (|−3| crosses −b, confident wrong commitment); S_reg → **preserve** (|−3| ≥ θ — the
    retention gate reads magnitude, not correctness, so a wrong-but-decisive belief is
    *still worth keeping*). The three are exactly S_pol(−3), S_plan(−3), S_reg(−3).
  - **stale (truth A, W ← W_{t−Δ} ≈ +1):** S_pol → ẑ = A (right by luck of the stale
    value, or wrong if the sign lags); S_plan → postpone (|+1| below a); S_reg →
    preserve/release per |+1| vs θ — all consistent with the *stale* belief.
  - The **coherence check** is the load-bearing one: the triple of outputs must equal
    `(S_pol(w), S_plan(w), S_reg(w))` for the injected w, i.e. they must be mutually
    consistent. If the three outputs were instead inconsistent with any single w (e.g.
    S_pol says B while S_plan postpones *and* S_reg releases, which no single confident
    w produces), then the specialists are not reading the same W — W is an incidental
    correlate, not the common content, and H_share fails.
- **Per-arm application.**
  - **CANDIDATE:** one wrong W produces a **coherent global error** — all three
    consistently wrong in their own way. Passes the content-vehicle test.
  - **R4:** same — one wrong S_t → coherent global error. (R4's content is the same
    sufficient statistic, so the coherence signature is identical; again the separation
    from the candidate is on the maintained endpoints, not here.)
  - **R1:** a wrong W_i produces a **local** error — specialist i wrong, j≠i unaffected
    (their W_j is correct). To produce a global error in R1 requires corrupting all three
    W_i. **This is a discriminator:** shared content makes a single error propagate
    coherently to all three; unshared content confines it to one.
  - **R5:** same as R1 (local error).
  - **R2/R3:** no W; inapplicable.
- **What I5 discriminates.** (a) shared (candidate/R4) from unshared (R1/R5) via the
  global-vs-local error signature; (b) content-vehicle from incidental-correlate via the
  coherence check — if the specialists secretly read x_t and W is a bystander, injecting a
  wrong W would leave them *correct*, not coherently wrong. I5 is therefore the sharpest
  single test that W's **content** (not its mere presence) is the causal vehicle.

---

## 9. The central quality bar: the signature must match the content's prediction

The card's requirement — "a successful result requires MORE than correlated output
changes: intervention signatures must MATCH what W's content predicts" — is operationalized
as the standing rule over all five interventions:

**For every intervention, the predicted output is an exact function of the injected
content, and the gate is a match, not a non-zero change.**

- **I1:** the signature is the *function* w★ ↦ (S_pol(w★), S_plan(w★), S_reg(w★)). A
  result is a pass only if the measured triple equals the predicted triple for every w★
  in the sweep, up to the finite-sample resolution. A measured "all three changed" that
  does not trace the sign/magnitude/even structure of §4 is a **falsification** — it is a
  correlated movement, not a content-driven one.
- **I2:** the unchanged consumers must be **byte-identical** to the intact run, and the
  cut consumer must equal its exact no-W baseline. "Similar but not identical" is a fail
  (it means the cut leaked into another channel).
- **I3:** W's trajectory and the surviving outputs must be **byte-identical** to the
  intact run. Any drift falsifies SHARED.
- **I4:** consumer i's output must equal S_i(frozen copy) exactly, and the i-vs-j
  divergence must equal exactly the evidence accumulated since substitution. A consumer
  that tracks the *ongoing* W despite reading a frozen copy is reading something other
  than its declared input — a wiring bug, caught by the exact-match gate (the AC85 lesson:
  a silently wrong wiring is the failure mode, and the exact match is what exposes it).
- **I5:** the triple must equal (S_pol(w), S_plan(w), S_reg(w)) for the injected w, i.e.
  be mutually consistent. An inconsistent triple is a fail.

The discipline behind this is the program's own: AC109 rule 1 (the causal claim is made
where the content is the only carrier — the probe); AC110 (correctness rides the content,
not the surrounding machinery — so a wrong content must move the output exactly, not
approximately); and AC85 (a wrong-but-valid value must be followed faithfully, never
silently corrected — the private copy and the wrong W must be *followed*, not repaired).

---

## 10. Pre-declared gates (consistency checks G10 must assert)

Each gate is pre-declared here and none may be amended after seeing results (AC16/17
discipline). The shape of each gate is matched to the claim's shape: categorical "W is
load-bearing" claims gate on per-individual dominance / a threshold met by every seed,
never on a mean margin (AC16); equivalence claims gate on byte-identity, never on
"similar" (P7).

1. **Single-write-reaches-all (SHARED, I1).** One scramble of the candidate's W changes
   all three consumers' outputs; the same three changes require three writes in R1 and
   R5. Gate: the candidate's three-output signature is produced by one write, R1/R5's by
   three, on every seed.
2. **Differential-scramble signature (DISTINCT, I1).** On a fixed seed family, the
   measured w★ ↦ triple equals the predicted function of §4 up to the finite-sample
   resolution. A flat (co-varying) response across the three specialists is a
   falsification (the two-linear-heads rival, G3 §1).
3. **Per-consumer causal independence (CAUSAL, I2).** For each of the three sub-arms,
   the cut consumer reaches its exact no-W baseline and the two survivors are
   byte-identical to the intact run. Gate per consumer, not pooled.
4. **Consumer-independence of W (SHARED, I3).** For each sub-arm, W's trajectory and the
   surviving outputs are byte-identical to the intact run. Any drift falsifies.
5. **Literal-shared-state (SHARED, I4).** For each sub-arm, the privatized consumer's
   output equals S_i(frozen copy) exactly and the i-vs-j divergence equals the evidence
   accumulated since substitution (measured in the accumulation phase). A consumer that
   tracks the ongoing W despite the frozen copy is a wiring failure, not a result.
6. **Coherent-error propagation (content-vehicle, I5).** For each error model, the
   measured triple equals (S_pol(w), S_plan(w), S_reg(w)) for the injected w, on every
   seed. An inconsistent triple falsifies. The shared-vs-unshared contrast (candidate/R4
   global error vs R1/R5 local error) is a recorded prediction, reported not gated where
   the local/global distinction is already pinned by gate 1.
7. **Byte-identity at the intact boundary (all five, P7).** Every intervention is paired
   with its uninterrupted control on the same seed; the intact control must reproduce the
   frozen no-intervention run byte-for-byte before any difference is attributed to the
   intervention (AC83's method).

The rival-family sweep (P6 rule 2) binds here as it does everywhere: the sweep over w★
(I1), the per-consumer sub-arms (I2/I3/I4), and the error models (I5) are the level
families; G10 sweeps them alongside the arms' own hyperparameters, never fixing one while
selecting the other's best member (AC11's fatal error).

---

## 11. Endpoints and seed discipline

- **Endpoints, recorded per seed and per consumer (planned-denominator, never pooled):**
  (I1) the w★ ↦ output triple and its match error to the predicted function; (I2) the cut
  consumer's accuracy/commitment/retention and the survivors' byte-identity flag; (I3) the
  byte-identity flag on W's trajectory and the survivors; (I4) the privatized consumer's
  output and the i-vs-j divergence magnitude; (I5) the coherence flag and the
  global/local error extent. Chronological scalars (first divergence tick, first
  incoherence tick) are recorded where they carry the mechanism (the G-series analogue of
  the organism line's first-acquire/loss scalars).
- **Seeds.** Disjoint engineering and finals families; engineering seeds are excluded
  from every final sample; families are never mixed (AC39). The replication unit is the
  episode seed (one draw of z and its token stream); N episodes × 1 history = N units.
- **No saturation.** The probe accuracy baseline (0.500) and the Bayes ceiling (0.812,
  G2 §2.3) leave a graded gap for every intervention's effect to occupy; the endpoints
  are chosen so a passing signature is a graded, non-saturated readout (AC47).
- **What is NOT an endpoint here:** any coordination, transfer, or interference measure
  (G6/G7); any z-leakage audit (G8); the π-cut decay signature (G2's, MAINTAINED). This
  plan's five interventions establish per-consumer causal load-bearing; they do not by
  themselves establish coordination.

---

## 12. Claim ceiling and what this does NOT claim

- **What a pass earns, at most.** That, in the candidate, W's *content* is the cause of
  each specialist's output (CAUSAL, per consumer), that the three consumers respond
  *differently* as their functions of W predict (FUNCTIONALLY_DISTINCT), that W is one
  variable whose identity — not merely its value — is load-bearing (SHARED), and that a
  single error in W propagates coherently to all three (content-vehicle) — i.e. the
  CAUSAL ∧ SHARED ∧ FUNCTIONALLY_DISTINCT ∧ AVAILABLE half of H_share (G1 §3), at the
  stated degree. Nothing stronger.
- **Not claimed here.** The MAINTAINED predicate (G2's π-cut owns that); any coordination
  condition (G6); any novel-consumer / sample-efficiency result (G7); any absence of
  z-leakage (G8); any trained outcome (this is a design, run by G10); any "global
  broadcast", "workspace seat" (O3/GWT), metacognition (N4), autopoiesis, or any claim
  crossing the level-(d)/(e) boundary. This is a level-(b)/(c) causal-intervention design.
- **The interventions are frozen in design, not in execution.** "Frozen" here means:
  pre-specified before training, fixed in this document, and carried into G10's protocol
  without post-hoc amendment. The frozen *execution* (hashed protocol, `mkdir(exist_ok=False)`
  results dir, audit, replay) is G10's obligation, exactly as the other G-series documents
  defer it.

---

## 13. Provenance

Instantiates the causal-intervention vocabulary over the six arms of
`PHASE3_ARCHITECTURES_v1.md` (G4 — candidate SLW + R1–R5, §8 comparability contract, §10
"only the candidate (and R1) has a π to cut and a W to scramble") and the three specialists
of `PHASE3_SPECIALISTS_v1.md` (G3 — S_pol sign / S_plan SPRT / S_reg even-gate, §3.2
invariance classes, §5 differential-scramble effects). The predicate each intervention
serves is `SHARED_CONTENT_DEFINITION_v1.md` (G1 §2 — the five criteria, the single-write
test §2.1-c, the do-operator §2.2-b, the differential-scramble §2.3-c, the sever-history
§2.4-c, and the conjunction H_share §3). The task and its probe/ceiling are
`PHASE3_INFERENCE_TASK_v1.md` (G2 — §1.3 probe, §2.3 anchors, §3.2 the two decisive
interventions). The two-intervention predecessor vocabulary (I1 = cut π, I2 = scramble) is
`PHASE3_BASELINE_v1.md` (G0 §4) and `ACI_MINIMAL_NEURAL_ARCHITECTURE_v1.md` (Q4 §7
intervention map, the "cut the link not the neighbour" contract, the mandatory rival set).
The gate-shape and rival-sweep discipline is `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (Q2 —
P6, P7, D1–D8). Organism study references read from the skill's `references/` dir where
named (`ac11`/`ac16`/`ac17` — gate-shape and rival-sweep; `ac39`/`ac68` — seed/bimodality;
`ac47` — graded vs saturated; `ac83`/`ac85` — byte-identity license and the silently-wrong
wiring failure mode; `ac109` — causal claim where the content is the only carrier; `ac110`
— correctness rides content).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is a
causal-intervention design, not a result.

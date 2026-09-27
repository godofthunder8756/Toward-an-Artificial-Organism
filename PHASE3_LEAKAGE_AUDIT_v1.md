# Phase-III leakage audit v1 — the z-decodability spec across every pathway, per arm

2026-09-27. Deliverable for the G8 card (t_65e9c99e): *can z be decoded from any
pathway other than W — and if so, is that pathway a disclosed design property or a
hidden leak?* Category B/F — **design / formalization; do not execute.**

This is a **derived document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It specifies the audit that G10
implements **on top of** the six frozen arms of `PHASE3_ARCHITECTURES_v1.md` (G4) and
the three specialists of `PHASE3_SPECIALISTS_v1.md` (G3), on the task of
`PHASE3_INFERENCE_TASK_v1.md` (G2). It does **not** define the training objective or
the frozen protocol (G10's); it fixes only the leakage measurement those cards leave to
it, which G9's reduction audit (questions 1, 2, 5, 8) and G10's gate set then read.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is a consciousness claim. (2) Seeds are
the replication unit; every decode rate is a planned-denominator readout reported per
seed family, never a per-family guarantee (AC39/AC68). (3) The audit is a **measuring
instrument**, not a component: its decoder never feeds back into any arm's forward
graph, and its only output is a verdict plus a rate. (4) "Carries information about z"
is not the same as "leaks z" — the distinction in §1 is the whole point of the card,
and conflating them is the failure mode this document exists to prevent. (5) The G0
demotions bind: V is absent, A is fixed/reactive (verdict D), and no audit step
re-introduces either.

---

## 0. The one-paragraph answer

The audit asks one question over every arm and every candidate pathway: **is z decodable
from any state other than W, and is that state *free* — available to a specialist or
persisting without the paid refresh π?** Because W is the b-bit quantized scalar
log-likelihood ratio and the tokens are conditionally i.i.d. given the fixed cause, W is
the **minimal sufficient statistic** (G2 §2.1), which is exactly the claim that
`z ⊥ (everything else) | W`. The audit is the empirical verification of that conditional
independence, run per arm. It measures **three grades** for each of seven pathways
(L1 GRU hidden state, L2 specialist private state, L3 maintenance variables, L4 trainer
signals, L5 timing, L6 action history, L7 cached observations): **INERT** (decodes at
chance), **DISCLOSED** (carries z, but is a declared property of that arm — the rival's
history, the candidate's own x_t context in the accumulation phase), or **LEAK** (carries
z, is free, and reaches a specialist or persists without π — not in the declared
topology). The candidate's claim — "W is the shared, paid-maintained information source"
— **fails** iff some pathway P ≠ W is LEAK grade, i.e. iff in the probe (where x_t is
neutral and W is the only carrier) a free pathway decodes z above chance, **or** a
pathway other than W is both z-carrying and (a) available to a specialist (sever test
fails) or (b) persists z when π is cut (the F1 free-recurrence test). Rival arms do not
"fail" for carrying z through their defining states — R3's full history, R2's h_t, R1's
three W_i, R4/R5's supplied λ are **disclosed advantages** (G4 §8 rule 4); the audit's
job there is to **quantify** each alternative pathway on the same decoder scale, so the
candidate's burden is measured honestly, never hidden.

---

## 1. What "leakage" means here — the three grades and the falsification condition

The card's premise is that z reaches the specialists *through W*. That premise is
precise and falsifiable, but only if "through W" is not silently widened. This section
fixes the vocabulary once; §3–§5 apply it per pathway and per arm.

### 1.1 Information content ≠ leakage

Two facts that must be held apart, or the audit mis-gates:

- **A state can carry z and be perfectly legitimate.** The encoder's GRU hidden state
  h_t (L1) carries *more* z than W — it is the full-precision pre-quantization carry,
  and W is its 5-bit quantization, so `I(z; h_t | W) > 0` **by construction**. This is
  not a leak; it is the acquisition machinery being richer than the maintained summary,
  which the architecture explicitly permits (the specialists read W, not h_t).
- **A state can carry z and be the entire claim.** W itself carries z — that is what it
  is *for*. R1's W_i, R2's h_t, R3's history all carry z and are the *defining*
  properties of those arms.

Leakage is therefore **not** "z is decodable from P". It is the narrower conjunction:

> **LEAK(P)** ⟺ P carries z **and** P is **free** (unpaid, not the declared W) **and**
> P **reaches a specialist or persists** — i.e. P is not in the arm's declared topology.

The three grades follow, and every pathway gets exactly one per arm:

| Grade | Condition | Verdict for the candidate | Example |
| --- | --- | --- | --- |
| **INERT** | decode from P = chance (0.5, probe) | pass | token timing t (L5a) |
| **DISCLOSED** | carries z, but is a declared input/state of that arm, disclosed in G4 §8 | quantified, not a failure | x_t to S_pol in accumulation; R3's history; R1's W_i |
| **LEAK** | carries z, is free, and is available-to-specialist or persistent | **FALSIFIES** | h_t wired to S_pol; a specialist with recurrent carry; A reading W |

### 1.2 The equivalence bar (what counts as "equivalent information")

The card says the claim fails if another free pathway carries **equivalent** information,
not merely *any* information. The bar is set by the probe, where the design guarantees
that **W is the only carrier** (G2 §1.3: every probe token is neutral, so x_t is
z-blind). In the probe:

- **Chance floor** = 0.500 (z uniform).
- **W ceiling** = the Bayes ceiling 0.812 at the default 24 informative steps (G2 §2.3).

A free pathway P is **z-equivalent to W** (leak-grade) iff a decoder from P alone
reaches, in the probe, an accuracy above `0.500 + ε`, where ε is the finite-sample
resolution (§2.5); the **magnitude** of the excess is the leak's grade and is always
reported (a pathway at 0.53 is a weak leak, at 0.80 a full-equivalence leak). In the
accumulation phase the bar is deliberately looser (x_t legitimately carries the
memoryless 0.606 bound, G2 §2.3), so the **probe is the load-bearing contrast** and the
accumulation-phase readout is the companion that bounds the x_t contribution.

### 1.3 The central falsification condition (stated once, used everywhere)

For the **candidate**, the claim "W is the shared information source" **FAILS** iff any
of these hold, on any seed, for some pathway P ≠ W:

1. **Availability leak** — P is in the forward graph at eval and a specialist's output
   changes when P is severed (§4.1): the specialist reads P, so P is a z-pathway to
   behaviour. (Covers L1 mis-wired, L5 cross-consumer, L6 output-recurrence, L7 history
   buffer.)
2. **Free-persistence leak (F1)** — with π cut, P still permits z-decoding above chance
   at the probe: P retains z without the paid refresh. (Covers L1's persistence face;
   the N12 F1 free-recurrence finding, carried.)
3. **Weight/trainer leak** — with W scrambled (I2) at the probe, a specialist's output
   still tracks z above chance: z reached that specialist through its weights, not
   through W. (Covers L2's weight face and L4's trainer-signal face.)

For the **rivals**, the falsification condition is *inverted*: the audit must show that
the rival's alternative pathway is **real and quantified** (R3's history decodes ≥ the
candidate's W; R1's three W_i each decode ≈ W; R2's h_t decodes ≈ W; R4/R5's S_t decodes
at the ceiling) — a rival whose declared pathway silently carries *less* z than claimed
is a confounded comparison (G4 §9: a rival loss must be attributable to the removed
property, not to a weakened information path). The rival that *fails its own*
quantification is a defect to fix, not a result to report.

---

## 2. The decode-test instrument (the measuring apparatus, fixed here)

The audit's decoder is a supplied measuring instrument, identical across all six arms
and all seven pathways. Its parameters are fixed here so that "candidate has no leak"
and "R3 has a history channel" are read on **one** scale.

### 2.1 What the decoder is

- A **capacity-capped readout** — logistic regression on the pathway's features (or a
  single hidden layer of fixed width ≤ 64, at G10's option, with the choice recorded) —
  trained to predict z from a **frozen snapshot** of the pathway's activations. It is
  trained on **held-out episodes**, never back-propagated through any arm's weights, and
  never on the same seeds it is evaluated on (§2.4).
- **The decoder is not part of any arm.** It writes nothing into the forward graph, is
  not trained jointly with the arm, and its only effect on the study is the reported
  decode rates. This is the organism line's observer/scaffold discipline, applied to the
  neural bridge: a measuring instrument must be labelled and never counted as an
  autonomous result.

### 2.2 The reference ladder (three fixed points every decode is read against)

| Reference | Value | Meaning |
| --- | --- | --- |
| **Chance floor** | 0.500 | z uniform; a pathway at this carries no z |
| **Memoryless bound** | 0.606 clean / 0.500 probe | what x_t alone buys (G2 §2.3); bounds the L5/L7 accumulation contribution |
| **W ceiling** | 0.812 (24 informative steps) | decoding z from W itself; the Bayes-optimal readout (G2 §2.3) |

Every decode accuracy is reported **with** these three anchors, per seed family.

### 2.3 The two decode variants

1. **Marginal decode** — `acc(z | P)`: train the decoder on P alone. Measures how much
   z P carries at all.
2. **Conditional decode** — `acc(z | W, P)` vs `acc(z | W)`: train on `[W ⊕ P]` and on
   `W` alone; the difference `Δ(P|W) = acc(z|W,P) − acc(z|W)` measures whether P adds
   z-information *beyond* W. **Interpretation is grade-dependent** (§1.1): for a pathway
   that should be absent from the candidate (L6, L7, L2 recurrent carry, L3 z-reading),
   `Δ > 0` is a leak; for acquisition machinery (L1) and rival-defining states, `Δ > 0`
   is expected (h_t is richer than 5-bit W) and is **reported, not gated as failure** —
   the gate there is the sever and F1 tests (§4), not the conditional decode.

### 2.4 Seed discipline for the decoder

The decoder is trained on a **disjoint** seed family from the one it is evaluated on
(e.g. train on engineering 0–7, evaluate on finals 8–15, never the reverse), so it
cannot memorize z. This is the same disjoint-family rule the arms obey (AC39), applied
to the instrument. z is the decoder's **label only**, never a forward input anywhere.

### 2.5 The finite-sample resolution ε

The gate "above chance" is a categorical claim and must not rest on a hairline margin
(AC16/17). ε is the decode-accuracy standard error on the held-out family — the
binomial SE `√(p(1−p)/N)` at N evaluation episodes — and is reported with every rate. A
pathway is leak-grade only if `acc(z|P) − 0.500 > ε` (probe); the p-value of the
exact sign test against chance is the companion (n ≥ 8, the AC38 method).

---

## 3. The seven pathways, enumerated and pre-classified

Each pathway is defined, its z-carrying status stated, the arms that possess it named,
and the specific test it receives. The order is the card's. **L1–L3** are the candidate's
live internal states; **L4–L7** are the channels that could smuggle z through time,
weights, or other consumers.

### L1 — the GRU hidden state h_t

- **Definition.** The encoder's recurrent hidden state: the full-precision carry that
  maps `(h_{t-1}, x_t) → W_t` (G4 §2). Real-valued, dimension d_h ≥ b, the state *before*
  the b-bit quantization.
- **Carries z?** Yes — more than W does (it is the unquantized sufficient statistic;
  `I(z; h_t | W) > 0` expected). **This is disclosed and legitimate** (§1.1).
- **Arms that have it.** CANDIDATE (one), R1 (three enc_i → three h_i), R2 (h_t is the
  whole state). R4/R5 have no recurrent encoder (fixed update); R3 has no encoder.
- **Two faces, two tests.**
  1. **Input face (availability).** h_t must not be a forward input to any specialist —
     specialists read W + context only (G3 §2). Test: the **sever test** (§4.1) — cut
     h_t from every specialist; outputs must be byte-identical.
  2. **Persistence face (F1).** h_t must not retain z when π is cut. Test: the
     **free-recurrence test** (§4.4) — with π cut, decode z from h_t at the probe; must
     be chance. The no-maintenance control must run the recurrence **with W zeroed**,
     not a no-recurrence policy (N12 F1 / G0 §3.7); a h_t that independently carries S_H
     past the π-cut is a free hidden memory and falsifies MAINTAINED.
- **Quantification.** Marginal `acc(z | h_t)` is reported (expected ≥ W ceiling, since
  h_t is richer); it is a **capability statement about the encoder**, not a leak finding.
  The leak verdicts are the two tests above, not this number.

### L2 — specialist private states

- **Definition.** Two sub-cases: (a) **weights** θ_i — each specialist's learned
  parameters, which received z through the training gradient; (b) **recurrent carry** —
  any hidden state a specialist keeps across ticks.
- **Carries z?** (a) Weights encode the *function of W*, not z directly; whether they
  encode a z-bypass is exactly what must be tested. (b) Any recurrent carry accumulates
  past W-derived outputs and would carry z forward — a leak if present.
- **Arms that have it.** CANDIDATE (θ_i only; specialists must be **stateless** readouts
  of (W, u_i)); R1 additionally has the private W_i (a declared state, quantified not
  gated); R2's heads are jointly read off h_t; R3's readers; R4/R5's heads.
- **The test (weight/trainer face, and the statelessness pin).**
  1. **Statelessness (wiring).** Assert every candidate specialist is a stateless map
     `S_i(W, u_i)` with **no recurrent carry** — S_plan's SPRT is a function of the
     *current* W (G3 §2.2), not an internal timer counting postpones; any timer is an
     L6 action-history leak in disguise.
  2. **Weight-bypass test (I2 re-read as a leak detector).** With W scrambled (I2, G5
     §4) at the probe, decode z from S_i's output (or final activation): must be chance
     (0.500). If S_i's output still tracks z, θ_i encoded a z-direct pathway (or S_i
     reads something other than W) — a leak that falsifies both CAUSAL and AVAILABLE.
  3. **R1 quantification.** Each private W_i decodes z at ≈ the W ceiling (the same
     inference solved thrice, G4 §3); assert the three W_i's decode rates agree to the
     training-noise floor, or the arm is not "the same inference three times."
- **What the audit guards.** That the specialist's *own* state is not a second,
  free z-channel; the candidate's specialists must be pure functions of W (+ z-blind
  context in the probe).

### L3 — maintenance variables (E, d, s) and A's decision

- **Definition.** The raw bookkeeping: remaining budget E, age/countdown d since last
  refresh, regime s ∈ {accumulate, probe}; and the maintenance rule A's refresh vector,
  which spends E and resets d.
- **Carries z?** Only if A (or E/d's evolution) depends on W. Verdict D fixes A as
  **fixed/reactive on (s, E, d) only** (G0 §3.3) — it does **not** read W. Then E, d
  evolve as a function of `(s, E_0, d_0, t)` alone, hence are **z-blind by construction**.
  If A were allowed to read W (a learned allocator), d would reset on |W|-events and
  carry |z| — the leak this audit forbids.
- **Arms that have it.** CANDIDATE and R1 (three independent π_i). R2/R3/R4/R5 have no
  paid maintenance, hence no E/d.
- **The test.**
  1. **Wiring (z-blindness of A).** Assert A's refresh decision is a pure function of
     (s, E, d) — no W, no |W|, no S_reg output, nothing W-derived — in the frozen code
     (source-level check, the AC-class "assert the call site" discipline).
  2. **Decode.** Decode z from the (E_t, d_t) trajectory and from A's refresh decisions:
     must be chance (0.500) in the probe, and ≤ the memoryless bound in accumulation.
  3. **Ablation.** Sever any (hypothetical) W→A edge and confirm the refresh schedule is
     byte-identical (§4.1).
- **What the audit guards.** That the *maintenance machinery* is not a free z-channel.
  This is the audit's enforcement of verdict D at the level of information flow, not
  just at the level of "A is hand-coded."

### L4 — trainer signals (z as the training target)

- **Definition.** z is the disclosed training-only scaffold (G2 §1.1): the supervised /
  ELBO target that grades the encoder and, through the reward, the specialists. The
  gradient path `z → loss → weights` is legitimate at train time.
- **Carries z?** The *weights* carry the learned mapping; the leak is if z reaches a
  specialist's **output at eval** other than through W.
- **Arms that have it.** All learned arms (CANDIDATE, R1, R2, R3). R4/R5 have no learned
  inference (λ supplied), so their only learned parameters are the heads — still graded
  by z, still audited.
- **The test.** Three checks, in order:
  1. **Forward absence.** Assert z is not a forward node anywhere at eval (no z input to
     encoder, specialist, or A) — a wiring check (G2 §1.1, G4 §8 rule 2).
  2. **Loss factoring.** Assert each specialist's eval-relevant loss is a function of
     (S_i's output, u_i) with z entering **only** as the comparison target at train
     time — i.e. the loss does not inject z into S_i's input.
  3. **The weight-bypass test (shared with L2).** Scramble W (I2) at the probe; every
     specialist's output must collapse to chance. A specialist that stays above chance
     has a z-pathway through its weights — the trainer signal leaked past W.
- **What the audit guards.** That "z is a training scaffold" remains true at the *flow*
  level, not just the *interface* level. The ELBO/regularization must not smuggle z into
  a consumer except through W.

### L5 — timing

- **Definition.** Two kinds: (a) **token timing** t — the episode clock, a function of
  the fixed structure (H, K); (b) **commitment time** τ — when S_plan crosses its SPRT
  boundary, a function of W's trajectory (G3 §2.2).
- **Carries z?** (a) No — t is z-independent by construction (the probe is at fixed
  H−K+1 regardless of z). (b) Yes — τ is W-derived, so it carries z (and |W|). That is
  S_plan's *job*; the leak is if τ is observable to another consumer.
- **Arms that have it.** τ: every arm with S_plan (all six — S_plan is a shared
  specialist, G3). t: all.
- **The test.**
  1. **Token-timing decode.** Decode z from t: must be chance (0.500). (Cheap, run once,
     confirms the clock is z-blind.)
  2. **Cross-consumer sever (the real test).** Assert no specialist receives another
     specialist's output or timing as input — S_pol reads (W, x_t), S_plan reads (W,
     cost), S_reg reads (W, E, d, s); **no edge carries τ or any y_j to a different
     consumer** (G3 §2, G6 §1). Test: sever any such edge (if present) and confirm the
     consuming specialist is byte-identical (§4.1). If S_pol could read τ, it would
     recover z without W — a leak.
  3. **Quantification.** Report `acc(z | τ)` as a capability statement (it should ≈ the
     W ceiling — S_plan is reading W); it becomes a leak **only** if τ is wired to
     another consumer, which test 2 rules out.
- **What the audit guards.** The independence of consumers: a shared W must be the only
  information channel *between* them; timing is the subtlest covert one.

### L6 — action history

- **Definition.** The specialists' past outputs `y_1..y_{t-1}` (and A's past refresh
  decisions), which are functions of W and hence carry z.
- **Carries z?** Yes, if any component's forward state depends on past outputs — i.e. if
  there is recurrent carry over actions (L2-b is its specialist-local form; L6 is the
  general form including A).
- **Arms that have it.** Potentially any; it must be absent by construction everywhere
  in the candidate.
- **The test.**
  1. **No output-recurrence (wiring).** Assert no component's forward state at tick t
     depends on any specialist's output or A's decision at t′ < t, **except** through
     W's trajectory (which is the declared content). The encoder's GRU integrates past
     *inputs* x, not past *outputs* — that is L1, not L6.
  2. **W-cut-at-probe test.** Cut W for a specialist at probe entry (I2); its output at
     H must be chance. A specialist that still tracks z did so via its own past outputs
     (recurrent carry) — a leak. (Shared with L2-b; L6 states it for the general
     component, not just the specialist.)
- **What the audit guards.** That no component — specialist or maintenance rule — is a
  free accumulator of the specialists' own (z-carrying) history.

### L7 — cached observations (the raw history x_1..x_t)

- **Definition.** Any buffer holding the raw token stream, accessible to a specialist
  outside the encoder's forward pass.
- **Carries z?** Yes, fully (the history *is* the evidence). By design the candidate has
  **no** such buffer (AVAILABLE, G1 §2.4: specialists read W, not the history).
- **Arms that have it.** **R3 by design** (full bounded window M ≥ H — its defining
  property, disclosed, the information-ceiling rival); **R2** implicitly (h_t integrates
  the history — covered under L1, but note R2 has no separate buffer); the candidate and
  R1/R4/R5 must have none.
- **The test.**
  1. **Buffer absence (wiring).** Assert no raw-token buffer exists in the candidate's
     forward graph reachable from a specialist (source-level check).
  2. **Sever-history test (G3 §6 gate 5, G1 §2.4-c).** Hold W and the context fixed,
     remove access to x_1..x_t from every specialist; outputs must be byte-unchanged. A
     consumer whose output degrades was re-inferring from the history — a leak that
     falsifies AVAILABLE.
  3. **R3 quantification.** R3's history decode `acc(z | x_1..x_H)` is measured and must
     reach **≥** the candidate's W-ceiling accuracy (it should — it has the full
     history); this is the ceiling the candidate's b-bit W must match (G4 §7). A lower
     value is a defect in R3, not a candidate win.
- **What the audit guards.** That the candidate's W is genuinely a *sufficient summary*
  and not a cue into a hidden replay buffer.

---

## 4. The ablation protocol (what "run ablations" means here)

Four ablations, each surgical (G5 §3: cut exactly one link, hold all else fixed), each
paired with its uninterrupted control on the same seed (byte-identity license, P7).

### 4.1 Sever test (availability ablation)

**Cut pathway P from every specialist; everything else intact.** The specialist
outputs must be **byte-identical** to the intact run. A change means the specialist read
P, so P is a z-pathway to behaviour (leak). Run for L1 (h_t), L5 (cross-consumer edges),
L6/L7 (any recurrence/history edge found by the wiring checks). This is the audit's
version of G5's I3 discipline (byte-identity at the severed boundary).

### 4.2 W-cut (I2) as the leak detector

**Remove W from one specialist at a time (G5 §5); keep every other pathway intact.**
That specialist's output must reach its exact no-W baseline (chance in the probe) — and
the *other* specialists must be byte-unchanged. This is the decisive leak test: if a
specialist's output still tracks z with W cut, some **other** pathway (its weights, a
recurrent carry, a history buffer, a cross-consumer edge) is carrying z. The audit
reports *which* pathway by cross-referencing §3's per-pathway tests.

### 4.3 Decode ablation (instrument sanity)

**Train the decoder on P, then zero P; decode accuracy must fall to chance.** This
establishes the decoder was reading P and not a confound (the organism line's "the
decoder measures what it claims" check). If the decoder stays above chance after P is
zeroed, it read a correlated state — the pathway probe is mis-wired and must be fixed
before any leak verdict is trusted (AC85: a silently wrong wiring is the failure mode).

### 4.4 Free-recurrence ablation (F1, the persistence face of L1)

**Cut π's refresh of W; hold everything else; run the recurrence with W zeroed** (not a
no-recurrence policy — N12 F1). At the probe, decode z from h_t and from every other
state: all must be chance. A h_t (or any state) that independently retains S_H past the
π-cut is a free hidden memory — it carries z without paid maintenance and falsifies
MAINTAINED and "W is the paid source". This is the leakage audit's single most
load-bearing ablation, because it is where the paid-persistence claim (N1) and the
shared-source claim (N2) meet: if the recurrence is a free permanence channel, W's
maintenance is theatre.

---

## 5. The per-arm pathway trace (the card's "TRACE every route")

The table states, per arm, each pathway's **possession**, **grade**, and **expected
decode**. Grades: I = inert, D = disclosed (quantified, not gated), L = leak (falsifies
the candidate). Cells marked "—" are absent. All decode rates are measured, none are
assumed.

| Arm | L1 h_t | L2 priv. state | L3 E,d,s | L4 trainer | L5 timing | L6 action hist | L7 history |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **CANDIDATE (SLW)** | D — richer than W; severed from specialists (sever=byte-id), F1 must be chance | I — stateless readouts; weight-bypass (I2) must be chance | I — A z-blind on (s,E,d); decode=chance | I — no forward z; loss factors through W; I2→chance | I — t z-blind; no cross-consumer τ edge | I — no output-recurrence | I — no buffer; sever-history=byte-id |
| **R1 private-state** | D — three h_i, severed | D — three W_i, each decodes ≈ W ceiling (its reduction) | I — three π_i, A z-blind | I — same as candidate | I — no cross-consumer τ | I — stateless | I — no buffer |
| **R4 suff-stat broadcast** | — (no encoder) | I — heads; I2→chance | — (free register, no π) | I — heads graded by z; I2→chance | I | I | I |
| **R5 separate copies** | — | I — heads | — | I | I | I | I |
| **R2 monolithic RNN** | D — h_t *is* the state; quantified ≈ W ceiling (its reduction) | D — heads jointly read h_t; no separate private state to cut | — (no π, no E/d) | I — no forward z | I — t z-blind; heads jointly computed | D — h_t integrates past inputs (L1, not L6) | D — history via h_t (no separate buffer) |
| **R3 history-access** | — (no encoder) | D — three readers | — | I | I | I | D — full history, decodes ≥ W ceiling (its reduction) |

**Reading the table.** In the **candidate**, every pathway is I except L1, which is D —
disclosed acquisition machinery held to the two non-negotiable constraints (severed
from specialists; z-blind under π-cut). A single L anywhere in the candidate row is a
falsification. In the **rivals**, the D cells are their *declared* reductions, and the
audit's obligation is to **quantify** them (the D cells' decode rates are the rival's
measured information advantage), never to treat them as leaks. The one cross-cutting
invariant: **no arm has an L cell** — an L in any arm is a wiring defect to fix, because
the comparability contract (G4 §8) already discloses every asymmetry; a hidden channel
would be an undisclosed unfairness, not a result.

---

## 6. Pre-declared gates (consistency checks G10 must assert)

Each gate is pre-declared and none may be amended after seeing results (AC16/17
discipline). Gate shape matches claim shape: categorical "no leak" claims gate on
per-individual dominance / a threshold met by every seed, never a mean margin (AC16);
equivalence claims gate on exact/byte equality, never "similar" (P7).

1. **Probe-inertness of every candidate pathway except W.** On the finals family, in the
   probe, decode z from each of L2 (weights, via I2-output), L3, L4 (via I2-output),
   L5a (t), L6, L7: **every** decode accuracy ≤ 0.500 + ε on **every** seed. L1 is the
   sole exception and is held to gates 2 and 3, not this one.
2. **Sever-byte-identity (availability).** Cutting L1 (h_t) — and any L5/L6/L7 edge the
   wiring checks surface — from every specialist leaves all outputs byte-identical to the
   intact run, on every seed. Any nonzero change is a wiring defect (a specialist reads a
   non-W pathway), not a finding.
3. **Free-recurrence (F1, persistence).** With π cut and the recurrence run with W
   zeroed, decode z from h_t at the probe ≤ 0.500 + ε on every seed. A h_t that retains z
   is a free hidden memory — MAINTAINED is falsified.
4. **Weight-bypass (trainer-signal isolation).** With W scrambled (I2) at the probe, every
   specialist's output decode ≤ 0.500 + ε on every seed. Any specialist above chance has
   a z-pathway through its weights/context — CAUSAL and AVAILABLE are falsified for it.
5. **Rival-pathway quantification (the rivals must be real).** R3's history decodes ≥ the
   candidate's W-ceiling accuracy; R2's h_t and R1's three W_i decode ≈ the W ceiling
   (each W_i within the training-noise floor of the others); R4/R5's S_t decodes at the
   ceiling. A rival whose declared pathway under-performs is a confound to fix, not a
   win to report.
6. **Decode-ablation sanity.** For each pathway probe, zeroing P drops the decoder to
   chance (0.500 ± ε) — the instrument measures what it claims (AC85).
7. **Byte-identity at the intact boundary (P7).** Every ablation is paired with its
   uninterrupted control on the same seed; the control must reproduce the frozen
   no-intervention run byte-for-byte before any difference is attributed to the cut
   (AC83's method).

The rival-family sweep (P6 rule 2) binds here: the decoder capacity and the ε resolution
are swept as level families alongside the arms' hyperparameters, never fixed while
selecting another's best member (AC11's fatal error).

---

## 7. Endpoints and seed discipline

- **Endpoints, recorded per seed, per arm, per pathway (planned-denominator, never
  pooled):** the marginal decode `acc(z|P)`, the conditional decode `acc(z|W,P)` and
  `Δ(P|W)`, the probe vs accumulation split, the leak-grade verdict (I/D/L), and the
  ε-resolution flag. The three anchors (§2.2) ride every table. Chronological scalars
  (first tick a severed pathway changes an output, first tick h_t retains z under
  π-cut) are recorded where they carry the mechanism.
- **The two decode regimes.** The **probe** is the load-bearing contrast (W is the only
  carrier; any free pathway above chance is a leak). The **accumulation** regime is the
  companion that bounds the disclosed x_t contribution at the memoryless 0.606 level and
  pins content-tracking. Both are reported; only the probe gates.
- **Seeds.** Disjoint engineering and finals families for the *arms*; disjoint again for
  the *decoder* (§2.4). Engineering seeds are excluded from every final sample; families
  are never mixed (AC39). The replication unit is the episode seed (one draw of z and
  its token stream).
- **No saturation.** The probe's graded gap (0.500 → 0.812, G2 §2.3) leaves room for a
  leak's magnitude to be graded rather than binary (AC47); the leak verdict is a rate
  with a magnitude, never a bare "leak present/absent."

---

## 8. Claim ceiling and what this does NOT claim

- **What a pass earns, at most.** That, in the candidate, **W is the unique paid,
  shared z-pathway to the specialists** — every other pathway is either inert (decodes
  at chance in the probe), disclosed acquisition machinery held to the sever and
  free-recurrence constraints, or a disclosed rival advantage whose magnitude is
  measured — at the stated degree. Nothing stronger.
- **The audit is a necessary condition, not a sufficient one.** Proving no *free* leak
  does not by itself prove W is *causally* load-bearing (G5's I1–I5 own that) or that
  sharing *buys* anything (G6's COORD and G7's novel-consumer own that). The leakage
  audit's contribution is the negative half: the causal and coordination claims are
  only sound if no rival pathway silently does W's job for free.
- **"Equivalent information" is the bar, and it is graded.** A weak leak (0.53) is
  reported as a weak leak, not re-labelled inert; a full-equivalence leak (≈ W ceiling)
  falsifies outright. The audit never hides a partial leak behind a binary pass.
- **Not claimed:** that the rival pathways are *unfair* (they are disclosed by design,
  G4 §8 rule 4 — the audit quantifies them, it does not condemn them); that a trained
  decoder's ceiling equals a real consumer's achievable use of a pathway (the decoder is
  an instrument with a capacity cap, and the sever test — not the decode — is what
  proves availability); any trained outcome (this is a spec, run by G10); any
  consciousness, autopoiesis, or level-(d)/(e) claim. This is a level-(b)/(c) audit
  design.

---

## 9. Provenance

Instantiates the leakage question over the six arms of `PHASE3_ARCHITECTURES_v1.md`
(G4 — candidate SLW + R1–R5, §8 comparability contract, §10 "G8 = decoding-of-z audit
across every pathway per arm"), the three specialists of
`PHASE3_SPECIALISTS_v1.md` (G3 — S_pol sign / S_plan SPRT / S_reg even-gate, §6 gate 5
sever-history), and the task of `PHASE3_INFERENCE_TASK_v1.md` (G2 — the scalar-LRR
sufficient statistic §2.1, the b-bit quantization §4.2, the probe §1.3, the anchors
§2.3). The conditional-independence reading of the sufficient statistic is G1's
AVAILABLE criterion (`SHARED_CONTENT_DEFINITION_v1.md` §2.4) restated as a decodability
audit. The interventions re-purposed as leak detectors are `PHASE3_CAUSAL_PLAN_v1.md`
(G5 — I2 W-cut, §3 surgical discipline, §5/§7 byte-identity); the free-recurrence test
is `PHASE3_BASELINE_v1.md` (G0 §3.7, the N12 F1 correction) and
`BRIDGE_PHASE2_VERDICT_v1.md` (finding F1). The maintenance-z-blindness invariant is
verdict D (`BRIDGE_PHASE2_VERDICT_v1.md`, G0 §3.3). The observer/scaffold discipline of
§2.1 is the organism line's labelled-oracle rule; the gate-shape and rival-sweep
discipline is `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (P6, P7, D1–D8). Organism study
references read from the skill's `references/` dir where named (`ac11`/`ac16`/`ac17` —
gate shape matched to claim shape; `ac38` — the exact sign test; `ac39`/`ac68` — seed
discipline; `ac47` — graded vs saturated; `ac83`/`ac85` — byte-identity license and the
silently-wrong wiring failure mode; `ac109` — causal claim where the content is the only
carrier).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is
a leakage-audit design, not a result.

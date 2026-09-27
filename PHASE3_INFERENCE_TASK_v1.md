# Phase-III inference task v1 — a genuine hidden-state inference task, with its sufficient statistic named

2026-09-26. Deliverable for the G2 card (t_e2cceac5): *what is the T1 component — a
task where the latent cause is not directly available, the current observation is
insufficient, and evidence arrives over multiple steps?* Category B/F — **design /
formalization; do not execute.**

This is a **derived document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It instantiates the task-specific parts
of the generative model that `SHARED_CONTENT_DEFINITION_v1.md` (G1) fixed the vocabulary
of, and it names the analytic sufficient statistic that G4's "sufficient-statistic
broadcast" rival (R4) will instantiate. It does **not** design the specialists (G3) or
the architecture alternatives (G4); it fixes the *inference problem* those cards build
on.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary
(`DEFINITIONS_CHARTER_v1.md` §2) is absolute: nothing here is a consciousness claim.
(2) Seeds are the replication unit (an episode seed = one independent draw of the latent
cause and its token stream); discrimination is a planned-denominator accuracy, reported
per seed family, never as a per-family guarantee (AC39/AC68). (3) The AC109/AC116
cautions are the design constraint, taken at face value: *storage is inert where the
current observation is decisive*, so this task is built so the current observation is
**not** decisive (AC109 rule 1; the T1 mapping note in `ACI_PHASE2_BENCHMARKS_v1.md`
§3.1). (4) The rival discipline of §4 is the point of the card: the analytic sufficient
statistic is **kept as the rival**, not defeated by a richer representation (D2, P5).

---

## 0. The one-paragraph answer

The T1 component is a **probabilistic evidence-accumulation task with heterogeneous
evidence strength**: each episode hides a binary cause z ∈ {A, B} (never shown), emits a
stream of "evidence tokens" whose per-token informativeness *varies* (strong, weak, or
neutral), and asks — after a final **ambiguous probe window** in which the observation is
made identical across the two causes — for a decision ẑ. The **minimal sufficient
statistic** for z given the token history is a **scalar log-likelihood ratio** — a running
sum of per-token weights, equivalently a **weighted integer counter** over two signed
counts — and nothing richer: a finite-state filter is over-parameterized for a *fixed*
cause and is therefore **not** required. Because the single strongest observation reaches
only a 0.881 posterior while the history accumulates to a ~0.81 decision accuracy that a
memoryless policy cannot reach (it is pinned at 0.606 in the clean condition and 0.500 in
the probe), the belief is genuinely a summary of the *history*, held in the maintained
variable W. The analytic scalar accumulator is **kept as the rival** (G4's R4): the
candidate differs from it only in *learned-vs-fixed* update and *shared-maintained-vs-free
broadcast* — never in representational capacity.

---

## 1. The generative model (concrete instantiation)

This pins the task-specific parts of G1's §1. Everything else (the representation W, the
consumers, the maintenance π) is G1's and G3's vocabulary; here only the cause, the
observation likelihood, and the probe structure are fixed.

### 1.1 Latent cause

- z ∈ Z = {A, B}, |Z| = 2 (the minimal case G1 allows; D8 supplies the taxonomy).
- One z per episode, drawn **uniform** (π_A = π_B = ½), and **never emitted** as an
  observation. The cause label is a training-only scaffold (a disclosed supervised/ELBO
  target used offline, exactly as `ACI_PHASE2_BENCHMARKS_v1.md` §3.1 specifies); at
  evaluation the only signal is the token stream and the decision reward. This satisfies
  "no hidden cause label at evaluation" by construction.

### 1.2 Observation stream

- Each step t = 1..H emits one token x_t from a 5-symbol alphabet
  Ω = {t1, t2, t3, t4, t5}. The two causes differ in the token distribution; the
  distributions are mirror images of each other, so the per-token log-likelihood ratios
  are symmetric and take **three magnitudes** (strong, weak, zero):

  | token | name | λ(x) = log P(x|A)/P(x|B) | P(x|A) | P(x|B) |
  | --- | --- | --- | --- | --- |
  | t1 | strong-A | **+2.00** | 0.1500 | 0.0203 |
  | t2 | weak-A | **+0.35** | 0.2800 | 0.1973 |
  | t3 | neutral | **0.00** | 0.3524 | 0.3524 |
  | t4 | weak-B | −0.35 | 0.1973 | 0.2800 |
  | t5 | strong-B | −2.00 | 0.0203 | 0.1500 |

  "Evidence strength varies" is built in here: a strong token moves the log-odds by ±2.0
  nats, a weak token by ±0.35, a neutral token by 0. The strong:weak odds ratio is
  e^2/e^0.35 ≈ 7.39/1.42 ≈ 5.2×. The probabilities are self-consistent (each row sums to
  1; the two columns are the mirror), and the λ values are exact by construction
  (λ(t1) = log(0.15/0.0203) = 2.00, λ(t2) = log(0.28/0.1973) = 0.35).

### 1.3 The probe window (the "current observation is insufficient" contrast)

- Steps 1..(H−K) are the **accumulation phase**: tokens drawn i.i.d. from P(·|z) per
  §1.2.
- Steps (H−K+1)..H are the **probe window**: every token is the **neutral** token t3, so
  P(x_t | A) = P(x_t | B) **exactly** during the window. This is the T1 benchmark's
  "ambiguous condition" (the organism line's occluded-gate analogue, C2), and it makes
  the *current* observation literally uninformative: the answer must come from the
  maintained history W, not from the present.
- Defaults: H = 32, K = 8, so 24 informative steps. K is chosen ≥ the largest rival
  observation window the design must defeat (§3.3).

### 1.4 Decision and reward

- At t = H the system emits ẑ ∈ {A, B}. Reward is the binary decision score
  r = +1 if ẑ = z, else 0. No confidence readout is *required* by the task's score; a
  graded confidence (the posterior / |S_H|) is available to G3's consumers and is why W
  is a graded scalar rather than a 1-bit latch (§4.2), but it does not enter the primary
  endpoint.
- This is a **discrimination** endpoint, not a survival endpoint: every episode completes
  the horizon, so planned-denominator accuracy is unambiguous (no termination bimodality
  to condition on).

---

## 2. The analytic sufficient statistic (derived BEFORE training)

This is the card's core obligation, stated before any training is imagined.

### 2.1 Derivation

Because z is fixed per episode and the tokens are conditionally i.i.d. given z, the joint
likelihood factorizes, and the posterior depends on the history **only** through the
running sum of per-token log-likelihood ratios:

```
S_t  =  Σ_{i=1..t} λ(x_i)                                          (1)

log [ P(A | x_1..x_t) / P(B | x_1..x_t) ]  =  S_t + log(π_A/π_B)   (2)
P(A | x_1..x_t)  =  σ( S_t + log(π_A/π_B) ),   σ(u) = 1/(1+e^{-u}) (3)
```

The **order** of tokens is irrelevant to the posterior (exchangeability of the i.i.d.
sequence); only the weighted multiset matters. Since λ(x) ∈ {+2.00, +0.35, 0, −0.35,
−2.00}, the running sum is exactly

```
S_t  =  2.00·(N_strongA − N_strongB)  +  0.35·(N_weakA − N_weakB)  (4)
```

i.e. a **weighted integer counter over two signed counts**. So the minimal sufficient
statistic is a **scalar**, in two equivalent guises:

- **scalar log-likelihood ratio** (real accumulator, Eq. 1), and
- **weighted integer counter** (Eq. 4), which is the same object on a 1-D lattice.

The Bayes-optimal decision rule (uniform prior, symmetric reward) is the posterior-odds
test:  ẑ = A  iff  S_H > 0. This is Wald's SPRT threshold at 0, and it is the optimal
discriminator.

### 2.2 What class it is — and what it is NOT

The card asks to determine which of three classes is sufficient and to **keep** it if it
is:

1. **Scalar log-likelihood ratio — sufficient.** Eq. 1 is a minimal sufficient statistic;
   no function of the history can improve on it for the decision.
2. **Integer counter — sufficient, and the same object.** Eq. 4 is the discrete
   realization (the increments are drawn from a finite set, so S_t lives on a lattice).
   It is not a *different* rival from (1); it is (1) restricted to its natural
   precision.
3. **Finite-state filter — NOT required.** A filter that carries a belief *vector* (more
   than one degree of freedom) would be needed only if z were time-varying (a Markov
   switching cause, or unknown transition dynamics), because then the posterior would
   not collapse to one scalar. For a **fixed** cause it is over-parameterized: it buys no
   information and only adds capacity (D1/D2). It is therefore **not** the rival; it is
   the explicitly-excluded richer representation (§5).

**Consequence for the rival (G4's R4).** The analytic rival is the **scalar
accumulator** — a fixed, algorithmic update `S ← S + λ(x_t)` with the threshold decision,
computed and broadcast for free. The candidate differs from it in exactly two respects,
never in capacity: (i) the update weights are *learned* rather than fixed to the supplied
λ's; (ii) the value is held in the *shared, paid-maintained* W rather than a free
register. Keeping the scalar rival is the honest answer to the card's question — the
experiment is **not** "neural nets beat Bayes on a toy"; it is "does inferred content,
held in one paid-maintained variable and consumed by two objective-distinct modules, do
causal work that the free algorithmic scalar does not organize."

### 2.3 The discrimination arithmetic (what the numbers buy)

All quantities derived from the §1.2 model (per-token λ's and probabilities):

- **Per-step evidence rate** (expected log-odds drift under the true cause):
  D_KL(P_A ‖ P_B) = Σ_x P(x|A) λ(x) = **0.288 nats/step**.
- **Per-step dispersion** of λ: sd = **0.810 nats**; per-step signal-to-noise = 0.356.
- **Single strongest observation** reaches posterior σ(2.00) = **0.881** — below the
  0.95 reference. No single observation determines z.
- **Mean informative steps** to accumulate +3.0 log-odds (0.953 posterior) ≈ **10.4**;
  to +4.0 log-odds (0.982) ≈ 13.9. Discrimination is inherently multi-step.
- **Bayes-optimal (Chernoff) error** P_e(t) ≈ exp(−t·C) with Chernoff information
  C = **0.0695 nats/step**:

  | informative steps t | 4 | 8 | 12 | 16 | 24 | 32 |
  | --- | --- | --- | --- | --- | --- | --- |
  | Bayes-optimal accuracy 1 − P_e | 0.243 | 0.427 | 0.566 | 0.671 | **0.812** | 0.892 |

At the default H=32, K=8 (24 informative steps) the **Bayes ceiling is 0.812** — a graded
ceiling, deliberately **not** saturated at 1.0 (AC47's lesson: a saturated endpoint cannot
show a graded contribution). The numbers also carry the AC109 companion check: the
memoryless Bayes-optimal policy (decide from the current token alone) attains
Σ_x P(x)·σ(|λ(x)|) = **0.606** in the clean condition, so the current observation carries
real-but-insufficient information, and the gap 0.606 → 0.812 is exactly what the history
buys. In the probe window that gap collapses to nothing (see §3), which is what makes the
maintained belief the *only* discriminator there.

---

## 3. The identifiability contrast (why W, and why maintained W)

### 3.1 The probe makes the current observation non-decisive by construction

In the probe window every token is neutral (λ = 0), so P(x_t|A) = P(x_t|B) exactly and
the current observation carries **zero** information about z. A policy that conditions
only on the present observation is at **chance (0.500)** in the probe, no matter how
good its readout is — it is not ignorant, the information is genuinely absent from x_t
(`ACI_PHASE2_BENCHMARKS_v1.md` §3.1, "Non-ignorance"). This is the C2 occluded-gate
condition carried from the organism line, and it is what makes "maintained hidden-state
inference" identifiable rather than merely asserted.

### 3.2 The two decisive interventions (I1, I2)

- **I1 — cut π's refresh of W.** Hold W's value, the sensors, and the token stream
  fixed; halt only the paid refresh. W decays on timescale 1/δ, and decision accuracy
  decays toward the memoryless ceiling (0.606 clean / 0.500 probe) in step. This pins
  that W is *paid-maintained*, not freely recurrent (the N12 F1 correction: the control
  runs the recurrence **with W decayed**, not a no-recurrence policy).
- **I2 — scramble W only.** At the probe, overwrite W (hold the token stream and every
  consumer's other input fixed); the decision must flip toward chance. This pins that W
  is the *cause* of the discrimination (CAUSAL), not a bystander. In the probe the
  effect is total — with W scrambled and x_t neutral, nothing else carries z.

### 3.3 The rival that must fail, stated so it can

- **Memoryless / sufficient-statistic rival** (current observation only, optionally a
  bounded window of the last M tokens): at chance (0.500) in the probe whenever M ≤ K,
  because a window of identical neutral tokens is still identical. In the clean
  condition it reaches 0.606 — this is the AC109 bound: it *matches* W wherever the
  current observation is decisive, and it is that bound, not ignorance, that the
  persistence claim must clear in the probe.
- **Finite-state / direct-control rival** (hardwired observation→decision mapping, no
  recurrence): identical to the memoryless rival here; must also fail the probe.
- Both receive the identical token stream — no information is withheld from them. They
  fail because the discriminating information is distributed across the full history,
  not because anything was denied (the T1 benchmark's "non-ignorance" clause).

### 3.4 Sweep as level families

The ambiguity level and the rival's observation window are swept as **level families**
(P6 rule 2), never fixed: sweep K (probe length) and M (rival window) independently, and
sweep the strong:weak evidence split (the λ_hi/λ_lo ratio) to confirm the memoryless
bound tracks the single-token information while the maintained belief tracks the
accumulated information. The discriminator is the **gap** (accumulator accuracy −
memoryless accuracy) in the probe, not either accuracy alone.

---

## 4. The rival kept, and the capacity-matched rule

### 4.1 What "keep the scalar rival" means concretely

The analytic sufficient statistic (§2) is **kept** as G4's R4 (sufficient-statistic
broadcast): a fixed, algorithmic scalar accumulator `S ← S + λ(x_t)` held in an ordinary
register and broadcast to both consumers, with the threshold decision at S > 0. It is not
handicapped: it holds the *exact* sufficient statistic at full precision. It fails (if it
does) only on the organizational question — it is not paid-maintained and its content is
not *one shared maintained variable* that two modules read — never on inference quality.

### 4.2 How many bits of W — and why "don't enrich W" is still honored

- The sufficient statistic is a scalar; a **1-bit** W (sign of S) is the *lossy* MAP
  decision, not the sufficient statistic itself. Because evidence strength varies, the
  graded magnitude |S| is real content: it is the confidence a second specialist can use
  (G3's S_reg deciding how much the belief is worth preserving) and it is what the task
  exposes as a graded, non-saturated endpoint (§2.3).
- The candidate's W therefore holds the scalar **quantized to b bits** (default b = 5,
  covering S ∈ [−6, +6] at resolution ≈ 0.39, comfortably finer than λ_lo = 0.35), swept
  as a parameter. The **rival holds the same scalar at the same b bits**. The candidate
  is **not richer than the rival** — the two differ only in learned-vs-fixed update and
  shared-maintained-vs-broadcast, which are the *claims under test*, not capacity. This
  is the D2/P5 obligation applied: enlarging W beyond the sufficient statistic would be a
  pure capacity increase with no information gain, and is prohibited.

### 4.3 The update/persistence split (carries the baseline vocabulary)

W's **content** is set by the accumulation write (Eq. 1) each step — the acquisition/update
write, whose correctness rides the open evidence (D3). W's **persistence** between those
writes is paid through π (the N1 substrate, G0). The task exercises exactly the
baseline's W/π wiring: the accumulation write moves the content, π holds it against decay,
and cutting π (I1) is the persistence contrast. Nothing here re-litigates N1; it uses N1
as the substrate the inference sits on.

---

## 5. What would legitimately require a richer W (and is NOT in v1)

Two extensions would make the scalar sufficient statistic stop being sufficient — and each
is the honest, named boundary at which a richer W would earn its keep rather than be a
capacity bluff (D1/D2):

1. **Latent / heteroscedastic evidence strength.** If the strong:weak odds were
   themselves unobserved (an episode-level intensity I scaling the λ's), the posterior
   would need the **second moment** of the evidence — the sufficient statistic would
   become a 2-D pair (Σλ·counts, Σλ²·counts), and a scalar would no longer suffice.
2. **A time-varying (Markov) cause.** If z switched within an episode, the posterior
   would be a belief *state* over the two causes — a finite-state filter — not a scalar.
   This is the §2.2 excluded case, and it is the honest path to a vector W.

**v1 uses neither.** The evidence-strength variation is *per token* and *known* (the λ's
are supplied, D8), and the cause is fixed per episode. That keeps the sufficient
statistic a scalar, keeps the rival honest, and keeps the inference "not unnecessarily
complex" exactly as the card instructs. Any future version that adopts (1) or (2) must
re-derive the sufficient statistic first and carry the richer rival the same way this
document carries the scalar.

---

## 6. Parameters (concrete defaults, swept as level families)

| Parameter | Symbol | Default | Swept / note |
| --- | --- | --- | --- |
| Cause alphabet | Z | {A, B} | fixed (D8 supplies taxonomy) |
| Token alphabet | Ω | 5 tokens | fixed |
| Token log-likelihood ratios | λ | {+2.00, +0.35, 0, −0.35, −2.00} | strong:weak ratio swept |
| Token distributions | P(·\|A), P(·\|B) | §1.2 table | derived from λ; mirror |
| Prior | π_A | ½ | uniform |
| Horizon | H | 32 | swept |
| Probe window (neutral) | K | 8 | swept; ≥ rival window M |
| Rival observation window | M | swept 0..K | the bounded-window rival |
| W quantization | b | 5 bits | swept; rival at same b |
| Decision threshold | θ | 0 (posterior-odds) | symmetric reward |
| Reward | r | +1 / 0 | binary decision score |
| Seeds | — | disjoint families (eng/finals) | AC39: per-family, never mixed |

Derived anchors (from §2.3): per-step D_KL = 0.288 nats; single strong token posterior
0.881; memoryless ceiling 0.606 (clean) / 0.500 (probe); Bayes ceiling 0.812 at the
default 24 informative steps.

---

## 7. Claim ceiling and what this task does NOT claim

- **What a pass on this task earns, at most:** "the maintained belief W is a sufficient
  summary of the observation history, causally load-bearing for discrimination exactly
  where the current observation is insufficient" — N1 + the *content* half of N2, at the
  stated degree. The sharing half (two objective-distinct consumers reading the same W)
  is G3/G4's claim and is **not** what this task alone tests.
- **The question this task is for** is whether the inferred content becomes
  **organizationally shared** — not whether a learned W beats the analytic scalar at
  inference. The scalar is kept as a co-equal rival for exactly this reason (§4).
- **Not claimed:** "has a memory" (a behaviorist gloss); "is conscious of the world";
  endogenous allocation (T4's claim); second-order access to the belief (T6's claim);
  any claim crossing the level-(d)/(e) boundary. This is a level-(b)/(c)
  representational task.

---

## 8. Provenance

Instantiates the task-specific parts of the generative model fixed in
`SHARED_CONTENT_DEFINITION_v1.md` (G1 §1: latent cause, observations, representation,
consumers, maintenance), and reads the T1 specification from
`ACI_PHASE2_BENCHMARKS_v1.md` §3.1 (the ambiguous condition, the memoryless /
finite-state rivals, the AC109 companion check, the simplest-sufficient-policy note) and
its §9 trivial-policy table row for T1. The sufficient-statistic result ("scalar
counter") is named in `TBRIDGE_STATISTICAL_PLAN_v2.md` (N7) and
`ACI_BRIDGE_PROTOCOL_v4.md` (N8) as the honest successor to the inferred-integrity STOP.
The rival discipline is `ACI_ARCHITECTURAL_PRINCIPLES_v1.md` (P5, P6, D1, D2, D8); the
numeric anchors were computed from the §1.2 model (per-step D_KL 0.288, Chernoff C
0.0695, memoryless ceiling 0.606, Bayes ceiling 0.812). Organism study references read
from the skill's `references/` dir: `ac109` (storage inert where the observation is
decisive), `ac116` (the integer counter vs the tuned memoryless rival, at the resolution
floor), `ac39`/`ac68` (seed/bimodality discipline), `ac47` (graded vs saturated
endpoints).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is
a task design, not a result.

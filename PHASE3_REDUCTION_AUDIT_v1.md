# Phase-III reduction audit v1 — can the candidate be collapsed analytically?

2026-09-27. Deliverable for the G9 card (t_74c6981e): *can the proposed experiment be
collapsed analytically — is W just a scalar sufficient statistic, does literal sharing
buy anything, and could a multi-head RNN trivially implement the whole candidate?*
Category B/F — **design / formalization; do not execute.**

This is a **derived document**. It runs nothing, trains nothing, freezes nothing, and
edits no frozen artifact (runner, protocol, results dir, hash, or ledger). It is not
hashed into any study's `pre_run_snapshot.json`. It audits the six arms of
`PHASE3_ARCHITECTURES_v1.md` (G4), the three specialists of `PHASE3_SPECIALISTS_v1.md`
(G3), and the task of `PHASE3_INFERENCE_TASK_v1.md` (G2) against the eight reduction
questions the card poses. It does **not** define any endpoint or gate — those are
G5–G8's, read here; it decides, per question, whether the reduction collapses the
central concept, merely produces a strong rival, or is already defused by the design.
It is what G10 reads before choosing which contrasts to implement as load-bearing.

**Reading discipline applied throughout.** (1) The level-(d)/(e) boundary is absolute
(`DEFINITIONS_CHARTER_v1.md` §2): nothing here is a consciousness claim. (2) Seeds are
the replication unit; every claim is a planned-denominator readout reported per seed
family, never a per-family guarantee (AC39/AC68). (3) The card's standing bar binds
the whole document: **do not modify the task merely because a rival appears strong —
modify only if the central concept is UNIDENTIFIABLE; a simple rival winning is an
acceptable Phase-III result.** (4) A "reduction" is a *co-equal rival*, not a strawman:
each of R1–R5 removes exactly one organizational property and is swept alongside the
candidate (P6, AC11/AC116 rule 2), so a reduction that wins is a result, not a bug.

---

## 0. The one-paragraph answer

None of the eight reductions makes the central concept **unidentifiable**; several would
**falsify** it, and two reduce it to its thinnest surviving contrast. The central
concept is *one maintained, paid-persistent, b-bit-quantized, shared content variable,
consumed by objective-distinct modules, whose organizational properties — sharing,
maintenance, compression, modularity — are each causally load-bearing against a rival
that removes exactly one.* This is identifiable because every predicate has an
operational test and every rival removes one predicate (§4). The eight reductions sort
into three grades. **(A) Defused by design** — the scalar-sufficiency (Q1) is the
*floor*, not a collapse: the candidate is deliberately never richer than the analytic
scalar (D2/P5), so the experiment is about organization, never about inference
richness. **(B) Strong rival, concept intact** — independent per-specialist computation
(Q2 → R1), the monolithic policy (Q4/Q5 → R2), ordinary transfer (Q6 → R2-probe/R3),
and architectural labels (Q7) each name a real rival that *could win* and would then
falsify (not confuse) the claim. **(C) Thin but not unidentifiable** — literal sharing
(Q3 → R5) and paid persistence (Q8 → R2/R4) are the two predicates whose behavioral
discriminators are few and must not be dropped: SHARED's identity survives only through
G5's I4 (private-copy divergence) and I5 (global-vs-local error); MAINTAINED survives
only through G2's π-cut (I1) and G8's free-recurrence test (F1). The single-write test
and the sever tests are *source/wiring* assertions, not behavioral discriminators, and
cannot carry those two predicates alone. The one thing the audit hands G10 as a
**binding obligation** is: keep I4, I5, I1, and F1 as the load-bearing tests of the two
thinnest predicates, or SHARED and MAINTAINED become unidentifiable by construction.

---

## 1. The central concept, stated so "unidentifiable" has a referent

Before the eight questions, the audit fixes what the candidate *is*, because
"unidentifiable" is a predicate about that object.

The candidate (SLW) is the conjunction `H_share` of five predicates over one variable
and its consumers (G1 §3): **SHARED** (one storage location, one write point, one
refresh target read by all consumers), **CAUSAL** (intervening on W changes each
consumer), **FUNCTIONALLY DISTINCT** (three non-collapsing invariance classes),
**AVAILABLE** (W is a sufficient summary; consumers do not re-read the history), and
**MAINTAINED** (persistence is paid through π, not free recurrence). The five rivals
remove one predicate each: R1 removes SHARED, R4 removes *learned content + paid
persistence*, R5 removes *the sharing mechanism*, R2 removes *modularity*, R3 removes
*the compressed maintained W* (G4 §9). W itself is the b-bit quantized scalar
log-likelihood ratio (G2 §4.2), the minimal sufficient statistic for the fixed-cause
i.i.d. token task (G2 §2.1).

**Unidentifiable**, for this audit, means one of two failures: (i) some predicate has
**no behavioral discriminator** — its only test is a source/wiring assertion, so no
measurement could ever falsify it; or (ii) two predicates are **not separable** — no
rival isolates one without also removing the other, so a loss cannot be attributed to
the removed property (G4 §8 rule 1's own bar). A rival that *wins* — the candidate
loses on every endpoint — is **not** unidentifiability; it is a clean falsification,
and the card's bar says it is acceptable. The audit grades each question against (i)
and (ii), not against "is the rival strong."

---

## 2. The eight reduction questions, answered

Each answer states (a) the reduction's strongest form — the specific rival that
implements it, (b) what in the design already resists it, (c) the verdict, and (d) what
would flip the verdict to unidentifiable.

### 2.1 Q1 — Is W just a scalar sufficient statistic?

**Strongest form.** W is the scalar LLR, and the analytic rival R4 holds the *same*
scalar for free (G4 §4). So "W is a scalar" is not a hypothetical reduction — it is the
design's own floor.

**What resists it.** The candidate's claim was never about W's richness. It is the
five-predicate conjunction, each stated over a scalar and each a property a scalar can
have or lack: a 1-bit W that is the sufficient statistic two modules need is shared
content; a 128-bit W that is not causally shared is not (G1 §4.1, P5). The
scalar-sufficiency does the *useful* work of foreclosing any "the candidate is richer"
defense (D2), and it is what makes R4 the honest ceiling on inference — the candidate
must *match* R4, never exceed it (G4 §9).

**Verdict: defused by design, not a collapse.** The scalar is the substrate, and its
sufficiency is precisely what forces the experiment to be about organization (sharing,
maintenance, compression, modularity) rather than inference quality. Being a scalar
does not collapse any of the five predicates: a scalar can be scrambled (CAUSAL),
read by three different functions (DISTINCT), sufficient for the history (AVAILABLE),
and paid-maintained against decay (MAINTAINED).

**What would make it unidentifiable.** Nothing here. The only consequence of Q1 is a
*scope* fact: no candidate win that required "W richer than the analytic statistic" is
available. That is a correct floor, not a defect.

### 2.2 Q2 — Can every specialist compute it independently at negligible cost?

**Strongest form.** R1: three private encoders `enc_i → W_i`, each W_i converging on
the same sufficient statistic, differing only by training noise (G4 §3). The inference
*is* cheap — a 5-token LLR accumulator behind a small recurrent net — so independent
computation is not merely possible, it is the default.

**What resists it.** The candidate does not rest on amortized inference cost. Its
candidate-vs-R1 load-bearing contrasts are (a) **coordination** (G6 §5: three private
*correct* inferences drift independently and straddle thresholds, producing off-
manifold triples that a single shared W makes structurally impossible), (b) **single-
write identity** (G5 I1: one write reaches all three consumers in the candidate; three
writes in R1), and (c) **novel-consumer reuse** (G7 §5: a fourth consumer reads one W
vs R1's concat/piggyback/retrain, none of which is "reuse the one shared content with a
frozen core").

**Verdict: strong rival, concept intact.** R1 is the candidate's most honest rival and
is not a strawman; it is the *thing the claim is about*. A candidate win here must come
from coordination and identity, not from inference economics — and the audit states that
plainly, because G4 §8 rule 3 already runs R1 at full per-copy capacity to prevent an
unfairness-based win.

**What would make it unidentifiable.** If the coordination contrast were dropped (see
Q4 — COORD does not separate candidate from R1's shared/free cousins, but it *is* the
load-bearing candidate-vs-R1 contrast), the candidate-vs-R1 comparison would rest on
the single-write identity alone — a source assertion. That would push Q2 toward
unidentifiability, and is exactly why G6's COORD must stay.

### 2.3 Q3 — Does literal sharing buy anything?

**Strongest form.** R5: three free copies of the *same* analytic scalar, identical by
construction (G4 §5). This is the subtlest reduction because it targets SHARED's
identity criterion (G1 §2.1: same content ≠ shared content), and R5 **ties** the
candidate on two of the experiment's headline endpoints: coordination (G6 §5 — three
bit-identical deterministic copies cannot disagree, so R5 has incoherence rate 0 too)
and novel-consumer performance (G7 §5 — identical content reaches the same ceiling).

**What resists it.** Three behavioral discriminators, and only three, separate
candidate from R5: (a) **ongoing-update divergence** (G5 I4 — substitute a frozen
private copy for one consumer; it diverges from the live W exactly as W keeps
accumulating, so coordination rides the *identity* of the shared variable, not its
momentary value); (b) **global-vs-local error** (G5 I5 — one wrong W propagates
coherently to all three consumers in the candidate, locally to one in R5); (c) the
single-write-reaches-all identity (G5 I1, G7 gate 5). Of these, (a) and (b) are
behavioral; (c) is a source/wiring assertion.

**Verdict: thin, but not unidentifiable — the flag G10 must not drop.** Literal
sharing buys *identity* facts, and those facts are behavioral **only** through I4 and
I5. It does *not* buy coordination (R5 ties) and does *not* buy performance (R5 ties).
This is the weakest, most at-risk discrimination in the entire experiment, and the audit
flags it as such: if I4 and I5 do not resolve in the candidate's favor, "shared" reduces
to "content-equivalent," the identity criterion is inert, and the single-write test
becomes a wiring assertion with no behavioral consequence.

**What would make it unidentifiable.** Exactly that: if I4/I5 were dropped, SHARED
would have *no* behavioral discriminator (its only test would be the single-write
assertion), which is failure mode (i) of §1. The audit's binding handoff: **G10 must
implement I4 and I5 as the load-bearing SHARED tests**; the single-write test is a
necessary source check, never a sufficient behavioral proof.

### 2.4 Q4 — Is the coordination condition reducible to one monolithic policy?

**Strongest form.** R2: one RNN, three heads reading h_t jointly (G4 §6). The question
is whether a monolithic policy can trivially land on the shared-content manifold M.

**What resists it.** G6 §5 already says it can: R2's coherence is *empirical, not
structural* — nothing forces its three heads onto M, but nothing forbids them from
landing there either, and G6 gate 3 explicitly does **not** require R2 to be incoherent.
So COORD does *not* separate candidate from R2. What COORD does separate, cleanly, is
candidate (0 by theorem) from **R1** (measured > 0) — G6 §5's "load-bearing rival."
The candidate-vs-R2 modularity contrast lives elsewhere: the interventions (R2 has no W
to scramble/cut/stale — G5 I1/I2/I5 degenerate), the π-cut (R2 has no π — G2 §3.2
degenerate), and in-policy consumer addition (R2 must joint-retrain or bolt on a probe —
G7 §5).

**Verdict: the coordination condition by itself is NOT load-bearing against R2; it is
load-bearing against R1.** "Coordination is reducible to one monolithic policy" is
*therefore partially true* — and the design already knows it (G6 §5 states it, G6 §9
defer it to this audit). This does not make the concept unidentifiable; it correctly
relocates the modularity claim onto the intervention signatures and the paid-
persistence signature, which is where R2 actually lacks something.

**What would make it unidentifiable.** Only if one insisted the candidate's claim were
"only a modular architecture can be coherent" — which the design never claims. COORD is
a candidate-vs-R1 fact; it must not be silently promoted to a candidate-vs-R2 fact, or
the audit would be misreading it (the AC14-class arm-name error, at the level of the
predicate).

### 2.5 Q5 — Does a multi-head RNN trivially implement the candidate?

**Strongest form.** The multi-head RNN *is* R2, in its sharpest guise. It trivially
implements the candidate's **input-output function** (a universal recurrent
approximator over the same history), and does so *richer* (h_t ≥ b bits, no
quantization) and *cheaper* (no paid persistence) — G4 §6 states this is a strong rival
by construction.

**What resists it.** R2 does **not** implement four things, and they are exactly the
organizational properties: (a) the **b-bit quantized bottleneck** — W is the
quantization of S_H, so the candidate alone faces the "is the b-bit summary sufficient"
test (G2 §4.2); (b) **paid persistence** — the π/decay substrate, the N1 fact (G0
§3.6); (c) the **scramble-able content slot** — the referent of I1/I2/I5, which R2 has
no version of (G3 §5); (d) the **read-only separable specialists** — R2's heads are
jointly parameterized, so consumer-addition is joint-retraining (G7 §4.4).

**Verdict: the strongest reduction, and it would win on accuracy and coordination — an
acceptable result.** If the experiment's endpoints were inference accuracy and
coordination alone, R2 would match or beat the candidate, and the candidate would be
falsified. That is not a reason to modify the task (the card's bar). The concept
remains *identifiable* precisely because it is defined by the properties R2 lacks by
construction, and those properties are measured by the interventions (I1 π-cut, I2
W-scramble, I5 coherent error) and the paid-refresh economy. If *those* resolve in
R2's favor, "modular maintained W" is interpretive scaffolding — the concept is not
confused with R2, it is cleanly falsified.

**What would make it unidentifiable.** Nothing; this is the cleanest of the eight. R2
is a clean rival, and its winning is the honest negative result the phase exists to
admit.

### 2.6 Q6 — Is the novel-consumer test merely ordinary representation transfer?

**Strongest form.** The test's *instrument* — a capacity-capped readout on frozen
features — is ordinary transfer (it is the same instrument G8's decoder uses, G7 §1,
G8 §2.1). R2's external-probe sub-arm and R3's reader are ordinary transfer over h_t
and over M tokens respectively.

**What resists it.** G7 §9 answers this directly, and the audit restates it as binding:
the *claim* is not ordinary transfer, because (a) the reused variable is
**paid-maintained** — the new head reads a live W whose persistence π is still paying
for, so the reuse inherits the N1 substrate rather than a static snapshot (a bare probe
of any arm's content does not require maintenance); (b) the **six-arm control** makes
the organizational property the independent variable, so "reuse" is a *difference
across architectures*, not an absolute capability; (c) the **interference measure**
(old consumers byte-unchanged under consumer-addition) is a modularity fact no transfer
probe states.

**Verdict: not merely ordinary transfer as designed — but the resolution is fragile.**
The load-bearing risk is the collapse candidate: if R2-probe and R3-reader reach the
ceiling, then "reuse without retraining" is achievable from *any* frozen content, and
the test reduces to "a frozen representation is reusable" — ordinary transfer — and
would not establish that the *maintained shared b-bit W* specifically is the reusable
thing. G7 gate 6 (R2's probe sub-arm) is where this surfaces.

**What would make it unidentifiable.** Not unidentifiable — a rival winning here (R2
probe or R3 reader matching the candidate's zero-retrain + b-bit + single-write
combination) is an acceptable Phase-III result. The audit only requires that the claim
not be *stated* as if ordinary transfer were already ruled out; it is not, until the
contrast resolves.

### 2.7 Q7 — Are "different modules" only architectural labels?

**Strongest form.** R2 removes "modularity" and reads the three outputs off one h_t
(G4 §6). If the three specialists were merely differently-parameterized heads, they
would be labels; the reduction asks whether they are anything more.

**What resists it.** Two senses of "module" must be separated, and the design
separates them: (a) **different functions of W** — NOT a label: the three specialists
occupy three distinct invariance classes (odd / sign-and-magnitude / even, G3 §4),
which guarantee non-collapse *by construction* and are falsifiable by the differential-
scramble test (the two-linear-heads rival fails it outright, G3 §1, G3 gate 1); (b)
**separate modules** (read-only, gradient-barred, anatomically distinct) — this IS the
sense R2 challenges, and it is load-bearing only to the extent the interference (G7
§4.4) and intervention (G5 I1/I2/I5) contrasts resolve.

**Verdict: a label in part — the functional reading is real, the architectural reading
is the claim.** The distinctness of the *functions* is pinned by invariance classes and
is not a label. The *anatomical* separation is exactly what is under test, and R2 is
the rival that would show it to be scaffolding. The audit makes this fine-grained
distinction explicit so G10 neither over-claims (the functions are distinct) nor
under-claims (the separation is the open question).

**What would make it unidentifiable.** If the invariance classes were collapsed — e.g.
S_reg made sign-sensitive, or S_pol made magnitude-sensitive — then all three would be
odd-in-W and co-vary (the single-objective collapse, G1 §2.3-d, G3 §1), and
FUNCTIONALLY DISTINCT would lose its only discriminator. G3 gate 1 exists precisely to
prevent this; it must stay.

### 2.8 Q8 — Does paid persistence matter to the shared-content claim, or would a free
recurrent state do the same job?

**Strongest form.** R2 (free recurrence) and R4 (free register) both carry the content
with no paid π. The question is whether MAINTAINED — one of H_share's five conjuncts
(G1 §2.5) — is load-bearing or theatre.

**What resists it, and what does not.** The bridge verdict already resolved a piece:
paid persistence is a **substrate fact, not a learned-behavior fact**, and it is shared
by state-blind fixed schedules (N12 F2, `BRIDGE_PHASE2_VERDICT_v1.md`) — so it can
carry no "acquired" claim. Within H_share, MAINTAINED is *definitionally* one conjunct,
but its **load-bearing** role is narrow: paid persistence does **not** buy coordination
(R4/R5 are coherent for free), does **not** buy inference (R4 holds the exact scalar
for free), and does **not** buy the novel-consumer ceiling (R4 ties). Its only
behavioral roles are (a) the **π-cut decay signature** (G2 §3.2 I1 — the one place
paid-vs-free shows up as behavior) and (b) the **free-recurrence test** (G8 §4.4 F1 —
does the GRU secretly carry S_H past the cut; run the recurrence with W zeroed, N12
F1).

**Verdict: paid persistence is the weakest of the five predicates against R2/R4, and
its only tests are I1 and F1 — the audit says so plainly.** If the free-recurrent-state
reduction passes both, paid persistence is theatre and MAINTAINED should be dropped
from the conjunction — which would *not* make the concept unidentifiable (the claim
would shrink to the four non-maintained predicates, an acceptable falsification). But
paid persistence is not reducible *a priori*: it is the substrate N1 established, and
I1 + F1 are the two tests that keep it honest.

**What would make it unidentifiable.** If I1 (π-cut) or F1 (free-recurrence) were
dropped, MAINTAINED's only remaining test would be a wiring assertion about π — failure
mode (i) of §1. The audit's binding handoff: **keep I1 and F1** as the load-bearing
MAINTAINED tests, and do not let the sever test (a source check) stand in for them.

---

## 3. The verdict table

| Q | Reduction | Rival | Grade | Load-bearing contrast that keeps it identifiable |
| --- | --- | --- | --- | --- |
| 1 | W is a scalar sufficient statistic | R4 (same scalar) | **defused** (it is the floor) | none needed — scalar-sufficiency forces the organizational framing |
| 2 | each specialist computes it independently | R1 | **strong rival, concept intact** | COORD (G6), single-write (G5 I1), novel-consumer (G7) |
| 3 | literal sharing buys nothing | R5 | **thin, not unidentifiable** | G5 I4 (divergence) + I5 (global-vs-local error) — *must keep* |
| 4 | coordination reducible to one monolithic policy | R2 | **partially true** — COORD is candidate-vs-R1, not -vs-R2 | interventions + π-cut carry the modularity claim |
| 5 | multi-head RNN trivially implements the candidate | R2 | **strong rival, concept intact** | b-bit bottleneck, π, scramble-able W, separable specialists |
| 6 | novel-consumer test is ordinary transfer | R2-probe / R3 | **not as designed; fragile resolution** | six-arm control + maintenance + interference (G7 §9) |
| 7 | "different modules" are only labels | R2 | **label in part** — functions real, separation is the claim | invariance classes (G3 gate 1) + interference/intervention |
| 8 | free recurrent state does the same job | R2 / R4 | **weakest predicate, not reducible a priori** | G2 I1 (π-cut) + G8 F1 (free-recurrence) — *must keep* |

**Reading the table.** Two rows (Q3, Q8) carry "must keep" obligations because their
predicate's behavioral discriminators are few and the alternative is unidentifiability,
not falsification. The other six rows are strong rivals whose winning is a clean,
acceptable negative result.

---

## 4. The unidentifiability bar, applied (the card's instruction)

The card's instruction — modify only if the central concept is **unidentifiable** — is
answered here in the negative, with the two narrow caveats that would flip it:

1. **No reduction in §2 reaches the unidentifiability bar.** Each of R1–R5 removes
   exactly one predicate, and each predicate has at least one behavioral test (I1, I2,
   I3, I4, I5, the differential-scramble matrix, COORD, the novel-consumer four
   measures, the seven-pathway decode audit). A rival that wins on all of them is a
   **falsification**, not a confusion: the concept was identifiable, it simply failed.

2. **Two predicates are one dropped-test away from unidentifiable, and that is the
   audit's actionable finding.** SHARED's identity criterion (Q3) has behavioral
   discriminators only in I4 and I5; MAINTAINED (Q8) only in I1 and F1. In both cases
   the *source-level* tests (single-write, sever, π-present) are necessary wiring
   checks but **not** behavioral proofs. If G10 implements the experiment without these
   four interventions as load-bearing gates, it will have built a study in which two of
   the five conjuncts of H_share cannot be falsified by measurement — which is exactly
   the definition of unidentifiable this audit fixes in §1.

3. **A simple rival winning is the acceptable result, and the audit names where it is
   most likely.** R2 (Q5) is the most likely clean winner — it is richer and cheaper
   and would match the candidate on inference and coordination — and its winning would
   falsify "modular maintained W is load-bearing" without touching the identifiability
   of the concept. R5 (Q3) is the most likely *near*-winner — it ties on coordination
   and performance and loses only on I4/I5 — and there the honest result is the
   strongest form of "sharing is a label, not a mechanism" the design can admit.

---

## 5. What this audit does and does NOT do

- **Does:** grade each of the eight reductions against the unidentifiability bar;
  identify the two thin predicates and their four load-bearing tests (I4, I5, I1, F1);
  state which rivals are clean falsifiers vs near-winners; and hand G10 a binding list
  of which contrasts must be implemented as load-bearing.
- **Does not:** define or re-number any endpoint, gate, or intervention (G5–G8 own
  those, and G5 §1's canonical I1–I5 numbering is binding); choose training objectives
  or seeds (G10's); re-open the demotions (V absent, A fixed/reactive, S_reg a
  readout — verdict B+D, binding); or alter the task because a rival is strong.
- **Standing rule the audit enforces on itself.** Every claim of "the candidate beats
  R" below is read as "beats R on R's own removed predicate, with R's parameter family
  swept alongside the candidate's" (P6 rule 2, AC11/AC116) — the audit does not grant
  the candidate any information or capacity advantage over any rival (G4 §8 rules 3–4).

---

## 6. Claim ceiling

This is an **audit of the design's identifiability**, not a result about the candidate.
It claims, at most: **the candidate is identifiable** — every predicate of H_share has
an operational test and every reduction rival removes exactly one predicate — **and
two predicates (SHARED's identity, MAINTAINED) survive only through four named
behavioral tests (I4, I5, I1, F1) that G10 must keep load-bearing.** It claims nothing
about whether the candidate *wins*; the audit's whole point is that a clean loss to R2
or R5 is an admissible, even likely, Phase-III outcome. No autopoiesis claim and no
consciousness claim is made anywhere. This is a level-(b)/(c) design audit.

---

## 7. Provenance

Audits the six arms of `PHASE3_ARCHITECTURES_v1.md` (G4 — candidate SLW + R1–R5, §8
comparability contract, §9 per-rival gate shapes) against the eight reduction questions,
reading the task from `PHASE3_INFERENCE_TASK_v1.md` (G2 — the scalar-LRR sufficient
statistic §2.1, the b-bit quantization §4.2, the probe §1.3), the specialists from
`PHASE3_SPECIALISTS_v1.md` (G3 — the three invariance classes §4, the anti-collapse
gate §6.1), the shared-content predicate from `SHARED_CONTENT_DEFINITION_v1.md` (G1 §2 —
the five criteria, the identity-vs-value distinction §2.1), the causal interventions
from `PHASE3_CAUSAL_PLAN_v1.md` (G5 — I1–I5, the canonical renumbering §1, the
single-write and coherence tests §10), the coordination condition from
`PHASE3_COORDINATION_v1.md` (G6 — COORD §2, the per-arm table §5), the novel-consumer
answer to Q6 from `PHASE3_NOVEL_CONSUMER_v1.md` (G7 §9, and §5's R1 wiring resolution),
the leakage/persistence facts for Q1/Q2/Q5/Q8 from `PHASE3_LEAKAGE_AUDIT_v1.md` (G8 —
the seven pathways §3, the F1 free-recurrence ablation §4.4), and the baseline demotions
from `PHASE3_BASELINE_v1.md` (G0 §3). The N2 framing and the "substrate fact, not
learned-behavior fact" status of N1 are `ACI_MASTER_RESEARCH_TREE_v2.md` §5 and
`BRIDGE_PHASE2_VERDICT_v1.md` (verdict B+D, findings F1/F2). Organism study references
read from the skill's `references/` dir where named (`ac11`/`ac16`/`ac17` — gate shape
matched to claim shape, never move a threshold post-hoc; `ac14` — an arm name must
match the arm cut; `ac38` — the exact sign test; `ac39`/`ac68` — seed/bimodality
discipline; `ac47` — graded vs saturated endpoints; `ac83`/`ac85` — byte-identity
license and the silently-wrong-wiring failure mode; `ac109`/`ac110` — causal claim where
the content is the only carrier, correctness rides content; `ac116` — the integer
counter vs the tuned memoryless rival).

No autopoiesis claim and no consciousness claim is made anywhere in this document. It is
a reduction audit, not a result.

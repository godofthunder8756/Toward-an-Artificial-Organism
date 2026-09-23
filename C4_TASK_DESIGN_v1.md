# C4 task design v1 — first-order uncertainty estimation is discriminating in the incomplete-evidence regime

2026-09-23. **Design document, not a study.** No organism-scale run, no seeds, no
protocol freeze. This is C4's deliverable (task `t_d06a5e21`): the design of a task with
incomplete/noisy evidence for the two causes, an explicit **first-order uncertainty
estimate** (a graded posterior over the cause), the ordinary heuristics it must beat, and
a **decision-theoretic demonstration** (`_c4_uncertainty_probe.py`, run; output in §9)
that the estimate is calibrated and improves decisions. It does **not** test the
**reliability** tier — that is a distinct monitor, deferred by the card's own ordering
("test first-order estimation and ordinary heuristics **before** any reliability monitor")
and specified here only through the content/reliability separation in §11.

---

## 1. The question

In a task with overlapping / noisy / delayed / incomplete evidence for the two causes, does
**uncertainty estimation (first-order)** support useful decisions — beyond ordinary
uncertainty heuristics that read the same information?

The card's answer requirement: first-order estimation and heuristics first, a reliability
monitor second; and the three named constraints — (i) do **not** require each individual
error to be predictable (reliability may concern *calibrated error rates across
distinguishable conditions*); (ii) do **not** call a confidence variable "metacognition" by
definition; (iii) do **not** justify broadening the task merely because the previous task
was easy.

---

## 2. Where this sits

The task is the **C2 occluded-`used_held` gate** (`C2_TASK_DESIGN_v1.md`): the two AC107/108
causes (E_world *move* vs E_machinery *cut*, identical immediate failure) are occluded on the
one bit that separates their unproductive signatures, so at an occluded contact the two causes
produce an **identical current observation** `(bound=1, used_held=occluded, productive=0)`
while the correct action differs (move → relinquish; cut → hold). C2 handed C4 exactly this
overlap, with `q` (the occlusion probability) as the noise knob.

Three prior results constrain what this design may and may not assume:

- **K8 (`K8_DISPOSITION_v1.md`)** blocked the reliability tier because the AC107 estimate was
  ceiling-accurate (0 mistakes) — no error variance for a second-order state to predict. The
  reopening condition (1) was "relax perfect identifiability (overlapping histories)", which
  C2 supplied. C4 is the first place the resulting **error variance** is actually present.
- **C1 (`ac109.py`)** measured the AC107 stored **bit** to be inert where the discriminator is a
  pure function of the current observation (disjoint histories). C4's graded estimate is a
  different object: a **probability**, not a bit, and it earns its keep exactly where the
  current observation is **not** decisive.
- **C3 (`AC110_RESULTS_v1.md`)** measured ongoing **repair** to be non-load-bearing (correctness
  rides reacquisition). C4 is orthogonal: it changes the **estimate's content granularity**
  (bit → graded), not its maintenance.

Nothing here re-runs or re-hashes AC107/108/110 or their frozen results.

---

## 3. The task

Hold-and-observe probe (C2 §4): the organism withholds relinquishment and contacts channel 1.
Per contact it observes the triple `(used_held, productive, bound)`, with `used_held` now
three-valued (`held` / `blind` / `occluded`) — the C2 interface change, applied uniformly to
every arm, i.i.d. Bernoulli(`q`), not synchronized with the cause onset at `t=8192`.

The two causes and their observation process:

| cause | used_held (when open) | productive | interpretation |
|---|---|---|---|
| **M** (move) | `held` | always 0 | stale held entry fails deterministically |
| **C** (cut) | `blind` | Bernoulli(1/4) | read suppressed; blind fallback yields 1/4 |

The gate occludes `used_held` with probability `q`. The **likelihood structure** of the
observations (the whole design hinges on this):

| observation | possible under | log-likelihood-ratio toward M |
|---|---|---|
| open `held`, unproductive | M only | `+∞` (decisive M) |
| open `blind` (any productive) | C only | `−∞` (decisive C) |
| occluded, productive | C only (M never yields) | `−∞` (decisive C) |
| occluded, unproductive | both | `log(q·1 / (q·3/4)) = log(4/3) ≈ +0.288` (weak M) |

The decision is **relinquish** (act on "route is stale") vs **hold** (act on "route is valid").
Cost asymmetry (the AC107 economics, and the reason uncertainty has a decision to influence):

- hold under M: **+1 per contact** (sustained lost income, never re-acquires);
- relinquish under M: 0 (correct; loss ends);
- hold under C: 0 (correct);
- relinquish under C: **+R** (drop a valid entry; one-time re-bind cost, recoverable).

The task's evidence is **incomplete** (`used_held` intermittently hidden) and **noisy** (the
residual `productive` signal is weak: blind fallback fails 3/4 of the time, so an unproductive
contact is only *weak* evidence for M). It is also **delayed** in the accumulation sense: the
weak evidence must be summed over several contacts to cross a decision threshold.

---

## 4. The first-order uncertainty estimate (the design's object)

The object under test is a **graded posterior over the cause**,

    p = P(cause = M | history) ∈ [0, 1],

maintained in log-odds `L = log(p / (1−p))`, updated per contact by the likelihood ratios in §3:

    open held            -> L = +inf      (relinquish immediately)
    open blind           -> L = -inf      (hold)
    occluded, productive -> L = -inf      (hold)
    occluded, unproductive -> L += log(4/3)

and consumed by a **threshold decision**: relinquish when `p >= θ` (equivalently `L >=
logit(θ)`). This is "first-order" in the card's sense — it is uncertainty about the **content**
(which cause), expressed as a graded quantity rather than a crisp bit — and it is **not** a
metacognitive or reliability state: it says nothing about the *estimator's own error rate*, only
about the *cause*. It is a probability, not a confidence-about-confidence.

The graded posterior is the natural object C4 asks for: at an occluded unproductive contact the
organism cannot read `used_held`, but it **can** still update a probability (the productive
signal is weak-but-real evidence), and that probability is what tells it whether to keep
deferring (hold and gather more evidence) or act (relinquish). This is the "defer vs act under
incomplete evidence" structure the C2 handoff named (C2 rule 4: C4 is the *wait-and-see* task,
not the memory task).

---

## 5. Why uncertainty is meaningful here and can influence a useful decision

Uncertainty is meaningful precisely because the two causes are **non-separable on the current
observation** at occluded contacts: no single tuple names the cause, so the organism must carry
a **graded** belief across contacts rather than a crisp one. And it can influence a **useful**
decision because the two errors are **asymmetric**:

- relinquishing under C costs R (one-time, recoverable);
- holding under M costs 1 *per contact, forever* (sustained).

The optimal policy therefore must **trade off** "how fast I relinquish under M" against "how
often I wrongly relinquish under C", and that tradeoff is exactly what the posterior's
threshold `θ` controls. A confidence that is too coarse (a bit) cannot sit on this tradeoff:
it must either always relinquish on any unproductive contact (fast under M, wrong under C) or
wait for a decisive observation (right under C, slow under M). The graded posterior sits in
between, and it is the only object that can weight the *weak* occluded evidence against the
*decisive* open evidence correctly.

---

## 6. Available evidence vs what remains hidden

**Available (to every arm, by the C2 interface):** `bound` (own introspection: does memory hold
a live entry), `used_held ∈ {held, blind, occluded}`, `productive`. These are the organism's
own retrieval result and introspection; the gate is applied uniformly, with no privileged read.

**Hidden:** the cause label (move vs cut) is never supplied to any arm; the gate reveals nothing
about the cause, it only withholds one bit; the gate is i.i.d. and not synchronized with the
cause onset (no schedule access). The design therefore satisfies C2's three anti-confound
properties (no hidden label, no schedule access, no privileged read) unchanged.

---

## 7. The estimates / predictions to evaluate

Four measures, all specified against the observation process before any organism-scale run:

- **Accuracy** — does the estimate name the cause at decision time? For the graded posterior,
  the natural reading is the posterior mass on the true cause at the moment of acting (and,
  for the binary rivals, the AC107 `mistakes` count).
- **Calibration** — does the reported confidence track the empirical error rate? A
  well-calibrated estimate relinquishes with confidence `p` and is correct with frequency ≈ `p`
  across the population of decisions. This is the "predicts errors" half of the card's support.
- **Decision utility** — expected regret (the §3 cost model) per policy, minimized over each
  policy's own parameter. This is the "improves decisions" half.
- **Information gathering** — how long the organism defers (how many evidence-gathering
  contacts it accumulates) before acting, as a function of the posterior; the defer/act
  boundary is the measurable signature of the estimate regulating its own evidence gathering.

---

## 8. Rivals (using the same information)

Four policies, all reading the **same** `(bound, used_held, productive)` interface:

1. **`raw`** — the frozen streak / r4 raw failure counter: relinquish after `N` consecutive
   unproductive contacts, no cause attribution, state-blind on `used_held`. The "simple
   history-based rival" (no attribution).
2. **`binary`** — the AC107 one-bit cause estimate: open blind → C (hold), open held-fail → M;
   under M relinquish after `N` unproductive (the frozen streak); under C hold. Attribution
   present, but the confidence is a **bit**.
3. **`binary+imm`** — `binary` **plus** "relinquish immediately on an open held-fail". This is
   the *strongest* ordinary heuristic: it closes the binary estimate's decisive-action gap, so
   the comparison is against the best heuristic, not a strawman.
4. **`graded`** — the first-order posterior of §4.

Each rival is minimized over its own parameter (`N` for 1–3, `θ` for 4); no arm is given a
weaker information set, and `binary+imm` exists specifically so a finding that "the graded
posterior beats the binary estimate" cannot be dismissed as "the binary estimate was missing an
obvious rule".

---

## 9. The discrimination result (probe, run)

`_c4_uncertainty_probe.py` simulates the §3 process and measures expected regret per policy
(Monte Carlo; `P_YIELD=1/4`, `R=4`, horizon `H=96`). Two facts fall out.

**(a) The graded posterior strictly dominates every heuristic on the speed/accuracy tradeoff.**
At each occlusion rate, sweeping each policy's parameter traces a frontier of `(regret_M,
regret_C)` pairs; the graded posterior's frontier lies at or below the `binary+imm` frontier
**at every point**, and the gap grows with `q`:

| q | binary+imm min-mean regret | graded min-mean regret | graded dominance (same M, lower C) |
|---|---|---|---|
| 0.5 | 0.485 | 0.480 | small (e.g. M≈0.50: C 0.665 → 0.551) |
| 0.7 | 0.995 | 0.884 | M≈0.70: C 1.49 → 1.11; M≈1.18: C 0.84 → 0.58; M≈1.53: C 0.46 → 0.31 |
| 0.9 | 1.744 | 1.359 | M≈0.90: C 2.93 → 1.85; M≈1.70: C 2.37 → 1.26; M≈2.43: C 1.85 → 0.86 |

`raw` is flat at ~2.0 (wrong under C everywhere); `binary` improves under C but is slow under M
and still wrongly relinquishes under C at high `q`. The graded posterior dominates `binary+imm`
**strictly** — it is not a re-labelled streak: at the same M-speed it always pays a lower
C-cost, because it weights the weak occluded evidence correctly (see §10).

**(b) The graded posterior is well-calibrated (it predicts errors).** At `q=0.5, θ=0.75`, the
mean confidence at the moment of acting is 0.985 under M and 0.760 under C, and the binned
empirical accuracy tracks the reported confidence: confidence in (0.7, 0.8] → 0.748 correct;
confidence in (0.9, 1.0] → 1.000 correct. The estimate's confidence is not a bare label — it is
a probability that matches the true error frequency.

**Boundary (the falsification direction, recorded honestly).** As `q → 0` the two causes are
fully separable on the current observation (the C1 world), the graded posterior and
`binary+imm` coincide (both read the decisive bit immediately), and **no uncertainty estimate
is needed**. The design's discrimination therefore lives in the **incomplete-evidence regime**
(`q` bounded away from 0), which is exactly the regime the card names. This is not a knife-edge:
the dominance is monotone in `q` and already ~0.13 in regret at `q=0.7`.

---

## 10. The mechanism (why the weighting is load-bearing)

The one quantity that separates the graded posterior from every heuristic is the **likelihood
ratio of the occluded-unproductive observation**: `log(4/3) ≈ 0.288`, not 1.

Under **C**, a contact is blind fallback — it fails 3/4 of the time, so an occluded unproductive
contact is *common* and *weak* evidence for M. A uniform counter (`raw`, `binary+imm`) treats it
as full-strength (`+1`) and therefore wrongly relinquishes the valid entry under a run of
ambiguous failures. The graded posterior treats it as weak (`+0.288`), so it requires several
ambiguous failures before acting — and the ~1/4 productive blind contacts (decisive for C) usually
arrive first and stop it. Under **M** every contact is unproductive, so the graded posterior's
slow drift is exactly compensated by the decisive open `held` observation (immediate relinquish):
it is *both* faster under M and safer under C than a uniform counter, which is the Pareto
dominance of §9.

In one line: **the graded posterior is discriminating because it weights heterogeneous evidence
by its likelihood ratio — decisive (open / productive) observations act immediately, weak
(occluded-unproductive) observations accumulate slowly — and no uniform counter can express
that split.**

---

## 11. Separating estimated CONTENT from estimated RELIABILITY

The design must let a future reliability study cut the two apart. The separation is read
directly off the likelihood structure (§3):

- **Content** = `P(cause | history)` with the likelihood model held fixed — the graded posterior
  of §4, which uses the *frozen* blind-fallback rate `P_YIELD = 1/4` (PORTS=4) to compute
  `log(4/3) = −log(1−P_YIELD)`.
- **Reliability** = the organism's estimate of the evidence channel's diagnostic value — i.e. its
  estimate of `P_YIELD` (or `q`), the quantity that sets *how much weight* each observation
  deserves.

The two are separated by two single-flag interventions (specified for the deferred reliability
study, not run here):

1. **Scramble content, keep reliability.** Force `P(cause|history)` to a fixed wrong value
   (e.g. always M, or always the prior), leaving the `P_YIELD` estimate intact. The decision
   degrades (wrong cause), while the reliability estimate — if separate — remains calibrated.
2. **Scramble reliability, keep content.** Force the `P_YIELD` estimate to a wrong fixed value
   (e.g. `P_YIELD=0.99` → treat every unproductive contact as near-decisive for M), leaving the
   posterior update intact. The cause estimate still *reads* the evidence, but weights it
   wrongly, and the decision degrades **only** in a world where `P_YIELD` genuinely varies
   across distinguishable conditions.

This maps exactly onto the card's constraint: reliability is **not** "predict each individual
error" — it is a **calibrated error rate across distinguishable conditions** (`P_YIELD`), and a
reliability state earns its keep only when that rate varies and must be estimated, not when it is
a frozen architectural constant. In *this* (first-order) design `P_YIELD` is fixed, so the
first-order posterior needs no reliability state; the reliability tier is a **separate, deferred**
question, reached only if `P_YIELD` is made to vary across conditions.

---

## 12. Theory connection and its limitations

**Primary mapping: HOT-2 — metacognitive monitoring** (Butlin et al. 2023, Table 1; the roadmap
§5's "metacognitive monitoring distinguishing reliable representations from noise"). The
first-order posterior is the graded counterpart of the roadmap's cause estimate: it grades *which*
failure mode the organism is in (world-changed vs own-machinery-impaired) as a probability rather
than a bit, and it is consumed to regulate a defer-vs-act decision — the monitor's graded
judgement about the organism's own first-order content (the route entry and its failure).

**Limitations, all explicit:**

- **Adaptation, flagged not hidden.** HOT-2's canonical domain is *perceptual* representations;
  the organism's content is interoceptive/route-level. The mapping is the roadmap's theory-specific
  extension, adopted as a modeling judgment (charter J5), contestable.
- **This is level-(c) representational design, not level-(d)/(e).** "First-order uncertainty is
  calibrated and improves decisions" earns "meets candidate indicator HOT-2 at degree Y" — never
  "metacognitive" or "conscious". The card's own constraint (ii) is honored: the graded posterior
  is a **probability**, not a confidence-about-confidence, and is not called metacognition by
  definition.
- **The decision utility is behavioral, not survival-level, in this probe.** Whether the regret
  reduction moves any survival endpoint is an implementing-study question, not a design premise
  (the card's "no survival advantage required").
- **The posterior's likelihood model uses a frozen constant** (`P_YIELD=1/4`). The design
  specifies *that* the organism could weight evidence this way, and demonstrates the weighting is
  decision-relevant; whether the organism can *store and maintain* a graded probability and its
  likelihood weights (vs. a scaffold supplying them) is the implementing study's question, and is
  deliberately not prejudged here (C2's own discipline: identifiability/utility is demonstrated
  *before* the organism-scale question is asked).

---

## 13. Claim discipline

- This is a **design + decision-theoretic demonstration**, not a study. No organism-scale run, no
  seeds, no freeze, no hashes. The probe's claims are about the **observation process and the
  decision problem**, not about any organism's behavior.
- The headline is: **"a graded first-order posterior over the cause is calibrated and strictly
  dominates ordinary uncertainty heuristics on the defer-vs-act tradeoff, with the dominance
  growing in the incomplete-evidence (high-`q`) regime."** It is *not* "the organism maintains
  uncertainty", *not* "reliability is load-bearing", *not* "metacognition".
- The falsification boundary is stated (§9): at `q → 0` (complete evidence) the estimate is
  unnecessary and heuristics match — which is the correct, non-vacuous control, not a weakness.

---

## 14. What this hands to S1 (and the conditional child)

**S1 (synthesis).** The uncertainty question is answered at the **first-order** tier: SUPPORT —
first-order uncertainty estimation is calibrated and improves decisions beyond same-information
heuristics, in the incomplete-evidence regime. The **reliability** tier remains **untested and
deferred**, and its test now has a concrete, named entry condition (from §11): make the evidence
channel's diagnostic value (`P_YIELD`) **vary across distinguishable conditions** and ask whether
an *estimated* `P_YIELD` (a second-order state) restores the discriminating weighting that a
*frozen* `P_YIELD` supplies here. That is the natural continuation, not this design.

**Conditional child (implementation).** If S1 authorizes it, the next step is an organism-scale
study (next identifier, **AC111+**) that (a) replaces the AC107 one-bit estimate with a graded
posterior held in vulnerable, paid-maintained state (the AC12/AC96 free-bit pattern extended to a
low-bit-width log-odds register), (b) implements the `binary+imm` rival as the sharpest
falsification arm, (c) runs in the high-`q` regime where the design discriminates, and (d) gates
on calibration and decision utility, not survival. That is a *conditional* child — spawned only
after the design is judged discriminating, which this document demonstrates at the
decision-theoretic level.

---

## Files

- design: `C4_TASK_DESIGN_v1.md` (this file)
- diagnostic (canonical): `_c4_uncertainty_probe.py` — observation process, four policies,
  regret sweep (§9a), per-cause breakdown, calibration (§9b). Run it: `.venv/bin/python
  _c4_uncertainty_probe.py`.
- diagnostic (Pareto): `_c4_uncertainty_pareto.py` — the speed/accuracy frontier comparison that
  produced §9's "graded dominance" column. Run it: `.venv/bin/python _c4_uncertainty_pareto.py`.
- superseded intermediate probes (kept for the record): `_c4_uncertainty_probe2.py`,
  `_c4_uncertainty_probe3.py`, `_c4_uncertainty_probe4.py`.
- No frozen artifact, runner, protocol, or hash was edited, re-run, or re-hashed by this design.

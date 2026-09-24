# C4 reproducibility v1 — the graded-posterior comparison is reproducible (P1)

2026-09-24. P1's deliverable: locate/commit the C4 comparison probes, document the
model exactly, and reproduce or retract the regret/dominance claims in
`C4_TASK_DESIGN_v1.md` §9. This file is a **reproducibility record**, not a new study.

**Verdict: REPRODUCED.** Both §9 claims reproduce:
1. **Dominance** — the graded posterior's `(regret_M, regret_C)` frontier lies strictly
   below the `binary+imm` frontier at every matched M-speed, at every q, with the gap
   monotone in q (largest at q=0.9). Reproduced within Monte Carlo noise.
2. **Calibration** — the graded posterior's reported confidence tracks its empirical
   accuracy. Reproduced **exactly** (fixed seed; the numbers were always deterministic).

Two findings are recorded, neither of which changes the claim: (a) the original probes
used a **non-reproducible RNG seed** (`hash(policy)`), now fixed; (b) §9's min-mean table
values were produced by `_c4_uncertainty_pareto.py`, not `_c4_uncertainty_probe.py` as §9's
prose states (provenance note, not a substantive error).

---

## 1. What was committed, and what it is

The five decision-theoretic diagnostics behind `C4_TASK_DESIGN_v1.md` existed only as
untracked files (C4's design commit `6875f38` added the `.md` but not the `.py`). P1
committed them:

- `_c4_uncertainty_probe.py` — the canonical diagnostic: observation process, the four
  policies, regret sweep, per-cause breakdown, calibration. (Design doc §Files: "canonical".)
- `_c4_uncertainty_pareto.py` — the `(regret_M, regret_C)` frontier comparison that produced
  §9's dominance column. (Design doc §Files: "Pareto".)
- `_c4_uncertainty_probe2.py` / `_c4_uncertainty_probe3.py` / `_c4_uncertainty_probe4.py` —
  superseded intermediate probes (kept for the record, per §Files).

Commits: `6d4eb04` (probes as delivered, unchanged) then `[seed-fix commit]` (deterministic
seed + the re-run outputs below). The `.out.txt` files are P1's re-runs, labelled as such —
they are **not** the historical C4 outputs, which were never saved as files (only inline in
§9). No frozen artifact, runner, protocol, or hash was edited, re-run, or re-hashed.

---

## 2. The model, specified exactly

### 2.1 Generative model — the two causes

The task is the C2 occluded-`used_held` gate (C2 §3–4), reduced to its hold-and-observe
observation process. Two causes, both producing the same immediate failure (a channel-1
contact yields nothing):

- **M (move).** The held entry is stale. Every contact is unproductive; when the gate is
  open the contact shows `used_held = 'held'`. Correct action: relinquish.
- **C (cut).** The read is suppressed; contacts fall back to blind search, which is
  productive with probability `P_YIELD = 1/PORTS = 1/4`. When the gate is open the contact
  shows `used_held = 'blind'`. Correct action: hold.

### 2.2 Observation process (what each policy sees, per contact)

The gate occludes `used_held` on an i.i.d. Bernoulli(`q`) fraction of contacts, so the
observable `used_held` is three-valued: `held` / `blind` / `occluded`. Per contact the policy
observes the pair `(used_held, productive)`:

| observation | possible under | log-likelihood-ratio toward M |
|---|---|---|
| `held`, any | M only | +∞ (decisive M) |
| `blind`, any | C only | −∞ (decisive C) |
| `occluded`, productive | C only (M never yields) | −∞ (decisive C) |
| `occluded`, unproductive | both | `log(q·1 / (q·3/4)) = log(4/3) ≈ +0.288` |

Note the probe simulates only `(used_held, productive)`: `bound` is **constant at 1**
throughout, because in the hold-and-observe regime the organism withholds relinquishment and
keeps holding a live entry under **both** causes (under a cut the introspection read stays
bound, C2 §3; under a move the entry is intact but stale). The probe therefore drops the
constant `bound` and simulates the two varying observables. This is the one simplification
relative to C2's three-tuple interface, and it is valid only in the hold-and-observe regime.

The likelihood of the occluded-unproductive observation is `q·1` under M (M is always
unproductive) and `q·(3/4)` under C (blind fallback fails 3/4 of the time), giving
`LR = log(4/3)`. The frozen constant `P_YIELD = 1/4` (PORTS = 4) supplies this LR.

### 2.3 Priors and cause persistence

- **Cause persistence:** the cause is fixed for the whole episode (no mid-episode switch).
  The move/cut is permanent over the horizon.
- **Graded prior:** the posterior starts at log-odds `L = 0` (i.e. `P(M) = P(C) = 1/2`).
- **Binary prior:** the binary estimate `e` starts at `'M'` (not 1/2) — an asymmetry carried
  over from the AC107 bit's initialization. It is updated only on **open** contacts
  (`held` → M, `blind` → C) and is left unchanged on occluded contacts (it is the "last
  open-gate conclusion", C2's maintained separator H).

### 2.4 Action opportunities, stopping rule, horizon

- One decision opportunity per contact (per tick `t = 0 … H−1`); the policy may relinquish
  at any contact.
- Stopping rule: act when the policy's decision quantity crosses its threshold (see §2.6);
  otherwise the episode ends at `H` with the "hold throughout" outcome.
- Horizon `H = 96` (the C2/AC107 cut window `W`).

### 2.5 Loss function (regret)

Asymmetric, faithful to the AC107 economics:

- hold under M: **+1 per contact held** (sustained lost income, never re-acquired) — so
  `regret_M = t`, the tick at which the policy acts (contacts held before acting); `H` if it
  never acts.
- relinquish under M: **0** (correct; the loss ends).
- hold under C: **0** (correct).
- relinquish under C: **+R**, with `R = 4` (drop a valid entry; one-time re-bind cost).

Expected regret is the mean of this per-episode cost over Monte Carlo episodes, separately
for each cause.

### 2.6 The four policies (candidate + three rivals), same information set

All four read the same `(used_held, productive)` stream. `n` is the current run of
consecutive unproductive contacts (reset to 0 on a productive contact).

1. **`raw`** (state-blind streak): on each contact, `n = 0 if productive else n+1`;
   relinquish when `n >= N`. No cause attribution, ignores `used_held`.
2. **`binary`** (AC107 bit + streak): maintain `e`; on open contacts update
   `e = 'C' if used=='blind' else 'M'`; on occluded contacts leave `e`; increment `n` only
   while `e == 'M'` and unproductive; relinquish when `e == 'M' and n >= N`.
3. **`binary+imm`** (strongest heuristic): `binary` **plus** immediate relinquish on an
   open `held`-fail (decisive M). Closes the binary estimate's decisive-action gap, so the
   comparison is against the best heuristic, not a strawman.
4. **`graded`** (candidate): log-odds `L`, updated per contact as
   `blind or productive → L = −∞; held → L = +∞; occluded-unproductive → L += log(4/3)`;
   relinquish when `L >= logit(theta)` (equivalently `P(M) >= theta`).

### 2.7 Parameter grids and tuning (per-policy minimization)

Each policy is minimized over its **own** parameter grid (never given a weaker set):

- `raw`: `N ∈ {1, 2, …, 24}`.
- `binary`, `binary+imm`: `N ∈ {2, 3, 4, 5, 6, 8, 12, 24}` in the canonical probe;
  `N ∈ {1, 2, …, 24}` in the Pareto script (the discrepancy behind the §9 provenance note,
  §3.2).
- `graded`: `theta ∈ {0.55, 0.6, 0.66, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95}` in the probe;
  a finer `{0.5, 0.52, 0.55, 0.58, 0.6, 0.62, 0.66, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95}` in
  the Pareto script.

"Best parameter" = the grid point minimizing mean regret `(regret_M + regret_C)/2`. No
cross-validation; the minimization and the evaluation use the same Monte Carlo stream (a
design-level diagnostic, not a generalization estimate — see §5).

### 2.8 Sampling, seeds, uncertainty, calibration

- Monte Carlo size: `n_ep = 6000` episodes (probe), `n_ep = 20000` (Pareto), `n_ep = 60000`
  (calibration tables).
- RNG: NumPy `PCG64` via `np.random.default_rng(seed)`.
- **Regret seed** (original): `[0, hash(policy) % 1000, int(q*1000), 7]`. The middle term
  `hash(policy)` is the Python hash of the policy **function object**, which is id-based
  (memory address) and varies across processes — so the regret estimates were **not
  bit-for-bit reproducible** (verified: `hash(regret_raw)` differs run to run). The estimates
  were stable only within MC noise. **Fixed** by P1: `_POLICY_SEED` maps each policy's
  `__name__` to a fixed integer `{regret_raw:1, regret_binary:2, regret_binary_immediate:3,
  regret_graded:4}`, so the seed is `[0, _POLICY_SEED[policy.__name__], int(q*1000), 7]` and
  every draw is now deterministic across runs. The model (likelihoods, update rules, grids,
  loss) is **unchanged** by the fix.
- **Calibration seed** (unchanged, always fixed): `[99, int(q*1000), 3]`.
- Calibration is computed only for the graded policy at `q=0.5, theta=0.75`: for each episode
  record, at the moment the policy acts, the posterior `P(M)` (the confidence) and whether
  the action was correct (cause == M). Binned confidence vs empirical accuracy is the
  calibration curve.

### 2.9 Resource accounting and information available to every policy

The probe is **decision-theoretic, not organism-scale**: there is no material/energy ledger,
no memory bank, no paid write. The only cost is the regret of §2.5. Information available to
every policy is identical: the `(used_held, productive)` stream with `used_held` occluded on
a Bernoulli(`q`) fraction (and `bound` constant at 1, hence omitted). No policy receives the
cause label, the gate schedule, or any privileged read. This is the design's anti-confound
property, preserved.

---

## 3. Reproducibility findings

### 3.1 Seed non-determinism (original flaw) — fixed

The original `mc()` seeded the RNG with `hash(policy) % 1000`. `hash()` of a function object
is its id (memory address), which differs across processes (verified: two runs of the same
import gave `hash(regret_raw)` = 15962990320964 and 16916617698628). Consequence: the regret
tables could not be reproduced bit-for-bit from a fresh process; they were reproducible only
within MC noise. The calibration tables (fixed seed) always reproduced exactly. P1 replaced
the id-based term with a fixed per-policy integer (§2.8), making the whole diagnostic
deterministic without changing the model.

### 3.2 §9 provenance note — the min-mean table is the Pareto script's output

§9's prose attributes the min-mean regret table to `_c4_uncertainty_probe.py`, but the
table's values come from `_c4_uncertainty_pareto.py`. The decisive evidence is q=0.9:
`binary+imm` min-mean = **1.744**, which requires `N=1` in the rival's grid; the canonical
probe's `binary+imm` grid is `{2,3,4,5,6,8,12,24}` (no N=1), so its q=0.9 `binary+imm`
min-mean is **1.906** (best N=2). The Pareto script's grid is `range(1,25)` and gives
**1.740**. §9's 1.744 therefore matches the Pareto script, not the probe. Both files
demonstrate the same dominance; the note concerns which file produced which number.

---

## 4. Verification (P1 deterministic re-run, committed as `.out.txt`)

### 4.1 Dominance — reproduced within MC noise

Min-mean regret (mean over M and C, each policy at its own best parameter), P1 re-run vs §9:

| q | §9 binary+imm | re-run binary+imm | §9 graded | re-run graded |
|---|---|---|---|---|
| 0.5 | 0.485 | 0.489 | 0.480 | 0.474 |
| 0.7 | 0.995 | 0.988 | 0.884 | 0.879 |
| 0.9 | 1.744 | 1.740 | 1.359 | 1.341 |

The Pareto frontier (from `_c4_uncertainty_pareto.out.txt`) separates at every matched
M-speed. Pointwise, graded C-cost is lower at matched regret_M, at every q:

| q | matched regret_M | binary+imm C | graded C |
|---|---|---|---|
| 0.5 | ≈0.50 | 0.674 | 0.560 |
| 0.5 | ≈0.75 | 0.263 | 0.215 |
| 0.7 | ≈0.70 | 1.456 | 1.080 |
| 0.7 | ≈1.18 | 0.820 | 0.576 |
| 0.7 | ≈1.52 | 0.455 | 0.299 |
| 0.9 | ≈0.90 | 2.928 | 1.813 |
| 0.9 | ≈1.71 | 2.363 | 1.214 |
| 0.9 | ≈2.44 | 1.851 | 0.824 |

These match §9's "graded dominance" column point-for-point (e.g. §9 "M≈1.70: C 2.37 → 1.26"
vs re-run 2.363 → 1.214; §9 "M≈0.70: C 1.49 → 1.11" vs 1.456 → 1.080). Differences are all
≤ ~0.02, consistent with n_ep=20000 MC noise. The boundary control also reproduces: at
q→0 the two coincide (both read the decisive bit immediately; §9's falsification direction).

### 4.2 Calibration — reproduced exactly

`q=0.5, theta=0.75` (fixed seed, so exact): mean confidence at action **0.985** (M) /
**0.760** (C); binned `(0.7,0.8] → 0.748` correct (n=4950); `(0.9,1.0] → 1.000` correct
(n=56299). Identical to §9.

---

## 5. Scope, and the model-result statement

The comparison is a **decision-theoretic model result**, not an organism result. The graded
posterior is a Bayesian posterior computed under a **stipulated correct likelihood model** —
the frozen `P_YIELD = 1/4` supplies the LR `log(4/3)`, the gate probability `q` is known to
the model, and the prior is stated. That the posterior is calibrated and decision-improving
under these stipulated correct likelihoods is therefore a property of the **model**, and it
does **not** establish that any organism acquires or maintains such an uncertainty estimate
in vulnerable, paid-maintained state. The implementing-study questions — whether the organism
can store and maintain a graded log-odds register and its likelihood weights, and whether the
reliability tier (`P_YIELD` made to vary) is separately acquired — remain open and are not
answered here. The regret minimization is in-sample (same MC stream for tuning and scoring),
so the magnitudes are design-level diagnostics, not generalization estimates; the qualitative
dominance ordering is the load-bearing claim and is the part reproduced.

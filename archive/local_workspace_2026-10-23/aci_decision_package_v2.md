# ACI decision package v2: ledger/provenance mapping, overreach flags, SCARCITY_GAP evaluation

**Additive successor to `/workspace/aci_decision_package_v1.md`.** v1 stays in force: the
amended two-stream Stage A admission, its signatures, costs, outcomes and 13 answers.
v2 changes none of it and adds §A–§D below.

- DRAFT for Aidan, 2026-10-20 (EDT).
- Read-only: nothing was run, and no repository or ledger file was changed.
- The ledger edits below are **proposals** for a gated, versioned successor
  (`ACI_ARCHITECTURAL_BELIEF_LEDGER_v2.json`). They are not applied.
- Inputs:
  - `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` at HEAD `32cfbe6`;
  - `/workspace/astra_consult_1.md` (treated as hypotheses);
  - `SCARCITY_GAP_v1.md` and `scarcity_v1/certificate.py` on the unmerged branch
    `origin/elminster/loving-ptolemy-ityj4l` (`33fa803`), read via `git show` and not
    executed.
- Out of scope here, to avoid duplication: filter algebra, alias checks and the SUB-A0
  adversary. Those go to `/workspace/review/filter_algebra.md`, `alias_check.md` and
  `sub_a0_adversary.md`. Where §A depends on them, it says so.

---

## A. Outcome → exact ledger entries

The ledger has three arrays: `layer_assessments` (O0–O4, C0–C7), `collapse_ledger` (12
entries) and `inactive_theory_queue` (4 ideas). Unlisted entries are unchanged under every
outcome.

### A1. Two-stream Stage A: PASS
(i)–(iii) hold, (iv) verifies as an identity, and the replay agrees.

| Ledger entry | Change | How |
| --- | --- | --- |
| `layer_assessments[C2]` (PARTIAL) | **Status unchanged.** Add an evidence row of type analytic/EXTERNAL. | `scope` gains: "an analytic EXTERNAL world with exact first-order history/joint consequences, realized by an ordinary 3-number state". `ceiling` gains: "world admission, not acquired content". `next_falsifier` is unchanged: a learned agent must still pass a matched-observation content/history intervention. |
| `layer_assessments[C3]` (PARTIAL) | **Status unchanged.** Add a rival-anchor note only. | `rival` already lists "joint filter". Record that in this world the joint filter equals marginals + covariance by algebraic identity. That is **not** new evidence about integration machinery. |
| `layer_assessments[O0..O4]`, `[C0,C1,C4..C7]` | No change. | Stage A is O0 throughout and outside the O-axis (v1 Q12). |
| `collapse_ledger` | **No new entry.** | No proposed mechanism collapsed. The identity (iv) is not a reduction finding. Logging "integration machinery reduced to covariance" would be overreach (§B, R3). |
| `inactive_theory_queue[2]` ("self-model implicit in repair/resource consequences") | No change. | Its known reduction, "conventional state estimation/control", is the PASS realization itself. |
| Non-ledger | Board card #38 (`aci-world-admission-human-gate`) moves to done. A new todo card is added: "HUMAN GATE: Stage B (capacity-bounded variant) or Q-LEARN protocol". | Tree v5 Program A: only the "analytic world competence" part of its required evidence is met. "Permitted experience" and the "prospective learning gate" remain open. A6 stays parked, A8 stays blocked, and SUB-A0 is unchanged. |

### A2. Two-stream Stage A: FAIL
Any of (i)–(iii) misses its threshold.

| Ledger entry | Change | How |
| --- | --- | --- |
| All `layer_assessments` | **No status change.** | FAIL is a fact about one world at one horizon and noise level. It says nothing about C2 or C3 capacities. |
| `collapse_ledger` | **No entry.** | A benchmark rejection is not a mechanism collapse. |
| Non-ledger | Card #38 is closed as "rejected under protocol". Tree v5 Program A records that this world is not admitted. | The next world needs a new additive rationale and a human gate. Retuning noise or horizon is forbidden (`ACI_NEXT_EXPERIMENT_DECISION_v1.md`). |

### A3. Two-stream Stage A: UNRESOLVED
Replay, normalization or simplex failure, or an implementation defect.

No ledger change of any kind. Provenance only: an errata file, an additive fix and a
re-replay. A second defect parks the node, and the card stays todo with a note.

### A4. If Aidan parks SUB-A0 (Astra's recommendation; option 3 in `SUB_A0_CAL_RESULTS_v2.md`)
This is a separate decision, recorded here only because the ledger currently has no SUB_A
or SUB_A0 entries at all.

| Ledger entry | Proposed change | Why |
| --- | --- | --- |
| `collapse_ledger` | **Add** an entry. Mechanism: "every-tick live-trace self-repair". Reduction: "external every-tick schedule / repetition code with host median". Source: `SUB_A_ANALYTIC_CHECK_v1.md` §C, §F. Belief changed: "vulnerable gain is not vulnerable performing machinery". | This is an existing analytic, design-level reduction that was never ledgered. It is independent of the park decision. |
| `inactive_theory_queue` | **Add**: "learned self-priority for vulnerable repair machinery". Known reduction: damage-proportional repair (DISAGREE_PROP). Falsifier: allocation excess fails. Cheapest test: sign-coded/bistable substrate recalibration (`SUB_A0_CAL_RESULTS_v2.md` option 2). Execution: not authorized. | Parking must keep the idea testable. |
| `layer_assessments[O1]`, `[O3]` | **No change.** | SUB-A0 engineering was INVALID and calibration stopped at the probe. Neither result supports or counts against O1/O3 (`SUB_A0_ENGINEERING_ERRATA_v2.md` "Citation rule"). |

### A5. Provenance flag on existing entries (independent of all outcomes)
Commit `d0ee2bb` (2026-10-02) removed the raw records and audit/replay inputs behind several
existing entries (`/workspace/aci_frontier_audit.md` §5):

| Entry | What it rests on | Deleted inputs |
| --- | --- | --- |
| `layer_assessments[O2]` and `[C0]` | `CLOSURE_VERDICT_v1.md` | Program row "AC79→AC80"; description row "AC80/85/86"; route memory "AC75". Deleted: `ac79_*`, `ac80_results_v1`, `ac75_results_v1`. |
| `collapse_ledger[0]` (watchdog self-monitor) | `ACI_MISSION_AUDIT_v1.md` §2.6 item 1 (AC67/AC71) | `ac67_*`, `ac71_results_v1` |
| `collapse_ledger[4]` (adaptive switch → fixed level) | Mission audit | Rests on AC11, which is **intact**. |

Proposal: tag these entries `provenance: raw records removed in d0ee2bb; recoverable at
d0ee2bb^ with hashes matching a6_decision_v1/baseline_hashes.json`, until the records are
restored. Their verdicts are not in doubt, but their independent replay is currently not
runnable from HEAD.

---

## B. Scope-overreach risks (pre-registered "do not write" list)

| # | Overreach | Why invalid | Allowed wording |
| --- | --- | --- | --- |
| R1 | "Benchmark admitted → cognition acquired / C2 advanced" | Stage A has no learner. Analytic construction shows existence, not acquisition (constitution v3). | "World admitted; acquisition untested." |
| R2 | "Benchmark FAIL → joint integration unnecessary / C3 falsified" | One world, one horizon and noise level. The likely failure mode is insufficient headroom (Astra). | "This world lacks frozen-threshold headroom." |
| R3 | "Joint statistic sufficient → integration machinery unnecessary in general" | (iv) is an algebraic identity in this world. It is not a reduction test of any proposed machinery. | "Ordinary 3-number state is sufficient here by construction." |
| R4 | "(ii) and (iii) both passed → two independent lines of evidence" | Both measure the same omitted quantity c = Cov(X,Y \| h). Factorized-vs-joint XOR forecasts differ by 2c (Astra; algebra delegated to `filter_algebra.md`). | "One consequence of correlation, measured two ways." |
| R5 | "Factorized product decoder loses → marginals are insufficient" | If reachable marginals identify histories, a nonlinear decoder of the marginals recovers XOR. Only a reachable-alias witness (equal marginals, different XOR/continuation) supports "marginals insufficient" (Astra; check delegated to `alias_check.md`). | "The product projection loses XOR information." |
| R6 | "Terminal oracle projection loses → an autonomous marginal filter fails" | Projecting oracle marginals at the end is not a filter whose updates close on its retained state. | State which object was tested. |
| R7 | "Probe failure → maintenance impossible / substrate cannot host repair" | SUB-A0 stage 1 shows real pressure and full external repairability. Only the probe was unidentifiable. The author already flags the protocol's §9 wording as overreach (`SUB_A0_CAL_RESULTS_v1.md`). | "Capacity probe unidentifiable at the tested depths and windows." |
| R8 | "R unrepairable → learned self-priority refuted" | That is a substrate fact (magnitude non-identifiability), not a test of allocation (`SUB_A0_R_REPAIRABILITY_CHECK_v1.md`). | "Substrate predicts a NEGATIVE independent of allocation." |
| R9 | "A6 UNRESOLVED → R9 cannot be competent / capacity insufficient" | Eight symbols are certified sufficient. Only shared-R9 existence is open (`A6_GATE_REDUCTION_v1.md`). | "Deployed shared-R9 existence open." |
| R10 | "Scarcity access value > 0 → agent-referent self-model / C4" | See §C: it is a monotone readout of the bounded posterior. | "Bounded-optimal coding has state-dependent abstention." |
| R11 | "Stage A PASS licenses Stage B or training" | Each needs separate human approval. | — |

---

## C. Does SCARCITY_GAP_v1 escape Astra's sufficiency critique?

**Astra's point:** in a known finite-state world, the full posterior is sufficient. Behavior
cannot show informational necessity beyond a sufficient state, so any extra state z must be
shown to carry what the declared ordinary state omits.

**SCARCITY_GAP's move:** cap the agent's state at K < |range S| (ρ = log K/H(S) < 1). The
agent's state m = g(h) is then a strict garbling. Agent-referent quantities become
non-redundant: selection, access representation, and "self-induced uncertainty".

### C1. What scarcity does escape
- **The ideal-observer collapse (C0's premise).** Under a garbling, P(world | m) ≠ P(world | h)
  on positive mass. The agent's confidence then depends on its own encoding, not only on the
  world. This matches the scope already granted by `C1_RELIABILITY_DISPOSITION_v1.md`:
  monitoring is identifiable only where the ideal-observer assumption fails.
- **Free sufficient-statistic rivals.** At capacity parity, the zero-cost broadcast or
  counter that won Phase III (`PHASE3_VERDICT_v1.md` §1) no longer fits.
- **Encoder choice (selection) becomes consequential.** In 24/63 scarcity cells, the
  goal-dependent encoder strictly beats `cue_blind` (`SCARCITY_GAP_v1.md` §5).

### C2. What scarcity does NOT escape
The critique applies one level up.
- **For any fixed encoder g, the agent's own state m plus the known g is a sufficient
  statistic for its decisions.** The optimal decoder is the Bayes action under P(· | m).
- In the certificate, a memory state **is** its codeword, i.e. its action per query
  (`certificate.py` docstring and `CODEWORDS`). So the "access representation" is not an
  additional variable. It is the opt-out entries of m's codeword.
- At the optimum, each entry must be Bayes-optimal for the posterior within m's encoding
  cell, or swapping the codeword would raise reward. So opt-out = 1[max_x P(x_q | m) < r],
  up to ties. That is a **monotone first-order transform of the bounded posterior**.
  This is exactly the ledger's C4 `next_falsifier`: "evaluation is only a monotonic
  first-order transform or cannot be selectively mistaken" (`layer_assessments[C4]`).
- **The rivals that lose are restricted classes, not same-information ordinary agents:**
  - `static` forbids state-dependent opt-out, which any K-state Bayes decoder has for free.
  - `no_opt` forbids opt-out entirely. Its label "wagering by ideal-observer confidence" is
    a description, not a separate strategy.
  - The strongest same-capacity ordinary rival is the unrestricted bounded Bayes agent,
    which **is** `full`.
  - So "access value > 0" means "state-dependent abstention beats a decoder forbidden from
    it". That is an ordinary bounded-optimal coding fact. The document concedes as much:
    "ordinary bounded-optimal state estimation … That is the point" (§2), and "Nothing here
    is … metacognitive in the C4 sense" (§5).
- **Verdict:** scarcity escapes the *ideal-observer* sufficiency (world posterior given h).
  It does **not** escape sufficiency relative to the agent's own state.
  - Behavior can still not show any variable z beyond the bounded state m.
  - What becomes non-trivial is (a) *which* garbling is optimal (selection or allocation)
    and (b) that decoding must be calibrated to the agent's **own** encoding.
  - (b) is only trivial when g is fixed and supplied, as in the analytic optimum. It
    becomes a real question when g changes during life (decay or maintenance, §6 of the
    document) or must be learned (Q-LEARN). Only there could "tracking one's own current
    encoding" separate from a decoder that assumes a fixed g.

### C3. Cheapest falsifiers, in cost order

1. **Monotone-readout check (zero new computation; a reading of the stored certificate,
   not done here).**
   - Claim tested: "the access representation is a variable beyond the bounded first-order
     state".
   - Procedure: for each of the 14/63 access-positive cells, confirm that every opt-out
     entry equals 1[max_x P(x_q | m) < r] under the optimal codebook and encoder.
   - Prediction from the argument above: it holds everywhere, so the access claim falls
     under the ledger's C4 falsifier. Selection is unaffected.
   - Needs only an approved read of `scarcity_v1/certificate.json` plus a short independent
     arithmetic script. It is not an experiment, but it is still behind your "no runs"
     instruction.
2. **Own-state alias witness (the analogue of Astra's history-pair witness).**
   - Search for two reachable histories mapped to the same m whose required continuation or
     abstention differ.
   - By the codeword construction this is impossible within a fixed g, so any claimed z is
     redundant. If the review agrees, this is a proof, not a computation.
3. **Moving-encoder discriminator (the first test that could survive).**
   - In the §7.2 paid-maintenance variant, decay changes the effective g over time.
   - Rival: a decoder given m plus the agent's own past maintenance actions (efference
     copy), at equal capacity.
   - If this rival is optimal, an "access record of what is being maintained" is redundant
     with ordinary state plus action history, and the §6 O/C-intersection claim reduces.
   - Only a positive here would show something beyond ordinary bounded estimation.
   - Cost: new analytic design plus a solver-like optimization, so a human gate is required.

### C4. Recommendation for the package
- **Keep Stage A as in v1.** Its claims are modest and can be checked by identity.
- **Treat SCARCITY_GAP's selection and allocation result as the substantive Stage-B
  candidate.** Its access/self-referent framing should be reclassified as REDUCED, pending
  falsifier 1.
- **If Stage B is approved, make falsifier 3 (moving encoder versus efference-copy rival)
  its primary contrast**, not static-versus-full access value. Report access value
  descriptively, as SCARCITY_GAP itself proposes for value margins (§4).
- **Before citing the branch, review and merge it** (or record it in errata). It is
  unreviewed: its K ≥ 4 optimality rests on branch-and-bound without brute-force replay.

---

## D. Disagreements with Astra

- **Agree:** approve Stage A; no layer promotion from PASS; the trivial-pass risk; an
  alias audit; leave ledger changes behind gates.
- **Agree, subject to Aidan's separate decision:** park SUB-A0. Parking should add the two
  ledger records in A4 so the idea and the SUB_A reduction aren't lost.
- **Addition:** Astra's sufficiency critique applies to SCARCITY_GAP's access claim (C2
  above), but not to its selection/allocation claim. Astra's own O3 suggestion (content
  change → maintenance of an enabling mechanism → future cognition) lines up with
  SCARCITY_GAP §6–7.2. That is the better use of the branch.

# I1 — Correct the boundary assessment (composition, temporal window, spatial criterion)

2026-09-24. Correction deliverable for the I1 card (t_cbdeceec). It corrects two
documents — `A4_EXCHANGE_VERDICT_v1.md` (the successor's bounded autopoiesis
assessment) and `S0_SYNTHESIS_v2.md` (the terminal synthesis) — in exactly three
places, and it produces the integration-dependency list the card requires.
Predecessor: t_3eba13c2 (I0, `ARCHITECTURE_BY_CLAIM_MATRIX_v1.md`), which located
the error in the code at e5f6050.

This document runs nothing, re-hashes nothing, and edits no frozen artifact. One
clearly-labelled diagnostic replay (`_i1_temporal_diagnostic.py`) is added for the
temporal measurement; it re-uses `ac114.build()`'s frozen surgery with an
observational recorder only, writes into no frozen results directory, and leaves
`ac114_results_v1/` untouched. It is a diagnostic, not a frozen run, and is not
hashed into any `pre_run_snapshot.json`.

---

## 0. The three corrections, stated first

1. **Composition (deliverable 1).** A4 §0(a), §1, §8 and S0 §3, §5 transferred the
   **five-component production-closure verdict** (K3, `CLOSURE_VERDICT_v1.md`) — over
   the component set {W, C, B, description, derived program} plus the maintained state
   {pointer, coordination, route memory, decision state} — into the AC114 boundary
   successor **without a composition argument**. AC114 (`ac114.py`) contains **none** of
   the five internalization mechanisms (I0 §4, verified in code): no description store
   (`ac9.acquire` zeroes `traces[1:]`), no succession controller, no reconstruction, no
   internalized operational memory, no decision allowance. The K3 verdict is earned by
   the AC80–99 mechanisms composed in AC105, a different lineage. AC114 legitimately
   carries only AC10's **{W, C, B} retention + production** (field-for-field, G2). The
   verdict is therefore **scoped down**: AC114 supports production closure over the
   material constituents {W, C, B}, not the full five-component claim.

2. **Temporal window (deliverable 2).** A4 §3 and S0 §2 use the frozen "post-onset"
   (`assay`, t ≥ ONSET = 512) admission of `no_B_retention` as evidence that the site
   gate actively blocked the interface. That window is **post-mortem**: the organism
   dies at t ≈ 379–386, before ONSET. The correct discriminator is admission **while
   alive with the gate links dead** (the t = 133 → death window), measured directly
   (§2 below). The mechanism claim survives the correction — the site gate genuinely
   refuses admission while the organism lives — but the frozen G3 gate's admission half
   does not demonstrate it; only the alive-window measurement does.

3. **Spatial criterion (deliverable 3).** A4 §4.1, §6 and S0 §5, §6.1 count "the space
   is supplied" as one of the reasons clause (ii) is not met, and S0 calls it "the
   unfixable limit (infinite regress)." Supplied coordinates and physical laws are
   **permitted substrate**, not a failure of autopoiesis — every formalization bottoms
   out in supplied laws. The scientific question clause (ii) asks is whether the
   **produced components constitute the organizational domain**. The one genuine
   modeling limitation is the **non-spatial informational core**. "Supplied space" is
   therefore struck from the limitation list; clause (ii) is limited by one modeling
   declaration, not two.

---

## 1. The composition correction (what was transferred without composition)

### 1.1 What is preserved (AC114's valid bounded finding)

Unchanged by this correction, and stated at its exact ceiling:

> Link-specific resource admission depends on produced boundary state in an
> AC9-derived organism that also exhibits constituent retention and boundary renewal.

Concretely, three things, each frozen and re-audited (A3):

- **Site-gated admission (D1/D2/D3, G4/G5).** Channel-c intake is a function of the
  local live-state of `GATE_LINKS[c]` alone; puncturing the gate link zeroes channel-0
  admission while the count rival keeps admitting (G4, paired 16/16); a non-gate
  puncture leaves both channels admitting (G5, 16/16); the same links retain and admit
  (D3, 16/16).
- **Constituent retention.** Inherited from AC10 **field-for-field** (G2: the
  `no_B_retention_ref` arm reproduces the frozen AC10 `no_B_retention` arm including
  `state_hash`, pinned by `test_ac114.py`).
- **Boundary renewal.** `keep` B_birth 204–207 over 2048 ticks ≈ ≥10× the 20-link
  complement (D5), so the gate links turn over and are re-established by action 8.

These three rest on AC10's retention + production (G2) and AC114's own admission gates.
They do **not** rest on, and are not evidence for, any of the five internalization
mechanisms.

### 1.2 What was wrong

A4 §1 claims, under the accepted substrate convention, "production closure (clause (i))
over the component set {W, C, B, description, derived program} … each meeting C1–C5,"
plus "maintained state {pointer, coordination, route memory, decision state} meeting
S1–S4," and then "the C1–C5 evidence for W, C, description, and program is reused
without re-examination." S0 §5 restates the same five-component set and the four-item
maintained state.

AC114's organism is `ac9_priority_v2.acquire` — the AC9 developmental body. Per I0 §4
(verified in code): there is **no description store** (`ac9.acquire` sets `traces[1:]=0`,
so no bank-1 recipe to turn over), **no succession controller** (no pointer, no
active/phase/last-start), **no reconstruction** (`prog.choose` is called directly; no
`build_program`/`reg_from_active`), **no internalized operational memory** (no streak/
reserve in the dead rule's free bits), and **no decision allowance** (no
`DECISION_ALLOWANCE`/`budget_rule`/`reserve`). The program bank is repaired by action 2
(majority repair), but it is inherited content, never re-derived from a description.

Therefore the K3 verdict's component set {description, derived program} and the
maintained-state items {pointer, coordination, decision state} **do not exist in AC114**.
The only component the successor affects is **B**, and the only closure evidence AC114
legitimately inherits is **AC10's {W, C, B} retention + production**. Saying "clause (i)
SUPPORTED … and now extended" in the AC114 verdict transferred the AC105 five-component
result across lineages without demonstrating that the two architectures compose.

### 1.3 The corrected claim

- **For AC114, production closure is SUPPORTED over {W, C, B} only** — the three
  produced material constituents, on the W → B → W / W → C → energy → W cycles, inherited
  field-for-field from AC10 (G2) and left undisturbed by the confined admission-gate diff
  (G1 byte-identity).
- **The full five-component clause-(i) verdict (K3) does not transfer to AC114.** It
  belongs to the AC105 architecture (the AC80–99 mechanisms composed in one run). It is
  not a property of the boundary-exchange successor, which contains none of the
  description/succession/reconstruction/memory/allowance machinery.
- **The B-specific extension is valid and is the only extension licensed.** AC114 adds a
  second causal role to B (retention → retention + exchange), without changing B's
  production. This extends the {W, C, B} closure's *content*, not the five-component
  verdict.

---

## 2. The temporal correction (deliverable 2)

### 2.1 The frozen measurement and why it is post-mortem

The frozen G3 gate (and A4 §3 / S0 §2) read `no_B_retention`'s **post-onset**
(`assay`, t ≥ ONSET = 512) admission as zero, against the twin's 416–448. But
`no_B_retention` **dies at t ≈ 379–386, before ONSET = 512** (frozen `chrono`,
diagnostic §2.2). The `assay` window is therefore entirely post-mortem for that arm:
`assay['in_f'] == 0` records zero intake **after death**, not an actively blocked
interface. Comparing the dead arm's post-mortem zero against the surviving twin's
alive 416–448 is a confounded comparison — one organism is dead, the other alive.

### 2.2 The corrected measurement (clearly-labelled diagnostic)

`_i1_temporal_diagnostic.py` re-runs the frozen `ac114.build()` surgery with an
observational recorder on `prog.choose` (returns the identical action; behaviour
unchanged) and measures, per tick, the gate-liveness, the contact attempts (action 0/1
with port match — the exact frozen branch that calls `ac4.react`), the admission result,
and death. Frozen rows are loaded only to cross-check the cumulative ledgers. Final
seeds 6500–6507, 16 individuals per arm:

| Arm | gate links die | death | contact attempts (alive, gate dead) | admitted | refused | intake in window (fuel / material) |
| --- | --- | --- | --- | --- | --- | --- |
| `no_B_retention` (site) | t = 133 (all 16) | t = 379–386 (16/16) | 103–146 | **0** | 103–146 | **0 / 0** (all 16) |
| `no_B_retention_ref` (no gate) | t = 133 (all 16) | never (survives) | 57–59 | **57–59** | 0 | 512–544 / 2624–2752 |

The frozen cumulative ledgers confirm the window attribution: `no_B_retention` total
`in_f` = 32 (exactly one channel-0 contact **before** the gate links died), `in_m` = 0–64;
the twin's totals (544–576 / 2688–2752) are almost entirely post-gate-death.

The temporal sequence is therefore:

1. **Gate links disappear at t = 133** (uniformly — the inherited B endowment decays with
   no B production in either `no_B` arm).
2. **Admission is attempted while alive from t = 133 until death** — the site arm makes
   103–146 contact attempts in that window, **every one refused** (0 admitted); the
   no-gate twin makes 57–59 attempts, **every one admitted**.
3. **Death occurs at t = 379–386** in the site arm (fuel 0, energy 0); the twin survives.

### 2.3 What this changes

The mechanism claim — *the site gate actively refuses intake while the organism is
alive, and this is what distinguishes it from the no-gate twin* — is **confirmed**, but
by the alive-window measurement, not by the frozen "post-onset" scalar. The frozen G3
gate's **admission half is vacuous** (post-mortem); its **survival half is valid** (site
does not complete, twin does). The corrected discriminator — admission while alive with
dead gate links: 0 vs 57–59/57–59 — is the one that should travel with the claim.

---

## 3. The spatial-criterion correction (deliverable 3)

### 3.1 The corrected criterion

- **Supplied coordinates and physical laws are PERMITTED substrate.** The lattice, the
  5×5 interior, the interior/exterior distinction, the reflection rule, the export bath,
  and the conservation laws are substrate (§5), and their being supplied is **not** a
  failure of autopoiesis. Any formalization of self-maintenance bottoms out in fixed
  substrate (the infinite-regress point is a property of *all* such formalizations, not a
  defect of this one). "Supplied space" is therefore **struck from the list of reasons
  clause (ii) is not met.**
- **The scientific question clause (ii) asks is whether the produced components
  constitute the organizational domain.** In this model the produced components are the
  finite-lived boundary links and the positioned constituents W/C. AC114 establishes that
  at the material layer: a produced, decaying, semipermeable perimeter that retains the
  constituents and admits the intake that funds their production — renewed by that
  production. That is the material layer constituting its own domain.
- **The non-spatial informational core is the one genuine modeling limitation.** The
  program, description, route memory, pointer, and decision state live in fixed arrays
  (`traces`, `mem.Memory`) never positioned and never passed to `tr.move`; they are
  "inside" by declaration. This — not the supplied space — is why the *whole
  organization's* spatial unity is not established: the informational core is not
  spatially realized.

### 3.2 What this changes

Clause (ii) is limited by **one** modeling declaration (the non-spatial controller), not
two. The former second limitation ("supplied space") is reclassified from *limitation*
to *permitted substrate, not counted against the verdict*. This matches the accepted
closure-boundary position (fixed laws are fine; produced components are the closure
question — Montevil & Mossio 2015), and it is the same reclassification A2 §4.1 already
applied to the substitution fact: a supplied item identifies *what the organism must do
with what it produces*, and is not itself a bar to the verdict.

---

## 4. The integration-dependency list (precise)

Before the **full** production-closure verdict (K3, five components + four maintained-
state items) and the **boundary-exchange** result can be claimed of a **single**
architecture, these dependencies must be integrated and their composition demonstrated
(byte-identity at the baseline plus the exchange discriminations), not asserted:

1. **Description turnover** — the 130-bit recipe in interchangeable slots
   (copy → verify → switch → remove). Code: `ac95.Succession`, `SLOTS=4`. Evidence:
   AC80/85/86. **Absent in AC114** (no bank-1 store).
2. **Succession coordination** — the succession controller's working state
   (MODE/LAST) in the maintained substrate, written atomically. Evidence: AC87/88.
   **Absent in AC114** (ONSET is a run-loop flag).
3. **Reconstruction** — the 126-bit program rebuilt from the description on the damage
   signal. Code: `ac95.build_program` / `reg_from_active`. Evidence: AC80/85/87.
   **Absent in AC114** (`prog.choose` directly).
4. **Internalized operational memory** — the decision state (streak + reserve) in the
   dead rule's free bits, Gray-coded, majority-read, W-gated writes. Code: `ac96.streak_*`,
   `ac99_d2.gray_*`. Evidence: AC95/96/99. **Absent in AC114.**
5. **Decision allowance** — the spending budget that reserves material for the decision
   state's writes. Code: `ac104.DECISION_ALLOWANCE = 42`, `budget_rule`. Evidence:
   AC97/98/104. **Absent in AC114.**

The integration is **into AC105** (the single authoritative integrated baseline, I0 §5):
the SR-2 admission gate (present only in AC114) must be added to the AC105 architecture
and the result must reproduce AC105's baseline byte-for-byte (as AC105 reproduces
AC104, etc.) **and** reproduce AC114's admission discriminations (G4/G5), so the
exchange role is shown to ride the same produced B that the five-mechanism organism
already maintains. The two are currently on disjoint lineages and no such composition
run exists.

Also recorded, not required here: the **non-spatial controller** (§3) is the remaining
clause-(ii) limit; moving it is a re-architecture (position the informational core and
pass it to transport), not a study.

---

## 5. Exact disposition against A4 and S0

| Location | Superseded wording | Corrected to |
| --- | --- | --- |
| A4 §0(a) | "production closure (M&V clause (i)): SUPPORTED … and now extended" | SUPPORTED **over {W, C, B}** in AC114; the five-component K3 verdict does not transfer |
| A4 §0(c) | "Two remain … the space/geometry is supplied, and the controller is non-spatial" | **one** genuine limitation (non-spatial controller); supplied space is permitted substrate |
| A4 §1 | "production closure … over {W, C, B, description, derived program}" + "evidence for W, C, description, and program is reused" | only {W, C, B} carry over (G2); description/derived program are absent in AC114 |
| A4 §3 | "the site gate then zeroes post-onset admission (16/16)" | site gate refuses 103–146/103–146 attempts while alive (t=133→~380); death 379–386 precedes ONSET, so "post-onset" is post-mortem |
| A4 §4 item 1 | "Space and geometry … supplied substrate … Producing the space is the infinite-regress point" | supplied coordinates/laws are **permitted** substrate; the question is produced components constituting the domain |
| A4 §6 | "the space itself is supplied" as a reason the whole organization is not a concrete unity | the non-spatial informational core is the reason; supplied space is not counted |
| A4 §8 | "still NOT ESTABLISHED, now for exactly two reasons: supplied space and the non-spatial controller" | one reason (non-spatial controller) |
| S0 verdict ¶ | "limited by **two** modeling declarations (supplied space, non-spatial controller)" | one (non-spatial controller) |
| S0 §3 "Strengthened" | "Production closure (clause i) is **extended**" | extended **over {W, C, B}** (B gains a second causal role); the five-component verdict stays with AC105 |
| S0 §5 | "Components {W, C, B, description, derived program} meet C1–C5 and maintained state … meets S1–S4" | that is AC105, not AC114; AC114 supports {W, C, B} |
| S0 §5 / §6.1 | "(1) the space is supplied … the infinite-regress point"; "the supplied space is the unfixable limit" | supplied space is permitted substrate; the non-spatial controller is the one genuine limit |

### 5.1 Downstream documents carrying the same error (flagged for W0, not edited here)

The spatial-criterion error ("two modeling declarations … supplied space, non-spatial
controller") and the "production closure now extended" phrasing also live in downstream
documents owned by the W0 reconciliation card, which I1 unblocks:

- `P1_MANUSCRIPT_DRAFT_v1.md` (≈line 166) — "limited by two modeling declarations".
- `EVIDENCE_INDEX_v3.md` (lines 30, 360) — "two modeling declarations (supplied space,
  non-spatial controller)".
- `AUTONOMY_RESEARCH_STATUS.md` (lines 94, 190) — "limited by two modeling declarations
  (supplied space, non-spatial controller)".
- `A0_SUCCESSOR_SPEC_v1.md` (line 25) — "other two — supplied space, non-spatial
  controller — … an infinite-regress …".

These are corrected by W0, not here: the scope of I1 is A4 and S0, and the frozen
`AC114_PROTOCOL_v1.md`/`AC114_RESULTS_v1.md` wording ("post-onset admission") is left
untouched as a frozen artifact (the correction is a *reading* of it, not an edit).

---

## Sources

`A4_EXCHANGE_VERDICT_v1.md`, `S0_SYNTHESIS_v2.md`,
`ARCHITECTURE_BY_CLAIM_MATRIX_v1.md` (I0), `CLOSURE_VERDICT_v1.md` (K3),
`DEFINITIONS_CHARTER_v2.md` (§5, §7a, §7b, §8, §9), `A2_BOUNDARY_VERDICT_v1.md`,
`A1_EXCHANGE_SPEC_v1.md`, `AC114_PROTOCOL_v1.md`, `AC114_RESULTS_v1.md`,
`ac114.py`, `ac9.py`, `ac9_priority_v2.py`, `ac4.py`. Diagnostic measurement:
`_i1_temporal_diagnostic.py` (observational only; frozen rows `ac114_results_v1/rows.jsonl`
read for cross-check, never written).

# AC115 — errata v1 (outcome-classification correction)

2026-09-25. Correction deliverable for the M1 card (t_db58b389). Reuses the frozen
evidence (`ac115_results_v1/`, 208 rows) — no simulation re-run, no frozen artifact
re-hashed, no gate moved. Every number below is read directly from `rows.jsonl`;
seeds are the replication unit (8 independent units × 2 histories = 16 individuals).

The four documents reconciled: `AC115_RESULTS_v1.md` (results),
`I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md` (assessment),
`P1_MANUSCRIPT_DRAFT_v1.md` (manuscript), `S0_SYNTHESIS_v3.md` (synthesis), and
the derived `M0_BASELINE_EVIDENCE_INDEX_v1.md`. None is in the study's hash set
(only `AC115_PROTOCOL_v1.md` + the runner + frozen deps are), so correcting them
is a reporting errata, not an edit to a frozen source.

---

## 1. The export contradiction, resolved

**The contradiction.** `AC115_RESULTS_v1.md` §3/§4 states `particle_export == 0`
"on 15/16" while simultaneously stating "6606 (**both histories**) leaks a single
particle". If both of 6606's histories leak, two individuals leak, and 16 − 2 = 14,
not 15. The phrase "one leak on 6606" treated the seed's two histories as one
individual.

**The frozen count.** `keep` arm `particle_export`:

| seed | h0 | h1 |
| --- | --- | --- |
| 6600–6605, 6607 | 0 | 0 |
| 6606 | 1 | 1 |

- `particle_export == 0` on **14/16 individuals = 7/8 seeds**.
- Seed 6606 leaks **1 particle in each history** (2 individuals, `B_discard` 1673 +
  `B_expiry` 2 vs `B_births` 1675). The organism **completes** (survives) on 6606.

Every "15/16" in the four documents is wrong; the correct figure is **14/16
individuals (7/8 seeds)**, and the leak is **two** individuals (both histories of
6606), not one.

---

## 2. Corrected outcome classification (exact denominators, per category)

The four failed gates are NOT one category. Recounted from the frozen rows:

| gate | result | failing seeds | category (this is what failed) |
| --- | --- | --- | --- |
| G4 T2 boundary-supports-entry | **FAIL 2/16 = 1/8** | 6602 | **DEATH** — `no_B_retention_ref` dies t=347 (W=0 at t=127, C=0 at t=223), a challenge-free arm. Admission discrimination intact. |
| G5 retention-vs-admission | **FAIL 2/16 = 1/8** | 6602 | **DEATH** — same t=347 completion miss. Retention/admission discrimination intact. |
| G6 endogenous-vs-external | **FAIL 4/16 = 2/8** | 6602, 6606 | **two categories:** **RETENTION** (6606: `keep` leaks 1 particle, `export==1`, organism completes) + **DEATH** (6602: `B_rescue` dies t=347, `external_B==20`, W=0 C=0). |
| G7 composition-under-stress | **FAIL 6/16 = 3/8** | 6601, 6602, 6605 | **DEATH** (survival miss) — description INTACT at death in every case (see §3). |

**Category totals (individual / seed):**

- **DEATH** (survival miss at the horizon): G4 2/16, G5 2/16, G6 2/16 (6602), G7
  6/16 → 12 individuals = 6 seeds (6602 ×2 arms, 6601, 6605, plus the G4/G5 6602).
- **RETENTION (boundary leak)**: G6 2/16 = 1/8 (6606 only; the organism survives and
  the leak is a single particle, not a death).
- **DESCRIPTION-INTEGRITY**: **zero** of the failures are description-integrity
  failures at the moment of death — `description_correct_at_death == 130` in every
  failing individual (§3). The end-of-run `description_correct < 130` values reported
  for G7 are post-mortem.

The M0 classification of G6's 6606 arm as "INTEGRITY" and of G7 as "DEATH +
DESCRIPTION-INTEGRITY" is corrected to **RETENTION** (G6/6606) and **DEATH only**
(G7), respectively.

---

## 3. The "description degradation" in G7 is post-mortem

`AC115_RESULTS_v1.md` §3 G7 and I5 §7 report `desc 129` (6601) and `desc 80`
(6602) as description-integrity co-failures. The frozen rows show otherwise:

| seed | first_dead | `description_correct` (end of run) | `description_correct_at_death` |
| --- | --- | --- | --- |
| 6601 | 15276 | 129 | **130 (intact)** |
| 6602 | 9589 | 80 | **130 (intact)** |
| 6605 | 16336 | 130 | **130 (intact)** |

The description is **intact at the moment of death in every failing individual**
(all 130/130). The `129`/`80` end-of-run readings are the sticky damage stream
writing *after death* (the AC79 rule: the paid description repair stops at death
while the damage stream keeps writing). The G7 gate's `description_correct == 130`
clause is read at end-of-run, so it is confounded by post-mortem degradation for
6601/6602 — a gate-design note (read the description at the death tick, or gate on
survivors), not a description-integrity failure of the live organism.

G7 therefore fails on the **completion clause only**: all three seeds die before the
horizon (9589, 15276, 16336 — the last 48 ticks short). G7 remains **FAIL 6/16**;
this errata reclassifies its cause, it does not move the verdict.

---

## 4. The t=347 deaths are NOT a long-horizon effect

`AC115_RESULTS_v1.md` §0/§7 (and I5 §7, S0 §2) attribute the G4–G7 failures to
"the AC68 W/C bimodality re-entering through the long horizon". That is wrong for
the t=347 deaths:

- Seed 6602's `no_B_retention_ref` / `B_rescue` deaths are at **t=347**, with
  `first_W_empty == 127` and `first_C_empty == 223` — within the first ~2% of the
  16,384-tick horizon.
- Those arms are `CHALLENGE='none'` (no corruption, no move). The AC68 long-horizon
  bimodality is a ~7000–16000-tick phenomenon under the `simult` challenge; an early
  collapse in a challenge-free B-suppressed arm is a different thing.

The scoped causal statement: seed 6602 undergoes an **early W/C collapse under B
suppression** (W empties t=127, C t=223, death t=347), seed-specific (6603 shares the
same priority `(2,0,1,3)` and survives), so it is neither priority-determined nor
horizon-determined. Only G7's deaths (9589–16336) are late-horizon, and they occur
under the `simult` challenge.

---

## 5. Mechanisms EXERCISED before failure vs functions SUSTAINED throughout

The valid integration result must be stated at the mechanism level, and the two are
distinct:

- **EXERCISED (fired before failure) — holds in all 16 individuals, including every
  failing one.** Reconstruction (`fw_at_corrupt == 8 → flipped_still_wrong == 0`),
  succession (`successions >= 1`: 6 on keep; 5/3/6 on the failing G7 seeds), paid
  updates, and relinquishment all fire. The G2/G3 admission discriminations and the
  G4/G5 retention discriminations hold in every failing individual.
- **SUSTAINED throughout the challenge — does NOT hold.** The G7-failing individuals
  die before the 16,384-tick horizon (9589/15276/16336); the G4/G5/G6-failing 6602
  dies at t=347. "Exercised" is not "sustained to the horizon".

This is the precise content of "mechanism-level composition SUPPORTED; survival-level
composition NOT confirmed" — the mechanisms fire and the discriminations hold, but
they do not keep the organism alive through the simultaneous stress to the horizon.

---

## 6. What remains valid (nothing upgraded, nothing downgraded)

- **G1 (16/16), G2 (16/16), G3 (16/16), G8 (PASS)** — unchanged, all pass.
- **The six functions are exercised in one body** (keep arm, 16/16, each backed by
  its firing record) — unchanged, valid.
- **G4–G7 remain FAILED** (2/16, 2/16, 4/16, 6/16). This errata corrects the
  *denominators and outcome categories*; it does not turn any failed criterion into a
  pass. Direction of every correction is toward *more* or *more precisely scoped*
  failure, never toward a pass:
  - export 15/16 → **14/16** (one *more* leaking individual);
  - G7 "death + description-integrity" → **death only** (the description was intact
    at death; the verdict FAIL 6/16 is unchanged because the completion clause fails);
  - t=347 re-scoped from "long horizon" to "early W/C collapse under B suppression".

Licensed wording is unchanged: *one organism renews its produced exchange boundary
while the admission gate is byte-inert at the intact boundary (G1), admission is
link-specific (G2) and local (G3), and the five internalization mechanisms are
preserved byte-for-byte (G1) and recorded exercised (keep arm).* NOT licensed:
survival-level composition under simultaneous stress.

---

## Sources

`ac115_results_v1/rows.jsonl` (208 rows), `ac115_results_v1/results.json`,
`audit_ac115.py` (G1/G2/G3/G8 pass; G4/G5/G6/G7 fail, retained by design;
`boundary_production_all == false` because of the 6606 leak). No frozen artifact
touched; no study re-run.

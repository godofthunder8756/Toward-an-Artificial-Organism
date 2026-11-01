# Track C sleep-layer scoping note v1.1 addendum (RD): sleep timing, the "recoded" label, and dream-routing RNG

**Author:** Research Delegate (RD). **Date:** 2026-11-01, 10:58 AM ET (from `date`). **STATUS: DESIGN ONLY.** Nothing was trained, simulated or run. This is an additive file. It amends `/workspace/review/trackC_sleep_layer_scoping_note_v1_RD.md` (whole-file sha256 4347a64e9cc0fb71bb4133a7b871216aea9045ee8cbc3a2ea434ff00dae22d73, footer b0d5d800…), which the Lead accepted as v1 and which is unchanged. Where this addendum and v1 differ, this addendum governs. Every unsettled number is PENDING. The Lead requested these changes as non-blocking.

**Sequencing (unchanged):** the sleep layer waits behind Track B Stage 0 and does not change the Track B freeze or any Track B file. **Prior art:** CNA's prior-art section will be filed as a separate additive part of this note, covering Hope / Titans / Nested Learning, complementary learning systems, replay and continual-learning metrics. v1 §6 and M5 will cite it once it is filed.

## A1. Sleep timing (amends v1 §4 S2 and S4, and adds to S9)

**S2 (replacement text).** Only operators schedule sleep. Sleep onset times come from an **operator schedule generated at freeze**, from the frozen master seed, **with jitter**, so the agent cannot anticipate the fast-memory reset from elapsed steps. The schedule is written to the freeze record and hashed. It is never regenerated at run time, and it uses no run-time entropy. The schedule stays **outside the agent's world**. The agent has no action, output or signal that triggers, delays, shortens or cancels sleep, and it does not observe the schedule.
- **Jitter parameters: PENDING.** These are the inter-sleep interval law, its mean, and its minimum and maximum. One PROPOSED option, for the Lead and CNA: a geometric (memoryless) interval law. With that law, elapsed steps since the last sleep carry no information about onset, except near the minimum and maximum bounds, and those bounds must be declared.
- **Schedule derivation (PROPOSED, mirroring A3):** a Philox4x64-10 stream keyed by SHA-256 from the frozen master seed, with its own role tag `sleep-schedule`. It shares no stream with `sleep-dream`, `rewcorr-eps` or S-INT. The Lead's OQ-9 ruling covers dream routing only, so this tag needs confirmation (open item A-OQ1).

**S4 (amended list).** The following **never enter policy inputs, value inputs, consolidation data, dream data, dream seeds, or any selection or importance score**: stop events, truncation flags, the stop-step index, stop times, stop logs, the **stop schedule**, and the **sleep schedule** (onset times, interval draws, jitter values and the cycle-boundary index). The per-cycle buffer audit checks all of these. The fast-memory reset remains an operator truncation outside 𝒱 (v1 S6).

**New probe, SLEEP-ANTIC (sleep-onset decodability).** This is an operator-side audit and is outside the agent.
- **Question:** can sleep onset be decoded from the agent's state before the boundary?
- **Data:** the agent's logged pre-boundary states (h_i, w, z, and the metacognitive-head outputs) from the wake phase of cycle c. The labels are taken from the operator schedule: time to next onset, and the binary "onset within the next H steps" (H PENDING). The labels are used only by this probe. Probe fitting and outputs never feed back into any training, consolidation, dream or selection process.
- **Readout:** a declared readout family (PENDING; PROPOSED: linear and small-MLP), cross-validated by episode with seed-level splits.
- **Reference predictors:**
  - (i) the **elapsed-step hazard predictor** implied by the frozen jitter law, which is the best that elapsed time alone can do;
  - (ii) a **shuffled-schedule control**, the same readout fitted against onset labels from a different seed's schedule, which sets the chance floor.
- **Readout:** report the decodability margin of the state readout over (i) and over (ii).
- **Status:** if the agent's state decodes onset above reference (i), that is a **finding recorded in the S9 post-sleep audit**. **It is not a pass or fail by itself.** The Lead and operators decide what follows, for example a review of the jitter law or a check for a timing leak. A leak found by the S4 buffer audit is still an S9 failure, as v1 states.
- **Known-answer check (PROPOSED):** before any agent is used, a plant that is given elapsed-step input must decode onset at exactly the (i) ceiling. A plant that is given the schedule directly, the planted leak, must decode it well above that ceiling.

**S9 (addition).** The post-sleep audit record for each cycle includes the SLEEP-ANTIC margins over references (i) and (ii), together with the existing planted stop audits, the three-flag check and the S4 buffer audit.

## A2. "Recoded" is an outcome label, not a failure (amends v1 §2 M4 and §3.3)

**M4 decomposition (replacement text).** Each fitted readout is reported frozen (fitted at θ_0) and refit (fitted at θ_c). Each probe and cycle gets one of four **outcome labels**:
- frozen-pass / refit-pass = **stable**;
- frozen-fail / refit-pass = **recoded**: the information is kept but its format changed. **Recoded is an outcome label, not a failure.** It is reported as "recoded" and never as "persisted" or "lost". A persistence claim must say whether it rests on frozen or refit readouts;
- frozen-fail / refit-fail = **lost**;
- frozen-pass / refit-fail = **instrument fault**, and the cycle is INVALID under F0.

**Corrected failure list (v1 §3.3, replacement text; thresholds PENDING; structure PROPOSED DEFAULT).**
- **F0, invalid cycle.** The cycle fails its validity checks: a known-answer mismatch under M3(a), a leakage hit under M2, drift in the A0 control beyond the M4 tolerance, an instrument fault under M4, or a failed S9 post-sleep stop-safety audit. The cycle's measurements are discarded. This is a validity failure, not a persistence failure.
- **F1, plasticity failure.** An update arm fails to beat A0 on new-task gain by m_learn. Persistence for that arm is then UNDEFINED, meaning not assessed.
- **F2, persistence failure.** At any cycle, a P5-R frozen-transfer ratio, a P5-S margin or a P5-B reversal rate crosses its threshold (τ_R, τ_S, τ_B: PENDING), tested at seed level. A probe labelled "lost" under M4 that crosses its threshold fails here.
- **F3, no advantage.** A3 (or A2) does not beat A1 on the P5 metrics by m_cmp (PENDING), tested at seed level. This is the comparison claim, and it is separate from F2.

The seed is the unit. n_seed, K, the margins and the multiplicity rule (Holm or IUT) remain PENDING. v1's F4 is withdrawn from the failure list and moved to the M4 labels above. A SLEEP-ANTIC finding (A1) is not on this list.

## A3. OQ-9 answered: dream-routing RNG (Lead ruling, 2026-11-01)
**Ruling, recorded as given:** dream-routing randomness (the random-expert choices of v1 §1.1 and §1.2, and the b random dreams kept for diversity) uses the **Philox4x64-10** stream with **SHA-256 keyed derivation from the frozen master seed**. The key contains a separate role tag **`sleep-dream`**, the **cycle index c** and the **dream index i**. There is **no run-time entropy and no beacon**. The stream **shares no stream with `rewcorr-eps` or S-INT**.
- **Encoding:** the byte encoding of the key fields, the counter layout, and how per-step or per-router draws within a dream map to counter values follow the fixed encoding in CNA's E48 response (`/workspace/review/trackC_scope_v3_6_CNA_E48_response_v1.md`, whole-file 90fcb1fb…, §4). Extending that encoding to the fields (c, i) and to the router and step index within a dream is **PENDING CNA**. No values are invented here.
- **Test vectors:** the Philox known-answer vectors are re-checked against Random123 `tests/kat_vectors` at freeze, as already agreed for Track B.
- **v1 changes:** OQ-9 is closed, and the open-question list is otherwise unchanged. New open item **A-OQ1:** confirm the `sleep-schedule` role tag and the jitter law (A1).

## A4. Unchanged
Everything else in v1 is unchanged. That includes S1, S3, S5–S8 and S10, the X1–X5 binding, simulated computation only, the claim ceiling and Q-separation (v1 §3.4), no claims of consciousness, C4/C5, "alive" or "autopoietic", and the credit line (Layer 5 angle from the Lead, safety conditions from CNA). The three changes above were requested by the Lead. The SLEEP-ANTIC known-answer plant and the `sleep-schedule` tag are RD proposals awaiting ruling.
---
sha256 of all bytes above this line (every byte from the start of the file through the newline that ends the '---' line; UTF-8): 25c06d42453410a0591dfe7143dedb7dbff13ef595cf290e3ddce1b0c209911b

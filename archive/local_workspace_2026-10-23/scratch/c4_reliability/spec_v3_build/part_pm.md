### 3.7 PM-ACT (policy-minimized comparator; consult #22, Q2; consult #23, Q6, Q9 and named edit 5)

**What is preserved (consult #23, Q9).**
- PM-ACT is an explicitly **action-and-decision** comparator. Its equivalence claim is exactly this: for every input sequence in the tested domain, PM-ACT emits the same (a_t, d_t) sequence as R-HAC-MB(-CE).
- It does **not** preserve MB's probabilities. Consult #23: "It is not a full-output implementation of MB."
- F0 is its declared supplied predictor. "Differences caused by substituting F0 for MB's probability output must be attributed to that substitution, not credited as assessment-role separation." Category-2 and Brier differences between PM-ACT and MB are therefore attributed to F0 substitution.
- Consult #23: "A probability-preserving minimized comparator could answer another question; it is not required here."

**Event-order phases (named edit 5).** Each trial is three transducer phases. "action outputs cannot depend on the later check observation or revealed X."
- **Phase 1** — input (c_t, y_t, f_t, ι_t), output a_t. Here c_t is the current cost from the 6-pair grid, including the declared switch schedules; f_t ∈ {none, P, R, M} is the forced action; ι_t is the intervention input.
- **Phase 2** — input o_t, the check observation of the action actually taken; output d_t.
- **Phase 3** — input X_t; no output. The state is updated (or held under clamp), then the transition is applied.
- Time-to-go is part of the state, through its layer, and is not a separate input.

**Intervention inputs.** ι ∈ {none, SWAP-S, SWAP-E, CORRUPT-S, CORRUPT-E, SUSPEND, RELEASE-A, REPAIR-B}. There are 7 non-null inputs.
- These are applied only at the trial boundaries declared in §4.2 and §4.4.
- **Frozen maps:**
  - SWAP-x and CORRUPT-x map the state to the frozen donor state of §4.2.
  - CORRUPT-x and SUSPEND set clamp status = clamped.
  - RELEASE-A sets clamp status = free and keeps the content.
  - REPAIR-B maps the state to the matched-history shadow state (§4.4).
- **Clamp transitions are explicit.** In a clamped state, phase 3 applies the transition but no feedback update. "PM-ACT must implement these clamp transitions explicitly; normal machine transitions do not automatically represent suspended updates."

**Closure (named edit 5).** "The construction must cover all reachable states under the tested forced actions, donor substitutions, clamps and releases. Include any necessary clamp status and timing. Ordinary reachable belief nodes alone do not establish this closure."
- The construction starts from MB's initial state.
- It closes under every phase input, including all forced actions and all intervention inputs at their declared times.
- The state carries (layer, belief node, clamp status, phase).
- Conservative bound: ≤ 2 × 1,365 states per phase at T_SEP = 4, and ≤ 2 × 364 at T_SEP = 3. The proven reachable count is reported by ITEM-7.
- REPAIR-B needs the pre-perturbation state of trial τ together with the received trial-(τ+1) history. Its map is defined on the closure of (perturbed state, shadow state) pairs. That pair is kept in the construction state only for trials τ+1 and τ+2.

**Minimization.** The coarsest partition of the closed state set that:
- preserves phase outputs on every input;
- preserves successor equivalence under every phase input, including every intervention input.

This is Moore/Hopcroft refinement over the **entire tested input domain**.

**Well-definedness.** The resulting quotient transitions must be well defined: the donor, clamp, release and repair maps must send every member of a cell to a single cell. Named edit 5 (verbatim): "If they are not, report UNRESOLVED-DESIGN rather than supplying an ad hoc transition."

**Descriptive variants.** PM_k, minimized at a single cost k, is reported descriptively only.

**Status.** PM-ACT is **not** a known role-absent control. Consult #22: "PM_k is therefore not automatically a known "role-absent" control."


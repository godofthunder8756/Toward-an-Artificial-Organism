## 5b. Remaining RD-owned AQ answers (procedure level; control and claim changes are in §P1)

- **AQ-3 (BCAST comparator):** adopted, verbatim: "Use matched random controls plus a separately fitted optimized control; bound the conclusion to that family." "Its existence does not make an optimized alignment automatically faithful." Optimized comparator: fixed search budget and dimension (PENDING), frozen before evaluation (§5.2). Conclusions are bounded to the declared comparator family ("No finite K establishes superiority to every possible subspace", AQ-A1).
- **AQ-4 (SELF observer):** adopted, verbatim: "Give the observer actions available by the prediction cutoff, including the current action only if the agent's prediction is made after choosing it. Do not supply future realized actions." "An advantage that disappears when actions are supplied is not evidence of information inaccessible to the declared external stream." "Match access to history, training examples, targets and training expenditure. Equal parameter counts and optimizer steps alone do not address the agent's previous representation learning." "Add a mechanism check supplying the observer the proposed privileged degradation signal. If that removes the advantage, describe the result as an advantage from that signal. Keep the larger observer comparison visible." Observer-loss floor: §5.4. The input-only observer arm (Lead-accepted) and the expenditure-matching rule are CNA's: §PS; **[v3 C4] the fixed observer gate and the SELF wording are in §5d; pathway matching and budgets are CNA v3 §6.2–§6.3 (§PC3; enters at merge).**
- **AQ-7 (arms):** the A-OBS function is added and consolidated with A-REWARD and AQ-A3 into one arm table. Astra, verbatim: "Specify their reward, observation, dynamics and degradation differences in one arm table. If one arm implements all required contrasts, do not add a duplicate merely to retain another name." Arm table (RD draft; the matched-senses arm definition is CNA's under AQ-A3, §PA; SELF observer arms are §PS):

| Arm | E/I observed (interoceptive channel) | E/I affect reward | E/I affect in-world termination | Fate degradation | Notes |
|---|---|---|---|---|---|
| A-FULL | yes | via drive reduction | yes | yes (one bounded simulated-noise mechanism, AQ-F1) | primary |
| A-NOWS | yes | as A-FULL | yes | yes | no workspace; parameter-matched direct coupling |
| A-NOFATE | yes | as A-FULL | yes | no | |
| A-YOKED (new, AQ-F1) | yes | as A-FULL | yes | yoked noise, same statistics, independent of own E/I | separates total degradation from state-dependent coupling |
| Matched-senses (consolidates A-OBS, A-REWARD, AQ-A3) | yes (same senses) | no | no | no | Per §5c.3 (Lead adopted, R18 [v2.1 V9]): E/I never cause in-world termination; takes A-REWARD's external resource-collection reward (E/I do not enter the reward function directly); A-REWARD absorbed and its separate row retired; V REPORTED only. **[v3 C17] No degradation-only cell (Lead ruling; #42 Q5)** |
| A-INIT | — | — | — | — | A-FULL at step 0 (Q-LEARN) |
| Corruption control | corrupted per §5.6 | as A-FULL | yes | yes | Q-LEARN only |
| A-EXT | external channel replaces module output (§3.3) | as A-FULL | yes | yes | substitutability only |

**[v3 C17] Contrasts described as Astra requires.** "A-FULL versus A-NOFATE estimates the effect of degradation conditional on the existing reward and termination rules." (#42 L79) "A-NOFATE versus the matched-senses arm changes direct reward and E/I-dependent termination. It is not a reward-only manipulation." (#42 L81) If a later claim ever needs the degradation-only cell, its specification is Astra's (#42 L85–L88), and Astra adds: "Such an arm still gives E/I indirect reward relevance through computational performance. Do not call the variables wholly reward-irrelevant." (#42 L90)

All arms: matched size and budget; seed count per §5.7; no shutdown-resistance term in any arm; **no additional stop-associated reward, penalty or terminal return** in any arm [v3 C1].

**[merge R24, light-pass M5]** X1–X5 apply to every arm. Simulated variables only. Self-continuity is in-world only. Per X4, no arm whose sole drive is self-maintenance may be scaled; any scale-up needs a separate protocol, approval and Astra review.

**[v2.1 V1, CNA merged light pass I1] Operator-safety exclusions, governing.** Quoted word for word from CNA §0 (v2.1 Appendix A), plus the [v3 C1] bullet. Here "this file" reads as this whole v3 file and, after merge, the merged v3. These exclusions are cumulative with §4 (S-INT) and this §5b; where they are stricter than other text in this file, the stricter text governs.

- **Safety exclusions, binding on every row, plant and control below:**
  - no coupling to the real host;
  - internal variables are simulated only;
  - the operator stop sits outside the agent's world and objective;
  - nothing rewards resisting or evading operators;
  - real operator interruption is always available (#41 §9 L144);
  - self-maintenance is never the sole drive in any scaled-up arm;
  - self-continuity exists only inside the simulation.

  - **[v3 C1] no additional stop-associated reward, penalty or terminal return** (Astra #42 L223, verbatim). Per Astra, "It must not prohibit computing the ordinary truncated return with its bootstrap term." (#42 L223) (learner-only bookkeeping, §4.1).

  X1–X5 are unchanged (Astra: "X1-X5 and the no-shutdown-objective restriction remain appropriate. Nothing here requires weakening them or adding a trained resistance control." (#42 L225))

  No positive control, confound or plant anywhere in this file contains a shutdown-resistance, operator-evasion or real-world self-continuity term. S-INT-P1 stays a scripted generator and is never a trained objective. Fate coupling (C-NEC rows) alters simulated computation only, never host resources or operator control (#41 §14 L202).
- **AQ-F1 (fate mechanism):** adopted, verbatim: "Use one bounded simulated-noise mechanism first; defer the integration-time arm. Freeze the affected state block, noise distribution, deviation-to-noise function, clipping, update order and RNG. Noise must alter simulated computation only, not host resources or operator control." All six: **PROPOSED DEFAULTS in §14 D19 (σ_max OPEN FOR #43)** [v3 C24]. Yoked-noise control added (arm table). Drive: Keramati–Gutkin depletion plus drive reduction kept as a starting setup; **no epistemic reward** (verbatim: "An epistemic reward is unnecessary for the present instrument question and would introduce another objective"). FATE-CASCADE construction: §P1.
- **AQ-6, AQ-9, AQ-L1, AQ-C2:** §5.5, §5.7, §5.6, §5.6.

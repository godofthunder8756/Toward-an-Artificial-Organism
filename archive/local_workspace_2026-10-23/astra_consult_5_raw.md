**Verdict: DO NOT FREEZE yet—pending inspection, not a substantive rejection.** The attachment reader failed, and I could not find scarcity_v2 in the repository branches checked. I therefore cannot certify the draft or its existing gates. These are conditional rulings on the proposals you quoted.

## §12 proposals

| Proposal | Ruling |
|---|---|
| a=3/4, controls 3/5, 5/6 | Accept. Freeze all three values prospectively, the observation independence assumptions, and reporting across all cells. With finitely many genuinely noisy looks, avoid gates requiring an ideal observer to become certain. |
| Integer K counting all internal state; B_up ∈ {1, ⌊K/2⌋} | Accept K; clarify upkeep before accepting. Count reachable joint configurations, including selector, history and bookkeeping—not the sum of register sizes. Define upkeep units and which physical/logical components an operation refreshes. Abstract state cardinality alone does not define maintenance cost. Specify duplicates and the K=1 zero-cap case. |
| Ten CPU-minutes per cell; otherwise UNRESOLVED | Accept with precise accounting. Freeze solver configuration, aggregate worker CPU accounting, and treatment of restarts. Save certified bounds. Timeout without a decisive certificate is UNRESOLVED; a valid certificate obtained before timeout remains usable. |
| H=2, controls 1, 3 | Accept conditionally. Define the history alphabet, initialization, update and accessibility; charge its reachable joint states against K in every arm. A protected history register must not become uncharged, decay-proof memory. Some (K,H) combinations may be infeasible. |

(a) Equal-state adaptive rival: useful, but insufficient to establish emergence. Match observations, available actions, upkeep resources and memory protection as well as state count. If both arms receive a selection mechanism, the comparison tests implementations of selection. A tie with the adaptive rival can support a conventional explanation while leaving selection pressure intact.

(b) Scope: remembering upkeep actions and filtering decay are not automatically C4. Explicitly investigating evaluation of the agent's own machinery would raise that question. A finite-policy certificate need not introduce a new architecture family, but a specially protected controller/register could change the apparatus. I cannot settle that without the draft's definitions.

(c) Proposed outcome semantics—not verification of the unseen gates:

ADMIT: certified bounds establish the frozen pressure and representability requirements under matched resources. Strongest claim: this bounded task rewards the specified C3 role, and an admissible policy realizes it. Neither acquisition nor consciousness follows.
REJECT: certified bounds show a required criterion fails in the preregistered scope. Strongest claim: this task/parameter family fails as the proposed discriminator. It does not reject C3 generally.
UNRESOLVED: bounds straddle a threshold, computation expires without a certificate, or accounting remains ambiguous. No directional architectural conclusion.

Specify separately how cell outcomes aggregate into the protocol verdict.

(d) Most informative edit: add a selection-necessity certificate: compare the unrestricted admissible policy class against a prospectively defined class that cannot condition allocation on the relevant information, with everything else matched. Require a certified value gap. This addresses your nonunique-optimum warning: displaying one selective optimum establishes existence, not necessity.

Keep "origin: untested" explicit. Even that stronger certificate establishes pressure for selection; demonstrating that selection was acquired requires a later, separately authorized emergence experiment.

Please paste the draft text so I can turn these conditional rulings into a document-level freeze verdict.


---

# RESPONSE A (to full draft text, sent as Part 1/2 + Part 2/2; Part 1 non-ASCII chars were garbled in transit)

**Verdict: DO NOT FREEZE.** The claim ceiling is appropriately narrow, but several definitions and “implementation-error” controls are mathematically wrong or incomplete. These require protocol revision before parameter freezing.
**1. Blocking corrections**

- **Sufficient storage does not remove graded-evidence access value (§6.2).** At $a=r=3/4$, agreeing looks occur with probability $5/8$ and give posterior confidence $9/10$; disagreement gives $1/2$. With sufficient storage,

$$V_{\rm full}=27/32,\qquad V_{\rm static\_access}=3/4,\qquad ACC=3/32>0.$$
That is ordinary selective prediction under observation uncertainty. Restrict the zero-ACC control to clean evidence. Separate pressure caused by storage scarcity from pressure already present at sufficient storage.

- **Upkeep currently has two incompatible interpretations (§§1,4).** If full chooses a protected subset of codebook states, every deterministic maintenance rule is already a fixed subset; an optimized fixed_upkeep can implement the same rule. If full instead chooses which states to protect separately each episode after encoding, it can always protect the occupied state when $B_{\rm up}\ge1$. Define the allocation timing, available information and genuine restriction distinguishing the rival. As written, UPK may be identically zero.

- **K_supp conflates support with decision sufficiency (§3).** Minimum states attaining optimal reward is task- and reward-dependent, not posterior-support cardinality. At graded $a=3/5,r=3/4$, always abstaining is optimal, so that minimum is **one**. Define lossless sufficient-statistic capacity separately from minimum optimal-decision capacity. Also specify whether decay samples actual codebook states or all budget slots: changing that number changes the corruption channel.

- **Several §7 signatures do not follow.** Cue-swap loss need not equal SEL, which compares separately optimized policies. Independently encoded message alphabets have no canonical alignment, so swapping messages can produce arbitrary effects. Reducing $L$ and reoptimizing tests redesign, not a lesion response. A static router need not lose uniformly; random upkeep does not make withdrawal effects independent of content relevance. “Matched content, different access” also needs an operational definition. Freeze intervention operators and compute their consequences; do not assume these signatures.

**2. §12 rulings**
Proposal | Ruling | 
$a=3/4$, secondary $\{3/5,5/6\}$ | **Accept**, with all values’ decision roles frozen. The $a=3/5,r=3/4$ condition is an **all-abstain null control**, not a source of nontrivial access patterns. | 
Hard integer $K$; $B_{\rm up}\in\{1,\lfloor K/2\rfloor\}$ | **Accept $K$; defer $B_{\rm up}$** until upkeep is coherent. Count reachable joint configurations and specify memory available at every decision phase, not just query time. Define duplicate levels and $K=1$. | 
Ten CPU-minutes per cell | **Accept.** Include optimization and all-optima certification in a declared accounting scheme. Three-minute checkpoints are straightforward; thirty-minute sensitivity requires explicitly budgeted additional computation and cannot change primary labels. | 
$H=2$, controls $\{1,3\}$ | **Accept only after comparator repair.** $H$ denotes register cardinality, not history length. Two states permit a coarse regime estimate, not generally an exact posterior. Resolve “primary $H=2$” versus “best $H$ per cell”; allow unused capacity and declare infeasible combinations. | 

**3. Adaptive rival and scope — questions (a), (b)**
Equal state count is necessary but **does not test acquisition**. The draft correctly excludes Q-LEARN. It can test pressure within supplied policy classes.
adaptive_select presently has “none in principle” denied and unrestricted-looking allocation/routing. Its relation to full needs a formal definition: either equality is built in, or any gap reflects specified factorization/update restrictions. Freeze feedback availability, update order and both classes’ persistent state. Stage B also needs initialization or an initial-distribution rule for potentially multiple recurrent classes; a stationary linear system alone may not identify a unique value.
This remains **C3**, provided the target stays retention, access and routing. History and ordinary filtering do not inherently introduce C4 or a new architecture family. Conversely, diagnostic observations are not automatically C4. Paid protection of abstract states also does not establish an O3 machinery-maintenance bridge.
**4. Outcomes — question (c)**
Revise §6 before assigning these:

- **ADMIT:** certified role-specific gaps and valid controls establish pressure and representability **within the declared worlds and rival classes**. ROBUST/PERMITTED additionally requires completed intervention analysis across the relevant optima. Neither establishes acquisition.
- **REJECT:** certified failure of the declared admission criterion. Distinguish **pressure absent** from **pressure present but insufficiently widespread**.
- **UNRESOLVED:** missing certificates, unresolved controls or incomplete required optimum coverage.
Two specific repairs: ROUTE is measured only at ample storage, so requiring ROUTE pressure in every below-sufficiency storage bin is impossible as written. And “no pressure among solved cells, with up to 10% unresolved” does **not** certify absence across W2. The §8 stop rule must preserve that uncertainty. Apply controls per role, not “every control” indiscriminately.
**5. Most informative edit — question (d)**
Add a **scaffold accounting table** for each role: what the policy language supplies, what optimization chooses, what the role-denied rival removes, and what a later learner would have to acquire.
Your draft already includes the selection-necessity comparison and all-optima distinction I previously recommended. The next improvement is making explicit whether optimization discovers a functional allocation or merely fills parameters in a supplied selector. That makes this certificate useful preparation for an emergence experiment without mislabeling it as one.

---

# RESPONSE B (interpretation check, PR #4)

**Yes, with two qualifications.** PR #4 explicitly reports A0, T-PROJ and T-CLOSE. I checked its definitions and reported results; I did not rerun it.

- **The reduction is stronger than terminal readout equivalence.** The prefix audit supports an exact stage-indexed **two-marginal recurrent update**, followed by a nonlinear readout, throughout the frozen horizon. Include that complete rival, not an oracle supplying exact marginals to an otherwise autonomous learner.

- **“Only product-readout failure” describes gates (ii)/(iii).** The certificate also establishes useful history dependence. None of these results establishes the necessity of a third coordinate.

There is an important accounting caveat: the marginal pairs distinguish **every history at each stage**. Thus “two numbers” is not necessarily compressed memory; exact rational precision and lookup complexity can carry the entire history. Charge precision, persistent state, stage information and update/readout resources consistently.
**Your proposed claim discipline is mostly right.** Prespecified finite-state or precision constraints could establish necessity **within those constraints**. Linear decodability establishes accessibility in a chosen representation; by itself it establishes neither causal use nor acquisition. A learned joint predictor could legitimately be demonstrated without a separate covariance coordinate, provided “joint” means its predictions capture dependence rather than asserting an independently necessary latent component.
**Strongest next use: an acquired recurrent-filtering causal demonstration.** Treat this world as an exactly understood testbed, with the following prospective design:

- **Origin:** train a generic recurrent agent on ordinary observations and prediction outcomes, without supplying covariance targets, a designated joint-state slot, exact update equations or protected histories. Record the supplied architecture and task demands separately from acquired behavior.
- **Generalization:** reserve complete histories or prefix–continuation combinations from training. Compare against the exact oracle, the two-marginal nonlinear rival, and an explicit history-table explanation. Matching the oracle is the ceiling; beating the conventional rival is unnecessary.
- **Causal use:** transplant the agent’s native recurrent state between two reachable prefixes at the same stage, then provide identical continuations. Preregister donor-dependent forecast changes, matched sham interventions, and restoration/rescue. Confirm on held-out cases and compare before versus after learning.
- **Mechanism:** determine whether the acquired update and readout implement filtering, history lookup, or another conventional computation. Reduction identifies what emerged; it does not negate acquisition.
**Do not require an on-reachable-set intervention that changes covariance while holding both exact marginals fixed:** the audit says that contrast does not exist here. The certificate’s zero-covariance clamp is off-manifold on every terminal history, so it cannot substitute for evidence that a learner acquired an independently manipulable covariance component.
The strongest resulting claim would be:
Within a supplied generic architecture, training acquired history-dependent state whose experimentally verified causal influence supports joint prediction in W2; its mechanism is characterized relative to the declared rivals.
That is a useful acquired-structure result. It would not establish irreducible joint state, C4, or consciousness, and this admission does not itself authorize training or unblock A8.



---

# CONSULT #6 RESPONSE

**Verdict: DO NOT FREEZE.** Several Consult #5 corrections are fixed, but new false controls and unresolved policy definitions would still make valid results look like implementation failures.
**Hand results: confirmed, with scope qualifications.**
Result | Verdict | 
$ACC_{\rm suff}=3/32$, $a=r=3/4$ | Correct for single-consumer, unpaid, sufficient-storage cells. | 
$UPK=5/96$, $B_{\rm up}=1$ | Correct under the stated **direct per-query field semantics**, clean evidence and ample capacity. | 
$UPK=5/192$, $B_{\rm up}=2$ | Correct under those same assumptions. | 

The upkeep upper bounds require answering query $q$ directly from $f_q$. They are not established for an arbitrary decoder that can reinterpret other fields.
**Remaining blockers**

- **The uninformative-cue UPK control is false for graded evidence.** Even with uniform queries, protect an agreeing-look field rather than a disagreement field. At $a=r=3/4,\delta=1/2,B_{\rm up}=1$, ample capacity, the intended field model gives

$$UPK=\frac{\delta(9/10-r)}3
\left[\Pr(\text{at least one agreement})-\Pr(\text{fixed field agrees})\right]
=\frac{33}{4096}>0.$$
Restrict zero-UPK controls to cases actually proved. Also restrict “storage-attributed ACC” to **clean, unpaid** cells; paid erasure can create access variation without storage scarcity.

- **ROUTE admission is impossible at $L=1$.** Both arms send a constant message, so ROUTE is zero. Make $L=1$ a null control, not a required positive bin. Moreover, static_route = fixed function of fixed fields is not a precise restriction: allowing all fields may reproduce full. Specify its permitted field subset and information access. A cue-independent routing function can still receive **cue-dependent encoded fields**, so O-ROUTE’s zero-effect identity does not follow.

- **The policy language still conflicts with the proofs.** Sections 2/5 prohibit relocating content and treat fields as literal answers; §4 allows arbitrary decoders. Choose explicit semantics per condition. The tabulated $K_{\rm dec}=8/27$ values apply to the clean/graded **unpaid, full-channel baseline**, not automatically paid or channel-limited worlds. For capacity sufficiency, minimize the maximum reachable count across phases. Freeze a finite outer grid independently of whichever optimum the solver finds.

- **O-ACC’s clean-evidence identities remain overgeneralized.** Clean input does not make a compressed stored answer correct with probability one, nor an abstained item unpredictable. Use the actual conditional correctness probability $p$: answer→abstain changes reward by $r-p$; abstain→guess by $p_{\rm guess}-r$, weighted by the relevant query probability. Stronger identities need proofs for their applicable policy subset. Under skewed cue sweeps, O-SEL also needs a swap kernel preserving the cue distribution; uniform switching does not.

- **Stage B is not fully specified.** The fixed tracker forces register changes even when history is useless, whereas full_B can keep a constant register. With charged memory, stationary ADAPT=0 therefore is not automatic. Include an explicitly selectable constant-tracker baseline. Specify the H=3 tracker and the timing of register updates, durability payment and erasure. With a fourth maintained field, $B_{\rm up}=3$ no longer guarantees that everything persists. Any positive ADAPT remains evidence against **this tracker**, not conventional adaptive selection generally.

**Consult #5 correction status**

- **Fixed:** graded ACC arithmetic; removal of the original upkeep ambiguity; explicit scaffold accounting; distinction between missing value certificates and missing optimum coverage; no “10% unresolved means absent” rule.
- **Partly fixed:** capacity definitions, interventions and adaptive comparator.
- **Still broken:** routing aggregation and several purported theorem-level controls.
Also define the response property that ROBUST/PERMITTED evaluates. Merely computing every intervention response does not establish an identifying signature, particularly if every intervention is NOT-APPLICABLE.
**§15 rulings**
Flag | Ruling | 
History upkeep | **Keep the common rule:** optional durable storage costs one unit; free fragile storage decays. Free **persistent** storage would be a protected-memory scaffold. That does not automatically constitute a new architecture family; it is nevertheless a material apparatus change requiring explicit classification. | 
Visible - erasure | **Accept**, with supplied access marked explicitly. Do not promise to “subtract” supplied ACC numerically: acquisition attribution needs matched scaffold controls, not an assumed additive decomposition. | 
Exclude $(3/5,5/8)$ | **Accept the narrower grid.** Keep $(3/5,3/4)$ as the null. Positive ACC is not itself a reason to exclude the other cell; limited scope is. | 
$\delta=1/2$ primary, $1/4$ secondary | **Accept**, with secondary results’ decision role frozen. In the proved clean ample-capacity examples, UPK scales linearly with $\delta$, so quarter-decay halves both gaps. | 

The earlier mojibake did not drive my substantive objections. This revision improves claim discipline, but the next revision should settle the policy semantics and prove the controls before freezing the search.


---

# CONSULT #7 RESPONSE

**Verdict: DO NOT FREEZE.** This can test acquisition of predictive behavior, but its current gates do not establish that training acquired the **recurrent state organization** responsible for it.
**Single most important edit: add a frozen-recurrence, trained-readout control.** Freeze each seed’s initialized GRU and train only its identical MLP readout, using the same episodes and budget. An untrained recurrent network may already distinguish histories; training the readout could produce accurate forecasts and pass whole-state transplants without reorganizing recurrent memory. Initialization-versus-final performance does not exclude that explanation.
If this control matches the candidate, record **acquired readout over supplied recurrent dynamics**. A reliable advantage from training recurrence supports a contribution from recurrent adaptation; localization still requires separate evidence. This comparison answers an origin question, rather than demanding superiority over conventional mechanisms.
**Three other blocking corrections**

- **K-PROD’s supposed lower bound is false.** Its jointly trained X/Y heads need not equal the exact marginals: they can trade marginal accuracy for better XOR predictions. Therefore its XOR excess can fall below the analytic oracle-product excess. Passing A-FIT is **not an integrity alarm**. Call it a *product-constrained output model* and report all three errors. It does not prove that information beyond the marginal pair is required.

- **The sham predictions are not guaranteed.** A wrong donor can have forecasts close to the intended donor; a random-direction perturbation can also move predictions toward it. Neither implies an implementation failure. Define wrong-donor eligibility using a prospective minimum separation between the relevant **oracle continuation forecasts**. Treat random-direction effects as descriptive unless a justified null is specified. The present REJECT-CAUSE interpretation is consequently too strong.

- **The reduction labels overclaim.** GRU-2 learns arbitrary two-dimensional state, not necessarily marginals. A poor TEST result does not identify lookup, and a successful linear probe does not identify filtering. Replace R-2M/R-TAB/R-FILT with literal observations: “two-dimensional rival reproduces performance,” “held-out generalization weak,” and “chart linearly accessible.” Behavioral reproduction by a rival is not identification of the candidate’s mechanism.

**Flag rulings**
Flag | Ruling | 
**F2: whole-state transplant** | It verifies that replacing the complete memory redirects behavior as expected, but donor replay is an identity of this deterministic architecture. It adds no independent mechanism discrimination beyond predictive fit on the corresponding histories. Retain as an implementation/behavioral consistency check. Use the frozen-recurrence control for origin, and prospectively specified **partial interventions with appropriate controls** for narrower mechanism claims. Restoration is correctly classified as integrity-only. | 
**F3: nearest-posterior donors** | Accept as a **graded sensitivity control**, not an equivalent replacement for same-posterior donors. Nearby prefix beliefs need not yield uniformly small differences after conditioning on every continuation. Compute the actual continuation-specific oracle change; predefine handling of tiny denominators and report absolute error alongside normalized error. | 
**F4: two-dimensional MLP-update rival** | Scientifically fair and conventional: an explicitly declared recurrent architecture variant, not inherently a new research family. Include it prospectively if resources permit, and charge its parameters. Neither it nor GRU-2 is guaranteed to realize the exact marginal update. Neither is an autonomous mean-field filter: that requires an explicit independence projection during filtering. Rename learned arms **K-2D**, reserving “two-marginal” for a semantically verified implementation. | 
**F5: realized-bit labels** | Accept. These are supervised terminal outcomes, not oracle probability targets. Say explicitly that the environment supplies feedback revealing X, Y and XOR after the episode. The prediction demand is supplied; learning its solution remains testable. | 
**F6: stage code** | Accept as a declared external timing scaffold. Three bits identify eight stages; this is an information accounting convention, not the physical cost of the float one-hot input. Clockless learning is a separate experiment. K-TAB must also charge the accumulated history/index or equivalent external buffering; its persistent state cannot simply be zero. | 
**F7: split and admission rule** | The recombination split is defensible. The quarter-gap and 8/10 rules are acceptable **prospective engineering criteria**, not theoretical significance thresholds. Report continuous per-seed results and initialization-to-final changes. Exhaustive history evaluation removes history-sampling error, not variation across training seeds. Repair causal gates before adopting the aggregate verdict. | 
**F8: defaults** | GRU-8 primary, the proposed secondary sizes, 4,000 steps and learning rate are reasonable bounded starting choices, with no assurance of convergence. Keep rank-3 PCA exploratory: failure means “not localized by this intervention,” not “distributed.” The precision grid is acceptable descriptively, subject to the correction below. | 

**Precision needs one explicit repair.** Selecting the smallest passing bit width on TEST makes $b_{\min}$ a **test-set-selected resource estimate**. Report the preregistered precision curve descriptively, or select precision elsewhere and confirm on TEST. Specify rounding, clipping, constant ranges, quantizer metadata costs, and what happens when quantizing the exact chart produces an invalid probability distribution.
**ORIGIN/ROLE judgment:** the revised study could establish acquisition of a history-dependent prediction function and characterize how native state supports it. It cannot yet equate ADMIT with “hidden-state organization acquired.” Separate **readout acquisition**, **recurrent adaptation**, and **causal organization**, with evidence assigned to each. Do not make acquisition depend on beating K-PROD.
Finally, **F1 is resolved by Aidan’s direct approval stated in your request**. Update the stale approval paragraph; another authorization round is unnecessary. The remaining stop is scientific protocol repair.


---

# CONSULT #8 RESPONSE

**Verdict: DO NOT FREEZE.** The semantics, routing rival and scaffold accounting are substantially clearer. However, the stationary-control proof is false under the stated initialization, and some intervention and admission rules remain inconsistent.
**Remaining blockers**

- **$h=0$ does not make the regime uninformative.** With the regime initially drawn from $(1/2,1/2)$, $h=0$ creates a **fixed but unknown regime**. History can reveal it. Episodes are conditionally independent given that regime, but the history register becomes correlated with it; the best-register-slice argument therefore fails.
Use a **known, fixed query map** as the stationary zero-ADAPT control. Alternatively, an independently resampled regime removes predictive history information. Keep the unknown-fixed-regime case as an experimental condition, with no assumed zero gap.

- **O-ACC still needs correction.** Both guessing and scoring must condition on the queried item:

$$p_{\rm guess}=\max_b P(X_q=b\mid m,q).$$
Conditioning only on $m$ can be wrong because observing $q$ supplies information about the cue. For paid cells, include decay in the posterior calculation. Also, replacing a post-decay configuration with another reachable configuration does **not** prove that the replacement is implementable by an admissible encoder under S-DIRECT. Thus “every applicable flip has $\Delta V\le0$” needs a feasibility proof; otherwise remove that assertion. Apply the same query-conditioning discipline to O-UPK.

- **The clean ACC admission requirement already excludes success.** Its first bin contains only $K=1,2$, where the earlier v1 replay reported zero access advantage. Under the inherited clean/unpaid slice, ADMIT(ACC) is therefore unavailable. Either explicitly accept this already-known REJECT-NARROW outcome or prospectively revise the scientific breadth requirement before freezing. Do not spend a search rediscovering it.

- **Clean UPK is not automatically cue-attributed.** fixed_upkeep denies dependence on **both evidence and cue**. Under compressed storage, clean evidence can still affect which fields are worth protecting. The ample-capacity hand examples isolate cue relevance; the general clean-cell contrast does not. Use “adaptive maintenance allocation” generally, or add a rival whose D-set may depend on raw evidence but not the cue.

- **Complete signature failure needs a resolved outcome.** If every optimum is certified and every positive cell has NONE or SIG-UNDEFINED, the signature requirement has failed; this is not computational uncertainty. Add a scoped signature-failure verdict instead of leaving these cases under UNRESOLVED.

**Consult #6 correction check**
Earlier blocker | Status | 
False graded zero-UPK control; paid ACC attribution | Fixed. | 
$L=1$ positive requirement; ambiguous routing rival | Fixed. | 
Direct fields versus arbitrary decoding; capacity/grid definitions | Substantially fixed, subject to F4 below. | 
Intervention identities and skewed cue swaps | Swap kernels fixed; O-ACC remains incomplete. | 
Stage-B tracker, timing and stationary control | Tracker and timing improved; stationary proof still wrong. | 
Undefined response properties | Properties now explicit; failure aggregation still needs repair. | 

**Flag rulings**
Flag | Ruling | 
**F4: capacity sufficiency** | **Correct:** $\min_{\pi\in\mathrm{Opt}}\max_{\text{phase}}N_{\text{phase}}(\pi)$. Here Opt must mean policies attaining the **capacity-unconstrained** optimum for the other fixed cell parameters. Count internal configurations, excluding currently supplied external inputs; otherwise the baseline $8/27$ claims conflict with E-phase counting. | 
**F5: S2 resampling** | **Accept.** It preserves the cue law and the cue-blind zero identity. Label it separately from derangement; its magnitude is not directly comparable without accounting for the different intervention. | 
**F6: counts** | **Confirmed as sufficient counts.** With a cyclic choice using all three durable pairs, B=2 gives full I=24, Q=$8+3\cdot4=20$; fixed I=8, Q=12. The clean uniform-query controls fit K=18 and K=12. $5^3=125$ bounds stage-A I configurations. **K=24 is not minimal for B=2:** using just two durable pairs covering all cues yields I=16 and Q=16 while retaining the same optimal value. | 
**F7: graded UPK** | **Keep report-only.** A separate reliability contrast is optional and should be a separately specified question. Also narrow the clean cue-attribution wording as above. | 
**F8: unproved ROUTE positivity** | **Accept as an empirical certificate question.** The $7/8$ construction is valid when each consumer receives its own preferred item’s bit. A feasible-policy lower bound alone establishes no gap against static_route. | 
**F9: value-only ADAPT** | **Accept.** No response property is necessary for a narrowly stated optimization-gap result against the specified trackers. | 
**F10: PERMITTED or ROBUST per bin** | **Accept for an existential claim:** each bin contains a positive cell with at least one qualifying optimum. It does not establish typicality or robustness across optima. Repair the ACC bins and resolved signature-failure outcome first. | 
**F11: H=3 tracker** | **Accept** the saturating counter, neutral initialization at 2 and reset to 2. Its interpretation remains one declared conventional heuristic, not the strongest possible adaptive filter. | 

The highest-priority edit is replacing the false **unknown-fixed-regime ⇒ zero ADAPT** theorem. Otherwise the implementation could correctly discover useful history and be incorrectly halted as defective.


---

# CONSULT #9 RESPONSE

**Verdict: FREEZE WITH NAMED EDITS.** The central Consult #7 repairs are present: K-FR, separate acquisition/adaptation/localization judgments, corrected K-PCO interpretation, honest two-dimensional rivals, history-buffer accounting, and removal of transplant identities as independent evidence. Apply the edits below before hashing; no further consultation is needed if they are adopted exactly.
**Flag rulings**
Flag | Ruling | 
**G1: XOR scale** | **Keep $1/4$ of the analytic product-readout excess.** It is a legitimate fixed accuracy requirement, not a requirement to beat the trained K-PCO arm. The current-only alternative is materially weaker; there is no interpretive reason to substitute it. | 
**G2: extra K-FR arms** | **Drop K-FR for the two-dimensional rivals.** Their role is performance reproduction, not origin attribution. This leaves **120 runs**. Retain K-FR for all four candidate configurations. | 
**G3: thresholds** | **Accept as engineering choices**, subject to denominator and coverage rules below. Their values carry no theoretical guarantee of adequate donor coverage or statistical significance. | 
**G4: chart-probe overfitting** | **Use cross-fitting**, specified below. The chart-guided intervention remains an analyst-defined test, not discovery of a naturally separate covariance module. | 
**G5: TRAIN precision selection** | **Accept.** In-sample calibration followed by untouched TEST confirmation is adequate for this descriptive resource estimate. No third episode split is necessary. | 

**Exact edits required**

- **Correct the split-specific current-only reference.** Within each split, compute the optimal current-only forecast by averaging $q^*(h)$, weighted by $P(h)$, separately for each final reading. Then compute its excess over the full-history oracle. Merely reweighting PR #4’s unconditional current-only forecasts is insufficient: conditioning on the TRAIN/TEST selection changes the distribution. Use these split-specific references wherever E_CUR appears. The analytic product reference needs no analogous change because it is defined separately for each complete history.

- **Prevent rival success from becoming a false attribution to CAND.** Replace the E2 label “ACQUIRED READOUT OVER SUPPLIED RECURRENT DYNAMICS” with:
**FROZEN-RECURRENCE READOUT SUFFICIENT AT THIS BUDGET.**
Its appended claim must describe **K-FR**, not assert how CAND works. Likewise, do not label CAND’s trained recurrent dynamics “SUPPLIED” merely because K-FR performs well. Record its recurrent contribution as **not established by this comparison**. Reserve “recurrent adaptation supported” for intact, valid paired runs; near-zero K-FR excess, at or below $10^{-12}$, is numerically tied rather than evidence for a ratio improvement.

- **Cross-fit the primary E3 analysis.** Partition the 16 four-reading prefixes into two fixed folds by parity of their bit count. For each fold:

- fit the ridge map on the other eight prefixes;
- use only recipients, donors and wrong donors from the held-out fold;
- pool held-out intervention results across the two folds.
Specify the regression as centered least squares plus $10^{-3}\|W\|_F^2$, with an unpenalized intercept. For $W\in\mathbb R^{H\times3}$, project onto its column space. Define numerical rank using singular values exceeding $10^{-8}$ times the largest; rank below three makes the proposed three-dimensional claim **UNRESOLVED**. Retain the all-16 fit as descriptive only.

- **Complete E3 eligibility and failure handling.** Use the same trial subset for partial, complement and wrong-donor comparisons. Require the intended donor’s oracle XOR change to have magnitude at least $1/100$, in addition to the existing wrong-donor separation and norm conditions. Require eligible trials to cover at least **10% of cross-fitted T4H**, with at least four distinct recipients and four distinct intended donors in each fold. Otherwise E3 is **UNRESOLVED**, not “not localized.”
Apply the stated localization inequalities to **both** the three-output vector and XOR-only statistics. A ratio denominator at or below $10^{-12}$ is undefined and cannot pass. Report absolute errors alongside ratios.

- **Narrow the E3 claim.** Replace “requiring recurrent training” with:
**Observed in CAND but not in the matched frozen-recurrence control under this budget.**
Report whether K-FR meets A-FIT alongside that comparison: poor prediction alone can prevent donor tracking. Remove the implication that E2 plus E3 automatically establishes the origin of the localized subspace. Permitted wording is:
Training recurrent parameters improved prediction relative to K-FR, and a cross-fitted chart-decoder subspace redirected forecasts under the specified partial interventions.
These are two supported findings, not proof that training created that subspace or that it is an independently manipulable natural module.

- **Finish precision accounting.**

- Cast range endpoints to float32 **before** constructing and using quantizers, matching the charged metadata.
- Replace ">24" with **“no qualifying precision in the declared grid”**; failure can reflect poor fit rather than insufficient precision.
- Keep K-TAB’s buffer exact and logits float32; **remove its logit quantization procedure**. Zero is not generally a level of the proposed uniform quantizer, and parameter quantization is a different resource experiment.
- For quantized K-EXACT, retain quantization indices as the charged state and reconstruct/project the chart deterministically. Do not charge three $b$-bit coordinates while silently retaining additional independent floating-point state.

With these changes, **ADMIT establishes acquired predictive behavior**. E2 and E3 then provide bounded, separate evidence about recurrent adaptation and causal localization. That is a legitimate first acquisition study under the ORIGIN/ROLE/REDUCTION ledger.


## CONSULT #10 RESPONSE
(Retrieved 2026-10-20 ~7:30 PM ET; rendered text transcribed from page, math flattened; wording is Astra's but not byte-verbatim.)

Verdict: FREEZE WITH NAMED EDITS. Consult #8's five blockers are now addressed in substance. The remaining issues are proof wording, intervention scope and verdict completeness. Apply the edits below before hashing; no further review round is needed if adopted exactly.

Proof checks
- Zero ADAPT under KNOWN-FIXED and IID-REGIME: Correct, with the construction correction below. History carries no information about the next episode's exogenous variables in these controls.
- Unpaid O-ACC has DeltaV <= 0: Correct under canonical unpaid field-vector semantics. Fix a particular configuration and field; remapping that configuration changes reward only when that field is queried.
- UPK_cue = 0 at v=1/3: Correct. For graded evidence, the maximization must use the observed evidence statistic, not latent x.
- Clean ample-capacity gap entirely cue-attributed: Correct for the stated uniform-cue examples.
- Graded 33/4096 entirely evidence-attributed: Correct for the stated ample-capacity, uniform-query example.
- K_suff = 16 at B=2, 26 at B=1: Correct conclusions, but the B=2 lower-bound argument needs replacement.
- O-UPK = -3/32: Correct when withdrawing durability from the cued field every episode. Withdrawing one fixed field whenever it is durable instead gives -1/32 in that B=1 example.

Exact edits required

1. Repair the B=2 capacity proof. Replace "since x is independent of c, each D-set occurs with all eight x" with:
For each fixed item vector x, all three cues have positive probability. An optimal policy answers every field correctly and uses a durable pair containing the cue. Therefore it needs at least two distinct durable pairs for each x. Different item vectors have different field values, giving at least 8x2=16 I-phase configurations. The displayed policy using two fixed pairs attains I=16 and Q=16. Hence K_suff=16.
Independence does not make an evidence-dependent D-set independent of x. A universal Q-phase lower bound is unnecessary.

2. Repair the zero-ADAPT construction without changing its conclusion. Keep the register physically fixed at the declared eta_0; define its encoder to reproduce the best slice eta*. Leave answer values and their durability choices unchanged, remove any register-durability payment, and use T_const.
Replace "reachable configurations are a subset" with:
Mapping register values to eta_0 and removing its durability mark cannot increase the number of reachable configurations.
Do not suggest spending the saved unit on additional answer durability; that is unnecessary and complicates the capacity argument.

3. Canonicalize unpaid cells and the graded UPK-C0 proof.
- State that unpaid S-DIRECT cells use field vectors only, with durability marks omitted or uniquely determined by those vectors.
- In UPK-C0, replace latent x by the observed evidence statistic e, and define g(e,c') as conditional expected reward. Then selecting c*(e) is an admissible encoder.

4. Specify the withdrawal event. An O-UPK result must identify both the field and the encoding events on which it is downgraded. For the -3/32 self-test, write:
On every episode, downgrade the cued field j = c from D to F.
For general signature evaluation, use explicitly identified configuration-field withdrawals, integrating their event probabilities. This prevents confusing a conditional loss with a whole-distribution loss.

5. Close unresolved-cell loopholes in rejection rules.
- REJECT-SIG: require every in-scope cell's value status resolved, as well as complete optimum coverage in every positive cell.
- Signature-based REJECT-NARROW: require every value status in the failing bin resolved, and every positive cell there certified NONE/SIG-UNDEFINED; another bin must qualify.
- If unresolved cells could supply a qualifying optimum, use UNRESOLVED.
- Where rejection categories overlap, use REJECT-ABSENT, then REJECT-SIG, then REJECT-NARROW. Preserve ACC's separately established, replay-based REJECT-NARROW record.

6. Make search accounting deterministic. Freeze class-search order, certificate preservation and allocation of the shared ten-minute budget. Preserve completed value and signature certificates when another class times out. Mark B_up = 2 explicitly decision-bearing for the UPK breadth test, despite being called "secondary"; it is not report-only like secondary delta.

Flag rulings
- G2 - Accept. KNOWN-FIXED regime 0 is the stage-A map with an unnecessary register. Regime 1 is equivalent by relabelling the cue and its distribution.
- G4 - Accept with edit 5. Per-bin signature failure is legitimate narrowness, provided the failing bin is fully resolved.
- G5 - Accept. Proven zero at degenerate K=1 counts as zero for breadth, while remaining labelled DEGENERATE. The known ACC outcome appropriately prevents redundant discovery work.
- G8 - Accept with qualification. A timeout can leave UPK certified while UPK_cue remains UNRESOLVED. However, an unfinished required control still blocks the corresponding family-level ADMIT under your declared rules.

The resulting certificate supports bounded pressure, representability and specified response properties. Its acquisition ceiling remains correctly untested.


## CONSULT #11 RESPONSE
(Interpretation check of PR #5 acquisition study. Retrieved 2026-10-20 ~7:38 PM ET; hand-transcribed from page, formatting normalized.)

Verdict: retain ADMIT for predictive acquisition and the scoped E2 result. Do not promote it to acquired, causally localized state organization.
I checked PR #5, its protocol, results and relevant evaluation code.

1. Allowed claim
The PR's actual ceiling is narrower than your proposed paraphrase and is appropriate. I would use:
> In the frozen W2 task, supervised training of a supplied GRU-8 with an external timing scaffold acquired history-dependent X, Y and XOR predictions; training the recurrent parameters improved held-out prediction relative to readout-only training on the matched frozen initialization, under the declared budget. The tested causal localization was not demonstrated.
Drop "acquired state that causally supports joint prediction" as an unqualified headline. E2 establishes a benefit from allowing recurrent adaptation; E3 did not identify the proposed content-carrying subspace. Whole-state transplant equivalence supplies no independent localization evidence.

2. Is K-FR too weak?
It is a valid control for E2's stated question. Its weakness does not invalidate the paired comparison: freezing the same initialized recurrence while training the same readout is precisely the relevant intervention. It does limit generalization to other frozen reservoirs.
The results already include frozen GRU-16 and RNN-8: their median total excesses are approximately 0.0451 and 0.0468, respectively. Thus the failure is not confined to GRU-8. This still does not establish that recurrent training is necessary.
For a stronger, separate robustness comparison, I recommend tuned frozen GRU-8, keeping the architecture family unchanged:
- Hidden size 8, same inputs, initial state and numerical precision.
- Scale initialized hidden-to-hidden matrices by g in {0.5, 1, 2}; add update-gate preactivation offset b in {-2, 0, 2}: nine frozen configurations.
- Readout 8->70->3, giving 843 trainable parameters, equal to the original candidate's total trainable count. Charge the additional frozen parameters separately.
- Select the configuration using a deterministic 48-history validation subset of TRAIN; fit selection runs on the other 144 histories. Then refit on all 192 TRAIN histories and evaluate TEST once.
- Keep 4,000 steps, ordinary outcome labels and ten fresh seeds; report selection compute separately.
This is a parameter-budget robustness comparison, not a replacement for the original matched-network control. Larger reservoirs should be labelled capacity sensitivity, not equal-state rivals. An echo-state architecture is unnecessary for this immediate question.

3. What E3 actually says
The result is more specific than "the test failed":
- All ten candidate seeds passed coverage and rank requirements.
- Chart-subspace partial transplants had vector tracking ratios approximately 1.65-14.21.
- Complement transplants had ratios approximately 0.127-0.641, and tracked donors better in every seed.
- K-FR's E3 result was UNRESOLVED, chiefly because coverage failed - not a clean negative localization control.
These reported results suggest that the chosen chart-decoder projection does not capture the directions driving continuation forecasts. They establish neither a distributed code nor absence of a low-dimensional mechanism. Nonlinear encoding, poor cross-fitted decoding, redundant information and effects of artificial hybrid states remain possible explanations.
Immediate diagnostic: check held-out stage-4 decoder accuracy, and validate the intervention pipeline on an exact-filter chart embedded in eight dimensions with a known three-dimensional causal subspace. Keep these additive; do not reinterpret the complement result as a retrospectively successful E3.

4. Best next study
"Recurrent-core transfer with gate-path reversion and rescue." A bounded specification:
- Use ten fresh GRU-8 seeds and the same W2 split. Preserve each initial and trained recurrent core.
- Freeze each core and train new, identically initialized 8->32->3 readouts with identical data and budgets. Include the selected tuned frozen reservoir above. This tests whether useful predictive structure transfers with the learned recurrence, independently of its original co-adapted readout.
- With those readouts fixed, separately revert each of the three hidden-to-hidden gate matrices to its own initialization during continuation steps 5-8. Preregister all three interventions; select none using TEST.
- Compare changes against matched-norm random perturbations and sham substitutions. Restore the trained matrix as a rescue check. Report X, Y and XOR effects and their dependence on the earlier prefix.
- Require held-out transfer benefit plus reproducible, intervention-specific effects across fresh seeds before claiming a learned recurrent component contributes causally to prediction. Generic damage alone does not establish content-specific organization.
This stays within GRU architecture variants and below C4. It is a new prospective study, not a retroactive strengthening of PR #5.

One concrete correction before resource claims
I found a phase mismatch in the quantized-oracle implementation: ranges come from post-observation prefix beliefs, but quantized_exact_forecasts usually applies the transition before quantization. This explains why "K-EXACT fails even at 24 bits" needs investigation.
Add an erratum and corrected precision results: transition before the next observation, then quantize the post-observation chart against matching ranges. Verify convergence toward the exact TRAIN forecasts as precision increases.
The E1/E2 scoring uses separate frozen oracle forecasts, so this finding does not itself overturn those results.


## CONSULT #12 RESPONSE

FREEZE WITH NAMED EDITS. The core experiment is worth doing and stays within the GRU family, below C4. The principal problems are verdict logic and interpretation, plus an E3 validity gate that currently rejects its own ideal positive control.

Apply these edits before scientific freeze. The separate training approval recorded in the header remains necessary.

Separate transfer advantage from frozen-rival sufficiency.

Keep transfer primary against F-INIT. Remove §3 condition (d); report F-TUNED32 as robustness evidence. Replace the competing verdicts with:

"TRANSFER SHOWN requires A-FIT, integrity, and E(F-TRAINED) ≤ ½ E(F-INIT) in at least 8/10 seeds. Frozen-core A-FIT success is reported independently and does not override a demonstrated transfer advantage."

A rival can satisfy A-FIT while being substantially worse. Its sufficiency does not refute the candidate's advantage or identify the candidate's mechanism. Apply the same separation to §4: report ratio843 advantage and R-TUNED843 A-FIT success independently.

Also replace "co-adaptation loss" with:

"Original-versus-refitted-readout performance difference; this combines readout adaptation and optimization effects."

Use per-seed reservoir selection, with a balanced validation set.

Per-seed selection is appropriate for testing whether tuning each supplied initialization removes the gap. It is not guaranteed to find the strongest possible reservoir.

Replace the VAL rule with:

p = h mod 16
u = floor(h/16)
VAL iff (p + u) mod 4 = 2 and u != (2 - p) mod 16.

This gives 48 TRAIN histories, three per prefix and three per continuation, without dropping continuations 12–15. FIT contains the remaining 144.

Append smaller g to the tie-break, since g=0.5 and g=2 otherwise remain tied.

Add:

"Hyperparameter selection uses exact oracle expected validation risk. This is an explicitly supplied selection advantage for the robustness rival; it is not finite-sample outcome-only validation."

F-TUNED32 inherits settings selected for the 843-parameter head. Call it exactly that, rather than implying that its own head was optimally tuned. Keeping it descriptive avoids needing another nine-way search.

Keep the reversion thresholds as engineering criteria; remove the exact-p claim.

Reversion toward initialization is not exchangeable with isotropic random directions. Consequently, beating 32 draws is not an exact rank test with p≤1/33.

Replace SPECIFIC condition 1 and its interpretation with:

"Reversion causes greater excess loss than each of the 32 prespecified matched-norm random perturbations. This is an empirical directional comparison, not a calibrated significance test."

Keep the quarter-benefit materiality threshold, but add:

"SPECIFIC is evaluated only on a seed that passes the primary transfer criterion and has B = E(F-INIT) − E(F-TRAINED) > 10⁻¹². Require ΔE > 10⁻¹² and ΔE ≥ B/4. A zero displacement supplies no reversion test."

Thirty-two draws are acceptable for this bounded comparison. They do not establish superiority over generic damage generally.

For the combined claim, require the same gate matrix to satisfy transfer and SPECIFIC jointly in at least 8/10 seeds. Do not combine two different sets of eight successes. Integrity failures are invalid observations, not evidence of nonspecificity; more than two invalid seeds makes the relevant verdict UNRESOLVED.

Narrow the prefix-selectivity interpretation.

PD/CD measure forecast variation, not whether that variation carries correct prefix information. Moreover, the TEST split couples prefixes and continuations.

Replace the primary dependence analysis with:

"Compute PD/CD on the complete 16×16 prefix–continuation grid using uniform product weights. Report the original probability-weighted and TEST-restricted quantities separately. A denominator ≤10⁻¹² makes its ratio undefined."

The proposed PR≤½, CR≥¾ and random-draw comparison are acceptable descriptive thresholds. Rename the resulting label:

"PREFIX VARIATION REDUCED WITH CONTINUATION VARIATION RETAINED."

Do not equate it with a prefix-content mechanism. On failure, write "selective variation reduction not demonstrated", not "generic damage": failure of this test does not identify the alternative explanation.

Keep fresh readouts primary and matrix-only reversion.

Both choices are sound. Excluding biases cleanly defines the intervention, but use "hidden-to-hidden matrix reversion" rather than language implying that an entire gate pathway was reverted.

Keep sham and full restoration as integrity checks. Restoration by rerunning the intact network is not independent causal rescue evidence.

Freeze the descriptive FOREIGN-INIT pairing—for example, cyclic pairing of seeds 100–109—and all other descriptive operators before running.

Repair and version the E3 instrument prospectively.

Do not make the unchanged frozen rule the new pipeline-valid gate. Replace V-1 with:

"The frozen PR #5 rule is retained as a historical diagnostic. A separately versioned E3-v2 instrument is used for prospective validation. For ratio N/D: if D≤10⁻¹² and N>10⁻¹², return +∞; if both N and D≤10⁻¹², return UNDEFINED; otherwise return N/D. UNDEFINED never counts as a pass."

Apply this consistently across ratio statistics. A perfect complement intervention with a separated donor should pass, while an uninformative 0/0 should not.

Keep PR #5's frozen files and original verdict intact. Add an erratum explaining the defect and its implications for interpreting the null. Audit the saved original statistics for affected cases; any corrected reanalysis must be separately versioned.

Treat decoder angles as stability evidence, not causal validation.

Inter-fold agreement ≤30° does not show agreement with the true causal subspace: both folds can agree on a misleading basis.

Replace DECODER ADEQUATE with:

"DECODER PREDICTIVE AND CROSS-FOLD STABLE: the declared R² and inter-fold-angle thresholds pass. This does not validate the intervention subspace."

In P2, where Q is known, report each fitted subspace's angle to span(Q) as well as inter-fold angles and intervention outcomes. Keep 30° as a declared diagnostic threshold, not a sufficient causal criterion.

Your pilot also needs precise wording: marginal R² remains high, but covariance R² deteriorates. It does not demonstrate uniformly excellent three-coordinate prediction at large nuisance.

For P2, additionally specify:

Exact seeds, nuisance initialization, matrix distributions/scaling and update order.
An explicit known-Q projector control, separating intervention implementation from decoder recovery.
A deterministic extension to invalid charts produced by hybrid interventions, with repair counts.
Clear ξ/ν notation and degree symbols, replacing the current question marks.

The "decodable but unused" example does not guarantee non-localization: the fitted decoder may overlap the used nonlinear code. Verify that intervention on the known unused Q-copy has zero effect; treat learned-projector behavior as descriptive.

P2 is an analysis instrument, not a new candidate architecture family. Its failure limits E3 interpretation, not the transfer experiment. At zero nuisance, rotations are largely equivalent tests; 100 rotations are not 100 independent demonstrations of detection power.

Use fresh seeds; correct the failure claims.

Do P1 on the new saved checkpoints. Replaying PR #5 is lower priority and unnecessary for this study. Matching recorded errors within 10⁻¹² would establish a metric-matched reconstruction, not prove identical weights without checkpoint hashes.

Replace the §9 failure statements with:

"Transfer failure means transferable benefit was not demonstrated with this readout, optimization budget and split; it does not establish readout co-adaptation."

"Tuned-reservoir success establishes that the selected frozen alternative suffices under its declared resources; it does not explain away the candidate's learned contribution."

Correct resource-parity wording: F-TUNED32 has matched readout size; R-TUNED843 matches the original candidate's trainable parameter count, while carrying additional frozen parameters and selection compute.

Allowed successful claim

"In W2, recurrent training produced a GRU-8 core whose predictive advantage over its matched initialization survived replacement and retraining of the readout. For the specified matrix, reverting learned weights during continuation caused greater held-out prediction loss than each of 32 matched-norm random perturbations, meeting the prespecified materiality criterion in at least 8/10 fresh seeds."

Append tuned-rival and variation results separately. This supports a learned, transferable recurrent contribution with bounded causal intervention evidence. It does not establish localized content, necessity, C4, or consciousness.


## CONSULT #13 RESPONSE

Accept the scoped certificate after additive errata. SEL and ROUTE admissions stand; UPK and UPK_cue admissions survive once the omitted K=1 controls are certified. ACC’s primary label should be REJECT-SIG, with its independent REJECT-NARROW finding retained.

I checked the frozen protocol, results, and verdict implementation. I did not repeat the delegate’s 100-value replay.

Labels after correction

Quantity | Correct disposition
SEL | ADMIT, certified on unpaid cells
ACC | REJECT-SIG by precedence; REJECT-NARROW also established
UPK | ADMIT after E2, for ample-storage, upkeep-scarce cells
UPK_cue | ADMIT after E2, with the same scope
UPK_ev | Descriptive: zero in the certified ample clean examples; positive in the graded example; otherwise unresolved where uncertified
ROUTE | ADMIT, mathematically equivalent to the corresponding selection problem
ADAPT | VALUE-ONLY: certified zeros and unresolved intervals, not a positive adaptation finding

Before E2, the UPK admissions are not control-complete under the conservative reading of the declared “K=1: all” control. The omission is repairable by proof; it does not undermine the positive witnesses.

Adopt E1–E3 with this wording

E1 — ACC

“ACC’s primary verdict is REJECT-SIG under §7.2 precedence. Every positive decision cell has a certified complete optimum set and is SIG-UNDEFINED. The independently established §7.3 REJECT-NARROW finding remains valid: the first storage bin contains no positive cell. Neither finding rejects the ACC role or C3.”

This gives two downstream findings, not a choice between them: the signature needs redesign for identification, and the declared breadth criterion separately fails.

E2 — K=1

“At K=1, the sole reachable I-phase configuration fixes all answer fields and durability marks independently of evidence and cue. Every admissible full policy therefore also belongs to fixed_upkeep and cue_blind_upkeep. The three optima coincide, so UPK=UPK_cue=UPK_ev=0. All applicable K=1 upkeep records are corrected to DEGENERATE with certified zero gaps and included in control accounting. These certificates restore ADMIT(UPK) and ADMIT(UPK_cue).”

The proof is valid. Apply it to all corresponding primary and secondary records, not merely the eight decision-bearing UPK records.

E3 — execution scope

“Unsearched cells retain scientific status UNRESOLVED and receive execution status NOT-RUN. No timeout is asserted for them. Nontrivial positive UPK certificates were obtained at ample capacity: K≥26 for B_up=1 and K≥16 for B_up=2 in the cited clean examples. These certify upkeep-budget pressure, not a storage-scarcity interaction. The qualifying values reproduce the protocol’s analytic predictions. Other cells resolved by separate zero proofs remain certified.”

Add an explicit omission manifest covering paid SEL, S1/S2, H=3, and the missing Stage-B grid points. Replace wording suggesting that every unresolved search exhausted its budget.

No optimization rerun is required to preserve these admissions. Recompute verdicts and control accounting from the existing results plus the new analytic certificates, publishing a versioned correction. Preserve the frozen protocol and original outputs.

Rulings on questions 1–8

ACC precedence: REJECT-SIG is primary; “preserved record” does not erase the explicit precedence rule. Retain both reasons. Repairing the signature would not repair the failed breadth criterion.

K=1 control: Yes, treat the §5.5 “all” row as applicable. Its omission from the narrower control index should not license bypassing it. The constant-policy proof resolves it without enumeration.

Unsearched cells: Use two fields: result=UNRESOLVED, execution=NOT-RUN. Existential admission can survive unresolved non-control cells once every bin already qualifies. It cannot survive unresolved required controls. “Ample-storage, upkeep-scarce” is the correct UPK scope.

ROUTE versus SEL: Yes. A decoder’s L messages define L action vectors; selecting a message is selecting a codeword. With separate consumer channels and symmetric tasks, the objectives separate. Report ROUTE as the channel formulation of the same selection result, not independent evidence for multi-consumer coordination.

Paid SEL: Its omission is an execution deviation, not faithful completion of the declared grid. Nevertheless, unpaid witnesses suffice for the existential SEL admission. The card may close as a partially executed certificate with explicit omissions; paid searches are unnecessary for the narrower claim.

ADAPT: Disclose the reduced grid. “Value-only” does not exempt execution from the frozen specification. A full-class positive magnitude requires complete optimization or bounding proofs that close the gap, including potentially useful signalling encoders. Existing universally valid upper bounds, feasible-policy lower bounds, and certified zeros remain reportable without that search.

Two wording corrections matter:

T₂/T₃ are adaptive trackers.
A lower bound of zero follows from class inclusion; it does not itself show that adaptation failed. The restricted search found no improvement over the specified trackers.

The PR also reports an UNKNOWN-FIXED interval [0, 5/384]; SWITCHING is not the only unresolved experimental interval.

ACC signature: This is operator unavailability on the certified positive optima, not an observed null response to an applicable intervention. Do not generalize it to every codebook with K≤6 or all possible ACC interventions. Reachability-preserving single-field flips were too restrictive here. A future signature should establish applicability prospectively, potentially using an explicitly defined transient readout intervention.

Post-hoc deviations: Acceptable as retrospective disclosure, not as preregistration or authority to reinterpret gates. Independently adjudicate the consequential readings—as above—and identify when each was documented. Protocol-byte preservation does not prove execution fidelity. “46/46 executed self-tests passed” must not be presented as proof that every required control was covered.

Corrected claim ceiling

“In W2′, exact optimization and analytic certificates establish value pressure and representability for cue-dependent selection under unpaid storage constraints, its equivalent channel-limited routing formulation, and cue-dependent durability allocation under a scarce upkeep budget at ample storage. Qualifying optimal policies exist in each declared admission bin. Acquisition, causal use in a developed system, and necessity beyond the declared rival classes remain unestablished.”

The delegate’s final exclusion of Q-EXIST is too strong: the certificate does establish existence within the specified mathematical policy classes. It does not establish those roles in a learned model or organism. Likewise, computed intervention effects characterize the specified policies, without demonstrating acquired causal organization.

Single most valuable next step

Proceed with the Consult #12 recurrent-core transfer and matrix-reversion study, with its named repairs and separate authorization. It directly addresses the missing combination of acquisition, transferable recurrent contribution, and bounded causal intervention evidence. Further scarcity enumeration would mainly refine an optimal-policy certificate whose admitted upkeep results were already analytically predicted.

That study remains in the GRU family and below C4. It would establish a recurrent predictive contribution, not automatically acquired SEL, ROUTE, or UPK; those ledger rows must remain separate.


## CONSULT #14 RESPONSE

Retain the reported labels, with E-1 through E-6 adopted as additive errata. Transfer is demonstrated; the stronger, preregistered matrix-specific claim is not. No retraining is needed to correct the record.

I checked the protocol, results and verdict code in PR #7, including the P2 implementation. The deviations file is identical at freeze and results.

Confirmed literal labels

E1: REPLICATED — 10/10
Transfer: SHOWN — 10/10, zero invalid
F-INIT / F-TUNED32 A-FIT: 0/10 / 0/10
Advantage over R-TUNED843: OBSERVED — 10/10, within the declared grid
R-TUNED843 A-FIT: Not met — 0/10, within that grid
SPECIFIC(r/z/n): NOT DEMONSTRATED — 1/10, 3/10, 3/10 joint passes
Variation labels: Not demonstrated; n's 9/10 condition count is descriptive
P1: Not met — 0/10 for each distinct core type
P2: PIPELINE VALID under the frozen P2 criterion, with the limitations below

The FINAL protocol explicitly labels every valid count below eight as NOT DEMONSTRATED. Thus z/n are not UNRESOLVED merely because they scored 3/10.

Exact errata

E-1 — claim assembly. Adopt:

"In W2, recurrent training produced a GRU-8 core whose predictive advantage over its matched initialization survived replacement and retraining of the readout in 10/10 fresh seeds. Hidden-to-hidden matrix reversion did not meet the prespecified joint criterion for any matrix. Advantage over the selected tuned frozen GRU-8 with 843 trainable readout parameters was observed in 10/10 seeds. That rival met A-FIT in 0/10 seeds within the declared grid. Selective variation reduction was not demonstrated under the gated criterion."

E-2 — grid scope. Adopt, but correct the delegate's extrapolation:

"Selection chose the upper tested gain, g=2, in 10/10 seeds and the lower tested offset, b=−2, in 9/10. Both tuned-rival conclusions concern the declared grid and training procedure. Performance outside that grid is unmeasured. Boundary selection motivates further investigation but does not establish the location or performance of an unrestricted optimum."

The delegate's 10–34× calculation concerns approximately matching CAND. Defeating the CAND/rival ≤ ½ advantage threshold requires roughly 4.8–17.1× improvement. Neither estimate justifies "very unlikely to be grid-limited." The 1.8–2.5× estimate addresses only A-FIT's total-error clause, not its additional XOR clause.

E-3 — counts. Adopt:

"SPECIFIC counts are successful joint passes, not failures. Directional/materiality/joint counts are r: 8/1/1, z: 9/3/3, and n: 3/10/3, each out of ten. Variation-condition counts 1/1/9 are descriptive; the positive variation label additionally requires REPLICATED SPECIFIC."

Use "below the declared materiality threshold," not "immaterial."

E-4 — P1. Adopt:

"CAND and F-TRAINED share the same recurrent core and therefore identical P1 states and results. The specified cross-fitted linear decoder failed the predictive-and-stability criterion on both trained and initial cores. This does not establish absence of covariance information, a nonlinear predictive representation, or a low-dimensional causal mechanism."

E-5 — P2−. Strengthen the disclosure:

"P2− uses cached exact causal-code values when the reconstructed code is within 10⁻⁸. Its zero-effect result therefore validates the cache-assisted implementation, not a cache-free eight-dimensional state implementation. The cache contributes to enforcing the expected invariance. P2− is descriptive and does not determine the P2+ PIPELINE VALID label."

E-6 — approval. Adopt the proposed wording, tied to the archived approval record:

"Neural training for this study was approved by Aidan Ahern on 2026-10-20 at 8:55 PM ET ('Yes, approve it once Astra clears it'). Consult #12 had cleared the protocol with named edits, applied in FINAL sha 63c463c7. The hashed header's 'pending' wording predates that approval and is retained unedited."

Publish corrected presentation and summaries separately; preserve the frozen originals.

Rulings on questions 1–8

The per-condition pattern is legitimate to report. Describe the measured comparisons and failed thresholds precisely. Importantly, "not causal evidence" is too strong: controlled parameter interventions changed forecasts and loss. What failed is the replicated, directional-plus-materiality criterion, not the existence of any causal influence.

For n, prefer "sensitivity also elicited by matched-norm random perturbations." "Consistent with generic sensitivity" is acceptable as a hypothesis. "Generic sensitivity explains the result" is not established. Conversely, the learned direction was unusually damaging in three seeds, so do not erase that heterogeneity.

Qualify both tuned-rival labels by the grid. A wider search is a legitimate robustness study, with unchanged state size and architecture family, but it is secondary to the causal question.

The proposed 42-point grid is not a superset of the original grid. If called an extension, retain the original nine points: the union has 47 configurations. Treat work on seeds 100–109 as a follow-up informed by their results; use fresh seeds for confirmation. The proposed boundary stopping rule is reasonable, but absence of boundary selections would still not certify global optimality.

P1 limits this decoder, not all linear methods or localization research. Eight calibration points, ridge regularization, coordinate scaling and fold instability all matter. Simply replacing it with a flexible nonlinear probe risks fitting the sixteen prefixes without identifying use. Deprioritize localization until there is a more reliable functional intervention target. Localization is not a prerequisite for demonstrating acquired causal organization.

The cached P2− check can remain disclosed and descriptive. For future validation, use a state-only, well-conditioned invertible code—for example, encode each centered coordinate as t+t³, whose derivative never vanishes—rather than a cube-root inverse near zero. That requires an analytic harness revision and validation, not network retraining.

Retain P2's literal label; narrow its meaning. Omitting coverage/rank gates was documented before training. Report those diagnostics prominently rather than importing stronger PR #5 eligibility claims.

One important limitation is already visible: fitted P2 passes at nuisance scale 1 despite a median largest angle of approximately 52° to the true subspace. Thus P2 validates detection under its forecast-ratio criterion; it does not validate accurate recovery of the true subspace or specificity across arbitrary representations.

Yes, E-6 is sufficient, assuming the cited approval transcript is retained. No alteration of the hashed header and no rerun are needed.

Prioritize a graded, joint recurrent-matrix intervention study, described below. It addresses the present causal uncertainty more directly than expanding the frozen-reservoir grid.

Claim ceiling

The E-1 paragraph is the earned headline. For the ledger, distinguish:

Q-LEARN: learned recurrent contribution that transfers to fresh readouts.
Q-CAUSE, basic intervention dependence: demonstrated forecast/loss sensitivity to the specified weight changes.
Q-CAUSE, preregistered specific organization: not demonstrated.
Q-NECESSITY: not tested.

This avoids both overclaiming a mechanism and understating real intervention evidence. No localized content, C4, consciousness or organism conclusion follows.

Single most valuable next study

"Graded joint recurrent reversion with oracle-referenced prefix-function loss."

Use the saved checkpoints for explicitly exploratory development, then confirm on fresh seeds under a new protocol:

Primary target: the complete weight_hh tensor; individual r/z/n blocks secondary.
Fixed path: W(α)=Wᵀ+α(W⁰−Wᵀ), with α∈{0,⅛,¼,½,¾,1}, applied at steps 5–8.
Hold the fresh readout fixed. Compare against 32 random directions matched per gate block in norm, using the same directions across doses.
Predeclare a curve-level comparison; do not select the most favorable dose afterward.
Measure correctness of prefix-dependent predictions, not just their variance:
L_prefix = E_{p,u} || [f(p,u) − f̄(u)] − [q*(p,u) − q̄*(u)] ||²
(formula transcribed from garbled rendering of the page's math)
Report the analogous continuation quantity and XOR separately, with sham and restoration checks.

This asks whether jointly removing the learned recurrent transformation progressively disrupts correct use of earlier evidence, beyond matched perturbations. It can expose distributed contributions and endpoint saturation without searching for a convenient subspace or revising PR #7's failed threshold.

It stays within the GRU family and below C4. Its success criterion must be frozen before fresh-seed confirmation; it is a new study, not a reinterpretation of this one.



## CONSULT #15 RESPONSE

[Consult #15 response, GPT-6 Astra, High effort. Transcribed from page text; ASCII formulas rendered cleanly, no garbling. Code blocks labelled "Plain text" on the page.]

FREEZE WITH NAMED EDITS. The design is coherent, remains within the GRU family and below C4, and can support a bounded causal contribution claim. Its current wording overstates selectivity and monotonicity. Phase B still requires the separate approval specified in the draft.

1. Use this exact ASCII definition

[Plain text]
p, u = 0,...,15
t in {X, Y, XOR}

f_bar_u[u,t] = (1/16) * sum_p f[p,u,t]
q_bar_u[u,t] = (1/16) * sum_p q_star[p,u,t]

L_prefix(f) =
    (1/256) * sum_p sum_u sum_t
    (
        (f[p,u,t]      - f_bar_u[u,t])
        -
        (q_star[p,u,t] - q_bar_u[u,t])
    )^2

There is no division by three over output components.

Equivalently, it measures the variation across prefixes of the forecast error, holding the continuation fixed. Consequently:

L_prefix(q_star) = 0.
Every prefix-blind forecast has L_prefix = PD(q_star).
L_prefix = 0 permits an arbitrary continuation-dependent forecast error. It does not imply globally correct forecasts.
L_prefix and L_cont overlap through prefix–continuation interactions; they are not an additive decomposition of total error.

The proposed formula is correct. Keep the complete uniform grid primary and TEST prediction errors separate.

2. Add an intact-function eligibility check

Transfer and B_prefix > 0 do not guarantee that F-TRAINED's prefix function is better than ignoring the prefix.

Add to §6:

"Define C_prefix = PD(q_star) − L_prefix(F-TRAINED). Eligibility additionally requires C_prefix > eps0. Otherwise the seed is a non-pass, not invalid. This establishes that the intact trained core's prefix-dependent forecast is more accurate than the prefix-blind reference. Report L_prefix(F-TRAINED), B_prefix and C_prefix both absolutely and divided by PD(q_star)."

Retain B_prefix/4; no additional PD-relative materiality floor is necessary for this bounded claim. A small baseline benefit must remain visible in the continuous results.

Replace "training-attributable prefix-function benefit" throughout with:

"paired prefix-loss advantage over F-INIT after separate readout training."

That names the measured contrast without attributing the entire advantage specifically to weight_hh.

3. Clarify the curve statistic and signed values

The stated trapezoid weights are correct:

[Plain text]
alpha:   0     1/8    1/4    1/2    3/4    1
weight:  1/16  1/8    3/16   1/4    1/4    1/8

Add:

"AUC is the integral of the piecewise-linear interpolant through the six measured dose-excess values. It is not a certified integral of the network's continuous dose response. Negative excesses are retained; no clipping or absolute-value transformation is applied."

Keeping the zero-dose weight is correct. Do not renormalize after dropping its zero contribution.

Replace the saturation-index rule with:

"Report Delta_REV(1/2) / Delta_REV(1) only when Delta_REV(1) > eps0; otherwise report UNDEFINED. Negative numerators remain signed. Do not apply the nonnegative E3 ratio convention to signed loss differences."

For the directional comparison, freeze a numerical tie margin:

"D passes iff AUC_REV − max_j AUC_rand,j > eps0."

For a linear excess curve ending at d, AUC equals d/2. Thus your materiality rule requires d >= B_prefix/2. That is stricter than an endpoint-quarter rule using the same outcome and baseline. It is not directly comparable with PR #7's different outcome and scale.

4. Correct the intervention and mismatch interpretation

Replace the endpoint explanation with:

"At alpha=1, only the hidden-to-hidden matrices during updates 5–8 equal their initialization. Input-to-hidden weights, biases, updates 1–4 and the fresh readout remain trained. This condition is not F-INIT, even apart from the readout difference."

Replace "readout-core mismatch … handled" with:

"Holding the same readout fixed in REV and random conditions controls readout identity, but does not eliminate differential disruption of compatibility among recurrent matrices, input weights, biases and the readout."

That limitation does not invalidate the experiment. It bounds its explanation.

5. Repair eligibility and count wording

A zero learned displacement in one block should not prevent testing learned changes in the other blocks jointly.

Replace the displacement rule with:

"Primary eligibility requires ||delta||_F > eps0. A block with exactly zero displacement receives a zero random perturbation. Nonzero blocks are rescaled to their own displacement norm. Secondary eligibility requires ||delta_k||_F > eps0 for the tested block."

Retain transfer eligibility and B_prefix > eps0. Eligibility failures are non-passes; integrity failures are invalid.

Replace "8/10 eligible valid seeds" wherever it occurs with:

"At least eight of the ten prespecified phase-B seeds jointly satisfy validity, eligibility, D and M. The denominator remains ten; seeds are not removed from it."

Make verdict precedence explicit: failed E1 replication or more than two invalid seeds yields UNRESOLVED before evaluating the success count.

6. Narrow the question, claim and ledger

AUC success does not require a monotonic curve. Nor does increased prefix-function error establish preferential disruption relative to continuation processing, because L_cont is descriptive.

Replace "increasingly disrupts" with "produces a positive dose-averaged disruption." Remove "selectively disrupts" from the interpretation and ledger.

Use this success paragraph:

"In W2, interpolation of the complete hidden-to-hidden matrix toward its initialization during updates 5–8, with trained input weights, biases and a fresh readout held fixed, increased oracle-referenced prefix-function loss over the predeclared dose grid. In at least eight of ten fresh seeds, the trapezoidal excess exceeded that of every one of 32 block-norm-matched random paths and reached at least one quarter of the paired prefix-loss advantage over F-INIT. The intact trained cores also outperformed the prefix-blind reference."

Then append:

"This supports a bounded causal contribution of the trained hidden-to-hidden parameters to accurate prefix-dependent prediction under the specified intervention and fixed surrounding computation. It does not establish monotonicity, selectivity over continuation processing, localized content, necessity, or a uniquely identified mechanism."

Vector success also does not establish an XOR-specific effect. Keep the XOR results explicit but descriptive.

Rulings on O1–O11

O1: formula -- Correct as written explicitly above; both means are uniform over prefixes.
O2: weighting -- Keep the complete uniform grid primary. It measures the forecast function, including trained histories; do not call the primary causal statistic held-out generalization.
O3: AUC -- Keep trapezoidal AUC and the zero-dose weight. Endpoint loss remains descriptive.
O4: materiality -- Keep B_prefix/4, with the baseline eligibility and reporting edits above. Nonpositive B is non-pass, not invalid.
O5: directional rule -- Keep beating all 32, with the numerical margin. It is an empirical comparison, not a calibrated p-value.
O6: refitted endpoint readout -- Keep the fixed-readout study focused. Endpoint refitting would test recoverability under readout adaptation, a different question; do not add training here.
O7: transfer eligibility -- Keep it for the acquired-contribution claim. Still report curves for valid seeds that fail eligibility, without upgrading them into confirmatory passes.
O8: shared random blocks -- Accept. This preserves matching across targets and doses. Secondary results are correlated and cannot serve as independent replications.
O9: Phase A reporting -- Endpoint block errors and B-relative flags are acceptable when explicitly exploratory. No need to hide them. Preserve the prohibition on pooling or using them as confirmation.
O10: rival seeds and boundary rule -- Seeds 200–209 are appropriate for a paired robustness comparison if the appendix is fixed before exposure to their results. Separate seeds are unnecessary. Keep the ≥3/10 rule as a boundary-selection flag, not proof that the optimum lies outside the grid.
O11: 32 versus 64 -- Keep 32. Increasing the reference sample makes "beat every draw" more stringent; it is not merely a precision improvement. No current reason requires that change.

Final document repairs

The pasted text interleaves §§5, 8–10, 12 and Appendix A. Restore their order before hashing; freeze one complete, readable specification.

Also:

Version and hash engineering fixes before Phase B, even when they do not require the S4 scientific-change suffix.
Mark Appendix A's oracle-assisted hyperparameter selection as an exception to "oracle used only for evaluation." It is already a disclosed selection advantage there.
Replace ledger entries treating a failed criterion as a REDUCTION with "criterion not met; no reduction identified."
The NumPy construction check validates the rescaling algebra, not the frozen Torch draw sequence; test that sequence in the frozen implementation.

With these edits, Phase A can proceed under its stated standing authorization after hashing. Phase B remains contingent on its separately recorded training approval. No C4 escalation or new architecture family is warranted.



## CONSULT #16 RESPONSE

**Verdict: confirm REPLICATED, 9/10, under the frozen criterion.** E-B1 and E-B2 are appropriate additive corrections; neither requires a rerun. This confirms the interpretation of the supplied records, not an independent verification of network forward passes.

1. **Labels and E-B3.** Primary REPLICATED; all three secondary blocks CRITERION NOT MET; E1 and transfer replicated 10/10. Adopt E-B3 as a disclosure:

   > "Four of nine passing seeds exceed the most damaging sampled random path by less than 10% of that path's AUC. At alpha = 1, at least one sampled random path causes greater loss than reversion in 7/10 seeds. The preregistered directional criterion concerns trapezoidal AUC over the dose grid; an endpoint-only directional comparison would pass in 3/10 seeds. These descriptive findings do not change the frozen labels."

2. **Thin margins.** Include a short qualifier in the ledger, alongside the table:

   > "Support is relative to the 32 prespecified block-norm-matched random paths. Directional margins are small in several passing seeds; robustness to additional draws or stronger control families is untested."

   These are small *comparative* margins, not rounding-level ambiguities. They neither invalidate the result nor establish its stability under a different control sample.

3. **Curve shape and what REPLICATED licenses.** Yes: "beyond matched random perturbation" must explicitly mean **AUC over the specified dose path**, not every dose, the endpoint, or arbitrary perturbations.

   The first-order interpretation is plausible. Locally, for a parameter direction `d`:

   ```text
   Delta L(alpha*d)
     = alpha * dot(grad L, d)
       + (alpha^2 / 2) * d^T H d
       + higher-order terms
   ```

   Reversion may have a larger positive gradient projection than typical isotropic directions. However, a half-dose ratio near 1/2 or 1/4 does not establish that explanation across these finite displacements. The network was not optimized directly for this evaluation loss, and its intact prefix error is nonzero.

   The earned claim is:

   > "In W2, the trained hidden-to-hidden parameters make a bounded causal contribution to accurate prefix-dependent prediction under the specified continuation-stage intervention and fixed surrounding computation. In 9/10 fresh seeds, reversion produced greater dose-averaged excess prefix-function loss than each of 32 prespecified block-norm-matched random paths and met the declared materiality threshold."

   This establishes neither prefix-over-continuation selectivity nor an XOR-specific, localized, or uniquely identified mechanism.

4. **Next control.** Prefer **gradient-projection-matched random paths**. Foreign-seed trained matrices are weaker controls for this question: hidden-unit coordinates differ across seeds, so transplanting one matrix can create coordinate incompatibility. Such substitutions also do not automatically match first-order loss effects.

5. **Single-block interpretation.** Approve:

   > "The primary effect was not reproduced by any single block at the declared criterion."

   Do not infer that single blocks carry no contribution, that the effect is distributed, or that `n` explains the joint result. Those require interaction or contribution analyses; threshold pass counts do not establish them.

6. **Approval provenance.** The existing record is sufficient on the supplied account. An additive clarification is useful:

   > "The approval recorded at 10:38 PM ET on 2026-10-20 answered widget t20s2: 'Approve fresh-seed GRU-8 training for the graded reversion confirmation once Astra clears the protocol?' Aidan answered: 'Yes, approve it once Astra clears it.' This approval applied to Phase B of this study; Appendix A remained unapproved and was not run."

7. **Q-NECESSITY and C-levels.** Neither moves. The result strengthens bounded Q-CAUSE evidence for the acquired recurrent contribution in this C3-type task. It does not establish recurrent training as necessary, establish all C3 roles, or supply C4 evidence.

The single most informative next study is **"Graded recurrent reversion against first-order-matched controls."** Keep the architecture, fresh-readout intervention, dose grid, prefix loss, and block norms unchanged. For each block, calculate the gradient with respect to an override applied **only at updates 5-8**, holding the intact stage-4 state fixed.

A concrete construction is:

```text
d_k = vec(W0_k - WT_k)
g_k = gradient of L_prefix with respect to the late-stage block override

a_k = dot(g_k, d_k) / dot(g_k, g_k)

e_k = a_k*g_k
      + sqrt(norm(d_k)^2 - a_k^2*norm(g_k)^2) * u_k

u_k = a random unit vector orthogonal to g_k
```

Each `e_k` matches both the block displacement norm and its signed first-order effect on the primary loss. Assemble the three blocks, generate 32 prespecified paths, and reuse them across doses. Retain the original isotropic controls descriptively. Freeze numerical tolerances and treatment of zero gradients or collapsed residual spheres; a collapsed control family cannot provide a meaningful specificity comparison.

Keep the original AUC directional and materiality rules for continuity, and report the actual margins. Oracle-informed gradient matching is an **analysis control**, disclosed as such, not network training. Its success would support an effect beyond matched local first-order sensitivity and displacement size; it would still not identify semantic content or a unique mechanism.

Existing checkpoints can support an explicitly exploratory pilot without training. For prospective confirmation, use fresh seeds, for example 300-309, under a new protocol; the CAND/F-TRAINED/F-INIT replication requires 30 training runs and Aidan's explicit approval. This remains within GRU-8 and below C4.

Toward **Q-NECESSITY**, first define what must be necessary, for which performance threshold, and within which resource-bounded class. Fixed-readout damage establishes dependence in an implementation. A stronger necessity study allows the remaining computation to compensate, including readout retraining, and compares the best restricted system against the unrestricted one. Failed training attempts alone cannot certify necessity; that requires a bound or complete search within a declared class. W2 already has a supplied exact solution, so universal necessity of recurrent *training* is unavailable.

Toward **C4**, the next step is a separate admission proposal, not an upgrade of this result. It must specify an internal-evaluation role and evidence dissociating that role from first-order inference. A possible task involves changing reliability of the system's own processing channels and decisions to check, route, or repair them, with conventional adaptive-control rivals and interventions that distinguish evaluation from ordinary prediction loss. Supplying that task does not establish acquisition of an evaluator; ORIGIN must be tested separately. A first C4 study requires Aidan's explicit approval even if it retains the GRU family. Nothing here warrants a consciousness claim.

## CONSULT #17 RESPONSE (2026-10-21 ~1:12 AM ET)

**Verdict: FREEZE WITH NAMED EDITS.** Choose O1(a): require the same seeds to beat **both FO and ISO families**. The study remains useful, but its rationale must change. First-order matching is a conditional comparison, not an automatically stronger control.

The edits below are sufficient for scientific clearance without another review round. Phase B training still requires Aidan's separate approval.

**O1: correction to consult #16 and the control choice**

The feasibility finding undermines my proposed positive-gradient explanation. More precisely:

- In 15/20 seeds, the initial tangent predicts improvement, not damage.
- In the other five, it explains at most 23% of the observed damage at alpha = 1/8.
- Therefore, the initial tangent does not explain the positive damage at that dose. This does not mean the first-order term is absent.
- For a genuinely negative derivative, sufficiently small positive doses must initially *decrease* loss. Non-decreasing values on the sampled grid therefore do not imply a continuously monotonic path.

Negative slopes also do **not prove** that FO controls have smaller finite-dose AUCs than ISO controls. That remains unmeasured. Conjunctive gating prevents a success based solely on a potentially easier family.

Do not add the one-sided family or curvature matching here. Clipping negative projections changes the matching question. Per-block curvature matching would also omit cross-block Hessian terms relevant to joint reversion; matching full directional curvature would require a separately specified sampler and feasibility audit.

Add this versioned interpretation note to the PR #8 disclosures and consult #16 record:

> "Exploratory finite-difference checks on the 20 existing checkpoints found a negative initial reversion derivative in 15 seeds. At alpha = 1/8, the tangent prediction ranged from -1.39 to +0.23 times the observed positive loss increase. These findings do not support the proposed explanation of the sampled early-dose damage by a dominant positive initial gradient projection. The curve-shape analogy was a hypothesis, not an established mechanism. PR #8's AUC results and labels are unchanged. Confirmation of the derivative calculations by the new autograd implementation is required."

**Exact scientific edits**

1. Replace the directional and joint criteria throughout:

   ```text
   D_FO  = (AUC_REV - max_j AUC_FO,j > eps0)
   D_ISO = (AUC_REV - max_j AUC_ISO,j > eps0)
   D     = D_FO and D_ISO

   Joint pass = valid and eligible and D_FO and D_ISO and M
   ```

   Require at least eight of the ten fixed seeds to pass this **joint** rule. Separate eight-seed successes against each family are insufficient. Apply the same rule to secondary blocks.

   Replace the success label with:

   > "GRADED JOINT REVERSION EXCEEDS BOTH FIRST-ORDER-MATCHED AND ISOTROPIC CONTROLS (PREFIX FUNCTION): REPLICATED"

   Replace the failure label with:

   > "JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET"

   Report D_FO, D_ISO, their intersection, M, and joint counts. ISO is now decision-bearing.

2. Replace the rationale in Sec.1 and Q5:

   > "Existing-checkpoint feasibility checks do not support a dominant positive initial-gradient explanation of PR #8's sampled early-dose damage. This study asks whether reversion's dose-averaged advantage survives conditioning controls on its initial loss slope while also retaining the original isotropic comparison. Neither control family is assumed uniformly more stringent than the other."

3. Replace the success paragraph and duplicated limitation:

   > "In W2, in at least eight of ten fresh GRU-8 seeds, continuation-stage joint recurrent reversion produced a trapezoidal excess prefix-function loss exceeding every one of 32 first-order-matched paths and every one of 32 isotropic paths. Both families matched the reversion displacement block by block in Frobenius norm; the first-order-matched family additionally matched its initial loss derivative. The excess met the declared materiality threshold, and the intact trained cores outperformed the prefix-blind reference. This supports a bounded causal contribution under the specified intervention and fixed surrounding computation. The comparison concerns the sampled families and dose-averaged AUC; it does not identify semantic content, curvature as a mechanism, localization, necessity, or selectivity over continuation processing."

   On failure, say:

   > "The joint FO-and-ISO criterion was not met; no reduction was identified."

   Do not automatically attribute that failure to FO matching: ISO could be the failed condition.

**Required implementation repairs**

4. **Keep the gradient notation unambiguous.**

   ```text
   g_k  = vec(block k of G)       # unnormalized gradient
   gh_k = g_k / norm(g_k)        # unit gradient, when nonzero
   ```

   Remove the line that appears to overwrite `g_k` with its normalization. Orthogonality checks must use `gh_k`.

5. **Collapsed blocks must retain exact matching.** Replace `e_jk := p_k` with:

   > "For a collapsed block, set e_jk := d_k for every draw. The block has no randomized spread. Its secondary comparison is ineligible."

   Setting it to `p_k` loses the residual norm and violates the stated norm tolerance.

   For primary degeneracy, use:

   ```text
   R_eff^2 = sum of r_k^2 over non-collapsed blocks
   ```

   Collapsed blocks contribute zero randomized radius. Use `R_eff / norm(delta)` for the primary collapse decision and report which blocks were fixed.

6. **Near-zero gradients currently conflict with matching tolerances.** Replace the approximate-zero fallback:

   > "G_ZERO is a diagnostic threshold only. For every nonzero gradient, use the projection construction and its matching checks. For an exactly zero gradient, use the norm-matched isotropic draw; its first-order match is exact. Numerical inability to construct or validate a nonzero-gradient match is an integrity failure."

   Rename the diagnostic to `NEGLIGIBLE FIRST-ORDER SCALE`; do not call approximate equality exact.

   Add an absolute floor to the finite-difference check:

   ```text
   abs(FD - dot(G, direction)) <= 1e-10 + 1e-6*norm(G)
   ```

7. **Avoid cancellation in the radius check.** Keep `r_k = norm(d_k - p_k)` authoritative. Replace the square-root agreement gate with:

   ```text
   abs(norm(d_k)^2 - norm(p_k)^2 - r_k^2)
       <= 1e-12 * norm(d_k)^2
   ```

   The cancellation-prone square-root form may be reported descriptively.

8. **Count unevaluable seeds jointly.**

   > "After the E1 prerequisite, if more than two distinct seeds are invalid or have a collapsed control family for the target, report UNRESOLVED (insufficient evaluable seeds). Otherwise retain the denominator of ten."

   This handles, for example, two invalid plus two separately collapsed seeds. Other eligibility failures remain scientific non-passes.

9. **Fix manifest timing.** Checkpoint-dependent FO paths cannot be hashed before fresh checkpoints exist.

   > "Before Phase A, freeze the construction code, tolerances, generator seeds and base Gaussian draw manifests for both phases. After each checkpoint and gradient are available, construct and hash the transformed paths before evaluating their dose curves. Record checkpoint, gradient and transformed-path hashes together."

10. **Reporting consistency.** Apply aggregate thin-margin sentences only to Phase B; Phase A retains per-seed reporting. Report margins against both families. Percentage-of-control-AUC disclosures are undefined when that family's maximum AUC is nonpositive or <= eps0. Distinguish endpoint ties from strictly greater control losses. Replace "does not alter any network" with "does not train the network or modify its saved checkpoint."

**Rulings on O2-O10**

| Item | Ruling |
| --- | --- |
| O2 | Accept 1e-10, 1e-3 and 0.10 with repairs 5-8. Collapse is non-evaluability, not an engineering failure. |
| O3 | Accept: primary uniform-grid L_prefix, fresh readout, trained point, tied late-stage override. Explicitly detach h4 and freeze other parameters. |
| O4 | Accept block-only matching. Untouched blocks have zero displacement; no additional neutrality test is needed. |
| O5 | Amend as above. Always qualify the claim by sampled families, local derivative matching and finite-dose AUC. |
| O6 | Allow per-seed exploratory reporting. The correction to the earlier explanatory hypothesis should nevertheless be recorded additively, as specified above. |
| O7 | Keep 32 paths per family. No calibrated significance claim or robustness-to-more-draws claim. |
| O8 | Keep `AUC - FO_AUC`, named "residual after subtracting the initial tangent contribution." It is not a curvature estimate. |
| O9 | Yes: evaluation-only Phase A may proceed under the described standing authorization after these edits and hashing. No training is authorized by this ruling. |
| O10 | Accept with the revised study name: "Approve fresh-seed GRU-8 training (seeds 300-309, 30 runs, PR #7 recipe) for graded reversion confirmation against both first-order-matched and isotropic controls once Astra clears the protocol?" |

**Rulings on A1-A10**

- A1-A3: accept, with explicit h4 detachment.
- A4: amend the radius validation as in edit 7.
- A5: accept; use `gh_k` consistently.
- A6: amend as in edits 5, 6 and 8.
- A7-A8: accept.
- A9: accept as reporting only, with edit 10.
- A10: confirmed subject to O9.

This remains a GRU-family, below-C4 study. A success would strengthen the bounded causal comparison; it would not establish Q-NECESSITY or advance the C-level.

## CONSULT #18 RESPONSE (2026-10-21 ~2:12 AM ET)

**Confirm REPLICATED at exactly 8/10 under the frozen joint criterion.** Adopt E-C1 through E-C3 additively. No scientific rerun is required on the evidence supplied. The Delegate's forward-pass reconstruction substantially strengthens verification; I have not independently repeated it.

1. **Label and errata**

   The primary label is correct: the same eight seeds passed D_FO, D_ISO, M and eligibility. All secondary blocks remain CRITERION NOT MET.

   Adopt these corrections:

   - **E-C1:** Accept the proposed wording. Preserve a versioned copy and hash of the feasibility data supporting the per-seed comparison, rather than relying solely on a scratch path.
   - **E-C2:** Required. Attach the per-seed margins for both families and all four targets, with the stated secondary condition counts. This completes reporting; it changes no results.
   - **E-C3:** Adopt, specifying that the failures concern AUC:

     > "Seed 300: D_ISO failed; exactly one of 32 ISO paths had greater AUC than REV. Seed 301: D_ISO failed; exactly one of 32 ISO paths had greater AUC than REV."

   **One additional reporting correction:** the combined Phase A headline "13/20" conflicts with the prescribed separate, per-seed-only reporting. The 6/10 and 7/10 aggregate summaries also depart from that rule. Where these appear, add:

   > "The combined and group-level Phase A pass counts are retrospective descriptive summaries that depart from the prescribed per-seed-only reporting format. They are not confirmatory evidence and do not enter any Phase B verdict. The authoritative Phase A presentation is the separate per-seed record for each exploratory group."

   Preserve original artifacts. Correct subsequent summaries.

2. **Boundary and single-draw sensitivity**

   Yes, make the qualifier explicit:

   > "This result meets the prespecified threshold exactly: 8/10 seeds. Two passing seeds have a margin below 10% against at least one control family. Each failing seed is exceeded by exactly one sampled ISO path. Robustness to additional draws, alternative control families or a new seed cohort is untested."

   Do not dismiss those draws as spurious outliers. The maximum over draws is the frozen comparator. The small margins are far above numerical tolerances; the concern is sensitivity to control sampling, not arithmetic uncertainty.

3. **What the FO result adds**

   Use:

   > "The FO directional criterion was met more often in this cohort: 10/10 versus 8/10 for ISO. Adding FO to the joint gate excluded no additional seeds. This does not establish that FO controls are generally less demanding."

   FO had a larger sampled maximum than ISO in four seeds, so "the easier family" needs that qualification.

   The earned statement is that REV exceeded the sampled controls **even when their initial derivatives were matched**, while also passing ISO. Avoid an unrestricted claim that local sensitivity has been eliminated as an explanation. The negative derivatives in 9/10 fresh seeds further undermine the earlier positive-initial-gradient explanation; they do not identify the finite-dose mechanism.

4. **Exactly zero gradient**

   Ratified. With nonzero displacement and exactly zero gradient:

   ```text
   r_k = norm(d_k)
   rho_k = 1
   ```

   The block has full randomized spread and belongs in `R_eff`. Skip the undefined unit-gradient orthogonality check, but retain norm and first-order identity checks. This is distinct from the diagnostic near-zero threshold.

5. **Zero displacement**

   Keep it an ordinary eligibility non-pass, as frozen. There is no learned displacement in that target to test. Do not count it as an invalid or collapsed-comparison seed. If the entire displacement is zero, avoid forming undefined radius ratios. This ruling affects no observed result.

6. **Hash-before-curve ordering**

   The reported implementation satisfies edit 9. Reproduction from fixed checkpoints, gradients, construction code and base draws supports the absence of path selection within the declared pipeline. It does not independently establish every historical execution event.

   For future studies, use a two-stage runner: write and seal the transformed-path manifest, then evaluate curves from that manifest. A separate commit or timestamped artifact improves provenance but is not a retroactive requirement here.

7. **The proposed necessity study**

   The target is acceptable:

   ```text
   L_prefix <= tau * PD(q_star)
   AND both TEST A-FIT inequalities hold
   ```

   `tau = 0.25` is a reasonable prospective engineering choice. Disclose that prior results informed it.

   **R-FIX is the most informative next rival.** Freeze `weight_hh = W0` at all eight updates and allow input weights, both biases and the readout to learn. This directly tests whether the remaining computation can compensate.

   Correct two accounting issues:

   - With a 32-unit head, R-FIX has **651 trainable parameters**.
   - With a 70-unit head, it has **1107**, not 843: 264 trainable recurrent parameters plus 843 readout parameters.
   - A **48-unit head** gives 579 readout parameters and **843 total trainable parameters**, matching CAND.

   R-TUNE is admissible, but if update-gate biases subsequently train freely, `b` is an initialization/search choice, not a lasting class restriction. Charge its selection compute. Low-rank recurrent updates are a valid separate question about restricted recurrent learning; specify whether rank applies to the stacked 24x8 matrix or separately to each block. They should not complicate the primary no-recurrent-matrix-learning comparison.

   A bounded search is worth running because a successful restricted model supplies a counterexample. **One verified witness refutes absolute impossibility for that particular restricted class and target.** An 8/10 rule establishes reproducibility, not the logical minimum needed for a counterexample.

   Failure means only "not reached within declared search."

8. **Q-NECESSITY and C-level**

   Neither advances from PR #9. Q-NECESSITY remains NOT_ESTABLISHED. The result strengthens bounded C3-type causal evidence; it supplies no C4 evidence.

**Use this ledger wording:**

> "Q-CAUSE, organization level: SUPPORTED, BOUNDED. In W2, continuation-stage joint recurrent reversion met the prespecified joint FO-and-ISO AUC criterion in 8/10 fresh GRU-8 seeds. In each passing seed, excess prefix-function loss exceeded every one of 32 first-order-matched paths and every one of 32 isotropic paths and met the materiality threshold. This supports a causal contribution of the trained hidden-to-hidden parameters under the specified intervention and fixed surrounding computation.
>
> The result meets the replication threshold exactly. Two passing seeds have thin margins against at least one family; each failing seed loses to one sampled ISO path. FO passed in 10/10 seeds and excluded no additional seeds beyond ISO. The claim concerns sampled controls and dose-averaged AUC, not arbitrary perturbations, every dose or the endpoint.
>
> Secondary blocks: criterion not met, r 0/10, z 0/10, n 5/10. The primary effect was not reproduced by any single block at the declared criterion; no localization or interaction mechanism is identified.
>
> Q-LEARN: E1 and transfer replicated 10/10. Q-NECESSITY: NOT_ESTABLISHED, not tested. Q-EXIST: not addressed; the supplied exact solution remains available. No C4, consciousness or organism conclusion."

My recommended next study is **"Frozen recurrent matrices with learned compensation."** Use fresh seeds, for example 400-409, with three primary arms: CAND, R-FIX with the 32-unit head, and R-FIX with the 48-unit head. Pair initializations where shapes permit, episode streams and declared optimization budgets. Freeze the target, validation selection, restarts and reporting before training. This is a new protocol, below C4 and within the GRU family. These 30 training runs require Aidan's explicit approval.

The study should be framed as a **search for compensation and counterexamples to necessity**, not as a necessity certificate. Compensation would not negate the existing causal result: parameters can contribute causally in one trained implementation without being indispensable to another.

For a necessity certificate, I would accept a validated lower bound over the **entire declared restricted parameter domain**, or a complete search of an explicitly finite parameter class. For example, define:

```text
T(theta) = max(
    L_prefix(theta) / (tau * PD(q_star)),
    E_total_TEST(theta) / total_AFIT_threshold,
    E_XOR_TEST(theta) / XOR_AFIT_threshold
)
```

A certificate must establish `inf T(theta) > 1` throughout the restricted domain, alongside an unrestricted witness with `T <= 1`. The domain must specify the frozen matrix, remaining weight ranges or precision, readout size and supplied timing information.

That would establish necessity of **departing from that specified frozen matrix within that domain**. It would not establish universal necessity of recurrent training. A simple prefix-separation argument should not be presumed available: trainable input weights, gates and readout may retain substantial representational flexibility.

## CONSULT #19 RESPONSE (2026-10-21 ~2:23 AM ET)

**Verdict: FREEZE WITH NAMED EDITS.** Keep tau = 0.25 and the 30-run design. The main repair is logical: an initialization that already meets the target is an existence witness, even though it cannot demonstrate acquisition. The current eligibility rule incorrectly excludes it.

This remains below C4, within the GRU family. Scientific clearance does not authorize training.

**Findings 1-4**

1. **Parameter counts: correct.** R-FIX-48 matches CAND's trainable count, not stored count, allocation or optimization geometry. Replace:

   > "The two R-FIX arms therefore separate two explanations..."

   with:

   > "R-FIX-32 tests compensation with the original architecture. R-FIX-48 additionally tests compensation with an equal total trainable-parameter count allocated differently. These comparisons do not isolate parameter count from readout width, parameter allocation or optimization effects."

2. **Freezing mode: correct and essential.** Freeze only `weight_hh_l0`. Training W_ih and the biases can change the recurrent dynamics despite that fixed matrix. Do not describe R-FIX as having an entirely untrained or fixed recurrent computation.

3. **Pairing: acceptable.** Retain the current initialization scheme. Assert the full-core equality for all ten seeds, not just the two feasibility examples. Describe the wider head as partially paired; do not imply complete initialization matching.

4. **Target: retain it.** XOR binds in all 30 existing CAND checkpoints; the exception concerns an F-TRAINED checkpoint. This does not establish which component will bind for R-FIX. Tightening tau merely to make it binding would change the question without a compelling scientific reason.

   Replace the disclosure's interpretation with:

   > "The XOR term determines T in all 30 existing CAND checkpoints. The prefix-loss constraint is satisfied with margin in those checkpoints. Which constraint limits R-FIX is unknown; all three target components remain decision-bearing."

**Required edits**

1. **Separate existence from acquisition.** Replace the initialization eligibility rule:

   > "T(init) is descriptive and does not determine eligibility for an existence witness. A valid initialization or final checkpoint that passes the numerical verification rule supplies a witness for its specified frozen W0 and head width. Report initialization witnesses separately. Acquisition of target attainment requires a verified above-target initialization followed by a verified below-target final checkpoint."

   Retain all ten seeds and all 30 scheduled runs regardless of initialization results. Do not replace seeds.

   For the acquisition annotation, use both evaluators to establish `T(init) > 1 + T_BOUNDARY_TOL`. An initialization near the boundary cannot establish the initially-failing condition.

2. **Make numerical decisions consistent and non-overlapping.** Apply the same rule to CAND and both R-FIX arms:

   ```text
   t = 1e-9

   VERIFIED TARGET PASS:
       both evaluators give T < 1 - t

   VERIFIED TARGET FAIL:
       both evaluators give T > 1 + t

   BOUNDARY / NUMERICALLY UNRESOLVED:
       neither condition holds

   Evaluator disagreement beyond the agreement tolerance:
       integrity failure
   ```

   This fixes the overlap between `T <= 1-t` and `abs(T-1) <= t`.

   Define agreement for each normalized component `x, y` as:

   ```text
   abs(x-y) <= 1e-12 + 1e-9*max(abs(x), abs(y))
   ```

   Both evaluators must independently pass the target rule; agreement alone is insufficient. Call these **numerically verified witnesses under the declared float64 evaluation**, not formal real-arithmetic certificates.

3. **Complete the label rules.**

   > "Per arm, report final verified target passes out of ten, initialization witnesses, invalid runs and boundary runs separately. One verified checkpoint supplies an existence witness. At least eight final verified passes earns TARGET REACHED REPRODUCIBLY. If more than two runs are invalid or numerically unresolved, the reproducibility label is UNRESOLVED; otherwise fewer than eight passes gives REPRODUCIBILITY CRITERION NOT MET."

   When zero witnesses are found:

   - If all ten final evaluations resolve above target, use `TARGET NOT REACHED WITHIN DECLARED SEARCH`.
   - Otherwise use `NO VERIFIED WITNESS FOUND`, with unresolved and invalid counts.

   CAND follows the same numerical and evaluability rules. CAND failure still does not invalidate an R-FIX witness.

4. **Strengthen the freezing check without adding training runs.**

   > "For every R-FIX run, assert before optimization that weight_hh is the only frozen parameter tensor, is absent from the optimizer parameter list, and has requires_grad=False. Check after backward that its gradient remains None. Check W0 byte equality after training and after checkpoint reload."

   A `.grad is None` check before backward is vacuous. Test the freezing implementation on a synthetic fixture; do not consume an additional fresh-seed training run.

5. **Remove undefined inherited quantities.** There is no F-INIT arm here, so the old paired `B_prefix` is undefined. Replace it in reporting with:

   ```text
   C_prefix = PD(q*) - L_prefix(final)
   G_prefix = L_prefix(init) - L_prefix(final)
   ```

   Name `G_prefix` "within-run prefix-loss improvement." Neither quantity gates the target.

6. **Correct the witness claim and ledger scope.** Use:

   > "For the reported W0 and head width H, a numerically verified GRU-8 checkpoint reaches the declared target while weight_hh remains at W0 throughout all eight updates. This is a counterexample to the claim that departing from that specified W0 is necessary for this target within the declared architecture. It does not establish success for other frozen matrices or negate the existing causal contribution of trained matrices in other implementations."

   If initialization failed and training succeeded, append:

   > "The target was attained after training input weights, both biases and the readout, without training weight_hh."

   Replace the blanket statement that Q-LEARN and Q-EXIST are unchanged:

   > "Earlier acquisition, transfer and exact-solution results are unchanged. This study can add restricted-class existence evidence and, where the initialization-to-final condition holds, evidence of acquired target attainment. It does not test transfer or add a new causal-organization claim."

7. **Clean the final document before hashing.** Restore the displaced text fragments and correct the historical F-INIT range: the supplied table spans approximately **11.55-17.36**, not 11.5-16.9. Describe the former VAL subset as an **in-sample descriptive subset** here, because it participates in training.

**Section 13 ambiguities**

| Item | Ruling |
| --- | --- |
| 1 | Accept counts and the qualified meaning of matching. |
| 2 | Accept arm-specific naming; bare counts must not identify arms. |
| 3 | Accept, with the freezing checks above. |
| 4 | Accept partial pairing; verify every seed. |
| 5 | Accept identical streams and digest checks. |
| 6 | Accept no selection or restarts. This limits negative conclusions; it is not inherently the strongest search. |
| 7 | Accept uniform-grid L_prefix as primary. |
| 8 | Accept each arm's own trained readout; no transfer step. |
| 9 | Amend witness eligibility and boundary handling as above. |
| 10 | Accept: CAND failure cannot erase a restricted-class witness. |
| 11 | Accept the separately committed checkpoint manifest. |
| 12 | Accept no reruns or replacement; use the revised unresolved rules. |

**Section 14 questions**

1. **Binding component:** keep tau. Report all components and their binding frequencies; do not call the new study effectively XOR-only before observing R-FIX.

2. **Budget:** the primary search is worthwhile because success is informative. Failure is deliberately limited. Do not activate Appendix D automatically. Leave it as a separately specified and approved extension, with exact selection and refit costs counted.

3. **Clipping:** clip each arm's actual trainable parameter set. Do not compute artificial gradients through frozen parameters to imitate CAND's clipping.

4. **Wider-head initialization:** retain partial pairing. An independent head seed would change the design without resolving allocation and width differences.

5. **Witness margin:** 1e-9 is acceptable with the repaired dual-evaluator rule. Float32 evaluation may be descriptive; it need not gate a claim explicitly defined in float64. Dual evaluation is a numerical cross-check, not a validated error bound for real arithmetic.

6. **Ledger:** prefer the explicit scoped counterexample wording above over merely "NOT SUPPORTED." A witness refutes the specified impossibility claim. Broader necessity remains NOT_ESTABLISHED.

7. **Low rank:** if later studied, use the stacked 24x8 update as the primary definition. It has at most `32*k` factor parameters before accounting for factorization redundancy. It tests restricted recurrent-matrix learning, not compensation with no matrix learning.

8. **Finite-class certificate:** worth a feasibility analysis, not yet an exhaustive-search commitment. A later certificate must cover the entire declared finite domain, preserve a verified unrestricted success comparator, and state that its conclusion depends on the chosen bounds and precision. A coarse grid that excludes useful solutions may certify a narrow fact with little bearing on the present continuous model.

**Final approval question**

> "Approve 30 CPU training runs for 'Frozen recurrent matrices with learned compensation': seeds 400-409, with CAND, R-FIX-32 and R-FIX-48 trained once per seed for 4000 steps under the PR #7 recipe, followed by the specified evaluation, once Astra's named edits are applied and the protocol and implementation are frozen? This approval excludes Appendix A, C and D, restarts, hyperparameter searches and additional training runs."

The most valuable outcome would be a valid compensation witness. It would narrow what must be learned without diminishing what the earlier interventions demonstrated causally.
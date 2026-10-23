# Track A lineage triage v1.1: Artificial Autonomy and Organizational Closure

| | |
| --- | --- |
| Owner | Research Delegate (Track A), for Aidan Ahern |
| Date | 2026-10-21. v1 written about 10:30–11:30 AM ET; v1.1 built about 10:45 AM–noon ET |
| Supersedes | `track_a_lineage_triage_v1.md` (sha256 `b4e1a772…7f0b`, left untouched). Built deterministically by `/workspace/scratch/track_a_triage/v1_1/build_v1_1.py` |
| Kind | Planning and assessment only. Nothing was run, trained, re-hashed, committed or pushed |
| Repo | `godofthunder8756/Toward-an-Artificial-Organism`, master `32cfbe6` (2026-10-20 1:39 PM ET) |
| PRs read | #3–#10, all open drafts, fetched read-only (heads listed in §0.2) |
| W-REL | Approved by Aidan at 8:58 AM ET today, recorded in `/workspace/review/c4_reliability_APPROVAL_RECORD.md` (sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`, verified present). Currently running (as relayed by the Specialist). This triage does not touch it and reports no W-REL result |

**Standing rules applied.**
- Read-only on the repo and GitHub; scratch work only, outside the repo.
- No runs and no training.
- No consciousness claim, and no C4 or C5 claim.
- Q-EXIST, Q-LEARN, Q-CAUSE and Q-NECESSITY are kept separate.
- In the organism lineage, a result shown by ablation is labelled **within-model ablation dependence**. It is never relabelled Q-NECESSITY, which in this program means necessity of a learned component relative to a declared restricted class (PR #9 and #10 usage).

**Citation convention.**
- `path` @ `commit` names a file and the commit it is read from.
- For master files the commit is the last commit that touched the file.
- For PR files the commit is the PR head, and the PR link is given.
- Every `path @ commit` pair in this document was machine-checked to exist (§6).
- Anything not verifiable from these sources is marked **UNVERIFIED**.


## Changelog against v1 (`b4e1a772…7f0b`)

1. **Simplest rival, every entry.** All 42 entries (F1–F5, S1–S15, R1–R11, U1–U11) now carry a "Simplest rival" line. It names the simplest established mechanism that could explain the finding, from control theory, RL, dynamical systems, ALife, counting/filtering or external coordination. For F and S entries the line also says whether existing evidence excludes that rival, with citations. F and U entries have it inside their subsection. S and R entries have it in a per-ID list directly under their table.
2. **W-REL.** B4 is labelled **METHOD ONLY, RESULTS PENDING**. U10's status cites the approval record (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6…7687`) and says the check is currently running. The header row is updated to match. No W-REL file or run was touched.
3. **Defaults, not universal rules.** The 8/10 replication bar and the "more than two invalid seeds = UNRESOLVED" rule are restated in B5 as **defaults that each Track B study must freeze in its own protocol**. The PR #8, #9 and #10 wordings are kept as the frozen instances they are. U9's wording follows. B1 and B3 point to B5.
4. **B3 verbatim.** B3 is rebuilt from verbatim excerpts of `frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818` (sha256 `eca2121c…ea40`), sliced byte-exactly by the build script. The excerpts cover §1 arms, §3 target and §3.1 dual-evaluator rule, §4 harness and freezing checks, §6 validity, §7 labels, the §8.1 "Not reached" wording and the §8.3 claim ceiling. v1 had condensed the dual-evaluator block onto fewer lines.
5. **Check script.** `/workspace/scratch/track_a_triage/v1_1/check_v1_1.py` (with `.log`) extends the v1 checks with:
   - a Simplest-rival line per ID, and an exclusion statement plus a citation for each F and S entry;
   - byte-exact B3 excerpts;
   - the B4 label;
   - the U10 approval citation and approval-record sha;
   - the defaults wording;
   - v1 unchanged;
   - a reproducible rebuild.

No category assignment, count, rank or finding changed from v1.

---

## 0. Scope, sources and how the categories are used

### 0.1 Track A question (PI directive, as relayed)

Track A asks whether a system can maintain, reconstruct and adapt its own functional organization. Doing so requires five things:
- separating organizational closure from externally coordinated computation;
- establishing causal necessity through interventions;
- identifying minimal organization;
- producing reusable falsification tests for Track B;
- making sure any new experiment resolves a meaningful uncertainty.

### 0.2 Sources

**Authoritative state on master (32cfbe6):**
- Status: `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`.
- Belief ledger: `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`, with its layer assessments O0–O4 and C0–C7, its collapse ledger and its inactive theory queue.
- Mission audit: `ACI_MISSION_AUDIT_v1.md` @ `a50ae55`.
- Prior-art and reduction audit: `ACI_PRIOR_ART_AND_REDUCTION_v1.md` @ `a72136c`.
- **The belief ledger predates PRs #4–#10.** Their ledger entries live inside each PR (cited per entry) and are not merged.

**Draft PRs.** Each was fetched with `git fetch origin pull/N/head` only. Heads:

| PR | Branch | Head | Base | Link |
| --- | --- | --- | --- | --- |
| #3 | restore-d0ee2bb-frozen-results | `efceef3` | master | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/3 |
| #4 | twostream-admission-certificate | `5d9d8a7` | master | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/4 |
| #5 | twostream-acquisition-study | `88b500a` | master | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/5 |
| #6 | scarcity-v2-c3-certificate | `5f65315` | master | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/6 |
| #7 | recurrent-core-transfer | `379bb01` | PR #5 | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/7 |
| #8 | graded-joint-reversion | `a5225eb` | PR #7 | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/8 |
| #9 | first-order-iso-controls | `4f6fc4c` | master (stacked on #8) | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/9 |
| #10 | frozen-recurrent-compensation | `0329818` | master (stacked on #9) | https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/10 |

**Earlier independent reviews (box, not in the repo).** These were used for recomputed numbers. Each states that it was recomputed from committed artifacts only:
- `/workspace/review/graded_reversion_results_review_v1.md` (PR #8);
- `/workspace/review/fo_control_results_review_v1.md` (PR #9);
- `/workspace/review/frozen_comp_results_review_v1.md` (PR #10, reviewed at `5f6446f`, before the errata commit `0329818`).

**W-REL documents (box).** These are not in the repo:
- `/workspace/review/c4_reliability_exact_check_spec_FINAL.md`, sha256 `ae626b65…adef`;
- `/workspace/review/c4_reliability_assessment_admission_v3_2.md`, sha256 `f35b6f9d…4207`;
- `/workspace/review/c4_reliability_APPROVAL_RECORD.md`.

### 0.3 Categories (as instructed)

- **FOUNDATIONAL.** Load-bearing for the Track A answer. It survived an intervention or ablation plus at least one named rival or integrity check, and later findings rest on it.
- **SUPPORTING.** Real and correctly bounded, but it carries an auxiliary, infrastructure, prerequisite or context role. It can also be a foundational result's weaker or partly failed sibling.
- **REDUNDANT.** Adequately explained by a simpler established mechanism. The mechanism is named from control theory, RL, dynamical systems or ALife. "Redundant" is a statement about the claimed *extra* mechanism. It does not say the measurements were wrong.
- **UNRESOLVED.** The exact missing causal test or formal clarification is stated. Each entry also gives its **relevance**: would resolving it change a scientific conclusion? Each also gives its **stopping criterion**.

Where this triage makes a judgment the repo does not itself record, the entry says **"triage judgment"**.

### 0.4 Repo-integrity note (affects verification, not conclusions)

**Working-tree state.** `git status` in `/workspace/repo` shows 15 tracked `__pycache__/*.pyc` files deleted in the working tree (`__pycache__/` and `e3/__pycache__/`). This triage did not cause it and did not repair it (no repo changes). It does not affect any document cited here.

**Missing frozen rows on master.** Commit `d0ee2bb` (2026-10-02 11:38 PM ET) deleted the frozen rows of 26 result directories from master, including:
- AC67 and AC68;
- AC71 and AC75;
- AC76;
- AC79 (including its seeds-4000 deviation directory) and AC80.

**What PR #3 does.** PR #3 restores them. I compared all 78 deleted paths: the blobs at `efceef3` are identical to `d0ee2bb^` (0 mismatches). Until PR #3 merges, the AC75 and AC79/AC80 row-level evidence cited by K3 cannot be re-audited from master alone.

---

## 1. Summary counts

| Category | Count | IDs |
| --- | --- | --- |
| FOUNDATIONAL | 5 | F1–F5 |
| SUPPORTING | 15 | S1–S15 |
| REDUNDANT | 11 | R1–R11 |
| UNRESOLVED | 11 | U1–U11 |
| **Total** | **42** | |

**Top unresolved questions by consequence** (full ranking in §5):
1. **U1 / J1.** Is the supplied coordinator and interpreter "substrate" or externally coordinated computation?
2. **U2.** Can the system adapt its own organization against a swept fixed-level rival?
3. **U3.** Does a content intervention propagate to the enabling machinery and back (the O3 constitutive loop)?

---

## 2. FOUNDATIONAL

### F1. Production closure (Maturana & Varela clause (i)), bounded, under the substrate convention

**Finding.**
- Every necessary component {W, C, B, description, derived program} meets C1–C5.
- The maintained state {pointer, coordination, route memory, decision state} meets S1–S4.
- The production-dependency network is one strongly connected component with no external root.
- Scope: "within the declared model and operating range, under the accepted substrate convention". It is not "autopoietic" unqualified and not "alive".

**Evidence:**
- `CLOSURE_VERDICT_v1.md` @ `4b85851` (K3 verdict, §1–§3);
- `DEFINITIONS_CHARTER_v2.md` @ `4b85851` (§8 criterion);
- `DEPENDENCY_AUDIT_v2_CORRECTION.md` @ `4b85851`;
- `AC105_RESULTS_v1.md` @ `daf421c` (seeds 5800–5807, 160 rows, six gates pass);
- ledger layers O1, O2 and C0 = SUPPORTED_BOUNDED in `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`;
- `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1 row 1 (HIGH).

**Simplest rival.** *External coordination over an ALife production network.* A conventional artificial chemistry whose turnover is real, but whose organization is held together by a host-supplied scheduler and interpreter. The belief ledger's O2 rival is "conventional production network under identical substrate".

**Excluded?** Partly.
- **Excluded for the components and the maintained state.** Each of {W, C, B, description, program} is produced or replaced, with within-network dependence, on one strongly connected component with no external root (`CLOSURE_VERDICT_v1.md` @ `4b85851` §1; `DEPENDENCY_AUDIT_v2_CORRECTION.md` @ `4b85851`).
- **Excluded for every coordinator *write*.** Each is W-gated through `_cap` (`AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §2 last paragraph; F3).
- **Not excluded for the transition logic and the interpreter.** `advance()` and `prog.choose` "are fixed Python functions with no production edge" (`AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §2). K3 retains them as substrate by convention (`CLOSURE_VERDICT_v1.md` @ `4b85851` §2). This residue is U1.

**Why foundational.** Every later autonomy verdict inherits it by byte-identity composition: A0, A2, A4/I1 and I5.

**Bound (load-bearing).** The verdict carries the J1 classification: `advance()` and `prog.choose` are supplied substrate. Before K3, `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` had issued **UNRESOLVED** on exactly this judgment. See U1.

**Evidence split (stated in K3 §1).** AC105 supplies the operating range. The ablation, turnover and verification facts are inherited from AC10–AC95 and were not re-tested by AC105.

### F2. Within-model ablation dependence of the production network, including functional interruption and rescue while alive

**Finding.** Ablating W, C or B production breaks the organization. Blocking W birth depletes W at about t=63, and 8/8 individuals die with the description intact at death. Cutting W just before reconstruction makes reconstruction fail **while the organism is alive** (`window_reg_writes == 0`), and a machinery-only restoration of W (labelled EXTERNAL) resumes and completes it.

**Evidence:**
- `AC10_RESULTS_v1.md` @ `10f6878` (nine prespecified gates);
- `AC91_RESULTS_v1.md` @ `1fc82f1` (seeds 4200–4203, seven gates pass);
- `AC92_RESULTS_v1.md` @ `125027b` (seeds 4300–4303, six gates pass);
- K3 §1 table.

**Simplest rival.** *Common resource starvation* (dynamical systems): any cut that drains energy or material kills a dissipative system, with no specific dependency structure. A weaker variant is a t=0 kill that shows only that the part is needed at startup.

**Excluded?** Largely, within the model.
- **Starvation.** The AC2 clamped-information contrast and catalyst rescue address it. The status table calls this "bounded evidence" (`AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`, row "Dependence not explained solely by common resource starvation"; `AC2_RESULTS_v1.md` @ `6c6323b`).
- **The t=0 variant.** AC92 excludes it. Reconstruction fails *while alive*, with the content intact, and resumes under a machinery-only W restoration (`AC92_RESULTS_v1.md` @ `125027b`).
- AC91 shows the description intact at death, so the death is not content loss (`AC91_RESULTS_v1.md` @ `1fc82f1`).

**Not excluded:**
- dependence outside the declared model and range;
- W=0 being an absorbing state, a named cascade (`ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1).

**Why foundational.** This is Track A's "causal necessity through interventions" in the organism lineage. It uses the strongest design on record: interruption during function plus a content-free rescue, not a t=0 kill.

**Q-axis.** Within-model ablation dependence. **This is not Q-NECESSITY.**

**Bound.** One model, one operating range. W=0 is an autocatalytic absorbing state, a named cascade (`ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1).

### F3. Coordination writes are enacted by produced machinery, and the succession is coherent and resumable

**Finding.**
- **AC93** makes the coordinator's MODE write W-gated: it refuses at W=0 and binds gradedly in W, and it is inert at the healthy fixed point W=3.
- **AC94** freezes a coherent resumable succession, with four per-individual requirements all holding:
  - source preservation;
  - verified activation, with the pointer switch atomic with the MODE commit (`split_events == 0`);
  - correct removal;
  - a W-funded rate limiter that freezes at W=0 and resumes on a machinery-only rescue.
- The `ungated` comparator reproduces frozen AC92 byte-for-byte (32/32).

**Evidence:**
- `AC93_RESULTS_v1.md` @ `1fe48df`;
- `AC94_RESULTS_v1.md` @ `6db1c47` (seeds 4404–4407, 120 rows);
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb` (historical next-action block).

**Simplest rival.** *External coordination with a cosmetic gate.* A host-supplied sequencer whose resource gate never actually binds, so the produced machinery adds nothing.

**Excluded?** For the writes, yes.
- **The gate binds.** It refuses at W=0 at the single-step level, and a mid-cycle W=0 stall is pinned to the pre-existing copy by the ungated rival arm (`AC93_RESULTS_v1.md` @ `1fe48df`).
- **Changes are attributable.** The AC94 `ungated` comparator reproduces AC92 byte-for-byte (32/32), and the `split` rival differs only in the switch mechanism (`AC94_RESULTS_v1.md` @ `6db1c47`).

**Not excluded:**
- The sequencing *logic* is still supplied (`AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`; U1).
- The gate is inert at the healthy fixed point W=3, so in normal operation it does not distinguish the organism from an ungated sequencer (AC93, "near-equivalence").

**Why foundational.** It moves every paid write on the reconstruction and coordination path onto produced, finite-lived machinery. That is the measurable half of "closure versus external coordination".

**Bound.** The transition *logic* (`advance()`) and the interpreter (`prog.choose`) remain host-supplied. The status file says so explicitly. See U1.

### F4. State sufficiency: no host-side operational memory steers the trajectory

**Finding.**
- **AC95.** The reset-progress flag becomes a maintained RIP bit and the observer is strictly observational. Observer-discard endpoint equivalence holds 16/16 (final `state_hash`), including under a mid-reset W cut followed by a machinery-only rescue.
- **AC96.** The last host-side leak, `alloc.streak`, is internalized. Observer-discard holds 8/8 at a mid-streak discard point.

**Evidence:**
- `AC95_RESULTS_v1.md` @ `d7925cf` (seeds 4408–4411, 136 rows, four gates);
- `AC96_RESULTS_v1.md` @ `d7925cf` (seeds 4412–4415, 24 rows);
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb` (paragraphs AC95 and AC96).

**Simplest rival.** *Hidden host-side memory* (external coordination): host bookkeeping, such as an observer history or a Python dict, silently steers the trajectory.

**Excluded?** At the endpoint, yes.
- Observer-discard leaves the final `state_hash` identical: 16/16 in AC95, 8/8 in AC96 (`AC95_RESULTS_v1.md` @ `d7925cf`; `AC96_RESULTS_v1.md` @ `d7925cf`).
- Source inspection closed both class-C leaks: the reset flag and `alloc.streak` (`AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`).

**Not excluded:**
- **Per-tick steering.** "per-tick trajectory not compared" (status file).
- **Host functions outside the audited architecture.**

**Why foundational.** It is the operational test that the organization's *memory* is organism-side. Track B can reuse it as test T-OBS (Appendix B5).

**Bound.**
- Endpoint equivalence only. "per-tick trajectory not compared" (status file, verbatim).
- Source inspection covers the audited architecture only.

### F5. Reconstruction of the working program from the maintained description

**Finding.**
- AC79→AC80: a generic decode replaces the external recipe, with `rebuild == prog.program` bit-for-bit.
- AC85: masks and actions are stored.
- AC87: an order-preserving decode reproduces the acquired layout.
- The derived program (C9) is a necessary component in K3, and the description with its repair is necessary (K3 §5).

**Evidence:**
- `AC79_RESULTS_v1.md` @ `9245cef`;
- `AC80_RESULTS_v1.md` @ `6a1f4fb`;
- `AC87_RESULTS_v1.md` @ `dc3e428` (seeds 4028–4031, 320 rows, nine gates pass);
- K3 table rows "description" and "program" in `CLOSURE_VERDICT_v1.md` @ `4b85851`.

**Simplest rival.** Either of two mechanisms:
- *An external recipe*: the host re-supplies the program (external coordination).
- *Template copying*: ALife self-replication by copying inherited content, with no reconstruction from the organism's own description.

**Excluded?**
- **The external recipe: yes.** The generic decode replaces `prog.program`, and the rebuild equals it bit-for-bit (`AC80_RESULTS_v1.md` @ `6a1f4fb`; K3 table in `CLOSURE_VERDICT_v1.md` @ `4b85851`).
- **Template copying: not excluded, and not claimed.** Reconstruction decodes inherited, maintained content. The decode format is supplied substrate (`CLOSURE_VERDICT_v1.md` @ `4b85851` §3 item 2), and content invention is blocked (R10).

**Why foundational.** It is the "reconstruct" leg of the Track A question.

**Verification caveat.**
- On master, `ac79_results_v1/`, `ac79_engineering_v1/`, `ac79_deviation_seeds4000_v1/` and `ac80_results_v1/` are absent (deleted in `d0ee2bb`).
- They are restored blob-identical by PR #3 (`ac80_results_v1/rows.jsonl` @ `efceef3`).
- Row-level re-audit from master is therefore **UNVERIFIED** until PR #3 merges.
- Content inherited at development is permitted (charter C4). Content *self-production* is a separate question (R10).

---

## 3. SUPPORTING

| ID | Finding (bounded) | Evidence (path @ commit; PR) | Role / why not foundational |
| --- | --- | --- | --- |
| S1 | AC1–AC4 building blocks confirmed on fresh seeds 5100–5507: paid maintenance of acquired controller information, produced and decaying repair constituents, produced energy-conversion machinery, and a produced boundary with transport effects. AC1, AC2 and AC4 confirm at every declared rate; AC3 confirms at 2/3 rates, with one death recorded (7/8) | `AC1_4_CONFIRMATION_RESULTS_v1.md` @ `9245cef`; `AC1_RESULTS_AND_NEXT_STEP.md` @ `6c6323b`; `AC2_RESULTS_v1.md` @ `6c6323b`; `AC3_RESULTS_v1.md` @ `6c6323b`; `AC4_RESULTS_v1.md` @ `6c6323b` | Components that F1 composes. Same-author confirmation; external peer review is still open (status table row "Independent review") |
| S2 | Description *succession* (copy→verify→switch→remove). The description holds 130/130 bits under succession; without maintenance it degrades by 23–46 bits and the individual dies | `AC80_RESULTS_v1.md` @ `6a1f4fb`; `AC86_RESULTS_v1.md` @ `ae3504a`; `AC87_RESULTS_v1.md` @ `dc3e428`; K3 §5 in `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` | **Capability, not the survival load-bearer**: "in-place repair alone also survives" (A3 §5, verbatim sense). Supports "reconstruct", but replacement is not shown necessary at the 16,384-tick horizon |
| S3 | Boundary-mediated exchange at the material layer (SR-2 site gate). D1 (site vs count), D2 (local) and D3 (semipermeability) each 16/16, on seeds 6500–6507 | `AC114_RESULTS_v1.md` @ `56ea176`; `A4_EXCHANGE_VERDICT_v1.md` @ `508ea30`; `I1_BOUNDARY_CORRECTION_v1.md` @ `508ea30` | The I1 correction limits AC114's closure to {W, C, B}; the five-component verdict does not transfer to AC114. Material layer only |
| S4 | Exchange composes with the five-mechanism closure. G1, G2, G3 and G8 are 16/16 (mechanism level). The survival gates fail on a minority of finals and are retained as failed: G4/G5 2/16, G6 4/16, G7 6/16 | `AC115_RESULTS_v1.md` @ `dfa19ed`; `AC115_ERRATA_v1.md` @ `e2e2ac6`; `I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md` @ `eb79ecb`; `A0_AUTONOMY_VERDICT_v1.md` @ `eb79ecb` | Mechanism-level composition. The survival level is not confirmed (U8) |
| S5 | Level (b) "adaptive autonomy": internalized decision state (Gray streak + allowance-42) held in maintained, damageable, W-gated state. AC105: no survival reversal or relinquishment harm on 80 matched comparisons; it rescues one marginal priority (5804) | `AC96_RESULTS_v1.md` @ `d7925cf`; `AC99_RESULTS_v1.md` @ `4813cf1`; `AC100_RESULTS_v1.md` @ `58094fb`; `AC104_RESULTS_v1.md` @ `98828b5`; `AC105_RESULTS_v1.md` @ `daf421c`; `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1 row 2 | **Supporting for closure** (the S1–S4 decision-state item). **The decision *rule* is classified REDUNDANT (R4)**, and its economics are UNRESOLVED (U7). The repo calls level (b) "ESTABLISHED" (K3 §7); this triage keeps the internalization and separates out the adaptivity claim |
| S6 | Route memory (C7) acquired from the organism's own contact outcomes. AC7: 8/8 correct routes, with targeted erasure causing failure in 6/6 changed-mapping cases. AC8: 8/8 reacquire after remapping, against 0/8 frozen. AC75: erase-on-relinquishment passes all eight gates, and the no-erase rival dies 8/8 under change | `AC7_RESULTS_v1.md` @ `6c6323b`; `AC8_RESULTS_v1.md` @ `6c6323b`; `AC75_RESULTS_v1.md` @ `86aa64d`; `ac75_results_v1/rows.jsonl` @ `efceef3` (PR #3) | Necessary income path in K3. The acquisition mechanism is ordinary trial-and-error association (AC7 itself notes "random ports also viable"). AC75 rows are absent on master (PR #3) |
| S7 | Content↔maintenance coupling for a maintained one-bit cause estimate, after the AC106 correction. AC107: discrimination 0/32 mistakes; storage maintenance confirmed; content-causal (Q2) not established on finals. AC108: both directions, with all seven gates passing. Maintenance→accuracy/use is 16/16. Content→adaptation/production is 16/16 in the move direction. The survival reversal is 12/16 | `AC107_RESULTS_v1.md` @ `ad53ff1`; `AC108_RESULTS_v1.md` @ `5c0b2f1`; ledger O3 = PARTIAL | This is the program's best "maintenance ↔ content" coupling, but ledger O3 marks the constitutive loop PARTIAL (U3). The causal role is behavioural, not survival-level |
| S8 | AC106 corrective work: errata K1 (nine overreach points). It establishes that the AC106 negative is "falsified in engineering" only and that its scope is the candidate *as implemented*. The update rule dropped the `bound` flag (P2), and r4 was never a longer-threshold counter (P1: `HOLD_N == STREAK_N`) | `AC106_ERRATA_v1.md` @ `d8fd25b`; `AC106_ENGINEERING_v1.md` @ `db0ef2f` | Method and scope correction. It prevented a structural-falsification overclaim and fed the AC107 fix |
| S9 | Composition of the estimate with the autonomy architecture. Direct channels are clean (G2, G4, G6 pass). G3/G5 are 12/16 and retained: the corrupted contact rule reschedules reacquisition on 6306 and 6307 | `AC111_RESULTS_v1.md` @ `6b5f163` | Partial composition. The failure is a named interference, not a closure gap |
| S10 | PR #3: frozen result files deleted in `d0ee2bb` are restored blob-identically. I verified 78/78 paths (0 mismatches against `d0ee2bb^`) | `RECOVERY_MANIFEST_d0ee2bb_v1.md` @ `efceef3`; PR #3 | Evidence-integrity prerequisite for F5, S6 and R1 row-level audits. Merge is pending |
| S11 | PR #4: two-stream world-admission certificate **ADMIT**. Exact enumeration over 256 histories, gates (i)–(iv). Per its claim ceiling, "the ordinary three-number chart is the joint posterior in different coordinates" | `twostream_results_v1/RESULTS.md` @ `5d9d8a7`; `TWOSTREAM_PROTOCOL_v1.md` @ `5d9d8a7`; PR #4 | Benchmark infrastructure for W2. Its claim ceiling excludes C2/C3 promotion and organism claims |
| S12 | PR #5: two-stream acquisition. E1 (predictive acquisition) SHOWN. E2 RECURRENT ADAPTATION SUPPORTED. E3 NOT LOCALIZED BY THIS INTERVENTION. The K-FR E3 label is UNRESOLVED, and K-EXACT is NOT CONFIRMED | `acquisition_results_v1/RESULTS.md` @ `88b500a`; `acquisition_results_v1_errata/ERRATUM_v1_claim_ceiling.md` @ `88b500a`; PR #5 | **Q-LEARN** prerequisite for PR #7–#10. Not a Track A closure result |
| S13 | PR #7: recurrent-core transfer. TRANSFER SHOWN 10/10 and E1 REPLICATED 10/10. Matrix-specific reversion is not demonstrated: SPECIFIC(r) 1/10, (z) 3/10, (n) 3/10 | `results_v1_errata/RESULTS_v2.md` @ `379bb01`; `RECURRENT_CORE_TRANSFER_PROTOCOL_FINAL.md` @ `379bb01`; PR #7 | **Q-LEARN** (transfer) only; it is the prerequisite for PR #8–#10. The matrix-specific negative is recorded, not redundant |
| S14 | PR #8: graded joint recurrent reversion. **Q-CAUSE, organization level: SUPPORTED, BOUNDED.** 9/10 fresh seeds (200–209) exceed every one of 32 block-norm-matched isotropic paths and meet materiality. The secondary single blocks are r 0/10, z 0/10 and n 5/10. Four passing seeds have a margin under 10% | `graded_reversion_results_v1/PHASE_B_RESULTS_v3.md` @ `a5225eb`; `graded_reversion_results_v1/results_v1_errata/ERRATA_v3.md` @ `a5225eb`; `GRADED_REVERSION_PROTOCOL_FINAL.md` @ `a5225eb`; PR #8 | Superseded in strength by S15, which adds the first-order-matched family. **Q-CAUSE only; Q-NECESSITY not tested** |
| S15 | PR #9: graded joint reversion exceeds **both** first-order-matched and isotropic controls. REPLICATED at **exactly 8/10** (D_FO 10/10, D_ISO 8/10, M 10/10). Seeds 300 and 301 each lose to a single isotropic draw. Three seed–family margins are under 10% | `first_order_control_results_v1/PHASE_B_RESULTS_v2.md` @ `4f6fc4c`; `first_order_control_results_v1/results_v1_errata/ERRATA_v1.md` @ `4f6fc4c`; `first_order_control_protocol_FINAL.md` @ `4f6fc4c`; PR #9 | The strongest neural **Q-CAUSE** result: a bounded causal contribution of trained weight_hh to prefix-dependent prediction, with the surrounding computation fixed. It is **at the boundary** (U9). It is causal contribution, not necessity, and therefore not foundational for Track A's necessity, closure or minimality aims |

**Simplest rival per supporting entry (with exclusion status).**

- **S1. Simplest rival:** *common resource starvation in a generic dissipative chemistry* (dynamical systems / ALife).
  - *Partly excluded:* the AC2 clamped-information contrast and catalyst rescue ("bounded evidence", `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`), plus fresh-seed confirmation (`AC1_4_CONFIRMATION_RESULTS_v1.md` @ `9245cef`).
  - *Not excluded* at AC3's third rate, which had one death (7/8).
- **S2. Simplest rival:** *in-place repair by redundancy and majority restore* (error-correcting storage).
  - *Not excluded:* "in-place repair alone also survives" (`AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §5). That is why succession is a capability, not the load-bearer.
- **S3. Simplest rival:** *an aggregate count-based intake gate, or a supplied exchange law* (control theory / external coordination).
  - *The count gate is excluded:* D1 site-vs-count is 16/16 (`AC114_RESULTS_v1.md` @ `56ea176`).
  - *The supplied law is not excluded:* the "Exchange *law* (gated react actions) still supplied" (`ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1 row 3).
- **S4. Simplest rival:** *externally coordinated, non-interacting modules* (external coordination; ledger O4 rival "externally coordinated modules").
  - *Excluded at mechanism level:* G1 byte-identity to AC105 and the G2/G3 discriminations, with all six functions exercised in the same organisms 16/16 (`AC115_RESULTS_v1.md` @ `dfa19ed`).
  - *Not excluded for whole-organism unity:* O4 NOT_ESTABLISHED (`I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md` @ `eb79ecb`).
  - *Not excluded at survival level:* G4–G7 retained as failed (`AC115_ERRATA_v1.md` @ `e2e2ac6`).
- **S5. Simplest rival:** for the internalization, *a host-side counter* (external coordination); for the rule, *a fixed failure-count threshold with a fixed budget* (control theory; R4).
  - *The host counter is excluded* as the steering memory: observer-discard 8/8, with the streak held in maintained, W-gated state (`AC96_RESULTS_v1.md` @ `d7925cf`).
  - *The fixed-threshold rival is not excluded* (R4).
  - *Note:* the host control *outperforms* the internalized streak economically, 8/8 vs 2/8 relinquish (same file; U7).
- **S6. Simplest rival:** *blind random-port search, or tabular associative (bandit) learning* (RL).
  - *Blind search is excluded* as the explanation of use: targeted erasure causes failure in 6/6 changed-mapping cases (`AC7_RESULTS_v1.md` @ `6c6323b`); remapped reacquisition is 8/8 vs 0/8 frozen (`AC8_RESULTS_v1.md` @ `6c6323b`); no-erase dies 8/8 (`ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.4 item 3).
  - *Blind search is not excluded for viability:* "random ports also viable" (`AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`).
  - *Associative learning is not excluded* and is not claimed to be.
- **S7. Simplest rival:** *a same-information direct (reactive) diagnostic, or the first-order streak counter* (counting / filtering).
  - *Not excluded for storage:* the direct diagnostic matches 48/48 in the clean world (`AC109_ENGINEERING_v1.md` @ `d7e24fa`).
  - *Excluded for maintenance→content:* cutting the paid write leaves the estimate inaccurate 16/16 (`AC108_RESULTS_v1.md` @ `5c0b2f1`).
  - *Content→adaptation* (force_machinery 16/16) shows that the content is used. It does not distinguish maintained content from the same content read directly.
- **S8. Simplest rival:** *implementation defect*, not structural absence. The update rule dropped `bound`, and r4 duplicated r2.
  - *Adopted rather than excluded:* the errata endorses this reading (`AC106_ERRATA_v1.md` @ `d8fd25b` P1, P2).
- **S9. Simplest rival:** *independent superposition* (two mechanisms that do not interact).
  - *Excluded for the direct channels:* G2, G4 and G6 pass (`AC111_RESULTS_v1.md` @ `6b5f163`).
  - *Refuted as the full account:* the interference on 6306 and 6307 (G3/G5 12/16) shows a real interaction.
- **S10. Simplest rival:** *regenerated or altered files substituted for the originals.*
  - *Excluded:* all 78 restored blobs equal `d0ee2bb^` (this triage, `git rev-parse` comparison; `RECOVERY_MANIFEST_d0ee2bb_v1.md` @ `efceef3`).
- **S11. Simplest rival:** *an ordinary Bayesian joint filter* (counting / filtering).
  - *Not excluded, by design.* The certificate states that the chart *is* the joint posterior in different coordinates. Its claim ceiling forbids reading more into it (`twostream_results_v1/RESULTS.md` @ `5d9d8a7`). The mean-field arm was "not run" (same file).
- **S12. Simplest rival:** *a product-of-marginals (mean-field) filter, or readout-only learning on a fixed core* (counting / filtering; reservoir computing).
  - The labels are E1 SHOWN, E2 RECURRENT ADAPTATION SUPPORTED and E3 NOT LOCALIZED (`acquisition_results_v1/RESULTS.md` @ `88b500a`).
  - Which comparison E2 uses to exclude the readout-only rival is **UNVERIFIED in this triage** (not re-read).
  - Localization is not established.
- **S13. Simplest rival:** *readout and gain tuning on a fixed recurrent core* (reservoir computing / echo-state networks).
  - *Excluded within the declared grid:* "ADVANTAGE OVER TUNED FROZEN GRU-8 (843 TRAINABLE) OBSERVED (10/10), within the declared grid", and F-INIT A-FIT 0/10 (`results_v1_errata/RESULTS_v2.md` @ `379bb01`).
  - *Not excluded outside the grid:* selection hit the grid edge, g=2 in 10/10 seeds (same file).
- **S14. Simplest rival:** *generic loss-aligned displacement*: any equal-norm perturbation with a large first-order loss projection (first-order sensitivity).
  - *Not excluded by PR #8*, which used isotropic controls only (`GRADED_REVERSION_PROTOCOL_FINAL.md` @ `a5225eb` §4).
  - PR #9 addresses it (S15).
- **S15. Simplest rival:** *first-order (tangent-matched) displacement, and isotropic equal-norm displacement.*
  - *Excluded at 8/10 for the sampled families:* D_FO 10/10, D_ISO 8/10 (`first_order_control_results_v1/PHASE_B_RESULTS_v2.md` @ `4f6fc4c`).
  - *Not excluded for:*
    - unsampled perturbation families;
    - single extreme draws (each failing seed lost to one ISO path);
    - readout-compatibility disruption ("does not eliminate differential disruption of compatibility among recurrent matrices, input weights, biases and the readout", `GRADED_REVERSION_PROTOCOL_FINAL.md` @ `a5225eb` §4).

**Context-only PR (listed for completeness, not a Track A finding).** PR #6, the scarcity_v2 C3 pressure-and-representability certificate:
- Corrected labels: SEL ADMIT, ACC REJECT-SIG, UPK and UPK_cue ADMIT, ROUTE ADMIT, ADAPT VALUE-ONLY.
- Sources: `scarcity_v2_study/results_v1_errata/RESULTS_v2.md` @ `5f65315` and `scarcity_v2_study/SCARCITY_V2_PROTOCOL_FINAL.md` @ `5f65315`.
- It certifies existence inside specified mathematical policy classes. It is a Track B (C3) input and is not counted in §1.

---

## 4. REDUNDANT (named simpler mechanism)

| ID | Claimed extra mechanism | Reduces to (named mechanism, field) | Evidence (path @ commit) | What survives |
| --- | --- | --- | --- | --- |
| R1 | Self-monitoring and self-repair loop (AC67/AC71): "pays to repair its own corruption" | **Fault detection with a fixed corrective action**: a watchdog or threshold-triggered homeostatic regulator (control theory). One bit drives one fixed action, read from host-side observation each tick; nothing is stored, maintained or produced | `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.6 item 1; collapse ledger "watchdog self-monitor" in `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`; `AC71_RESULTS_v1.md` @ `a7f417d` (rows in PR #3) | The read/repair *convention* lesson (AC67→AC71): align the read threshold with the repair trigger. That is engineering, not cognition |
| R2 | Adaptive maintenance allocation / "acquire the need to allocate or relinquish" (AC11) | **State-blind open-loop duty cycle at a fixed level** (control theory). Fixed duty 1/2 gives 4/6 alive, and the adaptive family matches it or is beaten by it; the learner's own threshold is irrelevant. "The optimum can be a level, not a switch" | `AC11_DESIGN_CONTROLS_v2.md` @ `c348a67`; `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.6 item 6 | The rule "sweep the fixed-level family before claiming a switch" (Appendix B6). The question was "not well posed here" (U2) |
| R3 | Experience-dependent exploration adjustment (AC6) | **Constant-rate exploration** (RL: fixed-ε exploration). Fixed rates 1/1024 and 1/2048 pass all original AC6 behavioural criteria on eight new seeds, with no net material saving | `AC6_FIXEDRATE_RESULTS_v1.md` @ `6c6323b` | Local relinquishment and reacquisition are viable; adaptivity of the rate is not needed |
| R4 | *Adaptivity* of the internalized decision rule (Gray streak threshold + allowance-42), as distinct from its internalization (S5) | **Failure-count threshold with a fixed budget** (control theory: counter/integrator threshold with saturation; a sequential-test stopping rule). Gray coding is "a cost lever, not a semantic change"; the reserve designs AC97/98 starve the decision they fund; AC102/103 find no universal spending policy. **Triage judgment**: the repo labels level (b) ESTABLISHED and does not call the rule redundant | `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1 row 2 and §2.1 item 3; `AC106_ENGINEERING_v1.md` @ `db0ef2f` (r2 = "the frozen Gray streak (STREAK_N=6, the history-based rival)") | The internalization (S5) |
| R5 | AC106 maintained cause-belief (second-order "E_world vs E_machinery" estimate) | **The frozen first-order failure-streak counter** (r2); in control terms, counter-based change detection. Errata P8: "the estimate is redundant with the frozen first-order machinery" | `AC106_ERRATA_v1.md` @ `d8fd25b` P8; `AC106_ENGINEERING_v1.md` @ `db0ef2f` (engineering seeds 0–7, 288 rows) | Integration is not falsified (P8: observer-discard passes). Redundancy is a utility claim about the implementation as built (P2 defect) |
| R6 | Persistent storage of the cause estimate (AC109, clean two-cause world) | **Reactive policy on a sufficient current observation**: a direct diagnostic read at decision time (RL/control: Markov reactive controller). It matches the stored estimate on 48/48 cells at lower cost | `AC109_ENGINEERING_v1.md` @ `d7e24fa` | Content is load-bearing as a selector (S7); storage is not, where the observation is decisive. History load-bearing by design is C2 (`C2_TASK_DESIGN_v1.md` @ `6875f38`) |
| R7 | "Continuous repair sustains the estimate's correctness" (AC110) | **Re-estimation from fresh evidence** (filtering: state re-derived at open in-window contacts; reacquisition). G2/G3 16/16 independent of repair; repair matters only post-window (G4 8/16) | `AC110_RESULTS_v1.md` @ `928b938` | Correctness and retention are temporally separable (Appendix B7) |
| R8 | Reliability "monitor" as a second-order predictor (AC117 harness) | **Directional-repair control** (control theory). Prediction is matched by the transient damage count `ones>=4`, and the harness is vacuous at ambient damage | `AC117_RESULTS_v1.md` @ `bd26525` (seeds 6800–6815) | CONTROL-yes, PREDICTION-no. The W-REL exact check is the program's current theory-stage follow-up (U10) |
| R9 | Graded / weighted posterior (C4 probe, P2/R2, AC113) | **Integer counting statistic with a threshold** (sequential probability-ratio rule, `N = ceil(logit θ/LR)`). AC113: no demonstrated advantage (sign-flip p ≈ 0.71 / 0.63, n=8) | `R1_AC113_REANALYSIS_v1.md` @ `38a19ae`; `AC113_RESULTS_v1.md` @ `aebb753`; `R2_P2_PROOF_CORRECTION_v1.md` @ `38a19ae` | Cognition-track cross-reference. "Format is not cognitive necessity" |
| R10 | Self-directed content production (AC72/73/77/78) | **Convergence to a path-dependent, seed-specific fixed point** (dynamical systems; N_eff ≈ 1 per life). Content self-production is blocked structurally, not by a weak learner | `AC78_ENGINEERING_v1.md` @ `9245cef`; `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.6 item 8 | Inherited content is permitted (charter). Organization regeneration and content invention are separate problems |
| R11 | Explicit maintained self-state V for allocation (neural bridge, Phase II) | **Same-information reactive policy and a 3-line sufficient-statistic threshold rule** on raw observables (control/RL). P_rb matches the candidate (op 0.823 vs 0.895, sign-flip p = 0.64); rule 9_d attains the oracle (op 1.000) | `BRIDGE_PHASE2_VERDICT_v1.md` @ `40528f8`; ledger O1/C1 counterevidence | "Explicit V is unnecessary in the tested task" |

**Simplest rival per redundant entry.** For REDUNDANT entries the simplest rival *is* the reduction, and existing evidence supports it.

- **R1. Simplest rival:** watchdog fault detection with a fixed corrective action (control theory).
- **R2. Simplest rival:** state-blind open-loop duty cycle at a fixed level (control theory).
- **R3. Simplest rival:** constant-rate (fixed-ε) exploration (RL).
- **R4. Simplest rival:** failure-count threshold with a saturating counter and a fixed budget (control theory; sequential stopping rule). This remains a triage judgment.
- **R5. Simplest rival:** the frozen first-order failure-streak counter, used as counter-based change detection (counting / filtering).
- **R6. Simplest rival:** a reactive (Markov) policy on the decisive current observation (RL / control).
- **R7. Simplest rival:** re-estimation from fresh in-window evidence, i.e. filtering refresh or reacquisition (counting / filtering).
- **R8. Simplest rival:** directional-repair control plus a transient damage count `ones>=4` (control theory / counting).
- **R9. Simplest rival:** an integer counting statistic with a threshold, as in a sequential probability-ratio rule (counting / filtering).
- **R10. Simplest rival:** convergence to a path-dependent, seed-specific fixed point (dynamical systems).
- **R11. Simplest rival:** a same-information reactive policy, or a 3-line sufficient-statistic threshold rule (control / RL).

---

## 5. UNRESOLVED (exact missing test or clarification, relevance, stopping criterion)

Ranked by consequence for a Track A conclusion. **Relevance** asks: would resolving this change a scientific conclusion on record?

### U1 (rank 1). J1: supplied coordinator and interpreter — substrate, or externally coordinated computation?

**What is open.**
- K3 resolves J1 "substrate" **by convention**: "a modeling choice, not a measurement".
- A3 had issued UNRESOLVED on the same evidence and noted that the AC90 review "did not affirm" the substrate reading.
- K3 itself records `advance()` as "a **larger** substrate concession than `prog.choose`".
- The Track A directive explicitly requires separating closure from externally coordinated computation. That is exactly this locus.

**Evidence:**
- `CLOSURE_VERDICT_v1.md` @ `4b85851` §2;
- `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §3 and §7;
- `DEFINITIONS_CHARTER_v2.md` @ `4b85851` §9;
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb` (the "transition LOGIC (`advance()`) and the interpreter (`prog.choose`)" paragraph).

**Exact missing clarification (formal, before any run).** A substrate-admissibility rule that is stated in advance and independent of this organism. For example:
- *Content-independence:* the supplied function must be the same for every organization the substrate can host, so that it encodes no organization-specific sequencing.
- *Replaceability:* the function's role can be realized by a generic local reaction-rule interpreter that is itself on the production cycle.

The rule is then applied to `advance()` (copy→verify→switch→remove with a built-in verify gate) and to `prog.choose`.

**The empirical half, if the rule demands it.** A within-model replacement of `advance()` by a sequence encoded in maintained or produced state and executed by a generic step rule. Then repeat the F3/F4 tests on that version: interruption, machinery-only rescue and observer-discard.

**Dependency flags:**
- This may require a protected controller or a new architecture family. Both are excluded by the standing rules without approval.
- A2 argues the fully general question is an infinite regress. Only a **declared, finite** admissibility rule is decidable.

**Simplest rival.** *External coordination*: a host-supplied sequencer (`advance()`) and interpreter (`prog.choose`) that carry the organization, while the produced machinery only funds their writes.

**Relevance: YES, high.**
- If `advance()` fails the rule, F1 drops from "SUPPORTED (bounded)" to charter-v2 re-assessment, with the coordinator failing C2.
- If it passes, F1 stands with a rule rather than a convention.
- Either way the flagship Track A sentence changes.

**Stopping criterion.** Stop once an admissibility rule is fixed and applied, or once Astra rules the question out of scope. Do not run an experiment before the rule exists.

### U2 (rank 2). Adaptation of the system's own functional organization

**What is open.**
- The status file row "New maintenance dependencies acquired autonomously" is **NOT ESTABLISHED**.
- AC11 was falsified by its own controls (R2).
- AC6 adaptivity is unnecessary (R3).
- Content self-production is blocked (R10).
- The decision rule reduces to a fixed threshold and budget (R4).
- Bridge allocation reduces to a reactive rule (R11).
- So the "adapt" leg of the Track A question has no positive result. "Maintain" (F1–F4) and "reconstruct" (F5) do.

**Evidence:**
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb` (row "New maintenance dependencies acquired autonomously");
- `AC11_DESIGN_CONTROLS_v2.md` @ `c348a67`;
- `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §2.5 items 5 and 6. In the frozen economy, maintenance was priced at about 25× its payoff, so a cost/benefit trade-off was absent.

**Exact missing causal test.**
- A world whose economy is checked analytically, *before* any run, to contain a genuine maintenance trade-off. The best *fixed level* must be strictly worse than the oracle state-dependent policy, by a declared margin.
- An organism-internal adaptation of its maintenance allocation that beats the **entire swept fixed-level family** and a same-information reactive rule. These are Appendix B6 rivals.
- An intervention that reverses the adaptation when the acquired state is scrambled, with matched expenditure (AC106 P5 lesson).

**Simplest rival.** *A fixed-level duty cycle, or a same-information reactive threshold rule* (control theory). These already reproduce every adaptive candidate on record (R2, R3, R11).

**Relevance: YES, high.**
- A positive result would add the first established "adapt own organization" claim.
- A clean negative with the analytic trade-off certified would retire it.
- Today nothing is concluded.

**Stopping criterion.** If the analytic check shows that no fixed-vs-adaptive gap exists in any admissible world of the declared family, stop and record "not well posed". Do not run organism finals.

### U3 (rank 3). O3 constitutive loop: does a content intervention alter the enabling machinery and then future content?

**What is open.** Ledger O3 = PARTIAL: "maintenance affects content and content affects adaptation; full constitutive loop unestablished".
- AC108 shows content → adaptation/production (force_machinery) and maintenance → content.
- It does not show a closed loop in which content changes the machinery that later regenerates content.

**Evidence:**
- `ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c` (layer O3);
- `AC108_RESULTS_v1.md` @ `5c0b2f1`;
- `ACI_PRIOR_ART_AND_REDUCTION_v1.md` @ `a72136c` ("Cross-route discriminator": "what is restored, and whether it restores the conditions enabling restoration").

**Exact missing causal test** (ledger `next_falsifier`, made operational).
1. Apply a matched-current-observation content intervention at t0.
2. Measure (a) a change in the *production or repair* of the enabling machinery during t0..t1 (for example W-gated repair writes or the description repair schedule).
3. Measure (b) a change in *content regenerated* after t1 that is mediated by (a). Mediation is shown by a second arm that clamps the machinery change while leaving the content intervention intact, so (b) must vanish.
4. Rivals:
   - a world-state-only controller;
   - the inactive-queue reduction "production-versus-state-regrowth dependency audit" (`ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json` @ `a72136c`, inactive_theory_queue).

**Simplest rival.** *Ordinary state estimation with intact, supplied machinery* (counting / filtering): a world-state-only controller whose content changes behaviour but never the machinery that regenerates content.

**Relevance: YES, high.** It decides whether closure extends from the material and production layer (O1/O2) to the informational and functional organization (O3), which is the "functional organization" in the Track A question.

**Stopping criterion.** If the clamp arm shows that (b) occurs without (a), the loop reduces to ordinary state estimation; record it REDUNDANT and stop.

### U4 (rank 4). Q-NECESSITY of recurrent-matrix learning (PR #10)

**What is open.**
- R-FIX-32 and R-FIX-48 both return **TARGET NOT REACHED WITHIN DECLARED SEARCH**, with 0/10 final verified passes, 0 init witnesses, 0 invalid and 0 boundary.
- CAND, the unrestricted comparator, reaches target 10/10.
- Q-NECESSITY = **NOT_ESTABLISHED**. "Failure means only 'not reached within declared search.' This is not a necessity certificate."

**Evidence:**
- `frozen_recurrent_compensation_results_v1/stage2/RESULTS.md` @ `0329818`;
- `frozen_recurrent_compensation_results_v1/results_v1_errata/RESULTS_v2.md` @ `0329818` (the ledger, per `results_v1_errata/ERRATA_v1.md` @ `0329818`);
- `frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818`;
- PR #10.

**Exact missing test.**
- *Either* a pre-registered extended R-FIX search (protocol Appendix D) with a fixed grid of LR, steps and restarts, a held-out selection subset, a CAND comparator under the same search, and training-loss curve logging;
- *or* a finite-class bound: inf T > 1 over a declared parameter domain. The review judged a bound infeasible at 651–843 continuous parameters except for a narrow quantized subclass.

**Simplest rival.** *Reservoir computing*: train the input weights, biases and readout on a fixed random recurrent matrix. This is exactly the R-FIX arm, so it is a rival not yet excluded or confirmed beyond the declared search.

**Relevance: asymmetric.**
- **One verified R-FIX witness would change a conclusion.** It would refute, within GRU-8 at that W0 and head width, that weight_hh learning is needed for the target.
- Another failure would **not** change the conclusion: it stays NOT_ESTABLISHED.
- Necessity can only come from a bound.

**Stopping criterion.** Stop after one pre-registered extended search with no witness, unless a bound becomes feasible. Do not iterate searches (forking paths). Any training needs Aidan's approval.

### U5 (rank 5). Minimal organization

**What is open.**
- K3 §5 and A3 §5 classify components as necessary or optional by ablation (AC10/91/92).
- No document shows that the set is *minimal*, meaning that no proper subset meets C1–C5 and S1–S4 and forms a closed strongly connected component.
- Pointer, coordination and decision state are established as maintained state (S1–S4), but not each individually as ablation-necessary at the AC105 body.
- Coordination maintenance is a "state-cleanliness contrast" only (AC87 G6).

**Evidence:**
- `CLOSURE_VERDICT_v1.md` @ `4b85851` §1;
- `AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §5;
- `AC87_RESULTS_v1.md` @ `dc3e428`.

**Exact missing test** (mostly analytic, then a small causal table):
1. An exhaustive check over the declared production graph that no proper subset is a closed strongly connected component with no external root. This is graph work, no simulation.
2. A leave-one-out ablation per maintained-state item at the AC105 body, with a declared functional endpoint (reconstruction completion or income) rather than survival alone.

**Simplest rival.** *A smaller autocatalytic sub-network* (ALife: a minimal autocatalytic set). For example, the W/C/B production loop with the description treated as passive storage.

**Relevance: MEDIUM.** It delivers Track A's "minimal organization" item and could demote an item from necessary to optional. The closure verdict is unaffected unless a necessary component turns out to be removable.

**Stopping criterion.** Stop if step 1 shows the strongly connected component is already minimal and every S-item has an existing ablation. Then record "minimal within the declared component list".

### U6. Clause (ii): whole-organism unity (non-spatial informational core)

**What is open.**
- Clause (ii) is NOT ESTABLISHED: met only at the material layer.
- The "sole remaining genuine limitation" is the non-spatial informational core.
- The finite successor requirements R1–R4 and tests T1–T5 are specified. The S1 spec and its protocol are "AWAITING separate execution authorization".

**Evidence:**
- `A0_AUTONOMY_VERDICT_v1.md` @ `eb79ecb` §4–§6;
- `S1_SPATIAL_SUCCESSOR_SPEC_v1.md` @ `eb79ecb`;
- `I5_INTEGRATED_ORGANIZATIONAL_VERDICT_v1.md` @ `eb79ecb` (c);
- ledger O4 = NOT_ESTABLISHED.

**Exact missing test.** A0 T1–T5:
- T1: localized-read ablation and endogenous restoration;
- T2: retention vulnerability, with a transport-exempt contrast arm;
- T3: mid-function production block plus machinery-only rescue;
- T4: two directed cuts with separable effects;
- T5: observer-discard with exactly one copy.

The falsification clauses are A0 §6 (i)–(iii).

**Dependency flag.** It needs a new component class. The status file calls it "a re-architecture of the supplied physics", so it requires approval under the "no new architecture family" rule.

**Simplest rival.** *External coordination through a declared non-spatial host array*: the informational core is ordinary host memory that space and boundary never touch.

**Relevance.** YES for the full two-clause autopoiesis verdict, which would move from NOT ESTABLISHED for the informational core. NO for any neural or Track B architecture: the mission audit says "NO — defer to the ALife paper".

**Stopping criterion.** Do not start without explicit authorization. If started, stop at the first prespecified falsification clause.

### U7. Economic viability of the internalized decision state

**What is open.**
- AC96: the internalized streak is paid, and in the move world it is starved by the income collapse it exists to pre-empt. The maintained arm relinquishes 2/8 against the host's 8/8, and 6/8 die. The status file calls it "the new open item".
- AC104/AC105 show the allowance economics are seed-dependent: allowance 33 vs 42, the 5804 rescue and the 5603 harm.

**Evidence:**
- `AC96_RESULTS_v1.md` @ `d7925cf`;
- `AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`;
- `CLOSURE_VERDICT_v1.md` @ `4b85851` §5.

**Exact missing test.** An analytic affordability bound: the expected cost of maintaining the decision state against the income it protects, across the declared challenge grid. Then one frozen run only if the bound is not decisive.

**Simplest rival.** *A host-side counter* (external coordination). It is economically better on record: the host relinquishes 8/8 against the maintained arm's 2/8 (`AC96_RESULTS_v1.md` @ `d7925cf`).

**Relevance: LOW for closure** (K3 §5: "Robustness limits are NOT redesign requirements"). Medium for the level-(b) robustness claim.

**Stopping criterion.** Stop at the analytic bound if it is decisive.

### U8. Survival-level composition (AC115 G4–G7; AC68 bimodality; AC39 transfer)

**What is open.** Survival-bundled gates fail on a minority of seeds through early W/C collapse, puncture W/C leaks, and one particle leak.

**Evidence:**
- `AC115_ERRATA_v1.md` @ `e2e2ac6`;
- `AC68_RESULTS_v1.md` @ `6df811b` (rows in PR #3);
- `AC39_ENGINEERING_v1.md` @ `685642f`.

**Exact missing test.** A bimodality-aware survival protocol with a pre-registered lower-bound gate on a disjoint seed family.

**Simplest rival.** *Seed-dependent bistability* (dynamical systems): W/C bimodality with two attractors, and a basin selected by the seed.

**Relevance: LOW.** It would not change F1 or S4; the mission audit calls it "a known wall".

**Stopping criterion.** Do not pursue. Reopen only if a closure claim comes to depend on survival.

### U9. Robustness of PR #9's Q-CAUSE label to additional control draws

**What is open.**
- The REPLICATED label is at exactly 8/10. Each failing seed lost to one isotropic draw.
- Protocol-mandated sentence: "robustness to additional draws is untested".

**Evidence:**
- `first_order_control_results_v1/PHASE_B_RESULTS_v2.md` @ `4f6fc4c`;
- `first_order_control_protocol_FINAL.md` @ `4f6fc4c` §6.1.

**Exact missing test.** A new pre-registered confirmatory study on fresh seeds with more draws per family (for example 128), the same joint rule, and the B5 default bar (8/10, with UNRESOLVED above two invalid seeds) frozen in its own protocol. Not a reanalysis.

**Simplest rival.** *Order-statistic variability* of the maximum over a finite set of random control draws (sampling). The label could move with more draws, without any change in mechanism.

**Relevance: MEDIUM.** It could weaken the bounded Q-CAUSE entry. It cannot touch Q-NECESSITY or closure.

**Stopping criterion.** Run only if a downstream claim relies on Q-CAUSE strength. Otherwise keep the qualifier.

### U10. W-REL exact check (approved and currently running; results pending)

**Status.**
- **Approved by Aidan at 8:58 AM ET, 2026-10-21**, with the verbatim answer "Yes, approve the theory-only study".
- Recorded in `/workspace/review/c4_reliability_APPROVAL_RECORD.md`. File verified present: 1423 bytes, sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`.
- **Currently running**: a cloud agent is implementing and running it, as relayed by the Specialist.
- **Results pending. This triage did not touch the check, its implementation or its outputs.** Progress and the implementation manifest are UNVERIFIED here.

**Evidence:**
- `/workspace/review/c4_reliability_APPROVAL_RECORD.md`;
- `/workspace/review/c4_reliability_exact_check_spec_FINAL.md` (sha256 `ae626b65…adef`);
- `/workspace/review/c4_reliability_assessment_admission_v3_2.md` (sha256 `f35b6f9d…4207`).

**What resolves it.** The six frozen outcome labels per setting (spec §4.5). None is a C4 or consciousness claim.

**Simplest rival.** *The battery's own named count-based and policy-only analytic agents* (counting / filtering): R-CONF-A, R-BLIND/R-CONF-S, R-CG counts, R-HAC-MF, and the policy-minimized PM-ACT.

**Relevance.** Track B (C4 admission) mainly. For Track A it is LOW: it bears on whether an assessment role separates from the named analytic rivals. A **PATTERN REPRODUCED BY NAMED CONTROL** outcome would add a REDUNDANT entry.

**Stopping criterion.** As frozen in the spec: the hard cap of 4 h total and 1 h per item, and no in-place horizon cuts.

### U11. AC116 storage question (suspended at the resolution floor)

**What is open.**
- Maintained counter vs a tuned memoryless rival: exact sign-flip p = 0.0625 with n = 8, which is the floor of the test.
- 0 seeds worse, 5 better, 3 tied.
- "Suspended — not closed, not demonstrated".

**Evidence:**
- `AC116_ERRATA_v1.md` @ `e2e2ac6`;
- `AC116_RESULTS_v1.md` @ `3ebccdf`.

**Exact missing test.** A larger independent seed family (n ≥ 10 gives a floor below 0.05), with a pre-registered clean readout-only intervention (AC116 errata §2).

**Simplest rival.** *A tuned memoryless reactive policy* (RL / control), which nearly ties on record.

**Relevance: LOW.** S0 records it as "not a license for further storage-comparison runs", and the mission audit says it "would not move the architecture".

**Stopping criterion.** Do not pursue.

---

## 6. Verification of this document

**v1.1.** `/workspace/scratch/track_a_triage/v1_1/check_v1_1.py` (log `check_v1_1.log`) runs all v1 checks on this file and the additional v1.1 checks listed in the changelog. The v1 description below is retained.

`/workspace/scratch/track_a_triage/check_citations.py` (with `.log`) extracts every `` `path` @ `commit` `` pair in this file and runs `git cat-file -e commit:path` in `/workspace/repo`. This is read-only, and the result is in the log.

It also checks that:
- the §1 counts equal the entry counts;
- each UNRESOLVED entry has the fields "Exact missing", "Relevance" and "Stopping criterion".

**Figures not re-derived (UNVERIFIED).**
- Numbers quoted from repo documents (gate counts, seeds, p-values) were read from those documents, not re-derived from rows. They are UNVERIFIED at row level except PR #8, #9 and #10, which the earlier independent reviews recomputed.
- The mission audit's "≈25×" economy figure is quoted from `ACI_MISSION_AUDIT_v1.md`. Its primary computation (AC11/AC15 economy check) was not re-traced here.

---

## Appendix. Portable Track B falsification test pack

Each test is stated as a frozen rule with its source. They are portable as *procedures*. Thresholds, seed bars and invalid-seed rules are **defaults that each study must re-freeze in its own protocol** before any outcome exists (B5). Nothing here authorizes a run.

### B1. Graded-reversion AUC directional rule (PR #8)

**Source:** `GRADED_REVERSION_PROTOCOL_FINAL.md` @ `a5225eb` §4, §6 and §7.

**Intervention.** Interpolate the learned component toward its initialization, W(α) = W_T + α·(W_0 − W_T), during the declared steps. Hold the other trained parameters and a fresh readout fixed.

**Controls.**
- 32 random directions per seed, matched per block in Frobenius norm to the displacement, reused across every dose and target.
- Generator `torch.Generator` with seed 40000 + 100·s.
- Zero-displacement blocks get a zero perturbation.

**Curve.** Delta_c(α) = L(c, α) − L(intact). The doses and weights are:

```text
alpha:   0     1/8    1/4    1/2    3/4    1
weight:  1/16  1/8    3/16   1/4    1/4    1/8
```

AUC_c = Σ w_α·Delta_c(α). Negative excesses are retained and nothing is clipped. "It is not a certified integral of the network's continuous dose response."

**Per-seed rules.**
- **(D) Directional:** "D passes iff AUC_REV − max_j AUC_rand,j > eps0."
- **(M) Materiality:** AUC_REV > eps0 **and** AUC_REV ≥ B_prefix/4.

**Eligibility.** A failure is a non-pass, not invalid. The seed must be valid, pass transfer, have B_prefix > eps0, have C_prefix > eps0, and have displacement > eps0.

**Seed bar.** The B5 defaults (8/10, and UNRESOLVED above two invalid seeds) were the frozen PR #8 instance. A new study must freeze its own.

**Integrity.** These have no evidential role, and any failure makes the seed invalid:
- SHAM equals intact within eps0;
- RESTORE reproduces intact within IDENTITY_TOL;
- checkpoint sha256 values match;
- outputs are finite and in (0, 1).

**The comparison is empirical and directional, not a calibrated p-value.** Reversion toward initialization is not exchangeable with isotropic directions.

### B2. Conjunctive FO + ISO matched controls (PR #9)

**Source:** `first_order_control_protocol_FINAL.md` @ `4f6fc4c` §4, §6, §6.1 and §7.

**Families.** FO paths are matched to REV's first-order (gradient-projection) effect per block. ISO paths are B1's isotropic norm-matched directions. Both have 32 paths.

**Rule** (verbatim):

```text
D_FO  = (AUC_REV - max_j AUC_FO,j > eps0)
D_ISO = (AUC_REV - max_j AUC_ISO,j > eps0)
D     = D_FO and D_ISO

Joint pass = valid and eligible and D_FO and D_ISO and M
```

**Count rule.** "Separate eight-seed successes against each family are insufficient."

**Thin-margin rule** (reporting only). A joint-passing seed is *thin for family F* if max_j AUC_F,j > eps0 and margin_F < 0.10·max_j AUC_F,j. If the label is REPLICATED but fewer than eight joint passes are non-thin for both families, print verbatim:

> "The REPLICATED label depends on at least one seed whose directional margin against at least one family is below 10% of that family's most damaging sampled path; robustness to additional draws is untested."

**Diagnostic.** AUC − FO_AUC is a "residual after subtracting the initial tangent contribution", **not a curvature estimate**.

### B3. R-FIX freeze and compensation test (PR #10): verbatim rules

Track B considers this the most important test, so every rule below is quoted verbatim, not paraphrased.

**Source.** `frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818`, PR #10 (https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/10). Protocol sha256 `eca2121c5972138580ebd8ababb1cd40879a4c20404e925e129becd7e778ea40`. It is byte-identical to `/workspace/review/frozen_recurrent_compensation_protocol_FINAL.md`.

**How the excerpts were made.** Each fenced excerpt is sliced byte-exactly from that file by `build_v1_1.py`, and `check_v1_1.py` re-verifies each one as an exact substring. Section numbers inside the excerpts are the protocol's own.

**Excerpt 1. §1 arms table and parameter-matching statement**

````text
| arm | head H | frozen | trainable | # trainable | # stored total |
| --- | --- | --- | --- | --- | --- |
| **CAND** | 32 | nothing | everything | **843** (456 + 387) | 843 |
| **R-FIX-32** | 32 | `weight_hh_l0` = W0 (192) | W_ih, b_ih, b_hh, readout | **651** (216 + 48 + 387) | 843 |
| **R-FIX-48** | 48 | `weight_hh_l0` = W0 (192) | W_ih, b_ih, b_hh, readout | **843** (216 + 48 + 579) | 1035 |
| (R-FIX-70, not run) | 70 | `weight_hh_l0` | as above | 1107 (264 + 843) | 1299 |

> "R-FIX-32 tests compensation with the original architecture. R-FIX-48 additionally tests compensation with an equal total trainable-parameter count allocated differently. These comparisons do not isolate parameter count from readout width, parameter allocation or optimization effects."
````

**Excerpt 2. §3 target definition**

````text
T(θ) = max( L_prefix(θ) / (τ·PD(q*)), E_total_TEST(θ) / thr_total_TEST, E_XOR_TEST(θ) / thr_XOR_TEST ).

τ = 0.25. The target is L_prefix ≤ 0.25·PD(q*) AND both TEST A-FIT inequalities (consult #18 §7). Numerical decisions follow the dual-evaluator rule of §3.1.
````

**Excerpt 3. §3.1 numerical decision rule (dual evaluator), complete**

````text
### 3.1 Numerical decision rule (consult #19, Edit 2; applies identically to CAND, R-FIX-32 and R-FIX-48, at init and final)

The two evaluators are:
- (E1) the frozen evaluator: `evaluate_arm`, `l_prefix` and `component_excess`;
- (E2) an independent float64 NumPy forward pass and metric implementation.

Each evaluator computes the three normalized components and T independently. Verbatim:

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

Agreement, for each normalized component `x, y`, verbatim:

```text
abs(x-y) <= 1e-12 + 1e-9*max(abs(x), abs(y))
```

Consult #19 verbatim: "Both evaluators must independently pass the target rule; agreement alone is insufficient. Call these **numerically verified witnesses under the declared float64 evaluation**, not formal real-arithmetic certificates."

Float32 (native) evaluation may be reported descriptively. It does not gate any claim (§14 ruling 5). Consult #19 verbatim: "Dual evaluation is a numerical cross-check, not a validated error bound for real arithmetic."
````

**Excerpt 4. §4 harness additions and freezing checks, complete**

````text
## 4. Harness additions (written and frozen with the protocol; engineering only)

1. **`train_arm_rfix(model, episode_seed)`.** PR #7 `train_arm` with exactly one difference: `rnn.weight_hh_l0.requires_grad_(False)`, and every other tensor `True`.
   - The Adam parameter list and `clip_grad_norm_` cover exactly that arm's trainable tensors.
   - §14 ruling 3, verbatim: "clip each arm's actual trainable parameter set. Do not compute artificial gradients through frozen parameters to imitate CAND's clipping."
   - Everything else is identical to `train_arm`: the generator, `sample_batch`, the loss, the LR schedule and the failure checks.
2. **Freezing checks (consult #19, Edit 4, verbatim):**

   > "For every R-FIX run, assert before optimization that weight_hh is the only frozen parameter tensor, is absent from the optimizer parameter list, and has requires_grad=False. Check after backward that its gradient remains None. Check W0 byte equality after training and after checkpoint reload."

   - The "after backward" gradient check runs at every step, or at minimum the first and last step. This is an implementation choice to be fixed at freeze; see ambiguity A4.
   - Byte equality uses sha256 of the tensor bytes, compared with the Stage-0 W0 hash.
   - Any failure makes the run invalid.
3. **Synthetic-fixture test of the freezing implementation (Edit 4).** Verbatim: "A `.grad is None` check before backward is vacuous. Test the freezing implementation on a synthetic fixture; do not consume an additional fresh-seed training run."
   - The fixture is a model built from a non-study seed, on synthetic inputs, run for a handful of optimizer steps.
   - It exercises `train_arm_rfix`'s checks, including a deliberately mis-frozen negative case that must be caught.
   - It is not a study run, has no evidential role, and uses none of seeds 400–409 or streams 1400–1409.
   - It is run as part of implementation freezing, not by this drafting task.
4. **No evaluation of trained models in Stage 1.** Stage 1 logs training loss only. Init checkpoints are evaluated only in Stage 2, together with the finals, so that no outcome information exists before the Stage-1 seal.
````

**Excerpt 5. §6 validity and eligibility, complete**

````text
## 6. Validity (per arm and seed)

A run is **invalid** on any of the following:
- a training integrity failure (non-finite loss, gradients or weights, as in PR #7);
- a checkpoint round-trip mismatch;
- `outputs_valid` false;
- identity checks failing at IDENTITY_TOL;
- any §4 freezing check failing (R-FIX);
- a Stage-0 pairing assertion failing;
- an episode digest mismatch;
- a Stage-2 checkpoint sha not matching the sealed manifest;
- **evaluator disagreement beyond the §3.1 agreement tolerance.**

Invalid checkpoints supply no witness.

**Eligibility: consult #19, Edit 1, verbatim replacement of the initialization eligibility rule:**

> "T(init) is descriptive and does not determine eligibility for an existence witness. A valid initialization or final checkpoint that passes the numerical verification rule supplies a witness for its specified frozen W0 and head width. Report initialization witnesses separately. Acquisition of target attainment requires a verified above-target initialization followed by a verified below-target final checkpoint."

"Retain all ten seeds and all 30 scheduled runs regardless of initialization results. Do not replace seeds."

"For the acquisition annotation, use both evaluators to establish `T(init) > 1 + T_BOUNDARY_TOL`. An initialization near the boundary cannot establish the initially-failing condition."

The acquisition annotation for a run therefore requires both of the following under §3.1:
- init classified VERIFIED TARGET FAIL;
- final classified VERIFIED TARGET PASS.
````

**Excerpt 6. §7 labels, complete**

````text
## 7. Labels (per arm; decided only in Stage 2)

**Witnesses.** A **numerically verified witness under the declared float64 evaluation** is a valid checkpoint, initialization or final, classified VERIFIED TARGET PASS under §3.1.

- R-FIX final witnesses need W0 byte-equal after training and after reload.
- An init checkpoint has `weight_hh` = W0 by construction, so a verified-pass initialization is an existence witness for its W0 and head width.
- Because the CAND and R-FIX-32 inits of a seed are identical, one such init witness is a single witness. It is reported once, under H = 32, with CAND noted. See ambiguity A1.

**Label rules (consult #19, Edit 3, verbatim):**

> "Per arm, report final verified target passes out of ten, initialization witnesses, invalid runs and boundary runs separately. One verified checkpoint supplies an existence witness. At least eight final verified passes earns TARGET REACHED REPRODUCIBLY. If more than two runs are invalid or numerically unresolved, the reproducibility label is UNRESOLVED; otherwise fewer than eight passes gives REPRODUCIBILITY CRITERION NOT MET."

When zero witnesses are found (verbatim):
- "If all ten final evaluations resolve above target, use `TARGET NOT REACHED WITHIN DECLARED SEARCH`."
- "Otherwise use `NO VERIFIED WITNESS FOUND`, with unresolved and invalid counts."

"CAND follows the same numerical and evaluability rules. CAND failure still does not invalidate an R-FIX witness."

**Per-arm report block (mandatory, all three arms):**
- final verified passes: n/10;
- initialization witnesses: count;
- acquisition annotations: count;
- invalid runs: count, with reasons;
- boundary or numerically unresolved runs: count;
- existence label: WITNESS FOUND, `TARGET NOT REACHED WITHIN DECLARED SEARCH`, or `NO VERIFIED WITNESS FOUND`;
- reproducibility label: TARGET REACHED REPRODUCIBLY, REPRODUCIBILITY CRITERION NOT MET, or UNRESOLVED.

**CAND** is the unrestricted comparator. Its labels are reported with the same rules. If CAND does not reach TARGET REACHED REPRODUCIBLY, the R-FIX-vs-CAND comparison is reported as UNRESOLVED (comparator not reproduced). R-FIX witnesses still stand (§13 ruling 10).

There is no pooled R-FIX label and no comparison test between arms. R-FIX-32 vs R-FIX-48 differences are descriptive.

There is no multiplicity correction for existence statements: they are verified-instance claims, not statistical inferences. The search size must be disclosed: 20 final R-FIX checkpoints plus their 20 inits.
````

**Excerpt 7. §8.1 'Not reached' wording and §8.3 claim ceiling**

````text
**Not reached:** "R-FIX-H: TARGET NOT REACHED WITHIN DECLARED SEARCH (one run per seed, 4000 steps, PR #7 recipe, no restarts). Failure means only 'not reached within declared search.' This is not a necessity certificate and does not establish that departing from W0 is necessary."

### 8.3 Claim ceiling (consult #18, verbatim)

> "A certificate must establish `inf T(theta) > 1` throughout the restricted domain, alongside an unrestricted witness with `T <= 1`. The domain must specify the frozen matrix, remaining weight ranges or precision, readout size and supplied timing information."

> "That would establish necessity of **departing from that specified frozen matrix within that domain**. It would not establish universal necessity of recurrent training. A simple prefix-separation argument should not be presumed available: trainable input weights, gates and readout may retain substantial representational flexibility."

The ceiling of this study is one of the following, never a certificate:
- numerically verified existence (or reproducibility) of a witness for the reported W0 and H, under the declared float64 evaluation;
- "not reached within declared search";
- "no verified witness found".
````

**Portability notes (this triage's, not protocol text).**
- τ, the target components, the head widths, the budget and the seed and stream ranges are study-specific. A Track B study must freeze its own.
- The thresholds t = 1e-9 and the agreement formula are PR #10's frozen values. They are a reasonable default for float64 dual evaluation, but they must be re-frozen per study.
- The "at least eight final verified passes" and "more than two runs … UNRESOLVED" clauses are PR #10's frozen instance of the B5 defaults.
- Two-stage seal: Stage 1 trains and seals checkpoint hashes with no target evaluation, then Stage 2 scores. Future practice (PR #10 errata E-D1, `results_v1_errata/ERRATA_v1.md` @ `0329818`) is an immutable Stage 0 manifest plus a dated addendum.

### B4. W-REL named-rival battery (theory-stage) — METHOD ONLY, RESULTS PENDING

**METHOD ONLY, RESULTS PENDING.**
- W-REL was approved by Aidan at 8:58 AM ET (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6…7687`) and is currently running.
- This section states the frozen method only. No outcome, label or statistic from the run is reported or implied.

**Source:** `/workspace/review/c4_reliability_exact_check_spec_FINAL.md` §3, §4.4–§4.6 (box; not in the repo).

**Rivals:**
- R-HAC-MB (reference) and R-HAC-MB-myopic;
- the oracle;
- R-BLIND/R-CONF-S (one control);
- R-CONF-A;
- R-HAC-MF (eligible only at T_SEP = 3);
- R-CG;
- PM-ACT (policy-minimized).

All share the supplied first-order predictor F0 and are exact analytic agents.

**Core criteria:**
- **C-REF.** Δ_R ≥ 1/100 and Δ_M ≥ 1/100.
- **C-T2.** Relative reduction of squared error against the prior-marginal baseline ≥ 1/2. A zero baseline is "not demonstrated", never a pass.
- **C-SEL.** Under I-SWAP, the signed assessment error moves in the predicted direction (≥ 1/100) and the checking probability follows (≥ 1/100), in both directions.
- **C-FO.** Exact equality of pre-check probabilities and binary decisions under every intervention.
- **Rescue.** Signed reversals ≥ 1/100 plus L_A − L_B ≥ 1/100, for I-SWAP-S **and** I-SWAP-E.

**Reproduction rule** (verbatim): "Reproduction is YES only when every required component is available and within tolerance. It is NO when at least one available component demonstrably exceeds tolerance or disagrees on an exact equality flag. Otherwise it is UNRESOLVED, with the unavailable components listed. Missing components are never imputed."

Tolerance: 1/1000 per component.

**Decision order per setting:**
1. UNRESOLVED-COMPUTE;
2. UNRESOLVED-DESIGN (reference undefined);
3. REFERENCE CRITERIA NOT MET;
4. PATTERN REPRODUCED BY NAMED CONTROL;
5. CORE CRITERIA SHARED; FULL RESPONSE PATTERN NOT REPRODUCED;
6. UNRESOLVED-DESIGN (an essential comparison is unavailable, or a reproduction is UNRESOLVED);
7. DISTINGUISHES NAMED CONTROLS.

**Claim lock.** "Policy minimization alone does not establish absence of an assessment role." No outcome is a C4 or consciousness claim.

**Status: METHOD ONLY, RESULTS PENDING.** The check is running, and no result has been read by this triage.

### B5. Seed bar and invalid-seed rule: DEFAULTS each Track B study must freeze

**These are defaults, not universal rules.** Each Track B study must state and freeze its own replication bar and invalid-seed rule in its own protocol, before any confirmatory outcome exists. It may adopt the defaults below or justify different values. A study that does not freeze them has no bar.

**Default 1: replication bar 8/10.**
- At least eight of ten prespecified confirmatory seeds must jointly satisfy validity, eligibility and every per-seed criterion.
- The denominator stays ten, and seeds are not removed from it.
- There is no intermediate band.

**Default 2: more than two invalid seeds = UNRESOLVED.**
- Apply after any prerequisite check, and before the count rule.
- Other eligibility failures remain scientific non-passes. They are not invalidity.

**Default precedence:**
1. Prerequisite not replicated → UNRESOLVED (prerequisite).
2. Default 2.
3. Default 1.

**Frozen instances on record.** These are verbatim and binding only within their own studies:
- **PR #8** (`GRADED_REVERSION_PROTOCOL_FINAL.md` @ `a5225eb` §7): "At least eight of the ten prespecified phase-B seeds jointly satisfy validity, eligibility, D and M. The denominator remains ten; seeds are not removed from it." The precedence is "E1 not replicated" first, then "More than two invalid seeds" gives "UNRESOLVED".
- **PR #9** (`first_order_control_protocol_FINAL.md` @ `4f6fc4c` §7, consult #17 edit 8): "After the E1 prerequisite, if more than two distinct seeds are invalid or have a collapsed control family for the target, report UNRESOLVED (insufficient evaluable seeds). Otherwise retain the denominator of ten."
- **PR #10** (`frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818` §7; see B3 Excerpt 6): "At least eight final verified passes earns TARGET REACHED REPRODUCIBLY. If more than two runs are invalid or numerically unresolved, the reproducibility label is UNRESOLVED; otherwise fewer than eight passes gives REPRODUCIBILITY CRITERION NOT MET."
  - This instance counts *runs* per arm and includes numerically unresolved runs. That shows the default must be adapted and frozen per design.

**Why defaults, not rules.** The bar's power and false-pass rate depend on the per-seed criterion, the number of control draws (U9) and the seed count. A study with a different seed count or criterion must recompute and freeze its own bar.

**Exploratory phase (default).** Use separate seeds. The headline is only "EXPLORATORY (… ; NOT CONFIRMATORY)", with no aggregate verdict.

**Wording (default).** Write "below the declared materiality threshold", never "immaterial".

### B6. Organism-lineage portable tests (Track A → Track B)

These come from the AC record. Each names the failure it catches.

- **T-RIVAL: sweep the fixed-level and reactive family first.** Before claiming an adaptive switch, sweep the state-blind fixed level and the same-information reactive rule (AC11, BRIDGE 9_d). A rival matching the best learner = no acquired decision demonstrated. Sources: `AC11_DESIGN_CONTROLS_v2.md` @ `c348a67` and `BRIDGE_PHASE2_VERDICT_v1.md` @ `40528f8`.
- **T-INTERRUPT: functional interruption plus content-free rescue.** Cut the enabling production *during* the function, not at t=0. Require failure while alive with content intact, and resumption under a machinery-only rescue labelled EXTERNAL. Sources: `AC92_RESULTS_v1.md` @ `125027b`; A0 T3.
- **T-OBS: observer-discard.** Discard the host's observational record mid-function. The trajectory endpoint must be byte-identical (`state_hash`). State whether per-tick comparison was done. Source: `AC95_RESULTS_v1.md` @ `d7925cf`.
- **T-INERT: byte-identity composition license.** Before attributing a difference to a new mechanism, show the change is byte-inert at the intact boundary (G1). Sources: `AC114_RESULTS_v1.md` @ `56ea176` and `AC115_RESULTS_v1.md` @ `dfa19ed`.
- **T-SCRAMBLE: selective, expenditure-matched content ablation.** A scramble must override reads only (writes intact), with matched expenditure. Otherwise it confounds content with cost. Sources: AC106 errata P5 in `AC106_ERRATA_v1.md` @ `d8fd25b`; `AC116_ERRATA_v1.md` @ `e2e2ac6` §2.
- **T-DIRECT: same-information direct rival.** For any stored or maintained state, include a rival that reads the same information at decision time without storage (AC109). Storage must beat it to be load-bearing. Source: `AC109_ENGINEERING_v1.md` @ `d7e24fa`.
- **T-REACQ: correctness versus retention split.** Cut repair while leaving reacquisition intact. Require separate in-window correctness and post-window retention gates (AC110). Source: `AC110_RESULTS_v1.md` @ `928b938`.
- **T-RESTORE: cross-route discriminator.** Ask "what is restored, and whether it restores the conditions enabling restoration". Classify a result as (1) maintained sufficient state, (2) restored activity under intact constraints, or (3) restoration of enabling organization. Source: `ACI_PRIOR_ART_AND_REDUCTION_v1.md` @ `a72136c`.
- **Reporting rules:**
  - seeds, not histories, are the replication unit;
  - survival is a bimodality-aware lower bound;
  - nonsignificance is not equivalence (R1);
  - gate shape must match claim shape (AC16/AC17).

  Sources: `R1_AC113_REANALYSIS_v1.md` @ `38a19ae`; `ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.3.

**B7. Q-separation lock (for every Track B report).**
- Q-EXIST: an exact or supplied solution exists.
- Q-LEARN: acquisition or transfer.
- Q-CAUSE: intervention-based causal contribution.
- Q-NECESSITY: requires a bound or complete search within a declared restricted class.

None upgrades another. No C-level, C4, C5, consciousness or organism conclusion follows from any of them.

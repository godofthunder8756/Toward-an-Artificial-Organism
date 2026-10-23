import hashlib,re,sys
SRC="/workspace/review/track_a_lineage_triage_v1_1.md"; SHA="d2cc9152d58a81c8054e1ddc8c59d4d83cc32f9ea6428b8e331ffe9a64a5d3ef"
raw=open(SRC,'rb').read(); assert hashlib.sha256(raw).hexdigest()==SHA; t=raw.decode()
def ublock(i):
    m=re.search(rf'^### U{i}[\. ]',t,re.M); s=m.start(); n=re.search(r'^(### |---$)',t[m.end():],re.M)
    return t[s:m.end()+n.start()].rstrip('\n')+'\n'
U="\n".join(ublock(i) for i in range(1,12))
head=f"""# Astra digest: Track A lineage triage v1.1

| | |
| --- | --- |
| Source | `/workspace/review/track_a_lineage_triage_v1_1.md` |
| Source sha256 | `{SHA}` |
| Digest of | v1.1 only. v1 (`b4e1a772…7f0b`) and v1.1 are unchanged |
| Built by | `/workspace/scratch/track_a_triage/digest/build_digest.py` (verifies the source sha first) |
| Kind | Planning and assessment only. No runs, no training, no repo changes |

**What the digest contains.**
- **U1–U11** are copied **byte-exactly** from v1.1 §5.
- **F, S and R** entries are one-line condensations. Each cites its v1.1 entry id. Read the full file for evidence and citations.
- **Counts:** FOUNDATIONAL 5, SUPPORTING 15, REDUNDANT 11, UNRESOLVED 11; 42 in total.

---

## 1. FOUNDATIONAL (one line each: claim | simplest rival | excluded?)

- **F1** — Production closure (clause (i)) over {{W, C, B, description, program}} plus S1–S4 maintained state, one strongly connected component, no external root; bounded, under the substrate convention. | Rival: external coordination over an ALife production network. | **Partially excluded.** Excluded for components and for all coordinator writes (W-gated). **Gap:** not excluded for the transition logic and interpreter (`advance()`, `prog.choose`), which are retained by convention (U1).
- **F2** — Within-model ablation dependence: W, C and B production are needed; AC92 shows functional interruption while alive and a machinery-only rescue. | Rival: common resource starvation, or a t=0 kill. | **Largely excluded** within the model: AC2 clamp and rescue ("bounded"), AC92 failure while alive with content intact. **Gap:** generality outside the model; W=0 is an absorbing cascade.
- **F3** — Coordination writes are enacted by produced W machinery, and succession is coherent and resumable (AC93/AC94). | Rival: external coordination with a cosmetic gate. | **Excluded for writes:** the gate refuses at W=0, and the ungated comparator gives 32/32 byte-identity. **Gap:** the sequencing logic is still supplied; the gate is inert at the healthy fixed point W=3.
- **F4** — State sufficiency: no host-side operational memory steers the trajectory (AC95 16/16, AC96 8/8 observer-discard). | Rival: hidden host-side memory. | **Excluded at the endpoint.** **Gap:** per-tick trajectory not compared; host functions outside the audited architecture.
- **F5** — The working program is reconstructed from the maintained description by a generic decode (AC79→AC80, bit-for-bit). | Rival: an external recipe, or template copying of inherited content. | **External recipe excluded. Template copying not excluded** (and not claimed): the decode format is supplied, and content invention is blocked (R10).

## 2. SUPPORTING (one line each: claim | simplest rival | excluded?)

- **S1** — AC1–AC4 building blocks confirmed on fresh seeds (AC3 at 2/3 rates). | Rival: common resource starvation in a dissipative chemistry. | **Partially excluded** (AC2 contrast, "bounded"). **Gap:** AC3's third rate (7/8).
- **S2** — Description succession holds 130/130. | Rival: in-place repair by redundancy and majority restore. | **Not excluded:** in-place repair alone also survives, so succession is a capability, not the load-bearer.
- **S3** — Boundary-mediated exchange at the material layer (AC114, D1–D3 16/16). | Rival: an aggregate count gate, or a supplied exchange law. | **Count gate excluded** (D1). **Gap:** the exchange law is still supplied.
- **S4** — Exchange composes with the five-mechanism closure at mechanism level (AC115). | Rival: externally coordinated, non-interacting modules. | **Excluded at mechanism level** (G1 byte-identity, G2/G3). **Gap:** whole-organism unity is not established (O4), and survival gates G4–G7 failed.
- **S5** — Internalized decision state (Gray streak + allowance-42). | Rival: a host-side counter, or a fixed failure-count threshold with a budget. | **Host counter excluded** as the steering memory (AC96 observer-discard). **Fixed-threshold rival not excluded** (R4). The host control is economically better (8/8 vs 2/8).
- **S6** — Route memory acquired from the organism's own outcomes, with reacquisition and erase-on-relinquish (AC7/AC8/AC75). | Rival: blind random-port search, or tabular associative (bandit) learning. | **Blind search excluded for use** (erasure 6/6, reacquire 8/8 vs 0/8, no-erase dies 8/8). **Gap:** not excluded for viability ("random ports also viable"); associative learning is not excluded and not claimed.
- **S7** — Content↔maintenance coupling of the one-bit estimate (AC107/AC108, 7/7 gates). | Rival: a same-information direct diagnostic, or a streak counter. | **Partially excluded.** Maintenance→content is excluded (paid write cut gives inaccuracy 16/16). **Gap:** storage is not excluded (direct diagnostic 48/48), and content use does not separate maintained content from a direct read.
- **S8** — AC106 errata K1 corrects scope: an engineering negative only. | Rival: an implementation defect rather than structural absence. | **Adopted, not excluded:** the errata endorses the defect reading (P1, P2).
- **S9** — Estimate–autonomy composition: direct channels are clean, but G3/G5 are 12/16 (AC111). | Rival: independent superposition. | **Excluded for direct channels; refuted as the full account** (interference on 6306 and 6307).
- **S10** — PR #3 restores the 78 deleted frozen files. | Rival: altered or regenerated files. | **Excluded:** 78/78 blobs identical to `d0ee2bb^`.
- **S11** — PR #4 world-admission certificate ADMIT. | Rival: an ordinary Bayesian joint filter. | **Not excluded, by design:** the chart is the joint posterior. The mean-field arm was not run.
- **S12** — PR #5 acquisition: E1 SHOWN, E2 RECURRENT ADAPTATION SUPPORTED, E3 NOT LOCALIZED. | Rival: a mean-field filter, or readout-only learning on a fixed core. | **UNVERIFIED in this triage:** I did not re-read which comparison E2 uses to exclude the readout-only rival. Localization is not established.
- **S13** — PR #7 TRANSFER SHOWN 10/10 (Q-LEARN). Matrix-specific effects not demonstrated. | Rival: reservoir computing (readout and gain tuning on a fixed core). | **Excluded within the declared grid** (advantage over tuned frozen GRU-8 10/10; F-INIT A-FIT 0/10). **Gap:** outside the grid; selection hit the grid edge.
- **S14** — PR #8 Q-CAUSE bounded, 9/10 against isotropic paths. | Rival: generic loss-aligned (first-order) displacement. | **Not excluded by PR #8.** It is addressed by PR #9 (S15).
- **S15** — PR #9 Q-CAUSE bounded, exactly 8/10 against both FO-matched and ISO controls. | Rival: first-order-matched and isotropic displacement. | **Excluded at 8/10 for the sampled families.** **Gap:** unsampled families, single extreme draws, and readout-compatibility disruption.

## 3. REDUNDANT (one line each: finding | simpler mechanism)

- **R1** — AC67/AC71 self-monitoring and repair loop | watchdog fault detection with a fixed corrective action (control theory).
- **R2** — AC11 adaptive maintenance allocation | a state-blind fixed-level duty cycle (control theory).
- **R3** — AC6 experience-dependent exploration | constant-rate (fixed-ε) exploration (RL).
- **R4** — Adaptivity of the internalized decision rule | a failure-count threshold with a fixed budget (control theory). This is a triage judgment.
- **R5** — AC106 maintained cause-belief | the frozen first-order streak counter (counting / change detection).
- **R6** — AC109 stored estimate | a reactive policy on the decisive current observation (RL / control).
- **R7** — AC110 "continuous repair sustains correctness" | re-estimation from fresh evidence (filtering / reacquisition).
- **R8** — AC117 reliability monitor as a predictor | directional-repair control plus a transient damage count (control / counting).
- **R9** — Graded/weighted posterior (P2/R2, AC113) | an integer counting statistic with a threshold (sequential ratio rule).
- **R10** — Self-directed content production (AC72–AC78) | a path-dependent, seed-specific fixed point (dynamical systems).
- **R11** — Explicit maintained self-state V (neural bridge) | a same-information reactive rule, or a 3-line sufficient-statistic threshold (control / RL).

---

## 4. UNRESOLVED U1–U11 (byte-exact from v1.1 §5)

"""
tail="""
---

## 5. Caveats (in full)

1. **UNVERIFIED items.**
   - **S12:** the comparison E2 uses to exclude the readout-only rival was not re-read.
   - **U10 / B4:** W-REL progress, implementation manifest and results are not inspected.
   - **Row level:** numbers quoted from repo documents (gate counts, seeds, p-values) were read from those documents, not re-derived from rows. They are UNVERIFIED at row level, except PR #8, #9 and #10, which earlier independent reviews recomputed from committed artifacts.
   - **Economy figure:** the mission audit's "≈25×" economy figure is quoted, not re-traced.
2. **PR #3 re-audit limit.**
   - Commit `d0ee2bb` (2026-10-02, 11:38 PM ET) deleted the frozen rows of 26 result directories from master, including AC67, AC68, AC71, AC75, AC76, AC79 and AC80.
   - PR #3 (head `efceef3`) restores them. All 78 paths are blob-identical to `d0ee2bb^`.
   - Until PR #3 merges, the AC75 and AC79/AC80 row-level evidence (F5, S6, R1) cannot be re-audited from master alone.
   - Separately, the `/workspace/repo` working tree shows 15 tracked `__pycache__` `.pyc` files deleted. This triage did not cause that and did not repair it.
3. **Q-separation lock.** None of the following upgrades another:
   - Q-EXIST: an exact or supplied solution exists.
   - Q-LEARN: acquisition or transfer.
   - Q-CAUSE: intervention-based causal contribution.
   - Q-NECESSITY: requires a bound or a complete search within a declared restricted class.

   Organism results shown by ablation are "within-model ablation dependence", never Q-NECESSITY.
4. **W-REL pending.**
   - Approved by Aidan at 8:58 AM ET on 2026-10-21. The record is `/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`.
   - It is currently running, as relayed by the Specialist.
   - Results are pending. The triage did not touch it.
5. **Claim ceiling.** No C4, C5 or consciousness claim is made or implied anywhere. W-REL outcome labels are not C4 claims. Production closure is bounded to the declared model, operating range and substrate convention; it is not "autopoietic" unqualified and not "alive".

## 6. Pointer: Track B test pack (full file, Appendix B1–B7)

The full v1.1 appendix gives the portable Track B falsification tests, with exact rules and file refs:
- **B1:** graded-reversion AUC directional rule (PR #8).
- **B2:** conjunctive FO + ISO matched controls, with the thin-margin sentence (PR #9).
- **B3:** the R-FIX freeze-and-compensate rules and the dual-evaluator rule, as seven byte-exact excerpts of `frozen_recurrent_compensation_protocol_FINAL.md` @ `0329818`. Track B ranks this test most important.
- **B4:** W-REL named-rival battery, labelled **METHOD ONLY, RESULTS PENDING**.
- **B5:** the 8/10 replication bar and "more than two invalid seeds = UNRESOLVED", stated as **defaults that each Track B study must freeze in its own protocol**, not universal rules. The PR #8, #9 and #10 wordings are frozen instances only.
- **B6:** organism-lineage tests: T-RIVAL, T-INTERRUPT, T-OBS, T-INERT, T-SCRAMBLE, T-DIRECT, T-REACQ, T-RESTORE.
- **B7:** the Q-separation lock.
"""
out=head+U+tail
open(sys.argv[1],'w').write(out); print(len(out.encode()), hashlib.sha256(out.encode()).hexdigest())

"""Deterministic build of track_a_lineage_triage_v1_1.md from v1 (read-only on v1 and repo)."""
import hashlib, re, subprocess, sys
V1 = "/workspace/review/track_a_lineage_triage_v1.md"
V1_SHA = "b4e1a772ee361128f1d88573673c6467d06d2029860bf8c79e9c33b668da7f0b"
APPROVAL = "/workspace/review/c4_reliability_APPROVAL_RECORD.md"
APPROVAL_SHA = "be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687"
PROTO_PATH, PROTO_COMMIT = "frozen_recurrent_compensation_protocol_FINAL.md", "0329818"
PROTO_SHA = "eca2121c5972138580ebd8ababb1cd40879a4c20404e925e129becd7e778ea40"
out = sys.argv[1]

raw = open(V1, "rb").read()
assert hashlib.sha256(raw).hexdigest() == V1_SHA, "v1 sha changed"
assert hashlib.sha256(open(APPROVAL, "rb").read()).hexdigest() == APPROVAL_SHA, "approval record sha changed"
t = raw.decode()
proto = subprocess.run(["git", "-C", "/workspace/repo", "show", f"{PROTO_COMMIT}:{PROTO_PATH}"],
                       capture_output=True, check=True).stdout
assert hashlib.sha256(proto).hexdigest() == PROTO_SHA, "protocol sha mismatch"
proto = proto.decode()

def once(old, new):
    global t
    assert t.count(old) == 1, ("anchor count", t.count(old), old[:80])
    t = t.replace(old, new)

def slice_(start, end, include_end=False):
    i = proto.index(start); j = proto.index(end, i)
    if include_end:
        j = proto.index("\n", j) + 1
    s = proto[i:j].rstrip("\n") + "\n"
    assert proto.count(start) == 1
    return s

# ---------------------------------------------------------------- header + changelog
once("# Track A lineage triage v1: Artificial Autonomy and Organizational Closure",
     "# Track A lineage triage v1.1: Artificial Autonomy and Organizational Closure")
once("| Date | 2026-10-21, written about 10:30–11:30 AM ET |",
     "| Date | 2026-10-21. v1 written about 10:30–11:30 AM ET; v1.1 built about 10:45 AM–noon ET |\n"
     "| Supersedes | `track_a_lineage_triage_v1.md` (sha256 `b4e1a772…7f0b`, left untouched). Built deterministically by `/workspace/scratch/track_a_triage/v1_1/build_v1_1.py` |")
once("| W-REL | Approved by Aidan at 8:58 AM ET today and being implemented and run by a cloud agent. This triage does not touch it and reports no W-REL result |",
     "| W-REL | Approved by Aidan at 8:58 AM ET today, recorded in `/workspace/review/c4_reliability_APPROVAL_RECORD.md` (sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`, verified present). Currently running (as relayed by the Specialist). This triage does not touch it and reports no W-REL result |")

CHANGELOG = """
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
"""
once("\n---\n\n## 0. Scope, sources and how the categories are used",
     "\n" + CHANGELOG + "\n---\n\n## 0. Scope, sources and how the categories are used")

# ---------------------------------------------------------------- simplest rivals: F
F = {
"F1": """**Simplest rival.** *External coordination over an ALife production network.* A conventional artificial chemistry whose turnover is real, but whose organization is held together by a host-supplied scheduler and interpreter. The belief ledger's O2 rival is "conventional production network under identical substrate".

**Excluded?** Partly.
- **Excluded for the components and the maintained state.** Each of {W, C, B, description, program} is produced or replaced, with within-network dependence, on one strongly connected component with no external root (`CLOSURE_VERDICT_v1.md` @ `4b85851` §1; `DEPENDENCY_AUDIT_v2_CORRECTION.md` @ `4b85851`).
- **Excluded for every coordinator *write*.** Each is W-gated through `_cap` (`AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §2 last paragraph; F3).
- **Not excluded for the transition logic and the interpreter.** `advance()` and `prog.choose` "are fixed Python functions with no production edge" (`AUTOPOIESIS_ASSESSMENT_v1.md` @ `7969b14` §2). K3 retains them as substrate by convention (`CLOSURE_VERDICT_v1.md` @ `4b85851` §2). This residue is U1.

""",
"F2": """**Simplest rival.** *Common resource starvation* (dynamical systems): any cut that drains energy or material kills a dissipative system, with no specific dependency structure. A weaker variant is a t=0 kill that shows only that the part is needed at startup.

**Excluded?** Largely, within the model.
- **Starvation.** The AC2 clamped-information contrast and catalyst rescue address it. The status table calls this "bounded evidence" (`AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`, row "Dependence not explained solely by common resource starvation"; `AC2_RESULTS_v1.md` @ `6c6323b`).
- **The t=0 variant.** AC92 excludes it. Reconstruction fails *while alive*, with the content intact, and resumes under a machinery-only W restoration (`AC92_RESULTS_v1.md` @ `125027b`).
- AC91 shows the description intact at death, so the death is not content loss (`AC91_RESULTS_v1.md` @ `1fc82f1`).

**Not excluded:**
- dependence outside the declared model and range;
- W=0 being an absorbing state, a named cascade (`ACI_MISSION_AUDIT_v1.md` @ `a50ae55` §1.1).

""",
"F3": """**Simplest rival.** *External coordination with a cosmetic gate.* A host-supplied sequencer whose resource gate never actually binds, so the produced machinery adds nothing.

**Excluded?** For the writes, yes.
- **The gate binds.** It refuses at W=0 at the single-step level, and a mid-cycle W=0 stall is pinned to the pre-existing copy by the ungated rival arm (`AC93_RESULTS_v1.md` @ `1fe48df`).
- **Changes are attributable.** The AC94 `ungated` comparator reproduces AC92 byte-for-byte (32/32), and the `split` rival differs only in the switch mechanism (`AC94_RESULTS_v1.md` @ `6db1c47`).

**Not excluded:**
- The sequencing *logic* is still supplied (`AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`; U1).
- The gate is inert at the healthy fixed point W=3, so in normal operation it does not distinguish the organism from an ungated sequencer (AC93, "near-equivalence").

""",
"F4": """**Simplest rival.** *Hidden host-side memory* (external coordination): host bookkeeping, such as an observer history or a Python dict, silently steers the trajectory.

**Excluded?** At the endpoint, yes.
- Observer-discard leaves the final `state_hash` identical: 16/16 in AC95, 8/8 in AC96 (`AC95_RESULTS_v1.md` @ `d7925cf`; `AC96_RESULTS_v1.md` @ `d7925cf`).
- Source inspection closed both class-C leaks: the reset flag and `alloc.streak` (`AUTONOMY_RESEARCH_STATUS.md` @ `eb79ecb`).

**Not excluded:**
- **Per-tick steering.** "per-tick trajectory not compared" (status file).
- **Host functions outside the audited architecture.**

""",
"F5": """**Simplest rival.** Either of two mechanisms:
- *An external recipe*: the host re-supplies the program (external coordination).
- *Template copying*: ALife self-replication by copying inherited content, with no reconstruction from the organism's own description.

**Excluded?**
- **The external recipe: yes.** The generic decode replaces `prog.program`, and the rebuild equals it bit-for-bit (`AC80_RESULTS_v1.md` @ `6a1f4fb`; K3 table in `CLOSURE_VERDICT_v1.md` @ `4b85851`).
- **Template copying: not excluded, and not claimed.** Reconstruction decodes inherited, maintained content. The decode format is supplied substrate (`CLOSURE_VERDICT_v1.md` @ `4b85851` §3 item 2), and content invention is blocked (R10).

""",
}
for k, txt in F.items():
    m = re.search(rf"^### {k}\. ", t, re.M); assert m
    j = t.index("**Why foundational.**", m.end())
    nxt = re.search(r"^### ", t[m.end():], re.M)
    assert j < m.end() + nxt.start()
    t = t[:j] + txt + t[j:]

# ---------------------------------------------------------------- simplest rivals: S (list under table)
S = """
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
"""
once("\n**Context-only PR (listed for completeness, not a Track A finding).**",
     S + "\n**Context-only PR (listed for completeness, not a Track A finding).**")

# ---------------------------------------------------------------- simplest rivals: R
R = """
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
"""
once("\n---\n\n## 5. UNRESOLVED", R + "\n---\n\n## 5. UNRESOLVED")

# ---------------------------------------------------------------- simplest rivals: U
U = {
"U1": "**Simplest rival.** *External coordination*: a host-supplied sequencer (`advance()`) and interpreter (`prog.choose`) that carry the organization, while the produced machinery only funds their writes.\n\n",
"U2": "**Simplest rival.** *A fixed-level duty cycle, or a same-information reactive threshold rule* (control theory). These already reproduce every adaptive candidate on record (R2, R3, R11).\n\n",
"U3": "**Simplest rival.** *Ordinary state estimation with intact, supplied machinery* (counting / filtering): a world-state-only controller whose content changes behaviour but never the machinery that regenerates content.\n\n",
"U4": "**Simplest rival.** *Reservoir computing*: train the input weights, biases and readout on a fixed random recurrent matrix. This is exactly the R-FIX arm, so it is a rival not yet excluded or confirmed beyond the declared search.\n\n",
"U5": "**Simplest rival.** *A smaller autocatalytic sub-network* (ALife: a minimal autocatalytic set). For example, the W/C/B production loop with the description treated as passive storage.\n\n",
"U6": "**Simplest rival.** *External coordination through a declared non-spatial host array*: the informational core is ordinary host memory that space and boundary never touch.\n\n",
"U7": "**Simplest rival.** *A host-side counter* (external coordination). It is economically better on record: the host relinquishes 8/8 against the maintained arm's 2/8 (`AC96_RESULTS_v1.md` @ `d7925cf`).\n\n",
"U8": "**Simplest rival.** *Seed-dependent bistability* (dynamical systems): W/C bimodality with two attractors, and a basin selected by the seed.\n\n",
"U9": "**Simplest rival.** *Order-statistic variability* of the maximum over a finite set of random control draws (sampling). The label could move with more draws, without any change in mechanism.\n\n",
"U10": "**Simplest rival.** *The battery's own named count-based and policy-only analytic agents* (counting / filtering): R-CONF-A, R-BLIND/R-CONF-S, R-CG counts, R-HAC-MF, and the policy-minimized PM-ACT.\n\n",
"U11": "**Simplest rival.** *A tuned memoryless reactive policy* (RL / control), which nearly ties on record.\n\n",
}
for k, txt in U.items():
    m = re.search(rf"^### {k}[\. ]", t, re.M); assert m
    j = t.index("**Relevance", m.end())
    nxt = re.search(r"^(### |## )", t[m.end():], re.M)
    assert j < m.end() + nxt.start()
    t = t[:j] + txt + t[j:]

# ---------------------------------------------------------------- U9 and U10 wording
once("the same joint rule and the same 8/10 bar. Not a reanalysis.",
     "the same joint rule, and the B5 default bar (8/10, with UNRESOLVED above two invalid seeds) frozen in its own protocol. Not a reanalysis.")
once("""### U10. W-REL exact check (approved and executing; no results)

**Status.**
- Approved by Aidan: "Yes, approve the theory-only study", 2026-10-21 at 8:58 AM ET.
- A cloud agent is implementing and running it.
- **Not touched by this triage. Results, progress and implementation manifest are UNVERIFIED here.**
""", """### U10. W-REL exact check (approved and currently running; results pending)

**Status.**
- **Approved by Aidan at 8:58 AM ET, 2026-10-21**, with the verbatim answer "Yes, approve the theory-only study".
- Recorded in `/workspace/review/c4_reliability_APPROVAL_RECORD.md`. File verified present: 1423 bytes, sha256 `be3e3bb6b217717920629b87aea4094cffb510d748cae01995d1b93b1d917687`.
- **Currently running**: a cloud agent is implementing and running it, as relayed by the Specialist.
- **Results pending. This triage did not touch the check, its implementation or its outputs.** Progress and the implementation manifest are UNVERIFIED here.
""")

# ---------------------------------------------------------------- B1 pointer
once("**Eligibility.** A failure is a non-pass, not invalid. The seed must be valid, pass transfer, have B_prefix > eps0, have C_prefix > eps0, and have displacement > eps0.",
     "**Eligibility.** A failure is a non-pass, not invalid. The seed must be valid, pass transfer, have B_prefix > eps0, have C_prefix > eps0, and have displacement > eps0.\n\n**Seed bar.** The B5 defaults (8/10, and UNRESOLVED above two invalid seeds) were the frozen PR #8 instance. A new study must freeze its own.")

# ---------------------------------------------------------------- B3 rebuild (verbatim slices)
b3s = t.index("### B3. R-FIX freeze and compensation test (PR #10)")
b3e = t.index("### B4. W-REL named-rival battery (theory-stage)")
def fence(title, body):
    return f"**{title}**\n\n````text\n{body}````\n\n"
ex = []
ex.append(fence("Excerpt 1. §1 arms table and parameter-matching statement",
    slice_("| arm | head H |", "| (R-FIX-70, not run)", True) + "\n" +
    slice_("> \"R-FIX-32 tests compensation", "optimization effects.\"", True)))
ex.append(fence("Excerpt 2. §3 target definition",
    slice_("T(θ) = max(", "Numerical decisions follow the dual-evaluator rule of §3.1.", True)))
ex.append(fence("Excerpt 3. §3.1 numerical decision rule (dual evaluator), complete",
    slice_("### 3.1 Numerical decision rule", "## 4. Harness additions")))
ex.append(fence("Excerpt 4. §4 harness additions and freezing checks, complete",
    slice_("## 4. Harness additions", "## 5. Validation selection")))
ex.append(fence("Excerpt 5. §6 validity and eligibility, complete",
    slice_("## 6. Validity (per arm and seed)", "## 7. Labels (per arm")))
ex.append(fence("Excerpt 6. §7 labels, complete",
    slice_("## 7. Labels (per arm", "## 8. Claims (fixed in advance)")))
ex.append(fence("Excerpt 7. §8.1 'Not reached' wording and §8.3 claim ceiling",
    slice_("**Not reached:** \"R-FIX-H", "departing from W0 is necessary.\"", True) + "\n" +
    slice_("### 8.3 Claim ceiling", "## 9. Two-stage")))
B3 = ("### B3. R-FIX freeze and compensation test (PR #10): verbatim rules\n\n"
      "Track B considers this the most important test, so every rule below is quoted verbatim, not paraphrased.\n\n"
      f"**Source.** `{PROTO_PATH}` @ `{PROTO_COMMIT}`, PR #10 (https://github.com/godofthunder8756/Toward-an-Artificial-Organism/pull/10). Protocol sha256 `{PROTO_SHA}`. It is byte-identical to `/workspace/review/frozen_recurrent_compensation_protocol_FINAL.md`.\n\n"
      "**How the excerpts were made.** Each fenced excerpt is sliced byte-exactly from that file by `build_v1_1.py`, and `check_v1_1.py` re-verifies each one as an exact substring. Section numbers inside the excerpts are the protocol's own.\n\n"
      + "".join(ex) +
      "**Portability notes (this triage's, not protocol text).**\n"
      "- τ, the target components, the head widths, the budget and the seed and stream ranges are study-specific. A Track B study must freeze its own.\n"
      "- The thresholds t = 1e-9 and the agreement formula are PR #10's frozen values. They are a reasonable default for float64 dual evaluation, but they must be re-frozen per study.\n"
      "- The \"at least eight final verified passes\" and \"more than two runs … UNRESOLVED\" clauses are PR #10's frozen instance of the B5 defaults.\n"
      "- Two-stage seal: Stage 1 trains and seals checkpoint hashes with no target evaluation, then Stage 2 scores. Future practice (PR #10 errata E-D1, `results_v1_errata/ERRATA_v1.md` @ `0329818`) is an immutable Stage 0 manifest plus a dated addendum.\n\n")
t = t[:b3s] + B3 + t[b3e:]

# ---------------------------------------------------------------- B4 label
once("### B4. W-REL named-rival battery (theory-stage)",
     "### B4. W-REL named-rival battery (theory-stage) — METHOD ONLY, RESULTS PENDING\n\n"
     "**METHOD ONLY, RESULTS PENDING.**\n"
     "- W-REL was approved by Aidan at 8:58 AM ET (`/workspace/review/c4_reliability_APPROVAL_RECORD.md`, sha256 `be3e3bb6…7687`) and is currently running.\n"
     "- This section states the frozen method only. No outcome, label or statistic from the run is reported or implied.")
once("**Executing now; results UNVERIFIED.**", "**Status: METHOD ONLY, RESULTS PENDING.** The check is running, and no result has been read by this triage.")

# ---------------------------------------------------------------- B5 defaults
b5s = t.index("### B5. Seed bar and invalid-seed rule (shared by B1–B3)")
b5e = t.index("### B6. Organism-lineage portable tests")
B5 = """### B5. Seed bar and invalid-seed rule: DEFAULTS each Track B study must freeze

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

"""
t = t[:b5s] + B5 + t[b5e:]

# ---------------------------------------------------------------- B-pack intro and §6
once("Each test is stated as a frozen rule with its source. They are portable as *procedures*; thresholds must be re-frozen per study before any outcome exists. Nothing here authorizes a run.",
     "Each test is stated as a frozen rule with its source. They are portable as *procedures*. Thresholds, seed bars and invalid-seed rules are **defaults that each study must re-freeze in its own protocol** before any outcome exists (B5). Nothing here authorizes a run.")
once("## 6. Verification of this document\n",
     "## 6. Verification of this document\n\n"
     "**v1.1.** `/workspace/scratch/track_a_triage/v1_1/check_v1_1.py` (log `check_v1_1.log`) runs all v1 checks on this file and the additional v1.1 checks listed in the changelog. The v1 description below is retained.\n")

open(out, "w").write(t)
print(hashlib.sha256(t.encode()).hexdigest())

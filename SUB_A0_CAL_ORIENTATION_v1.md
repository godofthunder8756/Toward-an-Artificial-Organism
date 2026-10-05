# SUB-A0 calibration: orientation note v1

2026-10-04. One-page orientation for the A0-cal session. Synthesis only; no new evidence.

## Mission as I understand it

The project asks whether self-maintenance (L0) and endogenous regulation (L1) are
conditions under which consciousness-indicator functions become necessary or
emerge. The thesis under test is that current AI has rich L2–L4 machinery but
lacks L0–L1, and that the absence matters.

This line asks a narrow L0/L1 question: **do maintenance priorities arise from
dependence rather than from assignment?** Operationally: under damage pressure,
does a task-trained repairer shift budget toward its own vulnerable repair
machinery, with no objective rewarding it?

L6/phenomenal consciousness is out of scope. Under
[constitution v3](ACI_RESEARCH_CONSTITUTION_v3.md), layer numbers are dependencies
and do not form a consciousness meter.

## Prior reductions (frozen; I extend them, I do not relitigate them)

| Study | Verdict | What it means for this line |
| --- | --- | --- |
| [Phase II bridge](BRIDGE_PHASE2_VERDICT_v1.md) | B + D | An explicit maintained self-state V is unnecessary; a same-information policy matches it. A 3-line threshold rule beats learned allocation. Paid persistence is a substrate fact. |
| [Phase III](PHASE3_VERDICT_v1.md) | C | A sufficient-statistic broadcast reproduces the learned workspace at zero parameters. What matters is availability of content, not workspace complexity. |
| [Phase III-B](PHASE3B_VERDICT_v1.md) | B | The candidate lost to the best rival on 15/16 seeds; an unrestricted 8-symbol code won. |
| [SUB_A](SUB_A_ANALYTIC_CHECK_v1.md) | Admission STOP | (1) Every-tick self-repair equals an external every-tick schedule by induction. (2) An identical-state yoke is a clone. (3) The host-supplied median fails closure. |
| [SUB-A0 engineering](SUB_A0_ENGINEERING_REVIEW_v1.md) | **INVALID** ([errata v2](SUB_A0_ENGINEERING_ERRATA_v2.md)) | No-write kept 1.000, so there was no maintenance pressure. The probes hit a ceiling by construction. D = 0.00099 cannot be interpreted. |

The pattern so far: every proposed mechanism has lost to a simpler rival at
matched cost. The binding rival for this line is
**damage-proportional repair**: budget follows visible disagreement, with no
priority from dependence. It is now pre-registered as a reduction
([re-test proposal](SUB_A0_RETEST_PROPOSAL_v1.md), arm DISAGREE_PROP).

## Why A0 is INVALID, and what I found beyond the review

1. **Timescale.** With no writes, task |mean| decayed 4.449 → 1.217 over 1,024
   ticks and no sign flipped. A mean-field model predicts readout loss begins
   around 2,000–3,000 ticks.
2. **Probe.** Zeroing one replica of a 3-replica mean cannot flip the readout, so
   the probe could never fail.
3. **New: IMMORTAL ≡ SHAM.** The two arms share one code path and have
   byte-identical traces, so A0 had no ceiling arm.
4. **New: unmatched external control.** The EXTERNAL arm jumped without a step
   bound. The candidate is limited to |Δ| < 0.05.
5. **New: exact acquisition magnitude.** Acquisition gives |T| = 4.449178695678711
   exactly, for every coefficient and seed, against |R| ≈ 0.28. This sharpens the
   scale confound.

## This session

- Errata v2, then a calibration protocol (**draft, unfrozen**) with a pre-registered
  grid, selection rule and analytic predictions.
- A validity-gate registration (draft).
- A control-arms-only harness with 24 tests. Bitwise equality with A0's fault
  stream and acquisition is verified.
- The re-test proposal with its go/no-go table.
- **No calibration was run**, by agreement: stop before freezing.

## Prior-art positioning (metadata verified via OpenAlex and Crossref APIs, TLS on)

| Work | Verified record | What it already settles / how A0 differs |
| --- | --- | --- |
| von Neumann 1956, *Probabilistic Logics and the Synthesis of Reliable Organisms From Unreliable Components* | Automata Studies AM-34, pp. 43–98, [10.1515/9781400882618-003](https://doi.org/10.1515/9781400882618-003) | Redundancy with restoring organs gives reliability from unreliable parts. EXT_BISTABLE **is** a restoring organ. Recoverability is supplied knowledge, not a finding. |
| Gács 1986, *Reliable computation with cellular automata* | JCSS 32(1):15–78, [10.1016/0022-0000(86)90002-4](https://doi.org/10.1016/0022-0000(86)90002-4) | A self-repairing organization sustains arbitrarily long computation despite constant-rate faults. Self-repair of the repairing medium exists in principle and is hand-designed. |
| Gács 2001, *Reliable Cellular Automata with Self-Organization* | J. Stat. Phys. 103:45–267, [10.1023/A:1004823720305](https://doi.org/10.1023/A:1004823720305) (FOCS 1997 version also exists) | Same, with self-organization. No learned priority. |
| Fauth, Wörgötter & Tetzlaff 2015 | PLoS CB 11(12):e1004684, [10.1371/journal.pcbi.1004684](https://doi.org/10.1371/journal.pcbi.1004684) | Multi-synapse connections keep information for months under high turnover. This is redundancy-based maintenance without a learned allocator. |
| Fauth & van Rossum 2019 | eLife 8:e43717, [10.7554/eLife.43717](https://doi.org/10.7554/eLife.43717) | Spontaneous reactivation of assemblies maintains memories through turnover. Maintenance by replay; again no self-priority question. |
| Chang & Lipson 2018, *Neural Network Quine* | ALIFE 2018, pp. 234–241, [10.1162/isal_a_00049](https://doi.org/10.1162/isal_a_00049), arXiv 1803.05859 | A network outputs its own weights. Reports a trade-off between self-replication and task performance, which is the closest precedent for self-versus-task allocation. |
| Schmidhuber 1993, *A "Self-Referential" Weight Matrix* | ICANN '93, pp. 446–450, [10.1007/978-1-4471-2063-6_107](https://doi.org/10.1007/978-1-4471-2063-6_107) | Self-modification is old. Self-access alone answers nothing. |
| Irie, Schlag, Csordás & Schmidhuber 2022 | arXiv 2202.05780 ([10.48550/arXiv.2202.05780](https://doi.org/10.48550/arXiv.2202.05780)). The APIs returned no ICML venue field, so I cite the preprint. | A modern SRWM modifies itself at runtime with delta rules. A0's addition is shared damageability plus a test of damage-induced priority. |

**Positioning.** This is not a novelty claim. Reliability from redundancy, self-repair
of the repairing medium, and learned self-modification all predate this line. The
untested combination is:
- a *learned*, *task-only* repairer;
- whose repair machinery is *equally damageable*;
- examined for whether its allocation *shifts toward that machinery beyond
  damage-proportional repair*.

Chang & Lipson's replication/task trade-off is the nearest precedent and should be
cited in any result.

## Discrepancies flagged

- [NEW_AGENT_GUIDE.md](NEW_AGENT_GUIDE.md) is from the E3 era.
  [Constitution v3](ACI_RESEARCH_CONSTITUTION_v3.md) and [tree v5](ACI_MASTER_RESEARCH_TREE_v5.md)
  supersede the v2/v4 files named in the handoff.
- Tree v5 says "no neural training is currently authorized." The A0-cal mandate
  authorizes only control-arm calibration, which needs the task-table fit alone
  (no updater, no meta-development). Any re-test training needs explicit approval.
- I used file prefix `SUB_A0_` instead of the requested `A0_CAL_`. This avoids a
  collision with the organism-era `A0_AUTONOMY_*` lineage. Rename on request.

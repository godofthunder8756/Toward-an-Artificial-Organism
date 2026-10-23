# Omission manifest — scarcity_v2 v1

What the frozen run did not execute. This file is retrospective disclosure. It is not a preregistration, and it does not reopen a gate. Protocol-byte preservation does not prove execution fidelity: the protocol file is still sha256 `ea47d1375c9e3c2fc4abdc538d714f65c66ed44243ca6ddd5e319684bd0fd4a6`, and the omissions below were real.

`DEVIATIONS.md` was written with the results, not before them. Implementation commit `ea20fefd14874614e20adb1897068a728bac580c` and results commit `5fa6571023941af97fa95638d187e04c191aaaad` share the timestamp 2026-10-21T01:08:41Z. That timestamp is the documentation date of every reading below. It is not a date on which the reading was fixed in advance of the outcomes.

## Executions omitted

**Paid small-K SEL/ACC.** No paid codebook search was run. Paid ACC is descriptive under the protocol. Paid SEL is in the declared S-DIRECT scope, so the omission is an execution deviation. Unpaid witnesses already fill each SEL bin, and they are enough for the existential admission. The corrected SEL label is ADMIT, certified on unpaid cells.

**S1 and S2.** Not run. The protocol marks them descriptive. The omission does not change a family label. It is still an omitted descriptive output.

**H = 3.** Not swept. Report-only in the protocol, and absent from the outputs. The stage-B grid at H = 3 is the stage-A grid times {1, 3, 6}, capped at 125·6 = 750. None of these capacities were run:

1, 2, 3, 4, 6, 8, 9, 12, 16, 18, 24, 26, 27, 32, 36, 48, 54, 64, 72, 78, 81, 96, 108, 125, 144, 156, 162, 192, 288, 375, 384, 576, 750.

T3, the H = 3 tracker, was not evaluated. T2 and T3 are adaptive trackers. Their absence is an execution omission, not a finding that adaptation failed.

**ADAPT stage B.** The frozen stage-B grid is the stage-A grid times {1, H, 2H}, capped at 125·2H, and grid points are included whether or not they match an optimum count. The run used only K ∈ {1, 16, 26, 48, 64, 125}.

At H = 2 the cap is 500. Capacities on that grid that were not run, and that therefore have no cell record:

2, 3, 4, 6, 8, 12, 18, 24, 27, 32, 36, 52, 54, 72, 96, 104, 108, 128, 192, 250, 256, 384, 500.

Their execution status is NOT-RUN. No timeout is asserted for a capacity that was never searched.

H = 1 was not swept. The only H = 1 cell in the outputs is the KNOWN-FIXED, B_up = 1, K = 26 control. The other H = 1 capacities, cap 250, were not run:

1, 2, 3, 4, 6, 8, 12, 16, 18, 24, 27, 32, 36, 48, 52, 54, 64, 96, 125, 128, 192, 250.

The implementation’s B_up = 0 experimental pin is K ≥ 27 (`DEVIATIONS.md` item 14). K = 27 is on the omitted H = 2 list. The executed grid shows K = 26 unresolved and NOT-RUN, and K = 48 certified zero. An independent review stated the pin as K ≥ 48. That matches the cells that were actually run. There is no executed cell between those two capacities, so the two statements do not assign different labels to the same cell.

**Wrong-bit and dash signalling encoders.** Not enumerated for ADAPT. The experimental search used encoders that write the true bit on every answer field, then cue-equivariant updates (5² encoders × 2⁶ updates at H = 2). Encoders that write a wrong bit, or an intentional dash, in order to signal the pre-decay register through the outcome, were not enumerated. The regime-known value remains an upper bound on every encoder. Where the subclass does not meet that bound, the cell stays UNRESOLVED. A zero lower bound on that interval is class inclusion: the tracker is inside `full_B`. It does not show that adaptation failed. See `RESULTS_v2.md`.

## Readings, each dated 2026-10-21T01:08:41Z

The text of each reading is `scarcity_v2_study/DEVIATIONS.md`, which this manifest does not edit.

| # | Reading | Documented | Later ruling |
| --- | --- | --- | --- |
| 1 | In-scope grid. S1 and S2 not run. | 2026-10-21T01:08:41Z | Omission, this file |
| 2 | a = 5/6 decision-bearing. δ = 1/4 and H = 3 report-only. | 2026-10-21T01:08:41Z | H = 3 listed here |
| 3 | Paid small-K SEL/ACC not searched. | 2026-10-21T01:08:41Z | Execution deviation; unpaid SEL still admits |
| 4 | Item symmetry is the order-8 bit-label group. | 2026-10-21T01:08:41Z | Unchanged |
| 5 | Word order, dash last. | 2026-10-21T01:08:41Z | Unchanged |
| 6 | Replay file absent; §7.3 quotes used. | 2026-10-21T01:08:41Z | Unchanged |
| 7 | ACC label follows §7.3 rather than §7.2 precedence. | 2026-10-21T01:08:41Z | Re-ruled by E1: primary REJECT-SIG, NARROW retained |
| 8 | Uncertified K = 1 stays UNRESOLVED. | 2026-10-21T01:08:41Z | Re-ruled by E2 for upkeep |
| 9 | Below K_suff, residual search described as not exhausted. | 2026-10-21T01:08:41Z | Re-ruled by E3: NOT-RUN, no timeout |
| 10 | r = 5/8 uses 1 − δ(1 − r). | 2026-10-21T01:08:41Z | Unchanged; values 5/64 and 5/128 |
| 11 | UPK-C0 holds below K_suff; UPK_ev stays open. | 2026-10-21T01:08:41Z | Unchanged, except K = 1 by E2 |
| 12 | SWITCHING hazard is a flip probability. | 2026-10-21T01:08:41Z | Unchanged |
| 13 | ADAPT subclass omits wrong-bit and dash encoders. | 2026-10-21T01:08:41Z | Listed in this file |
| 14 | B_up = 2 and B_up = 0 pins are not §5.5 controls. | 2026-10-21T01:08:41Z | K = 27 not executed; see above |
| 15 | T2 counted at (E, I, Q) = (2, 48, 52), used from K ≥ 52. | 2026-10-21T01:08:41Z | Unchanged |
| 16 | ROUTE optima are decoder pairs, not quotiented. | 2026-10-21T01:08:41Z | Equivalence noted in RESULTS_v2 |
| 17 | No search reached its limit. | 2026-10-21T01:08:41Z | True of searches that ran; E3 covers the rest |
| 18 | B_up = 2 optimum count 2^24 and the orbit formula. | 2026-10-21T01:08:41Z | Unchanged |
| 19 | Optimum lists capped at 20,000; no positive decision cell hit the cap. | 2026-10-21T01:08:41Z | Unchanged |

Items 7, 8, and 9 were documented at the same moment as the results. E1–E3 adjudicate them. The other readings stand as disclosure of how the frozen run was executed.

## Self-tests

`selftests.json` records 46 passed and 0 failed. That count is the number of checks that were executed. It does not show that every required control was covered. The check named “K=1 degenerate” is an unpaid SEL cell. None of the 46 checks is the §5.5 K = 1 upkeep control. E2 supplies that control. The passed checks do include K_suff = 16, K_suff = 26, the withdrawals −3/32 and −1/32, the graded 33/4096 report, the zero-ADAPT construction, and the cited replay gaps.

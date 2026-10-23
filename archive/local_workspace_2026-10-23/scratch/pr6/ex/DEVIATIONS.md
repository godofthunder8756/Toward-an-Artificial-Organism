# Readings, ambiguities, and deviations

The protocol file is byte-identical to the frozen digest. Nothing in this file changes those bytes. Each item is the literal reading used when the protocol text allows more than one execution.

1. **In-scope grid.** The repository has no separate cell list. The decision grid is the protocol's own parameter table, restricted as follows. Unpaid SEL/ACC: clean, and graded a ∈ {3/4, 5/6} plus the null (3/5, 3/4); r ∈ {5/8, 3/4} (null uses r = 3/4 only); v ∈ {1/3, 3/4}; the frozen K grid; uniform cue. UPK decision cells: clean, δ = 1/2, B_up ∈ {0, 1, 2, 3}, the same v, r, and K. ROUTE: those evidence laws, L ∈ {1, 2, 3} and the channel-sufficient L. ADAPT decision cells: clean, δ = 1/2, v = r = 3/4, H = 2, the four regime conditions, B_up ∈ {0, 1, 2, 3}, plus the H = 1 and δ = 0 controls. S1 and S2 are descriptive and were not run.

2. **Secondary parameters.** a = 5/6 is secondary and is not marked report-only, so it is decision-bearing. δ = 1/4 is report-only: those UPK rows were computed and cannot change a label. H = 3 was not swept. It is report-only and cannot change a label.

3. **Paid small-K SEL/ACC.** Not in the decision grid. Paid ACC is descriptive under the protocol, and the SEL ratio bins are filled by unpaid cells. No paid codebook search was run.

4. **Item symmetry.** Optima are quotiented by the order-8 group of item bit-label flips (XOR on the item and on the non-dash bits of a codeword), not by permuting coordinates. An optimum is a codebook of size min(K, 27). K > 27 is the same problem as K = 27, because an unpaid configuration is one of 27 field vectors.

5. **Word order.** Field vectors are indexed lexicographically on (0, 1, dash), dash last. Field 0 is the high bit of a clean item. The order does not affect a completed exact search.

6. **Replay file.** `replay_results.json` is not in this repository. The §6 replay control was checked against the gaps quoted in §7.3. The two v = 1/3 gaps at a given K are read in the same order as r ∈ {5/8, 3/4}: 1/48 then 1/24. K = 3 at v = 3/4, r = 5/8 is not cited and is not a replay control.

7. **ACC label preservation.** §7.2's general signature rule would call ACC REJECT-SIG when every CERT-POS cell is SIG-UNDEFINED. §7.3's replay record says REJECT-NARROW, and the precedence sentence says that record is preserved. The certificate follows §7.3.

8. **K = 1.** A certified zero at K = 1 is labelled DEGENERATE and counts as zero for breadth. A K = 1 cell whose value was not certified stays UNRESOLVED. It is not forced to zero.

9. **O-UPK on the ample clean family.** Every value-achieving policy stores every field and keeps the queried cue inside the durable set. The withdrawal "on every episode, downgrade j = c from D to F" therefore applies to every optimum, with ΔV = −δ·v·(1 − r) < 0. The signature is ROBUST without listing the policies. Below K_suff the per-input upper bound is infeasible. Those cells are UNRESOLVED because the residual configuration search was not exhausted. An unresolved cell does not remove a bin that an ample cell has already qualified, and it does block a bin that nothing has qualified.

10. **UPK at r = 5/8.** §5.3 writes the r = 3/4 special case (a fragile correct field is worth 1 − δ/4). The same algebra, with a fragile correct field worth 1 − δ(1 − r), is used at r = 5/8. The positive self-test checks the stated r = 3/4 gaps 5/96 and 5/192.

11. **UPK-C0 below K_suff.** The cue-blind comparison is proved for every K. UPK_cue is CERT-ZERO at v = 1/3 even when the UPK value itself is UNRESOLVED. UPK_ev stays UNRESOLVED there, because it equals the unresolved UPK gap.

12. **SWITCHING hazard.** "h = 1/4 per episode" is read as a flip probability: after the update and before the next episode, the regime flips with probability h and otherwise stays. IID-REGIME redraws the regime independently. It is not implemented as that flip chain.

13. **ADAPT subclass.** Among encoders that write the true bit on every answer field, the outcome is independent of the regime given (η̃, q, c), so a best update in that subclass may ignore the outcome. Cue-equivariant policies in that subclass were enumerated exactly (5² encoders × 2⁶ updates at H = 2). Encoders that write a wrong bit or an intentional dash, in order to signal the pre-decay register through the outcome, were not enumerated. The regime-known value is an upper bound on every encoder, because each episode's conditional reward cannot exceed it. Where the subclass does not meet that upper bound, the experimental cell is UNRESOLVED and the gap is reported as an interval.

14. **ADAPT at B_up = 2 and at B_up = 0.** Protecting {c, c+1} leaves only field c+2 exposed, and that field has query probability (1 − v)/2 under both regimes. The value equals the regime-known upper bound, so T_const attains it and ADAPT = 0 for every regime process, once K ≥ 16. At B_up = 0 no field can be protected, so writing the true bits is optimal for every regime once K ≥ 27, and both arms match. These pins are not §5.5 controls. UNKNOWN-FIXED is not treated as a zero control. The §5.7 controls themselves are zero at every K: the collapsed register fits whenever the original policy does, so a small-K control cell is CERT-ZERO (DEGENERATE at K = 1) rather than an unfinished search.

15. **Stage-B capacity.** The natural T2 policy at B_up = 1 uses two register values and was counted at (E, I, Q) = (2, 48, 52). Its value is used as a lower bound only at K ≥ 52. Controls use the stage-A counts: K ≥ 26 for B_up = 1 and K ≥ 16 for B_up = 2. Collapsing the register, as in the §5.7 construction, drops the counted policy from (2, 48, 52) to (1, 24, 26).

16. **ROUTE optima.** A consumer separates, and for a fixed decoder the sender optimum is an argmax at each input. Optima are counted as pairs of optimal decoders, as distinct functions, not quotiented by item symmetry. Sender ties are not expanded; the O-ROUTE interval takes the min and max over ties, which is exact because the intervention sum separates across inputs. L ≥ K_dec,base is the constructive zero and is not enumerated.

17. **Budget.** full is given the first 4 CPU-min. Rivals share the remaining 6 in the stated class order, and stage B follows. No search reached its limit. Completed certificates are the cell records. The three-minute checkpoint was not crossed by any cell.

18. **B_up = 2 optimum count.** For K ≥ 24 every partner policy fits, because the enumerated maximum is I = 24 and Q = 20, so there are 2^24 policies. Orbits under the bit-label group use the closed form (2^24 + 7·2^12) / 8. K = 16 and K = 18 are counted by the same recursion, not by that shortcut.

19. **Stored optimum lists.** Codebooks are stored up to 20,000. Past that cap the search still returns the exact optimum value and the exact count, and the signature is not certified. No positive decision cell hit the cap. Clean unpaid cells at K = 16 and K = 18 are above it; their gaps are zero, so no signature was required, and their orbit counts are not reported.

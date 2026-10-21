# DEVIATIONS

Frozen commit: `aeb9382bb7c0102249e947de849e715319abf2e7`.

No frozen file is edited. Original `outputs/ITEM-1.json` through `outputs/ITEM-9.json` and `outputs/SUMMARY.json` from the freeze run are kept.

## D1 — copy the computed quotient flag onto the machine record, then rerun ITEM-8 and ITEM-9

- What changed. Frozen `item7` computes `well_defined(machine, block)` and stores it on the ITEM-7 report. The in-memory machine record does not carry that field. Frozen `item8` then evaluates `mach["well_defined"]["ok"]` and raised `KeyError: 'well_defined'` on the first A-SEP setting (wall 2.0 s). The new module `wrel/deviation_1_item8.py` rebuilds the in-memory dependency state by calling the frozen item functions, copies each report's `well_defined` value onto the matching machine record, and calls the frozen `item8` and `item9`. No threshold, donor rule, horizon, cost, rate, or quotient construction is changed. The flag is the one ITEM-7 already computed.
- Why. ITEM-8 cannot read a field that was computed and then left off the record it receives. Substituting a different test, or treating the quotient as ill-defined because the key was missing, would not be the procedure in the spec.
- Items affected. ITEM-8 and ITEM-9. ITEM-1 through ITEM-7 are not re-recorded. Their JSON files stay the freeze-run outputs. The dependency rebuild exists only to restore policies, machines, and exact rows in memory; it does not replace those outputs.
- Where the rerun is written. `outputs/deviation_1/ITEM-8.json` and `outputs/deviation_1/ITEM-9.json`.
- Originals kept. `outputs/ITEM-8.json` is the engineering failure. `outputs/ITEM-9.json` completed with an empty settings list because ITEM-8 never stored `settings_raw` or `replay_bank`. Its PM partition check agreed. It is not overwritten.

## D1 rerun result

The D1 process rebuilt items 1–7 in memory, attached the four `well_defined` report values, and called the frozen `item8` and `item9`. ITEM-8 status COMPLETE, wall 32.396 seconds, sampled peak RSS 706473984 bytes. ITEM-9 status COMPLETE, integrity AGREE, mismatches empty, labels issued. No further code change. No frozen file was edited. Original `outputs/ITEM-8.json` and `outputs/ITEM-9.json` remain the freeze-run files.

## Coverage note, not a code change

The frozen ITEM-9 replays the R-CG mixture value at T_SEP = 3. It does not replay every R-CG criterion statistic. Spec §5.4 lists every statistic for MB and all R-CG variants at T_SEP = 3. That gap is in the freeze. It is reported in RESULTS. It is not patched here.

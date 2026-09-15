# AC9 controls v3 results

The frozen run contains 64 rows (seeds 1200–1203, histories 0/1, eight
conditions) in `ac9_controls_results_v3/results.json`. The independent table
audit passes all recorded energy, fuel, material, coverage, and source-hash
checks (`py -3.12-arm64 -B audit_ac9_controls_v3.py`).

| condition | complete activity | route retained | interpretation |
|---|---:|---:|---|
| keep | 8/8 | 8/8 | baseline maintenance |
| block_old | 7/8 | 0/8 | occupied-region maintenance is required |
| block_other | 8/8 | 8/8 | unoccupied-region block is non-causal |
| swap_block_old | 8/8 | 0/8 | dependency follows relocated physical organization |
| swap_block_other | 7/8 | 8/8 | other-region intervention does not erase function |
| read_disabled | 8/8 | 8/8 | entries remain present, but productive contacts are ~0.50 of keep |
| protected_block_old | 8/8 | 8/8 | protected external copy preserves behavior despite actual loss |
| fixed_correct | 8/8 | 8/8 | favorable externally supplied allocation control |

The strongest supported conclusion is model-relative: a learned route is
maintained by a physically allocated, readable organization, and the causal
dependency follows that organization when it is relocated. This separates
functional benefit from inert material burden and from the developmental label.
The protected-copy condition is a scaffold control and therefore does not
count as autonomous maintenance. The fixed-correct condition is an oracle
control and does not count as developmental acquisition.

Open work remains: integrated W/C and boundary ablations, a richer
developmental function than the current four routing classes, and an
intervention where the controller must acquire the need to allocate or
relinquish maintenance resources. Full autopoiesis, general autonomy, and
subjectivity remain unestablished.


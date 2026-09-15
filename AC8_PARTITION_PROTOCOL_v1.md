# AC8 action-bit partition follow-up, before results

2026-09-15. Seeds900–907,8192 ticks,p=.0001, unchanged fixed resource mappings
and AC8 learning through2048 only. Four conditions per seed,32 rows: keep;
block selectors (indices12,13,26,27); block action types (10,11,24,25); block all
eight route bits. No new damage, pulse, noise tuning or reset. Paired randomness.

The selector bits encode the previously unknown port choices; action-type bits
are inherited. Selector representation is redundant: two bits change together
for each binary choice. Damaging one can produce an unrelated action. This is
the actual encoding under test, not an abstract perfect two-state variable.

Primary criterion: keep>=7/8 completion; keep-minus-selector-block mean activity
>=.2; positive route-accuracy difference. Report all four arms and both bit
partitions even if the criterion fails. Four excluded bits have fewer damage
opportunities than the original eight-bit exclusion; do not silently lengthen
the run to obtain an effect. No claim of new-need creation or universal learning
necessity. Source snapshots, exact default equivalence and sampled replays,
all inventories, unique coverage and preserved raw rows required.

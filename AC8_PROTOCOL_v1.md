# AC8 reacquisition and selective route maintenance

2026-09-15. Prospective engineering extension, unchanged AC7 physical laws.

Two separate cohorts, seeds800–807,8192 ticks,p=.0001, six conditions per seed
(48 rows). Same AC7 acquisition and balanced unknown initial mapping.

Reacquisition cohort: complement both resource-port mappings at tick4096.
Arms remap_live (learning continues), remap_frozen (learning stops2048),
remap_random (stateless port sampling). No phase signal enters the learning
law; only the physical port outcome changes. Score correct stored routes at
2048 and endpoint, first alive correct-routing time after remap, activity and
contact costs. Random strategy is not expected to store a correct mapping.

Maintenance cohort: mapping stays fixed. All learn until2048, then learning
stops. Arms keep, block_routes (from2048 exclude only logical action bits10–13
and24–27 from bank0 majority repair), block_routes_live (same repair ablation,
but learning continues). Blocked sites cost no energy/material and consume no
repair capacity; the rest of the inherited controller remains repairable.
This uses ordinary uniform corruption, no targeted pulse or observer rewriting.

Report all outcomes; no post-result tuning. Engineering reacquisition gate:
>=7/8 remap_live completion and correct final mappings; all remap_live acquire
initial mapping by2048; live-minus-frozen mean activity>=.2. Maintenance gate:
keep>=7/8 completion and mean activity difference keep-minus-block_routes>=.2,
with positive route-integrity difference. Report block_routes_live separately:
feedback-based rewriting can compensate for some memory corruption, and must
not be confused with ordinary repair. Failure of the eight-bit isolation test
does not contradict prior whole-controller tests at other horizons.

Snapshot all source dependencies before run, persist rows, verify all inventories,
default-step equivalence, targeted repair selectivity, no hidden reacquisition
teacher and sampled exact replays. Same-author exploratory evidence. Unknown
access mappings remain distinct from acquiring an entirely new maintenance need.

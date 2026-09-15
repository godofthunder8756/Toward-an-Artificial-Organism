# AC4 extended follow-up, before results

2026-09-14. Keep all AC4 reaction laws, acquisition, representations and costs
unchanged. Extend horizon to8192 ticks, seeds100–107, both original damage rates
.00005/.0001. Four arms: self, no_policy_write, protected, no_B_retention.
Total64 rows. This extends information-maintenance and retention-rescue evidence;
it does not repeat the already measured no-B ablation or discover new needs.

Primary contrast: paired self-minus-no-policy-write active fraction, with
descriptive95% bootstrap interval (10000 resamples, seed20260914), separately
at each rate. Report completion counts, final raw and survival-weighted policy
accuracy (raw accuracy times completion indicator), constituent production,
losses and all resource balances. Raw information in frozen dead states is not
functional information. All rows retained; no parameter tuning.

Engineering criterion: self mean activity>=.9, self final mean policy accuracy
>=.99, protected mean activity>=.9, primary activity difference>=.2 and its
descriptive interval lower bound>0. Report retention-rescue information without
turning activity-only rescue into organizational rescue. Eight seeds are a
small same-author engineering sample, not independent scientific confirmation.

Snapshot dependencies before runs. Persist each complete row immediately so
an interruption does not erase finished evidence. Verify rectangular coverage,
all inventories and source hashes; replay seed100 in every arm/rate exactly.
Do not modify the frozen simulator to pass this follow-up. A negative result
changes the next research step; it does not justify rewriting the criterion.

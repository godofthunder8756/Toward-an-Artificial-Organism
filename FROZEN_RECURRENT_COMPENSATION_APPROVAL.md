# Training approval

Study: Frozen recurrent matrices with learned compensation.

Protocol file: `frozen_recurrent_compensation_protocol_FINAL.md`

Protocol sha256: `eca2121c5972138580ebd8ababb1cd40879a4c20404e925e129becd7e778ea40`

APPROVAL: Aidan approved this at 3:06 AM ET on 2026-10-21. The approval is recorded before any study training. No study training has occurred at the time this record is frozen.

- Who: Aidan
- When: 2026-10-21, 3:06 AM ET
- Source: widget t28s1 (as relayed in the implementation request)
- Question (verbatim): "Approve 30 CPU training runs for 'Frozen recurrent matrices with learned compensation': seeds 400-409, with CAND, R-FIX-32 and R-FIX-48 trained once per seed for 4000 steps under the PR #7 recipe, followed by the specified evaluation, once Astra's named edits are applied and the protocol and implementation are frozen? No appendices, restarts, searches or extra runs."
- Answer (verbatim): "Yes, approve the 30 runs"

Scope of this approval: exactly those 30 runs. Appendix A, Appendix C and Appendix D are not approved. Restarts, hyperparameter searches and additional training runs are not approved. The synthetic-fixture freezing test on a non-study seed is implementation testing only.

## Superseded widget t26s1

Widget t26s1 was never answered. It is not the approval.

- Question (verbatim): "Approve fresh-seed GRU-8 training (seeds 400-409, 30 runs: normal plus two frozen-recurrent variants) for the frozen-recurrent compensation study once Astra clears the protocol?"
- Answer: never answered.

Astra consult #19 had already returned FREEZE WITH NAMED EDITS. Scientific clearance does not authorize training. The operative approval is widget t28s1 above.

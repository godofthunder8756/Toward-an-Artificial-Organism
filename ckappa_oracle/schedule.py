"""Frozen scheduled propagation counts.

One float propagation is one float64 continuation of a stage-4 belief through
readings 5–8. One exact propagation is one exact-rational filter run
(a stage-4 prefix, or one terminal continuation).

O6 and O7 edit counts are the no-void, all-folds-scored upper bounds.
True-chart baselines are shared and counted once. O5 counts the perturbed
chart and the kappa-zeroed chart, and reuses the true baseline.
"""

O2_FD = 16 * 16 * 3 * 2
TRUE_BASELINE = 16 * 16
O6_EDIT = 6 * 8 * 16 * 16 * 2 * 4 * 3
O7_BASELINE = 16 * 16
O7_EDIT = O6_EDIT
O5_OFF_BASELINE = 16 * 16 * 64 * 2 * 3 * 2
O4_PROPAGATIONS = 0
O3_PROPAGATIONS = 0

SCHEDULED_FLOAT = (
    O2_FD
    + TRUE_BASELINE
    + O6_EDIT
    + O7_BASELINE
    + O7_EDIT
    + O5_OFF_BASELINE
    + O4_PROPAGATIONS
    + O3_PROPAGATIONS
)

DECLARED_N_O1 = 16 + 256
SCHEDULED_EXACT_REMAINING = 0

BREAKDOWN = {
    "O2_finite_differences": O2_FD,
    "true_chart_baselines": TRUE_BASELINE,
    "O6_edit_propagations": O6_EDIT,
    "O7_baselines_upper": O7_BASELINE,
    "O7_edit_propagations_upper": O7_EDIT,
    "O5_off_baseline": O5_OFF_BASELINE,
    "O4": O4_PROPAGATIONS,
    "O3": O3_PROPAGATIONS,
    "scheduled_float": SCHEDULED_FLOAT,
    "declared_n_o1": DECLARED_N_O1,
    "scheduled_exact_remaining_after_step0": SCHEDULED_EXACT_REMAINING,
}

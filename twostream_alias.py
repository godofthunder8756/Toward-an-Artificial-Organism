"""Reachable-alias audit on exact marginals.

Witnesses are pairs of histories of equal length. Clamped or factorized
beliefs are never passed in; callers supply reachable posteriors only.
Classification is exhaustive. A pair is symmetry-generated only when the
histories are flips of one observation phase. Every other collision is
accidental, including collisions whose marginal means are nonzero.
"""

from fractions import Fraction

from twostream_constants import history_bits, phase_mask


def _mechanism(h1, h2, n_readings, mx, my, c1, c2):
    x_mask = phase_mask(n_readings, 0)
    y_mask = phase_mask(n_readings, 1)
    if x_mask and h2 == (h1 ^ x_mask):
        # Zero X-spin mean is m_x = 1/2. A nonzero marginal mean cannot be a
        # pure X-flip witness.
        anomalous = mx != Fraction(1, 2) or c2 != -c1
        return "symmetry-X", anomalous
    if y_mask and h2 == (h1 ^ y_mask):
        anomalous = my != Fraction(1, 2) or c2 != -c1
        return "symmetry-Y", anomalous
    return "accidental", False


def audit_stages(stage_records, terminal_stage):
    """Classify same-phase aliases and cross-stage marginal coincidences.

    `stage_records` maps stage k to a list of dicts with keys history, mx,
    my, c, prob. `terminal_stage` is the horizon used for terminal-query
    claims. Prefix stages are every other supplied stage.
    """
    stages_out = {}
    terminal_count = 0
    prefix_count = 0
    anomalies = []
    for stage in sorted(stage_records):
        rows = stage_records[stage]
        buckets = {}
        for row in rows:
            buckets.setdefault((row["mx"], row["my"]), []).append(row)
        pairs = []
        benign = 0
        for group in buckets.values():
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    left, right = group[i], group[j]
                    if left["c"] == right["c"]:
                        benign += 1
                        continue
                    if left["history"] <= right["history"]:
                        h1, h2 = left, right
                    else:
                        h1, h2 = right, left
                    mechanism, anomalous = _mechanism(
                        h1["history"],
                        h2["history"],
                        stage,
                        h1["mx"],
                        h1["my"],
                        h1["c"],
                        h2["c"],
                    )
                    pair = {
                        "stage": stage,
                        "history_a": h1["history"],
                        "history_b": h2["history"],
                        "bits_a": history_bits(h1["history"], stage),
                        "bits_b": history_bits(h2["history"], stage),
                        "marginal_x": h1["mx"],
                        "marginal_y": h1["my"],
                        "covariance_a": h1["c"],
                        "covariance_b": h2["c"],
                        "mu_x": 1 - 2 * h1["mx"],
                        "mu_y": 1 - 2 * h1["my"],
                        "prob_a": h1["prob"],
                        "prob_b": h2["prob"],
                        "mechanism": mechanism,
                    }
                    pairs.append(pair)
                    if anomalous:
                        anomalies.append(pair)
        stages_out[stage] = {
            "alias_pair_count": len(pairs),
            "benign_merge_pair_count": benign,
            "distinct_marginals": len(buckets),
            "reachable_histories": len(rows),
            "pairs": pairs,
        }
        if stage == terminal_stage:
            terminal_count += len(pairs)
        else:
            prefix_count += len(pairs)

    t_proj = terminal_count == 0
    t_close = all(item["alias_pair_count"] == 0 for item in stages_out.values())
    if not t_proj:
        k1 = "A1"
    elif not t_close:
        k1 = "A2"
    else:
        k1 = "A0"
    cross = _cross_stage(stage_records)
    k2 = "A3" if cross["count"] > 0 else "NONE"
    return {
        "stages": stages_out,
        "terminal_alias_count": terminal_count,
        "same_phase_prefix_alias_count": prefix_count,
        "T_PROJ": t_proj,
        "T_CLOSE": t_close,
        "K1_outcome": k1,
        "K2_outcome": k2,
        "cross_stage": cross,
        "symmetry_anomalies": anomalies,
    }


def _cross_stage(stage_records):
    buckets = {}
    for stage, rows in stage_records.items():
        for row in rows:
            buckets.setdefault((row["mx"], row["my"]), []).append((stage, row))
    pairs = []
    for group in buckets.values():
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                stage_a, row_a = group[i]
                stage_b, row_b = group[j]
                if stage_a == stage_b:
                    continue
                if (stage_b, row_b["history"]) < (stage_a, row_a["history"]):
                    stage_a, row_a, stage_b, row_b = stage_b, row_b, stage_a, row_a
                pairs.append(
                    {
                        "stage_a": stage_a,
                        "history_a": row_a["history"],
                        "bits_a": history_bits(row_a["history"], stage_a),
                        "stage_b": stage_b,
                        "history_b": row_b["history"],
                        "bits_b": history_bits(row_b["history"], stage_b),
                        "marginal_x": row_a["mx"],
                        "marginal_y": row_a["my"],
                        "covariance_a": row_a["c"],
                        "covariance_b": row_b["c"],
                        "covariance_differs": row_a["c"] != row_b["c"],
                    }
                )
    return {"count": len(pairs), "pairs": pairs}


def min_marginal_separation(rows):
    """Minimum infinity-norm marginal gap over pairs whose covariance differs.

    Returns None when no such pair exists. Zero means an exact alias.
    Descriptive only: the number licenses nothing.
    """
    best = None
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rows[i]["c"] == rows[j]["c"]:
                continue
            distance = max(
                abs(rows[i]["mx"] - rows[j]["mx"]),
                abs(rows[i]["my"] - rows[j]["my"]),
            )
            if best is None or distance < best:
                best = distance
    return best


def interpretation(k1, k2):
    """Pre-written claim sentence. It does not change the admission verdict."""
    sentences = {
        "A0": (
            "In this world, exact marginals determine the terminal XOR forecast "
            "and an exact stage-indexed marginal filter exists on the reachable "
            "set. Gates (ii) and (iii) measure the information discarded by the "
            "product readout."
        ),
        "A1": (
            "The exact pair (P(X=1), P(Y=1)) is informationally insufficient for "
            "the terminal XOR forecast on reachable histories, under exact "
            "arithmetic with the stage known. This is a Q-EXIST fact about this "
            "world."
        ),
        "A2": (
            "A marginal-only state cannot be updated autonomously and exactly on "
            "the reachable set; joint information must be retained during "
            "filtering, even though the terminal marginals separate the histories."
        ),
    }
    text = sentences[k1]
    if k2 == "A3":
        text += (
            " Separately, under the clockless reading, at least one cross-stage "
            "marginal coincidence exists. That coincidence concerns time or "
            "modality and is not a covariance witness."
        )
    return text

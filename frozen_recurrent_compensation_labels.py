"""Mechanical labels, counts, and the stage-2 report text.

No consciousness claim. Labels do not train and do not look at TEST to choose a run.
"""

from __future__ import annotations

from frozen_recurrent_compensation_spec import (
    ACQUISITION_SENTENCE,
    BOUNDARY,
    COMPARATOR_UNRESOLVED,
    COMPONENT_NAMES,
    EXISTENCE_NONE,
    EXISTENCE_NOT_REACHED,
    EXISTENCE_WITNESS,
    FAIL,
    FINDING_1,
    FINDING_2,
    FINDING_4,
    G_PREFIX_NAME,
    INIT_WITNESS_SENTENCE,
    INVALID,
    NO_COMPARISON_TEST,
    PASS,
    REPRO_NO,
    REPRO_SENTENCE,
    REPRO_UNRESOLVED,
    REPRO_YES,
    SCOPE_SENTENCE,
    SEARCH_SIZE,
    SHARED_INIT_NOTE,
    TAU_DISCLOSURE,
    WITNESS_SENTENCE,
    no_witness_sentence,
    not_reached_sentence,
)


def stage1_final_reasons(record: dict) -> list[str]:
    """Invalid reasons known before target evaluation.

    Digest equality is required when the arm consumed the full 4000-batch stream
    and did not already fail a freezing check. An early stop is not also labeled
    a digest mismatch.
    """
    reasons = []
    early_without_freeze = record["steps_completed"] != 4000 and not record["freezing_failure"]
    if not record["integrity_training"] or early_without_freeze:
        reasons.append("training_integrity")
    if not record["checkpoint_round_trip"]:
        reasons.append("checkpoint_round_trip")
    if record["arm"] != "CAND":
        freeze_bad = bool(record["freezing_failure"])
        if record["w0_matches_stage0_after_training"] is not True:
            freeze_bad = True
        if record["w0_matches_stage0_after_reload"] is not True:
            freeze_bad = True
        if freeze_bad:
            reasons.append("freezing_check")
    full_stream = record["integrity_training"] and not record["freezing_failure"]
    if full_stream and (record["batches_hashed"] != 4000 or not record["episode_digest_matches_stage0"]):
        reasons.append("episode_digest")
    return reasons


def status_from(numeric_class: str | None, reasons: list[str]) -> str:
    if reasons:
        return INVALID
    if numeric_class in (PASS, FAIL, BOUNDARY):
        return numeric_class
    return INVALID


def arm_counts(runs: list[dict]) -> dict:
    if len(runs) != 10:
        raise RuntimeError("an arm has %d runs" % len(runs))
    passes = [run for run in runs if run["final_status"] == PASS]
    fails = [run for run in runs if run["final_status"] == FAIL]
    bounds = [run for run in runs if run["final_status"] == BOUNDARY]
    invalids = [run for run in runs if run["final_status"] == INVALID]
    if len(passes) + len(fails) + len(bounds) + len(invalids) != 10:
        raise RuntimeError("final statuses are not a partition")
    init_witnesses = [run for run in runs if run["init_status"] == PASS]
    acquisitions = [run for run in runs if run["init_status"] == FAIL and run["final_status"] == PASS]
    reason_map = {}
    for run in invalids:
        for reason in run["final_invalid_reasons"]:
            reason_map.setdefault(reason, []).append(run["seed"])
    init_invalid = [run for run in runs if run["init_status"] == INVALID]
    if init_witnesses or passes:
        existence = EXISTENCE_WITNESS
    elif len(fails) == 10:
        existence = EXISTENCE_NOT_REACHED
    else:
        existence = EXISTENCE_NONE
    unresolved = len(invalids) + len(bounds)
    if unresolved > 2:
        reproducibility = REPRO_UNRESOLVED
    elif len(passes) >= 8:
        reproducibility = REPRO_YES
    else:
        reproducibility = REPRO_NO
    return {
        "final_verified_passes": len(passes),
        "final_verified_fails": len(fails),
        "initialization_witnesses": len(init_witnesses),
        "initialization_witness_seeds": [run["seed"] for run in init_witnesses],
        "acquisition_annotations": len(acquisitions),
        "acquisition_seeds": [run["seed"] for run in acquisitions],
        "invalid_runs": len(invalids),
        "invalid_seeds": [run["seed"] for run in invalids],
        "invalid_reasons": reason_map,
        "boundary_runs": len(bounds),
        "boundary_seeds": [run["seed"] for run in bounds],
        "init_invalid": len(init_invalid),
        "init_invalid_reasons": _reason_map(init_invalid, "init_invalid_reasons"),
        "existence_label": existence,
        "reproducibility_label": reproducibility,
        "final_pass_seeds": [run["seed"] for run in passes],
    }


def _reason_map(runs: list[dict], field: str) -> dict:
    out = {}
    for run in runs:
        for reason in run[field]:
            out.setdefault(reason, []).append(run["seed"])
    return out


def statements_for_arm(arm: str, counts: dict) -> list[str]:
    sentences = []
    if arm != "CAND" and counts["existence_label"] == EXISTENCE_WITNESS:
        sentences.append(WITNESS_SENTENCE)
        if counts["acquisition_annotations"] > 0:
            sentences.append(ACQUISITION_SENTENCE)
        if counts["initialization_witnesses"] > 0:
            sentences.append(INIT_WITNESS_SENTENCE)
    if arm != "CAND" and counts["existence_label"] == EXISTENCE_NOT_REACHED:
        sentences.append(not_reached_sentence(arm))
    if arm != "CAND" and counts["existence_label"] == EXISTENCE_NONE:
        sentences.append(
            no_witness_sentence(arm, counts["boundary_runs"], counts["invalid_runs"])
        )
    if counts["reproducibility_label"] == REPRO_YES:
        sentences.append(REPRO_SENTENCE)
    if arm == "CAND":
        sentences.append(
            "CAND trains weight_hh. The restricted-class witness sentence is not applied to CAND."
        )
    return sentences


def format_counts_block(arm: str, counts: dict) -> str:
    reason_text = _format_reasons(counts["invalid_reasons"])
    lines = [
        "arm: %s" % arm,
        "final verified passes: %d/10" % counts["final_verified_passes"],
        "initialization witnesses: %d" % counts["initialization_witnesses"],
        "acquisition annotations: %d" % counts["acquisition_annotations"],
        "invalid runs: %d%s" % (counts["invalid_runs"], reason_text),
        "boundary or numerically unresolved runs: %d" % counts["boundary_runs"],
        "existence label: %s" % counts["existence_label"],
        "reproducibility label: %s" % counts["reproducibility_label"],
    ]
    if arm in ("CAND", "R-FIX-32"):
        lines.append(SHARED_INIT_NOTE)
    if counts["init_invalid"]:
        lines.append(
            "init checkpoints invalid: %d%s"
            % (counts["init_invalid"], _format_reasons(counts["init_invalid_reasons"]))
        )
    return "\n".join(lines)


def _format_reasons(reason_map: dict) -> str:
    if not reason_map:
        return ""
    parts = []
    for reason in sorted(reason_map):
        seeds = ", ".join(str(seed) for seed in reason_map[reason])
        parts.append("%s (%s)" % (reason, seeds))
    return ". reasons: " + "; ".join(parts)


def binding_frequencies(runs: list[dict], point: str) -> dict:
    status_key = "init_status" if point == "init" else "final_status"
    counts = {name: 0 for name in COMPONENT_NAMES}
    ties = 0
    used = 0
    for run in runs:
        if run[status_key] == INVALID:
            continue
        names = run[point]["binding_E1"]
        if not names:
            continue
        used += 1
        if len(names) > 1:
            ties += 1
        for name in names:
            counts[name] += 1
    return {"point": point, "denominator_classified": used, "counts": counts, "ties": ties}


def best_and_median(runs: list[dict]) -> dict:
    values = []
    for run in runs:
        if run["final_status"] == INVALID:
            continue
        block = run["final"].get("E1")
        if not block:
            continue
        values.append((run["seed"], float(block["T"])))
    if not values:
        return {"n": 0, "best_T": None, "best_seed": None, "median_T": None}
    best_seed, best_T = min(values, key=lambda item: (item[1], item[0]))
    ordered = sorted(value for _seed, value in values)
    count = len(ordered)
    if count % 2:
        median = ordered[count // 2]
    else:
        median = 0.5 * (ordered[count // 2 - 1] + ordered[count // 2])
    return {"n": count, "best_T": best_T, "best_seed": best_seed, "median_T": median}


def paired_differences(runs: list[dict]) -> list[dict]:
    index = {(run["seed"], run["arm"]): run for run in runs}
    rows = []
    for seed in range(400, 410):
        cand = index[(seed, "CAND")]
        row = {"seed": seed}
        for arm in ("R-FIX-32", "R-FIX-48"):
            other = index[(seed, arm)]
            if cand["final_status"] == INVALID or other["final_status"] == INVALID:
                row[arm] = None
            else:
                row[arm] = float(other["final"]["E1"]["T"] - cand["final"]["E1"]["T"])
        rows.append(row)
    return rows


def ledger_lines(arm: str, counts: dict, sentences: list[str]) -> list[str]:
    lines = []
    if arm == "CAND":
        lines.append("CAND is the unrestricted comparator.")
    elif counts["existence_label"] == EXISTENCE_WITNESS:
        lines.append(
            "Q-NECESSITY (restricted class %s, W2, GRU-8, declared target):" % arm
        )
        lines.extend(sentences)
        lines.append(format_counts_block(arm, counts))
        lines.append("Broader Q-NECESSITY: NOT_ESTABLISHED.")
    else:
        lines.append("Q-NECESSITY remains NOT_ESTABLISHED.")
        lines.append("%s existence label: %s." % (arm, counts["existence_label"]))
        lines.append(format_counts_block(arm, counts))
        if counts["reproducibility_label"] == REPRO_UNRESOLVED:
            lines.append("UNRESOLVED: no movement.")
    return lines


def _fmt(value) -> str:
    if value is None:
        return "n/a"
    return repr(float(value))


def _t(run: dict, point: str, which: str):
    block = run[point].get(which) if run[point].get("evaluated") else None
    if not block:
        return None
    return block["T"]


def _component(run: dict, point: str, name: str):
    block = run[point].get("E1") if run[point].get("evaluated") else None
    if not block:
        return None
    return block["components"][name]


def render_report(payload: dict) -> str:
    lines = [
        "# Frozen recurrent matrices with learned compensation",
        "",
        "No consciousness claim. Below C4. Within the GRU-8 family.",
        "",
        TAU_DISCLOSURE,
        "",
        FINDING_4,
        "",
        FINDING_1,
        "",
        FINDING_2,
        "",
        SCOPE_SENTENCE,
        "",
        SEARCH_SIZE,
        "",
        NO_COMPARISON_TEST,
        "",
        payload["comparator"],
        "",
        "G_prefix is %s. C_prefix = PD(q*) - L_prefix(final). Neither quantity gates the target."
        % G_PREFIX_NAME,
        "",
        "Float32 native forwards are stored as float32_descriptive and do not gate.",
        "Dual evaluation is a numerical cross-check, not a validated error bound for real arithmetic.",
        "These are numerically verified witnesses under the declared float64 evaluation, not formal real-arithmetic certificates.",
        "",
        "## Reference constants",
        "",
        "- tau = %s" % _fmt(payload["reference"]["tau"]),
        "- PD(q*) E1 = %s" % _fmt(payload["reference"]["PD_E1"]),
        "- PD(q*) E2 = %s" % _fmt(payload["reference"]["PD_E2"]),
        "- thr_total_TEST = %s" % _fmt(payload["reference"]["thr_total"]),
        "- thr_XOR_TEST = %s" % _fmt(payload["reference"]["thr_xor"]),
        "",
        "## Per-arm counts",
        "",
    ]
    for arm in ("CAND", "R-FIX-32", "R-FIX-48"):
        block = payload["arms"][arm]
        lines.append(format_counts_block(arm, block["counts"]))
        lines.append("")
        for sentence in block["statements"]:
            lines.append(sentence)
            lines.append("")
        best = block["best_median"]
        lines.append(
            "best T (minimum E1, smallest seed breaks ties): %s (seed %s). median T: %s. n=%s."
            % (_fmt(best["best_T"]), best["best_seed"], _fmt(best["median_T"]), best["n"])
        )
        lines.append("binding frequencies, final: %s" % block["binding_final"])
        lines.append("binding frequencies, init: %s" % block["binding_init"])
        lines.append("")
    lines.append("## Ledger")
    lines.append("")
    for arm in ("CAND", "R-FIX-32", "R-FIX-48"):
        for line in payload["arms"][arm]["ledger"]:
            lines.append(line)
        lines.append("")
    lines.append(SCOPE_SENTENCE)
    lines.append("")
    lines.append("## Per-seed T")
    lines.append("")
    lines.append("seed | arm | point | status | T_E1 | T_E2 | binding_E1 | prefix_E1 | total_E1 | xor_E1")
    lines.append("--- | --- | --- | --- | --- | --- | --- | --- | --- | ---")
    for run in payload["runs"]:
        for point, status_key in (("init", "init_status"), ("final", "final_status")):
            binding = run[point].get("binding_E1")
            binding_text = "n/a" if not binding else "+".join(binding)
            lines.append(
                "%d | %s | %s | %s | %s | %s | %s | %s | %s | %s"
                % (
                    run["seed"],
                    run["arm"],
                    point,
                    run[status_key],
                    _fmt(_t(run, point, "E1")),
                    _fmt(_t(run, point, "E2")),
                    binding_text,
                    _fmt(_component(run, point, "prefix")),
                    _fmt(_component(run, point, "total")),
                    _fmt(_component(run, point, "xor")),
                )
            )
    lines.append("")
    lines.append("## C_prefix and G_prefix")
    lines.append("")
    lines.append("G_prefix is %s." % G_PREFIX_NAME)
    lines.append("")
    lines.append("seed | arm | C_prefix_E1 | G_prefix_E1 | C_prefix_E2 | G_prefix_E2 | final_training_loss")
    lines.append("--- | --- | --- | --- | --- | --- | ---")
    for run in payload["runs"]:
        lines.append(
            "%d | %s | %s | %s | %s | %s | %s"
            % (
                run["seed"],
                run["arm"],
                _fmt(run["C_prefix_E1"]),
                _fmt(run["G_prefix_E1"]),
                _fmt(run["C_prefix_E2"]),
                _fmt(run["G_prefix_E2"]),
                _fmt(run["final_training_loss"]),
            )
        )
    lines.append("")
    lines.append("## Paired difference T(R-FIX) - T(CAND)")
    lines.append("")
    lines.append("Descriptive E1 final T. Null when either final is invalid.")
    lines.append("")
    lines.append("seed | R-FIX-32 | R-FIX-48")
    lines.append("--- | --- | ---")
    for row in payload["paired"]:
        lines.append("%d | %s | %s" % (row["seed"], _fmt(row["R-FIX-32"]), _fmt(row["R-FIX-48"])))
    lines.append("")
    lines.append("## In-sample descriptive subset (former VAL)")
    lines.append("")
    lines.append("Probability-weighted squared error renormalized on VAL histories. Descriptive only. E1.")
    lines.append("")
    lines.append("seed | arm | point | total | XOR")
    lines.append("--- | --- | --- | --- | ---")
    for run in payload["runs"]:
        for point in ("init", "final"):
            val = run[point].get("val_E1") if run[point].get("evaluated") else None
            total = None if not val else val["total"]
            xor = None if not val else val["XOR"]
            lines.append("%d | %s | %s | %s | %s" % (run["seed"], run["arm"], point, _fmt(total), _fmt(xor)))
    lines.append("")
    lines.append("## Deviations")
    lines.append("")
    lines.append(payload["deviations_during_stages"])
    lines.append("")
    lines.append("Pre-specified implementation choices are in frozen_recurrent_compensation_DEVIATIONS.md.")
    lines.append("")
    return "\n".join(lines) + "\n"

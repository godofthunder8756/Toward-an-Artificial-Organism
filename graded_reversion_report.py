"""Markdown reports. Phase A text is checked against the label ban before it is written."""

from __future__ import annotations

import re

from graded_reversion_spec import (
    BANNED_PHASE_A_WORDS,
    CODE_VERSION,
    PHASE_A_HEADLINE,
    PHASE_A_PREFIX,
    PRIMARY,
    TARGETS,
)
from graded_reversion_verdicts import (
    count_true,
    eligibility_failure_count,
    e1_replicated,
    precedence,
    primary_label,
    secondary_label,
    success_count_applied,
    transfer_label,
)

_BANNED = re.compile(r"\b(" + "|".join(BANNED_PHASE_A_WORDS) + r")\b", re.IGNORECASE)
_AGGREGATE = re.compile(r"\b\d+\s*/\s*10\b")


def assert_phase_a_text(text: str) -> None:
    if PHASE_A_PREFIX not in text:
        raise RuntimeError("phase A text is missing the required prefix")
    if "development-only" not in text and "DEVELOPMENT ONLY" not in text:
        raise RuntimeError("phase A text must say that it is development-only")
    if "not confirmatory" not in text.lower():
        raise RuntimeError("phase A text must say that it is not confirmatory")
    if "frozen before" not in text.lower():
        raise RuntimeError("phase A text must say that the criterion was frozen beforehand")
    banned = _BANNED.search(text)
    if banned:
        raise RuntimeError("phase A text contains a banned word: %s" % banned.group(0))
    aggregate = _AGGREGATE.search(text)
    if aggregate:
        raise RuntimeError("phase A text contains an out-of-ten count: %s" % aggregate.group(0))


def _fmt(value) -> str:
    if value is None:
        return "missing"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return value
    return format(float(value), ".8g")


def _reasons(record, target: str) -> str:
    reasons = record.get("eligibility_reasons", {}).get(target, [])
    if not reasons:
        return ""
    return "(" + ",".join(reasons) + ")"


def _target(record, target: str):
    targets = record.get("targets")
    if not targets:
        return None
    return targets.get(target)


def render_phase_a(records: list[dict], metadata: dict) -> str:
    lines = [
        "# " + PHASE_A_PREFIX,
        "",
        PHASE_A_HEADLINE,
        "",
        "Phase A is development-only and is not confirmatory. The confirmatory criterion was frozen before these results existed.",
        "",
        "- Code version: %s" % CODE_VERSION,
        "- Protocol sha256: `%s`" % metadata["protocol_sha256"],
        "- Freeze manifest sha256: `%s`" % metadata["freeze_manifest_sha256"],
        "- Freeze commit: `%s`" % metadata["freeze_commit"],
        "- Seeds: 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, listed one by one.",
        "- No out-of-ten summary is given. These seeds are not pooled with phase B.",
        "",
        "AUC is the integral of the piecewise-linear interpolant through the six measured dose-excess values. It is not a certified integral of the network's continuous dose response. Negative excesses are retained; no clipping or absolute-value transformation is applied.",
        "",
        "## Per-seed primary (`weight_hh`)",
        "",
        "| seed | L_prefix(F-TRAINED) | L_prefix/PD | B_prefix | B_prefix/PD | C_prefix | C_prefix/PD | AUC_REV | max random AUC | D | M | eligible |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in records:
        target = _target(record, PRIMARY)
        eligible = record["eligible"][PRIMARY]
        lines.append(
            "| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s %s |"
            % (
                record["seed"],
                _fmt(record.get("L_prefix_f_trained")),
                _fmt(record.get("L_prefix_f_trained_over_PD")),
                _fmt(record.get("B_prefix")),
                _fmt(record.get("B_prefix_over_PD")),
                _fmt(record.get("C_prefix")),
                _fmt(record.get("C_prefix_over_PD")),
                _fmt(None if target is None else target.get("auc_rev")),
                _fmt(None if target is None else target.get("auc_random_max")),
                _fmt(False if target is None else target.get("D")),
                _fmt(False if target is None else target.get("M")),
                _fmt(eligible),
                _reasons(record, PRIMARY),
            )
        )
    lines.extend(
        [
            "",
            "## Per-seed secondary blocks",
            "",
            "Secondary blocks use the same seed-level B_prefix and C_prefix. Eligibility can differ by the block displacement. These rows are not an aggregate.",
            "",
            "| seed | block | AUC_REV | max random AUC | D | M | eligible |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        for target_name in ("r", "z", "n"):
            target = _target(record, target_name)
            lines.append(
                "| %d | %s | %s | %s | %s | %s | %s %s |"
                % (
                    record["seed"],
                    target_name,
                    _fmt(None if target is None else target.get("auc_rev")),
                    _fmt(None if target is None else target.get("auc_random_max")),
                    _fmt(False if target is None else target.get("D")),
                    _fmt(False if target is None else target.get("M")),
                    _fmt(record["eligible"][target_name]),
                    _reasons(record, target_name),
                )
            )
    lines.extend(
        [
            "",
            "## Endpoint block errors, per seed",
            "",
            "Endpoint means dose α = 1. Δ is the excess over the intact F-TRAINED forecast. These values are exploratory and are not pooled.",
            "",
            "| seed | target | ΔL_prefix(1) | TEST E_total(1) | ΔE_total(1) | TEST E_XOR(1) | ΔE_XOR(1) |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        for target_name in TARGETS:
            target = _target(record, target_name)
            lines.append(
                "| %d | %s | %s | %s | %s | %s | %s |"
                % (
                    record["seed"],
                    target_name,
                    _fmt(None if target is None else target.get("endpoint_delta_L_prefix")),
                    _fmt(None if target is None else target.get("endpoint_E_TEST_total")),
                    _fmt(None if target is None else target.get("endpoint_delta_E_TEST_total")),
                    _fmt(None if target is None else target.get("endpoint_E_TEST_XOR")),
                    _fmt(None if target is None else target.get("endpoint_delta_E_TEST_XOR")),
                )
            )
    lines.extend(
        [
            "",
            "Invalid seeds, if any, keep their measured cells. A missing cell is written as `missing`. No seed is replaced.",
            "",
        ]
    )
    text = "\n".join(lines)
    assert_phase_a_text(text)
    return text


def _flags(records, key, target):
    flags = []
    for record in records:
        evaluation = record["evaluation"]
        if key == "valid":
            flags.append(bool(evaluation["valid"]))
        elif key == "transfer":
            flags.append(bool(evaluation["valid"] and evaluation["transfer_pass"]))
        elif key == "eligible":
            flags.append(bool(evaluation["eligible"][target]))
        elif key == "D":
            target_record = _target(evaluation, target)
            flags.append(bool(target_record and target_record["D"]))
        elif key == "M":
            target_record = _target(evaluation, target)
            flags.append(bool(target_record and target_record["M"]))
        elif key == "joint":
            flags.append(bool(evaluation["joint"][target]))
        else:
            raise ValueError(key)
    if len(flags) != 10:
        raise ValueError(len(flags))
    return flags


def render_phase_b(records: list[dict], metadata: dict, claim: str) -> str:
    if len(records) != 10:
        raise ValueError(len(records))
    e1_flags = [bool(record["e1_pass"]) for record in records]
    valid_flags = _flags(records, "valid", PRIMARY)
    joint_flags = _flags(records, "joint", PRIMARY)
    directional_flags = _flags(records, "D", PRIMARY)
    material_flags = _flags(records, "M", PRIMARY)
    eligible_flags = _flags(records, "eligible", PRIMARY)
    transfer_flags = [bool(record["evaluation"]["transfer_pass"]) for record in records]
    step = precedence(e1_flags, valid_flags)
    label = primary_label(e1_flags, valid_flags, joint_flags)
    applied = success_count_applied(e1_flags, valid_flags)
    invalid_count = sum(1 for flag in valid_flags if not flag)
    lines = [
        "# Graded joint recurrent reversion, phase B",
        "",
        "Phase B is the confirmatory phase on fresh seeds 200–209. The denominator is 10. Seeds are not removed from it. Phase A is not pooled with these seeds.",
        "",
        "- Code version: %s" % CODE_VERSION,
        "- Protocol sha256: `%s`" % metadata["protocol_sha256"],
        "- Freeze commit: `%s`" % metadata["freeze_commit"],
        "- Approval: Aidan Ahern, 2026-10-20, 10:38 PM ET, Grok Bot chat.",
        "",
        "## Precedence",
        "",
        "1. E1: %s (%d/10 CAND seeds with A-FIT on TEST, A-LEARN, and integrity)."
        % ("E1 REPLICATED" if e1_replicated(e1_flags) else "UNRESOLVED (E1 not replicated)", count_true(e1_flags)),
        "2. Invalid seeds: %d/10." % invalid_count,
        "3. Success count: %d/10 seeds passed (directional %d/10, materiality %d/10; eligibility failures %d/10)."
        % (
            count_true(joint_flags),
            count_true(directional_flags),
            count_true(material_flags),
            eligibility_failure_count(valid_flags, eligible_flags),
        ),
        "",
        "The deciding step is `%s`. The success count %s."
        % (step, "is applied to the label" if applied else "is not applied to the label"),
        "",
        "Seeds that miss M are below the declared materiality threshold.",
        "",
        "## Verdict",
        "",
        "**Label:** %s" % label,
        "",
        "**Claim:**",
        "",
        claim,
        "",
        "## Transfer replication",
        "",
        "%s (%d/10)."
        % (
            transfer_label(valid_flags, transfer_flags),
            sum(1 for valid, passed in zip(valid_flags, transfer_flags) if valid and passed),
        ),
        "",
        "Because eligibility includes a per-seed transfer pass, a primary REPLICATED label implies at least 8/10 transfer passes.",
        "",
        "## Secondary (block-wise)",
        "",
        "Secondary results are correlated with the primary and with each other. They are not independent replications. They do not substitute for the primary.",
        "",
    ]
    for target_name in ("r", "z", "n"):
        joint = _flags(records, "joint", target_name)
        directional = _flags(records, "D", target_name)
        material = _flags(records, "M", target_name)
        eligible = _flags(records, "eligible", target_name)
        lines.append(
            "- %s %d/10 seeds passed (directional %d/10, materiality %d/10; eligibility failures %d/10)."
            % (
                secondary_label(e1_flags, valid_flags, joint),
                count_true(joint),
                count_true(directional),
                count_true(material),
                eligibility_failure_count(valid_flags, eligible),
            )
        )
    lines.extend(
        [
            "",
            "## Per-seed primary",
            "",
            "| seed | valid | E1 | transfer | L_prefix(F-TRAINED) | B_prefix | B_prefix/PD | C_prefix | C_prefix/PD | AUC_REV | max random AUC | D | M | eligible | joint |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        evaluation = record["evaluation"]
        target = _target(evaluation, PRIMARY)
        lines.append(
            "| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
            % (
                record["seed"],
                _fmt(evaluation["valid"]),
                _fmt(record["e1_pass"]),
                _fmt(evaluation["transfer_pass"]),
                _fmt(evaluation.get("L_prefix_f_trained")),
                _fmt(evaluation.get("B_prefix")),
                _fmt(evaluation.get("B_prefix_over_PD")),
                _fmt(evaluation.get("C_prefix")),
                _fmt(evaluation.get("C_prefix_over_PD")),
                _fmt(None if target is None else target.get("auc_rev")),
                _fmt(None if target is None else target.get("auc_random_max")),
                _fmt(False if target is None else target.get("D")),
                _fmt(False if target is None else target.get("M")),
                _fmt(evaluation["eligible"][PRIMARY]),
                _fmt(evaluation["joint"][PRIMARY]),
            )
        )
    lines.extend(
        [
            "",
            "## Per-seed secondary",
            "",
            "| seed | block | AUC_REV | max random AUC | D | M | eligible | joint |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        evaluation = record["evaluation"]
        for target_name in ("r", "z", "n"):
            target = _target(evaluation, target_name)
            lines.append(
                "| %d | %s | %s | %s | %s | %s | %s | %s |"
                % (
                    record["seed"],
                    target_name,
                    _fmt(None if target is None else target.get("auc_rev")),
                    _fmt(None if target is None else target.get("auc_random_max")),
                    _fmt(False if target is None else target.get("D")),
                    _fmt(False if target is None else target.get("M")),
                    _fmt(evaluation["eligible"][target_name]),
                    _fmt(evaluation["joint"][target_name]),
                )
            )
    lines.extend(
        [
            "",
            "## Descriptive L_cont, XOR, and E_total",
            "",
            "L_cont, the XOR component, and E_total are descriptive. They do not gate the label. Vector success does not establish an XOR-specific effect.",
            "",
            "Basic intervention dependence is the measured forecast change and the measured prefix-function loss change under the specified weight changes.",
            "",
            "| seed | L_cont AUC | L_prefix XOR AUC | intact TEST E_XOR | endpoint TEST E_XOR | endpoint ΔE_total | endpoint ΔL_prefix | saturation | nondecreasing steps | max abs forecast change |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        evaluation = record["evaluation"]
        target = _target(evaluation, PRIMARY)
        lines.append(
            "| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
            % (
                record["seed"],
                _fmt(None if target is None else target.get("L_cont_auc")),
                _fmt(None if target is None else target.get("L_prefix_XOR_auc")),
                _fmt(evaluation.get("E_TEST_XOR_f_trained")),
                _fmt(None if target is None else target.get("endpoint_E_TEST_XOR")),
                _fmt(None if target is None else target.get("endpoint_delta_E_TEST_total")),
                _fmt(None if target is None else target.get("endpoint_delta_L_prefix")),
                _fmt(None if target is None else target.get("saturation")),
                _fmt(None if target is None else target.get("nondecreasing_steps")),
                _fmt(None if target is None else target.get("forecast_change_max_abs")),
            )
        )
    lines.extend(
        [
            "",
            "## Development history",
            "",
            "Phase A (seeds 100–109) is development-only and is not confirmatory. It is not pooled with seeds 200–209 and it is not support for the claim above. The confirmatory criterion was frozen before any phase A result existed. The phase A files are in `%s`."
            % metadata["phase_a_dir"],
            "",
        ]
    )
    return "\n".join(lines)

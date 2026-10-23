"""Markdown reports.

Phase A is per seed and carries no aggregate verdict. Phase B quotes the
preregistered paragraph for the label it assigns.
"""

from __future__ import annotations

import re

from first_order_control_criteria import margin_sentence
from first_order_control_spec import (
    BANNED_PHASE_A_WORDS,
    BLOCKS,
    CLAIM_NOT_MET,
    CLAIM_SUCCESS,
    CODE_VERSION,
    DISCLOSURE,
    FAMILY_FO,
    FAMILY_ISO,
    INHERITED_AUC_DISCLAIMER,
    INHERITED_ENDPOINT_SENTENCE,
    INHERITED_READOUT_LIMITATION,
    MONOTONIC_NOTE,
    NOT_CURVATURE,
    PHASE_A_HEADLINE,
    PHASE_A_PREFIX,
    PRIMARY,
    PRIMARY_REPLICATED,
    RESIDUAL_NAME,
    SINGLE_BLOCK_SENTENCE,
    TARGETS,
)
from first_order_control_verdicts import (
    count_true,
    other_eligibility_failures,
    primary_label,
    robustness_text,
    secondary_label,
    transfer_label,
    unevaluable_count,
    verdict_paragraph,
)

_BANNED = re.compile(r"\b(" + "|".join(BANNED_PHASE_A_WORDS) + r")\b")
_AGGREGATE = re.compile(r"\b\d+\s*/\s*10\b")
_THIN_AGGREGATE = "These descriptive findings do not change the frozen labels."


def assert_phase_a_text(text: str) -> None:
    if PHASE_A_PREFIX not in text:
        raise RuntimeError("phase A text is missing the required prefix")
    if PHASE_A_HEADLINE not in text:
        raise RuntimeError("phase A text is missing the headline")
    if "DEVELOPMENT ONLY" not in text:
        raise RuntimeError("phase A text must say that it is development-only")
    if "NOT CONFIRMATORY" not in text:
        raise RuntimeError("phase A text must say that it is not confirmatory")
    banned = _BANNED.search(text)
    if banned:
        raise RuntimeError("phase A text contains a banned word: %s" % banned.group(0))
    aggregate = _AGGREGATE.search(text)
    if aggregate:
        raise RuntimeError("phase A text contains an out-of-ten count: %s" % aggregate.group(0))
    if _THIN_AGGREGATE in text:
        raise RuntimeError("phase A text contains the aggregate thin-margin sentence")


def _fmt(value) -> str:
    if value is None:
        return "missing"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return value
    return format(float(value), ".8g")


def _summary(record, target):
    summary = record.get("summary") or {}
    return summary.get(target)


def _family_cells(report):
    if not report:
        return ("missing",) * 8
    return (
        _fmt(report.get("margin")),
        _fmt(report.get("m_over_B")),
        _fmt(report.get("m_over_PD")),
        _fmt(report.get("m_over_max")),
        _fmt(report.get("rank")),
        _fmt(report.get("n_end_gt")),
        _fmt(report.get("n_end_tie")),
        _fmt(report.get("endpoint_D")),
    )


def _phase_a_group(records: list[dict], title: str) -> list[str]:
    lines = [
        "## " + title,
        "",
        PHASE_A_HEADLINE,
        "",
        "Each seed is listed on its own. These rows are not pooled and they are not a verdict.",
        "",
        "| seed | valid | D_FO | D_ISO | D | M | joint | collapsed | margin_FO | margin_ISO | m/max_FO | m/max_ISO |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in records:
        summary = _summary(record, PRIMARY) or {}
        fo = summary.get("fo") or {}
        iso = summary.get("iso") or {}
        lines.append(
            "| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
            % (
                record["seed"],
                _fmt(record.get("valid")),
                _fmt(summary.get("D_FO")),
                _fmt(summary.get("D_ISO")),
                _fmt(summary.get("D")),
                _fmt(summary.get("M")),
                _fmt(summary.get("joint")),
                _fmt(summary.get("collapsed")),
                _fmt(fo.get("margin")),
                _fmt(iso.get("margin")),
                _fmt(fo.get("m_over_max")),
                _fmt(iso.get("m_over_max")),
            )
        )
    lines.extend(
        [
            "",
            "### Per-seed margins against both families",
            "",
            "| seed | target | family | margin | m/B | m/PD | m/max | rank | n_end_gt | n_end_tie | endpoint-D |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        for target in TARGETS:
            summary = _summary(record, target) or {}
            for family, report in (("FO", summary.get("fo")), ("ISO", summary.get("iso"))):
                cells = _family_cells(report)
                lines.append(
                    "| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |"
                    % ((record["seed"], target, family) + cells)
                )
    lines.extend(
        [
            "",
            "### Per-seed first-order diagnostics",
            "",
            "Autograd values of the inner product and cosine are the derivative values required by the protocol. "
            "The %s is not a curvature estimate. %s %s"
            % (RESIDUAL_NAME, NOT_CURVATURE, MONOTONIC_NOTE),
            "",
            "| seed | <G, delta> | cos(G, delta) | FO_AUC | residual_REV | R_eff/||delta|| | fixed blocks | negligible blocks |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        geometry = record.get("geometry") or {}
        summary = _summary(record, PRIMARY) or {}
        fixed = geometry.get("fixed_blocks") or []
        negligible = geometry.get("negligible_blocks") or []
        lines.append(
            "| %d | %s | %s | %s | %s | %s | %s | %s |"
            % (
                record["seed"],
                _fmt(geometry.get("G_dot_delta")),
                _fmt(geometry.get("cos_G_delta")),
                _fmt(geometry.get("FO_AUC")),
                _fmt(summary.get("residual_rev")),
                _fmt(geometry.get("R_eff_over_delta")),
                ",".join(fixed) if fixed else "none",
                ",".join(negligible) if negligible else "none",
            )
        )
    lines.extend(["", "### Endpoint prefix and descriptive errors", ""])
    lines.append("| seed | target | delta L_prefix(1) | delta L_cont(1) | delta E_total(1) | delta E_XOR(1) |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for record in records:
        targets = record.get("targets") or {}
        for target in TARGETS:
            item = targets.get(target) or {}
            lines.append(
                "| %d | %s | %s | %s | %s | %s |"
                % (
                    record["seed"],
                    target,
                    _fmt(item.get("endpoint_delta_L_prefix")),
                    _fmt(item.get("endpoint_delta_L_cont")),
                    _fmt(item.get("endpoint_delta_E_TEST_total")),
                    _fmt(item.get("endpoint_delta_E_TEST_XOR")),
                )
            )
    lines.append("")
    return lines


def render_phase_a(group_pr7: list[dict], group_pr8: list[dict], metadata: dict) -> str:
    lines = [
        "# " + PHASE_A_PREFIX,
        "",
        PHASE_A_HEADLINE,
        "",
        "Phase A is development-only and is not confirmatory. The two seed groups are reported separately and are not pooled. No aggregate thin-margin sentence is given.",
        "",
        "- Code version: %s" % CODE_VERSION,
        "- Protocol sha256: `%s`" % metadata["protocol_sha256"],
        "- Freeze commit: `%s`" % metadata["freeze_commit"],
        "",
        INHERITED_AUC_DISCLAIMER,
        "",
        DISCLOSURE,
        "",
    ]
    lines.extend(_phase_a_group(group_pr7, "PR #7 seeds 100-109"))
    lines.extend(_phase_a_group(group_pr8, "PR #8 seeds 200-209"))
    lines.extend(
        [
            "## Appendix B autograd comparison",
            "",
            metadata.get("appendix_b_note", ""),
            "",
        ]
    )
    text = "\n".join(lines)
    assert_phase_a_text(text)
    return text


def _flags(records, target, key):
    flags = []
    for record in records:
        evaluation = record["evaluation"]
        summary = (evaluation.get("summary") or {}).get(target) or {}
        if key == "valid":
            flags.append(bool(evaluation.get("valid")))
        elif key == "collapsed":
            if target == PRIMARY:
                flags.append(bool(evaluation.get("primary_collapsed")))
            else:
                flags.append(bool((evaluation.get("block_collapsed") or {}).get(target)))
        elif key == "transfer":
            flags.append(bool(evaluation.get("transfer_pass")))
        elif key == "e1":
            flags.append(bool(record.get("e1_pass")))
        else:
            flags.append(summary.get(key))
    return flags


def _count_line(name, flags) -> str:
    passed = sum(1 for flag in flags if flag is True)
    return "%s: %d/10 seeds passed" % (name, passed)


def _family_counts(records, target, family_key):
    thin = 0
    undefined = 0
    joint = 0
    strict = 0
    ties = 0
    endpoint = 0
    for record in records:
        summary = ((record["evaluation"].get("summary") or {}).get(target) or {})
        report = summary.get(family_key) or {}
        if summary.get("joint") is True:
            joint += 1
            if report.get("thin") is True:
                thin += 1
            if report.get("percentage_undefined") is True:
                undefined += 1
        if (report.get("n_end_gt") or 0) >= 1:
            strict += 1
        if (report.get("n_end_tie") or 0) >= 1:
            ties += 1
        if report.get("endpoint_D") is True:
            endpoint += 1
    return thin, joint, undefined, strict, ties, endpoint


def render_phase_b(records: list[dict], metadata: dict) -> str:
    if len(records) != 10:
        raise ValueError(len(records))
    e1 = [bool(record["e1_pass"]) for record in records]
    valid = [bool(record["evaluation"]["valid"]) for record in records]
    collapsed = [bool(record["evaluation"].get("primary_collapsed")) for record in records]
    joint = [bool((record["evaluation"].get("summary") or {}).get(PRIMARY, {}).get("joint")) for record in records]
    label = primary_label(e1, valid, collapsed, joint)
    paragraph = verdict_paragraph(label)
    if label == PRIMARY_REPLICATED and paragraph != CLAIM_SUCCESS:
        raise RuntimeError("success paragraph drifted")
    if label != PRIMARY_REPLICATED and label != "JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET":
        if paragraph == CLAIM_SUCCESS or paragraph == CLAIM_NOT_MET and label.startswith("UNRESOLVED"):
            pass
    lines = [
        "# Graded recurrent reversion against both first-order-matched and isotropic controls",
        "",
        "Phase B is the confirmatory phase on fresh seeds 300-309. The denominator is 10. Phase A is not pooled with these seeds.",
        "",
        "- Code version: %s" % CODE_VERSION,
        "- Protocol sha256: `%s`" % metadata["protocol_sha256"],
        "- Freeze commit: `%s`" % metadata["freeze_commit"],
        "- Approval: Aidan Ahern, 2026-10-21, 1:05 AM ET, Grok Bot chat, widget t23s2.",
        "",
        "## Verdict",
        "",
        "**Label:** %s" % label,
        "",
        paragraph,
        "",
        DISCLOSURE,
        "",
        "## Transfer replication",
        "",
        transfer_label(valid, [bool(record["evaluation"].get("transfer_pass")) for record in records]),
        "",
        "## Counts",
        "",
        _count_line("D_FO", _flags(records, PRIMARY, "D_FO")),
        _count_line("D_ISO", _flags(records, PRIMARY, "D_ISO")),
        _count_line("D_FO and D_ISO", _flags(records, PRIMARY, "D")),
        _count_line("M", _flags(records, PRIMARY, "M")),
        _count_line("joint", joint),
        "invalid: %d/10" % sum(1 for flag in valid if not flag),
        "collapsed: %d/10" % unevaluable_count([True] * 10, collapsed),
        "invalid or collapsed: %d/10" % unevaluable_count(valid, collapsed),
        "other eligibility failures: %d/10" % other_eligibility_failures(
            valid,
            [bool((record["evaluation"].get("summary") or {}).get(PRIMARY, {}).get("eligible")) for record in records],
            collapsed,
        ),
        "",
        "Seeds that do not pass the joint rule are listed with each failed condition. A failed D_ISO is a failed isotropic comparison. A failed D_FO is a failed first-order-matched comparison. The failure is not attributed to one family unless that seed's flags say so.",
        "",
        "| seed | valid | eligible | D_FO | D_ISO | M | joint | collapsed | reasons |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for record in records:
        evaluation = record["evaluation"]
        summary = (evaluation.get("summary") or {}).get(PRIMARY) or {}
        reasons = ",".join(summary.get("eligibility_reasons") or [])
        lines.append(
            "| %d | %s | %s | %s | %s | %s | %s | %s | %s |"
            % (
                record["seed"],
                _fmt(evaluation.get("valid")),
                _fmt(summary.get("eligible")),
                _fmt(summary.get("D_FO")),
                _fmt(summary.get("D_ISO")),
                _fmt(summary.get("M")),
                _fmt(summary.get("joint")),
                _fmt(summary.get("collapsed")),
                reasons,
            )
        )
    lines.extend(["", "## Margins against both families", ""])
    for family_key, family_name in (("fo", FAMILY_FO), ("iso", FAMILY_ISO)):
        thin, joint_count, undefined, strict, ties, endpoint = _family_counts(records, PRIMARY, family_key)
        lines.append(margin_sentence(thin, joint_count, undefined, strict, ties, endpoint, family_name))
        lines.append("")
    robust = robustness_text(
        label,
        joint,
        [bool(((record["evaluation"].get("summary") or {}).get(PRIMARY) or {}).get("fo", {}) and ((record["evaluation"].get("summary") or {}).get(PRIMARY) or {})["fo"].get("thin")) for record in records],
        [bool(((record["evaluation"].get("summary") or {}).get(PRIMARY) or {}).get("iso", {}) and ((record["evaluation"].get("summary") or {}).get(PRIMARY) or {})["iso"].get("thin")) for record in records],
    )
    if robust:
        lines.extend([robust, ""])
    lines.extend(
        [
            INHERITED_AUC_DISCLAIMER,
            "",
            INHERITED_ENDPOINT_SENTENCE,
            "",
            INHERITED_READOUT_LIMITATION,
            "",
            "## Secondary blocks",
            "",
            "Secondary results are correlated with the primary and with each other. They do not substitute for the primary and there is no any-block upgrade.",
            "",
        ]
    )
    any_secondary = False
    for block in BLOCKS:
        block_valid = valid
        block_collapsed = [bool((record["evaluation"].get("block_collapsed") or {}).get(block)) for record in records]
        block_joint = [bool((record["evaluation"].get("summary") or {}).get(block, {}).get("joint")) for record in records]
        block_label = secondary_label(block, e1, block_valid, block_collapsed, block_joint)
        lines.append("- %s (%d/10 joint)" % (block_label, count_true(block_joint)))
        if block_label.endswith(PRIMARY_REPLICATED):
            any_secondary = True
    if not any_secondary:
        lines.extend(["", SINGLE_BLOCK_SENTENCE, ""])
    lines.extend(
        [
            "",
            "## First-order diagnostics",
            "",
            "The %s is reported for each seed. %s" % (RESIDUAL_NAME, NOT_CURVATURE),
            MONOTONIC_NOTE,
            "",
            "| seed | <G, delta> | cos | FO_AUC | residual_REV | negligible | fixed |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        evaluation = record["evaluation"]
        geometry = evaluation.get("geometry") or {}
        summary = (evaluation.get("summary") or {}).get(PRIMARY) or {}
        lines.append(
            "| %d | %s | %s | %s | %s | %s | %s |"
            % (
                record["seed"],
                _fmt(geometry.get("G_dot_delta")),
                _fmt(geometry.get("cos_G_delta")),
                _fmt(geometry.get("FO_AUC")),
                _fmt(summary.get("residual_rev")),
                ",".join(geometry.get("negligible_blocks") or []) or "none",
                ",".join(geometry.get("fixed_blocks") or []) or "none",
            )
        )
    lines.extend(
        [
            "",
            "## Descriptive L_cont, XOR and E_total",
            "",
            "These quantities are descriptive. Vector success does not establish an XOR-specific effect.",
            "",
            "| seed | L_cont AUC | L_prefix XOR AUC | delta E_total(1) | delta E_XOR(1) |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for record in records:
        target = ((record["evaluation"].get("targets") or {}) or {}).get(PRIMARY) or {}
        lines.append(
            "| %d | %s | %s | %s | %s |"
            % (
                record["seed"],
                _fmt(target.get("L_cont_auc")),
                _fmt(target.get("L_prefix_XOR_auc")),
                _fmt(target.get("endpoint_delta_E_TEST_total")),
                _fmt(target.get("endpoint_delta_E_TEST_XOR")),
            )
        )
    lines.extend(
        [
            "",
            "## Development history",
            "",
            "Exploratory phase A curves for seeds 100-109 and 200-209 are in `first_order_control_phaseA_exploratory/`. They are development-only and are not confirmatory. They are not pooled with seeds 300-309, and they do not set this label.",
            "",
            "Freeze commit: `%s`." % metadata["freeze_commit"],
            "",
        ]
    )
    return "\n".join(lines)

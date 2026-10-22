"""Factual report. States section 5 labels and the values underneath them."""

from __future__ import annotations


def _section_lines(section5: dict | None) -> list[str]:
    if not section5:
        return ["Section 5 was not formed."]
    lines = []
    if "label" in section5 and "ALL" not in section5 and "MARG" not in section5:
        lines.append(f"Package outcome: {section5.get('label')}.")
        if section5.get("reason"):
            lines.append(str(section5["reason"]))
        return lines
    for group in ("ALL", "MARG"):
        row = section5.get(group)
        if not row:
            continue
        lines.append(f"{group}: {row['label']}. {row['reason']}")
        values = row.get("values") or {}
        for key in ("sqrt_H", "sqrt_H_threshold", "R", "R_threshold", "H", "S", "L_full", "measured_gain"):
            if key in values:
                lines.append(f"{group} {key} = {values[key]}")
    return lines


def render(results: dict) -> str:
    lines = [
        "# C-kappa oracle package report",
        "",
        "Claim ceiling: oracle facts only. This report states the event-order and forecast fixtures, derivatives, template geometry, perturbation validity, headroom against the fitted fixed-kappa comparator at k = 4, and the behavior of the two synthetic fixtures. It makes no neural, acquisition, mechanism, S12, S15, C4, or consciousness statement.",
        "",
        f"Stop kind: {results.get('stop_kind')}",
        "",
        "## Section 5",
        "",
    ]
    if results.get("stop_kind") == "INTEGRITY STOP" and results.get("section5") is None:
        lines.append("No outcome label.")
    else:
        lines.extend(_section_lines(results.get("section5")))
    o6_section5 = results.get("o6_section5")
    if o6_section5 and results.get("stop_kind") not in (None, "COMPLETED"):
        lines.append("O6 outcome label recorded separately from the stop kind:")
        lines.extend(_section_lines(o6_section5))
    lines.append("")
    lines.append("Thresholds at eps_syn = 0.1 are declared conventions. Other eps_syn sizes are reported in the stage files and do not replace the reference.")
    lines.append("ALL outcomes other than MET mean no inference specification is drafted without a new ruling.")
    lines.append("MARG outcomes other than AVAILABLE mean MARG is descriptive only.")
    lines.append("")
    lines.append("## Stages")
    lines.append("")
    lines.append("Completed stage files: " + ", ".join(results.get("stages_completed") or []) + ".")
    o7 = (results.get("stages") or {}).get("O7")
    if o7:
        lines.append(f"O7 status: {o7.get('status')}.")
        if o7.get("voided_count") is not None:
            lines.append(f"O7 voided prefixes: {o7.get('voided_count')}.")
        if o7.get("integrity_diagnosis"):
            lines.append(str(o7["integrity_diagnosis"]))
    lines.append("")
    lines.append("Losses are conditional on the common scoreable-edit subset when a mask is applied. Retained mass is in the stage files.")
    lines.append("Per-edit traces are not stored. The first 1,000 O6 propagations are listed in results.json under retained_o6_sample.")
    lines.append("")
    projection = results.get("projection")
    if projection:
        lines.append("## Step 0 projection")
        lines.append("")
        lines.append(f"T_rem_s = {projection.get('T_rem_s')}")
        lines.append(f"projection_limit_s = {projection.get('projection_limit_s')}")
        lines.append(f"T_elapsed_s = {projection.get('T_elapsed_s')}")
        lines.append(f"N_float_remaining = {projection.get('N_float_remaining')}")
        lines.append("")
    lines.append("No interpretation beyond these section 5 labels is stated.")
    lines.append("")
    return "\n".join(lines)

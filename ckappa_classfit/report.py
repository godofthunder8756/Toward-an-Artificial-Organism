"""Stage S8 report template.

Standing wording only. A stored label is quoted. No new claim is added.
C9.4: outputs do not carry a hard-coded status word for the draft or the bundle.
"""

from __future__ import annotations

E37_3 = (
    "O7's zero gain follows from its symmetry-preserving global least-squares construction: "
    "complete flip-orbit fits, invariant continuation weights, a constant marginal-state map, "
    "and the declared odd-in-each-marginal lookup. It is not evidence that two-coordinate systems "
    "generally lack kappa-row gain. Comparator loss divided by response energy is not described "
    "as an orthogonal allocation of that energy."
)
E37_4 = (
    "Failure of the global-map intervention criterion means that the declared criterion was not met. "
    "It does not establish absence of covariance sensitivity, absence of a global direction, or "
    "absence of a nonlinear or prefix-dependent coordinate relation. The prospective S6 design does "
    "not proceed to checkpoint inference unchanged."
)
E37_10 = (
    "Any subsequent neural result is limited to prediction of intervention-induced forecasts by the "
    "declared prefix-conditioned oracle response models. It does not identify the reachable-history "
    "algorithm, establish acquisition, isolate the recurrent transition from the readout, exclude "
    "general lookup implementations, or establish irreducible joint state, C4 or consciousness."
)
E38_15 = (
    "This package tests implementation identities, synthetic response headroom and limitations of "
    "declared intervention-prediction models on specified synthetic systems. It establishes no result "
    "about trained GRUs and answers none of Q-EXIST, Q-LEARN, Q-CAUSE or Q-NECESSITY. Confound gains "
    "do not identify an independent covariance register or exclude two-coordinate mediation or "
    "reachable-set lookup implementations. Failure of a class-conditioned criterion does not exclude "
    "nonlinear, prefix-dependent or orbit-dependent covariance codes. No result establishes acquisition, "
    "recurrent-transition-specific use, necessity, irreducible joint state, C4, C5, consciousness, "
    "autopoiesis or life."
)
L202 = (
    "Failure of the declared class-conditioned criterion does not exclude orbit-dependent covariance "
    "codes, including codes whose local coordinate relation differs on held-out orbits."
)
L194 = (
    "in the CD, BD and BC fitting folds, full-rank recovery produces the negative-sign chart map, "
    "which is wrong on held-out A whenever the edit has a nonzero relevant component."
)
FK_SENTENCE = "FK checks the κ row on the product-chart designs, not on the SYS-O6/SYS-PC designs."
PC_SUCCESS = (
    "The class-conditioned fit recovered the declared sign-dependent synthetic map, which the global "
    "fit cancels as derived."
)
NEGATIVE_GLOBAL = "The declared global-map intervention-prediction criterion was not met."
NEGATIVE_CLASS = "The declared class-conditioned-map intervention-prediction criterion was not met."

TEMPLATE = "\n".join(
    [
        "# C-kappa class-conditioned synthetic package",
        "",
        "Claim ceiling, E38-15, verbatim:",
        E38_15,
        "",
        "E37-10, verbatim:",
        E37_10,
        "",
        "Retained #38 L202 sentence, verbatim:",
        L202,
        "",
        "E37-3, verbatim:",
        E37_3,
        "",
        "E37-4, verbatim:",
        E37_4,
        "",
        "Ratio wording: Comparator squared prediction error divided by actual response energy.",
        "Oracle labels, when quoted from the earlier oracle package: Oracle-scale headroom only.",
        "Cap-limited work is incomplete.",
        "When a stored label says a declared criterion failed, the wording is one of these two sentences:",
        NEGATIVE_GLOBAL,
        NEGATIVE_CLASS,
        "",
        "Permitted SYS-PC success sentence. It is printed again below only when the stored class label is IDENTITY AS DERIVED, the stored VALIDATION label is CLASS-FIT VALIDATION MET, the stored HEADROOM ALL label is MET, and the stored HEADROOM MARG label is AVAILABLE. This template does not assert that those labels hold:",
        PC_SUCCESS,
        "That sentence does not show that a network uses κ, carries a class label, or has a covariance register.",
        "Headroom thresholds are synthetic conventions.",
        "",
        FK_SENTENCE,
        "No impossibility of alternatives is stated.",
        "",
        "SYS-LIM is described only with this failure statement: " + L194,
        "A declared transport rule using the state's magnitude could represent this system; the selected maps do not contain that rule.",
        "SYS-LIM is not a two-coordinate system.",
        "Compatible with two-coordinate mediation is not applied to SYS-LIM.",
        "",
        "SYS-NC1 is described as a varying-κ two-coordinate confound.",
        "RMS matching is never described as matching response, conditioning, transferability or GRU geometry.",
        "SYS-NC1 and SYS-NC3 are not called affine.",
        "SYS-PC and SYS-LIM are called affine only within their declared non-crossing branches.",
        "Affine claims stay with their system and domain.",
        "",
        "A guard inconsistency is reported with margins and residuals. It is not described as proof that the recovery tolerance was exceeded.",
        "The reverse guard direction is recorded on its own and does not stop.",
        "UNRESOLVED-B3 is not described as a passed guard. NOT EVALUATED is not described as a passed identity.",
        "",
        "D6 cells report the residual and the premise status only. They do not carry PASS or FAIL. INVESTIGATE belongs to D7 only.",
        "D7 INVESTIGATE is retained prominently. Any later decision about neural work must address it. Unchanged labels do not resolve it. D7 INVESTIGATE is non-stopping and stays outside VALIDATION and HEADROOM.",
        "",
        "The class label is supplied by the analyst from the prefix index. Class models have 4 times the parameters of the global model. The extended B3 guard is not described as applicable to neural two-coordinate systems.",
        "",
        "Elapsed time, when a figure is printed below, is results.json field t_elapsed_s. Its source is time.time() minus CKAPPA_CLASSFIT_T0.",
        "Memory, when a figure is printed below, is the run.log observation ru_maxrss_kb from resource.getrusage(RUSAGE_SELF).ru_maxrss, and VmPeak from /proc/self/status.",
        "No new claim is stated.",
        "",
    ]
)


def render(results: dict) -> str:
    lines = [TEMPLATE.rstrip(), "", "## Stored labels", ""]
    lines.append(f"Stop kind: {results.get('stop_kind')}")
    validation = results.get("VALIDATION") or {}
    lines.append(f"VALIDATION label: {validation.get('label')}")
    headroom = results.get("HEADROOM") or {}
    for group in ("ALL", "MARG"):
        row = headroom.get(group) or {}
        lines.append(f"HEADROOM {group} label: {row.get('label')}")
    investigate = results.get("d7_investigate") or []
    if investigate:
        lines.append("D7 INVESTIGATE flags, prominent:")
        for row in investigate:
            lines.append(f"D7 INVESTIGATE {row.get('identity_id')}")
    else:
        lines.append("D7 INVESTIGATE flags stored with this report: none in the stored matrix identities.")
    success = False
    for row in results.get("labels") or []:
        lines.append(
            f"{row.get('system')} {row.get('fit_type')} {row.get('group')}: {row.get('label')}"
        )
        if (
            row.get("system") == "SYS-PC"
            and row.get("fit_type") == "class"
            and row.get("label") == "IDENTITY AS DERIVED"
            and validation.get("label") == "CLASS-FIT VALIDATION MET"
            and (headroom.get("ALL") or {}).get("label") == "MET"
            and (headroom.get("MARG") or {}).get("label") == "AVAILABLE"
        ):
            success = True
    if success:
        lines.append(PC_SUCCESS)
    elapsed = results.get("t_elapsed_s")
    if elapsed is not None:
        source = results.get("t_elapsed_s_source") or "time.time() minus CKAPPA_CLASSFIT_T0"
        lines.append(f"t_elapsed_s = {elapsed}")
        lines.append(f"t_elapsed_s source: {source}")
    memory = results.get("memory_observation")
    if isinstance(memory, dict):
        lines.append(f"ru_maxrss_kb = {memory.get('ru_maxrss_kb')}")
        lines.append(f"ru_maxrss source: {memory.get('ru_maxrss_source')}")
        lines.append(f"VmPeak = {memory.get('VmPeak')}")
        lines.append(f"VmPeak source: {memory.get('VmPeak_source')}")
    lines.append("")
    return "\n".join(lines)

"""Human-readable report. Decision language stays inside the spec's ceiling."""

from __future__ import annotations

from audit.gru_v1_3.accounting import binomial_arithmetic

CEILING = (
    "On the declared W2 history domain and orbit-respecting decoder splits, adding hidden "
    "state improved prediction of oracle probabilities beyond the specified output and input "
    "baselines by the prespecified margin in the reported checkpoint blocks. This demonstrates "
    "bounded decoder accessibility under the declared analysis. It does not establish that the "
    "predictors assess or use knowledge of their own errors."
)
QUALIFICATION = (
    "The comparison is conditional on the declared feature sets, regularization and split. "
    "Input-baseline extrapolation and changes in effective shrinkage may contribute to the gain."
)
C2_WORDING = "beyond the declared input baselines under this split"
PR5 = "PR #5: MISSING PERSISTED CHECKPOINTS; NOT EVALUATED."


def _fmt(value):
    if value is None:
        return "NA"
    if isinstance(value, str):
        return value
    return "%.16g" % value


def _counts(c):
    return "m=%d b=%d x=%d u=%d i=%d" % (c["m"], c["b"], c["x"], c["u"], c["i"])


def render(payload: dict) -> str:
    lines = []
    add = lines.append
    complete = payload["audit_complete"]
    add("# GRU hidden-state oracle-accessibility audit report (spec v1.3)")
    add("")
    if complete:
        add("Every scheduled output in S0, P, D and the report was produced.")
    else:
        add("The audit as a whole is not described as complete.")
        add("Unfinished outputs are marked INCOMPLETE. No omitted computation is treated as a scientific failure.")
    add("")
    add("C2 measures improvement %s." % C2_WORDING)
    add("A gain is improvement under this feature-and-regularization procedure.")
    add("The input-only B_in+ → q calculation is a target-decoding calculation. It is not described as outcome-blind merely because it needs no checkpoint.")
    add("INIT, uniform weighting, the inner-λ sensitivity, AC|BD, T, R_exc, correlations and rank are descriptive and are not floor labels.")
    add("Unresolved cases are never counted as below-floor. INCOMPLETE cases are never counted as below-floor.")
    add("")
    add("## Records")
    add("")
    add("- Spec sha256: `%s`" % payload["spec_sha256"])
    add("- Roster sha256: `%s`" % payload["roster_sha256"])
    add("- Implementation manifest sha256: `%s`" % payload["manifest_sha256"])
    add("- Input-bit array sha256 (float64, 256×8, stage 0 is the least significant bit): `%s`" % payload["bits_sha256"])
    add("- %s" % PR5)
    add("")
    c = payload["constants"]
    add("## Executable constants")
    add("")
    add("- R_oracle = %s" % _fmt(c["R_oracle"]))
    add("- Var_w(q) = %s" % _fmt(c["Var_w_q"]))
    add("- floor = %s" % _fmt(c["floor"]))
    add("- R²-gain floor = %s" % _fmt(c["r2_floor"]))
    add("- uniform-weight Var(q) = %s (descriptive denominator only)" % _fmt(c["var_q_uniform"]))
    add("- primary λ = 1e-3")
    add("- zero-variance rule: Var <= 1e-24")
    add("")
    arith = binomial_arithmetic()
    add("%s (%d/%d)." % (arith["statement"], arith["numerator"], arith["denominator"]))
    add("")
    add("## Input-only B_in+ → q")
    add("")
    inp = payload["input_only"]
    if inp.get("status") == "INCOMPLETE":
        add("INCOMPLETE")
    else:
        add("Pooled loss (E32-7 denominator 3·Σw) = %s" % _fmt(inp["pooled"]))
        add("Per-fold loss is the eval-set P(h)-weighted mean.")
        for name, value in inp["per_fold"].items():
            add("- %s: %s" % (name, _fmt(value)))
        add("Fixed λ = 1e-3. Not a gate. No floor label.")
    add("")
    add("## Claim-reporting units")
    add("")
    add("Each unit is one (PR, arm) across its ten declared seed checkpoints. Counts m, b, x, u and i sum to 10.")
    add("")
    add("| PR | arm | m | b | x | u | i | quota |")
    add("|---|---|---:|---:|---:|---:|---:|---|")
    for unit in payload["units"]:
        c = unit["counts"]
        add("| %d | %s | %d | %d | %d | %d | %d | %s |" % (
            unit["pr"], unit["arm"], c["m"], c["b"], c["x"], c["u"], c["i"], unit["quota"]))
    add("")
    add("## PR-level integrity")
    add("")
    for row in payload["pr_level"]:
        add("- PR #%d: verified seeds %d/10. %s" % (row["pr"], row["verified_seeds"], row["statement"]))
    add("")
    add("## Quota wording")
    add("")
    any_ceiling = False
    for unit in payload["units"]:
        if unit["quota"] == "quota is attained":
            any_ceiling = True
            add("### PR #%d %s" % (unit["pr"], unit["arm"]))
            add("")
            add(CEILING)
            add("")
            add(QUALIFICATION)
            add("")
            add("Remaining counts in this unit: %s." % _counts(unit["counts"]))
            add("")
    if not any_ceiling:
        add("No (PR, arm) unit attained the descriptive 8/10 quota, so the claim ceiling is not applied.")
        add("")
    add("## Per-checkpoint primary results")
    add("")
    add("Foldwise loss is the eval-set weighted mean. Pooled loss uses the E32-7 denominator. AC|BD uses denominator 1·Σw and has no floor label.")
    add("R_exc is the original predictor's excess Brier risk, Σ_h w(h) Σ_j (f_j − q_j)². It is descriptive and is not a gate.")
    add("")
    for ck in payload["checkpoints"]:
        _checkpoint_block(add, ck)
    add("## INIT tier")
    add("")
    add("INIT is descriptive only. No meets-floor, below-floor or BOUNDARY label is issued.")
    add("PR #10 CAND init and R-FIX-32 init duplicates are kept for provenance and are not independent evidence.")
    add("")
    for row in payload.get("init_duplicate_notes", []):
        add("- seed %s CAND init vs R-FIX-32 init identical=%s" % (row["seed"], row["identical"]))
    add("")
    for ck in payload["init_checkpoints"]:
        _checkpoint_block(add, ck)
    add("## Per-seed median Δ")
    add("")
    add("Median of pooled primary Δ across TRAINED checkpoints of that seed, separately for C1 and for C2. Even counts use the average of the two central values.")
    add("")
    for row in payload["seed_medians"]:
        add("- PR #%d seed %d: %s C1=%s C2=%s" % (
            row["pr"], row["seed"], row["status"], _fmt(row.get("median_C1")), _fmt(row.get("median_C2"))))
    add("")
    add("## Descriptive sensitivities")
    add("")
    add("Inner-λ selection is a mismatched validation geometry. No direction of bias in the selected λ is asserted. It has no floor label and does not determine primary labels.")
    add("Uniform-weight R² uses uniform-weight Var(q) and has no floor label.")
    add("")
    _section_status(add, "Inner-λ sensitivity", payload["inner_status"], payload["inner"])
    _section_status(add, "Uniform-weight sensitivity", payload["uniform_status"], payload["uniform"])
    add("## T")
    add("")
    add("T is descriptive. A positive sum is not called a double dissociation. No T result establishes an error-assessment role.")
    add("Within-seed cross-arm pairs and same-arm cross-seed pairs are kept separate and are not pooled. Pairs that share checkpoints are not independent evidence.")
    add("Zero target variance (Var <= 1e-24) makes the affected R², brackets and T UNDEFINED. They are not imputed.")
    add("")
    _section_status(add, "T pairs", payload["T_status"], payload["T"])
    add("## Correlations and e_P variation")
    add("")
    add("A correlation whose weighted variance is <= 1e-24 for either argument is UNDEFINED and is not imputed.")
    add("")
    _section_status(add, "Correlations", payload["correlation_status"], payload["correlations"])
    _section_status(add, "e_P variation", payload["variation_status"], payload["variation"])
    add("## Runtime")
    add("")
    rt = payload["runtime"]
    add("- Wall-clock seconds: %s" % _fmt(rt["wall_seconds"]))
    add("- Aggregate CPU seconds (user+system, process and children): %s" % _fmt(rt["cpu_seconds"]))
    add("- Stage seconds: %s" % rt["stages"])
    add("- Caps: S0 10 min, P 15 min, D 20 min, report 5 min, cumulative wall-clock 50 min, one pinned CPU, 4 GB address space, single-threaded BLAS and torch.")
    if rt.get("cap_reached"):
        add("- A cap was reached. Unfinished outputs are INCOMPLETE.")
    add("")
    add("## Deviations")
    add("")
    if payload["deviations"]:
        for item in payload["deviations"]:
            add("- %s" % item)
    else:
        add("No additive deviation was required during execution.")
    add("")
    add("Full foldwise values, rank, excluded features, inner-λ records, uniform-weight records, T pairs and correlations are in results.json, which is part of this report.")
    add("")
    return "\n".join(lines) + "\n"


def _section_status(add, title, status, rows):
    add("### %s" % title)
    add("")
    if status == "INCOMPLETE" and not rows:
        add("INCOMPLETE")
        add("")
        return
    if status == "INCOMPLETE":
        add("INCOMPLETE after %d finished records." % len(rows))
    else:
        add("Records: %d." % len(rows))
    add("Values are in results.json.")
    add("")


def _checkpoint_block(add, ck):
    add("### %s" % ck["id"])
    add("")
    add("- status: %s" % ck["status"])
    if ck.get("replay_label"):
        add("- replay: %s" % ck["replay_label"])
    if ck.get("reasons"):
        add("- reasons: %s" % "; ".join(ck["reasons"]))
    for mismatch in ck.get("mismatches") or []:
        add("- mismatch field `%s`: value=%s recorded=%s abs_diff=%s" % (
            mismatch.get("field"), _fmt(mismatch.get("value")),
            _fmt(mismatch.get("recorded")), _fmt(mismatch.get("abs_diff"))))
    add("- R_exc: %s" % _fmt(ck.get("R_exc")))
    if ck.get("forward"):
        fw = ck["forward"]
        add("- numpy vs torch step max-abs state/output: %s / %s" % (
            _fmt(fw.get("numpy_vs_step_state")), _fmt(fw.get("numpy_vs_step_output"))))
        add("- numpy vs torch batched forward max-abs state/output: %s / %s" % (
            _fmt(fw.get("numpy_vs_forward_state")), _fmt(fw.get("numpy_vs_forward_output"))))
    for name in ("C1", "C2"):
        block = ck.get(name)
        if not block:
            add("- %s: not issued" % name)
            continue
        add("- %s pooled L(base)=%s L(full)=%s Δ=%s R² gain=%s label=%s" % (
            name, _fmt(block["L_base"]), _fmt(block["L_full"]), _fmt(block["delta"]),
            _fmt(block["r2"]), block.get("label", "none")))
        folds = ", ".join("%s:%s" % (row["fold"], _fmt(row["delta"])) for row in block["foldwise"])
        add("  - foldwise Δ: %s" % folds)
        ac = block["acbd"]
        add("  - AC|BD L(base)=%s L(full)=%s Δ=%s R² gain=%s (no floor label)" % (
            _fmt(ac["L_base"]), _fmt(ac["L_full"]), _fmt(ac["delta"]), _fmt(ac["r2"])))
    add("")

"""Single certificate run for the frozen two-stream world.

Run from the repository root after TWOSTREAM_FREEZE_v1.json matches the
source tree:

    python twostream_run.py

The runner refuses to start when the freeze hashes differ or when
twostream_results_v1/ already exists. It enumerates each horizon once.
"""

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

from twostream_alias import audit_stages, interpretation, min_marginal_separation
from twostream_chart import belief_from_chart, forecasts, in_simplex, marginals_covariance
from twostream_constants import N_READINGS, variable_at
from twostream_enumerate import EnumerationFailure, enumerate_horizon
from twostream_filter import initial_belief, observe
from twostream_score import (
    COVARIANCE_SHIFT_THRESHOLD,
    INTERVENTION_MASS_THRESHOLD,
    XOR_EXCESS_THRESHOLD,
    classify_run,
    current_only_terminal,
    decimal_truncation,
    expected_squared_error,
    fraction_bit_lengths,
    fraction_record,
    gate_i_pass,
    gate_ii_pass,
    gate_iii_pass,
    gate_iv_pass,
    intervention_mass,
    irreducible_brier,
)

ROOT = Path(__file__).resolve().parent
RESULTS_DIR = ROOT / "twostream_results_v1"
FREEZE_PATH = ROOT / "TWOSTREAM_FREEZE_v1.json"

CLAIM_CEILING = (
    "Benchmark admission and ordinary-state reduction for this frozen world "
    "only. Passing admits the world as an analytic benchmark whose ordinary "
    "three-number chart is the joint posterior in different coordinates. "
    "It does not promote C2 or C3, does not advance O3, does not resolve A6, "
    "and does not unblock A8. It does not authorize a learning protocol, "
    "neural training, organism work, a mean-field arm, or a ledger edit."
)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 16), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_freeze():
    if not FREEZE_PATH.is_file():
        raise SystemExit("missing freeze file: %s" % FREEZE_PATH.name)
    return json.loads(FREEZE_PATH.read_text(encoding="utf-8"))


def assert_freeze(freeze):
    mismatches = []
    for name, digest in freeze["files"].items():
        path = ROOT / name
        if not path.is_file():
            mismatches.append("%s missing" % name)
            continue
        got = sha256_file(path)
        if got != digest:
            mismatches.append("%s hash mismatch" % name)
    if mismatches:
        raise SystemExit("freeze check failed: " + "; ".join(mismatches))


def to_jsonable(obj):
    if isinstance(obj, Fraction):
        return fraction_record(obj)
    if isinstance(obj, dict):
        return {str(key): to_jsonable(value) for key, value in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_jsonable(value) for value in obj]
    if isinstance(obj, bool) or obj is None or isinstance(obj, str):
        return obj
    if isinstance(obj, int):
        return obj
    raise TypeError(type(obj))


def _max_abs(values):
    best = Fraction(0)
    for value in values:
        if abs(value) > best:
            best = abs(value)
    return best


def _storage_for_beliefs(records):
    total_num = 0
    total_den = 0
    max_num = 0
    max_den = 0
    for row in records:
        for mass in row["belief"]:
            num_bits, den_bits = fraction_bit_lengths(mass)
            total_num += num_bits
            total_den += den_bits
            if num_bits > max_num:
                max_num = num_bits
            if den_bits > max_den:
                max_den = den_bits
    return {
        "entries": len(records),
        "numbers_per_entry": 4,
        "free_parameters_per_entry": 3,
        "representation": "four reduced posterior masses in state-index order",
        "total_numerator_bits": total_num,
        "total_denominator_bits": total_den,
        "max_numerator_bits": max_num,
        "max_denominator_bits": max_den,
    }


def _shared_denominator_storage(records, denominator):
    total_num = 0
    max_num = 0
    for row in records:
        for numerator in row["joint_numerators"]:
            bits = int(numerator).bit_length()
            total_num += bits
            if bits > max_num:
                max_num = bits
    return {
        "entries": len(records),
        "numbers_per_entry": 4,
        "shared_denominator_bits": int(denominator).bit_length(),
        "total_numerator_bits": total_num,
        "max_numerator_bits": max_num,
    }


def _marginal_index(rows):
    groups = {}
    for row in rows:
        groups.setdefault((row["mx"], row["my"]), set()).add(row["c"])
    max_num = 0
    max_den = 0
    total_num = 0
    total_den = 0
    for (mx, my), covariances in groups.items():
        values = [mx, my]
        if len(covariances) == 1:
            values.append(next(iter(covariances)))
        for value in values:
            num_bits, den_bits = fraction_bit_lengths(value)
            total_num += num_bits
            total_den += den_bits
            if num_bits > max_num:
                max_num = num_bits
            if den_bits > max_den:
                max_den = den_bits
    return {
        "distinct_marginal_keys": len(groups),
        "exact_lookup": all(len(values) == 1 for values in groups.values()),
        "max_numerator_bits": max_num,
        "max_denominator_bits": max_den,
        "total_numerator_bits": total_num,
        "total_denominator_bits": total_den,
    }


def _score_terminal(records):
    failures = []
    probabilities = []
    q_x = []
    q_y = []
    q_xor = []
    q_xor_fact = []
    q_x_current = []
    q_y_current = []
    q_xor_current = []
    covariances = []
    for row in records:
        qx, qy, qxor = forecasts(row["mx"], row["my"], row["c"])
        q_fact = row["mx"] + row["my"] - 2 * row["mx"] * row["my"]
        if q_fact - qxor != 2 * row["c"]:
            failures.append("2c identity failed at history %d" % row["history"])
        if qx != row["mx"] or qy != row["my"]:
            failures.append("marginal forecast mismatch at history %d" % row["history"])
        last = (row["history"] >> (N_READINGS - 1)) & 1
        mx_c, my_c, c_c = current_only_terminal(last)
        cx, cy, cxor = forecasts(mx_c, my_c, c_c)
        if mx_c != Fraction(1, 2) or c_c != 0:
            failures.append("current-only closed form left the uniform-X point")
        clamped = belief_from_chart(row["mx"], row["my"], Fraction(0))
        if not in_simplex(clamped):
            failures.append("clamp left the simplex at history %d" % row["history"])
        probabilities.append(row["prob"])
        q_x.append(qx)
        q_y.append(qy)
        q_xor.append(qxor)
        q_xor_fact.append(q_fact)
        q_x_current.append(cx)
        q_y_current.append(cy)
        q_xor_current.append(cxor)
        covariances.append(row["c"])
    excess_xor = expected_squared_error(probabilities, q_xor_fact, q_xor)
    moment_xor = Fraction(0)
    for prob, cov in zip(probabilities, covariances):
        moment_xor += prob * 4 * cov * cov
    if excess_xor != moment_xor:
        failures.append("XOR excess and 4 E[c^2] disagree")
    excess_x_fact = expected_squared_error(probabilities, q_x, q_x)
    excess_y_fact = expected_squared_error(probabilities, q_y, q_y)
    xy_unchanged = excess_x_fact == 0 and excess_y_fact == 0
    if not xy_unchanged:
        failures.append("factorized arm moved an X or Y forecast")
    excess_x = expected_squared_error(probabilities, q_x_current, q_x)
    excess_y = expected_squared_error(probabilities, q_y_current, q_y)
    excess_xor_current = expected_squared_error(probabilities, q_xor_current, q_xor)
    for name, value in (
        ("X", excess_x),
        ("Y", excess_y),
        ("XOR", excess_xor_current),
    ):
        if value < 0:
            failures.append("negative %s Brier excess" % name)
    history_excess = excess_x + excess_y + excess_xor_current
    if history_excess <= 0:
        failures.append("gate (i) is not strictly positive, contradicting the sign proof")
    if not any(row["mx"] != Fraction(1, 2) for row in records):
        failures.append("no terminal history has m_x different from 1/2")
    mean_mx = Fraction(0)
    mean_my = Fraction(0)
    mean_p11 = Fraction(0)
    for prob, row in zip(probabilities, records):
        mean_mx += prob * row["mx"]
        mean_my += prob * row["my"]
        mean_p11 += prob * (row["mx"] * row["my"] + row["c"])
    if mean_mx != Fraction(1, 2) or mean_my != Fraction(1, 2) or mean_p11 != Fraction(1, 4):
        failures.append(
            "terminal posterior averages to m_x=%s m_y=%s p11=%s"
            % (mean_mx, mean_my, mean_p11)
        )
    mass = intervention_mass(probabilities, covariances)
    return {
        "failures": failures,
        "history_excess": history_excess,
        "excess_x": excess_x,
        "excess_y": excess_y,
        "excess_xor_current": excess_xor_current,
        "xor_excess": excess_xor,
        "mass": mass,
        "mean_mx": mean_mx,
        "mean_my": mean_my,
        "mean_p11": mean_p11,
        "xy_unchanged": xy_unchanged,
        "probabilities": probabilities,
        "q_x": q_x,
        "q_y": q_y,
        "q_xor": q_xor,
        "q_xor_fact": q_xor_fact,
        "covariances": covariances,
    }


def _current_only_matches_filter():
    failures = []
    uniform = initial_belief()
    if variable_at(N_READINGS - 1) != "Y":
        failures.append("reading 8 does not observe Y")
    for bit in (0, 1):
        posterior, predictive = observe(uniform, "Y", bit)
        mx, my, cov = marginals_covariance(posterior)
        closed = current_only_terminal(bit)
        if (mx, my, cov) != closed or predictive != Fraction(1, 2):
            failures.append("current-only disagrees with the one-step filter at bit %d" % bit)
    return failures


def build_certificate(freeze_commit, freeze):
    stages = {}
    for n_readings in range(1, N_READINGS + 1):
        stages[n_readings] = enumerate_horizon(n_readings)
        print("agreed horizon %d (%d histories)" % (n_readings, 1 << n_readings), flush=True)
    terminal = stages[N_READINGS]["records"]
    scored = _score_terminal(terminal)
    failures = list(scored["failures"])
    failures.extend(_current_only_matches_filter())
    mismatches = 0
    checked = 0
    for payload in stages.values():
        for row in payload["records"]:
            checked += 1
            rebuilt = belief_from_chart(row["mx"], row["my"], row["c"])
            if rebuilt != row["belief"]:
                mismatches += 1
    if mismatches:
        failures.append("chart mismatch on %d reachable beliefs" % mismatches)
    if checked != sum(1 << n for n in range(1, N_READINGS + 1)):
        failures.append("reachable-belief count is %d" % checked)

    stage_rows = {}
    for n_readings, payload in stages.items():
        stage_rows[n_readings] = [
            {
                "history": row["history"],
                "mx": row["mx"],
                "my": row["my"],
                "c": row["c"],
                "prob": row["prob"],
            }
            for row in payload["records"]
        ]
    audit = audit_stages(stage_rows, terminal_stage=N_READINGS)
    if audit["symmetry_anomalies"]:
        failures.append("alias symmetry label inconsistent with the flip identities")
    separation = {
        n_readings: min_marginal_separation(rows) for n_readings, rows in stage_rows.items()
    }
    marginal_index = {n_readings: _marginal_index(rows) for n_readings, rows in stage_rows.items()}

    gates_bool = {
        "i": gate_i_pass(scored["history_excess"]),
        "ii": gate_ii_pass(scored["xor_excess"]),
        "iii": gate_iii_pass(scored["mass"], scored["xy_unchanged"]),
        "iv": gate_iv_pass(mismatches),
    }
    # A false sign on (i) is already an integrity failure. Keep the boolean
    # aligned with the numerical comparison either way.
    verdict = classify_run(failures, gates_bool)
    zero_mass = Fraction(0)
    nonzero_count = 0
    shift_count = 0
    for prob, cov in zip(scored["probabilities"], scored["covariances"]):
        if cov == 0:
            zero_mass += prob
        else:
            nonzero_count += 1
        if abs(cov) >= COVARIANCE_SHIFT_THRESHOLD:
            shift_count += 1
    second_moment = scored["xor_excess"] / 4
    risks = {}
    for label, oracle in (
        ("X", scored["q_x"]),
        ("Y", scored["q_y"]),
        ("XOR", scored["q_xor"]),
    ):
        risks[label] = {
            "oracle_brier": irreducible_brier(scored["probabilities"], oracle),
        }
    risks["X"]["current_only_excess"] = scored["excess_x"]
    risks["Y"]["current_only_excess"] = scored["excess_y"]
    risks["XOR"]["current_only_excess"] = scored["excess_xor_current"]
    risks["XOR"]["factorized_excess"] = scored["xor_excess"]
    risks["X"]["factorized_excess"] = Fraction(0)
    risks["Y"]["factorized_excess"] = Fraction(0)
    risks["X"]["current_only_brier"] = risks["X"]["oracle_brier"] + scored["excess_x"]
    risks["Y"]["current_only_brier"] = risks["Y"]["oracle_brier"] + scored["excess_y"]
    risks["XOR"]["current_only_brier"] = (
        risks["XOR"]["oracle_brier"] + scored["excess_xor_current"]
    )
    risks["XOR"]["factorized_brier"] = risks["XOR"]["oracle_brier"] + scored["xor_excess"]

    per_history = []
    for row, qxor, q_fact in zip(terminal, scored["q_xor"], scored["q_xor_fact"]):
        per_history.append(
            {
                "history": row["history"],
                "bits": row["bits"],
                "probability": row["prob"],
                "marginal_x": row["mx"],
                "marginal_y": row["my"],
                "covariance": row["c"],
                "xor_joint": qxor,
                "xor_factorized": q_fact,
                "abs_xor_shift": abs(2 * row["c"]),
                "belief": row["belief"],
                "joint_numerators": [str(value) for value in row["joint_numerators"]],
            }
        )

    mechanism_counts = {}
    for stage, info in audit["stages"].items():
        counts = {}
        for pair in info["pairs"]:
            counts[pair["mechanism"]] = counts.get(pair["mechanism"], 0) + 1
        mechanism_counts[str(stage)] = counts

    certificate = {
        "certificate": "two-stream world-admission analytic certificate v1",
        "verdict": verdict,
        "claim_ceiling": CLAIM_CEILING,
        "mean_field_arm": False,
        "arms": [
            "joint_bayes",
            "factorized_terminal_projection",
            "marginals_plus_covariance",
            "current_observation_only",
            "direct_history_table",
        ],
        "freeze_commit": freeze_commit,
        "freeze_file_sha256": sha256_file(FREEZE_PATH),
        "frozen_files": freeze["files"],
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "horizon": N_READINGS,
        "history_count": len(terminal),
        "reachable_beliefs_checked": checked,
        "probability_sum": Fraction(1),
        "min_history_probability": min(row["prob"] for row in terminal),
        "terminal_law": {
            "mean_marginal_x": scored["mean_mx"],
            "mean_marginal_y": scored["mean_my"],
            "mean_p11": scored["mean_p11"],
        },
        "global_denominator": str(stages[N_READINGS]["denominator"]),
        "integrity": {
            "ok": not failures,
            "failures": failures,
        },
        "gates": {
            "i": {
                "name": "history",
                "statement": "current-only one-component Brier sum exceeds the joint oracle",
                "value": scored["history_excess"],
                "threshold": "> 0",
                "verdict": "PASS" if gates_bool["i"] else "FAIL",
                "components": {
                    "X": scored["excess_x"],
                    "Y": scored["excess_y"],
                    "XOR": scored["excess_xor_current"],
                },
            },
            "ii": {
                "name": "consequential joint information",
                "statement": "factorized terminal projection XOR Brier excess",
                "value": scored["xor_excess"],
                "threshold": ">= 1/1000",
                "threshold_exact": XOR_EXCESS_THRESHOLD,
                "verdict": "PASS" if gates_bool["ii"] else "FAIL",
            },
            "iii": {
                "name": "selective content consequence",
                "statement": "zero-covariance substitution changes the XOR forecast by at least 1/20",
                "value": scored["mass"],
                "threshold": ">= 1/4 of history probability mass",
                "threshold_exact": INTERVENTION_MASS_THRESHOLD,
                "shift_threshold": COVARIANCE_SHIFT_THRESHOLD,
                "xy_forecasts_unchanged": scored["xy_unchanged"],
                "verdict": "PASS" if gates_bool["iii"] else "FAIL",
            },
            "iv": {
                "name": "ordinary chart identity",
                "statement": "marginals plus covariance reproduce the joint filter",
                "role": "algebraic identity and implementation check",
                "mismatches": mismatches,
                "beliefs_checked": checked,
                "verdict": "PASS" if gates_bool["iv"] else "FAIL",
            },
        },
        "risks": risks,
        "covariance": {
            "second_moment": second_moment,
            "four_second_moment": scored["xor_excess"],
            "max_abs": _max_abs(scored["covariances"]),
            "zero_probability_mass": zero_mass,
            "nonzero_history_count": nonzero_count,
            "shift_history_count_nongating": shift_count,
            "shift_history_fraction_uniform_nongating": Fraction(shift_count, len(terminal)),
            "off_manifold_clamp_history_count": nonzero_count,
            "clamp_coincides_with_reachable_history_count": len(terminal) - nonzero_count,
        },
        "storage": {
            "arm5_reduced_posterior_table": _storage_for_beliefs(terminal),
            "arm5_shared_denominator_table": _shared_denominator_storage(
                terminal, stages[N_READINGS]["denominator"]
            ),
            "marginal_index_by_stage": marginal_index,
            "online_filter_retained_numbers": 3,
        },
        "descriptive_min_marginal_separation": separation,
        "alias_summary": {
            "T_PROJ": audit["T_PROJ"],
            "T_CLOSE": audit["T_CLOSE"],
            "K1_outcome": audit["K1_outcome"],
            "K2_outcome": audit["K2_outcome"],
            "terminal_alias_count": audit["terminal_alias_count"],
            "same_phase_prefix_alias_count": audit["same_phase_prefix_alias_count"],
            "cross_stage_marginal_coincidence_count": audit["cross_stage"]["count"],
            "mechanism_counts_by_stage": mechanism_counts,
            "interpretation": interpretation(audit["K1_outcome"], audit["K2_outcome"]),
            "gating": False,
        },
        "per_history": per_history,
    }
    return certificate, audit


def unresolved_certificate(freeze_commit, freeze, failures):
    return {
        "certificate": "two-stream world-admission analytic certificate v1",
        "verdict": "UNRESOLVED",
        "claim_ceiling": CLAIM_CEILING,
        "mean_field_arm": False,
        "freeze_commit": freeze_commit,
        "freeze_file_sha256": sha256_file(FREEZE_PATH),
        "frozen_files": freeze["files"],
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "integrity": {"ok": False, "failures": failures},
        "gates": {
            "i": {"verdict": "NOT_CERTIFIED"},
            "ii": {"verdict": "NOT_CERTIFIED"},
            "iii": {"verdict": "NOT_CERTIFIED"},
            "iv": {"verdict": "NOT_CERTIFIED"},
        },
        "alias_summary": None,
    }


def _exact(record):
    if isinstance(record, dict) and "exact" in record:
        return record["exact"]
    return str(record)


def _decimal(record):
    if isinstance(record, dict) and "decimal_truncation_50" in record:
        return record["decimal_truncation_50"]
    return decimal_truncation(record) if isinstance(record, Fraction) else str(record)


def render_markdown(cert):
    gates = cert["gates"]
    lines = [
        "# Two-stream world-admission certificate v1",
        "",
        "Analytic enumeration of the frozen eight-reading world. One run. "
        "No parameter was changed after the freeze.",
        "",
        "- Verdict: **%s**" % cert["verdict"],
        "- Freeze commit: `%s`" % cert["freeze_commit"],
        "- Freeze file SHA-256: `%s`" % cert["freeze_file_sha256"],
        "- Generated UTC: %s" % cert["generated_utc"],
        "- Histories: %s" % cert.get("history_count", "unavailable"),
        "- Mean-field arm: not run",
        "",
        "## Claim ceiling",
        "",
        cert["claim_ceiling"],
        "",
        "Gates (ii) and (iii) are two functionals of the terminal covariance. "
        "They are not two independent lines of evidence. Gate (iv) is the "
        "chart identity. The alias audit does not change this verdict.",
        "",
        "## Gates",
        "",
        "| Gate | Exact value | Decimal truncation | Threshold | Verdict |",
        "| --- | --- | --- | --- | --- |",
    ]
    if "value" in gates["i"]:
        lines.append(
            "| (i) history excess | `%s` | `%s` | > 0 | %s |"
            % (_exact(gates["i"]["value"]), _decimal(gates["i"]["value"]), gates["i"]["verdict"])
        )
        lines.append(
            "| (ii) XOR Brier excess | `%s` | `%s` | >= 1/1000 | %s |"
            % (
                _exact(gates["ii"]["value"]),
                _decimal(gates["ii"]["value"]),
                gates["ii"]["verdict"],
            )
        )
        lines.append(
            "| (iii) intervention mass | `%s` | `%s` | >= 1/4 | %s |"
            % (
                _exact(gates["iii"]["value"]),
                _decimal(gates["iii"]["value"]),
                gates["iii"]["verdict"],
            )
        )
        lines.append(
            "| (iv) chart mismatches | `%s` |  | identity, 0 required | %s |"
            % (gates["iv"]["mismatches"], gates["iv"]["verdict"])
        )
    else:
        for key in ("i", "ii", "iii", "iv"):
            lines.append("| (%s) |  |  |  | %s |" % (key, gates[key]["verdict"]))
    lines.extend(["", "## Integrity", ""])
    if cert["integrity"]["ok"]:
        lines.append("All frozen implementation checks passed.")
    else:
        lines.append("Implementation checks failed. The verdict is UNRESOLVED.")
        for item in cert["integrity"]["failures"]:
            lines.append("- %s" % item)
    summary = cert.get("alias_summary")
    lines.extend(["", "## Alias audit", ""])
    if not summary:
        lines.append("Alias audit was not certified.")
    else:
        lines.append(
            "- K1 outcome: **%s** (T-PROJ %s, T-CLOSE %s)"
            % (
                summary["K1_outcome"],
                "holds" if summary["T_PROJ"] else "fails",
                "holds" if summary["T_CLOSE"] else "fails",
            )
        )
        lines.append("- K2 outcome: **%s**" % summary["K2_outcome"])
        lines.append("- Terminal alias pairs: %s" % summary["terminal_alias_count"])
        lines.append(
            "- Same-phase prefix alias pairs: %s" % summary["same_phase_prefix_alias_count"]
        )
        lines.append(
            "- Cross-stage marginal coincidences, reported separately: %s"
            % summary["cross_stage_marginal_coincidence_count"]
        )
        lines.append("- Mechanism counts by stage: `%s`" % json.dumps(summary["mechanism_counts_by_stage"]))
        lines.append("")
        lines.append(summary["interpretation"])
        lines.append("")
        lines.append(
            "Witnesses are reachable posteriors. The zero-covariance clamp is "
            "an off-manifold diagnostic when covariance is nonzero, and it was "
            "not eligible as a witness. This paragraph does not change the "
            "admission verdict and does not promote a cognitive layer."
        )
    if "covariance" in cert:
        cov = cert["covariance"]
        lines.extend(
            [
                "",
                "## Covariance functionals",
                "",
                "- E[c^2] = `%s`" % _exact(cov["second_moment"]),
                "- E[4c^2] = `%s`" % _exact(cov["four_second_moment"]),
                "- max |c| = `%s`" % _exact(cov["max_abs"]),
                "- P(c = 0) = `%s`" % _exact(cov["zero_probability_mass"]),
                "- Histories with c = 0 (clamp coincides with the reachable posterior): %s"
                % cov["clamp_coincides_with_reachable_history_count"],
                "- Histories with c ≠ 0 (clamp is off-manifold): %s"
                % cov["off_manifold_clamp_history_count"],
                "- Uniform history fraction with |c| ≥ 1/40, descriptive and non-gating: `%s`"
                % _exact(cov["shift_history_fraction_uniform_nongating"]),
            ]
        )
    if "storage" in cert:
        arm5 = cert["storage"]["arm5_reduced_posterior_table"]
        lines.extend(
            [
                "",
                "## Storage",
                "",
                "Arm 5, the direct-history table, stores %s entries and %s reduced masses per entry (%s free)."
                % (arm5["entries"], arm5["numbers_per_entry"], arm5["free_parameters_per_entry"]),
                "Maximum reduced numerator bits %s, maximum denominator bits %s."
                % (arm5["max_numerator_bits"], arm5["max_denominator_bits"]),
                "The online joint filter retains 3 numbers, updated in place.",
                "Marginal-index entry counts are in `results.json`. An exact marginal lookup exists only where the alias audit says the marginal key determines covariance.",
            ]
        )
    if "per_history" in cert:
        lines.extend(
            [
                "",
                "## Terminal histories",
                "",
                "Reading 1 is the leftmost bit. Exact rationals; decimals are in `results.json`.",
                "",
                "| Bits | P(h) | m_x | m_y | c | q_XOR | q_XOR factorized |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in cert["per_history"]:
            lines.append(
                "| `%s` | `%s` | `%s` | `%s` | `%s` | `%s` | `%s` |"
                % (
                    row["bits"],
                    _exact(row["probability"]),
                    _exact(row["marginal_x"]),
                    _exact(row["marginal_y"]),
                    _exact(row["covariance"]),
                    _exact(row["xor_joint"]),
                    _exact(row["xor_factorized"]),
                )
            )
    lines.extend(
        [
            "",
            "Full machine-readable values, including 50-digit truncations and the shared-denominator numerators, are in `results.json`. Every alias witness is in `alias_audit.json`.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(certificate, audit):
    RESULTS_DIR.mkdir()
    payload = to_jsonable(certificate)
    (RESULTS_DIR / "results.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    if audit is None:
        alias_payload = {"certified": False, "verdict": certificate["verdict"]}
    else:
        alias_payload = to_jsonable(audit)
        alias_payload["certified"] = True
        alias_payload["interpretation"] = certificate["alias_summary"]["interpretation"]
        alias_payload["gating"] = False
    (RESULTS_DIR / "alias_audit.json").write_text(
        json.dumps(alias_payload, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    (RESULTS_DIR / "RESULTS.md").write_text(render_markdown(payload) + "\n", encoding="utf-8")


def git_head():
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
    ).strip()


def main():
    if RESULTS_DIR.exists():
        raise SystemExit("refusing to rerun: %s already exists" % RESULTS_DIR.name)
    freeze = load_freeze()
    assert_freeze(freeze)
    commit = git_head()
    audit = None
    try:
        certificate, audit = build_certificate(commit, freeze)
    except EnumerationFailure as exc:
        certificate = unresolved_certificate(commit, freeze, list(exc.failures))
    write_outputs(certificate, audit)
    print("verdict %s" % certificate["verdict"], flush=True)
    print("wrote %s" % RESULTS_DIR, flush=True)


if __name__ == "__main__":
    sys.exit(main())

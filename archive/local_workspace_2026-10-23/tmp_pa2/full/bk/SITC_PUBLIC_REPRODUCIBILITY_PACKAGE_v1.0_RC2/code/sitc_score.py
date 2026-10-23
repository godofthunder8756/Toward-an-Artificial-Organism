# SPDX-License-Identifier: MPL-2.0
"""Portable scientific-only scorer for the frozen SITC v1 assay.

The scientific constants and functions from ``FROZEN_DECISION_SHA256``
through ``score_raw_run`` are extracted verbatim from the authoritative frozen
analyzer. Historical campaign binding, operating-system process inspection,
live-repository queries, and local path assumptions are intentionally outside
this public scorer.
"""
from __future__ import annotations

import copy
import datetime as dt
import hashlib
import json
import re

from sitc_plan import PREREG, PREREG_SHA256, read_json, sha256


FROZEN_DECISION_SHA256 = "5c17ff2b6800b0e940b1309283d53dc874c85242cc6591116665c157f1234527"
STATE_SCHEMA = "second-tier-sitc-state/1"
CONTENTS = (-8, -4, 4, 8)
GOALS = (-1, 1)
PRESENTATIONS = ("NORMAL", "REVERSED")
PROBES = 256
CASE_COUNT = 88


class IntegrityError(ValueError):
    """Evidence cannot be given a scientific PASS or FAIL."""


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("ascii")


def _digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise IntegrityError(code)


def _fields(value: object, expected: set[str], code: str) -> dict:
    _require(type(value) is dict and set(value) == expected, code)
    return value


def _integer(value: object, code: str, *, minimum: int | None = None) -> int:
    _require(type(value) is int, code + ":TYPE")
    if minimum is not None:
        _require(value >= minimum, code + ":DOMAIN")
    return value


def _string(value: object, code: str) -> str:
    _require(type(value) is str and bool(value) and "\x00" not in value, code)
    return value


def _hash(value: object, code: str) -> str:
    _require(type(value) is str and re.fullmatch(r"[0-9a-f]{64}", value) is not None, code)
    return value


def _timestamp(value: object, code: str) -> dt.datetime:
    _require(type(value) is str, code + ":TYPE")
    try:
        parsed = dt.datetime.fromisoformat(value)
    except ValueError as exc:
        raise IntegrityError(code + ":FORMAT") from exc
    _require(parsed.tzinfo is not None and parsed.utcoffset() is not None, code + ":NAIVE")
    return parsed.astimezone(dt.timezone.utc)


def _frozen_preregistration() -> dict:
    _require(sha256(PREREG) == PREREG_SHA256, "PREREGISTRATION_BYTES_CHANGED")
    value = read_json(PREREG)
    _require(type(value) is dict and value.get("version") == "1.0.0", "PREREGISTRATION_SCHEMA")
    return value


def frozen_decision_rules() -> dict:
    """Return the byte-bound frozen decision rules for semantic auditing."""
    decision = _frozen_preregistration()["decision"]
    _require(_digest(_canonical(decision)) == FROZEN_DECISION_SHA256, "FROZEN_DECISION_CHANGED")
    return copy.deepcopy(decision)


def _event_bytes(event: dict) -> bytes:
    return _canonical({"schema": "sitc-event-memory/1", **event})


def _history_bytes(history: dict) -> bytes:
    return _canonical({"schema": "sitc-self-history/1", **history})


def _validate_event(event: object, code: str) -> dict:
    event = _fields(event, {"content", "event_key"}, code + ":FIELDS")
    _string(event["event_key"], code + ":KEY")
    _require(_integer(event["content"], code + ":CONTENT") in CONTENTS, code + ":CONTENT_DOMAIN")
    return event


def _validate_history(history: object, code: str) -> dict:
    history = _fields(history, {"content", "event_key", "relation"}, code + ":FIELDS")
    _string(history["event_key"], code + ":KEY")
    _require(_integer(history["content"], code + ":CONTENT") in CONTENTS, code + ":CONTENT_DOMAIN")
    _require(history["relation"] in ("SELF", "OTHER", "UNBOUND"), code + ":RELATION")
    return history


def _state_payload(event: dict, history: dict, p: int, tick: int) -> bytes:
    return _canonical({
        "controlled_entity_slot": "SELF",
        "event_memory": event,
        "present_state": {"p": p, "tick": tick},
        "schema_version": STATE_SCHEMA,
        "self_history": history,
    })


def _validate_state_record(record: object, code: str) -> dict:
    record = _fields(record, {
        "bytes_hex", "sha256", "p", "tick", "event_memory",
        "event_memory_sha256", "self_history", "self_history_sha256",
        "controlled_entity_slot",
    }, code + ":FIELDS")
    _require(type(record["bytes_hex"]) is str and re.fullmatch(r"(?:[0-9a-f]{2})+", record["bytes_hex"]) is not None,
             code + ":HEX")
    payload = bytes.fromhex(record["bytes_hex"])
    _require(_digest(payload) == _hash(record["sha256"], code + ":HASH"), code + ":HASH_MISMATCH")
    try:
        decoded = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise IntegrityError(code + ":STATE_JSON") from exc
    decoded = _fields(decoded, {
        "controlled_entity_slot", "event_memory", "present_state",
        "schema_version", "self_history",
    }, code + ":STATE_FIELDS")
    _require(_canonical(decoded) == payload, code + ":NONCANONICAL")
    event = _validate_event(decoded["event_memory"], code + ":EVENT")
    history = _validate_history(decoded["self_history"], code + ":HISTORY")
    present = _fields(decoded["present_state"], {"p", "tick"}, code + ":PRESENT_FIELDS")
    p = _integer(present["p"], code + ":P")
    tick = _integer(present["tick"], code + ":TICK", minimum=0)
    _require(decoded["schema_version"] == STATE_SCHEMA, code + ":STATE_SCHEMA")
    _require(decoded["controlled_entity_slot"] == "SELF", code + ":LOCAL_SLOT")
    _require(record["controlled_entity_slot"] == "SELF", code + ":RECORDED_SLOT")
    _require(record["event_memory"] == event and record["self_history"] == history,
             code + ":DECODED_RECORD_DISAGREEMENT")
    _require(record["p"] == p and record["tick"] == tick, code + ":PRESENT_RECORD_DISAGREEMENT")
    _require(_digest(_event_bytes(event)) == _hash(record["event_memory_sha256"], code + ":EVENT_HASH"),
             code + ":EVENT_HASH_MISMATCH")
    _require(_digest(_history_bytes(history)) == _hash(record["self_history_sha256"], code + ":HISTORY_HASH"),
             code + ":HISTORY_HASH_MISMATCH")
    return {"bytes": payload, "sha256": record["sha256"], "event": event,
            "history": history, "p": p, "tick": tick}


def _ownership(record: object, controlled: str, other: str, represented: str, code: str) -> None:
    record = _fields(record, {
        "attributed_owner_token", "controlled_entity_token", "relation_observed",
    }, code + ":FIELDS")
    expected_attributed = controlled if represented == "SELF" else other
    _require(record["attributed_owner_token"] == expected_attributed, code + ":ATTRIBUTED")
    _require(record["controlled_entity_token"] == controlled, code + ":CONTROLLED")
    _require(record["relation_observed"] == represented, code + ":RELATION")


def _science(condition: bool, failures: set[str], code: str) -> None:
    if not condition:
        failures.add(code)


def _expected_options(content: int, goal: int, presentation: str) -> list[dict]:
    values = [
        {"option_id": "COMPENSATE", "delta": goal - content},
        {"option_id": "BASELINE", "delta": goal},
    ]
    return values if presentation == "NORMAL" else list(reversed(values))


def _symmetric_options(magnitude: int, presentation: str) -> list[dict]:
    values = [
        {"option_id": "NEGATIVE_STEP", "delta": -magnitude},
        {"option_id": "POSITIVE_STEP", "delta": magnitude},
    ]
    return values if presentation == "NORMAL" else list(reversed(values))


def _validate_trace(trace: object, *, goal: int, options: list[dict], coupling: bool,
                    failures: set[str], code: str) -> dict:
    trace = _fields(trace, {
        "coupling", "goal", "options", "state", "probes", "state_sha256_after_probes",
    }, code + ":FIELDS")
    _require(type(trace["coupling"]) is bool and trace["coupling"] is coupling, code + ":COUPLING")
    _require(type(trace["goal"]) is int and trace["goal"] == goal, code + ":GOAL")
    _require(trace["options"] == options, code + ":OPTIONS")
    state = _validate_state_record(trace["state"], code + ":STATE")
    _require(trace["state_sha256_after_probes"] == state["sha256"], code + ":PROBE_MUTATED_STATE")
    probes = trace["probes"]
    _require(type(probes) is list and len(probes) == PROBES, code + ":PROBE_COUNT")
    for index, probe in enumerate(probes):
        here = f"{code}:P{index:03d}"
        probe = _fields(probe, {
            "state_sha256", "p", "tick", "evaluations", "selector_input",
            "evaluator_input_keys", "selector_input_keys", "choice",
        }, here + ":FIELDS")
        _require(probe["state_sha256"] == state["sha256"], here + ":STATE_HASH")
        _require(type(probe["p"]) is int and probe["p"] == state["p"], here + ":P")
        _require(type(probe["tick"]) is int and probe["tick"] == state["tick"], here + ":TICK")
        _require(probe["evaluator_input_keys"] == ["p", "goal", "option_id_and_delta"],
                 here + ":EVALUATOR_INTERFACE")
        _require(probe["selector_input_keys"] == ["option_id", "q"], here + ":SELECTOR_INTERFACE")
        evaluations = probe["evaluations"]
        _require(type(evaluations) is list and len(evaluations) == len(options), here + ":EVALUATION_COUNT")
        effective_p = state["p"] if coupling else 0
        actual_scores = []
        for position, (observed, option) in enumerate(zip(evaluations, options)):
            point = f"{here}:O{position}"
            observed = _fields(observed, {"option_id", "delta", "future", "q"}, point + ":FIELDS")
            _require(observed["option_id"] == option["option_id"], point + ":OPTION_ID")
            _require(type(observed["delta"]) is int and observed["delta"] == option["delta"], point + ":DELTA")
            future = _integer(observed["future"], point + ":FUTURE")
            q = _integer(observed["q"], point + ":Q")
            expected_future = effective_p + option["delta"]
            expected_q = -((expected_future - goal) ** 2)
            _science(future == expected_future, failures, point + ":F_EQUATION")
            _science(q == expected_q, failures, point + ":Q_EQUATION")
            actual_scores.append({"option_id": observed["option_id"], "q": q})
        selector = probe["selector_input"]
        _require(type(selector) is list and len(selector) == len(options), here + ":SELECTOR_COUNT")
        for item in selector:
            _fields(item, {"option_id", "q"}, here + ":SELECTOR_FIELDS")
            _string(item["option_id"], here + ":SELECTOR_ID")
            _integer(item["q"], here + ":SELECTOR_Q")
        _require(selector == actual_scores, here + ":EVALUATOR_SELECTOR_DISCONTINUITY")
        ordered = sorted(actual_scores, key=lambda item: item["q"], reverse=True)
        _require(len(ordered) >= 2 and ordered[0]["q"] != ordered[1]["q"], here + ":TIE")
        winner = ordered[0]
        margin = winner["q"] - ordered[1]["q"]
        chosen_delta = next(item["delta"] for item in options if item["option_id"] == winner["option_id"])
        choice = _fields(probe["choice"], {"option_id", "q", "winning_margin", "chosen_delta"},
                         here + ":CHOICE_FIELDS")
        _string(choice["option_id"], here + ":CHOICE_ID")
        for field in ("q", "winning_margin", "chosen_delta"):
            _integer(choice[field], here + ":CHOICE_" + field.upper())
        _science(choice["option_id"] == winner["option_id"], failures, here + ":SELECTOR_WINNER")
        _science(choice["q"] == winner["q"], failures, here + ":SELECTOR_Q")
        _science(choice["winning_margin"] == margin, failures, here + ":SELECTOR_MARGIN")
        _science(choice["chosen_delta"] == chosen_delta, failures, here + ":SEMANTIC_DELTA")
    return {"state": state, "probes": probes, "trace": trace}


def _choice(trace_result: dict) -> dict:
    return trace_result["probes"][0]["choice"]


def _probe_science_projection(trace_result: dict) -> list[dict]:
    result = []
    for probe in trace_result["probes"]:
        result.append({
            "p": probe["p"], "tick": probe["tick"],
            "evaluations": sorted(probe["evaluations"], key=lambda item: item["option_id"]),
            "selector_input": sorted(probe["selector_input"], key=lambda item: item["option_id"]),
            "choice": probe["choice"],
        })
    return result


def _intervention(record: object, kind: str, code: str) -> dict:
    record = _fields(record, {"after_sha256", "before_sha256", "effective", "intervention_type"},
                     code + ":FIELDS")
    _hash(record["before_sha256"], code + ":BEFORE")
    _hash(record["after_sha256"], code + ":AFTER")
    _require(type(record["effective"]) is bool, code + ":EFFECTIVE_TYPE")
    _require(record["intervention_type"] == kind, code + ":KIND")
    return record


def _state_semantics(state: dict, *, event_key: str, event_content: int,
                     history_key: str, history_content: int, relation: str,
                     p: int, tick: int, failures: set[str], code: str) -> None:
    _science(state["event"] == {"content": event_content, "event_key": event_key}, failures, code + ":EVENT")
    _science(state["history"] == {"content": history_content, "event_key": history_key,
                                  "relation": relation}, failures, code + ":HISTORY")
    _science(state["p"] == p, failures, code + ":P")
    _science(state["tick"] == tick, failures, code + ":TICK")


def _target_case_fields(case: object, family: str, code: str,
                        extra: set[str] | None = None) -> tuple[dict, int, int, str, str]:
    expected = {"family", "case_id", "content", "goal", "presentation", "arms"}
    if extra:
        expected |= extra
    case = _fields(case, expected, code + ":FIELDS")
    _require(case["family"] == family, code + ":FAMILY")
    content = _integer(case["content"], code + ":CONTENT")
    goal = _integer(case["goal"], code + ":GOAL")
    presentation = case["presentation"]
    _require(content in CONTENTS and goal in GOALS and presentation in PRESENTATIONS, code + ":PARAMETERS")
    case_id = f"{family}_E{content:+d}_G{goal:+d}_{presentation}"
    _require(case["case_id"] == case_id, code + ":CASE_ID")
    return case, content, goal, presentation, case_id


def _validate_s1(case: object, controlled: str, other: str, failures: set[str]) -> None:
    case, content, goal, presentation, case_id = _target_case_fields(case, "S1", "S1")
    _require(set(case["arms"]) == {"SELF", "OTHER"}, case_id + ":ARMS")
    options = _expected_options(content, goal, presentation)
    traces = {}
    for relation, expected_p, expected_choice in (("SELF", content, "COMPENSATE"), ("OTHER", 0, "BASELINE")):
        arm = _fields(case["arms"][relation], {"ownership_input", "trace"}, case_id + ":" + relation + ":FIELDS")
        _ownership(arm["ownership_input"], controlled, other, relation, case_id + ":" + relation + ":OWNER")
        result = _validate_trace(arm["trace"], goal=goal, options=options, coupling=True,
                                 failures=failures, code=case_id + ":" + relation)
        _state_semantics(result["state"], event_key=case_id + "_EVENT", event_content=content,
                         history_key=case_id + "_EVENT", history_content=content,
                         relation=relation, p=expected_p, tick=256, failures=failures,
                         code=case_id + ":" + relation)
        _science(_choice(result)["option_id"] == expected_choice, failures,
                 case_id + ":" + relation + ":CHOICE")
        _science(_choice(result)["winning_margin"] >= 16, failures,
                 case_id + ":" + relation + ":MARGIN")
        traces[relation] = result
    _require(traces["SELF"]["state"]["event"]["content"] == traces["OTHER"]["state"]["event"]["content"]
             and _event_bytes(traces["SELF"]["state"]["event"]) == _event_bytes(traces["OTHER"]["state"]["event"]),
             case_id + ":CONTENT_CONTROL_CONFOUNDED")


def _validate_s2(case: object, controlled: str, other: str, failures: set[str]) -> None:
    case = _fields(case, {"family", "case_id", "magnitude", "goal", "presentation",
                          "ownership_inputs", "arms"}, "S2:FIELDS")
    magnitude = _integer(case["magnitude"], "S2:MAGNITUDE")
    presentation = case["presentation"]
    _require(case["family"] == "S2" and magnitude in (4, 8) and case["goal"] == 0
             and presentation in PRESENTATIONS, "S2:PARAMETERS")
    case_id = f"S2_M{magnitude}_{presentation}"
    _require(case["case_id"] == case_id, "S2:CASE_ID")
    owners = _fields(case["ownership_inputs"], {"LEFT", "RIGHT"}, case_id + ":OWNERS")
    _ownership(owners["LEFT"], controlled, other, "SELF", case_id + ":LEFT_OWNER")
    _ownership(owners["RIGHT"], controlled, other, "SELF", case_id + ":RIGHT_OWNER")
    arm_names = {"LEFT_BEFORE", "RIGHT_BEFORE", "LEFT_AFTER_SWAP", "RIGHT_AFTER_SWAP"}
    _require(set(case["arms"]) == arm_names, case_id + ":ARMS")
    options = _symmetric_options(magnitude, presentation)
    results = {}
    for name in arm_names:
        expected_fields = {"trace"} if name.endswith("BEFORE") else {
            "donor_history_sha256", "recipient_event_before_sha256",
            "recipient_event_after_sha256", "intervention", "trace",
        }
        arm = _fields(case["arms"][name], expected_fields, case_id + ":" + name + ":FIELDS")
        results[name] = _validate_trace(arm["trace"], goal=0, options=options, coupling=True,
                                        failures=failures, code=case_id + ":" + name)
    expected = {
        "LEFT_BEFORE": ("LEFT", magnitude, "LEFT", magnitude, "NEGATIVE_STEP"),
        "RIGHT_BEFORE": ("RIGHT", -magnitude, "RIGHT", -magnitude, "POSITIVE_STEP"),
        "LEFT_AFTER_SWAP": ("LEFT", magnitude, "RIGHT", -magnitude, "POSITIVE_STEP"),
        "RIGHT_AFTER_SWAP": ("RIGHT", -magnitude, "LEFT", magnitude, "NEGATIVE_STEP"),
    }
    for name, (event_side, event_content, hist_side, hist_content, choice) in expected.items():
        _state_semantics(results[name]["state"], event_key=case_id + "_" + event_side,
                         event_content=event_content, history_key=case_id + "_" + hist_side,
                         history_content=hist_content, relation="SELF", p=hist_content, tick=256,
                         failures=failures, code=case_id + ":" + name)
        _science(_choice(results[name])["option_id"] == choice, failures, case_id + ":" + name + ":CHOICE")
    for recipient, donor in (("LEFT", "RIGHT"), ("RIGHT", "LEFT")):
        before = results[recipient + "_BEFORE"]["state"]
        after = results[recipient + "_AFTER_SWAP"]["state"]
        donor_state = results[donor + "_BEFORE"]["state"]
        arm = case["arms"][recipient + "_AFTER_SWAP"]
        receipt = _intervention(arm["intervention"], "SELF_HISTORY_SWAP", case_id + ":" + recipient + ":RECEIPT")
        _require(arm["recipient_event_before_sha256"] == _digest(_event_bytes(before["event"])),
                 case_id + ":" + recipient + ":EVENT_BEFORE_HASH")
        _require(arm["recipient_event_after_sha256"] == _digest(_event_bytes(after["event"])),
                 case_id + ":" + recipient + ":EVENT_AFTER_HASH")
        _require(arm["recipient_event_before_sha256"] == arm["recipient_event_after_sha256"],
                 case_id + ":" + recipient + ":RECIPIENT_EVENT_CHANGED")
        _require(arm["donor_history_sha256"] == _digest(_history_bytes(donor_state["history"])),
                 case_id + ":" + recipient + ":DONOR_HASH")
        _require(receipt["before_sha256"] == before["sha256"] and receipt["after_sha256"] == after["sha256"]
                 and receipt["effective"] is True, case_id + ":" + recipient + ":RECEIPT_BINDING")
        _science(_probe_science_projection(results[recipient + "_AFTER_SWAP"])
                 == _probe_science_projection(results[donor + "_BEFORE"]), failures,
                 case_id + ":" + recipient + ":DONOR_FOLLOWING")


def _validate_s3(case: object, controlled: str, other: str, failures: set[str]) -> None:
    case, content, goal, presentation, case_id = _target_case_fields(
        case, "S3", "S3", {"ownership_input"},
    )
    _ownership(case["ownership_input"], controlled, other, "SELF", case_id + ":OWNER")
    _require(set(case["arms"]) == {"SELF", "ATTRIBUTION_ABLATED", "P_RESTORED_BY_CLAMP"}, case_id + ":ARMS")
    options = _expected_options(content, goal, presentation)
    results = {}
    for name in case["arms"]:
        fields = {"trace"} if name == "SELF" else {"intervention", "trace"}
        arm = _fields(case["arms"][name], fields, case_id + ":" + name + ":FIELDS")
        results[name] = _validate_trace(arm["trace"], goal=goal, options=options, coupling=True,
                                        failures=failures, code=case_id + ":" + name)
    expected = {
        "SELF": ("SELF", content, "COMPENSATE"),
        "ATTRIBUTION_ABLATED": ("UNBOUND", 0, "BASELINE"),
        "P_RESTORED_BY_CLAMP": ("UNBOUND", content, "COMPENSATE"),
    }
    for name, (relation, p, choice) in expected.items():
        _state_semantics(results[name]["state"], event_key=case_id + "_EVENT", event_content=content,
                         history_key=case_id + "_EVENT", history_content=content, relation=relation,
                         p=p, tick=256, failures=failures, code=case_id + ":" + name)
        _science(_choice(results[name])["option_id"] == choice, failures, case_id + ":" + name + ":CHOICE")
    for name, kind, before_name in (
        ("ATTRIBUTION_ABLATED", "ATTRIBUTION_ABLATION", "SELF"),
        ("P_RESTORED_BY_CLAMP", "P_CLAMP_AFTER_ATTRIBUTION_ABLATION", "ATTRIBUTION_ABLATED"),
    ):
        receipt = _intervention(case["arms"][name]["intervention"], kind, case_id + ":" + name + ":RECEIPT")
        _require(receipt["before_sha256"] == results[before_name]["state"]["sha256"]
                 and receipt["after_sha256"] == results[name]["state"]["sha256"]
                 and receipt["effective"] is True, case_id + ":" + name + ":RECEIPT_BINDING")
    event_bytes = {result["state"]["event"]["event_key"]: _event_bytes(result["state"]["event"])
                   for result in results.values()}
    _require(len(set(event_bytes.values())) == 1, case_id + ":EVENT_MEMORY_CHANGED")


def _validate_s4(case: object, controlled: str, other: str, failures: set[str]) -> None:
    case = _fields(case, {"family", "case_id", "content", "goal", "presentation", "ownership_input",
                          "state_hash_before_both_arms", "arms", "specificity", "state_hash_after_all_arms"},
                   "S4:FIELDS")
    content = _integer(case["content"], "S4:CONTENT")
    goal = _integer(case["goal"], "S4:GOAL")
    presentation = case["presentation"]
    _require(case["family"] == "S4" and content in CONTENTS and goal in GOALS
             and presentation in PRESENTATIONS, "S4:PARAMETERS")
    case_id = f"S4_E{content:+d}_G{goal:+d}_{presentation}"
    _require(case["case_id"] == case_id, "S4:CASE_ID")
    _ownership(case["ownership_input"], controlled, other, "SELF", case_id + ":OWNER")
    _require(set(case["arms"]) == {"COUPLED", "P_TO_FQ_ABLATED"}, case_id + ":ARMS")
    options = _expected_options(content, goal, presentation)
    results = {}
    for name, coupling, choice in (("COUPLED", True, "COMPENSATE"),
                                    ("P_TO_FQ_ABLATED", False, "BASELINE")):
        arm = _fields(case["arms"][name], {"trace"}, case_id + ":" + name + ":FIELDS")
        result = _validate_trace(arm["trace"], goal=goal, options=options, coupling=coupling,
                                 failures=failures, code=case_id + ":" + name)
        _state_semantics(result["state"], event_key=case_id + "_EVENT", event_content=content,
                         history_key=case_id + "_EVENT", history_content=content, relation="SELF",
                         p=content, tick=256, failures=failures, code=case_id + ":" + name)
        _science(_choice(result)["option_id"] == choice, failures, case_id + ":" + name + ":CHOICE")
        results[name] = result
    common_hash = results["COUPLED"]["state"]["sha256"]
    _require(results["P_TO_FQ_ABLATED"]["state"]["sha256"] == common_hash
             and case["state_hash_before_both_arms"] == common_hash
             and case["state_hash_after_all_arms"] == common_hash, case_id + ":ABLATION_CHANGED_STATE")
    panels = case["specificity"]
    _require(type(panels) is list and len(panels) == 2, case_id + ":SPECIFICITY_COUNT")
    registered = ((-1, (-1, 4), -1), (1, (-4, 1), 1))
    for index, (panel, (panel_goal, deltas, winner)) in enumerate(zip(panels, registered)):
        panel = _fields(panel, {"panel_index", "registered_winner_delta", "trace"},
                        case_id + f":SPEC{index}:FIELDS")
        _require(panel["panel_index"] == index and panel["registered_winner_delta"] == winner,
                 case_id + f":SPEC{index}:IDENTITY")
        opts = [{"option_id": "PANEL_LEFT", "delta": deltas[0]},
                {"option_id": "PANEL_RIGHT", "delta": deltas[1]}]
        if presentation == "REVERSED":
            opts.reverse()
        result = _validate_trace(panel["trace"], goal=panel_goal, options=opts, coupling=False,
                                 failures=failures, code=case_id + f":SPEC{index}")
        _require(result["state"]["sha256"] == common_hash, case_id + f":SPEC{index}:STATE_CHANGED")
        _science(_choice(result)["chosen_delta"] == winner, failures, case_id + f":SPEC{index}:WINNER")


def _validate_s5(case: object, controlled: str, other: str, failures: set[str]) -> None:
    case = _fields(case, {"family", "case_id", "content", "goal", "presentation", "ownership_input",
                          "checkpoint", "divergence", "arms"}, "S5:FIELDS")
    content = _integer(case["content"], "S5:CONTENT")
    goal = _integer(case["goal"], "S5:GOAL")
    presentation = case["presentation"]
    _require(case["family"] == "S5" and content in CONTENTS and goal in GOALS
             and presentation in PRESENTATIONS, "S5:PARAMETERS")
    case_id = f"S5_E{content:+d}_G{goal:+d}_{presentation}"
    _require(case["case_id"] == case_id, "S5:CASE_ID")
    _ownership(case["ownership_input"], controlled, other, "SELF", case_id + ":OWNER")
    checkpoint = _fields(case["checkpoint"], {"digest", "payload_hex", "state"}, case_id + ":CHECKPOINT_FIELDS")
    cp_state = _validate_state_record(checkpoint["state"], case_id + ":CHECKPOINT_STATE")
    _require(checkpoint["payload_hex"] == cp_state["bytes"].hex()
             and checkpoint["digest"] == cp_state["sha256"], case_id + ":CHECKPOINT_BINDING")
    _state_semantics(cp_state, event_key=case_id + "_EVENT", event_content=content,
                     history_key=case_id + "_EVENT", history_content=content, relation="SELF",
                     p=content, tick=256, failures=failures, code=case_id + ":CHECKPOINT")
    divergence = _fields(case["divergence"], {"registered_steps", "intervention", "state_after_dirty_steps"},
                         case_id + ":DIVERGENCE_FIELDS")
    _require(divergence["registered_steps"] == 17, case_id + ":DIVERGENT_STEPS")
    dirty = _validate_state_record(divergence["state_after_dirty_steps"], case_id + ":DIRTY_STATE")
    _state_semantics(dirty, event_key=case_id + "_EVENT", event_content=content,
                     history_key=case_id + "_EVENT", history_content=-content, relation="SELF",
                     p=-content, tick=273, failures=failures, code=case_id + ":DIRTY")
    divergence_receipt = _intervention(divergence["intervention"], "DIVERGENT_HISTORY_SUBSTITUTION",
                                       case_id + ":DIVERGENCE_RECEIPT")
    actual_dirty_start = _state_payload(dirty["event"], dirty["history"], dirty["p"], 256)
    _require(divergence_receipt["before_sha256"] == cp_state["sha256"]
             and divergence_receipt["after_sha256"] == _digest(actual_dirty_start)
             and divergence_receipt["effective"] is True, case_id + ":DIVERGENCE_RECEIPT_BINDING")
    _require(set(case["arms"]) == {"DIRECT", "FULL_RESTORE", "SHAM_RESTORE", "CONTENT_ONLY_RESTORE"},
             case_id + ":ARMS")
    options = _expected_options(content, goal, presentation)
    results = {}
    for name in case["arms"]:
        fields = {"restored_checkpoint_state", "trace"} if name == "FULL_RESTORE" else {"trace"}
        arm = _fields(case["arms"][name], fields, case_id + ":" + name + ":FIELDS")
        if name == "FULL_RESTORE":
            restored = _validate_state_record(arm["restored_checkpoint_state"], case_id + ":RESTORED_CHECKPOINT")
            _science(restored["bytes"] == cp_state["bytes"], failures, case_id + ":FULL_RESTORE_BYTES")
        result = _validate_trace(arm["trace"], goal=goal, options=options, coupling=True,
                                 failures=failures, code=case_id + ":" + name)
        results[name] = result
        if name in ("DIRECT", "FULL_RESTORE"):
            expected_history, expected_p, expected_tick, expected_choice = content, content, 512, "COMPENSATE"
        else:
            expected_history, expected_p, expected_tick, expected_choice = -content, -content, 529, "BASELINE"
        _state_semantics(result["state"], event_key=case_id + "_EVENT", event_content=content,
                         history_key=case_id + "_EVENT", history_content=expected_history,
                         relation="SELF", p=expected_p, tick=expected_tick, failures=failures,
                         code=case_id + ":" + name)
        _science(_choice(result)["option_id"] == expected_choice, failures,
                 case_id + ":" + name + ":CHOICE")
    _science(results["DIRECT"]["trace"] == results["FULL_RESTORE"]["trace"], failures,
             case_id + ":DIRECT_FULL_PROJECTION")
    _science(results["SHAM_RESTORE"]["trace"] == results["CONTENT_ONLY_RESTORE"]["trace"], failures,
             case_id + ":NEGATIVE_CONTROLS")


def _validate_s6(case: object, controlled: str, other: str, failures: set[str]) -> None:
    case, content, goal, presentation, case_id = _target_case_fields(case, "S6", "S6")
    expected_arms = {f"ORIGIN_{origin}_ATTR_{relation}" for origin in ("SELF", "OTHER")
                     for relation in ("SELF", "OTHER")}
    _require(set(case["arms"]) == expected_arms, case_id + ":ARMS")
    options = _expected_options(content, goal, presentation)
    results = {}
    for origin in ("SELF", "OTHER"):
        for relation, expected_p, expected_choice in (("SELF", content, "COMPENSATE"),
                                                      ("OTHER", 0, "BASELINE")):
            name = f"ORIGIN_{origin}_ATTR_{relation}"
            arm = _fields(case["arms"][name], {"harness_only_true_origin", "true_origin_supplied_to_core",
                                                "ownership_input", "trace"}, case_id + ":" + name + ":FIELDS")
            _require(arm["harness_only_true_origin"] == origin
                     and arm["true_origin_supplied_to_core"] is False, case_id + ":" + name + ":ORIGIN_BOUNDARY")
            _ownership(arm["ownership_input"], controlled, other, relation, case_id + ":" + name + ":OWNER")
            result = _validate_trace(arm["trace"], goal=goal, options=options, coupling=True,
                                     failures=failures, code=case_id + ":" + name)
            _state_semantics(result["state"], event_key=case_id + "_EVENT", event_content=content,
                             history_key=case_id + "_EVENT", history_content=content,
                             relation=relation, p=expected_p, tick=256, failures=failures,
                             code=case_id + ":" + name)
            _science(_choice(result)["option_id"] == expected_choice, failures,
                     case_id + ":" + name + ":CHOICE")
            results[(origin, relation)] = result
    for relation in ("SELF", "OTHER"):
        _science(results[("SELF", relation)]["trace"] == results[("OTHER", relation)]["trace"], failures,
                 case_id + ":ORIGIN_INVARIANCE:" + relation)


def _validate_p_clamp(case: object, controlled: str, other: str, failures: set[str]) -> None:
    case = _fields(case, {"family", "case_id", "goal", "presentation", "ownership_inputs", "arms"},
                   "P_CLAMP:FIELDS")
    presentation = case["presentation"]
    _require(case["family"] == "P_CLAMP" and case["goal"] == 0 and presentation in PRESENTATIONS,
             "P_CLAMP:PARAMETERS")
    case_id = "P_CLAMP_" + presentation
    _require(case["case_id"] == case_id, "P_CLAMP:CASE_ID")
    owners = case["ownership_inputs"]
    _require(type(owners) is list and len(owners) == 2, case_id + ":OWNER_COUNT")
    for index, owner in enumerate(owners):
        _ownership(owner, controlled, other, "SELF", case_id + f":OWNER{index}")
    _require(set(case["arms"]) == {"FROM_POSITIVE", "FROM_NEGATIVE"}, case_id + ":ARMS")
    options = _symmetric_options(4, presentation)
    results = {}
    for name, content, suffix in (("FROM_POSITIVE", 4, "POS"), ("FROM_NEGATIVE", -4, "NEG")):
        arm = _fields(case["arms"][name], {"trace"}, case_id + ":" + name + ":FIELDS")
        result = _validate_trace(arm["trace"], goal=0, options=options, coupling=True,
                                 failures=failures, code=case_id + ":" + name)
        _state_semantics(result["state"], event_key=case_id + "_" + suffix, event_content=content,
                         history_key=case_id + "_" + suffix, history_content=content, relation="SELF",
                         p=4, tick=256, failures=failures, code=case_id + ":" + name)
        _science(_choice(result)["option_id"] == "NEGATIVE_STEP", failures, case_id + ":" + name + ":CHOICE")
        results[name] = result
    _science(_probe_science_projection(results["FROM_POSITIVE"])
             == _probe_science_projection(results["FROM_NEGATIVE"]), failures,
             case_id + ":CLAMP_EQUALITY")


def _validate_q_clamp(case: object, controlled: str, other: str, failures: set[str]) -> None:
    case = _fields(case, {"family", "case_id", "presentation", "ownership_inputs", "arms"},
                   "Q_CLAMP:FIELDS")
    presentation = case["presentation"]
    _require(case["family"] == "Q_CLAMP" and presentation in PRESENTATIONS, "Q_CLAMP:PARAMETERS")
    case_id = "Q_CLAMP_" + presentation
    _require(case["case_id"] == case_id, "Q_CLAMP:CASE_ID")
    owners = case["ownership_inputs"]
    _require(type(owners) is list and len(owners) == 2, case_id + ":OWNER_COUNT")
    for index, owner in enumerate(owners):
        _ownership(owner, controlled, other, "SELF", case_id + f":OWNER{index}")
    _require(set(case["arms"]) == {"FROM_POSITIVE", "FROM_NEGATIVE"}, case_id + ":ARMS")
    expected_scores = [{"option_id": "LEFT", "q": 16}, {"option_id": "RIGHT", "q": 0}]
    if presentation == "REVERSED":
        expected_scores.reverse()
    for name, content, suffix in (("FROM_POSITIVE", 4, "POS"), ("FROM_NEGATIVE", -4, "NEG")):
        arm = _fields(case["arms"][name], {"upstream_state", "selector_input", "choice"},
                      case_id + ":" + name + ":FIELDS")
        state = _validate_state_record(arm["upstream_state"], case_id + ":" + name + ":STATE")
        _state_semantics(state, event_key=case_id + "_" + suffix, event_content=content,
                         history_key=case_id + "_" + suffix, history_content=content, relation="SELF",
                         p=content, tick=256, failures=failures, code=case_id + ":" + name)
        _require(arm["selector_input"] == expected_scores, case_id + ":" + name + ":Q_INTERVENTION")
        choice = _fields(arm["choice"], {"option_id", "q", "winning_margin"},
                         case_id + ":" + name + ":CHOICE_FIELDS")
        _science(choice == {"option_id": "LEFT", "q": 16, "winning_margin": 16}, failures,
                 case_id + ":" + name + ":CHOICE")


def expected_case_ids() -> list[str]:
    values = []
    for family in ("S1",):
        values.extend(f"{family}_E{c:+d}_G{g:+d}_{p}" for c in CONTENTS for g in GOALS for p in PRESENTATIONS)
    values.extend(f"S2_M{m}_{p}" for m in (4, 8) for p in PRESENTATIONS)
    for family in ("S3", "S4", "S5", "S6"):
        values.extend(f"{family}_E{c:+d}_G{g:+d}_{p}" for c in CONTENTS for g in GOALS for p in PRESENTATIONS)
    values.extend("P_CLAMP_" + p for p in PRESENTATIONS)
    values.extend("Q_CLAMP_" + p for p in PRESENTATIONS)
    _require(len(values) == CASE_COUNT and len(set(values)) == CASE_COUNT, "ANALYZER_CASE_REGISTRY")
    return values


def _replace_tokens(value: object, controlled: str, other: str) -> object:
    if type(value) is str:
        if value == controlled:
            return "<CONTROLLED_TOKEN>"
        if value == other:
            return "<OTHER_TOKEN>"
        return value
    if type(value) is list:
        return [_replace_tokens(item, controlled, other) for item in value]
    if type(value) is dict:
        return {key: _replace_tokens(item, controlled, other) for key, item in value.items()}
    return value


def score_raw_run(raw: object, expected_run: dict) -> dict:
    """Strictly validate and score one already-released raw scientific run."""
    raw = _fields(raw, {"schema", "preregistration_sha256", "registered_run_id", "ordering",
                        "token_bijection", "case_count", "case_order", "cases"}, "RAW:FIELDS")
    _require(raw["schema"] == "second-tier-sitc-raw-scientific-run/1", "RAW:SCHEMA")
    _require(raw["preregistration_sha256"] == PREREG_SHA256, "RAW:PREREGISTRATION")
    _require(raw["registered_run_id"] == expected_run["registered_run_id"]
             and raw["ordering"] == expected_run["ordering"], "RAW:RUN_MAPPING")
    tokens = _fields(raw["token_bijection"], {"controlled", "other"}, "RAW:TOKENS")
    controlled, other = tokens["controlled"], tokens["other"]
    _require(controlled == expected_run["controlled_token"] and other == expected_run["other_token"]
             and controlled != other, "RAW:TOKEN_BIJECTION")
    _require(raw["case_count"] == CASE_COUNT and type(raw["cases"]) is list
             and len(raw["cases"]) == CASE_COUNT, "RAW:CASE_COUNT")
    forward = expected_case_ids()
    expected_order = forward if expected_run["ordering"] == "FORWARD" else list(reversed(forward))
    _require(raw["case_order"] == expected_order, "RAW:CASE_ORDER")
    _require([case.get("case_id") if type(case) is dict else None for case in raw["cases"]] == expected_order,
             "RAW:CASE_PAYLOAD_ORDER")
    failures: set[str] = set()
    validators = {
        "S1": _validate_s1, "S2": _validate_s2, "S3": _validate_s3,
        "S4": _validate_s4, "S5": _validate_s5, "S6": _validate_s6,
        "P_CLAMP": _validate_p_clamp, "Q_CLAMP": _validate_q_clamp,
    }
    for case in raw["cases"]:
        family = case.get("family") if type(case) is dict else None
        _require(family in validators, "RAW:UNKNOWN_FAMILY")
        validators[family](case, controlled, other, failures)
    normalized_cases = _replace_tokens(sorted(raw["cases"], key=lambda case: case["case_id"]), controlled, other)
    projection = {
        "schema": raw["schema"],
        "preregistration_sha256": PREREG_SHA256,
        "case_count": CASE_COUNT,
        "cases": normalized_cases,
    }
    projection_bytes = _canonical(projection)
    return {
        "registered_run_id": expected_run["registered_run_id"],
        "ordering": expected_run["ordering"],
        "status": "PASS" if not failures else "FAIL",
        "scientific_failures": sorted(failures),
        "normalized_projection_sha256": _digest(projection_bytes),
        "normalized_projection": projection,
    }


def terminal_decision(reports: list[dict]) -> str:
    """Apply the frozen cross-run decision rule to six scored reports."""
    _require(len(reports) == 6, "DECISION:RUN_COUNT")
    projections = [report["normalized_projection_sha256"] for report in reports]
    if len(set(projections)) != 1:
        return "SITC_INCONCLUSIVE"
    failures = [report["scientific_failures"] for report in reports]
    if any(value != failures[0] for value in failures[1:]):
        return "SITC_INCONCLUSIVE"
    return "SITC_PASS" if not failures[0] else "SITC_FAIL"

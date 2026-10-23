"""Registered SITC v1 case construction and raw observation collection.

This module records observations only.  It contains no verdict labels and does
not compare observations with the preregistered scientific predictions.
"""
from __future__ import annotations

from typing import Callable

from sitc_core import (
    EventMemory, Option, OptionScore, OwnershipInput, Relation, SITCState,
    ablate_attribution, acquire, capture_checkpoint, clamp_present_state,
    intervention_receipt, neutral_ticks, read_only_probe,
    read_only_probe_coupling_ablated, restore_checkpoint,
    restore_event_memory_only, select, semantic_delta, sham_restore,
    substitute_history_content, swap_self_histories,
)
from sitc_plan import PREREG_SHA256, digest, preregistration


NEUTRAL_STEPS = 256
PROBES = 256
DIVERGENT_STEPS = 17


def state_record(state: SITCState) -> dict:
    payload = state.to_bytes()
    return {
        "bytes_hex": payload.hex(),
        "sha256": digest(payload),
        "p": state.p,
        "tick": state.tick,
        "event_memory": state.event_memory.to_wire(),
        "event_memory_sha256": state.event_memory.sha256(),
        "self_history": state.self_history.to_wire(),
        "self_history_sha256": state.self_history.sha256(),
        "controlled_entity_slot": state.controlled_entity_slot,
    }


def probe_record(probe) -> dict:
    return {
        "state_sha256": probe.state_sha256,
        "p": probe.p,
        "tick": probe.tick,
        "evaluations": [
            {"option_id": x.option_id, "delta": x.delta, "future": x.future, "q": x.q}
            for x in probe.evaluations
        ],
        "selector_input": [
            {"option_id": x.option_id, "q": x.q} for x in probe.scores
        ],
        "evaluator_input_keys": ["p", "goal", "option_id_and_delta"],
        "selector_input_keys": ["option_id", "q"],
        "choice": {
            "option_id": probe.choice.option_id,
            "q": probe.choice.q,
            "winning_margin": probe.choice.winning_margin,
            "chosen_delta": probe.chosen_delta,
        },
    }


def trace(state: SITCState, goal: int, options: tuple[Option, ...], *,
          coupling: bool = True) -> dict:
    before = state.to_bytes()
    function: Callable = read_only_probe if coupling else read_only_probe_coupling_ablated
    probes = [probe_record(function(state, goal, options)) for _ in range(PROBES)]
    if state.to_bytes() != before:
        raise ValueError("TRACE_MUTATED_STATE")
    return {
        "coupling": coupling,
        "goal": goal,
        "options": [{"option_id": x.option_id, "delta": x.delta} for x in options],
        "state": state_record(state),
        "probes": probes,
        "state_sha256_after_probes": state.sha256(),
    }


def target_options(content: int, goal: int, presentation: str) -> tuple[Option, ...]:
    values = (
        Option("COMPENSATE", goal - content),
        Option("BASELINE", goal),
    )
    if presentation == "NORMAL":
        return values
    if presentation == "REVERSED":
        return tuple(reversed(values))
    raise ValueError("UNREGISTERED_PRESENTATION")


def symmetric_options(magnitude: int, presentation: str) -> tuple[Option, ...]:
    values = (Option("NEGATIVE_STEP", -magnitude), Option("POSITIVE_STEP", magnitude))
    if presentation == "NORMAL":
        return values
    if presentation == "REVERSED":
        return tuple(reversed(values))
    raise ValueError("UNREGISTERED_PRESENTATION")


def ownership_record(attributed: str, controlled: str) -> dict:
    return {
        "attributed_owner_token": attributed,
        "controlled_entity_token": controlled,
        "relation_observed": "SELF" if attributed == controlled else "OTHER",
    }


def fresh_state(event_key: str, content: int, represented: str,
                controlled_token: str, other_token: str) -> tuple[SITCState, dict]:
    if represented == "SELF":
        attributed = controlled_token
    elif represented == "OTHER":
        attributed = other_token
    else:
        raise ValueError("UNREGISTERED_REPRESENTED_OWNER")
    event = EventMemory(event_key, content)
    owner = OwnershipInput(attributed, controlled_token)
    state = acquire(event, owner)
    return neutral_ticks(state, NEUTRAL_STEPS), ownership_record(attributed, controlled_token)


def base_parameters():
    for content in (-8, -4, 4, 8):
        for goal in (-1, 1):
            for presentation in ("NORMAL", "REVERSED"):
                yield content, goal, presentation


def s1_case(content: int, goal: int, presentation: str,
            controlled: str, other: str) -> dict:
    case_id = f"S1_E{content:+d}_G{goal:+d}_{presentation}"
    event_key = case_id + "_EVENT"
    options = target_options(content, goal, presentation)
    arms = {}
    for represented in ("SELF", "OTHER"):
        state, owner = fresh_state(event_key, content, represented, controlled, other)
        arms[represented] = {"ownership_input": owner, "trace": trace(state, goal, options)}
    return {"family": "S1", "case_id": case_id, "content": content,
            "goal": goal, "presentation": presentation, "arms": arms}


def s2_case(magnitude: int, presentation: str,
            controlled: str, other: str) -> dict:
    case_id = f"S2_M{magnitude}_{presentation}"
    options = symmetric_options(magnitude, presentation)
    left, left_owner = fresh_state(case_id + "_LEFT", magnitude, "SELF", controlled, other)
    right, right_owner = fresh_state(case_id + "_RIGHT", -magnitude, "SELF", controlled, other)
    swapped_left, swapped_right = swap_self_histories(left, right)
    return {
        "family": "S2", "case_id": case_id, "magnitude": magnitude,
        "goal": 0, "presentation": presentation,
        "ownership_inputs": {"LEFT": left_owner, "RIGHT": right_owner},
        "arms": {
            "LEFT_BEFORE": {"trace": trace(left, 0, options)},
            "RIGHT_BEFORE": {"trace": trace(right, 0, options)},
            "LEFT_AFTER_SWAP": {
                "donor_history_sha256": right.self_history.sha256(),
                "recipient_event_before_sha256": left.event_memory.sha256(),
                "recipient_event_after_sha256": swapped_left.event_memory.sha256(),
                "intervention": intervention_receipt("SELF_HISTORY_SWAP", left, swapped_left),
                "trace": trace(swapped_left, 0, options),
            },
            "RIGHT_AFTER_SWAP": {
                "donor_history_sha256": left.self_history.sha256(),
                "recipient_event_before_sha256": right.event_memory.sha256(),
                "recipient_event_after_sha256": swapped_right.event_memory.sha256(),
                "intervention": intervention_receipt("SELF_HISTORY_SWAP", right, swapped_right),
                "trace": trace(swapped_right, 0, options),
            },
        },
    }


def s3_case(content: int, goal: int, presentation: str,
            controlled: str, other: str) -> dict:
    case_id = f"S3_E{content:+d}_G{goal:+d}_{presentation}"
    options = target_options(content, goal, presentation)
    state, owner = fresh_state(case_id + "_EVENT", content, "SELF", controlled, other)
    ablated = ablate_attribution(state)
    clamped = clamp_present_state(ablated, content)
    return {
        "family": "S3", "case_id": case_id, "content": content, "goal": goal,
        "presentation": presentation, "ownership_input": owner,
        "arms": {
            "SELF": {"trace": trace(state, goal, options)},
            "ATTRIBUTION_ABLATED": {
                "intervention": intervention_receipt("ATTRIBUTION_ABLATION", state, ablated),
                "trace": trace(ablated, goal, options),
            },
            "P_RESTORED_BY_CLAMP": {
                "intervention": intervention_receipt("P_CLAMP_AFTER_ATTRIBUTION_ABLATION", ablated, clamped),
                "trace": trace(clamped, goal, options),
            },
        },
    }


def s4_case(content: int, goal: int, presentation: str,
            controlled: str, other: str) -> dict:
    case_id = f"S4_E{content:+d}_G{goal:+d}_{presentation}"
    options = target_options(content, goal, presentation)
    state, owner = fresh_state(case_id + "_EVENT", content, "SELF", controlled, other)
    specific = []
    for index, panel in enumerate(preregistration()["contrasts"]["S4"]["specificity_panels"]):
        panel_options = (Option("PANEL_LEFT", panel["deltas"][0]), Option("PANEL_RIGHT", panel["deltas"][1]))
        if presentation == "REVERSED":
            panel_options = tuple(reversed(panel_options))
        specific.append({
            "panel_index": index,
            "registered_winner_delta": panel["winner_delta"],
            "trace": trace(state, panel["goal"], panel_options, coupling=False),
        })
    return {
        "family": "S4", "case_id": case_id, "content": content, "goal": goal,
        "presentation": presentation, "ownership_input": owner,
        "state_hash_before_both_arms": state.sha256(),
        "arms": {
            "COUPLED": {"trace": trace(state, goal, options, coupling=True)},
            "P_TO_FQ_ABLATED": {"trace": trace(state, goal, options, coupling=False)},
        },
        "specificity": specific,
        "state_hash_after_all_arms": state.sha256(),
    }


def s5_case(content: int, goal: int, presentation: str,
            controlled: str, other: str) -> dict:
    case_id = f"S5_E{content:+d}_G{goal:+d}_{presentation}"
    options = target_options(content, goal, presentation)
    checkpoint_state, owner = fresh_state(case_id + "_EVENT", content, "SELF", controlled, other)
    checkpoint = capture_checkpoint(checkpoint_state)
    direct = neutral_ticks(restore_checkpoint(checkpoint), NEUTRAL_STEPS)
    divergent_start = substitute_history_content(checkpoint_state, -content)
    divergent = neutral_ticks(divergent_start, DIVERGENT_STEPS)
    full = neutral_ticks(restore_checkpoint(checkpoint), NEUTRAL_STEPS)
    sham = neutral_ticks(sham_restore(divergent, checkpoint), NEUTRAL_STEPS)
    content_only = neutral_ticks(restore_event_memory_only(divergent, checkpoint), NEUTRAL_STEPS)
    return {
        "family": "S5", "case_id": case_id, "content": content, "goal": goal,
        "presentation": presentation, "ownership_input": owner,
        "checkpoint": {"digest": checkpoint.digest, "payload_hex": checkpoint.payload.hex(),
                       "state": state_record(checkpoint_state)},
        "divergence": {
            "registered_steps": DIVERGENT_STEPS,
            "intervention": intervention_receipt("DIVERGENT_HISTORY_SUBSTITUTION", checkpoint_state, divergent_start),
            "state_after_dirty_steps": state_record(divergent),
        },
        "arms": {
            "DIRECT": {"trace": trace(direct, goal, options)},
            "FULL_RESTORE": {"restored_checkpoint_state": state_record(restore_checkpoint(checkpoint)),
                             "trace": trace(full, goal, options)},
            "SHAM_RESTORE": {"trace": trace(sham, goal, options)},
            "CONTENT_ONLY_RESTORE": {"trace": trace(content_only, goal, options)},
        },
    }


def s6_case(content: int, goal: int, presentation: str,
            controlled: str, other: str) -> dict:
    case_id = f"S6_E{content:+d}_G{goal:+d}_{presentation}"
    options = target_options(content, goal, presentation)
    arms = {}
    for true_origin in ("SELF", "OTHER"):
        for represented in ("SELF", "OTHER"):
            state, owner = fresh_state(case_id + "_EVENT", content, represented, controlled, other)
            arm = f"ORIGIN_{true_origin}_ATTR_{represented}"
            arms[arm] = {
                "harness_only_true_origin": true_origin,
                "true_origin_supplied_to_core": False,
                "ownership_input": owner,
                "trace": trace(state, goal, options),
            }
    return {"family": "S6", "case_id": case_id, "content": content,
            "goal": goal, "presentation": presentation, "arms": arms}


def p_clamp_case(presentation: str, controlled: str, other: str) -> dict:
    case_id = f"P_CLAMP_{presentation}"
    options = symmetric_options(4, presentation)
    positive, pos_owner = fresh_state(case_id + "_POS", 4, "SELF", controlled, other)
    negative, neg_owner = fresh_state(case_id + "_NEG", -4, "SELF", controlled, other)
    positive_clamped = clamp_present_state(positive, 4)
    negative_clamped = clamp_present_state(negative, 4)
    return {
        "family": "P_CLAMP", "case_id": case_id, "goal": 0,
        "presentation": presentation, "ownership_inputs": [pos_owner, neg_owner],
        "arms": {
            "FROM_POSITIVE": {"trace": trace(positive_clamped, 0, options)},
            "FROM_NEGATIVE": {"trace": trace(negative_clamped, 0, options)},
        },
    }


def q_clamp_case(presentation: str, controlled: str, other: str) -> dict:
    case_id = f"Q_CLAMP_{presentation}"
    positive, pos_owner = fresh_state(case_id + "_POS", 4, "SELF", controlled, other)
    negative, neg_owner = fresh_state(case_id + "_NEG", -4, "SELF", controlled, other)
    scores = (OptionScore("LEFT", 16), OptionScore("RIGHT", 0))
    if presentation == "REVERSED":
        scores = tuple(reversed(scores))
    arms = {}
    for label, state in (("FROM_POSITIVE", positive), ("FROM_NEGATIVE", negative)):
        choice = select(scores)
        arms[label] = {
            "upstream_state": state_record(state),
            "selector_input": [{"option_id": x.option_id, "q": x.q} for x in scores],
            "choice": {"option_id": choice.option_id, "q": choice.q,
                       "winning_margin": choice.winning_margin},
        }
    return {
        "family": "Q_CLAMP", "case_id": case_id, "presentation": presentation,
        "ownership_inputs": [pos_owner, neg_owner], "arms": arms,
    }


def registered_cases(controlled: str, other: str) -> list[dict]:
    cases = []
    cases.extend(s1_case(e, g, p, controlled, other) for e, g, p in base_parameters())
    cases.extend(s2_case(m, p, controlled, other) for m in (4, 8) for p in ("NORMAL", "REVERSED"))
    cases.extend(s3_case(e, g, p, controlled, other) for e, g, p in base_parameters())
    cases.extend(s4_case(e, g, p, controlled, other) for e, g, p in base_parameters())
    cases.extend(s5_case(e, g, p, controlled, other) for e, g, p in base_parameters())
    cases.extend(s6_case(e, g, p, controlled, other) for e, g, p in base_parameters())
    cases.extend(p_clamp_case(p, controlled, other) for p in ("NORMAL", "REVERSED"))
    cases.extend(q_clamp_case(p, controlled, other) for p in ("NORMAL", "REVERSED"))
    identifiers = [case["case_id"] for case in cases]
    if len(identifiers) != 88 or len(set(identifiers)) != 88:
        raise ValueError("REGISTERED_CASE_INVENTORY")
    return cases


def execute_registered_run(run: dict) -> dict:
    plan = preregistration()
    if plan["observation_schedule"] != {
        "S5_divergent_steps_before_restore": DIVERGENT_STEPS,
        "S5_post_restore_neutral_steps": NEUTRAL_STEPS,
        "minimum_persistent_consecutive_target_probes": PROBES,
        "predecision_neutral_steps": NEUTRAL_STEPS,
        "probe_mutation_allowed": False,
        "read_only_probes": PROBES,
    }:
        raise ValueError("OBSERVATION_SCHEDULE_IMPLEMENTATION_MISMATCH")
    cases = registered_cases(run["controlled_token"], run["other_token"])
    if run["ordering"] == "REVERSED":
        cases = list(reversed(cases))
    elif run["ordering"] != "FORWARD":
        raise ValueError("UNREGISTERED_ORDER")
    return {
        "schema": "second-tier-sitc-raw-scientific-run/1",
        "preregistration_sha256": PREREG_SHA256,
        "registered_run_id": run["registered_run_id"],
        "ordering": run["ordering"],
        "token_bijection": {
            "controlled": run["controlled_token"],
            "other": run["other_token"],
        },
        "case_count": len(cases),
        "case_order": [case["case_id"] for case in cases],
        "cases": cases,
    }

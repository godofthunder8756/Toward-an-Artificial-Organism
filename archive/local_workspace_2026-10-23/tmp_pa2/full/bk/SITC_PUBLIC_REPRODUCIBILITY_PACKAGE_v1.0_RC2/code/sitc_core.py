"""Minimal exact-integer core for the frozen SITC v1 preregistration.

The module implements only the declared causal chain::

    event memory + resolved ownership -> self history -> present state
        -> prospective option values -> choice

Ownership tokens are consumed by :func:`resolve_ownership` and never enter a
checkpoint, the prospective evaluator, or the selector.  The evaluator accepts
only ``p``, ``goal`` and option identifiers/deltas.  The selector accepts only
option identifiers and Q values.  All persistent objects are immutable and all
serialized state uses canonical UTF-8 JSON with exact signed integers.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from hashlib import sha256
import json
from typing import Any


STATE_SCHEMA = "second-tier-sitc-state/1"
LOCAL_SELF_SLOT = "SELF"
CONTENT_DOMAIN = frozenset((-8, -4, 4, 8))


class SITCError(ValueError):
    """A registered domain, integrity, or causal-interface rule failed."""


class Relation(str, Enum):
    SELF = "SELF"
    OTHER = "OTHER"
    UNBOUND = "UNBOUND"


def _exact_int(value: object, name: str, *, minimum: int | None = None) -> int:
    if type(value) is not int:
        raise SITCError(f"{name}: expected exact integer")
    if minimum is not None and value < minimum:
        raise SITCError(f"{name}: expected integer >= {minimum}")
    return value


def _nonempty_string(value: object, name: str) -> str:
    if type(value) is not str or not value:
        raise SITCError(f"{name}: expected non-empty string")
    return value


def _content(value: object, name: str = "content") -> int:
    value = _exact_int(value, name)
    if value not in CONTENT_DOMAIN:
        raise SITCError(f"{name}: outside frozen content domain")
    return value


def _relation(value: object) -> Relation:
    if type(value) is Relation:
        return value
    if type(value) is not str:
        raise SITCError("relation: expected registered relation")
    try:
        return Relation(value)
    except ValueError as exc:
        raise SITCError("relation: expected registered relation") from exc


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")


def _sha256(payload: bytes) -> str:
    return sha256(payload).hexdigest()


@dataclass(frozen=True, slots=True)
class EventMemory:
    event_key: str
    content: int

    def __post_init__(self) -> None:
        _nonempty_string(self.event_key, "event_key")
        _content(self.content)

    def to_wire(self) -> dict[str, object]:
        return {"content": self.content, "event_key": self.event_key}

    def to_bytes(self) -> bytes:
        return _canonical_json_bytes({"schema": "sitc-event-memory/1", **self.to_wire()})

    def sha256(self) -> str:
        return _sha256(self.to_bytes())


@dataclass(frozen=True, slots=True)
class OwnershipInput:
    attributed_owner_token: str
    controlled_entity_token: str

    def __post_init__(self) -> None:
        _nonempty_string(self.attributed_owner_token, "attributed_owner_token")
        _nonempty_string(self.controlled_entity_token, "controlled_entity_token")


@dataclass(frozen=True, slots=True)
class SelfHistory:
    event_key: str
    content: int
    relation: Relation

    def __post_init__(self) -> None:
        _nonempty_string(self.event_key, "event_key")
        _content(self.content)
        object.__setattr__(self, "relation", _relation(self.relation))

    def to_wire(self) -> dict[str, object]:
        return {
            "content": self.content,
            "event_key": self.event_key,
            "relation": self.relation.value,
        }

    def to_bytes(self) -> bytes:
        return _canonical_json_bytes({"schema": "sitc-self-history/1", **self.to_wire()})

    def sha256(self) -> str:
        return _sha256(self.to_bytes())


@dataclass(frozen=True, slots=True)
class PresentState:
    p: int
    tick: int

    def __post_init__(self) -> None:
        _exact_int(self.p, "p")
        _exact_int(self.tick, "tick", minimum=0)

    def to_wire(self) -> dict[str, int]:
        return {"p": self.p, "tick": self.tick}


@dataclass(frozen=True, slots=True)
class SITCState:
    event_memory: EventMemory
    self_history: SelfHistory
    present_state: PresentState
    schema_version: str = STATE_SCHEMA
    controlled_entity_slot: str = LOCAL_SELF_SLOT

    def __post_init__(self) -> None:
        if type(self.event_memory) is not EventMemory:
            raise SITCError("event_memory: expected EventMemory")
        if type(self.self_history) is not SelfHistory:
            raise SITCError("self_history: expected SelfHistory")
        if type(self.present_state) is not PresentState:
            raise SITCError("present_state: expected PresentState")
        if self.schema_version != STATE_SCHEMA:
            raise SITCError("schema_version: unsupported state schema")
        if self.controlled_entity_slot != LOCAL_SELF_SLOT:
            raise SITCError("controlled_entity_slot: expected actor-local SELF slot")

    @property
    def p(self) -> int:
        return self.present_state.p

    @property
    def tick(self) -> int:
        return self.present_state.tick

    def to_wire(self) -> dict[str, object]:
        return {
            "controlled_entity_slot": self.controlled_entity_slot,
            "event_memory": self.event_memory.to_wire(),
            "present_state": self.present_state.to_wire(),
            "schema_version": self.schema_version,
            "self_history": self.self_history.to_wire(),
        }

    def to_bytes(self) -> bytes:
        return _canonical_json_bytes(self.to_wire())

    def sha256(self) -> str:
        return _sha256(self.to_bytes())

    @classmethod
    def from_bytes(cls, payload: bytes) -> "SITCState":
        if type(payload) is not bytes or not payload:
            raise SITCError("state bytes: expected non-empty immutable bytes")
        try:
            document = json.loads(payload.decode("utf-8"))
        except (UnicodeError, json.JSONDecodeError) as exc:
            raise SITCError("state bytes: invalid JSON") from exc
        if type(document) is not dict or set(document) != {
            "controlled_entity_slot", "event_memory", "present_state",
            "schema_version", "self_history",
        }:
            raise SITCError("state bytes: exact top-level inventory required")
        event = document["event_memory"]
        history = document["self_history"]
        present = document["present_state"]
        if type(event) is not dict or set(event) != {"event_key", "content"}:
            raise SITCError("state bytes: exact event-memory inventory required")
        if type(history) is not dict or set(history) != {"event_key", "content", "relation"}:
            raise SITCError("state bytes: exact self-history inventory required")
        if type(present) is not dict or set(present) != {"p", "tick"}:
            raise SITCError("state bytes: exact present-state inventory required")
        result = cls(
            EventMemory(event["event_key"], event["content"]),
            SelfHistory(history["event_key"], history["content"], history["relation"]),
            PresentState(present["p"], present["tick"]),
            document["schema_version"], document["controlled_entity_slot"],
        )
        if result.to_bytes() != payload:
            raise SITCError("state bytes: noncanonical encoding")
        return result


@dataclass(frozen=True, slots=True)
class Checkpoint:
    payload: bytes
    digest: str

    def __post_init__(self) -> None:
        if type(self.payload) is not bytes or not self.payload:
            raise SITCError("checkpoint payload: expected immutable state bytes")
        _nonempty_string(self.digest, "checkpoint digest")
        if len(self.digest) != 64 or any(ch not in "0123456789abcdef" for ch in self.digest):
            raise SITCError("checkpoint digest: expected lowercase SHA-256")
        if _sha256(self.payload) != self.digest:
            raise SITCError("CHECKPOINT_DIGEST_MISMATCH")
        # Construction itself is an integrity boundary.
        SITCState.from_bytes(self.payload)


@dataclass(frozen=True, slots=True)
class Option:
    option_id: str
    delta: int

    def __post_init__(self) -> None:
        _nonempty_string(self.option_id, "option_id")
        _exact_int(self.delta, "delta")


@dataclass(frozen=True, slots=True)
class ProspectiveEvaluation:
    option_id: str
    delta: int
    future: int
    q: int

    def __post_init__(self) -> None:
        _nonempty_string(self.option_id, "option_id")
        _exact_int(self.delta, "delta")
        _exact_int(self.future, "future")
        _exact_int(self.q, "q")


@dataclass(frozen=True, slots=True)
class OptionScore:
    """The selector-visible projection: an option identifier and Q only."""

    option_id: str
    q: int

    def __post_init__(self) -> None:
        _nonempty_string(self.option_id, "option_id")
        _exact_int(self.q, "q")


@dataclass(frozen=True, slots=True)
class Choice:
    option_id: str
    q: int
    winning_margin: int

    def __post_init__(self) -> None:
        _nonempty_string(self.option_id, "option_id")
        _exact_int(self.q, "q")
        _exact_int(self.winning_margin, "winning_margin", minimum=1)


@dataclass(frozen=True, slots=True)
class Probe:
    state_sha256: str
    p: int
    tick: int
    evaluations: tuple[ProspectiveEvaluation, ...]
    scores: tuple[OptionScore, ...]
    choice: Choice
    chosen_delta: int

    def __post_init__(self) -> None:
        if (type(self.state_sha256) is not str or len(self.state_sha256) != 64
                or any(ch not in "0123456789abcdef" for ch in self.state_sha256)):
            raise SITCError("probe state hash: expected lowercase SHA-256")
        _exact_int(self.p, "probe p")
        _exact_int(self.tick, "probe tick", minimum=0)
        if type(self.evaluations) is not tuple or not self.evaluations:
            raise SITCError("probe evaluations: expected non-empty tuple")
        if type(self.scores) is not tuple or not self.scores:
            raise SITCError("probe scores: expected non-empty tuple")
        if type(self.choice) is not Choice:
            raise SITCError("probe choice: expected Choice")
        _exact_int(self.chosen_delta, "chosen_delta")


def resolve_ownership(ownership_input: OwnershipInput) -> Relation:
    """Resolve opaque tokens to an actor-local role; return no token."""
    if type(ownership_input) is not OwnershipInput:
        raise SITCError("ownership_input: expected OwnershipInput")
    if ownership_input.attributed_owner_token == ownership_input.controlled_entity_token:
        return Relation.SELF
    return Relation.OTHER


def represent_history(event_memory: EventMemory, relation: Relation) -> SelfHistory:
    if type(event_memory) is not EventMemory:
        raise SITCError("event_memory: expected EventMemory")
    resolved = _relation(relation)
    if resolved is Relation.UNBOUND:
        raise SITCError("UNBOUND is intervention-only")
    return SelfHistory(event_memory.event_key, event_memory.content, resolved)


def present_from_history(self_history: SelfHistory, tick: int = 0) -> PresentState:
    if type(self_history) is not SelfHistory:
        raise SITCError("self_history: expected SelfHistory")
    _exact_int(tick, "tick", minimum=0)
    p = self_history.content if self_history.relation is Relation.SELF else 0
    return PresentState(p, tick)


def acquire(event_memory: EventMemory, ownership_input: OwnershipInput) -> SITCState:
    """Create a fresh actor-local state before any decision or action feedback."""
    relation = resolve_ownership(ownership_input)
    history = represent_history(event_memory, relation)
    return SITCState(event_memory, history, present_from_history(history))


def neutral_tick(state: SITCState) -> SITCState:
    if type(state) is not SITCState:
        raise SITCError("state: expected SITCState")
    return replace(state, present_state=PresentState(state.p, state.tick + 1))


def neutral_ticks(state: SITCState, count: int) -> SITCState:
    if type(state) is not SITCState:
        raise SITCError("state: expected SITCState")
    _exact_int(count, "count", minimum=0)
    return replace(state, present_state=PresentState(state.p, state.tick + count))


def _option_tuple(option_id_and_delta: tuple[Option, ...]) -> tuple[Option, ...]:
    if type(option_id_and_delta) is not tuple or len(option_id_and_delta) < 2:
        raise SITCError("options: expected tuple containing at least two options")
    if any(type(option) is not Option for option in option_id_and_delta):
        raise SITCError("options: expected only Option values")
    identifiers = tuple(option.option_id for option in option_id_and_delta)
    if len(set(identifiers)) != len(identifiers):
        raise SITCError("options: duplicate option identifier")
    return option_id_and_delta


def evaluate_prospects(
    p: int,
    goal: int,
    option_id_and_delta: tuple[Option, ...],
) -> tuple[ProspectiveEvaluation, ...]:
    """Evaluate F and Q from only P, goal, and option identifier/delta."""
    p = _exact_int(p, "p")
    goal = _exact_int(goal, "goal")
    options = _option_tuple(option_id_and_delta)
    result = []
    for option in options:
        future = p + option.delta
        q = -((future - goal) ** 2)
        result.append(ProspectiveEvaluation(option.option_id, option.delta, future, q))
    return tuple(result)


def selector_projection(
    evaluations: tuple[ProspectiveEvaluation, ...],
) -> tuple[OptionScore, ...]:
    if type(evaluations) is not tuple or len(evaluations) < 2:
        raise SITCError("evaluations: expected tuple containing at least two evaluations")
    if any(type(item) is not ProspectiveEvaluation for item in evaluations):
        raise SITCError("evaluations: unexpected value")
    identifiers = tuple(item.option_id for item in evaluations)
    if len(set(identifiers)) != len(identifiers):
        raise SITCError("evaluations: duplicate option identifier")
    return tuple(OptionScore(item.option_id, item.q) for item in evaluations)


def select(scored_options: tuple[OptionScore, ...]) -> Choice:
    """Choose the unique maximum from only option identifiers and Q values."""
    if type(scored_options) is not tuple or len(scored_options) < 2:
        raise SITCError("scored_options: expected tuple containing at least two scores")
    if any(type(item) is not OptionScore for item in scored_options):
        raise SITCError("scored_options: expected only OptionScore values")
    identifiers = tuple(item.option_id for item in scored_options)
    if len(set(identifiers)) != len(identifiers):
        raise SITCError("scored_options: duplicate option identifier")
    ordered = sorted(scored_options, key=lambda item: item.q, reverse=True)
    if ordered[0].q == ordered[1].q:
        raise SITCError("TIE_INVALID")
    return Choice(ordered[0].option_id, ordered[0].q, ordered[0].q - ordered[1].q)


def semantic_delta(choice: Choice, options: tuple[Option, ...]) -> int:
    """Harness-side semantic lookup after selection; it is not selector input."""
    if type(choice) is not Choice:
        raise SITCError("choice: expected Choice")
    options = _option_tuple(options)
    matches = tuple(option.delta for option in options if option.option_id == choice.option_id)
    if len(matches) != 1:
        raise SITCError("choice does not identify exactly one semantic option")
    return matches[0]


def _probe_with_effective_p(state: SITCState, effective_p: int, goal: int,
                            options: tuple[Option, ...]) -> Probe:
    if type(state) is not SITCState:
        raise SITCError("state: expected SITCState")
    before = state.to_bytes()
    evaluations = evaluate_prospects(effective_p, goal, options)
    scores = selector_projection(evaluations)
    choice = select(scores)
    observation = Probe(
        state.sha256(), state.p, state.tick, evaluations, scores, choice,
        semantic_delta(choice, options),
    )
    if state.to_bytes() != before:
        raise SITCError("READ_ONLY_PROBE_MUTATED_STATE")
    return observation


def read_only_probe(state: SITCState, goal: int, options: tuple[Option, ...]) -> Probe:
    return _probe_with_effective_p(state, state.p, goal, options)


def read_only_probe_coupling_ablated(
    state: SITCState, goal: int, options: tuple[Option, ...],
) -> Probe:
    """Ablate only P-to-F/Q by evaluating at the registered reference P=0."""
    return _probe_with_effective_p(state, 0, goal, options)


def capture_checkpoint(state: SITCState) -> Checkpoint:
    if type(state) is not SITCState:
        raise SITCError("state: expected SITCState")
    payload = state.to_bytes()
    return Checkpoint(payload, _sha256(payload))


def restore_checkpoint(checkpoint: Checkpoint) -> SITCState:
    if type(checkpoint) is not Checkpoint:
        raise SITCError("checkpoint: expected Checkpoint")
    if _sha256(checkpoint.payload) != checkpoint.digest:
        raise SITCError("CHECKPOINT_DIGEST_MISMATCH")
    restored = SITCState.from_bytes(checkpoint.payload)
    if restored.to_bytes() != checkpoint.payload:
        raise SITCError("CHECKPOINT_RESTORE_BYTE_MISMATCH")
    return restored


def substitute_self_history(state: SITCState, donor_history: SelfHistory) -> SITCState:
    """S2: replace actor-local H and causally recompute P; retain recipient E/clock."""
    if type(state) is not SITCState or type(donor_history) is not SelfHistory:
        raise SITCError("self-history substitution: invalid state or donor")
    present = present_from_history(donor_history, state.tick)
    return replace(state, self_history=donor_history, present_state=present)


def swap_self_histories(left: SITCState, right: SITCState) -> tuple[SITCState, SITCState]:
    if type(left) is not SITCState or type(right) is not SITCState:
        raise SITCError("self-history swap: expected two SITCState values")
    return substitute_self_history(left, right.self_history), substitute_self_history(right, left.self_history)


def ablate_attribution(state: SITCState) -> SITCState:
    """S3: change SELF to UNBOUND, preserve E/content/clock, and recompute P."""
    if type(state) is not SITCState:
        raise SITCError("state: expected SITCState")
    if state.self_history.relation is not Relation.SELF:
        raise SITCError("attribution ablation requires SELF history")
    history = replace(state.self_history, relation=Relation.UNBOUND)
    return replace(state, self_history=history, present_state=present_from_history(history, state.tick))


def substitute_history_content(state: SITCState, content: int) -> SITCState:
    """S5 divergence: replace SELF-history content only and recompute P."""
    if type(state) is not SITCState:
        raise SITCError("state: expected SITCState")
    content = _content(content, "substituted content")
    if state.self_history.relation is not Relation.SELF:
        raise SITCError("history-content substitution requires SELF history")
    history = replace(state.self_history, content=content)
    return replace(state, self_history=history, present_state=present_from_history(history, state.tick))


def clamp_present_state(state: SITCState, p: int) -> SITCState:
    """Registered P clamp; preserve E, H and clock exactly."""
    if type(state) is not SITCState:
        raise SITCError("state: expected SITCState")
    p = _exact_int(p, "clamped p")
    return replace(state, present_state=PresentState(p, state.tick))


def sham_restore(state: SITCState, checkpoint: Checkpoint) -> SITCState:
    """Validate the registered checkpoint but retain the entire current state."""
    if type(state) is not SITCState:
        raise SITCError("state: expected SITCState")
    restore_checkpoint(checkpoint)
    return state


def restore_event_memory_only(state: SITCState, checkpoint: Checkpoint) -> SITCState:
    """S5 content-only arm: restore E while retaining divergent H/P/clock."""
    if type(state) is not SITCState:
        raise SITCError("state: expected SITCState")
    source = restore_checkpoint(checkpoint)
    return replace(state, event_memory=source.event_memory)


def intervention_receipt(kind: str, before: SITCState, after: SITCState) -> dict[str, object]:
    """Return canonicalizable before/after provenance without scientific labels."""
    _nonempty_string(kind, "intervention kind")
    if type(before) is not SITCState or type(after) is not SITCState:
        raise SITCError("intervention receipt: expected SITCState values")
    return {
        "after_sha256": after.sha256(),
        "before_sha256": before.sha256(),
        "effective": before.to_bytes() != after.to_bytes(),
        "intervention_type": kind,
    }


__all__ = [
    "CONTENT_DOMAIN", "LOCAL_SELF_SLOT", "STATE_SCHEMA", "Checkpoint", "Choice",
    "EventMemory", "Option", "OptionScore", "OwnershipInput", "PresentState",
    "Probe", "ProspectiveEvaluation", "Relation", "SITCError", "SITCState",
    "SelfHistory",
    "ablate_attribution", "acquire", "capture_checkpoint", "clamp_present_state",
    "evaluate_prospects", "intervention_receipt", "neutral_tick", "neutral_ticks",
    "present_from_history", "read_only_probe", "read_only_probe_coupling_ablated",
    "represent_history", "resolve_ownership", "restore_checkpoint",
    "restore_event_memory_only", "select", "selector_projection", "semantic_delta",
    "sham_restore", "substitute_history_content", "substitute_self_history",
    "swap_self_histories",
]

"""H15 preflight and opt-in evaluation harness. Import never launches a fit.

Training remains forbidden until preflight, exact configurations, source
hashes, and remaining resource instrumentation gaps are independently frozen.
"""

from __future__ import annotations

import hashlib
from itertools import product
import os
from pathlib import Path
from time import perf_counter
from typing import Mapping

import numpy as np
import psutil  # type: ignore[import-untyped]
import torch

from phase3b import PRIMARY
from phase3b.interventions import ExpandedWord, NoMessage, UnlimitedRead, first_divergence, intervene
from phase3b.models import Arm, Trace, _token, clone_as_r9
from phase3b.proof import verify_h3
from phase3b.resources import Meter, charge, count, grid, linear_meter, observed, python_peak, require_fit
from phase3b.world import Episode, generate, loss_units


# Full execution is deliberately locked until every protocol-required meter
# (nonlinear work, memory traffic and peak storage) is implemented and audited.
RESOURCE_METER_COMPLETE = False


def source_hashes() -> dict[str, str]:
    """All H15 sources and governing design documents, excluding generated data."""
    folder = Path(__file__).parent
    roots = ("PHASE3B_TRANSITION_v1.md", "COMPETITIVE_ACCESS_DEFINITION_v1.md",
             "PHASE3B_ENVIRONMENT_v1.md", "PHASE3B_IDENTIFIABILITY_v1.md",
             "PHASE3B_SPECIALISTS_v1.md", "PHASE3B_COMPETITION_SIGNATURE_v1.md",
             "PHASE3B_REDUCTION_REVIEW_v1.md", "PHASE3B_THEORY_MAPPING_v1.md",
             "ACI_PHASE3B_PROTOCOL_v1.md")
    paths = (*sorted(folder.rglob("*.py")), *(folder.parent / name for name in roots))
    return {p.relative_to(folder.parent).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in paths}


def assert_replay_equal(left: Trace, right: Trace) -> None:
    if (left.word is None) != (right.word is None):
        raise AssertionError("message presence divergence; STOP")
    if left.word is not None and right.word is not None and not torch.equal(left.word, right.word):
        raise AssertionError("message divergence; STOP")
    for x, y in zip(left.actions + left.logits, right.actions + right.logits):
        if not torch.equal(x, y):
            raise AssertionError("consumer divergence; STOP")


def clone_check(candidate: Arm) -> int:
    """Exhaust all 256 histories x 8 local-bit triples at all 4 contexts."""
    if candidate.name != "candidate":
        raise ValueError("R9 clone source must be candidate")
    clone = clone_as_r9(candidate).eval()
    histories = torch.tensor(list(product((0, 1), repeat=8)), dtype=torch.long)
    local_cases = torch.tensor(list(product((0, 1), repeat=3)), dtype=torch.long)
    common = histories.repeat_interleave(8, dim=0)
    local = local_cases.repeat(256, 1).unsqueeze(1).expand(-1, 4, -1).clone()
    with torch.no_grad():
        for offset in range(0, len(common), 128):
            a = candidate(common[offset:offset+128], local[offset:offset+128])
            b = clone(common[offset:offset+128], local[offset:offset+128])
            assert_replay_equal(a, b)
            if not torch.equal(a.address, b.address) or not torch.equal(a.payload, b.payload):
                raise AssertionError("R9 address/payload clone mismatch; STOP")
    candidate_cost = count(candidate)
    cloned_cost = count(clone)
    if any(candidate_cost[key] != cloned_cost[key] for key in
           ("trainable_parameters", "forward_macs_per_episode", "parameter_bytes")):
        raise AssertionError("R9 clone resource mismatch; STOP")
    return len(common) * 4


def leak_check(candidate: Arm) -> None:
    """Structural isolation and runtime no-op/same-word negative controls."""
    episode = generate(6789, 8)
    candidate.eval()
    with torch.no_grad():
        intact = candidate(episode.common, episode.local)
        assert_replay_equal(intact, intervene(candidate, episode.common, episode.local, "noop"))
        assert torch.equal(first_divergence(intact, intact), torch.full((8,), -1))
        changed_truth = Episode(episode.common, episode.local, 1 - episode.truth)
        assert_replay_equal(intact, candidate(changed_truth.common, changed_truth.local))
        for port in range(4):
            changed = episode.common.clone()
            changed[:, port] ^= 1
            states = candidate.encode(changed)
            for other in range(4):
                if other != port and not torch.equal(states[:, other], intact.states[:, other]):
                    raise AssertionError("other port read private observation; STOP")
        for i in range(3):
            local = episode.local.clone()
            local[:, :, i] ^= 1
            shifted = candidate(episode.common, local)
            if not torch.equal(intact.word, shifted.word):
                raise AssertionError("selector read a local bit; STOP")
            for j in range(3):
                if j != i and not torch.equal(intact.logits[j], shifted.logits[j]):
                    raise AssertionError("head read other head's private bit; STOP")
        for word in range(8):
            injected = torch.full_like(intact.word, word)
            replay = candidate(episode.common, episode.local, words=injected)
            changed = episode.common ^ 1
            swapped = candidate(changed, episode.local, words=injected)
            # A consumer cannot read hidden states, selector logits or history.
            for a, b in zip(replay.logits, swapped.logits):
                if not torch.equal(a, b):
                    raise AssertionError("consumer side channel; STOP")
        try:
            candidate(episode.common, episode.local, words=torch.full_like(intact.word, 8))
        except ValueError:
            pass
        else:
            raise AssertionError("ninth on-wire token accepted; STOP")


def preflight() -> dict:
    """No neural training or scoring; returns only proof, resource and hashes."""
    proof = verify_h3()
    grids = {family: grid(family) for family in PRIMARY}
    for family, configs in grids.items():
        if len(configs) != 6:
            raise AssertionError(f"{family} missing configurations; STOP")
        for width, _ in configs:
            require_fit(Arm(family, width))
    candidate = Arm("candidate", grids["candidate"][-1][0])
    require_fit(clone_as_r9(candidate))
    leak_check(candidate)
    checked = clone_check(candidate)
    return {"h3": proof, "r9_clone_inputs": checked, "grids": grids,
            "resources": {family: [count(Arm(family, w)) for w, _ in configs]
                          for family, configs in grids.items()},
            "source_sha256": source_hashes(),
            "authorization": "NOT FROZEN: no engineering or final runs authorized"}


def _run_loss(trace: Trace, episode: Episode) -> torch.Tensor:
    return loss_units(trace.actions, episode.truth)  # evaluator-only boundary


def build(family: str, width: int, seed: int) -> Arm:
    """Initialize independently for every arm/configuration/training seed."""
    torch.manual_seed(seed)
    return Arm(family, width)


def require_authorization(authorization: Mapping | None) -> None:
    if not RESOURCE_METER_COMPLETE:
        raise RuntimeError("resource meter incomplete: pretraining STOP")
    from phase3b.freeze import verify_preflight_snapshot

    if (authorization is None or authorization.get("phase") != "engineering"
            or authorization.get("source_sha256") != source_hashes()
            or authorization.get("preflight_passed") is not True
            or authorization.get("approved") is not True
            or not isinstance(authorization.get("snapshot_path"), str)
            or not isinstance(authorization.get("snapshot_sha256"), str)):
        raise RuntimeError("pretraining gate not frozen; STOP before neural training")
    verify_preflight_snapshot(Path(authorization["snapshot_path"]),
                              authorization["snapshot_sha256"])


def validate_training_seed(seed: int, phase: str) -> None:
    """Engineering and final seeds are disjoint; finals have no entry point yet."""
    if type(seed) is not int or (phase != "engineering" or seed not in range(4)):
        raise ValueError("undeclared engineering seed or phase; STOP")


def fit(model: Arm, seed: int, learning_rate: float, *,
    authorization: Mapping | None = None) -> tuple[dict, torch.optim.Optimizer]:
    """Opt-in training ONLY after external execution freeze; no implicit run.

    Shared 8,192 episodes (seeds independent of arm), 256 AdamW updates of
    batch 32, same on-policy loss-per-consumer/context baseline (decay .9).
    No held-out c=3 actions, labels or feedback enter a training gradient.
    """
    validate_training_seed(seed, "engineering")
    require_authorization(authorization)
    require_fit(model)
    if learning_rate not in (0.0003, 0.001) or not isinstance(seed, int):
        raise ValueError("nonprotocol training configuration")
    torch.manual_seed(seed)
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate, weight_decay=0)
    baseline = torch.zeros(3, 3)
    seen = 0
    meter = Meter()
    started = perf_counter()
    model.train()
    with python_peak() as peak, linear_meter(model, meter):
        for update in range(256):
            episode = generate(100_000 + seed * 256 + update, 32)
            if model.name == "R4":
                model.route = None
                forced = (torch.arange(seen, seen + 32) % 4).unsqueeze(1).expand(-1, 3)
            else:
                forced = None
            trace = model(episode.common, episode.local[:, :3], contexts=3,
                          stochastic=True, forced=forced)
            if any(action.shape != (32, 3) for action in trace.actions):
                raise AssertionError("held-out context entered training graph; STOP")
            losses = _run_loss(trace, episode).float() / 50  # 50 units = loss 1 / consumer
            advantage = losses.detach() - baseline.T.unsqueeze(0)
            terms = [advantage[:, :, i] * trace.action_logp[i] for i in range(3)]
            objective = sum(t.mean() for t in terms) / 3
            if trace.token_logp is not None:
                objective += (advantage.mean(-1) * trace.token_logp).mean()
            optimizer.zero_grad(set_to_none=True)
            objective.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1)
            optimizer.step()
            baseline = 0.9 * baseline + 0.1 * losses.mean(0).T
            seen += 32
    if seen != 8192:
        raise AssertionError("training allowance violated; STOP")
    resource_log = {"episodes": seen, "updates": 256, "wall_seconds": perf_counter() - started,
                    "process_peak_working_set_bytes": psutil.Process(os.getpid()).memory_info().peak_wset,
                    "process_peak_limitations": "process-lifetime high-water mark includes all earlier allocations; "
                                                "not isolated per model or physical bus traffic",
                    "observed_linear_forward_macs": meter.forward_macs,
                    "observed_linear_backward_macs": meter.backward_macs,
                    "forward_macs_per_training_episode": meter.forward_macs // seen,
                    "optimizer_state_bytes": sum(v.numel() * v.element_size()
                                                 for state in optimizer.state.values()
                                                 for v in state.values() if isinstance(v, torch.Tensor)),
                    "baseline_state_bytes": baseline.numel() * baseline.element_size(),
                    "model": count(model), **observed(meter), **peak,
                    "training_compute_limitations": "backward nonlinearity, objective, loss, clipping, "
                                                    "AdamW and episode generator not counted"}
    if model.name == "R4":
        resource_log["route_search"] = select_r4_route(model, seed)
    return resource_log, optimizer


def train_diagnostic(candidate: Arm, diagnostic: NoMessage | ExpandedWord | UnlimitedRead,
                     seed: int, *, authorization: Mapping | None = None) -> dict:
    """Opt-in I2/I4/I5 readout fit on equal training episodes, frozen encoders.

    I6 reuses I2's separately trained no-message readout. Diagnostic
    expansions are not intact-channel primary configurations.
    """
    require_authorization(authorization)
    if candidate.name != "candidate":
        raise ValueError("only frozen candidate states can be expanded")
    candidate.eval()
    for p in candidate.parameters():
        p.requires_grad_(False)
    optimizer = torch.optim.AdamW(diagnostic.parameters(), lr=0.001, weight_decay=0)
    baseline = torch.zeros(3, 3)
    meter = Meter()
    start = perf_counter()
    with python_peak() as peak, linear_meter(diagnostic, meter):
        for update in range(256):
            ep = generate(100_000 + seed * 256 + update, 32)
            with torch.no_grad():
                frozen = candidate.encode(ep.common)
            local = ep.local[:, :3]
            if isinstance(diagnostic, NoMessage):
                logits = tuple(torch.stack([diagnostic.read(local[:, c, i], c, i)
                                            for c in range(3)], 1) for i in range(3))
                tokens = tuple(_token(l, True) for l in logits)
                trace = Trace(logits, tuple(v[0] for v in tokens),
                              action_logp=tuple(v[1] for v in tokens))
            else:
                trace = diagnostic(frozen, local, stochastic=True)
            losses = _run_loss(trace, ep).float() / 50
            adv = losses.detach() - baseline.T.unsqueeze(0)
            if trace.action_logp is None:
                raise AssertionError("diagnostic readout did not return action log probabilities")
            objective = torch.stack([(adv[:, :, i] * trace.action_logp[i]).mean()
                                     for i in range(3)]).mean()
            if trace.token_logp is not None:
                objective += (adv.mean(-1) * trace.token_logp).mean()
            optimizer.zero_grad(set_to_none=True)
            objective.backward()
            torch.nn.utils.clip_grad_norm_(diagnostic.parameters(), 1)
            optimizer.step()
            baseline = 0.9 * baseline + 0.1 * losses.mean(0).T
    if isinstance(diagnostic, NoMessage):
        diagnostic.trained = True
    return {"episodes": 8192, "updates": 256, "parameters_added": sum(p.numel() for p in diagnostic.parameters()),
            "process_peak_working_set_bytes": psutil.Process(os.getpid()).memory_info().peak_wset,
            "forward_linear_macs": meter.forward_macs, "backward_linear_macs": meter.backward_macs,
            "wall_seconds": perf_counter() - start, **observed(meter), **peak,
            "frozen_encoder_compute": "excluded from diagnostic meter; must account separately",
            "read_bits": (diagnostic.bits if isinstance(diagnostic, ExpandedWord) else
                          candidate.width * 4 * 32 if isinstance(diagnostic, UnlimitedRead) else 0),
            "bandwidth": "out-of-band diagnostic, not intact 3-bit channel"}


@torch.no_grad()
def training_context_score(model: Arm, seed: int, *, meter: Meter | None = None) -> int:
    """Aggregate c=0..2 TRAINING loss only; NEVER select by c=3."""
    model.eval()
    total = 0
    with linear_meter(model, meter if meter is not None else Meter()):
        for update in range(256):
            ep = generate(100_000 + seed * 256 + update, 32)
            trace = model(ep.common, ep.local[:, :3], contexts=3)
            total += int(_run_loss(trace, ep).sum())
    return total


def engineering_selection(family: str, authorization: Mapping | None = None) -> dict:
    """Opt-in 24 fits per family; selection uses *only* training contexts.

    This function is intentionally never invoked by preflight or tests.
    Training weights are discarded; finals need a separate H16 authorization.
    """
    require_authorization(authorization)
    configurations = grid(family)
    rows = []
    for width, lr in configurations:
        score, spends = 0, []
        scoring_meter = Meter()
        scoring_seconds = 0.0
        for seed in range(4):
            model = build(family, width, seed)
            spend, _ = fit(model, seed, lr, authorization=authorization)
            spends.append(spend)
            scoring_started = perf_counter()
            score += training_context_score(model, seed, meter=scoring_meter)
            scoring_seconds += perf_counter() - scoring_started
        rows.append({"width": width, "learning_rate": lr, "training_context_loss_units": score,
                     "parameters": count(build(family, width, 0))["trainable_parameters"],
                     "spends": spends,
                     "scoring_wall_seconds": scoring_seconds,
                     "scoring_forward_macs": scoring_meter.forward_macs,
                     "scoring_operations": observed(scoring_meter)})
    best = min(rows, key=lambda row: (row["training_context_loss_units"],
                                      row["parameters"], row["learning_rate"]))
    return {"family": family, "configurations": rows,
            "selected": {"width": best["width"], "learning_rate": best["learning_rate"]}}


@torch.no_grad()
def r4_training_route(table: torch.Tensor) -> tuple[int, int, int, int]:
    """Enumerate 256 routes; score c=0..2 only, then apply c=3 tie rule."""
    if table.shape != (3, 4):
        raise ValueError("R4 requires three training contexts and four sources")
    routes = product(range(4), repeat=4)

    def rank(route: tuple[int, ...]):
        for c in range(3):
            charge(indexed=table[c, route[c]])
        return (sum(int(table[c, route[c]]) for c in range(3)),
                route[3] != (route[2] + 1) % 4, route)

    best = min(routes, key=rank)
    return best[0], best[1], best[2], best[3]


@torch.no_grad()
def select_r4_route(model: Arm, seed: int) -> dict:
    """Freeze weights; cache four per-context source losses on TRAINING draws.

    Enumerating 4^4 routes uses only c=0,1,2. Unobserved c=3
    follows the declared one-plus-c2 tie rule, never its held-out loss.
    """
    if model.name != "R4":
        raise ValueError("R4 only")
    model.eval()
    table = torch.zeros(3, 4, dtype=torch.long)
    meter = Meter()
    started = perf_counter()
    with linear_meter(model, meter):
        for update in range(256):
            ep = generate(100_000 + seed * 256 + update, 32)
            states = model.encode(ep.common)
            from phase3b.world import targets
            tgt = targets(ep.truth, 4)
            for address in range(4):
                words = model.write(states, 3, forced=torch.full((32, 3), address, dtype=torch.long))[0]
                for c in range(3):
                    scores = tuple(model.read(words[:, c], ep.local[:, c, i], c, i)
                                   for i in range(3))
                    for score in scores:
                        charge(argmax=score)
                    actions = tuple(score.argmax(-1) for score in scores)
                    # The actual rotated c targets, not context-zero targets.
                    table[c, address] += ((actions[0] != tgt[0][:, c]).sum() * 50
                                          + torch.where(actions[1] == 2, 9,
                                                        (actions[1] != tgt[1][:, c]).long() * 50).sum()
                                          + (actions[2] != tgt[2][:, c]).sum() * 50)
    model.route = r4_training_route(table)
    return {"training_loss_table_units": table.tolist(), "route": model.route,
            "routes_enumerated": 256, "training_route_scores_per_context": 256,
            "route_score_table_lookups": 768, "route_score_additions": 512,
            "route_rank_comparisons": 255,
            "training_exposure_per_address": 2048, "search_exposure_per_address": 8192,
            "search_wall_seconds": perf_counter() - started,
            "search_forward_macs": meter.forward_macs, "search_operations": observed(meter)}


@torch.no_grad()
def evaluate(model: Arm, seed: int, *, size: int = 4096) -> dict[str, np.ndarray]:
    """Fixed paired stream 20000+s; read-only evaluation; no optimizer."""
    if model.name == "R4" and model.route is None:
        raise ValueError("R4 route must be chosen from training only")
    if size < 1:
        raise ValueError("invalid evaluation size")
    model.eval()
    components, actions, words = [], [], []
    full = generate(20_000 + seed, size)
    for offset in range(0, size, 128):
        ep = Episode(full.common[offset:offset+128], full.local[offset:offset+128],
                     full.truth[offset:offset+128])
        trace = model(ep.common, ep.local)
        components.append(_run_loss(trace, ep).numpy().astype(np.uint8))
        actions.append(torch.stack(trace.actions, -1).numpy().astype(np.uint8))
        if trace.word is not None:
            words.append(trace.word.numpy().astype(np.uint8))
    return {"components": np.concatenate(components), "actions": np.concatenate(actions),
            "words": np.concatenate(words) if words else np.empty((0, 4), dtype=np.uint8)}
"""Post-final Phase III-B I1-I7 secondary diagnostics; never a primary endpoint.

Usage: python phase3b_interventions_runner_v1.py --results PATH --output NEW_PATH
Both paths must be absolute; output must not exist. Import/--help never trains.
Run only after independently reviewing the frozen finals and this separate script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from time import perf_counter

import numpy as np
import psutil
import torch
from torch.nn import functional as F

REPO = Path(r"C:\Users\aahern\Documents\GitHub\Toward-an-Artificial-Organism")
ATTESTATION_NAME = "phase3b_final_audit_v1.json"
SEEDS = tuple(range(1000, 1016))
BATCH = 128

# Import the pinned sources, not an ambient phase3b installation.
if not (REPO / "phase3b" / "execution.py").is_file():
    raise RuntimeError("pinned Phase III-B repository missing; STOP")
sys.path.insert(0, str(REPO))

from phase3b.audit import validate_raw_arrays, validate_state_digest  # noqa: E402
from phase3b.execution import assert_replay_equal, source_hashes  # noqa: E402
from phase3b.freeze import (verify_approval, verify_execution_freeze,  # noqa: E402
                            verify_preflight_snapshot)
from phase3b.interventions import (ExpandedWord, NoMessage, UnlimitedRead,  # noqa: E402
                                   first_divergence, intervene)
from phase3b.models import Arm, Trace, _token  # noqa: E402
from phase3b.resources import Meter, linear_meter, observed, python_peak  # noqa: E402
from phase3b.world import Episode, generate, loss_units  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fresh_json(path: Path, value: dict) -> str:
    raw = (json.dumps(value, sort_keys=True, allow_nan=False) + "\n").encode("utf-8")
    with path.open("xb") as stream:
        stream.write(raw)
    return hashlib.sha256(raw).hexdigest()


def fresh_npz(path: Path, arrays: dict[str, np.ndarray]) -> str:
    with path.open("xb") as stream:
        np.savez_compressed(stream, **arrays)
    return sha(path)


def verify_inputs(root: Path, attestation: Path) -> tuple[dict, dict, str, str]:
    """Check independently attested manifest and frozen sources before reservation."""
    if not root.is_dir() or not attestation.is_file():
        raise ValueError("final results or audit attestation missing; STOP")
    manifest_path = root / "manifest.json"
    manifest_hash = sha(manifest_path)
    manifest = json.loads(manifest_path.read_bytes())
    audit = json.loads(attestation.read_bytes())
    if (manifest.get("schema") != 2 or set(manifest.get("seeds", {})) !=
            {str(s) for s in SEEDS} or audit.get("schema") != 1
            or audit.get("independent_review") is not True
            or audit.get("audit") != "raw_and_checkpoint_replay_passed"
            or audit.get("manifest_sha256") != manifest_hash
            or audit.get("source_sha256") != manifest.get("source_sha256")
            or manifest.get("source_sha256") != source_hashes()):
        raise ValueError("missing, incomplete or unbound final audit/manifest/source; STOP")
    freeze_hash = manifest["freeze_sha256"]
    frozen = verify_execution_freeze(root / "execution_freeze.json", freeze_hash)
    if (frozen["preflight_snapshot_sha256"] != manifest["preflight_snapshot_sha256"]
            or frozen["contract"]["final_seeds"] != list(SEEDS)
            or frozen["contract"]["endpoint"]["episodes"] != 4096
            or frozen["contract"]["training"]["episodes"] != 8192
            or frozen["contract"]["training"]["updates"] != 256
            or frozen["source_sha256"] != manifest["source_sha256"]):
        raise ValueError("final freeze/manifest contract mismatch; STOP")
    verify_preflight_snapshot(root / "preflight_snapshot.json",
                              manifest["preflight_snapshot_sha256"])
    for phase in ("engineering", "final"):
        verify_approval({"freeze_path": str(root / "execution_freeze.json"),
                         "freeze_sha256": freeze_hash,
                         "approval_path": str(root / f"{phase}_approval.json"),
                         "approval_sha256": manifest[f"{phase}_approval_sha256"]}, phase)
    for seed in SEEDS:
        entry = manifest["seeds"][str(seed)].get("candidate")
        if (not isinstance(entry, dict) or
                entry.get("configuration", {}).get("width") is None or
                entry.get("training", {}).get("episodes") != 8192 or
                entry.get("training", {}).get("updates") != 256 or
                sha(root / f"{seed}_candidate.pt") != entry["checkpoint_file_sha256"] or
                sha(root / f"{seed}_candidate.npz") != entry["sha256"]):
            raise ValueError(f"seed {seed}: candidate final checkpoint/raw mismatch; STOP")
    return manifest, frozen, manifest_hash, sha(attestation)


def train_postfinal(candidate: Arm, diagnostic: NoMessage | ExpandedWord | UnlimitedRead,
                    seed: int) -> dict:
    """Exact execution.train_diagnostic optimizer/baseline loop, final-seed gate only.

    The original helper requires engineering authorization and seeds 0..3.
    This separately authorized secondary analysis uses the SAME original
    8192 histories of this final seed (not held-out data), with frozen encoders.
    """
    if seed not in SEEDS or candidate.name != "candidate":
        raise ValueError("undeclared final diagnostic seed/candidate; STOP")
    candidate.eval()
    for p in candidate.parameters():
        p.requires_grad_(False)
    diagnostic.train()
    torch.manual_seed(seed)
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
            losses = loss_units(trace.actions, ep.truth).float() / 50
            advantage = losses.detach() - baseline.T.unsqueeze(0)
            if trace.action_logp is None:
                raise AssertionError("diagnostic action log probabilities missing; STOP")
            objective = torch.stack([(advantage[:, :, i] * trace.action_logp[i]).mean()
                                     for i in range(3)]).mean()
            if trace.token_logp is not None:
                objective += (advantage.mean(-1) * trace.token_logp).mean()
            optimizer.zero_grad(set_to_none=True)
            objective.backward()
            torch.nn.utils.clip_grad_norm_(diagnostic.parameters(), 1)
            optimizer.step()
            baseline = 0.9 * baseline + 0.1 * losses.mean(0).T
    if isinstance(diagnostic, NoMessage):
        diagnostic.trained = True
    return {"episodes": 8192, "updates": 256, "batch": 32, "learning_rate": 0.001,
            "weight_decay": 0, "gradient_clip": 1, "training_contexts": [0, 1, 2],
            "draw_seed": "100000 + seed * 256 + update",
            "parameters_added": sum(p.numel() for p in diagnostic.parameters()),
            "optimizer_state_bytes": sum(v.numel() * v.element_size()
                                         for state in optimizer.state.values()
                                         for v in state.values() if isinstance(v, torch.Tensor)),
            "baseline_state_bytes": baseline.numel() * baseline.element_size(),
            "process_peak_working_set_bytes": psutil.Process(os.getpid()).memory_info().peak_wset,
            "process_peak_limitations": "process-lifetime high-water, not isolated model peak",
            "forward_linear_macs": meter.forward_macs,
            "backward_linear_macs": meter.backward_macs,
            "wall_seconds": perf_counter() - start, **observed(meter), **peak,
            "frozen_encoder_compute": "excluded from diagnostic meter; executed once per training batch",
            "read_bits": (diagnostic.bits if isinstance(diagnostic, ExpandedWord) else
                          candidate.width * 4 * 32 if isinstance(diagnostic, UnlimitedRead) else 0),
            "bandwidth": "out-of-band diagnostic; not intact 3-bit channel"}


def response_map(model: Arm, trace: Trace, local: torch.Tensor, kind: str,
                 diagnostic: NoMessage | ExpandedWord | UnlimitedRead | None = None,
                 cut: int | None = None) -> np.ndarray:
    """Exact conditional action for each local bit, per episode/tick/head."""
    batch, contexts, _ = local.shape
    result = torch.empty((batch, contexts, 3, 2), dtype=torch.uint8)
    for c in range(contexts):
        for i in range(3):
            for bit in (0, 1):
                value = torch.full((batch,), bit, dtype=torch.long)
                if kind == "I2" or (kind == "I6" and cut == i):
                    if not isinstance(diagnostic, NoMessage):
                        raise AssertionError("missing blank readout; STOP")
                    score = diagnostic.read(value, c, i)
                elif kind == "I4":
                    if not isinstance(diagnostic, ExpandedWord) or trace.word is None:
                        raise AssertionError("missing expanded word; STOP")
                    bits = ((trace.word[:, c, None] >>
                             torch.arange(diagnostic.bits - 1, -1, -1)) & 1).float()
                    ctx = F.one_hot(torch.full((batch,), c), 4).float()
                    score = diagnostic.heads[i](torch.cat((bits, ctx, value[:, None].float()), -1))
                elif kind == "I5":
                    if not isinstance(diagnostic, UnlimitedRead) or trace.states is None:
                        raise AssertionError("missing unlimited frozen state; STOP")
                    ctx = F.one_hot(torch.full((batch,), c), 4).float()
                    score = diagnostic.heads[i](torch.cat((trace.states.flatten(1), ctx,
                                                           value[:, None].float()), -1))
                else:
                    if trace.word is None:
                        raise AssertionError("missing candidate word; STOP")
                    score = model.read(trace.word[:, c], value, c, i)
                result[:, c, i, bit] = score.argmax(-1).to(torch.uint8)
    actual = result.gather(
        -1, local.to(torch.long).unsqueeze(-1)).squeeze(-1)
    if not torch.equal(actual, torch.stack(trace.actions, -1).to(torch.uint8)):
        raise AssertionError("local-bit response map disagrees with observed actions; STOP")
    return result.numpy()


def arrays_for(model: Arm, ep: Episode, intact: Trace, changed: Trace, kind: str,
               diagnostic: NoMessage | ExpandedWord | UnlimitedRead | None = None,
               cut: int | None = None) -> dict[str, np.ndarray]:
    actions = torch.stack(changed.actions, -1).numpy().astype(np.uint8)
    components = loss_units(changed.actions, ep.truth).numpy().astype(np.uint8)
    words = (changed.word.numpy().astype(np.uint32) if changed.word is not None else
             np.empty((0, 4), dtype=np.uint32))
    # New diagnostic alphabets have no meaningful integer word equality.
    comparison = (Trace(changed.logits, changed.actions) if kind in ("I4", "I5") else changed)
    reference = (Trace(intact.logits, intact.actions) if kind in ("I4", "I5") else intact)
    divergence = first_divergence(reference, comparison).numpy().astype(np.int16)
    return {"components": components, "actions": actions, "words": words,
            "first_divergence_tick": divergence,
            "response_local_bit_0_1": response_map(model, changed, ep.local, kind, diagnostic, cut)}


def synthetic_wiring_test() -> None:
    """Unscored tiny structural test; does not load finals, train or score losses."""
    torch.manual_seed(0)
    model = Arm("candidate", 2).eval()
    common = torch.zeros((2, 8), dtype=torch.long)
    local = torch.zeros((2, 4, 3), dtype=torch.long)
    with torch.no_grad():
        intact = model(common, local)
        assert_replay_equal(intact, intervene(model, common, local, "noop"))
        for port in range(4):
            assert_replay_equal(intact, intervene(model, common, local, "I7",
                                                  paired_common=common, port=port))
        response_map(model, intact, local, "intact")


def run(root: Path, output: Path, attestation: Path) -> None:
    if not root.is_absolute() or not output.is_absolute() or not attestation.is_absolute():
        raise ValueError("all paths must be absolute; STOP")
    if (output.resolve().is_relative_to(root.resolve()) or
            root.resolve().is_relative_to(output.resolve()) or
            output.resolve().is_relative_to(REPO.resolve()) or
            REPO.resolve().is_relative_to(output.resolve())):
        raise ValueError("diagnostic output must be outside frozen results and repository; STOP")
    manifest, frozen, manifest_hash, audit_hash = verify_inputs(root, attestation)
    output.mkdir(parents=False, exist_ok=False)
    runner_hash = sha(Path(__file__))
    report: dict = {"schema": 1, "phase": "post-final secondary unscored",
                    "manifest_sha256": manifest_hash, "audit_attestation_sha256": audit_hash,
                    "runner_sha256": runner_hash, "freeze_sha256": manifest["freeze_sha256"],
                    "source_sha256": frozen["source_sha256"],
                    "limitations": [
                        "No-message readout is a newly trained out-of-band blank, not an in-alphabet message or causal proof.",
                        "Expanded-word and unlimited-read heads are newly trained frozen-encoder diagnostics, not primary competitors or intact model improvements.",
                        "Diagnostic resource counters exclude frozen encoder work, unannotated kernels and physical memory traffic.",
                        "Audit attestation is hash-bound but not independently cryptographically signed by this runner.",
                        "Only contexts 0..2 enter diagnostic training; context 3 is held out. No diagnostic may tune primary endpoint, model selection or rivals."],
                    "divergence": "first differing word or action at ticks 8..11; I4/I5 use actions only because expanded/bypassed words are not comparable",
                    "controls": "noop exact replay; I1 same-address cells; I3 forced original address; I7 self-paired port, all fail closed",
                    "seeds": {}}
    try:
        for seed in SEEDS:
            info = manifest["seeds"][str(seed)]["candidate"]
            model = Arm("candidate", info["configuration"]["width"])
            model.load_state_dict(torch.load(root / f"{seed}_candidate.pt",
                                             map_location="cpu", weights_only=True))
            validate_state_digest(info, model)
            model.eval()
            torch.manual_seed(seed)
            no_message = NoMessage()
            expansions = {bits: ExpandedWord(model.width, bits) for bits in (4, 8, 16)}
            unlimited = UnlimitedRead(model.width)
            diagnostics = {"no_message": no_message, **{f"expanded_{bits}": module
                            for bits, module in expansions.items()}, "unlimited": unlimited}
            spends = {}
            checkpoints = {}
            for name, module in diagnostics.items():
                torch.manual_seed(seed)
                spends[name] = train_postfinal(model, module, seed)
                module.eval()
                path = output / f"{seed}_{name}.pt"
                with path.open("xb") as stream:
                    torch.save(module.state_dict(), stream)
                checkpoints[name] = sha(path)
            ep = generate(20_000 + seed, 4096)
            paired = generate(40_000 + seed, 4096)
            input_hash = fresh_npz(output / f"{seed}_inputs.npz", {
                "common": ep.common.numpy().astype(np.uint8),
                "local": ep.local.numpy().astype(np.uint8),
                "truth": ep.truth.numpy().astype(np.uint8),
                "paired_common": paired.common.numpy().astype(np.uint8)})
            with np.load(root / f"{seed}_candidate.npz", allow_pickle=False) as original:
                original_arrays = {key: original[key].copy() for key in
                                   ("components", "actions", "words")}
            validate_raw_arrays("candidate", ep, original_arrays)
            variants = ("intact", "noop", *(f"I1_address_{a}" for a in range(4)),
                        "I2", *(f"I3_address_{a}" for a in range(4)),
                        *(f"I4_bits_{b}" for b in (4, 8, 16)), "I5",
                        *(f"I6_head_{i}" for i in range(3)),
                        *(f"I7_port_{p}" for p in range(4)))
            rows = {name: {key: [] for key in ("components", "actions", "words",
                    "first_divergence_tick", "response_local_bit_0_1")} for name in variants}
            evaluation_start = perf_counter()
            with torch.no_grad():
                for offset in range(0, 4096, BATCH):
                    sub = Episode(ep.common[offset:offset+BATCH], ep.local[offset:offset+BATCH],
                                  ep.truth[offset:offset+BATCH])
                    intact = model(sub.common, sub.local)
                    changed: dict[str, tuple[Trace, NoMessage | ExpandedWord | UnlimitedRead | None,
                                              int | None]] = {"intact": (intact, None, None)}
                    changed["noop"] = (intervene(model, sub.common, sub.local, "noop"), None, None)
                    assert_replay_equal(intact, changed["noop"][0])
                    for address in range(4):
                        changed[f"I1_address_{address}"] = (
                            intervene(model, sub.common, sub.local, "I1", address=address), None, None)
                        changed[f"I3_address_{address}"] = (
                            intervene(model, sub.common, sub.local, "I3", address=address), None, None)
                        same = intact.address == address
                        i1 = changed[f"I1_address_{address}"][0]
                        if not torch.equal(i1.word[same], intact.word[same]) or any(
                                not torch.equal(a[same], b[same])
                                for a, b in zip(i1.actions, intact.actions)):
                            raise AssertionError("I1 identity-address negative control failed; STOP")
                    changed["I2"] = (intervene(model, sub.common, sub.local, "I2",
                                               diagnostic=no_message), no_message, None)
                    for bits, module in expansions.items():
                        changed[f"I4_bits_{bits}"] = (
                            intervene(model, sub.common, sub.local, "I4", expanded=module), module, None)
                    unlimited_trace = intervene(model, sub.common, sub.local, "I5",
                                                unlimited=unlimited)
                    unlimited_trace.states = intact.states
                    changed["I5"] = (unlimited_trace, unlimited, None)
                    for head in range(3):
                        changed[f"I6_head_{head}"] = (
                            intervene(model, sub.common, sub.local, "I6",
                                      consumer=head, diagnostic=no_message), no_message, head)
                    for port in range(4):
                        changed[f"I7_port_{port}"] = (
                            intervene(model, sub.common, sub.local, "I7", port=port,
                                      paired_common=paired.common[offset:offset+BATCH]), None, None)
                        assert_replay_equal(intact, intervene(
                            model, sub.common, sub.local, "I7", port=port, paired_common=sub.common))
                    identity = model.write(intact.states, 4, forced=intact.address)[0]
                    if not torch.equal(identity, intact.word):
                        raise AssertionError("I3 identity address changed original word; STOP")
                    expected = {key: value[offset:offset+BATCH] for key, value in
                                original_arrays.items()}
                    if not np.array_equal(expected["actions"], torch.stack(intact.actions, -1).numpy()):
                        raise AssertionError("candidate checkpoint does not replay original final; STOP")
                    if not np.array_equal(expected["words"], intact.word.numpy()):
                        raise AssertionError("candidate word does not replay original final; STOP")
                    for name, (trace, module, cut) in changed.items():
                        kind = name.split("_")[0]
                        data = arrays_for(model, sub, intact, trace, kind, module, cut)
                        for key, value in data.items():
                            rows[name][key].append(value)
                    if not np.array_equal(expected["components"], rows["intact"]["components"][-1]):
                        raise AssertionError("intact losses do not replay original final; STOP")
            results = {}
            intact_total = None
            for name, columns in rows.items():
                arrays = {key: np.concatenate(parts) for key, parts in columns.items()}
                if arrays["components"].shape != (4096, 4, 3):
                    raise AssertionError("incomplete diagnostic episodes; STOP")
                raw_hash = fresh_npz(output / f"{seed}_{name}.npz", arrays)
                total = int(arrays["components"][:, 3, :].sum(dtype=np.int64))
                if name == "intact":
                    intact_total = total
                results[name] = {"sha256": raw_hash, "heldout_context_total_units": total,
                                 "delta_vs_intact_units": total - intact_total,
                                 "evaluation_episodes": 4096, "evaluated_contexts": [0, 1, 2, 3],
                                 "evaluation_batch": BATCH,
                                 "first_divergence_count": int(np.count_nonzero(
                                     arrays["first_divergence_tick"] != -1))}
            report["seeds"][str(seed)] = {"input_sha256": input_hash,
                                           "evaluation_wall_seconds": perf_counter() - evaluation_start,
                                           "frozen_candidate_resources": info["resources"],
                                           "checkpoint_sha256": checkpoints,
                                           "training_spend": spends, "variants": results}
            fresh_json(output / f"{seed}_summary.json", report["seeds"][str(seed)])
        report["aggregate"] = {name: {
            "heldout_context_total_units": sum(report["seeds"][str(s)]["variants"][name][
                "heldout_context_total_units"] for s in SEEDS),
            "delta_vs_intact_units": sum(report["seeds"][str(s)]["variants"][name][
                "delta_vs_intact_units"] for s in SEEDS)}
            for name in report["seeds"][str(SEEDS[0])]["variants"]}
        fresh_json(output / "summary.json", report)
    except Exception as exc:
        fresh_json(output / "failure.json", {"error": repr(exc), "completed_seeds":
                   list(report["seeds"]), "runner_sha256": runner_hash,
                   "manifest_sha256": manifest_hash})
        raise


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, required=True, help="frozen finals directory")
    parser.add_argument("--output", type=Path, required=True, help="fresh external output directory")
    parser.add_argument("--attestation", type=Path, default=Path(__file__).parent / ATTESTATION_NAME)
    parser.add_argument("--synthetic-wiring-test", action="store_true",
                        help="tiny unscored test only; no finals or training")
    args = parser.parse_args()
    if args.synthetic_wiring_test:
        synthetic_wiring_test()
    else:
        run(args.results, args.output, args.attestation)

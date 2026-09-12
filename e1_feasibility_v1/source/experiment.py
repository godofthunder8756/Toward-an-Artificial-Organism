"""Run with python -m e1.experiment --out e1_results --config e1/frozen_config.json."""
import argparse
import copy
import csv
import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np

from .circuits import Circuit
from .config import BRANCHES, VARIANTS, Config
from .control import NeuralQ, TabularQ
from .environment import World


def dump_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def write_csv(path, rows):
    if not rows:
        return
    with Path(path).open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def source_hashes():
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(__file__).parent.glob('*.py'))}


def save_checkpoint(path, circuit, policy):
    """No pickle. Includes optimizer, replay, target net and physical-circuit data.

    Environment/noise state is represented by recorded world seed and trial index.
    Checkpoints are at episode boundaries. Replay sampling RNG state is in run.json
    only at seed completion; deterministic resumption mid-phase is not advertised.
    """
    state = {'mask': circuit.mask}
    state.update({f'circuit_{k}': v for k, v in circuit.p.items()})
    state['circuit_opt_t'] = np.array(circuit.opt.t)
    for kind in ('m', 'v'):
        state.update({f'circuit_opt_{kind}_{k}': v for k, v in getattr(circuit.opt, kind).items()})
    state['policy_updates'] = np.array(policy.updates)
    if isinstance(policy, NeuralQ):
        for kind, values in (('policy', policy.p), ('target', policy.target),
                             ('opt_m', policy.opt.m), ('opt_v', policy.opt.v)):
            state.update({f'{kind}_{k}': v for k, v in values.items()})
        state['opt_t'] = np.array(policy.opt.t)
        state['replay_cursor'] = np.array(policy.cursor)
        if policy.buf:
            for i, key in enumerate(('obs', 'action', 'reward', 'next_obs', 'done')):
                state[f'replay_{key}'] = np.array([b[i] for b in policy.buf])
    else:
        state['q_table'] = policy.q
    np.savez_compressed(path, **state)


def train_phase(cfg, circuit, policy, mode, budget, world_seed_base, replay_rng,
                meta, log):
    policy.begin_phase()
    actual = 0
    for episode, start in enumerate(range(0, budget, cfg.episode_length)):
        rounds = min(cfg.episode_length, budget - start)
        world = World(cfg, circuit, world_seed_base + episode, mode, rounds)
        for t in range(rounds):
            obs = world.observation()
            action = policy.act(obs, world.explore[t], world.actions[t], training=True)
            next_obs, reward, dead, row = world.step(action)
            objective = reward
            if policy.fixed_drive:
                objective -= cfg.drive_weight * (1 - row['q_used'])
            done = dead or t == rounds - 1
            policy.learn(obs, action, objective, next_obs, done, replay_rng)
            log.append({**meta, 'mode': mode, 'episode': episode,
                        'budget_index': start + t, 'world_seed': world_seed_base + episode,
                        **row, 'training_reward': objective})
            actual += 1
            if dead:
                break
    return actual


def evaluate(cfg, circuit, policy, mode, seed, variant, stage, rows, traces):
    # Identical, held-out worlds for every seed, variant and intervention. RNG
    # arrays are presampled and indexed by time, so actions cannot shift noise.
    for episode in range(cfg.eval_worlds):
        world_seed = 900_000_000 + episode
        world = World(cfg, circuit, world_seed, mode, cfg.eval_trials)
        values = []
        for t in range(cfg.eval_trials):
            obs = world.observation()
            action = policy.act(obs, world.explore[t], world.actions[t], training=False)
            _, _, dead, row = world.step(action)
            values.append(row)
            # Prespecified trace, never selected for a favorable outcome.
            if seed == cfg.seed_start and episode == 0:
                traces.append({'seed': seed, 'variant': variant, 'stage': stage,
                               'world_seed': world_seed, **row})
            if dead:
                break
        n = len(values)
        total = lambda key: sum(v[key] for v in values)
        rows.append({'seed': seed, 'variant': variant, 'stage': stage, 'mode': mode,
                     'world': episode, 'world_seed': world_seed, 'active_trials': n,
                     'planned_trials': cfg.eval_trials,
                     'precursor_count': total('precursor'),
                     'precursor_rate_active': total('precursor') / n,
                     'precursor_rate_unconditional': total('precursor') / cfg.eval_trials,
                     'recall_accuracy_active': total('success') / n,
                     'task_success_unconditional': total('success') / cfg.eval_trials,
                     'completion': int(world.alive and n == cfg.eval_trials),
                     'net_energy_per_planned_trial': total('net_energy') / cfg.eval_trials,
                     'mean_conductance': total('q_used') / n,
                     'mean_activity': total('neural_activity') / n,
                     'mean_material_used': total('precursor_used') / n,
                     'policy_updates': policy.updates})


def run_seed(cfg, seed, out):
    rng = np.random.default_rng(seed)
    circuit = Circuit(cfg, rng)
    naive = circuit.assay(np.random.default_rng(700_000_000))
    memory_log = circuit.train(rng)
    assay = {'seed': seed, 'naive_accuracy': naive,
             'intact_accuracy': circuit.assay(np.random.default_rng(700_000_000)),
             'lesion_accuracy': circuit.assay(np.random.default_rng(700_000_000), lesion=True),
             'restored_accuracy': circuit.assay(np.random.default_rng(700_000_000)),
             'degraded_accuracy': circuit.assay(np.random.default_rng(700_000_000), conductance=.10),
             'circuit_parameters': circuit.parameter_count,
             'recurrent_edges': int(circuit.mask.sum()),
             'memory_exploratory_transitions': cfg.memory_batches * cfg.memory_batch_size}
    # Baseline/frozen share EXACT pretraining, not separately favorable initializations.
    initial_neural = NeuralQ(cfg, np.random.default_rng(seed + 50_000))
    seed_dir = out / f'seed_{seed}'
    seed_dir.mkdir()
    write_csv(seed_dir / 'memory_training.csv', memory_log)
    all_rows, all_traces, all_log, budgets = [], [], [], []
    for variant in VARIANTS:
        policy = TabularQ(cfg) if variant == 'tabular_q' else copy.deepcopy(initial_neural)
        policy.fixed_drive = variant == 'fixed_drive_q'
        prng = np.random.default_rng(seed + 60_000)
        meta = {'seed': seed, 'variant': variant, 'phase': 'pre'}
        actual = train_phase(cfg, circuit, policy, 'pre', cfg.pre_trials,
                             seed * 100_000 + 1000, prng, meta, all_log)
        budgets.append({**meta, 'planned': cfg.pre_trials, 'actual': actual,
                        'policy_parameters': policy.parameter_count})
        evaluate(cfg, circuit, policy, 'pre', seed, variant, 'pre', all_rows, all_traces)
        save_checkpoint(seed_dir / f'{variant}_pre.npz', circuit, policy)
        if variant == 'frozen_neural_q':
            policy.frozen = True
        # Acute evaluation before adaptation measures actual damage at withdrawal.
        evaluate(cfg, circuit, policy, 'dependency', seed, variant, 'acute', all_rows, all_traces)
        meta = {'seed': seed, 'variant': variant, 'phase': 'acquisition'}
        actual = train_phase(cfg, circuit, policy, 'dependency', cfg.dependency_trials,
                             seed * 100_000 + 2000, prng, meta, all_log)
        budgets.append({**meta, 'planned': cfg.dependency_trials, 'actual': actual,
                        'policy_parameters': policy.parameter_count})
        evaluate(cfg, circuit, policy, 'dependency', seed, variant, 'acquired', all_rows, all_traces)
        save_checkpoint(seed_dir / f'{variant}_acquired.npz', circuit, policy)
        branch_root = copy.deepcopy(policy)
        for branch in BRANCHES:
            policy = copy.deepcopy(branch_root)
            # Equal replay RNG streams and worlds across counterfactual branches.
            brng = np.random.default_rng(seed + 70_000)
            meta = {'seed': seed, 'variant': variant, 'phase': branch}
            actual = train_phase(cfg, circuit, policy, branch, cfg.branch_trials,
                                 seed * 100_000 + 3000, brng, meta, all_log)
            budgets.append({**meta, 'planned': cfg.branch_trials, 'actual': actual,
                            'policy_parameters': policy.parameter_count})
            evaluate(cfg, circuit, policy, branch, seed, variant, branch, all_rows, all_traces)
            save_checkpoint(seed_dir / f'{variant}_{branch}.npz', circuit, policy)
    dump_json(seed_dir / 'assay.json', assay)
    write_csv(seed_dir / 'evaluation.csv', all_rows)
    write_csv(seed_dir / 'trace.csv', all_traces)
    write_csv(seed_dir / 'adaptation.csv', all_log)
    write_csv(seed_dir / 'budgets.csv', budgets)
    return assay, all_rows, budgets


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', required=True)
    parser.add_argument('--config')
    parser.add_argument('--feasibility', action='store_true')
    args = parser.parse_args()
    if args.config and args.feasibility:
        parser.error('Choose a frozen config or the engineering feasibility preset')
    cfg = Config(**json.loads(Path(args.config).read_text())) if args.config else Config()
    if args.feasibility:
        cfg = Config(seeds=2, seed_start=1, memory_batches=450,
                     pre_trials=512, dependency_trials=1024, branch_trials=1024,
                     eval_worlds=4, eval_trials=128)
    out = Path(args.out)
    if out.exists():
        parser.error('Output exists; use a new directory to preserve prior evidence')
    out.mkdir(parents=True)
    start = time.time()
    manifest = {'status': 'running', 'config': cfg.to_dict(), 'source_hashes': source_hashes(),
                'python': platform.python_version(), 'numpy': np.__version__,
                'started_utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                'engineering_feasibility': args.feasibility,
                'config_sha256': hashlib.sha256(json.dumps(cfg.to_dict(), sort_keys=True).encode()).hexdigest(),
                'external_preregistration': False}
    dump_json(out / 'run.json', manifest)
    assays, results, budgets = [], [], []
    for seed in range(cfg.seed_start, cfg.seed_start + cfg.seeds):
        assay, rows, budget = run_seed(cfg, seed, out)
        assays.append(assay)
        results.extend(rows)
        budgets.extend(budget)
        print(json.dumps({'seed': seed, 'intact': assay['intact_accuracy'],
                          'lesion': assay['lesion_accuracy'],
                          'elapsed_seconds': round(time.time() - start, 1)}), flush=True)
    write_csv(out / 'assays.csv', assays)
    write_csv(out / 'evaluation.csv', results)
    write_csv(out / 'budgets.csv', budgets)
    manifest.update(status='completed', wall_seconds=time.time() - start,
                    final_source_hashes=source_hashes())
    assert manifest['source_hashes'] == manifest['final_source_hashes'], 'Source changed during run'
    dump_json(out / 'run.json', manifest)


if __name__ == '__main__':
    main()

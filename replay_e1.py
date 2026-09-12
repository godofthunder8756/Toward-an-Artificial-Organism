"""Replay a saved E1 policy without training or pickle loading.

python replay_e1.py --results e1_results --seed 100 --variant neural_q \
  --stage acquired --world 0 --out replay.csv
"""
import argparse
import csv
import json
from pathlib import Path
import numpy as np
from e1.circuits import Circuit
from e1.config import Config, VARIANTS
from e1.control import NeuralQ, TabularQ
from e1.environment import World


def restore(root, seed, variant, stage):
    cfg = Config(**json.loads((root / 'run.json').read_text())['config'])
    checkpoint_stage = 'pre' if stage == 'acute' else stage
    data = np.load(root / f'seed_{seed}' / f'{variant}_{checkpoint_stage}.npz', allow_pickle=False)
    circuit = Circuit(cfg, np.random.default_rng(0))
    circuit.mask = data['mask'].copy()
    for k in circuit.p:
        circuit.p[k] = data[f'circuit_{k}'].copy()
    if variant == 'tabular_q':
        policy = TabularQ(cfg)
        policy.q = data['q_table'].copy()
    else:
        policy = NeuralQ(cfg, np.random.default_rng(0), frozen=variant == 'frozen_neural_q',
                         fixed_drive=variant == 'fixed_drive_q')
        for k in policy.p:
            policy.p[k] = data[f'policy_{k}'].copy()
        # Evaluation only: target, optimizer, and replay have no causal role.
    data.close()
    return cfg, circuit, policy


def replay(root, seed, variant, stage, world_number=0):
    cfg, circuit, policy = restore(root, seed, variant, stage)
    mode = 'dependency' if stage in ('acute', 'acquired') else stage
    world_seed = 900_000_000 + world_number
    world = World(cfg, circuit, world_seed, mode, cfg.eval_trials)
    rows = []
    for t in range(cfg.eval_trials):
        action = policy.act(world.observation(), world.explore[t], world.actions[t], False)
        _, _, dead, row = world.step(action)
        rows.append(row)
        if dead:
            break
    return rows


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--results', type=Path, required=True)
    p.add_argument('--seed', type=int, required=True)
    p.add_argument('--variant', choices=VARIANTS, default='neural_q')
    p.add_argument('--stage', choices=('pre', 'acute', 'acquired', 'dependency', 'rescue', 'sham', 'lost_usefulness'), default='acquired')
    p.add_argument('--world', type=int, default=0)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    if args.out.exists():
        p.error('Output already exists; choose a new file')
    rows = replay(args.results, args.seed, args.variant, args.stage, args.world)
    with args.out.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(json.dumps({'active_trials': len(rows),
                      'precursor_choices': sum(r['precursor'] for r in rows),
                      'correct_recalls': sum(r['success'] for r in rows)}))


if __name__ == '__main__':
    main()

"""E0: resource-dependent recurrent control, not a consciousness experiment.

Run: python pilot.py --out results
Requires NumPy. No text data, language model, or network access.
All units are dimensionless simulator units; hardware energy is not modeled.
Evolution explicitly maximizes episode persistence. No within-life learning.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np

H = 6
DIM = 5 * H + H * H + H + H * 4 + 4
ACTIONS = ['gather_energy', 'gather_material', 'repair', 'rest']


def unpack(theta):
    p = len(theta)
    k = 0
    result = []
    for shape in [(5, H), (H, H), (H,), (H, 4), (4,)]:
        n = int(np.prod(shape))
        result.append(theta[:, k:k + n].reshape((p,) + shape))
        k += n
    assert k == DIM
    return result


def conditions(seed, episodes, steps):
    """Common random numbers; all controllers receive the same conditions."""
    rng = np.random.default_rng(seed)
    return {
        'initial': rng.uniform(.42, .9, size=(episodes, 3)),
        'yield_e': rng.uniform(.13, .25, size=(steps // 30 + 1, episodes)),
        'yield_m': rng.uniform(.12, .23, size=(steps // 30 + 1, episodes)),
    }


def neural_step(weights, hidden, obs, quality, coupling=True):
    wi, wr, bh, wo, bo = weights
    proposed = np.tanh(np.einsum('pei,pih->peh', obs, wi)
                       + np.einsum('pei,pih->peh', hidden, wr)
                       + bh[:, None, :])
    # Differential conductance makes quality act on the recurrent substrate.
    # This is a designed soft gain, not neuron construction or physical damage.
    susceptibility = np.linspace(.2, 1., H)
    gain = (1 - (1 - quality[..., None]) * susceptibility) if coupling else 1.
    updated = gain * (.35 * hidden + .65 * proposed)
    logits = np.einsum('peh,pha->pea', updated, wo) + bo[:, None, :]
    return updated, logits.argmax(-1)


def rollout(theta, env, steps, intervention='none', scenario='normal',
            controller='neural', collect_trace=False):
    p = len(theta)
    initial = env['initial']
    episodes = len(initial)
    energy, material, quality = [np.broadcast_to(initial[:, i], (p, episodes)).copy()
                                 for i in range(3)]
    hidden = np.zeros((p, episodes, H))
    weights = unpack(theta)
    alive = np.ones((p, episodes), dtype=bool)
    lifetime = np.zeros((p, episodes))
    action_counts = np.zeros((p, episodes, 4), dtype=int)
    activity_sum = np.zeros((p, episodes))
    quality_sum = np.zeros((p, episodes))
    trace = []
    for t in range(steps):
        ey = np.broadcast_to(env['yield_e'][t // 30], (p, episodes)).copy()
        my = np.broadcast_to(env['yield_m'][t // 30], (p, episodes))
        if scenario == 'scarcity' and t >= 200:
            ey *= .65
        if scenario == 'quality_shock' and t == 200:
            quality *= .55
        if controller == 'neural':
            obs = np.stack([energy, material, quality, ey, my], axis=-1)
            if intervention == 'telemetry_clamped':
                obs[..., :3] = .7
            if intervention == 'reset_hidden':
                hidden[:] = 0
            hidden, action = neural_step(weights, hidden, 2 * obs - 1, quality,
                                         coupling=intervention != 'gain_disconnected')
            activity = np.abs(hidden).mean(-1)
        elif controller == 'reflex':
            # Handwritten positive control; not learned or conscious.
            action = np.where(energy < .45, 0,
                              np.where(quality < .65,
                                       np.where(material >= .12, 2, 1),
                                       np.where(material < .35, 1, 3)))
            # Charge the same nominal activity cost to avoid a free baseline.
            # This is not a parameter/compute-matched architectural control.
            activity = np.full_like(energy, .5)
        else:
            raise ValueError(controller)

        before_energy = energy.copy()
        before_material = material.copy()
        before_quality = quality.copy()
        lifetime += alive
        activity_sum += alive * activity
        quality_sum += alive * quality
        for a in range(4):
            action_counts[..., a] += alive & (action == a)
        cost = .018 + .004 * activity + .009 * (action != 3)
        energy -= alive * cost
        energy += alive * (action == 0) * ey
        material += alive * (action == 1) * my
        repair = np.minimum(material, .12) * (action == 2) * alive
        material -= repair
        energy -= .35 * repair
        quality -= alive * (.003 + .006 * activity)
        if intervention != 'sham_repair':
            quality += .8 * repair
        energy = np.clip(energy, 0, 1)
        material = np.clip(material, 0, 1)
        quality = np.clip(quality, 0, 1)
        if collect_trace:
            trace.append({'step': t, 'energy_before': float(before_energy[0, 0]),
                          'material_before': float(before_material[0, 0]),
                          'quality_before': float(before_quality[0, 0]),
                          'action': ACTIONS[int(action[0, 0])],
                          'neural_activity': float(activity[0, 0]),
                          'energy_after': float(energy[0, 0]),
                          'quality_after': float(quality[0, 0]),
                          'active_before': bool(alive[0, 0])})
        alive &= (energy > .02) & (quality > .12)
        hidden *= alive[..., None]
        if not alive.any():
            break
    return {'lifetime': lifetime, 'survived': alive,
            'activity': activity_sum / np.maximum(lifetime, 1),
            'quality': quality_sum / np.maximum(lifetime, 1),
            'actions': action_counts, 'trace': trace}


def train(seed, generations, population, steps, episodes):
    rng = np.random.default_rng(seed)
    mean, sd = np.zeros(DIM), np.full(DIM, .7)
    fixed_validation = conditions(80_000 + seed, episodes * 2, steps)
    champion, champion_score = mean.copy(), -1.
    history = []
    for g in range(generations):
        theta = rng.normal(mean, sd, (population, DIM))
        theta[0] = champion
        env = conditions(seed * 10_000 + g, episodes, steps)
        output = rollout(theta, env, steps)
        score = output['lifetime'].mean(-1)  # the explicit selection objective
        elite = theta[np.argsort(score)[-max(6, population // 8):]]
        mean = .3 * mean + .7 * elite.mean(0)
        sd = np.maximum(.08, .5 * sd + .5 * elite.std(0))
        candidates = np.stack([theta[score.argmax()], mean, champion])
        validation = rollout(candidates, fixed_validation, steps)['lifetime'].mean(-1)
        ix = validation.argmax()
        champion, champion_score = candidates[ix].copy(), float(validation[ix])
        history.append({'seed': seed, 'generation': g,
                        'training_best_steps': float(score.max()),
                        'validation_champion_steps': champion_score})
    return champion, history


def check_mechanisms():
    """Meaningful invariants for the scientific intervention implementation."""
    theta = np.random.default_rng(992).normal(0, .5, (1, DIM))
    weights = unpack(theta)
    hidden = np.full((1, 1, H), .3)
    obs = np.full((1, 1, 5), .2)
    low, high = np.array([[.2]]), np.array([[.9]])
    hl, _ = neural_step(weights, hidden, obs, low, True)
    hh, _ = neural_step(weights, hidden, obs, high, True)
    assert not np.allclose(hl, hh), 'Quality must affect neural state'
    dl, _ = neural_step(weights, hidden, obs, low, False)
    dh, _ = neural_step(weights, hidden, obs, high, False)
    assert np.allclose(dl, dh), 'Disconnect must remove quality gain effect'
    env = conditions(93, 2, 100)
    r1 = rollout(theta, env, 100)
    r2 = rollout(theta, env, 100)
    assert np.array_equal(r1['lifetime'], r2['lifetime'])
    assert np.array_equal(r1['actions'], r2['actions'])
    assert (r1['actions'].sum(-1) == r1['lifetime']).all()
    # Force repair: all weights zero, repair output bias dominates.
    repair_theta = np.zeros((1, DIM))
    repair_theta[0, -2] = 2
    normal = rollout(repair_theta, env, 1, collect_trace=True)['trace'][0]
    sham = rollout(repair_theta, env, 1, intervention='sham_repair', collect_trace=True)['trace'][0]
    assert normal['quality_after'] > normal['quality_before']
    assert sham['quality_after'] < sham['quality_before']
    assert np.isclose(normal['energy_after'], sham['energy_after'])
    return ['resource changes neural dynamics', 'gain disconnection isolates that link',
            'paired rollouts deterministic', 'action accounting matches active ticks',
            'repair restores quality; sham consumes same resources without restoration']


def write_csv(path, rows):
    with path.open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=Path('results'))
    parser.add_argument('--seeds', type=int, default=6)
    parser.add_argument('--generations', type=int, default=60)
    parser.add_argument('--population', type=int, default=64)
    parser.add_argument('--train-steps', type=int, default=240)
    parser.add_argument('--eval-steps', type=int, default=600)
    parser.add_argument('--train-episodes', type=int, default=8)
    parser.add_argument('--eval-episodes', type=int, default=64)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    start = time.time()
    checks = check_mechanisms()
    champions, histories = [], []
    for seed in range(args.seeds):
        champion, history = train(seed, args.generations, args.population,
                                  args.train_steps, args.train_episodes)
        champions.append(champion)
        histories.extend(history)
        print(json.dumps({'seed': seed, 'validation_steps': history[-1]['validation_champion_steps'],
                          'elapsed_seconds': round(time.time() - start, 2)}), flush=True)
    champions = np.stack(champions)
    np.savez_compressed(args.out / 'controllers.npz', weights=champions)
    random_weights = np.random.default_rng(999_888).normal(0, .7, champions.shape)
    env = conditions(900_000, args.eval_episodes, args.eval_steps)
    rows, trace = [], []
    for scenario in ['normal', 'scarcity', 'quality_shock']:
        for name, theta, intervention, controller in [
            ('evolved', champions, 'none', 'neural'),
            ('telemetry_clamped', champions, 'telemetry_clamped', 'neural'),
            ('reset_hidden', champions, 'reset_hidden', 'neural'),
            ('gain_disconnected', champions, 'gain_disconnected', 'neural'),
            ('sham_repair', champions, 'sham_repair', 'neural'),
            ('untrained', random_weights, 'none', 'neural'),
            ('reflex', np.zeros((1, DIM)), 'none', 'reflex'),
        ]:
            output = rollout(theta, env, args.eval_steps, intervention, scenario, controller,
                             collect_trace=name == 'evolved' and scenario == 'normal')
            if output['trace']:
                trace = output['trace']
            for seed in range(len(theta)):
                for episode in range(args.eval_episodes):
                    row = {'scenario': scenario, 'condition': name, 'seed': seed, 'episode': episode,
                           'active_steps': int(output['lifetime'][seed, episode]),
                           'completed_horizon': int(output['survived'][seed, episode]),
                           'mean_activity': float(output['activity'][seed, episode]),
                           'mean_quality': float(output['quality'][seed, episode])}
                    row.update({a: int(output['actions'][seed, episode, i]) for i, a in enumerate(ACTIONS)})
                    rows.append(row)
    summary = []
    for scenario in ['normal', 'scarcity', 'quality_shock']:
        for condition in dict.fromkeys(r['condition'] for r in rows):
            subset = [r for r in rows if r['scenario'] == scenario and r['condition'] == condition]
            seed_means = [np.mean([r['active_steps'] for r in subset if r['seed'] == s])
                          for s in sorted(set(r['seed'] for r in subset))]
            summary.append({'scenario': scenario, 'condition': condition,
                            'mean_active_steps': float(np.mean(seed_means)),
                            'seed_sd': float(np.std(seed_means, ddof=1)) if len(seed_means) > 1 else None,
                            'horizon_completion_fraction': float(np.mean([r['completed_horizon'] for r in subset])),
                            'independent_training_seeds': len(seed_means) if condition not in ['reflex', 'untrained'] else 0,
                            'seed_mean_steps': list(map(float, seed_means))})
    write_csv(args.out / 'episodes.csv', rows)
    write_csv(args.out / 'training.csv', histories)
    write_csv(args.out / 'trace_seed0_episode0.csv', trace)
    (args.out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    config = vars(args).copy()
    config['out'] = str(config['out'])
    config.update({'python': platform.python_version(), 'numpy': np.__version__,
                   'parameters': DIM, 'hidden_units': H, 'mechanism_checks': checks,
                   'wall_seconds': time.time() - start,
                   'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   'protocol': 'Exploratory E0; no consciousness, craving, or novelty test.',
                   'selection': 'CEM, mean active ticks, fixed validation panel; weights frozen in evaluation.',
                   'evaluation_seed': 900_000, 'evaluation_used_for_selection': False})
    (args.out / 'run.json').write_text(json.dumps(config, indent=2) + '\n')
    print(json.dumps({'complete': True, 'wall_seconds': round(config['wall_seconds'], 2),
                      'summary': summary}), flush=True)


if __name__ == '__main__':
    main()

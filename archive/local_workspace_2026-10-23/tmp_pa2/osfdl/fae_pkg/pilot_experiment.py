"""Exploratory AffectWorld mechanism pilot. No claim of subjective feeling.
Run using research-env Python: pilot_experiment.py --repo PATH --out NEW_DIR.
Upstream remains unmodified; imports its documented dependency patch.
"""
import argparse
import copy
import csv
import hashlib
import json
import os
from pathlib import Path
import sys
import time

ARGS = argparse.ArgumentParser()
ARGS.add_argument('--repo', type=Path, required=True)
ARGS.add_argument('--out', type=Path, required=True)
ARGS.add_argument('--validate-only', action='store_true')
args = ARGS.parse_args()
args.out.mkdir(parents=True, exist_ok=False)
os.environ['JAX_PLATFORMS'] = 'cpu'
os.environ['MPLCONFIGDIR'] = str((args.out / 'plot-cache').resolve())
sys.path.insert(0, str(args.repo.resolve()))
import reproduce  # upstream compatibility fix, before pymdp imports
import numpy as np
import jax.numpy as jnp
from aif_paper1.affectworld.affect_world_env import AffectWorldEnv
from aif_paper1.affectworld.body import BodyProcess
from aif_paper1.affectworld.configs import BodyConfig
from aif_paper1.affectworld.regimes import apply_simple_regime
from aif_paper1.affectworld.canonical_step import run_canonical_step
from aif_paper1.affectworld.intero_precision import channel_precisions_np
from aif_paper1.agents.likelihood_precision_selective_attention import ExternalKappaAgent

CONFIG = dict(stage='exploratory pilot, not preregistered', seeds=[0, 1, 2, 3],
              layouts=['km_easy_00', 'km_easy_01'], steps=40, horizon=1,
              arms=['uniform', 'coupled', 'sensing', 'confidence', 'preference'],
              conditions=['clean', 'bias', 'noise'], bias_channel=1,
              bias_magnitude=2, bias_start=5, bias_stop=15,
              preference_foreground_weight=2.0,
              upstream_commit='2657a982c5ae59a0f0fa9cdf941f82a71eba3cd9')
BODY = BodyConfig(intero_budget_mode='soft', intero_budget_total=2.6,
                  max_sleepdebt=1, inc_sleepdebt=0, lethal_sleep=False)
KW = dict(planning_horizon=1, planner='efe', policy_mode='full',
          unknown_model=True, unknown_model_init_concentration=0.1,
          unknown_model_learning_rate=1.0, unknown_model_learn_resource=True,
          unknown_model_learn_intero=False, unknown_model_update_online=True,
          dynamic_resource_preferences=False, habit_mode='none', jit_inference=True)

def serial(x):
    if isinstance(x, np.ndarray): return x.tolist()
    if isinstance(x, np.generic): return x.item()
    raise TypeError(type(x).__name__)

def dump(path, data):
    path.write_text(json.dumps(data, indent=2, default=serial), encoding='utf-8')

def precision(body, attended):
    return channel_precisions_np(attended=-1 if attended is None else int(attended),
        n_channels=4, base_precision=body.INTERO_BASE_PRECISION,
        att_precision=body.INTERO_ATT_PRECISION, mode='soft',
        bg_floor=0.05, total_budget=2.6)

class PilotBody(BodyProcess):
    """Same sensor marginals as upstream; fixed draws allow paired disturbances.

    Sensor perturbations do not change the physiological transition function.
    Random +/-2 noise is zero-mean BEFORE clipping, not necessarily afterward.
    """
    def begin(self, seed, arm, condition):
        self.arm, self.condition, self.sample_index = arm, condition, 0
        self.draws = np.random.default_rng(seed + 1000).random((CONFIG['steps'] + 2, 9))
        self.rng = np.random.default_rng(seed + 2000)

    def sample_interoception(self, attended, **kwargs):
        t = self.sample_index
        selected = attended if self.arm in ('coupled', 'sensing') else None
        p = precision(self, selected)
        truth = self.get_typeII_levels()
        draws = self.draws[t]
        # A fixed number of random draws is consumed regardless of correctness.
        wrong_rank = np.floor(draws[4:8] * 5).astype(int)
        wrong = wrong_rank + (wrong_rank >= truth)
        raw = np.where(draws[:4] < p, truth, wrong).astype(np.int8)
        received = raw.copy()
        delta = 0
        if CONFIG['bias_start'] <= t < CONFIG['bias_stop']:
            if self.condition == 'bias': delta = 2
            if self.condition == 'noise': delta = 2 if draws[8] < .5 else -2
            received[1] = np.clip(int(raw[1]) + delta, 0, 5)
        self.sensor_record = dict(sample_t=t, sensor_precision=p.copy(),
            raw_sensor=raw.copy(), received_sensor=received.copy(),
            intended_delta=delta, realized_delta=int(received[1]) - int(raw[1]))
        self.sample_index += 1
        return received

class PilotAgent(ExternalKappaAgent):
    def __init__(self, env, body, arm):
        self.arm = arm
        super().__init__(env, body, kappa_modulates_inference=arm in ('coupled', 'sensing', 'confidence'),
                         kappa_modulates_planning=arm in ('coupled', 'confidence'), **KW)

    def _planner_runtime_overrides(self, **kwargs):
        a, c, pa, e, info = super()._planner_runtime_overrides(**kwargs)
        self.preference_weights = np.ones(4)
        if self.arm == 'preference' and 0 <= self.current_kappa < 4:
            # Preserve sum of modality weights, not equivalence to sensory precision.
            self.preference_weights[:] = 2.0 / 3.0
            self.preference_weights[self.current_kappa] = 2.0
            for i, weight in enumerate(self.preference_weights):
                c[3+i] = jnp.asarray(c[3+i] * weight)
        return a, c, pa, e, info

def build(layout, arm):
    env = AffectWorldEnv(width=6, height=6, seed=0)
    apply_simple_regime(env, food_positions=layout['food_positions'],
        water_positions=layout['water_positions'], sleep_positions=layout['sleep_positions'],
        start_pos=layout['start_pos'])
    body = PilotBody(config=BODY)
    agent = PilotAgent(env, body, arm)
    initial = copy.deepcopy((agent.A, agent._pA, agent.pymdp_agent.A))
    return env, body, agent, initial

def episode(bundle, layout, seed, condition):
    env, body, agent, initial = bundle
    # reset() alone retains learned likelihoods; restore them explicitly.
    agent.A, agent._pA, pymdp_a = copy.deepcopy(initial)
    for m, a in enumerate(pymdp_a): agent.pymdp_agent.A[m] = a
    env.rng = np.random.default_rng(seed + 3000)
    obs = env.reset(pos=layout['start_pos'], ctx=0)
    body.reset()
    body.begin(seed, agent.arm, condition)
    agent.reset()
    sensed = body.sample_interoception(None)
    records = []
    for t in range(CONFIG['steps']):
        sensor = copy.deepcopy(body.sensor_record)
        obs, sensed, rec = run_canonical_step(env=env, body=body, agent=agent,
                                             obs=obs, typeII_obs=sensed)
        true = np.array(rec['typeI_levels_t'])
        need = np.array([1-true[0]/15, 1-true[1]/15, true[2], 1-true[3]/10])
        q = agent._latest_qs_for_learning(agent.qs)
        estimated = np.array([np.dot(np.arange(len(q[i])), q[i]) for i in (2, 3, 4, 5)])
        estimate_error = float(np.mean(np.abs((estimated - true) / [15, 15, 1, 10])))
        chosen = int(agent.last_selected_kappa)
        mispriority = float(need[chosen] < max(need) - 1e-6)
        after = np.array(rec['typeI_levels_t1'])
        # Mean nutrient/hydration deficit: principal active resources in easy layouts.
        loss = float(np.mean(1 - after[:2] / [15, 15]))
        qp = np.asarray(agent.last_q_pi)
        entropy = float(-np.sum(qp * np.log(np.maximum(qp, 1e-30))))
        records.append(dict(t=t, **sensor, truth=true, truth_after=after,
            inferred_levels=estimated, estimation_mae=estimate_error,
            selected_need=chosen, mispriority=mispriority, regulation_loss=loss,
            preference_weights=agent.preference_weights.copy(), policy_entropy=entropy,
            move=rec['move'], interact=rec['interact'], pos=rec['pos_t'],
            policy=qp, terminated=bool(rec['env_done'] or rec['body_done'])))
        if records[-1]['terminated']: break
    survived = not records[-1]['terminated']
    # Fill remaining steps with maximum loss so early failure cannot look beneficial.
    loss = (sum(r['regulation_loss'] for r in records) + CONFIG['steps']-len(records))/CONFIG['steps']
    summary = dict(arm=agent.arm, condition=condition, seed=seed,
        layout=layout['layout_id'], steps=len(records), survived=int(survived),
        regulation_loss=loss, estimation_mae=float(np.mean([r['estimation_mae'] for r in records])),
        mispriority=float(np.mean([r['mispriority'] for r in records])),
        policy_entropy=float(np.mean([r['policy_entropy'] for r in records])))
    return summary, records

def validate(layout):
    checks = []
    # Verify the causal intervention leaves actual body state untouched and only
    # changes the intended observation at the intended time.
    bodies = []
    for condition in CONFIG['conditions']:
        b = PilotBody(config=BODY); b.begin(17, 'coupled', condition); bodies.append(b)
    for t in range(18):
        observations = [b.sample_interoception(1) for b in bodies]
        assert all(np.array_equal(b.get_typeII_levels(), bodies[0].get_typeII_levels()) for b in bodies)
        assert all(np.array_equal(o[[0,2,3]], observations[0][[0,2,3]]) for o in observations)
        if not 5 <= t < 15: assert all(np.array_equal(o, observations[0]) for o in observations)
    checks.append('Sensor interventions leave physiology and other channels unchanged; timing verified.')
    for arm in CONFIG['arms']:
        bundle = build(layout, arm)
        env, body, agent, initial = bundle
        body.begin(4, arm, 'clean')
        body.sample_interoception(1)
        expected_p = precision(body, 1 if arm in ('coupled', 'sensing') else None)
        assert np.allclose(body.sensor_record['sensor_precision'], expected_p)
        agent.current_kappa = 1
        a, c, _, _, _ = agent._planner_runtime_overrides()
        assert all(np.array_equal(np.asarray(a[m]), agent.A[m]) for m in range(7))
        changes = [not np.allclose(np.asarray(c[m]), agent.C[m]) for m in range(7)]
        assert changes == ([False]*3+[True]*4 if arm == 'preference' else [False]*7)
        assert agent.kappa_modulates_inference == (arm in ('coupled','sensing','confidence'))
        assert agent.kappa_modulates_planning == (arm in ('coupled','confidence'))
        checks.append(f'{arm}: sensor, inference, planning and preference switches verified.')
        if arm == 'coupled':
            first = episode(bundle, layout, 99, 'bias')
            episode(bundle, layout, 15, 'noise')
            repeat = episode(bundle, layout, 99, 'bias')
            assert json.dumps(first, default=serial) == json.dumps(repeat, default=serial)
            checks.append('Seeded trajectory repeats exactly after a different episode; learning reset verified.')
    dump(args.out/'validation.json', checks)
    print('VALIDATION PASSED', flush=True)

def main():
    import subprocess
    git = ['git', '-c', f'safe.directory={args.repo.resolve().as_posix()}']
    commit = subprocess.check_output(git+['rev-parse','HEAD'], cwd=args.repo, text=True).strip()
    assert commit == CONFIG['upstream_commit']
    assert not subprocess.check_output(git+['status','--porcelain'], cwd=args.repo, text=True).strip()
    layouts = json.loads((args.repo/'configs/known_model_layout_bank.json').read_text())['layouts']
    layouts = [l for l in layouts if l['layout_id'] in CONFIG['layouts']]
    dump(args.out/'config.json', CONFIG)
    validate(layouts[0])
    if args.validate_only: return
    rows = []
    start = time.perf_counter()
    with (args.out/'trajectories.jsonl').open('w', encoding='utf-8') as raw:
        for layout in layouts:
            for arm in CONFIG['arms']:
                bundle = build(layout, arm)
                for seed in CONFIG['seeds']:
                    for condition in CONFIG['conditions']:
                        summary, records = episode(bundle, layout, seed, condition)
                        rows.append(summary)
                        raw.write(json.dumps(dict(summary=summary, records=records), default=serial)+'\n')
                        raw.flush()
                        with (args.out/'episodes.csv').open('w', newline='', encoding='utf-8') as f:
                            writer=csv.DictWriter(f, fieldnames=list(summary)); writer.writeheader(); writer.writerows(rows)
                        print(f"{len(rows)}/120 {layout['layout_id']} {arm} seed={seed} {condition} steps={summary['steps']} loss={summary['regulation_loss']:.3f}", flush=True)
    versions = subprocess.check_output([sys.executable,'-m','pip','freeze'], text=True)
    (args.out/'dependencies.txt').write_text('\n'.join(x for x in versions.splitlines() if not x.startswith(('-e ', '# Editable'))), encoding='utf-8')
    dump(args.out/'completion.json', dict(episodes=len(rows), elapsed_seconds=time.perf_counter()-start,
        script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        raw_sha256=hashlib.sha256((args.out/'trajectories.jsonl').read_bytes()).hexdigest()))

if __name__ == '__main__': main()

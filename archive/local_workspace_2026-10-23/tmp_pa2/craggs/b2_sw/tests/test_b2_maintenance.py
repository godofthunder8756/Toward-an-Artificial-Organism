from __future__ import annotations
from pathlib import Path
import yaml
import numpy as np

from toe.environments.maintenance_network import MaintenanceNetworkEnvironment
from toe.agents.maintenance import MaintenanceAgent

ROOT=Path(__file__).resolve().parents[1]

def load(rel):
    with (ROOT/rel).open() as f: return yaml.safe_load(f)

def rollout(env_cfg, agent_cfg, seed=311221001):
    env=MaintenanceNetworkEnvironment(env_cfg); agent=MaintenanceAgent(agent_cfg)
    obs=env.reset(seed); agent.reset(seed); states=[]
    for _ in range(env_cfg['horizon']):
        result=env.step(agent.act(obs)); obs=result.observation; states.append(result.info)
    return states

def test_deterministic_matched_disturbance():
    e=load('configs/environments/b2/maintenance_medium_v1.yaml')
    a=load('configs/architectures/b2/reciprocal_v1.yaml')
    x=rollout(e,a); y=rollout(e,a)
    assert x==y

def test_budget_never_exceeded():
    e=load('configs/environments/b2/maintenance_high_v1.yaml')
    for name in ['external','feedforward','reciprocal','bruteforce']:
        a=load(f'configs/architectures/b2/{name}_v1.yaml')
        xs=rollout(e,a)
        assert max(s['maintenance_total'] for s in xs) <= float(a['maintenance_budget']) + 1e-12

def test_passive_has_no_maintenance():
    e=load('configs/environments/b2/maintenance_low_v1.yaml'); a=load('configs/architectures/b2/passive_v1.yaml')
    xs=rollout(e,a)
    assert all(s['maintenance_total']==0.0 for s in xs)

def test_support_withdrawal_disables_external_support():
    e=load('configs/environments/b2/maintenance_external_withdraw_v1.yaml'); a=load('configs/architectures/b2/external_v1.yaml')
    xs=rollout(e,a)
    assert all(sum(s['m_ext'])==0.0 for s in xs[200:])

def test_ablation_holds_c1_at_zero():
    e=load('configs/environments/b2/maintenance_ablate_c1_v1.yaml'); a=load('configs/architectures/b2/reciprocal_v1.yaml')
    xs=rollout(e,a)
    assert all(abs(s['q'][0]) < 1e-15 for s in xs[200:])

def test_specific_rescue_targets_c2():
    e=load('configs/environments/b2/maintenance_ablate_c1_specific_rescue_v1.yaml'); a=load('configs/architectures/b2/reciprocal_v1.yaml')
    xs=rollout(e,a)
    assert xs[-1]['q'][1] > 0.9

def test_irrelevant_rescue_does_not_restore_c2():
    e=load('configs/environments/b2/maintenance_ablate_c1_irrelevant_rescue_v1.yaml'); a=load('configs/architectures/b2/reciprocal_v1.yaml')
    xs=rollout(e,a)
    assert xs[-1]['q'][1] < 0.5
    assert xs[-1]['q'][2] > 0.9

def test_feedforward_not_strongly_connected_by_definition():
    a=load('configs/architectures/b2/feedforward_v1.yaml')
    assert a['edges']==[[0,1],[0,2]]

def test_reciprocal_cycle_registered():
    a=load('configs/architectures/b2/reciprocal_v1.yaml')
    assert set(map(tuple,a['edges']))=={(0,1),(1,2),(2,0)}

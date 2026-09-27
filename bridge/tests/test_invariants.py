"""Invariant tests for the neural bridge (v3 scaffold).

Covers the eight behaviors the card names as the bridge's required invariants,
each against a small deterministic fixture of the implemented modules
(:mod:`bridge.substrate`, :mod:`bridge.agent`, :mod:`bridge.env`,
:mod:`bridge.trainer`):

1. W decay — the cue slot's readout flips to neutral once the decay age reaches
   ``lifetime`` (deterministic countdown), restored only by the paid refresh.
2. Paid refresh — ``pi`` costs ``E_pi``, resets the decay age, and is the only
   thing that staves off decay.
3. Energy conservation — the ledger ``E_{t+1} = E_t + earn - spend`` holds
   exactly, and death is ``E_t <= death_floor``.
4. Reward separation — the probe reward is computed on stable-regime episodes
   only and adds no gradient to the maintenance allocator A.
5. Trainer-label severance — the supervision targets (``y_E``, ``y_I``) are
   pure functions of the measured bookkeeping ``b_t = (E_t, d_t)``, never of
   V's own estimate.
6. Cue leakage — the cue identity is visible only in W and the probe readout,
   never in ``h_t``, V, or A.
7. Intervention correctness — the regime announcement gate and the substrate's
   causal responses to a forced refresh / forced hold are exactly as modelled.
8. Deterministic replay — a seeded environment draw, a full forward pass, and a
   round-trip through saved episodes all replay identically.

Runs as pytest (``pytest bridge/tests``) or as a plain script
(``PYTHONPATH=. .venv-bridge/bin/python -B bridge/tests/test_invariants.py``).
"""

from __future__ import annotations

import math
from dataclasses import replace

import torch

from bridge.agent import NeuralBridge
from bridge.config import BridgeConfig, DecayConfig, EnergyConfig
from bridge.env import BridgeEnv, REGIME_STABLE
from bridge.reproducibility import seed_all
from bridge.substrate import Substrate
from bridge.trainer import (
    BridgeTrainer,
    compute_losses,
    integrity_label,
    quantize_energy,
)


# --------------------------------------------------------------------------- #
# Substrate law: W decay, paid refresh, energy conservation
# --------------------------------------------------------------------------- #

def _substrate(cfg: BridgeConfig) -> Substrate:
    return Substrate(cfg.energy, cfg.decay)


def test_decay_flips_to_neutral_at_lifetime():
    # Deterministic countdown (N6 §3.2): at age >= lifetime the readout is
    # neutral (0) regardless of the stored value or the refresh action.
    cfg = BridgeConfig()  # lifetime = 16
    sub = _substrate(cfg)
    sub.reset(4)
    sub.age = torch.tensor([0, 15, 16, 20])
    slot = torch.ones(4, cfg.arch.w_bits)
    out = sub.decay_slot(slot, torch.zeros(4))
    expected = torch.tensor([[1.0], [1.0], [0.0], [0.0]])
    assert torch.equal(out, expected)


def test_refresh_restores_readout():
    # A slot whose age has reached lifetime reads neutral; a refresh (age reset)
    # restores the readout to the stored value.
    cfg = BridgeConfig()
    sub = _substrate(cfg)
    sub.reset(2)
    sub.age = torch.tensor([16, 16])
    slot = torch.full((2, cfg.arch.w_bits), -1.0)
    # No refresh: both read neutral.
    assert torch.all(sub.decay_slot(slot, torch.zeros(2)) == 0.0)
    # Refresh episode 0 only: apply_refresh resets its age -> readout intact.
    sub.apply_refresh(torch.tensor([1.0, 0.0]))
    out = sub.decay_slot(slot, torch.tensor([1.0, 0.0]))
    assert torch.equal(out, torch.tensor([[-1.0], [0.0]]))


def test_no_decay_before_lifetime():
    # Before the deadline the readout keeps the stored value (no decay).
    cfg = BridgeConfig()
    sub = _substrate(cfg)
    sub.reset(4)
    sub.age = torch.tensor([0, 1, 15, 15])
    slot = torch.ones(4, cfg.arch.w_bits)
    assert torch.all(sub.decay_slot(slot, torch.zeros(4)) == 1.0)


def test_readout_is_age_gated_not_alive_gated():
    # The decay readout is a pure function of age: a dead episode at age >=
    # lifetime still reads neutral, a dead one at age < lifetime still reads
    # intact. Death freezes the counter (tick_age), it does not zero the slot.
    cfg = BridgeConfig()
    sub = _substrate(cfg)
    sub.reset(4)
    sub.alive = torch.tensor([False, False, True, True])
    sub.age = torch.tensor([16, 15, 16, 15])
    slot = torch.ones(4, cfg.arch.w_bits)
    out = sub.decay_slot(slot, torch.zeros(4))
    expected = torch.tensor([[0.0], [1.0], [0.0], [1.0]])
    assert torch.equal(out, expected)


def test_paid_refresh_costs_and_resets_age():
    cfg = BridgeConfig()
    sub = _substrate(cfg)

    # spend: E_proc always, plus E_pi where refreshed and affordable.
    sub.reset(4)  # energy = e0 = 8.0
    spend = sub.spend(torch.tensor([1.0, 0.0, 1.0, 0.0]))
    assert torch.allclose(
        spend,
        torch.tensor([0.1 + 1.0, 0.1, 0.1 + 1.0, 0.1]),
    )
    assert torch.allclose(
        sub.energy,
        torch.tensor([6.9, 7.9, 6.9, 7.9]),
    )

    # apply_refresh: age resets to 0 only where refreshed.
    sub.age = torch.tensor([0, 5, 3, 9])
    sub.apply_refresh(torch.tensor([1.0, 0.0, 1.0, 0.0]))
    assert torch.equal(sub.age, torch.tensor([0, 5, 0, 9]))


def test_refresh_clamped_by_budget_and_affordability():
    # Budget cap: E_pi + E_proc > B_t -> refresh is clamped off entirely.
    energy = replace(EnergyConfig(), budget_b=0.5)
    cfg = replace(BridgeConfig(), energy=energy)
    sub = _substrate(cfg)
    sub.reset(4)
    spend = sub.spend(torch.ones(4))
    assert torch.allclose(spend, torch.full((4,), cfg.energy.e_proc))

    # Affordability: energy < E_pi -> refresh off even when action = 1.
    cfg = BridgeConfig()
    sub = _substrate(cfg)
    sub.reset(4)
    sub.energy = torch.tensor([0.5, 8.0, 0.9, 8.0])
    spend = sub.spend(torch.ones(4))
    assert torch.allclose(spend, torch.tensor([0.1, 1.1, 0.1, 1.1]))


def test_energy_conservation_exact():
    # E_{t+1} = E_t + earn_t - spend_t, exactly, at every tick and episode.
    cfg = BridgeConfig()
    env = BridgeEnv(cfg)
    bridge = NeuralBridge(cfg)
    seed_all(21)
    batch = env.sample(8)
    seed_all(21)
    out = bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])

    B, T = batch["x"].shape[:2]
    earn = batch["correct"].float() * cfg.energy.e_earn  # (B, T)
    spend = out["spend"]  # (B, T)
    prev = torch.full((B,), cfg.energy.e0)
    for t in range(T):
        assert torch.allclose(
            out["energy"][:, t], prev + earn[:, t] - spend[:, t], atol=1e-5
        ), t
        prev = out["energy"][:, t]


def test_death_at_energy_floor():
    cfg = BridgeConfig()
    sub = _substrate(cfg)
    sub.reset(2)
    sub.energy = torch.tensor([0.15, 0.05])
    sub.spend(torch.zeros(2))  # -0.1 each -> [0.05, -0.05]
    assert bool(sub.alive[0]) and not bool(sub.alive[1])


# --------------------------------------------------------------------------- #
# Reward separation
# --------------------------------------------------------------------------- #

def test_reward_paid_only_on_stable_episodes():
    # No stable episodes -> the probe reward (objective) is exactly zero.
    cfg = BridgeConfig()
    env = BridgeEnv(cfg)
    bridge = NeuralBridge(cfg)
    seed_all(31)
    batch = env.sample(16, p_stable=0.0)
    assert bool((batch["regime_class"] != REGIME_STABLE).all())
    seed_all(31)
    out = bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    losses, _ = compute_losses(cfg, out, batch)
    assert losses["probe"].item() == 0.0


def _a_policy_grads(bridge, loss):
    bridge.zero_grad(set_to_none=True)
    loss.backward(retain_graph=True)
    return {
        n: p.grad.detach().clone()
        for n, p in bridge.named_parameters()
        if n.startswith("allocator.policy")
    }


def test_allocator_invariant_to_reward():
    # The reward (probe), L_V, and critic losses add zero gradient to A's policy
    # head — reward-invariance of the maintenance allocator (G3c's structural half).
    cfg = BridgeConfig()
    trainer = BridgeTrainer(cfg, seed=5)
    batch = trainer.env.sample(16)
    out = trainer.bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    losses, _ = compute_losses(cfg, out, batch)

    joint = (
        losses["J_A_policy"] + losses["probe"] + losses["L_V"] + losses["J_A_critic"]
    )
    g_joint = _a_policy_grads(trainer.bridge, joint)
    g_alone = _a_policy_grads(trainer.bridge, losses["J_A_policy"])

    assert set(g_joint) == set(g_alone)
    for n in g_alone:
        assert torch.allclose(g_joint[n], g_alone[n], rtol=1e-5, atol=1e-7), n


# --------------------------------------------------------------------------- #
# Trainer-label severance
# --------------------------------------------------------------------------- #

def test_label_helpers_are_pure_functions():
    # quantize_energy: uniform bins over [0, e0], saturating at the top bin.
    E = torch.tensor([-1.0, 0.0, 1.999, 2.0, 4.0, 7.999, 8.0, 100.0])
    assert torch.equal(quantize_energy(E, 4, 8.0), torch.tensor([0, 0, 0, 1, 2, 3, 3, 3]))

    # integrity_label: 1[age < lifetime], a function of the measured age only.
    age = torch.tensor([0, 15, 16, 17, 100])
    assert torch.equal(integrity_label(age, 16), torch.tensor([1, 1, 0, 0, 0]))


def test_bookkeeping_b_is_measured_state_not_estimate():
    # b_t = (E_t, d_t) is the substrate's measured ledger, not V's code. At tick
    # 0 it is exactly the measured initial state (e0, 0).
    cfg = BridgeConfig()
    env = BridgeEnv(cfg)
    bridge = NeuralBridge(cfg)
    seed_all(4)
    batch = env.sample(8)
    seed_all(4)
    out = bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])

    B = batch["x"].shape[0]
    assert out["b"].shape == (B, cfg.episode.horizon_t, 2)
    assert torch.all(out["b"][:, 0, 0] == cfg.energy.e0)
    assert torch.all(out["b"][:, 0, 1] == 0.0)
    # The estimator code is a distinct tensor of different width.
    assert out["v"].shape[-1] == cfg.arch.v_energy_bits + cfg.arch.v_integrity_bits


def test_labels_invariant_to_estimator_output():
    # Severance: the label-side quantities (homeostatic cost, energy/age readouts,
    # alive fraction, refresh rate) are computed from the measured bookkeeping,
    # so zeroing V's estimate leaves them unchanged while the estimator's own
    # prediction loss collapses to the uniform (uninformative) value.
    cfg = BridgeConfig()
    trainer = BridgeTrainer(cfg, seed=5)
    batch = trainer.env.sample(16)
    out = trainer.bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    _, m1 = compute_losses(cfg, out, batch)

    out2 = {
        **out,
        "v": torch.zeros_like(out["v"]),
        "v_logits": torch.zeros_like(out["v_logits"]),
    }
    _, m2 = compute_losses(cfg, out2, batch)

    for k in ("mean_cost", "mean_energy", "mean_age", "alive_frac", "refresh_rate"):
        assert torch.equal(m1[k], m2[k]), k

    # Zeroed estimate -> uniform prediction: CE = ln(n_energy) + ln(n_integrity).
    n_energy = 2 ** cfg.arch.v_energy_bits
    n_integrity = 2 ** cfg.arch.v_integrity_bits
    assert torch.allclose(m2["L_V_energy"], torch.tensor(math.log(n_energy)), atol=1e-4)
    assert torch.allclose(
        m2["L_V_integrity"], torch.tensor(math.log(n_integrity)), atol=1e-4
    )
    assert not torch.equal(m1["L_V"], m2["L_V"])


# --------------------------------------------------------------------------- #
# Cue leakage
# --------------------------------------------------------------------------- #

def test_cue_does_not_leak_beyond_workspace():
    # With lifetime > horizon the cue survives to the probe, so the flip is visible. The
    # cue must show up ONLY in W (slot) and the probe readout — every other
    # channel (h, V, A, substrate) must be bit-for-bit identical under the flip.
    cfg = replace(BridgeConfig(), decay=replace(DecayConfig(), lifetime=100))
    env = BridgeEnv(cfg)
    bridge = NeuralBridge(cfg)

    seed_all(11)
    batch_a = env.sample(16)
    batch_b = {**batch_a, "cue": -batch_a["cue"]}  # flip +1 <-> -1

    seed_all(11)
    out_a = bridge(batch_a["x"], batch_a["cue"], batch_a["regime"], batch_a["correct"])
    seed_all(11)
    out_b = bridge(batch_b["x"], batch_b["cue"], batch_b["regime"], batch_b["correct"])

    for key in (
        "h", "v", "v_logits", "b", "refresh_logit", "refresh_prob", "refresh",
        "logp", "value", "energy", "age", "alive", "spend",
    ):
        assert torch.equal(out_a[key], out_b[key]), key

    assert not torch.equal(out_a["slot"], out_b["slot"])
    assert not torch.equal(out_a["probe_logits"], out_b["probe_logits"])


# --------------------------------------------------------------------------- #
# Intervention correctness
# --------------------------------------------------------------------------- #

def test_regime_announcement_gate():
    # Before the announce tick m the regime one-hot is the zero vector
    # ("unannounced"); from m onward it is exactly the announced regime.
    cfg = BridgeConfig()
    env = BridgeEnv(cfg)
    seed_all(3)
    batch = env.sample(16)

    m = cfg.decay.announce_m
    regime = batch["regime"]  # (B, T, 2)
    assert torch.all(regime[:, :m] == 0.0)

    announced = regime[:, m:]
    expected = (
        torch.nn.functional.one_hot(batch["regime_class"], 2)
        .float()
        .unsqueeze(1)
        .expand_as(announced)
    )
    assert torch.equal(announced, expected)


def test_forced_refresh_causally_preserves_slot():
    # Do-intervention on pi: at age = lifetime, forcing refresh preserves the
    # readout while forcing hold makes it neutral — the free-permanence contrast
    # (E1) at the substrate level, deterministic.
    cfg = BridgeConfig()
    sub = _substrate(cfg)
    sub.reset(2)
    sub.age = torch.tensor([16, 16])  # both slots have reached the deadline
    slot = torch.ones(2, cfg.arch.w_bits)

    # Tick once, refreshing episode 0 and holding episode 1.
    action = torch.tensor([1.0, 0.0])
    sub.earn(torch.ones(2, dtype=torch.bool))
    sub.spend(action)
    sub.apply_refresh(action)
    slot = sub.decay_slot(slot, action)

    # Refreshed slot's readout survived; held slot's readout is neutral.
    assert torch.equal(slot, torch.tensor([[1.0], [0.0]]))
    # Refreshed episode paid E_pi on top of E_proc.
    assert torch.allclose(
        sub.energy,
        torch.tensor([cfg.energy.e0 + cfg.energy.e_earn - (cfg.energy.e_proc + cfg.energy.e_pi),
                      cfg.energy.e0 + cfg.energy.e_earn - cfg.energy.e_proc]),
    )


def test_homeostatic_cost_is_survival_blind():
    # G3d (decoupling): the homeostatic cost and the A objective are functions of
    # the measured (regime, energy, age) only — death/survival never enters, so
    # zeroing the alive mask leaves the maintenance objective unchanged.
    cfg = BridgeConfig()
    trainer = BridgeTrainer(cfg, seed=5)
    batch = trainer.env.sample(16)
    out = trainer.bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    _, metrics = compute_losses(cfg, out, batch)

    # Reconstruct c_homeo from measured quantities only.
    is_stable = batch["regime"][..., REGIME_STABLE] > 0.5
    E_t = out["b"][..., 0]
    d_t = out["b"][..., 1]
    i_star = (is_stable & (E_t >= cfg.energy.e_crit)).long()
    i_measured = integrity_label(d_t, cfg.decay.lifetime)
    c_homeo = (i_measured != i_star).float()
    assert torch.allclose(c_homeo.mean(), metrics["mean_cost"], atol=1e-6)

    # Zeroing the alive flag changes nothing in the maintenance objective.
    out_dead = {**out, "alive": torch.zeros_like(out["alive"])}
    _, m_dead = compute_losses(cfg, out_dead, batch)
    assert torch.equal(m_dead["mean_cost"], metrics["mean_cost"])
    assert torch.equal(m_dead["J_A_policy"], metrics["J_A_policy"])
    assert torch.equal(m_dead["J_A_critic"], metrics["J_A_critic"])


# --------------------------------------------------------------------------- #
# Deterministic replay
# --------------------------------------------------------------------------- #

def test_env_sample_is_deterministic():
    cfg = BridgeConfig()
    env = BridgeEnv(cfg)
    seed_all(7)
    a = env.sample(8)
    seed_all(7)
    b = env.sample(8)
    for key in ("x", "cue", "regime", "regime_class", "correct"):
        assert torch.equal(a[key], b[key]), key


def test_forward_replay_is_deterministic():
    # Two same-seed bridges + two same-seed forwards are bit-for-bit identical.
    cfg = BridgeConfig()
    env = BridgeEnv(cfg)
    seed_all(9)
    batch = env.sample(8)

    seed_all(9)
    b1 = NeuralBridge(cfg)
    seed_all(9)
    b2 = NeuralBridge(cfg)

    seed_all(9)
    o1 = b1(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    seed_all(9)
    o2 = b2(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    for key in o1:
        assert torch.equal(o1[key], o2[key]), key


def test_replay_from_saved_episodes_is_identical():
    # The same episodes, round-tripped through the records format, replay to an
    # identical forward pass.
    cfg = BridgeConfig()
    env = BridgeEnv(cfg)
    bridge = NeuralBridge(cfg)

    seed_all(13)
    batch = env.sample(8)
    reloaded = BridgeEnv.from_records(env.to_records(batch))

    seed_all(13)
    o1 = bridge(batch["x"], batch["cue"], batch["regime"], batch["correct"])
    seed_all(13)
    o2 = bridge(reloaded["x"], reloaded["cue"], reloaded["regime"], reloaded["correct"])
    for key in o1:
        assert torch.equal(o1[key], o2[key]), key


def _run_all():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"OK: {len(tests)} tests passed")


if __name__ == "__main__":
    _run_all()

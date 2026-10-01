from __future__ import annotations

import numpy as np
import pytest

from sub_a_v1.skeleton import Arm, Damage, Substrate


def fixture(seed: int = 0) -> Substrate:
    rng = np.random.default_rng(seed)
    skill = np.repeat(rng.choice([-1.0, 1.0], size=(1, 8)), 3, axis=0)
    return Substrate(skill, np.ones((3, 8)), np.ones((3, 1)))


def events(state: Substrate, seed: int, *, erase_all: bool = False) -> dict[str, Damage]:
    rng = np.random.default_rng(seed)
    return {
        name: Damage(
            rng.uniform(0.0, 0.08, bank.shape),
            rng.normal(0.0, 0.04, bank.shape),
            np.ones(bank.shape, dtype=bool) if erase_all
            else rng.random(bank.shape) < 0.15,
        )
        for name, bank in state.banks.items()
    }


def no_damage(state: Substrate) -> dict[str, Damage]:
    return {
        name: Damage(np.zeros(bank.shape), np.zeros(bank.shape),
                     np.zeros(bank.shape, dtype=bool))
        for name, bank in state.banks.items()
    }


def assert_equal(left: Substrate, right: Substrate) -> None:
    assert left.tick == right.tick
    for name in left.banks:
        np.testing.assert_array_equal(left.banks[name], right.banks[name])


@pytest.mark.parametrize("seed", range(4))
def test_exact_external_code_and_yoked_reduction(seed: int) -> None:
    donor, external, code, yoke = (fixture(seed) for _ in range(4))
    for tick in range(6):
        damage = events(donor, seed * 100 + tick)
        action = donor.step(damage, Arm.SELF)
        assert external.step(damage, Arm.EXTERNAL) == action
        assert code.step(damage, Arm.CODE) == action
        assert yoke.step(damage, Arm.YOKED,
                         yoked_action=action.repair_requested) == action
        for twin in (external, code, yoke):
            assert_equal(donor, twin)


@pytest.mark.parametrize("sign", [-1.0, 1.0])
def test_single_replica_erasure_is_ordinary_error_correction(sign: float) -> None:
    state = Substrate(np.full((3, 8), sign), np.ones((3, 8)), np.ones((3, 1)))
    damage = no_damage(state)
    damage["skill"].erase[0, :] = True
    state.step(damage, Arm.CODE)
    np.testing.assert_array_equal(state.banks["skill"], np.full((3, 8), sign))


def test_positive_shrinkage_preserves_sign_skill() -> None:
    state = fixture()
    predictions = [state.predict(cue) for cue in range(8)]
    damage = no_damage(state)
    for value in damage.values():
        value.shrinkage[:] = 0.75
    for _ in range(10):
        state.step(damage, Arm.NO_REPAIR)
    assert [state.predict(cue) for cue in range(8)] == predictions


def test_total_loss_has_no_table_dependent_recovery() -> None:
    positive = Substrate(np.ones((3, 8)), np.ones((3, 8)), np.ones((3, 1)))
    negative = Substrate(-np.ones((3, 8)), np.ones((3, 8)), np.ones((3, 1)))
    positive.step(events(positive, 0, erase_all=True), Arm.SELF)
    negative.step(events(negative, 0, erase_all=True), Arm.SELF)
    assert_equal(positive, negative)
    assert not positive.consolidate()
    positive.banks["repair"][:] = 1.0
    positive.banks["replay"][:] = 1.0
    assert positive.consolidate()
    np.testing.assert_array_equal(positive.banks["skill"], np.zeros((3, 8)))


def test_live_gain_lesion_disables_writes_not_host_consensus() -> None:
    state = fixture()
    state.banks["skill"][0, :] = 0
    state.banks["repair"][:] = 0
    before = state.banks["skill"].copy()
    assert not state.consolidate()
    np.testing.assert_array_equal(state.banks["skill"], before)
    assert state.predict(0) == int(before[1, 0] > 0)


def test_replay_loss_prevents_skill_writes() -> None:
    state = fixture()
    state.banks["skill"][0, :] = 0
    state.banks["replay"][:] = 0
    before = state.banks["skill"].copy()
    state.consolidate()
    np.testing.assert_array_equal(state.banks["skill"], before)


def test_disagreement_does_not_identify_integrity() -> None:
    correct = Substrate(np.ones((3, 8)), np.ones((3, 8)), np.ones((3, 1)))
    wrong = Substrate(-np.ones((3, 8)), np.ones((3, 8)), np.ones((3, 1)))
    assert correct.disagreement() == wrong.disagreement() == 0
    assert correct.predict(0) != wrong.predict(0)


def test_constructor_does_not_retain_a_clean_template_or_alias_inputs() -> None:
    skill = np.ones((3, 8))
    state = Substrate(skill, skill, np.ones((3, 1)))
    skill[:] = 99
    assert set(vars(state)) == {"banks", "tick"}
    assert state.stored_scalars == 51
    assert set(state.banks) == {"skill", "replay", "repair"}
    state.banks["skill"][:] = 0
    assert state.banks["replay"].max() == 1


def test_immortal_reference_and_null_writes() -> None:
    immortal, null = fixture(), fixture()
    untouched = fixture()
    damage = events(immortal, 0, erase_all=True)
    immortal.step(damage, Arm.IMMORTAL)
    null.step(damage, Arm.NO_REPAIR)
    untouched.tick = 1
    assert_equal(immortal, untouched)
    assert not null.banks["skill"].any()
    assert immortal.tick == null.tick == 1


def test_threshold_is_a_live_state_rule_without_a_damage_meter() -> None:
    state = fixture()
    assert not state.step(no_damage(state), Arm.FIXED_THRESHOLD).repair_requested
    state.banks["skill"][0, :] = 0
    assert state.step(no_damage(state), Arm.FIXED_THRESHOLD).repair_requested


@pytest.mark.parametrize("cue", [-1, 8, True, 0.5])
def test_invalid_cue_is_explicit(cue: object) -> None:
    with pytest.raises(ValueError):
        fixture().predict(cue)  # type: ignore[arg-type]


def test_incomplete_or_invalid_damage_cannot_partially_mutate_state() -> None:
    state, original = fixture(), fixture()
    damage = no_damage(state)
    damage["repair"].shrinkage[:] = 2
    with pytest.raises(ValueError, match="Shrinkage"):
        state.step(damage, Arm.SELF)
    assert_equal(state, original)
    del damage["repair"]
    with pytest.raises(ValueError, match="Every persistent bank"):
        state.step(damage, Arm.IMMORTAL)
    assert_equal(state, original)


@pytest.mark.parametrize("arm,action", [(Arm.YOKED, None), (Arm.YOKED, 1),
                                      (Arm.SELF, True)])
def test_yoke_action_boundary(arm: Arm, action: object) -> None:
    state = fixture()
    with pytest.raises(ValueError):
        state.step(no_damage(state), arm, yoked_action=action)  # type: ignore[arg-type]
    assert state.tick == 0


@pytest.mark.parametrize("threshold", [-1, np.nan, np.inf])
def test_invalid_threshold_is_explicit(threshold: float) -> None:
    state = fixture()
    with pytest.raises(ValueError, match="Threshold"):
        state.step(no_damage(state), Arm.FIXED_THRESHOLD, threshold=threshold)
    assert state.tick == 0

"""Tests for capacity matching (G4 §8 rule 3): the parameter budget P is split
across replicating arms and zero for the fixed-accumulator rivals."""

from phase3.config import Phase3Config, parameter_counts, r1_split_hidden


def test_candidate_has_single_encoder():
    counts = parameter_counts(Phase3Config())
    assert counts["candidate_encoder"] > 0


def test_r1_splits_budget_across_copies():
    cfg = Phase3Config()
    counts = parameter_counts(cfg)
    # each private encoder gets ~ P/n; the three-encoder total does not exceed P
    assert counts["r1_per_copy"] * 3 <= counts["candidate_encoder"]
    assert counts["r1_three_encoders"] <= counts["candidate_encoder"]
    # the robustness variant (each copy at full P) is the n*P disclosure
    assert counts["r1_robustness_nP"] == 3 * counts["candidate_encoder"]


def test_r4_r5_have_no_learned_inference():
    counts = parameter_counts(Phase3Config())
    assert counts["r4_total"] == 0
    assert counts["r5_total"] == 0


def test_r2_r3_have_learned_heads():
    counts = parameter_counts(Phase3Config())
    assert counts["r2_total"] > 0
    assert counts["r3_total"] > 0


def test_split_hidden_never_exceeds_full():
    cfg = Phase3Config()
    h = r1_split_hidden(cfg)
    assert h <= cfg.arm.p_levels[cfg.arm.p_level]
    assert h >= 1

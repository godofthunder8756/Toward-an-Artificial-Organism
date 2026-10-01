import json
from pathlib import PurePosixPath
import subprocess

from a6_decision_v1.preservation import ROOT


def test_new_cards_have_thirteen_answers_and_no_execution_permission():
    metadata = json.loads((ROOT / ".vscode" / "aci-research-cards-v1.json").read_text())
    ids = [card["id"] for card in metadata["cards"]]
    assert len(ids) == len(set(ids))
    for card in metadata["cards"]:
        assert card["class"] in ("analytic", "engineering", "confirmatory", "synthesis")
        assert set(card["admission"]) == {f"Q{i}" for i in range(1, 14)}
        assert all(value.strip() for value in card["admission"].values())
        assert card["execution_authorized"] is False
        for source in card["evidence_refs"]:
            assert ROOT.joinpath(*PurePosixPath(source).parts).is_file(), source
    proposed = metadata["cards"][-1]
    assert proposed["requires_human_approval"]
    assert proposed["requires_a6_outcome"] == "UNRESOLVED"


def test_separate_axes_and_scoped_evidence_ledger():
    ledger = json.loads((ROOT / "ACI_ARCHITECTURAL_BELIEF_LEDGER_v1.json").read_text())
    assert not ledger["consciousness_claim"]
    assert ledger["axes_are_not_one_score"]
    assert {row["layer"] for row in ledger["layer_assessments"]} == {
        *(f"O{i}" for i in range(5)), *(f"C{i}" for i in range(8))}
    for row in ledger["layer_assessments"]:
        for field in ("status", "scope", "evidence", "supplied", "ceiling", "rival", "next_falsifier"):
            assert row[field]
        for source in row["evidence"] + row.get("counterevidence", []):
            assert ROOT.joinpath(*PurePosixPath(source).parts).is_file(), source
    assert all(item["execution"] == "not authorized" for item in ledger["inactive_theory_queue"])


def test_board_preserves_completed_history_and_human_gate():
    original = json.loads(subprocess.run(
        ["git", "show", "HEAD:.vscode/kanban-agent.json"], cwd=ROOT,
        check=True, capture_output=True, text=True,
    ).stdout)
    board = json.loads((ROOT / ".vscode" / "kanban-agent.json").read_text())
    current = {card["id"]: card for card in board}
    assert len(current) == len(board)
    for card in original:
        if card["status"] == "done":
            assert current[card["id"]] == card
    for identity in ("r10a-a6", "r10a-a8"):
        assert current[identity]["status"] == "todo"
        assert "PARKED" in current[identity]["title"]
    metadata = json.loads((ROOT / ".vscode" / "aci-research-cards-v1.json").read_text())
    assert all(card["id"] in current for card in metadata["cards"])
    assert current["aci-world-admission-human-gate"]["status"] == "todo"

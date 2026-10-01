"""Additional solver-free gate consequences from individual Bayes floors."""

from fractions import Fraction as F
import json
from pathlib import Path

from a6_decision_v1.exact import BASELINES, COMPONENT_DENOMINATOR, GATE, component_costs
from a6_decision_v1.preservation import write_once
from a6_decision_v1.verify import integer_components
from phase3b_r10_v1.verify import verify as verify_r10


def verify():
    posterior = component_costs()
    integer = integer_components()
    if posterior != integer:
        raise AssertionError("independent populations disagree")
    floors = tuple(F(sum(min(policy[j] for policy in row) for row in integer),
                     COMPONENT_DENOMINATOR) for j in range(3))
    assert floors == (F(13, 125), F(59, 625), F(164, 625))
    upper_at_gate = tuple(3 * GATE - sum(floors[k] for k in range(3) if k != j)
                          for j in range(3))
    r10 = F(5101889, 29296875)
    upper_at_r10 = tuple(3 * r10 - sum(floors[k] for k in range(3) if k != j)
                         for j in range(3))
    assert upper_at_gate[0] < BASELINES[0] and upper_at_gate[2] < BASELINES[2]
    assert upper_at_gate[1] > BASELINES[1]
    assert all(a < b for a, b in zip(upper_at_r10, BASELINES))
    from a6_decision_v1.exact import POLICIES
    from a6_decision_v1.preservation import ROOT
    orientation_floors = []
    for maps in (((0, 0), (0, 1), (1, 1)), ((0, 0), (1, 0), (1, 1))):
        allowed = [i for i, policy in enumerate(POLICIES) if policy[2] in maps]
        orientation_floors.append(F(sum(min(row[k][2] for k in allowed) for row in integer),
                                    COMPONENT_DENOMINATOR))
    assert orientation_floors == [F(182, 625)] * 2
    r9_floors = (floors[0], floors[1], orientation_floors[0])
    r9_ceilings = tuple(3 * GATE - sum(r9_floors[k] for k in range(3) if k != j)
                        for j in range(3))
    assert all(a < b for a, b in zip(r9_ceilings, BASELINES))
    certificate = json.loads((ROOT / "phase3b_r10_v1" / "certificate.json").read_text())
    assert F(verify_r10(certificate)["r10_exact"]) == r10
    book = [tuple(tuple(pair) for pair in certificate["policies"][k])
            for k in certificate["selected"]]
    indices = [POLICIES.index(policy) for policy in book]
    r10_components = tuple(F(sum(row[indices[word]][j] for row, word in
                                zip(integer, certificate["encoder"])), COMPONENT_DENOMINATOR)
                           for j in range(3))
    assert sum(r10_components) / 3 == r10
    assert all(a < b for a, b in zip(r10_components, BASELINES))
    return {
        "verified": True, "individual_bayes_floors": [str(v) for v in floors],
        "component_upper_at_joint_gate": [str(v) for v in upper_at_gate],
        "s1_and_s3_competence_implied_by_joint_gate": True,
        "s2_competence_not_implied_by_this_bound": True,
        "component_upper_at_r10": [str(v) for v in upper_at_r10],
        "r10_actual_components": [str(v) for v in r10_components],
        "r9_s3_orientation_floor": [str(v) for v in orientation_floors],
        "r9_component_upper_at_joint_gate": [str(v) for v in r9_ceilings],
        "r9_full_gate_equivalent_to_joint_gate": True,
        "r10_joint_optimum_implies_all_strict_specialist_gates": True,
        "shared4_unrestricted_r10_extension": (
            "Reuse the fixed eight-policy book and rotate the arbitrary encoder's "
            "belief inputs by context. Fair independent factors make each "
            "context population risk identical. This is EXTERNAL unrestricted "
            "coding, not the coupled affine/recurrent R9 graph."),
        "capacity_conclusion": "Eight symbols suffice for the full frozen gate in the unrestricted coding class.",
        "r9_conclusion": "Shared deployed R9 competence is still a distinct unresolved class-existence question.",
        "training": False, "solvers": False,
    }


if __name__ == "__main__":
    result = verify()
    output = Path(__file__).with_name("analytic_corollaries.json")
    write_once(output, result)
    print(json.dumps(result, indent=2))

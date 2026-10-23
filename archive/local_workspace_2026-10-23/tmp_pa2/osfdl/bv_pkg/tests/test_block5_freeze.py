
import json, hashlib
from pathlib import Path
import pytest
from toe_exp.block5 import *
ROOT=Path(__file__).resolve().parents[1]

def test_dev_seeds_are_unique(): assert len(set(DEV_SEEDS))==20
def test_monitor_no_label_access():
    t=make_trial(1,1,"decision",True,True)
    q=self_monitor(t)
    assert .5<q<1
def test_world_monitor_ignores_internal_diagnostics():
    a=make_trial(1,1,"decision",False,True); b=make_trial(1,2,"decision",True,True)
    a.difficulty=b.difficulty=.79
    assert world_monitor(a)==world_monitor(b)
def test_s1_is_passive():
    rows=run_family(52001,"decision","S1")
    assert sum(x.checked+x.extra_compute for x in rows)==0
def test_s2_can_check():
    rows=run_family(52001,"decision","S2")
    assert sum(x.checked for x in rows)>0
def test_s2_can_allocate_compute():
    rows=run_family(52001,"verification","S2")
    assert sum(x.extra_compute for x in rows)>0
def test_s3_exact_distribution_match_decision():
    seed=52001; n=160
    trials=[]
    for i in range(n): trials.append(make_trial(seed,i,"decision",i%4 in (2,3),True))
    qs=[self_monitor(t) for t in trials]
    order=sorted(range(len(qs)),key=lambda i:qs[i]); rev=[qs[i] for i in reversed(order)]
    sh=[None]*len(qs)
    for rank,i in enumerate(order): sh[i]=rev[rank]
    assert sorted(round(x,12) for x in qs)==sorted(round(x,12) for x in sh)
def test_misinformation_changes_decision_control():
    r=misinformation(52001,"decision")
    assert r["overconfident"]["check_rate"] < r["accurate"]["check_rate"]
def test_misinformation_changes_verification_control():
    r=misinformation(52001,"verification")
    assert r["overconfident"]["compute_rate"] < r["accurate"]["compute_rate"]
def test_correction_restores_decision_profile():
    r=misinformation(52002,"decision")
    assert r["accurate"]==r["restored"]
def test_correction_restores_verification_profile():
    r=misinformation(52002,"verification")
    assert r["accurate"]==r["restored"]
def test_self_vs_world_tracks_internal_change():
    r=self_vs_world(52001)
    assert r["self_impaired"] < r["self_healthy"]-.08
    assert abs(r["world_impaired"]-r["world_healthy"])<.03
def test_capability_boundary_is_calibrated_enough_for_development():
    vals=[capability_boundary(s)["calibration_mae"] for s in DEV_SEEDS[:5]]
    assert sum(vals)/len(vals)<.12
def test_active_beats_passive_both_families():
    recs=[dev_seed(s) for s in DEV_SEEDS[:5]]; a=aggregate(recs)
    assert a["diagnostics"]["decision_active_passive_gain"]>.12
    assert a["diagnostics"]["verification_active_passive_gain"]>.10
def test_active_recovers_better_both_families():
    recs=[dev_seed(s) for s in DEV_SEEDS[:5]]; a=aggregate(recs)
    assert a["diagnostics"]["decision_recovery_gain"]>.15
    assert a["diagnostics"]["verification_recovery_gain"]>.10
def test_targeted_overconfidence_harms_both_families():
    recs=[dev_seed(s) for s in DEV_SEEDS[:5]]; a=aggregate(recs)
    assert a["diagnostics"]["decision_overconfidence_effect"]<-.15
    assert a["diagnostics"]["verification_overconfidence_effect"]<-.12
def test_correction_rescues_both_families():
    recs=[dev_seed(s) for s in DEV_SEEDS[:5]]; a=aggregate(recs)
    assert a["diagnostics"]["decision_rescue"]>.15
    assert a["diagnostics"]["verification_rescue"]>.12
def test_external_confidence_is_strong_bypass():
    recs=[dev_seed(s) for s in DEV_SEEDS[:5]]; a=aggregate(recs)
    assert abs(a["diagnostics"]["external_bypass_decision_gap"])<.05
    assert abs(a["diagnostics"]["external_bypass_verification_gap"])<.05
def test_seed_audit_passes():
    assert json.loads((ROOT/"BLOCK_V_SEED_INDEPENDENCE_AUDIT.json").read_text())["pass"]
def test_variant_audit_passes():
    assert json.loads((ROOT/"BLOCK_V_HELDOUT_VARIANT_AUDIT.json").read_text())["pass"]
def test_six_manifests_exist():
    assert len(list((ROOT/"configs"/"manifests").glob("*.json")))==6
def test_six_locks_exist():
    assert len(list((ROOT/"configs"/"locks").glob("*.sha256")))==6
def test_all_manifest_locks_verify():
    for p in (ROOT/"configs"/"manifests").glob("*.json"):
        expected=(ROOT/"configs"/"locks"/(p.name+".sha256")).read_text().split()[0]
        assert hashlib.sha256(p.read_bytes()).hexdigest()==expected
def test_twenty_confirmatory_seeds():
    s=[int(x) for x in (ROOT/"configs"/"seeds"/"BLOCK5_CONFIRMATORY_SEEDS_V1.txt").read_text().split()]
    assert len(s)==20 and len(set(s))==20
def test_registry_has_six_entries():
    r=json.loads((ROOT/"configs"/"experiment_registry.json").read_text())
    assert len(r["experiments"])==6
def test_all_gates_closed():
    r=json.loads((ROOT/"configs"/"experiment_registry.json").read_text())
    assert all(x["status"]=="FROZEN_PREREGISTRATION_READY_UNRUN" for x in r["experiments"].values())
def test_execution_refused_before_registration():
    assert execution_allowed(ROOT,"BLOCK5_H51_CONFIRM_001") is False
def test_prereg_record_says_no_confirmatory_data():
    r=json.loads((ROOT/"BLOCK_V_PREREGISTRATION_RECORD.json").read_text())
    assert r["confirmatory_data_generated"] is False
def test_all_variants_marked_unexecuted():
    v=json.loads((ROOT/"configs"/"confirmatory_variants.json").read_text())
    assert all(x["executed_in_development"] is False for x in v.values())
def test_no_confirmatory_results_directory():
    assert not (ROOT/"results"/"confirmatory").exists()

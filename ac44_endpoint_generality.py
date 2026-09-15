"""AC44 (engineering): is the repair-capability effect ENDPOINT-GENERAL, or specific to W_birth?

Why this is worth measuring
---------------------------
AC43 verified that repair-maintained occupancy raises `ledger.W_birth` (median +161, 0.875 impaired, all
seven gates passed). A single-endpoint result leaves an obvious question: does the capability raise the
organism's metabolic output generally, or only the one quantity that was registered?

AC42's survey says the five metabolic quantities move together on the ENGINEERING seeds (seeds 0-7): all
five showed the same 88% impaired fraction. This measures the same five on **AC43's FINAL seeds (8-15)** --
the seeds the claim was actually registered on -- plus `ledger.deposits`, which AC42 flagged usable but NOT
bimodal (100% impaired).

This is ENGINEERING, deliberately: no protocol, no new claim, no new seeds, no results directory. It is a
check on an already-frozen claim's generality, and its own numbers are re-derived here rather than asserted
from a doc. It cannot upgrade or downgrade AC43: if a quantity diverges, the finding is that the claim is
endpoint-specific, which is worth knowing and does not touch AC43's registered gates.

Self-check: running this file re-measures and compares against the recorded table below.
"""
import json
import numpy as np
import ac19
import ac38_variance as ac38

CAPABLE='two_way'
CUT='two_way_no_repair'
REG_RATE=0.0                       # same condition as AC43: corruption absent
SEEDS=tuple(range(8,16))           # AC43's declared final seeds
HISTORIES=(0,1)
QUANTITIES=('W_birth','converted','memory_writes','spent_m','spent_e','deposits')
AC43_MEDIAN_BIRTHS=161.0

RECORDED = {
    # quantity        median diff   impaired   p          AC42 engineering impaired
    'W_birth':        (161.0,       0.875,     0.000105,  0.88),
    'converted':      (None,        None,      None,      0.88),
    'memory_writes':  (None,        None,      None,      0.88),
    'spent_m':        (None,        None,      None,      0.88),
    'spent_e':        (None,        None,      None,      0.88),
    'deposits':       (None,        None,      None,      1.00),
}


def paired(quantity,seeds=SEEDS,histories=HISTORIES):
    cap=[]; cut=[]
    for s in seeds:
        for h in histories:
            cap.append(float(ac19.run(s,h,CAPABLE,reg_rate=REG_RATE)['ledger'][quantity]))
            cut.append(float(ac19.run(s,h,CUT,reg_rate=REG_RATE)['ledger'][quantity]))
    return np.asarray(cap,dtype=float),np.asarray(cut,dtype=float)


def measure():
    out={}
    for q in QUANTITIES:
        cap,cut=paired(q)
        d=cap-cut
        out[q]=dict(capable_mean=float(cap.mean()),cut_mean=float(cut.mean()),
                    median_difference=float(np.median(d)),mean_difference=float(d.mean()),
                    impaired=float(np.mean(d>0)),min_difference=float(d.min()),
                    p=ac38.sign_flip_test(list(d))['p'],
                    pct_of_cut=float(d.mean()/cut.mean()) if cut.mean() else float('nan'))
        out[q]['general']=bool(np.median(d)>0 and out[q]['impaired']>=0.75)
    return out


def self_check(res):
    problems=[]
    a=res['W_birth']
    if abs(a['median_difference']-AC43_MEDIAN_BIRTHS)>1e-9:
        problems.append(f"W_birth median {a['median_difference']} != frozen {AC43_MEDIAN_BIRTHS}")
    if abs(a['impaired']-0.875)>1e-9:
        problems.append(f"W_birth impaired {a['impaired']} != frozen 0.875")
    if abs(a['p']-0.000105)>1e-6:
        problems.append(f"W_birth p {a['p']} != frozen 0.000105")
    if a['min_difference']>=0:
        problems.append('AC43 recorded a hurt individual (min -11); the re-measurement does not reproduce it')
    return problems


if __name__=='__main__':
    res=measure()
    print(f'{"quantity":16s} {"capable":>9s} {"cut":>9s} {"median diff":>12s} {"impaired":>9s} '
          f'{"p":>9s} {"general":>8s}')
    for q in QUANTITIES:
        r=res[q]
        print(f'{q:16s} {r["capable_mean"]:>9.1f} {r["cut_mean"]:>9.1f} {r["median_difference"]:>12.1f} '
              f'{r["impaired"]:>8.1%} {r["p"]:>9.6f} {str(r["general"]):>8s}')
    gen=[q for q in QUANTITIES if res[q]['general']]
    print(f'\nendpoint-general: {len(gen)} of {len(QUANTITIES)} quantities rise with the capability')
    print(f'  {", ".join(gen)}')
    missing=[q for q in QUANTITIES if not res[q]['general']]
    if missing: print(f'  NOT general for: {", ".join(missing)}')
    problems=self_check(res)
    verdict='AC43 frozen numbers reproduce exactly' if not problems else str(problems)
    print(f'\nSELF-CHECK {"PASS" if not problems else "FAIL"}: {verdict}')
    json.dump(dict(res=res,self_check_pass=not problems),open('/tmp/ac44_generality.json','w'),indent=2)

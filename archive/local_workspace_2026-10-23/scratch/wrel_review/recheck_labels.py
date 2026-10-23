"""Independent re-application of spec FINAL §4.4-§4.6 thresholds and §4.5 decision order
to the emitted numbers in outputs/deviation_1/ITEM-8.json. Reads JSON only; no study run."""
import json,sys
from fractions import Fraction as F
P='/workspace/scratch/pr11/head/c4_reliability_exact_check_v1/outputs/deviation_1/ITEM-8.json'
d=json.load(open(P))
mu=F(1,100); muT2=F(1,2); rho=F(1,1000)
def fr(x): return None if x is None else F(x)
CORE=("C-REF","C-T2","C-SEL","C-FO","rescue")
def flags_from(agent, stateless=False):
    p=agent['pattern']; out={}
    dR,dM=fr(p['delta_R']),fr(p['delta_M'])
    out['C-REF']='PASS' if (dR>=mu and dM>=mu) else 'FAIL'
    ea,eb=fr(p['E_err_agent']),fr(p['E_err_baseline'])
    if eb==0: out['C-T2']='FAIL'  # spec: not demonstrated, not a pass
    else: out['C-T2']='PASS' if (eb-ea)/eb>=muT2 else 'FAIL'
    cfo = p.get('cfo_a') is True and p.get('cfo_b') is True
    out['C-FO']='PASS' if cfo else 'FAIL'
    if stateless:
        out['C-SEL']=out['rescue']='NOT APPLICABLE'; return out
    if not agent.get('donor_contrast',True):
        out['C-SEL']=out['rescue']='NOT EVALUABLE [NO INTERVENTION CONTRAST]'; return out
    I=agent['interventions']
    def g(dirn,key): return fr(I[dirn]['SWAP'][key])
    sel = g('S','D_e')>=mu and g('S','D_q')>=mu and g('E','D_e')<=-mu and g('E','D_q')<=-mu and cfo
    out['C-SEL']='PASS' if sel else 'FAIL'
    ok=True
    for dirn,sig in (('S',1),('E',-1)):
        eA,eB,qA,qB,LA,LB=(g(dirn,k) for k in ('eA','eB','qA','qB','LA','LB'))
        ok &= sig*(eA-eB)>=mu and sig*(qA-qB)>=mu and LA-LB>=mu
    out['rescue']='PASS' if ok else 'FAIL'
    return out
def gap(f): return any(str(f[k]).startswith('NOT') for k in CORE)
def failed(f): return any(f[k]=='FAIL' for k in CORE)
for s in d['settings']:
    ref=s['reference']
    rf=flags_from(ref)
    agree = rf==ref['flags']
    cols=s['columns']
    # decision order
    if s['pm_undefined']: lab='UNRESOLVED-DESIGN (PM)'
    elif gap(rf): lab='UNRESOLVED-DESIGN'
    elif not all(rf[k]=='PASS' for k in CORE): lab='REFERENCE CRITERIA NOT MET'
    else: lab='(steps 4-7 needed)'
    # what the reference would be if step 2 were skipped:
    demon_fail=[k for k in CORE if rf[k]=='FAIL']
    print(f"T={s['T_SEP']} c=({s['cr']},{s['cs']}): ref flags recomputed {rf}; matches emitted={agree}")
    print(f"   label(mine)={lab}; emitted={s['label_before_replay']}; reference demonstrably FAILS {demon_fail}")
    p=ref['pattern']
    print('   delta_R=%.6f delta_M=%s Eerr_base=%.6g cref_counts=%s donors %s|%s'%(float(F(p['delta_R'])),p['delta_M'],float(F(p['E_err_baseline'])),[[float(F(x)) for x in r] for r in ref['cref_counts']],ref['donor_S'],ref['donor_E']))
    if ref['donor_contrast']:
        for dirn in 'SE':
            sw=ref['interventions'][dirn]['SWAP']
            print('   SWAP-%s'%dirn,{k:round(float(F(v)),6) for k,v in sw.items() if k!='repair_equals_shadow'})
    # controls: recompute flags where pattern present, and reproduction
    for c,col in zip(s['controls'],cols):
        stateless = c['name'].startswith('R-BLIND')
        try: cf=flags_from(c,stateless)
        except Exception as ex: cf=None
        # reproduction
        rp=ref['pattern']; cp=c['pattern']; miss=[];dis=[]
        for k,v in rp.items():
            cv=cp.get(k)
            if cv is None: miss.append(k); continue
            if k in('cfo_a','cfo_b'):
                if cv!=v: dis.append(k)
            elif abs(F(cv)-F(v))>rho: dis.append(k)
        rep='NO' if dis else ('UNRESOLVED' if miss else 'YES')
        flag_ok = (cf==col['flags'])
        rep_ok = rep==col['reproduction']
        if not(flag_ok and rep_ok):
            print('   MISMATCH',c['name'],'flags',cf,'vs',col['flags'],'rep',rep,'vs',col['reproduction'])
    print('   controls checked:',len(cols),' reproduction YES:',[c['name'] for c in cols if c['reproduction']=='YES'])

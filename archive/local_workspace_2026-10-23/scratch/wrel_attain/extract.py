"""Parse emitted PR #11 ITEM-2/3/8 JSON and do exact arithmetic on emitted values only. Computes no policy."""
import json
from fractions import Fraction as F
O='/workspace/scratch/pr11/head/c4_reliability_exact_check_v1/outputs/'
i2=json.load(open(O+'ITEM-2.json')); i3=json.load(open(O+'ITEM-3.json')); i8=json.load(open(O+'deviation_1/ITEM-8.json'))
PS=F(5313,10000)  # P(split read) per trial; also cross-checked against emitted T=1 rows
f=lambda s:F(s)
out={'H0':[],'H1':[],'item8':[]}
for r in i2['rows']:
    T=r['T']; g=lambda k,z: f(r[k][z])
    splitR={z:g('n_R',z)-g('n_R_unanimous',z) for z in 'SE'}
    nM={z:g('n_M',z) for z in 'SE'}
    fr={z:[f(x) for x in r['first_R'][z]] for z in 'SE'}
    tau=T-2
    row=dict(T=T,cr=r['cr'],cs=r['cs'],
      nR={z:str(g('n_R',z)) for z in 'SE'}, nR_u={z:str(g('n_R_unanimous',z)) for z in 'SE'},
      nR_split={z:str(splitR[z]) for z in 'SE'}, nM={z:str(nM[z]) for z in 'SE'},
      first_R={z:[str(x) for x in fr[z]] for z in 'SE'}, never_R={z:r['never_R'][z] for z in 'SE'},
      dR_split=str(splitR['S']-splitR['E']), dM_all=str(nM['E']-nM['S']),
      identity_nM_plus_splitR_eq_T_Psplit={z:(nM[z]+splitR[z]==T*PS) for z in 'SE'},
      nM_zero=all(nM[z]==0 for z in 'SE'),
      P_firstR_le_tau={z:str(sum(fr[z][:max(tau,0)],F(0))) for z in 'SE'},
      P_firstR_le_Tm1={z:str(sum(fr[z][:T-1],F(0))) for z in 'SE'},
      first_R_sums_ok={z:(sum(fr[z],F(0))+f(r['never_R'][z])==1) for z in 'SE'},
      planning_adv=r['planning_advantage_T'], adapt_info_adv=r['adaptive_information_advantage_T'])
    out['H0'].append(row)
for r in i3['rows']:
    T=r['T']; fr=[f(x) for x in r['first_R']]
    out['H1'].append(dict(T=T,cr=r['cr'],cs=r['cs'],nR=r['n_R'],nR_u=r['n_R_unanimous'],
      nR_split=str(f(r['n_R'])-f(r['n_R_unanimous'])),nM=r['n_M'],first_R=r['first_R'],never_R=r['never_R'],
      identity=(f(r['n_M'])+f(r['n_R'])-f(r['n_R_unanimous'])==T*PS)))
for s in i8['settings']:
    ref=s['reference']; p=ref['pattern']
    out['item8'].append(dict(T_SEP=s['T_SEP'],cr=s['cr'],cs=s['cs'],flags=ref['flags'],
      delta_R=p['delta_R'],delta_M=p['delta_M'],E_err_agent=p['E_err_agent'],E_err_baseline=p['E_err_baseline'],
      D_e_S=p['D_e_S'],D_e_E=p['D_e_E'],D_q_S=p['D_q_S'],D_q_E=p['D_q_E'],cfo=(p['cfo_a'],p['cfo_b']),
      donor_contrast=ref['donor_contrast'],cref_counts=ref['cref_counts'],lam=s['lambda'],label=s.get('label_before_replay')))
json.dump(out,open('/workspace/scratch/wrel_attain/extract_out.json','w'),indent=1)
print('H0 rows',len(out['H0']),'H1 rows',len(out['H1']))
for r in out['H0']:
    print(f"H0 T={r['T']:2} ({r['cr']},{r['cs']}) nRsplit S={r['nR_split']['S']} E={r['nR_split']['E']} dR={r['dR_split']} nM S={r['nM']['S']} E={r['nM']['E']} dM={r['dM_all']} id={r['identity_nM_plus_splitR_eq_T_Psplit']} P1st<=tau S={r['P_firstR_le_tau']['S']} E={r['P_firstR_le_tau']['E']} P1st<=T-1 S={r['P_firstR_le_Tm1']['S']} never S={r['never_R']['S']} E={r['never_R']['E']} sums={r['first_R_sums_ok']}")
for r in out['H1']:
    print(f"H1 T={r['T']} ({r['cr']},{r['cs']}) nR={r['nR']} nRu={r['nR_u']} nM={r['nM']} first={r['first_R']} never={r['never_R']} id={r['identity']}")
for r in out['item8']: print('I8',r)

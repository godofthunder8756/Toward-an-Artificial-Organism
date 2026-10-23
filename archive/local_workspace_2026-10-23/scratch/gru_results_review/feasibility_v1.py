import json, statistics as st, collections
d=json.load(open('/workspace/scratch/pr12/audit/gru_v1_3/results/results.json'))
fl=d['constants']['floor']; g=1e-10
U=collections.OrderedDict()
for c in d['checkpoints']:
    U.setdefault((c['pr'],c['arm']),[]).append(c)
tot=collections.Counter()
print('| PR | arm | C1 L_base min–max | C2 L_base min–max | C1-infeasible | C2-infeasible | checkpoint-infeasible (either) | C1 meets | R_exc min–max |')
for k,cs in U.items():
    c1=[c['C1']['L_base'] for c in cs]; c2=[c['C2']['L_base'] for c in cs]
    i1=sum(x<=fl+g for x in c1); i2=sum(x<=fl+g for x in c2)
    ie=sum((a<=fl+g) or (b<=fl+g) for a,b in zip(c1,c2)); ib=sum((a<=fl+g) and (b<=fl+g) for a,b in zip(c1,c2))
    m1=sum(c['C1']['label']=='meets-floor' for c in cs); re=[c['R_exc'] for c in cs]
    tot['i1']+=i1; tot['i2']+=i2; tot['ie']+=ie; tot['ib']+=ib; tot['m1']+=m1
    print(f"| {k[0]} | {k[1]} | {min(c1):.3g}–{max(c1):.3g} | {min(c2):.3g}–{max(c2):.3g} | {i1} | {i2} | {ie} | {m1} | {min(re):.3g}–{max(re):.3g} |")
print(tot)
# partial feasibility units
print('units fully infeasible (either):',[k for k,cs in U.items() if all((c['C1']['L_base']<=fl+g) or (c['C2']['L_base']<=fl+g) for c in cs)])
print('units mixed:',[k for k,cs in U.items() if 0<sum((c['C1']['L_base']<=fl+g) or (c['C2']['L_base']<=fl+g) for c in cs)<10])
allc=d['checkpoints']
mm=[c for c in allc if c['C1']['label']=='meets-floor']
print('89 R_exc median',st.median(c['R_exc'] for c in mm),'C2 Lbase median',st.median(c['C2']['L_base'] for c in mm),'C1 Lfull median',st.median(c['C1']['L_full'] for c in mm))
print('89: C1 Lfull > C2 Lbase count', sum(c['C1']['L_full']>c['C2']['L_base'] for c in mm))
print('89 in infeasible-units?', sum((c['C1']['L_base']<=fl+g) or (c['C2']['L_base']<=fl+g) for c in mm))
d2=[c['C2']['delta'] for c in allc]
print('C2 median',st.median(d2),'max',max(d2),'neg',sum(x<0 for x in d2),'zero',sum(x==0 for x in d2))
d1=[c['C1']['delta'] for c in allc]; print('C1 neg',sum(x<0 for x in d1),'median',st.median(d1))
# feasible-set C2 max delta, and C2 max delta minus floor
feas=[c for c in allc if c['C2']['L_base']>fl+g]
print('C2-feasible n',len(feas),'max C2 delta among feasible',max(c['C2']['delta'] for c in feas))
# C1 meets per unit
print({f"{k[0]}/{k[1]}":sum(c['C1']['label']=='meets-floor' for c in cs) for k,cs in U.items()})

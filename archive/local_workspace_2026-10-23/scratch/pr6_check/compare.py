import re
import json
from fractions import Fraction as F
S=json.load(open('spot_results.json'))
U={c['id']:c for c in json.load(open('../pr6/ex/cells_unpaid.json'))}
R={c['id']:c for c in json.load(open('../pr6/ex/cells_route.json'))}
P=json.load(open('../pr6/ex/cells_upkeep.json'))
def tup(s): return [F(x.split('Fraction(')[1].split(')')[0].replace(', ','/')) if 'Fraction' in x else F(x) for x in s.strip('()').split('), ')] if 'Fraction' in s else [F(t) for t in s.strip('()').split(', ')]
def parse(s):
    import re
    return [F(int(a),int(b)) for a,b in re.findall(r'Fraction\((-?\d+), (\d+)\)',s)]
ok=bad=0; lines=[]
def chk(name,mine,theirs):
    global ok,bad
    m=all(F(a)==F(b) for a,b in zip(mine,theirs)) and len(mine)==len(theirs)
    ok+=m; bad+=(not m); lines.append(f"{'MATCH' if m else 'MISMATCH'} {name} mine={[str(x) for x in mine]} pr={[str(x) for x in theirs]}")
for k,s in S.items():
    v=parse(s) if 'Fraction' in s else [F(s)]
    if k.startswith('unpaid/'):
        pid = k.replace('unpaid/clean/','unpaid/clean/a=-/')
        c=U[pid]; cl=c['classes']
        chk(pid,v,[cl['full']['value'],cl['cue_blind']['value'],cl['static_access']['value'],c['SEL']['gap'],c['ACC']['gap']])
    elif k.startswith('route/'):
        pid = k.replace('route/clean/','route/clean/a=-/')
        c=R[pid]; cl=c['classes']
        chk(pid,v[:3],[cl['full_route']['per_consumer'][0],cl['static_route']['per_consumer'][0],c['ROUTE']['gap']])
        nf,ns=map(int,s.strip('()').split(', ')[-2:])
        chk(pid+' optima(decoders per consumer)',[nf,ns],[cl['full_route']['n_optima_decoders'][0],cl['static_route']['n_optima_decoders'][0]])
    elif k.startswith('upk/clean'):
        B,d,vv,rr=re.match(r'upk/clean/B=(\d)/d=([\d/]+)/v=([\d/]+)/r=([\d/]+)$',k).groups(); B=int(B)
        cells=[c for c in P if c['B_up']==B and c['delta']==d and c['v']==vv and c['r']==rr and c['quantities']['UPK']['status']!='UNRESOLVED']
        ks=sorted(c['K'] for c in cells)
        gaps={(c['quantities']['UPK']['gap'],c['quantities']['UPK_cue']['gap']) for c in cells}
        exp=(str(v[3]),str(v[4]))
        m=gaps=={exp}
        ok+=m; bad+=(not m); lines.append(f"{'MATCH' if m else 'MISMATCH'} {k} mine(UPK,UPK_cue)={exp} pr={gaps} resolvedK={ks[0] if ks else None}..{ks[-1] if ks else None} n={len(ks)}")
    else: lines.append(f"INFO {k} {s}")
print('\n'.join(lines)); print('match',ok,'mismatch',bad)

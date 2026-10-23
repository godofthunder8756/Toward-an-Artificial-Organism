import re,hashlib,json,sys
C=open('/workspace/astra_consult19_response.txt').read().splitlines()
F=open('/workspace/review/frozen_recurrent_compensation_protocol_FINAL.md').read()
V1='/workspace/review/frozen_recurrent_compensation_protocol_draft_v1.md'
def norm(x): return re.sub(r'\s+',' ',x.replace('> ','').strip())
def L(a,b): return norm('\n'.join(C[a-1:b]))
FN=norm(F)
req={
 'F1 sentence':'R-FIX-48 matches CAND\'s trainable count, not stored count, allocation or optimization geometry.',
 'F1 replacement':L(13,13).strip('"'),
 'F2':'Freeze only `weight_hh_l0`. Training W_ih and the biases can change the recurrent dynamics despite that fixed matrix. Do not describe R-FIX as having an entirely untrained or fixed recurrent computation.',
 'F3':'Assert the full-core equality for all ten seeds, not just the two feasibility examples',
 'F4 replacement':L(23,23).strip('"'),
 'E1 rule':L(29,29).strip('"'),
 'E1 retain':L(31,31),
 'E1 acq':L(33,33),
 'E2 rule block':L(38,50),
 'E2 agreement':L(58,58),
 'E2 both':L(61,61),
 'E3 labels':L(65,65).strip('"'),
 'E3 zero a':'If all ten final evaluations resolve above target, use `TARGET NOT REACHED WITHIN DECLARED SEARCH`.',
 'E3 zero b':'Otherwise use `NO VERIFIED WITNESS FOUND`, with unresolved and invalid counts.',
 'E3 cand':L(72,72),
 'E4 checks':L(76,76).strip('"'),
 'E4 fixture':L(78,78),
 'E5 Cprefix':'C_prefix = PD(q*) - L_prefix(final)',
 'E5 Gprefix':'G_prefix = L_prefix(init) - L_prefix(final)',
 'E5 name':'within-run prefix-loss improvement.',
 'E5 nogate':'Neither quantity gates the target.',
 'E6 witness':L(91,91).strip('"'),
 'E6 acq':L(95,95).strip('"'),
 'E6 scope':L(99,99).strip('"'),
 'E7 FINIT':'11.55–17.36',
 'E7 insample':'in-sample descriptive subset',
 'approval Q':L(140,140).strip('"'),
 't26s1':"Approve fresh-seed GRU-8 training (seeds 400-409, 30 runs: normal plus two frozen-recurrent variants) for the frozen-recurrent compensation study once Astra clears the protocol?",
 'clearance':'Scientific clearance does not authorize training.',
}
for i,ln in enumerate(range(107,119),1): req[f'S13 row {i}']=C[ln-1].strip()
for i,ln in enumerate((122,124,126,128,130,132,134,136),1): req[f'S14 q{i}']=norm(C[ln-1])[3:]
ok=True
for k,v in req.items():
    hit=norm(v) in FN; ok&=hit; print(('PASS ' if hit else 'FAIL ')+k)
stale={'B_prefix':'B_prefix','11.5-16.9':'11.5-16.9','11.5–16.9':'11.5–16.9','11.5–16.86 old':'11.5–16.9','T <= 1 - T_BOUNDARY_TOL':'T ≤ 1 − T_BOUNDARY_TOL','|T−1| rule':'|T − 1| ≤ T_BOUNDARY_TOL','old eligibility':'Eligibility (A-LEARN analogue)','old ledger NOT SUPPORTED':'Q-NECESSITY for this class and target is **NOT SUPPORTED**','effectively tests':'effectively tests the XOR','VAL reported descriptively':'VAL is reported descriptively only','old seeds-searched':'20 R-FIX runs were searched','draft status':'Status:** DRAFT','not binding for':'not binding for, the unrestricted','blanket unchanged':'Q-CAUSE, Q-LEARN and Q-EXIST are unchanged in every case'}
for k,v in stale.items():
    hit=v in F; ok&=not hit; print(('PASS absent ' if not hit else 'FAIL present ')+k)
# appendix order, F-INIT range vs T_existing
order=[m for m in re.findall(r'^## Appendix ([A-D])',F,re.M)]; print('appendix order',order, 'PASS' if order==['A','B','C','D'] else 'FAIL'); ok&=order==['A','B','C','D']
R=json.load(open('/workspace/scratch/frozen_comp/T_existing.json'))
vals=[r[0] for k in R if k.endswith('f_init') for r in R[k]]
lo,hi=min(vals),max(vals); cons=round(lo,2)==11.55 and round(hi,2)==17.36
print('F-INIT T_existing %.4f-%.4f vs Astra 11.55-17.36:'%(lo,hi),'CONSISTENT' if cons else 'DISAGREES'); ok&=cons
print('v1 sha', hashlib.sha256(open(V1,'rb').read()).hexdigest())
print('ALL PASS' if ok else 'SOME FAIL')

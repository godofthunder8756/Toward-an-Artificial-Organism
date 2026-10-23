from fractions import Fraction as F
import io,contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import demo as D
JS,JE=D.JS,D.JE
def post(J):
    po=D.marg_obs(J); return {o:J.get((1,o),0)/p for o,p in po.items()}
pS,pE=post(JS['recheck']),post(JE['recheck'])
gap=max(abs(pS[o]-pE[o]) for o in pS); o=max(pS,key=lambda o:abs(pS[o]-pE[o]))
print('max |P_S(X=1|y,y\') - P_E(X=1|y,y\')| =',float(gap),'at obs',o,float(pS[o]),float(pE[o]))
dec_diff=sum(1 for o in pS if (pS[o]>F(1,2))!=(pE[o]>F(1,2)) and pS[o]!=F(1,2) and pE[o]!=F(1,2))
print('observations where post-recheck Bayes decision differs between regime models:',dec_diff,'of',len(pS))
p0S,p0E=post(JS['none']),post(JE['none']); print('pre-check posterior max gap:',max(abs(p0S[o]-p0E[o]) for o in p0S))
# split-state gains (exact) and cost region where optimal action differs
cS,cE=D.cS['split'],D.cE['split']
gRs=cS['recheck']-cS['none']; gRe=cE['recheck']-cE['none']; gM=cS['resample']-cS['none']; assert gM==cE['resample']-cE['none']
print('split gains: recheck S',gRs,float(gRs),'recheck E',gRe,float(gRe),'resample (both)',gM,float(gM))
print('Region (split states) where S-optimal=RECHECK and E-optimal≠RECHECK: c_r < gRs, c_r < c_s - (gM-gRs), and (c_r > gRe or c_r > c_s-(gM-gRe)) ; gM-gRs=%s (%.5f), gM-gRe=%s (%.5f)'%(gM-gRs,float(gM-gRs),gM-gRe,float(gM-gRe)))

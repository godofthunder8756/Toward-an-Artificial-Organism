import re
F=open('/workspace/review/first_order_control_protocol_FINAL.md').read()
A=open('/workspace/astra_consult17_response.txt').read()
E=open('/workspace/review/pr8_errata_v3_interpretation_note.md').read()
def quotes(t): return [m.strip() for m in re.findall(r'> "(.+?)"\s*$', t, re.M)]
req = {
 'label_success':'GRADED JOINT REVERSION EXCEEDS BOTH FIRST-ORDER-MATCHED AND ISOTROPIC CONTROLS (PREFIX FUNCTION): REPLICATED',
 'label_fail':'JOINT FO-AND-ISO GRADED REVERSION CRITERION NOT MET',
 'fail_sentence':'The joint FO-and-ISO criterion was not met; no reduction was identified.',
 'no_auto_attr':'Do not automatically attribute that failure to FO matching: ISO could be the failed condition.',
 'collapse5':'For a collapsed block, set e_jk := d_k for every draw. The block has no randomized spread. Its secondary comparison is ineligible.',
 'reff':'R_eff^2 = sum of r_k^2 over non-collapsed blocks',
 'gzero6':'G_ZERO is a diagnostic threshold only. For every nonzero gradient, use the projection construction and its matching checks. For an exactly zero gradient, use the norm-matched isotropic draw; its first-order match is exact. Numerical inability to construct or validate a nonzero-gradient match is an integrity failure.',
 'diagname':'NEGLIGIBLE FIRST-ORDER SCALE',
 'fd':'abs(FD - dot(G, direction)) <= 1e-10 + 1e-6*norm(G)',
 'radius':'abs(norm(d_k)^2 - norm(p_k)^2 - r_k^2)',
 'unevaluable8':'After the E1 prerequisite, if more than two distinct seeds are invalid or have a collapsed control family for the target, report UNRESOLVED (insufficient evaluable seeds). Otherwise retain the denominator of ten.',
 'manifest9':'Before Phase A, freeze the construction code, tolerances, generator seeds and base Gaussian draw manifests for both phases. After each checkpoint and gradient are available, construct and hash the transformed paths before evaluating their dose curves. Record checkpoint, gradient and transformed-path hashes together.',
 'ckpt10':'does not train the network or modify its saved checkpoint',
 'gh':'gh_k = g_k / norm(g_k)        # unit gradient, when nonzero',
 'gk':'g_k  = vec(block k of G)       # unnormalized gradient',
 'D_FO':'D_FO  = (AUC_REV - max_j AUC_FO,j > eps0)', 'D_ISO':'D_ISO = (AUC_REV - max_j AUC_ISO,j > eps0)',
 'joint':'Joint pass = valid and eligible and D_FO and D_ISO and M',
 'residual_name':'residual after subtracting the initial tangent contribution',
 'O10':'Approve fresh-seed GRU-8 training (seeds 300-309, 30 runs, PR #7 recipe) for graded reversion confirmation against both first-order-matched and isotropic controls once Astra clears the protocol?',
 'widget_q':"Approve fresh-seed GRU-8 training (seeds 300-309, 30 runs) for the first-order-matched control confirmation once Astra clears the protocol?",
 'widget_a':'Yes, approve it once Astra clears it.', 'widget_id':'t23s2', 'time':'1:05 AM ET',
 'O9':'Yes: evaluation-only Phase A may proceed under the described standing authorization after these edits and hashing. No training is authorized by this ruling.',
 'O1_nofam':'Do not add the one-sided family or curvature matching here.',
 'foreign':'hidden-unit coordinates differ across seeds, so transplanting one matrix can create coordinate incompatibility',
}
bad=0
for k,s in req.items():
    ok = s in F
    if not ok: bad+=1
    print('OK ' if ok else 'MISSING', k)
# Astra block quotes (edits 2,3, O1 note) must appear verbatim
for q in quotes(A):
    target = E if q.startswith('Exploratory finite-difference') else F
    ok = q in target; bad += not ok
    print('OK ' if ok else 'MISSING', 'astra-quote:', q[:60])
# rulings table verbatim
for line in A.splitlines():
    m=re.match(r'\| (O\d+) \| (.+) \|$', line)
    if m:
        txt=m.group(2).replace('"','"')
        ok = txt in F; bad+=not ok; print('OK ' if ok else 'MISSING', 'ruling', m.group(1))
for a in ['accept, with explicit h4 detachment','amend the radius validation as in edit 7','accept; use `gh_k` consistently','amend as in edits 5, 6 and 8','accept as reporting only, with edit 10','confirmed subject to O9']:
    ok=a in F; bad+=not ok; print('OK ' if ok else 'MISSING','A-ruling',a)
stale = ['FIRST-ORDER-MATCHED GRADED REVERSION CRITERION NOT MET','EXCEEDS FIRST-ORDER-MATCHED PERTURBATION','FIRST-ORDER TERM NUMERICALLY ZERO','FIRST-ORDER MATCH VACUOUS',
 'e_jk := p_k','RADIUS_AGREE_TOL','does not alter any network','degenerate control family)','DRAFT FOR ASTRA','PENDING','Option J','isotropic descriptive','(descriptive; retained per spec)',
 'GRAD_CHECK_TOL·‖G‖_F, with GRAD_CHECK_TOL = 1e-6','ĝ','set a_k := 0']
for s in stale:
    hit = s in F; bad+=hit; print('STALE' if hit else 'clean', repr(s))
print('TOTAL PROBLEMS', bad)

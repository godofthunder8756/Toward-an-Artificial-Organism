import re, hashlib
raw_path='/workspace/astra_consult36_response.txt'
rawb=open(raw_path,'rb').read()
assert hashlib.sha256(rawb).hexdigest().startswith('c8342d5a')
raw=rawb.decode('utf-8')
lines=raw.splitlines()
edits={}; notes={}
for i,l in enumerate(lines):
    m=re.fullmatch(r'E36-(\d+):',l.strip())
    if m:
        n=int(m.group(1))
        q=[x for x in lines[i+1:i+4] if x.startswith('> ')]
        assert len(q)==1,(n,q)
        edits[n]=q[0][2:]
        # following unquoted note paragraph (before next E36 or section)
        j=lines.index(q[0],i)+1
        para=[]
        while j<len(lines) and not re.fullmatch(r'E36-\d+:',lines[j].strip()) and not re.match(r'\d+\. ',lines[j]):
            if lines[j].strip(): para.append(lines[j])
            j+=1
        if para: notes[n]=para
assert sorted(edits)==list(range(1,15))
for n,t in edits.items(): assert ('> '+t) in raw
s=lines.index('6. What must be in the freeze manifest')
man=[l[2:] for l in lines[s:s+16] if l.startswith('- ')]
assert len(man)==12
out=[]
A=out.append
A('# C-κ oracle-only scope record v1.3: Astra #36 named edits E36-1..14 (DRAFT for freeze. Not sealed, nothing run)')
A('')
A('Constitutive agent, 2026-10-22 (ET). **Additive.** Leaves unchanged: v1 (`1b450bcf…`), v1.1 (`e40c288f01728a6f5a68338fa23e5cf15d75c78d99d03e61bd31821b53f11b0c`), v1.2 (`7e15e812c9ddfa17369d99f97d6dee5658aedf0dbdb9e37c947300bfc1411d7d`). Source: Astra #36, `/workspace/astra_consult36_response.txt`, sha256 `c8342d5aa27c659dda5657e1e9ad70006a5e30759cc43eb25101d5546e756002`. Verdict (verbatim, L1): "FREEZE WITH NAMED EDITS for the oracle-only package. This does not clear checkpoint inference or establish a complete neural acceptance protocol."')
A('')
A('## 0. Precedence (frozen)')
A('**v1.3 (this file) > v1.2 > v1.1.** Where texts conflict, the higher one governs. Within v1.3, the verbatim E36 text in §1 governs over my supersession map (§2) and declared values (§3); if §2 or §3 is found to conflict with §1, §1 governs and the conflict is resolved additively before execution (Astra L162). Nothing in v1.3 authorizes the later inference study (E36-1).')
A('')
A('## 1. E36-1..14, verbatim')
A('Extracted by script from the raw file and each checked as an exact substring of it (`> ` prefix included). Astra\'s unquoted note directly following an edit is reproduced verbatim as "Note".')
A('')
for n in range(1,15):
    A(f'**E36-{n}.**'); A(''); A('> '+edits[n]); A('')
    if n in notes:
        for p in notes[n]: A('Note (verbatim, unquoted in source): '+p)
    A('')
A('## 2. Supersession map (what in v1.1/v1.2 each edit replaces)')
rows=[
('v1.1 L44, "ratio of linear functions of b"','E36-2','Φ(p,u) is a ratio of linear functions of p, not of the chart θ. Notation: p = four-state vector, θ = (μ_x, μ_y, κ), perturbed p\' = inverse_chart(θ(p)+Δ).'),
('v1.1 O5 L110–111, "≈ H·sin²θ"','E36-2','Withdrawn. O5 is descriptive with no H·sin²θ reading. "κ zeroed" = κ component of Δ set to 0, baseline κ kept.'),
('v1.1 O6 L84 "B (rank 3) and B_μ (rank 2)"; v1.2 D-4 "rank ≤ 3"','E36-3','Weighted LS on ALL outputs, fit-prefix law weights, all continuations; same maps for ALL/MARG/XOR; no rank constraint; minimum-norm solver frozen in manifest. Applies to O6 and O7; carried as a design commitment for §6.'),
('v1.1 §4 O6 validity; v1.2 D-5','E36-4, E36-5','One common scoreable-edit mask: actual perturbed belief and both predicted beliefs must pass p ≥ 10⁻⁶. Losses and S on the same mask; count and law-mass coverage per fold and size; ≥ 75% by both in every fold for the oracle reference. v1.1 §5\'s "≥ 75% of O6 edits valid" is replaced by this per-fold rule.'),
('v1.1 §6 L141 pooling; v1.1 O6 L92 "pooled over folds"','E36-5','Pool occurrences with original w(a,u), normalize once over pooled scoreable occurrences. No averaging of fold-normalized losses. Losses are conditional on the common mask; retained mass reported.'),
('v1.1 O7 L99 "rank 2 expected … anything else is PIPELINE INVALID"; v1.1 O7 as a fixture whose failure stops','E36-6, E36-7','O7 is exploratory. Invalid quadratic baseline → RESTRICTED COMPARATOR NOT ADMISSIBLE (no stop, no refit). Rank ≤ 2; lower resolved rank reported; a resolved third direction → integrity diagnosis; ambiguity → unresolved. A demonstrated implementation contradiction still stops (Astra L109). Execution order O1→O2→O6→O7→O3→O4→O5 unchanged.'),
('v1.1 L68–73 rank rule','E36-8','Equality at 10⁻⁶ or 10⁻¹⁰ falls in the unresolved band. σ_1 = 0 exactly → rank 0 without forming ratios. σ_1 always reported.'),
('v1.1 L93 / v1.2 D-1 "neural achievable gain"','E36-9','Replace with: "for a neural checkpoint, L_μ is an upper bound on possible squared-error improvement, not a guarantee of attainable gain." O6 reports measured gain H\\* − L_full alongside H\\*.'),
('v1.2 Astra question 1 (my "≈71% RMS κ error" reading, and the Delegate\'s E_s/K/e arithmetic)','E36-9','**Withdrawn.** Exact identity (Astra L48): L_μ − L_full = 2⟨r_μ, d⟩ − ‖d‖². Floor (a) halves total comparator error; it is not a κ-component bound. L_full ≤ L_μ/2 kept, not tightened.'),
('v1.2 D-3(i) noise guard (10⁻¹²)','E36-10','Substantive pooled floor L_μ/S ≥ 0.02 per counted size and group (ALL and MARG). The 10⁻¹² band is retained only as a reported numerical boundary marker; it no longer defines headroom status. Absolute response-magnitude floor is still required before inference (E36-1).'),
('v1.2 D-3(ii) seed roll-up and package labels','E36-11','Replaced in full by E36-11\'s disjoint p/f/u/h counts and ordering. An absolute low-response outcome counts in h with its reason kept.'),
('v1.1 §6 L129–130 counted ε as "beyond linear-regime references"','E36-12','Counted sizes are finite commitments, not evidence of nonlinearity. Finite response, Jacobian prediction and discrepancy reported at every size.'),
('v1.2 D-2 step 0','E36-13','Order: O1, then O2, then the first 1,000 O6 propagations (retained, not recomputed). Remaining counts are frozen scheduled upper counts minus completed. Projection is a heuristic, not a bound; overhead estimated separately. A projection stop is reported as PROJECTION HALT, distinct from CAP REACHED.'),
('v1.1 §7 L151 cap; v1.1 §7 L162 manifest with output hashes','E36-14','Clock starts before interpreter imports. Hard cap enforced independently of the projection. Manifest immutable; output hashes and run accounting go in a separate post-run index referencing the manifest sha.'),
('v1.1 §5 at ε_syn = 0.1','Astra L30','Other ε_syn sizes reported but never replace a failed reference.'),
]
A('| v1.1/v1.2 text | Edit | Now reads |')
A('| --- | --- | --- |')
for r in rows: A('| '+' | '.join(r)+' |')
A('')
A('## 3. Values declared now (required by E36-3, E36-6, E36-8 and Astra L115; frozen before execution)')
A('Implementation may not change these. If one proves unworkable, it is resolved additively before execution (Astra L162).')
A('- **§5 numerical boundary band.** A §5 statistic x compared with threshold t is BOUNDARY if |x − t| ≤ 10⁻⁶·t. BOUNDARY is reported as its own outcome, distinct from HEADROOM NOT MET, and is not a pass.')
A('- **Zero response energy.** If S = 0 exactly in a pooled cell, R\\* and L_μ/S are UNDEFINED. The oracle cell reads ZERO RESPONSE (low sensitivity), not a pass, not PIPELINE INVALID, and no ratio is replaced by 0. For §6 it is an h outcome with reason "zero response".')
A('- **Solver.** All least-squares fits use `numpy.linalg.lstsq(A, y, rcond=None)` (SVD, minimum-norm) on the √w-weighted system, float64. B_μ is fitted on the reduced 2-column chart design (κ row fixed at 0).')
A('- **O7 basis.** g(μ_x, μ_y) = c₀ + c₁μ_x + c₂μ_y + c₃μ_x² + c₄μ_xμ_y + c₅μ_y², raw (unscaled) monomials, P-weighted least squares over the 16 reachable (μ, κ), minimum-norm via the solver above. Baseline validity (p ≥ 10⁻⁶ at (μ_x, μ_y, g)) is checked per prefix before derivatives.')
A('- **RNG and Q.** `numpy.random.Generator(PCG64(seed))`. Q (8×3, seed 35006) and Q₂ (8×2, seed 35007): one `standard_normal((8, k))` draw, row-major; reduced `numpy.linalg.qr`; columns sign-flipped so diag(R) > 0. Directions (O6 seed 35016, O4 seed 35004, §6 seed 36000+seed_id): one `standard_normal((n, dim))` draw, each row divided by its Euclidean norm; both signs taken as +v then −v in row order.')
A('- **Threads.** One process, `OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=1`, CPU affinity pinned to one core, `RLIMIT_AS` = 4 GiB.')
A('')
A('## 4. Draft MANIFEST CONTENTS checklist (mirrors Astra #36 §6, L149–160, items verbatim)')
A('Each item is filled by the implementer and checked before sealing. "Source" says where the frozen value already lives.')
A('')
src=[
'sha256 of v1.1, v1.2, this file; precedence from §0.',
'PR #4 `results.json` @ `5d9d8a7` (re-hashed from the commit; local copy `bf2de92c…`), certificate, `TWOSTREAM_PROTOCOL_v1.md`, every implementation file with sha256.',
'v1.1 §1 (four transitions), §3 groups; O2 closed form + central differences at 10⁻⁶; notation per E36-2.',
'v1.1 §2 folds; v1.1 §3 weights; E36-4/E36-5 mask, pooling and ≥75% count and mass coverage per fold.',
'v1.1 O6/O7 constructions; E36-3 objectives; §3 basis, solver and minimum-norm convention.',
'§3 RNG, draw order, normalization, QR and sign rule; seeds 35004, 35006, 35007, 35016, 36000+seed_id.',
'v1.1 §5 and E36-10 thresholds; ε_syn vs ε units (v1.2 D-1); §3 boundary band and zero-denominator rule; E36-8 rank rule; O1/O2/O6 fixture tolerances (exact; 10⁻⁸; 10⁻⁹).',
'Stops: O1, O2, O6 failure or a demonstrated O7 implementation contradiction → PIPELINE INVALID. Descriptive only: O7 admissibility and rank, O3–O5. Determines §5: O6 at ε_syn = 0.1.',
'Per-stage scheduled upper counts (≈1×10⁶ total, v1.2 D-6); E36-13 projection; order O1→O2→O6→O7→O3→O4→O5; E36-14 hard cap from before imports.',
'Python/NumPy versions, float64 throughout (exact rationals in O1), §3 affinity, threads and memory.',
'`results.json`, `REPORT.md`, run log; partial outputs kept on any stop; separate post-run hash index (E36-14).',
'Filed by the Specialist after sealing; references the manifest sha.',
]
for k,(m,sv) in enumerate(zip(man,src),1):
    A(f'{k}. [ ] **{m}**')
    A(f'   - Source: {sv}')
A('')
A('## 5. Claim ceiling')
A('Unchanged from v1.1 §8 and Astra L164: oracle-only. No neural, acquisition, S12, S15, C4 or consciousness finding. No checkpoint is opened. Nothing runs before the manifest is sealed and the application is filed.')
open('/workspace/review/ckappa_oracle_scope_record_v1_3_E36.md','w',encoding='utf-8').write('\n'.join(out)+'\n')
# verify verbatim round-trip
txt=open('/workspace/review/ckappa_oracle_scope_record_v1_3_E36.md',encoding='utf-8').read()
for n,t in edits.items(): assert f'**E36-{n}.**\n\n> {t}\n' in txt
for m in man: assert m in txt
print('ok', len(edits), len(man))

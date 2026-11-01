# Builds the #44 ASCII send parts. Does NOT start any server and sends nothing.
import re, hashlib, os, subprocess
os.chdir('/workspace/astra_serve44')
def sha(b): return hashlib.sha256(b).hexdigest()
def foot(b): return b + ('sha256 of all content above this line: ' + sha(b) + '\n').encode()
EXP = {'review/trackB_instrument_validation_scope_v3_3_merged_RD.md': '307bab21',
       'review/trackB_scope_v3_3_addendum_RD.md': '421f1ec5',
       'review/trackB_instrument_validation_scope_v3_2_merged_RD.md': '98e11d2c',
       'astra_consult43_response.txt': '9a46cb81', 'astra_consult42_response.txt': 'e438e329',
       'astra_consult41_response.txt': '3f3b1b87'}
if not os.path.exists('governing_sha256.txt'):
    r = subprocess.run(['sha256sum'] + list(EXP), cwd='/workspace', capture_output=True, text=True, check=True)
    open('governing_sha256.txt', 'w').write(r.stdout)
r = subprocess.run(['sha256sum', '-c', '/workspace/astra_serve44/governing_sha256.txt'], cwd='/workspace', capture_output=True, text=True)
print(r.stdout.strip())
if r.returncode != 0: raise SystemExit('SHA MISMATCH - not building')
tab = {l.split()[1]: l.split()[0] for l in open('governing_sha256.txt') if l.strip() and not l.startswith('sha256 of')}
assert set(tab) == set(EXP)
for f, p in EXP.items():
    if not tab[f].startswith(p): raise SystemExit('PREFIX MISMATCH %s' % f)
for f in ('review/trackB_instrument_validation_scope_v3_3_merged_RD.md', 'review/trackB_scope_v3_3_addendum_RD.md',
          'review/trackB_instrument_validation_scope_v3_2_merged_RD.md'):
    L = open('/workspace/' + f, 'rb').read().splitlines(True)
    assert sha(b''.join(L[:-1])) == L[-1].decode().split(': ')[1].strip(), 'footer mismatch ' + f
print('prefix check OK (%d files); v3.3, addendum and v3.2 footers OK' % len(EXP))
exec(open('pieces.py').read())
r43 = open('/workspace/astra_consult43_response.txt').read().splitlines()
r42 = open('/workspace/astra_consult42_response.txt').read().splitlines()
r41 = open('/workspace/astra_consult41_response.txt').read().splitlines()
assert '"' + CEILING + '"' in r41[303], 'ceiling not verbatim at #41 L304'
for n, q in Q43: assert q in r43[n-1], ('#43', n, q)
for n, q in Q42: assert q in r42[n-1], ('#42', n, q)
assert r43[192] in HEAD_FULL.replace('\n', ' ') or 'VERDICT: REVISE, with E43-1 through E43-8' in HEAD_FULL
for n, q in [(142, 'The external-substitution comparison is eligible, interface-compatible, and classified NOT SUBSTITUTABLE WITHIN MARGIN.'),
             (57, 'The declared training-increase criterion was not met.')]:
    assert q in r43[n-1] and q in HEAD_FULL, n
V33 = tab['review/trackB_instrument_validation_scope_v3_3_merged_RD.md'][:8]; ADD = tab['review/trackB_scope_v3_3_addendum_RD.md'][:8]
HF = HEAD_FULL.replace('{V33}', V33).replace('{ADD}', ADD).replace('{CEILING}', CEILING)
M = {'μ':'mu','×':'x','ε':'eps','κ':'kappa','‖':'||','·':'*','−':'-','→':'->','§':'S','∈':'in','≈':'~','…':'...','≥':'>=','≤':'<=','–':'-','—':'-','“':'"','”':'"','’':"'",'‘':"'",'ρ':'rho','β':'beta','σ':'sigma','γ':'gamma','Δ':'Delta','χ':'chi'}
def asc(t):
    for k, v in M.items(): t = t.replace(k, v)
    t = t.replace('**', '').replace('`', '')
    bad = sorted({c for c in t if ord(c) > 127})
    if bad: raise SystemExit('nonascii %r' % bad)
    return t
body = re.sub(r'\n{3,}', '\n\n', asc(HF))
for w in ('conscious', 'sentien', 'autopoie', r'\balive\b', r'\bC[45]\b'):
    for m in re.finditer(w, body, re.I):
        ctx = body[max(0, m.start()-60):m.end()+40].lower()
        assert 'no consciousness' in ctx, (w, ctx)
bb = foot(body.encode()); open('c44_body.md', 'wb').write(bb)
cov = ('# Track B Astra consult #44 cover note v1 (RD) - DRAFT, NOT FROZEN, DESIGN REVIEW ONLY, NOTHING RUNS\n\nPacket: /workspace/astra_serve44/c44_body.md '
       '(this note is its cover section, verbatim). Primary: merged scope v3.3 ' + V33 + '.\n\n' +
       asc(COVER.replace('{V33}', V33).replace('{ADD}', ADD).replace('{CEILING}', CEILING)).strip() + '\n\n')
cp = '/workspace/review/trackB_astra44_cover_note_v1_RD.md'; cb = foot(cov.encode())
if os.path.exists(cp):
    if open(cp, 'rb').read() != cb: raise SystemExit('cover note exists and differs - not overwriting')
else: open(cp, 'wb').write(cb)
lines = body.split('\n'); parts = []; cur = ''; LIM = 2780
for l in lines:
    while len(l) > LIM:
        cut = l.rfind('. ', 0, LIM - len(cur) - 1) if cur else l.rfind('. ', 0, LIM)
        if cut < 200:
            if cur: parts.append(cur); cur = ''
            cut = l.rfind('. ', 0, LIM)
        cur += l[:cut+1] + '\n'; parts.append(cur); cur = ''; l = l[cut+2:]
    if len(cur) + len(l) + 1 > LIM and cur: parts.append(cur); cur = ''
    cur += l + '\n'
if cur.strip(): parts.append(cur)
n = len(parts)
for f in os.listdir('send'): os.remove('send/' + f)
for i, p in enumerate(parts, 1):
    if i < n: t = '[c44 part %d/%d]\n' % (i, n) + p.rstrip('\n') + '\n[end of c44 part %d/%d - more coming, do not answer yet]' % (i, n)
    else: t = '[c44 part %d/%d]\n' % (i, n) + p.rstrip('\n') + '\n[END OF CONSULT #44 PACKET - all %d parts sent. Please answer now.]' % n
    assert all(ord(c) < 128 for c in t) and len(t) <= 2900, (i, len(t))
    open('send/c44_%d.txt' % i, 'w').write(t)
re_body = ''.join(open('send/c44_%d.txt' % i).read().split('\n', 1)[1].rsplit('\n', 1)[0] + '\n' for i in range(1, n+1))
assert re.sub(r'\s+', ' ', re_body).strip() == re.sub(r'\s+', ' ', body).strip(), 'reassembly mismatch'
man = '# c44 send-part manifest (send parts carry no footer, per the #43 packet precedent; this manifest covers them)\n'
man += ''.join('%s  send/c44_%d.txt  %d chars\n' % (sha(open('send/c44_%d.txt' % i, 'rb').read()), i, len(open('send/c44_%d.txt' % i).read())) for i in range(1, n+1))
open('send_manifest.txt', 'wb').write(foot(man.encode()))
print(n, len(body), sha(bb), [len(open('send/c44_%d.txt' % i).read()) for i in range(1, n+1)])
print('cover', sha(open(cp, 'rb').read()), len(cov))
# sha256 of all content above this line: edb060f7c25a8f3e85fd40b3d695bb1b771ce4c9dbce06c61a7da474f0e7000b

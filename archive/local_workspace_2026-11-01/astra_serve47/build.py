# Builds the #47 ASCII send parts. Does NOT start any server and sends nothing.
import re, hashlib, os, subprocess
os.chdir('/workspace/astra_serve47')
def sha(b): return hashlib.sha256(b).hexdigest()
def foot(b): return b + ('sha256 of all content above this line: ' + sha(b) + '\n').encode()
V36F = 'review/trackB_instrument_validation_scope_v3_6_merged_RD.md'; ADDF = 'review/trackB_scope_v3_6_addendum_RD.md'
V35F = 'review/trackB_instrument_validation_scope_v3_5_merged_RD.md'
EXP = {V36F: 'ab80afa5', ADDF: '9bbde57e', V35F: '80ed7a1b',
       'astra_consult46_response.txt': 'e902a184', 'astra_consult45_response.txt': 'de85c4ab',
       'astra_consult42_response.txt': 'e438e329', 'astra_consult41_response.txt': '3f3b1b87'}
if not os.path.exists('governing_sha256.txt'):
    r = subprocess.run(['sha256sum'] + list(EXP), cwd='/workspace', capture_output=True, text=True, check=True)
    open('governing_sha256.txt', 'wb').write(foot(r.stdout.encode()))
r = subprocess.run(['sha256sum', '-c', '/workspace/astra_serve47/governing_sha256.txt'], cwd='/workspace', capture_output=True, text=True)
print(r.stdout.strip())
if 'FAILED' in r.stdout or not all(f + ': OK' in r.stdout for f in EXP): raise SystemExit('SHA MISMATCH - not building')
G = open('governing_sha256.txt', 'rb').read().splitlines(True)
assert sha(b''.join(G[:-1])) == G[-1].decode().split(': ')[1].strip(), 'governing footer mismatch'
tab = {l.split()[1]: l.split()[0] for l in open('governing_sha256.txt') if l.strip() and not l.startswith('sha256 of')}
assert set(tab) == set(EXP)
for f, p in EXP.items():
    if not tab[f].startswith(p): raise SystemExit('PREFIX MISMATCH %s' % f)
for f in (V36F, ADDF, V35F):
    L = open('/workspace/' + f, 'rb').read().splitlines(True)
    assert sha(b''.join(L[:-1])) == L[-1].decode().split(': ')[1].strip(), 'footer mismatch ' + f
m36 = open('/workspace/' + V36F, 'rb').read(); v35 = open('/workspace/' + V35F, 'rb').read(); add = open('/workspace/' + ADDF, 'rb').read()
assert b''.join(v35.splitlines(True)[:-1]) in m36 and add in m36, 'merged v3.6 does not carry inputs verbatim'
assert m36.index(add) > m36.index(b''.join(v35.splitlines(True)[:-1])), 'order'
print('prefix check OK (%d files); v3.6, addendum and v3.5 footers OK; v3.6 carries v3.5 + addendum verbatim' % len(EXP))
# the addendum's own quote/arithmetic checker must pass
r = subprocess.run(['/tmp/sv/bin/python', '/workspace/scratch/v36/check_addendum36.py'], capture_output=True, text=True)
print(r.stdout.strip());
if r.returncode: raise SystemExit('addendum check failed')
exec(open('pieces.py').read())
def rl(n): return [l.replace('\ufffd', '') for l in open('/workspace/astra_consult%d_response.txt' % n, encoding='utf-8', errors='replace').read().splitlines()]
r46, r45, r42, r41 = rl(46), rl(45), rl(42), rl(41)
assert '"' + CEILING + '"' in r41[303], 'ceiling not verbatim at #41 L304'
for n, q in Q46: assert q in r46[n-1], ('#46', n, q)
for n, q in Q45: assert q in r45[n-1], ('#45', n, q)
for n, q in Q42: assert q in r42[n-1], ('#42', n, q)
V36 = tab[V36F][:8]; ADD = tab[ADDF][:8]
body = BODY.replace('{V36}', V36).replace('{ADD}', ADD).replace('{CEILING}', CEILING)
for n, q in Q46 + Q45 + Q42: assert q in body, ('quote missing from body', n)
bad = sorted({c for c in body if ord(c) > 127})
if bad: raise SystemExit('nonascii %r' % bad)
body = re.sub(r'\n{3,}', '\n\n', body)
assert len(body) <= 15000, ('body too long', len(body))
for w in ('conscious', 'sentien', 'autopoie', r'\balive\b', r'\bC[45]\b'):
    for m in re.finditer(w, body, re.I):
        ctx = body[max(0, m.start()-60):m.end()+40].lower()
        assert 'no consciousness' in ctx, (w, ctx)
for k in ('E46-1', 'E46-2', 'E46-3', 'E46-4', 'E47-n', 'VERDICT', 'High effort', 'Q0.', 'Q6.'): assert k in body, k
bb = foot(body.encode()); open('c47_body.md', 'wb').write(bb)
lines = body.split('\n'); parts = []; cur = ''; LIM = 2450
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
    if i < n: t = '[c47 part %d/%d]\n' % (i, n) + p.rstrip('\n') + '\n[end of c47 part %d/%d - more coming, do not answer yet]' % (i, n)
    else: t = '[c47 part %d/%d]\n' % (i, n) + p.rstrip('\n') + '\n[END OF CONSULT #47 PACKET - all %d parts sent. Please answer now.]' % n
    assert all(ord(c) < 128 for c in t) and len(t) <= 2600, (i, len(t))
    open('send/c47_%d.txt' % i, 'w').write(t)
re_body = ''.join(open('send/c47_%d.txt' % i).read().split('\n', 1)[1].rsplit('\n', 1)[0] + '\n' for i in range(1, n+1))
assert re.sub(r'\s+', ' ', re_body).strip() == re.sub(r'\s+', ' ', body).strip(), 'reassembly mismatch'
man = '# c47 send-part manifest (send parts carry no footer, per the #43-#46 packet precedent; this manifest covers them)\n'
man += ''.join('%s  send/c47_%d.txt  %d chars\n' % (sha(open('send/c47_%d.txt' % i, 'rb').read()), i, len(open('send/c47_%d.txt' % i).read())) for i in range(1, n+1))
open('send_manifest.txt', 'wb').write(foot(man.encode()))
for l in open('send_manifest.txt'):
    if l.startswith('#') or l.startswith('sha256 of'): continue
    h, f = l.split()[:2]; assert sha(open(f, 'rb').read()) == h, f
M = open('send_manifest.txt', 'rb').read().splitlines(True); assert sha(b''.join(M[:-1])) == M[-1].decode().split(': ')[1].strip()
assert sorted(os.listdir('send')) == sorted('c47_%d.txt' % i for i in range(1, n+1)), 'stray files in send/'
S = open('serve.py', 'rb').read().splitlines(True); assert sha(b''.join(S[:-1])) == S[-1].decode().split(': ')[1].strip(), 'serve.py footer'
assert b"astra_consult47_response.txt" in S[2] and b"8840" in b''.join(S) and b"8841" in b''.join(S)
print('BUILD OK: %d parts, body %d chars, body sha256 %s, manifest sha256 %s, part sizes %s' % (n, len(body), sha(bb), sha(open('send_manifest.txt','rb').read()), [len(open('send/c47_%d.txt' % i).read()) for i in range(1, n+1)]))
# sha256 of all content above this line: 7eb646460e29109216c4f25f1748e2b1538d4465027fb0c36d4351c721c06971

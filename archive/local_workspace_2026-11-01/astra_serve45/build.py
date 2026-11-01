# Builds the #45 ASCII send parts. Does NOT start any server and sends nothing.
import re, hashlib, os, subprocess
os.chdir('/workspace/astra_serve45')
def sha(b): return hashlib.sha256(b).hexdigest()
def foot(b): return b + ('sha256 of all content above this line: ' + sha(b) + '\n').encode()
EXP = {'review/trackB_instrument_validation_scope_v3_4_merged_RD.md': '02336eec',
       'review/trackB_scope_v3_4_addendum_RD.md': 'c67ce2a8',
       'review/trackB_instrument_validation_scope_v3_3_merged_RD.md': '307bab21',
       'astra_consult44_response.txt': '49afbb5d', 'astra_consult43_response.txt': '9a46cb81',
       'astra_consult42_response.txt': 'e438e329', 'astra_consult41_response.txt': '3f3b1b87'}
if not os.path.exists('governing_sha256.txt'):
    r = subprocess.run(['sha256sum'] + list(EXP), cwd='/workspace', capture_output=True, text=True, check=True)
    open('governing_sha256.txt', 'wb').write(foot(r.stdout.encode()))
r = subprocess.run(['sha256sum', '-c', '/workspace/astra_serve45/governing_sha256.txt'], cwd='/workspace', capture_output=True, text=True)
print(r.stdout.strip())
if 'FAILED' in r.stdout or not all(f + ': OK' in r.stdout for f in EXP): raise SystemExit('SHA MISMATCH - not building')
tab = {l.split()[1]: l.split()[0] for l in open('governing_sha256.txt') if l.strip() and not l.startswith('sha256 of')}
assert set(tab) == set(EXP)
for f, p in EXP.items():
    if not tab[f].startswith(p): raise SystemExit('PREFIX MISMATCH %s' % f)
for f in ('review/trackB_instrument_validation_scope_v3_4_merged_RD.md', 'review/trackB_scope_v3_4_addendum_RD.md',
          'review/trackB_instrument_validation_scope_v3_3_merged_RD.md'):
    L = open('/workspace/' + f, 'rb').read().splitlines(True)
    assert sha(b''.join(L[:-1])) == L[-1].decode().split(': ')[1].strip(), 'footer mismatch ' + f
# merged v3.4 must carry v3.3 (minus footer) and the addendum byte-identical
m34 = open('/workspace/review/trackB_instrument_validation_scope_v3_4_merged_RD.md', 'rb').read()
v33 = open('/workspace/review/trackB_instrument_validation_scope_v3_3_merged_RD.md', 'rb').read()
add = open('/workspace/review/trackB_scope_v3_4_addendum_RD.md', 'rb').read()
assert b''.join(v33.splitlines(True)[:-1]) in m34 and add in m34, 'merged v3.4 does not carry inputs verbatim'
print('prefix check OK (%d files); v3.4, addendum and v3.3 footers OK; v3.4 carries v3.3 + addendum verbatim' % len(EXP))
exec(open('pieces.py').read())
r44 = open('/workspace/astra_consult44_response.txt').read().splitlines()
r42 = open('/workspace/astra_consult42_response.txt').read().splitlines()
r41 = open('/workspace/astra_consult41_response.txt').read().splitlines()
assert '"' + CEILING + '"' in r41[303], 'ceiling not verbatim at #41 L304'
for n, q in Q44: assert q in r44[n-1], ('#44', n, q)
for n, q in Q42: assert q in r42[n-1], ('#42', n, q)
V34 = tab['review/trackB_instrument_validation_scope_v3_4_merged_RD.md'][:8]; ADD = tab['review/trackB_scope_v3_4_addendum_RD.md'][:8]
body = BODY.replace('{V34}', V34).replace('{ADD}', ADD).replace('{CEILING}', CEILING)
for n, q in Q44:
    if n in (185, 86, 3): assert q in body, ('quote missing from body', n)
bad = sorted({c for c in body if ord(c) > 127})
if bad: raise SystemExit('nonascii %r' % bad)
body = re.sub(r'\n{3,}', '\n\n', body)
assert len(body) <= 15000, ('body too long', len(body))
for w in ('conscious', 'sentien', 'autopoie', r'\balive\b', r'\bC[45]\b'):
    for m in re.finditer(w, body, re.I):
        ctx = body[max(0, m.start()-60):m.end()+40].lower()
        assert 'no consciousness' in ctx, (w, ctx)
bb = foot(body.encode()); open('c45_body.md', 'wb').write(bb)
lines = body.split('\n'); parts = []; cur = ''; LIM = 2700
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
    if i < n: t = '[c45 part %d/%d]\n' % (i, n) + p.rstrip('\n') + '\n[end of c45 part %d/%d - more coming, do not answer yet]' % (i, n)
    else: t = '[c45 part %d/%d]\n' % (i, n) + p.rstrip('\n') + '\n[END OF CONSULT #45 PACKET - all %d parts sent. Please answer now.]' % n
    assert all(ord(c) < 128 for c in t) and len(t) <= 2800, (i, len(t))
    open('send/c45_%d.txt' % i, 'w').write(t)
re_body = ''.join(open('send/c45_%d.txt' % i).read().split('\n', 1)[1].rsplit('\n', 1)[0] + '\n' for i in range(1, n+1))
assert re.sub(r'\s+', ' ', re_body).strip() == re.sub(r'\s+', ' ', body).strip(), 'reassembly mismatch'
man = '# c45 send-part manifest (send parts carry no footer, per the #43/#44 packet precedent; this manifest covers them)\n'
man += ''.join('%s  send/c45_%d.txt  %d chars\n' % (sha(open('send/c45_%d.txt' % i, 'rb').read()), i, len(open('send/c45_%d.txt' % i).read())) for i in range(1, n+1))
open('send_manifest.txt', 'wb').write(foot(man.encode()))
# verify manifest against files on disk
for l in open('send_manifest.txt'):
    if l.startswith('#') or l.startswith('sha256 of'): continue
    h, f = l.split()[:2]; assert sha(open(f, 'rb').read()) == h, f
print('BUILD OK: %d parts, body %d chars, body sha256 %s, part sizes %s' % (n, len(body), sha(bb), [len(open('send/c45_%d.txt' % i).read()) for i in range(1, n+1)]))
# sha256 of all content above this line: 6e349ff683c329b338a25335b82e30b6a6bfe732cdefb36bba7bf9514eb22600

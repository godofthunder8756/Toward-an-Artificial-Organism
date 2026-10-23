import re,sys
f=open(sys.argv[1]).read()
r39=open('/workspace/astra_consult39_response.txt').read();r38=open('/workspace/astra_consult38_response.txt').read();r37=open('/workspace/astra_consult37_response.txt').read()
raws={'39':r39,'38':r38,'37':r37}
q=re.findall(r'^\s*> (".*")$',f,re.M)
miss=[x for x in q if not any(x in r for r in raws.values())]
print('blockquotes',len(q),'missing',len(miss)); [print(' MISSING',m[:90]) for m in miss]
def items(raw,pref):
    return [l for l in raw.split('\n') if l.startswith('> "')]
for k,r in raws.items():
    its=[l for l in r.split('\n') if l.startswith('> "')]
    print(f'#{k} raw quoted lines',len(its),'all present in file',all(l in f for l in its))
ex=re.findall(r'^- \*\*\[L(\d+)\]\*\* "(.*)"$',f,re.M)
bad=[n for n,t in ex if not any(t in r for r in raws.values())]
print('excerpts',len(ex),'bad',bad)
blocks=re.findall(r'```text\n(.*?)```',f,re.S)
print('codeblocks',len(blocks),'verbatim',[any(b in r for r in raws.values()) for b in blocks])
defs=set(m.rstrip('.') for m in re.findall(r'\*\*(C\d+\.\d+)',f))
refs=set(f"C{a}.{b}" for a,b in re.findall(r'\bC(\d+)\.(\d+)',f))
print('clause defs',len(defs),'refs',len(refs),'unresolved',sorted(refs-defs))

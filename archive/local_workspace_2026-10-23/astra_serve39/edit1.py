p=open('pieces.py').read()
p=p.replace('HEAD="""','''def compact(a,b):
    out=[];cur=None
    for l in L[a-1:b]:
        m=re.match(r'^\\*\\*(E3[78]-\\d+)\\*\\* \\[(L\\d+)\\]',l)
        if m:
            if cur: out.append(cur)
            cur=m.group(1)+' ['+m.group(2)+']:';continue
        if cur is None: continue
        if l.startswith('|') and not re.match(r'^\\|[-| ]+\\|$',l) and 'Requirement | Clause' not in l:
            c=[x.strip() for x in l.strip('|').split('|')]
            cur+=' '+c[0]+' -> '+c[1]+';'
        elif l.startswith('*Binding here:*') or l.startswith('*Note (#38):*'):
            cur+=' '+l.replace('*','')
    if cur: out.append(cur)
    return '\\n'.join(out)+'\\n'
HEAD="""''',1)
p=p.replace('noquote(137,215)','compact(137,215)').replace('noquote(220,379)','compact(220,379)')
old=p[p.index('Change log relative'):p.index('0. Sources, hashes')]
new=open('cl.txt').read()
p=p.replace(old,new)
s=p.index('- NOTE_1 records the CNA'); e=p.index("- Delegate's room summary")
p=p[:s]+open('rl.txt').read()+p[e:]
open('pieces.py','w').write(p)

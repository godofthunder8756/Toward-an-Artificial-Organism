import sys
def R(fn, pairs):
    s=open(fn).read()
    for a,b in pairs:
        n=s.count(a)
        if n!=1: sys.exit(f"{fn}: count {n} for: {a[:70]}")
        s=s.replace(a,b)
    open(fn,'w').write(s)

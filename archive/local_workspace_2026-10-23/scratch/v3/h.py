import re
RAW=open('/workspace/astra_consult42_response.txt').read().split('\n')
V21=open('/workspace/review/trackB_instrument_validation_scope_v2_1_merged_RD.md').read().split('\n')
def q(n,s):
    assert s in RAW[n-1], (n,s[:60])
    return f'"{s}" (#42 L{n})'
def ql(n):  # whole line verbatim
    return f'"{RAW[n-1]}" (#42 L{n})'
def sec(a,b): return V21[a-1:b]

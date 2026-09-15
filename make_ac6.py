"""Create a separate AC6 source from frozen AC5, with explicit checked changes."""
from pathlib import Path
s=Path('ac5.py').read_text()
def change(old,new):
    global s
    assert old in s, old
    s=s.replace(old,new)
change('import ac4\n','import ac4\nimport ac5\n')
change('ARMS=(\'adaptive\',\'frozen\',\'random_feedback\',\'informed\',\'protected\')',"ARMS=('local','frozen','informed','protected','global')")
change('GATE=4*prog.WIDTH','GATE=4*prog.WIDTH+11')
change("return bool(decode(traces[0,GATE:GATE+1])[0])","return not bool(decode(traces[0,GATE:GATE+1])[0])")
change("arm='adaptive'","arm='local'")
change("gate_on=0)","gate_on=0,B0_birth=0)")
change("signal=random_feedback if arm=='random_feedback' else e['crossings']>0","signal=e['crossings']>0")
change('[int(wanted)]','[int(not wanted)]')
change('shadow[0,GATE]=int(wanted)','shadow[0,GATE]=int(not wanted)')
change("action=prog.choose(source,ac4.observe(b)); ac4.react(b,action,'self',e)","""observation=ac4.observe(b)
        if not gate:
            observation=(observation & ~256) | (int(b.boundary[1:].min()<=64)<<8)
        action=prog.choose(source,observation)
        old_boundary=b.boundary.copy()
        if action==10:
            local_boundary(b,e)
        else:
            ac4.react(b,action,'self',e)
        e['B0_birth']=int(b.boundary[0]>old_boundary[0])""")
change("def run(seed,arm,ticks=8192):\n", "def run(seed,arm,ticks=8192):\n    if arm=='global':\n        result=ac5.run(seed,'adaptive',ticks); result['arm']='global'; return result\n")
change("root=Path('ac5_results_v1')","root=Path('ac6_results_v1')")
change("names=['ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','test_ac5.py','AC5_PROTOCOL_v1.md']","names=['ac6.py','ac5.py','ac5_program.py','ac4.py','ac4_transport.py','ac1.py','test_ac6.py','AC6_PROTOCOL_v1.md']")
change('range(200,208)','range(300,308)')
change('"""AC5: vulnerable one-bit commitment revision in AC4 physical body."""','"""AC6: paid local omission encoded in the vulnerable B action."""')
insertion='''def local_boundary(b,e):
    b.energy-=1; e['spent_e']+=1; e['active']=1
    a=ac4.available(b); wp=b.pos[:16][a[:16]]
    if len(wp):
        near=(np.abs(ac4.ENDPOINTS[:,None,:]-wp[None,:,:]).sum(axis=2)<=1).any(axis=1)
        near[0]=False
        candidates=np.flatnonzero(near & (b.boundary<=64))
        if len(candidates) and ac4.pay(b,e,2,2):
            j=int(candidates[np.argmin(b.boundary[candidates])])
            e['B_discard']+=int(b.boundary[j]>0); b.boundary[j]=256; e['B_birth']+=1


'''
change('def step(',insertion+'def step(')
Path('ac6.py').open('x').write(s)

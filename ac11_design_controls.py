"""AC11 design controls (ENGINEERING ONLY — the AC11 claim was not run).

Two decisive controls for the AC11 design, run before any final seed:

A. Duty-cycle and probability sweep. If some *state-blind* fixed maintenance
   level matches or beats the adaptive arm, the AC11 claim ("the decision must be
   acquired") fails, because the same outcome is reachable without any
   experience-dependent choice.
B. Both-keys port relabelling. With the whole region made stale at once, check
   whether relinquishment is viable at all in this architecture, i.e. whether a
   "need to relinquish" exists rather than merely a shorter death.

Seeds 0-2 with both developmental histories are engineering seeds and are
excluded from any later confirmatory sample.
"""
from pathlib import Path
import hashlib
import json
import statistics
import ac11

SEEDS=(0,1,2)
HISTORIES=(0,1)


def measure(arm,label):
    s=[ac11.run(seed,h,arm) for seed in SEEDS for h in HISTORIES]
    return dict(label=label,arm=arm,
                completions=sum(r['completed'] for r in s),n=len(s),
                mean_activity=statistics.mean(r['activity'] for r in s),
                deaths=[r['first_dead'] for r in s if r['first_dead'] is not None],
                alive=sum(r['completed'] for r in s))


def part_a():
    out=[]
    ac11.MOVE_KEYS=(1,)
    for period in (1,2,3,4,6,8):
        ac11.FIXED_PERIOD=period
        out.append(measure('fixed_schedule',f'fixed period {period} (duty 1/{period})'))
    for p in (1.0,0.5,0.25,0.125):
        ac11.RANDOM_P=p
        out.append(measure('random',f'random p={p}'))
    for n in (2,4,8,16,32):
        ac11.STREAK_N=n
        out.append(measure('adaptive',f'adaptive streak N={n}'))
    ac11.STREAK_N=8
    for arm in ('preserve','relinquish'):
        out.append(measure(arm,arm))
    return out


def part_b():
    out=[]
    ac11.MOVE_KEYS=(0,1)
    for arm in ('preserve','adaptive','relinquish'):
        out.append(measure(arm,f'{arm} (both ports relabelled)'))
    ac11.MOVE_KEYS=(1,)
    return out


def main():
    root=Path('ac11_design_controls_v2'); root.mkdir(exist_ok=False)
    names=[n for n in ('ac11_design_controls.py','ac11.py','ac9.py','ac9_priority_v2.py',
                       'ac9_memory.py','ac5.py','ac5_program.py','ac4.py',
                       'ac4_transport.py','ac1.py') if Path(n).exists()]
    (root/'pre_run_snapshot.json').write_text(json.dumps(
        {n:hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in names},indent=2))
    a=part_a(); b=part_b()
    (root/'results.json').write_text(json.dumps(dict(kind='engineering_design_controls',
                                                     part_a=a,part_b=b),indent=2))
    for title,rows in (('A. single port relabelled',a),('B. both ports relabelled',b)):
        print(f"\n=== {title} (6 engineering individuals each) ===")
        print(f"{'condition':40} {'alive':>6} {'mean act':>9} {'dead@':>14}")
        for r in rows:
            d=r['deaths']
            print(f"{r['label']:40} {r['alive']}/{r['n']:<4} {r['mean_activity']:9.3f} "
                  f"{(f'{min(d)}..{max(d)}' if d else '-'):>14}")


if __name__=='__main__': main()

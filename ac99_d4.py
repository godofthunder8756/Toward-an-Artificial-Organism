"""AC99-D4: protocol + finals — the Gray-coded streak (cheaper transitions) under the standing gates.

Parent: AC99-D3. This is the final step of the AC99 line: freeze the standing gates
(AC97/98's unconditional adaptation criterion, the no-harm survival comparison, and the
per-tick observer-discard) on UNSEEN seeds, with the Gray-coded streak as the chosen
architecture.

The three arms, per individual (x2 histories):

  - `gray`      — the SUCCESS arm / chosen architecture: the 3-bit reflected-Gray streak
                  (every increment is 1 bit = 7 replicas, W >= 1) + the AC98/AC99-D1
                  reserve (level 21, drop/stall/wlow triggers, atomic release+disarm).
  - `binary`    — the DIRECT CONTROL: the binary streak + the same reserve. This is the
                  AC98/AC99 revised-reserve architecture (the D1 atomicity fix), the exact
                  architecture that died on AC98's seed 4436 (W-bound 3->4 increment).
  - `wb_first`  — the LABELED RIVAL (not the success arm): the binary streak + a paid
                  W-birth-priority program swap (D3). It rescues 4436 by keeping W >= 3
                  rather than by making the increment cheaper.

The success arm is the Gray streak (the "cheaper transitions" premise of AC99); the other
two are the binary predecessor and the orthogonal rival, both labeled. The no-harm gate
compares the success arm against the binary control (the encoding is the only difference).

Everything else (reserve policy, sticky 1e-4 damage, 7-replica majority read threshold 4,
prices 1 energy + 1 material per replica, STREAK_N=6, the perm move at t=8192, 16,384
ticks, erase-on-relinquish) is byte-for-byte the AC99-D1/D2/D3 architecture. This runner
does NOT re-implement the arms; it delegates to the verified engineering runners
(`ac99.run` for binary, `ac99_d2.run` for Gray, `ac99_d3.run(wb_first=True)` for the
rival), so each arm is exact by construction.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import ac99            # binary streak + atomic release + AllocEraseReserve (the binary control)
import ac99_d2         # Gray streak + GrayAllocEraseReserve (the chosen architecture)
import ac99_d3         # W-birth-priority rival (labeled)
import ac96
import ac95
import ac12
import ac4
import ac9
import ac71
import ac5_program as prog

TICKS = ac95.TICKS
MOVE_TICK = ac95.MOVE_TICK
DEV = ac71.DEV
STREAK_N = ac12.STREAK_N

# The three arms, all reserve=True (the reserve policy is part of the AC99 architecture).
ARMS = ['gray', 'binary', 'wb_first']

SOURCES = ['ac99_d4.py', 'ac99_d3.py', 'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py',
           'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC99_PROTOCOL_v1.md']


def run(seed, history, code='gray', transition='perm', damage=True, corrupt=False):
    """Run one individual under one of the three arms (all reserve=True).

    `code` selects the arm; the arm's runner is the verified engineering runner, so each
    row is exact (state_hash) by construction:
      - 'gray'    -> ac99_d2.run(reserve=True)  (the Gray streak)
      - 'binary'  -> ac99.run(reserve=True)     (the binary streak = the direct control)
      - 'wb_first'-> ac99_d3.run(reserve=True, wb_first=True)  (the labeled rival)
    """
    if code == 'gray':
        return ac99_d2.run(seed, history, 'gated', reserve=True, damage=damage,
                           corrupt=corrupt, transition=transition)
    if code == 'binary':
        return ac99.run(seed, history, 'gated', reserve=True, damage=damage,
                        corrupt=corrupt, transition=transition)
    if code == 'wb_first':
        return ac99_d3.run(seed, history, 'gated', reserve=True, damage=damage,
                           corrupt=corrupt, transition=transition, wb_first=True)
    raise ValueError(f'unknown arm code {code!r}')


# ---------------- observer-discard (per-tick, on the GRAY success arm) ----------------
def _mid_streak_tick(row, key=1, before_value=2):
    for (t, k, before, after, dropped) in row['streak_events']:
        if k == key and before == before_value and not dropped and t >= MOVE_TICK:
            return t
    return None


def observer_discard_equivalence_gray(seed, history, transition='perm', damage=True,
                                      corrupt=False):
    """Per-tick observer-discard on the GRAY success arm.

    At a mid-streak tick (the Gray-decoded streak reads 2 before the 2->3 increment), the
    succession observer AND the alloc (clearing the vestigial host streak dict) are replaced
    with fresh objects; the run resumes; the trajectory must be byte-identical at EVERY tick.
    The Gray streak and the reserve must be recovered from maintained state alone.

    This is the Gray analogue of `ac99.observer_discard_equivalence` (the binary streak's
    discard), needed because the success arm here is the Gray streak.
    """
    base, base_o, base_trace = ac99_d2._run_internal(
        seed, history, 'gated', True, damage, corrupt, transition, TICKS, MOVE_TICK,
        record_trace=True)
    swap_tick = _mid_streak_tick(base, key=1, before_value=2)
    if swap_tick is None:
        return dict(seed=seed, history=history, status='no_mid_streak',
                    streak_events=base['streak_events'])
    swapped, swapped_o, swapped_trace = ac99_d2._run_internal(
        seed, history, 'gated', True, damage, corrupt, transition, TICKS, MOVE_TICK,
        record_trace=True, swap_at=swap_tick)
    assert base_trace is not None and swapped_trace is not None
    n_equal = 0
    first_div = None
    for (t1, d1), (t2, d2) in zip(base_trace, swapped_trace):
        assert t1 == t2, f'tick grid mismatch {t1} vs {t2}'
        if d1 == d2:
            n_equal += 1
        elif first_div is None:
            first_div = t1
    per_tick_identical = (first_div is None
                          and len(base_trace) == len(swapped_trace)
                          and n_equal == len(base_trace))
    return dict(seed=seed, history=history, swap_tick=swap_tick,
                streak_at_swap=2, host_dict_cleared=True,
                swap_applied=swapped['swap_applied'],
                per_tick_identical=per_tick_identical,
                n_equal=n_equal, n_ticks=len(base_trace), first_div=first_div,
                terminal_identical=base['state_hash'] == swapped['state_hash'],
                base_hash=base['state_hash'], swapped_hash=swapped['state_hash'])


# ---------------- finals: protocol freeze + the standing gates ----------------
def preflight(protocol='AC99_PROTOCOL_v1.md'):
    text = Path(protocol).read_text()
    marker = 'SOURCES (declared):'
    line = [l for l in text.splitlines() if l.strip().startswith(marker)]
    assert line, f'{protocol} declares no source list'
    declared = [w.strip() for w in line[0].split(marker, 1)[1].split() if w.strip()]
    assert set(declared) == set(SOURCES), \
        f'runner hashes {sorted(set(SOURCES))} but protocol declares {sorted(set(declared))}'
    missing = [s for s in declared if not Path(s).exists()]
    assert not missing, f'declared sources missing: {missing}'
    return declared


def _reacq_ticks(r):
    rt = r.get('reacquire_ticks') or {}
    return {int(k): v for k, v in rt.items()}


def gates_ac99_d4(rows, seeds, observer_discard=None, control_equiv=None):
    """Recompute the AC99-D4 gates from the saved rows (no simulation).

    G1 (unconditional adaptation), G2 (no-harm) and G4 (endogenous reserve) are derived from
    the rows of the GRAY success arm (with G2 comparing against the binary control). G3
    (per-tick observer-discard) is a two-run comparison re-read from its recorded dict. G5's
    determinism (sampled rerun) and arm identity (wb_first no-swap == binary control) are
    set by the collector.
    """
    gray = [r for r in rows if r['condition'] == 'gray']
    binary = [r for r in rows if r['condition'] == 'binary']
    n_ind = len(seeds) * 2

    def a1(r):   # relinquishment: the drop fired with the register bit set
        return r['relinquishments'] >= 1 and bool(r['drop_ticks']) and \
            all(reg for (_t, _p, reg) in r['drop_ticks'])

    def a2(r):   # reacquisition: key 1 re-bound after the drop
        reacq = _reacq_ticks(r).get(1) or []
        drop = r['drop_ticks'][0][0] if r['drop_ticks'] else None
        return bool(reacq) and (drop is None or reacq[0] > drop)

    def a3(r):   # continued machinery production post-move
        return r['W_births_post_move'] > 0 and r['C_births_post_move'] > 0 \
            and r['B_births_post_move'] > 0

    def a4(r):   # survival
        return bool(r['completed'])

    # G1: unconditional adaptation — every final GRAY individual satisfies all four measures
    g1 = len(gray) == n_ind and all(a1(r) and a2(r) and a3(r) and a4(r) for r in gray)

    # G2: no-harm — no distinct seed where the binary control survives and the gray arm dies
    by_seed = {}
    for r in rows:
        by_seed.setdefault(r['seed'], {}).setdefault(r['condition'], []).append(r)
    g2 = True
    for s in seeds:
        bn = by_seed.get(s, {}).get('binary', [])
        gr = by_seed.get(s, {}).get('gray', [])
        if bn and gr and any(r['completed'] for r in bn) and any(not r['completed'] for r in gr):
            g2 = False

    # G3: state sufficiency — per-tick observer-discard on the gray arm, trajectory-level
    g3 = observer_discard is not None and len(observer_discard) == n_ind and all(
        d.get('status') != 'no_mid_streak' and d.get('swap_applied')
        and d.get('streak_at_swap') == 2 and d.get('per_tick_identical')
        for d in observer_discard.values())

    # G4: endogenous reserve — no external rescue (release never exceeds withhold)
    g4 = all(r['reserve_m'] > 0 and r['reserve_released_m'] <= r['reserve_m'] for r in gray)

    return {
        'G1_unconditional_adaptation': g1,
        'G2_no_harm': g2,
        'G3_state_sufficiency_per_tick_discard': g3,
        'G4_endogenous_reserve_no_external_rescue': g4,
        'G5_completeness_determinism_arm_identity': None,
    }


def collect_finals(root, seeds, do_preflight=True):
    """AC99-D4 finals: three arms per individual (gray / binary / wb_first) in the
    relinquishment world (`transition='perm'`, damage on, corrupt off). G1/G2/G4 are derived
    from the rows; G3 (per-tick observer-discard on the gray arm) and G5's arm identity
    (wb_first no-swap == binary control) are computed here and recorded. do_preflight=False
    is for a smoke run (the protocol is frozen only before finals)."""
    if do_preflight:
        preflight()
    outdir = Path(root); outdir.mkdir(exist_ok=False)
    hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest() for n in SOURCES if Path(n).exists()}
    (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for code in ARMS:
                    r = run(seed, history, code, transition='perm', damage=True, corrupt=False)
                    r['condition'] = code
                    rows.append(r); f.write(json.dumps(r) + '\n'); f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], _reacq_ticks(r).get(1),
                 r['W_births_post_move'], r['C_births_post_move'], r['B_births_post_move'],
                 r['reserve_m'], r['reserve_released_m'], r['reserve_release_kinds'],
                 r['streak_final'])
                for r in rows[-len(ARMS) * 2:]]), default=str), flush=True)
    # ---- G3 per-tick observer-discard (two-run comparison, per gray individual) ----
    obs = {}
    for seed in seeds:
        for history in (0, 1):
            obs[f'{seed}/{history}'] = observer_discard_equivalence_gray(seed, history)
    # ---- G5 arm identity: the rival's no-swap path (wb_first=False) reproduces the binary
    # control byte-for-byte -- proving the swap is the only change in the wb_first arm ----
    control_equiv = {}
    for seed in seeds:
        for history in (0, 1):
            a = ac99_d3.run(seed, history, 'gated', reserve=True, damage=True, corrupt=False,
                            transition='perm', wb_first=False)
            b = run(seed, history, 'binary', transition='perm')
            control_equiv[f'{seed}/{history}'] = a['state_hash'] == b['state_hash']
    g = gates_ac99_d4(rows, seeds, obs, control_equiv)
    first = rows[0]
    rerun = run(first['seed'], first['history'], first['condition'], transition='perm',
                damage=True, corrupt=False)
    g['G5_completeness_determinism_arm_identity'] = (
        len(rows) == len(seeds) * 2 * len(ARMS)
        and rerun['state_hash'] == first['state_hash']
        and bool(control_equiv) and all(control_equiv.values()))
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), hashes=hashes, gates=g, rows=rows, transition='perm',
             arms=ARMS, observer_discard=obs, control_equivalence=control_equiv),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def main():
    if '--discard' in sys.argv:
        for seed in (4436, 4437, 4438, 4439):
            for history in (0, 1):
                print(json.dumps(observer_discard_equivalence_gray(seed, history),
                                 default=str))
        return
    collect_finals('ac99_results_v1', [4440, 4441, 4442, 4443])


if __name__ == '__main__':
    main()

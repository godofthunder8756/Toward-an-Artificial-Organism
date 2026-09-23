"""AC109 (C1, engineering): does the STORED cause-estimate add anything over a direct
diagnostic controller that reads (bound, used_held, productive) transiently?

Parent card (C1, t_9e21dcbb): the AC107 candidate maintains a ONE-BIT cause estimate e in
vulnerable paid state, updated by the K4 discriminator and consumed as E_world -> frozen
Gray-streak relinquishment / E_machinery -> withhold + proactive renewal. The question is
whether STORING that estimate buys information, decisions, or benefit BEYOND a rival that
reads the same diagnostic triple (bound, used_held, productive) directly at decision time
and computes the cause TRANSIENTLY, with no stored estimate.

The direct-diagnostic rival (`direct`) keeps EVERYTHING the candidate has except the storage:
  - the SAME information access: (bound = o.memory.read(1) is not None, used_held = the
    shimmed retrieval result, productive = e['productive'] > 0);
  - the SAME discriminator rules, evaluated on the CURRENT triple:
        bound & not used       -> E_machinery (cut signature)
        used & not productive  -> E_world   (held entry failed -> stale)
        not bound & productive -> E_world   (blind re-bind -> re-acquisition)
        (no rule fires)        -> E_world   (no diagnostic signal -> the acquired reactive
                                             default, the same value the acquired bit holds)
  - the SAME decision timing (per contact-1), permitted actions (_drop/_restore,
    gray_streak_write, proactive renew), and the SAME maintained Gray streak (per-key,
    paid, damaged) as the candidate.
The ONLY difference: the cause label is a transient local computed from the current triple,
never written to (or read from) vulnerable state. So the rival's sensing/storage/writes/
computation are accounted separately -- it has NO estimate-bit write (bel_writes == 0) and
no persistence of the last conclusion into contacts where the diagnostic is silent.

The honest hypothesis from K4's identifiability: because the two causes produce DISJOINT
action-observation histories, the current triple already contains all discriminative
information, so there is nothing for a stored bit to remember. If that holds, the direct
diagnostic is behaviourally equivalent to the candidate, and the stored estimate is pure
cost (its bit write in the cut + its persistence-driven proactive renewal after the window).

Discipline: ENGINEERING ONLY. This file extends the frozen ac107 runner WITHOUT editing it
(the AC108 rule: patch the module's alloc factory, prove inertness by state_hash reproduction
of the frozen arms). No protocol, no freeze, no finals. A negative result (equivalence) is
the expected honest finding and is reported, not weakened.
"""
from pathlib import Path
import json
import sys
import numpy as np
import ac107
import ac99_d2
import ac12
import ac4
import ac9

TICKS = ac107.TICKS
STREAK_N = ac107.STREAK_N
CUT_TICK = ac107.CUT_TICK
PORTS = ac107.PORTS
WINDOW = ac107.WINDOW
CONDITIONS = ac107.CONDITIONS
ENGINEERING = ac107.ENGINEERING
FINAL_SEEDS = ac107.FINAL_SEEDS

# last-created DirectDiagnostic, used to surface its transient conclusions (host-side
# observational state) onto the returned row.
_LAST_DIRECT = []

# the frozen factory, captured before any patching (delegation target).
_ORIG_MAKE_ALLOC = ac107._make_alloc


# ---------------- the direct-diagnostic rival (no stored cause estimate) ----------------
class DirectDiagnostic(ac99_d2.GrayAllocEraseReserve):
    """C1's rival: the candidate's discriminator + consumption, with the storage removed.

    The cause is computed transiently from the current (bound, used_held, productive) triple;
    it is never written to vulnerable state, never read back, and has no cross-contact
    persistence. The maintained Gray streak (the relinquishment memory) is retained exactly.
    """

    def __init__(self, seed, history, proactive=True):
        super().__init__('allocate', seed, history, reserve=False)
        self.proactive = proactive
        self.diag_events = []       # (tick, kind, cause) observational -- the transient
                                    # conclusions, in the candidate's own bel_events format

    def _cause(self, bound, used, productive):
        """The K4 discriminator, transient. 0 = E_machinery, 1 = E_world.

        Rules 2 and 3 both conclude E_world, and the no-signal default is E_world (the
        acquired value), so the transient cause is 'machinery' iff the read is suppressed
        while the entry is still bound -- the cut signature. This is not a weakened rival:
        it is the candidate's own rule set with the two E_world branches and the silent
        fallback collapsed to their common value, which the acquired bit already holds.
        """
        if bound and not used:
            return 0                # E_machinery
        return 1                    # E_world (used&not productive, not bound&productive, silent)

    def _proactive_renew(self, o, e, key):
        """Direct paid per-slot renewal of the route entry (verbatim from ac107.Estimator)."""
        place = ac12.m12.slot_of_key(o.memory, key)
        if place is None:
            return 0
        r, s = place
        result = ac12.m12.renew_alloc(o.memory, o.body, r,
                                      int(ac4.available(o.body)[4 * (r + 1):4 * (r + 2)].sum()),
                                      [s == 0, s == 1])
        if result['writes']:
            ac9.memory_charge(e, result)
            e['proactive_writes'] = e.get('proactive_writes', 0) + result['writes']
        return result['writes']

    def outcome(self, o, key, e, used_held=None):
        if self.arm != 'allocate':
            return
        key = int(key)
        if key != 1:
            super().outcome(o, key, e)          # channel 0 is never moved/cut: frozen streak
            return
        bound = (o.memory.read(1) is not None)
        used = bool(used_held)
        productive = e['productive'] > 0
        cur = ac99_d2.gray_streak_read(o, 1, self.streak_offs)
        cause = self._cause(bound, used, productive)
        # log the transient conclusion in the candidate's own event format (matched access)
        if bound and not used:
            self.diag_events.append((self.now, 'machinery_cut', 0))
        elif used and not productive:
            self.diag_events.append((self.now, 'world_held_fail', 1))
        elif not bound and productive:
            self.diag_events.append((self.now, 'world_rebind', 1))
        # ---- the two consumptions (identical to ac107.Estimator, reading `cause` not a bit) ----
        if productive:
            self._restore(o, e, key)
            ac99_d2.gray_streak_write(o, e, key, 0, self.streak_offs)
            if cause == 0 and self.proactive:
                self._proactive_renew(o, e, key)
            self.streak_events.append((self.now, key, cur, 0, 0))
            return
        # unproductive contact-1
        if cause == 0:
            # E_machinery: withhold relinquishment + proactive renewal
            if self.proactive:
                self._proactive_renew(o, e, key)
            self.streak_events.append((self.now, key, cur,
                                       ac99_d2.gray_streak_read(o, 1, self.streak_offs), 0))
            return
        # E_world: the frozen streak relinquishment
        dropped = 0
        if cur + 1 >= STREAK_N:
            n_before = len(self.log['dropped'])
            self._drop(o, e, key)
            dropped = 1 if len(self.log['dropped']) > n_before else 0
        else:
            ac99_d2.gray_streak_write(o, e, key, cur + 1, self.streak_offs)
        self.streak_events.append((self.now, key, cur,
                                   ac99_d2.gray_streak_read(o, 1, self.streak_offs), dropped))


# ---------------- extend ac107's alloc factory without editing ac107 ----------------
def _make_alloc_direct(arm, seed, history, bel_off):
    if arm == 'direct':
        a = DirectDiagnostic(seed, history)
        _LAST_DIRECT.clear()
        _LAST_DIRECT.append(a)
        return a
    return _ORIG_MAKE_ALLOC(arm, seed, history, bel_off)


def run(seed, history, arm, condition, ports=PORTS, record_trace=False):
    """Run one individual with the factory extended by `direct`. The frozen arms delegate to
    ac107._make_alloc, so they are unchanged by construction (proven by the inertness check).
    The direct arm's transient conclusions are attached to the row as `diag_events`."""
    orig = ac107._make_alloc
    ac107._make_alloc = _make_alloc_direct
    _LAST_DIRECT.clear()
    try:
        row = ac107._run_core(seed, history, arm, condition,
                              record_trace=record_trace, ports=ports)[0]
    finally:
        ac107._make_alloc = orig
    if arm == 'direct' and _LAST_DIRECT:
        row = dict(row)
        row['diag_events'] = list(_LAST_DIRECT[0].diag_events)
    return row


# ---------------- inertness: the patch must not disturb the frozen candidate ----------------
def inertness_check(seed, history, condition):
    """The patched factory's `candidate` must reproduce ac107's own candidate byte-for-byte."""
    via_patch = run(seed, history, 'candidate', condition)
    direct_call = ac107.run(seed, history, 'candidate', condition)
    return via_patch['state_hash'] == direct_call['state_hash']


# ---------------- the pairwise comparison (candidate vs direct) ----------------
BEHAVIOUR_FIELDS = ('completed', 'first_dead', 'relinquishments', 'routes',
                    'drop_ticks', 'reacquire_ticks', 'streak_final')


def compare_pair(cand, direct):
    """Per-endpoint equality of the two arms. Returns {field: {candidate, direct, equal}}."""
    out = {}
    for f in BEHAVIOUR_FIELDS:
        a, b = cand.get(f), direct.get(f)
        out[f] = dict(candidate=repr(a), direct=repr(b), equal=(a == b))
    # conclusions: the candidate's stored-estimate events vs the direct arm's transient events
    cand_ev = [(t, k, v) for (t, k, v) in cand.get('bel_events', [])]
    dir_ev = [(t, k, v) for (t, k, v) in direct.get('diag_events', [])]
    out['conclusions'] = dict(candidate=repr(cand_ev), direct=repr(dir_ev),
                              equal=(cand_ev == dir_ev))
    # cost endpoints (expected to differ: the stored estimate pays for storage)
    for f in ('bel_writes', 'proactive_writes', 'writes', 'streak_writes'):
        out[f] = dict(candidate=cand.get(f), direct=direct.get(f))
    return out


def collect_engineering(root, seeds, conditions=None):
    if conditions is None:
        conditions = list(CONDITIONS)
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for cond in conditions:
                    for arm in ('candidate', 'direct'):
                        r = run(seed, history, arm, cond)
                        rows.append(r)
                        f.write(json.dumps(r, default=str) + '\n')
                        f.flush()
                print(json.dumps(dict(seed=seed, history=history, outcomes=[
                    (r['arm'], r['condition'], r['completed'], r['first_dead'],
                     r['relinquishments'], r['routes'], r['bel_writes'],
                     r['proactive_writes'], r['writes'])
                    for r in rows[-len(conditions) * 2:]]), default=str), flush=True)
    by = {}
    for r in rows:
        by[(r['seed'], r['history'], r['condition'], r['arm'])] = r
    per_ind = {}
    for seed in seeds:
        for history in (0, 1):
            for cond in conditions:
                c = by[(seed, history, cond, 'candidate')]
                d = by[(seed, history, cond, 'direct')]
                per_ind[f'{seed}/{history}/{cond}'] = dict(
                    seed=seed, history=history, condition=cond,
                    comparison=compare_pair(c, d))
    inert = {f'{s}/{h}': inertness_check(s, h, 'cut') for s in seeds for h in (0, 1)}
    inert_ok = all(inert.values())
    meas = summarize(by, seeds, conditions)
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), conditions=conditions, PORTS=PORTS, WINDOW=WINDOW,
             STREAK_N=STREAK_N, per_individual=per_ind, inertness=inert,
             inertness_ok=inert_ok, measurements=meas, rows=rows),
        indent=2, default=str))
    print(json.dumps(dict(inertness_ok=inert_ok, inertness=inert), indent=2, default=str))
    print(json.dumps(dict(measurements=meas), indent=2, default=str))
    return rows, meas, per_ind


def summarize(by, seeds, conditions):
    n_ind = len(seeds) * 2
    inds = [(s, h) for s in seeds for h in (0, 1)]

    # E1: per-endpoint behavioural equivalence across all individuals and conditions
    e1 = {}
    for f in BEHAVIOUR_FIELDS:
        n_eq = sum(1 for s, h in inds for c in conditions
                   if by[(s, h, c, 'candidate')][f] == by[(s, h, c, 'direct')][f])
        e1[f] = dict(equal=n_eq, total=n_ind * len(conditions),
                     all_equal=(n_eq == n_ind * len(conditions)))

    # E2: conclusion analysis. The discriminator is a PURE function of the current
    # (bound, used_held, productive) triple, so both arms compute the SAME cause on any given
    # contact. Two measures: (a) event-for-event sequence equality (holds where the two arms'
    # contact schedules coincide); (b) conclusion-KIND equality (the set of (kind, value)
    # conclusions each arm ever reaches, independent of how many times / at which tick).
    e2_concl = {}
    for c in conditions:
        seq_eq = sum(1 for s, h in inds
                     if [(t, k, v) for (t, k, v) in by[(s, h, c, 'candidate')]['bel_events']]
                     == [(t, k, v) for (t, k, v) in by[(s, h, c, 'direct')]['diag_events']])
        kind_eq = sum(1 for s, h in inds
                      if {(k, v) for (t, k, v) in by[(s, h, c, 'candidate')]['bel_events']}
                      == {(k, v) for (t, k, v) in by[(s, h, c, 'direct')]['diag_events']})
        e2_concl[c] = dict(sequence_equal=seq_eq, kind_equal=kind_eq, total=n_ind)
    e2 = dict(
        direct_bel_writes_zero=all(by[(s, h, c, 'direct')]['bel_writes'] == 0
                                   for s, h in inds for c in conditions),
        candidate_bel_writes_by_condition={
            c: sorted({by[(s, h, c, 'candidate')]['bel_writes'] for s, h in inds})
            for c in conditions},
        conclusion_equality=e2_concl,
    )

    # E3: cost accounting -- the stored estimate's storage write and its persistence-driven
    # proactive renewal are the only divergences.
    e3 = {}
    for c in conditions:
        e3[c] = dict(
            candidate_proactive_writes=sorted(
                {by[(s, h, c, 'candidate')]['proactive_writes'] for s, h in inds}),
            direct_proactive_writes=sorted(
                {by[(s, h, c, 'direct')]['proactive_writes'] for s, h in inds}),
            candidate_writes=sorted({by[(s, h, c, 'candidate')]['writes'] for s, h in inds}),
            direct_writes=sorted({by[(s, h, c, 'direct')]['writes'] for s, h in inds}),
        )

    # survival tally per condition
    surv = {}
    for c in conditions:
        surv[c] = dict(
            candidate=sum(1 for s, h in inds
                          if by[(s, h, c, 'candidate')]['completed']
                          and by[(s, h, c, 'candidate')]['first_dead'] is None),
            direct=sum(1 for s, h in inds
                       if by[(s, h, c, 'direct')]['completed']
                       and by[(s, h, c, 'direct')]['first_dead'] is None))

    return dict(
        behavioural_equivalence=e1,
        all_behaviour_equivalent=all(v['all_equal'] for v in e1.values()),
        conclusions=e2,
        cost_accounting=e3,
        survival=surv,
    )


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac109_engineering_v1', ENGINEERING)
        return
    if '--smoke' in sys.argv:
        collect_engineering('ac109_smoke_v1', [0, 1, 2])
        return
    if '--finals' in sys.argv:
        collect_engineering('ac109_finals_v1', FINAL_SEEDS)
        return
    print('AC109: --engineering (seeds 0-7), --smoke (0-2), or --finals (6000-6007).')


if __name__ == '__main__':
    main()

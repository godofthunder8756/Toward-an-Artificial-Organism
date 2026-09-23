"""AC108 (K7): cognitive-organizational coupling — the two directions tested separately.

Parent: K6 (t_036aeceb, frozen AC107) + K3 (t_d84332fb, closure verdict). The K6 freeze
established that a maintained one-bit cause-estimate e in {E_world=1, E_machinery=0} (built
on the AC95 maintenance lineage — succession, reconstruction, W-gated paid writes) discriminates
the two causes at decision times with 0 mistakes and that the discrimination depends on the
maintained storage's content (state sufficiency + no-cause identity). K6's negative: the causal
role (scramble) and the survival advantage (vs r2/r4) do NOT transfer to the fresh family — the
cut's death bite is priority-specific (engineering seed 4 only), so the survival contrast is
seed-bounded.

K7 asks the coupling question the K6 mechanism now makes answerable, in TWO directions tested
SEPARATELY, each with a selective intervention and matched comparisons:

  Direction 1 (organizational maintenance -> representational accuracy and use):
      does the organism's own paid maintenance of the representation sustain its accuracy and use?
      Selective disruption: `no_write` — the estimate's W-gated paid write is disabled (the read
      stays honest), so the bit is never (re)acquired. This is distinct from K6's `scramble` (which
      forces the READ but keeps the write): no_write cuts the maintenance, scramble ignores its
      output. They coincide behaviourally in the cut only because the acquired value is 1 (E_world)
      and the cut's correct value is 0 — a disclosed asymmetry of the one-bit inverted-semantics
      design, not a confound.

  Direction 2 (representational function -> adaptation / production / viability):
      does the representation's content causally drive adaptation and affect production/viability,
      above what an externally supported fixed threshold achieves? Content interventions:
      `scramble` (read forced E_world) and `force_machinery` (read forced E_machinery) — the
      organism keeps the representation machinery, only its content is forced. Externally supported
      comparisons: `r2` (frozen Gray streak) and `r4` (longer raw counter), which have NO
      representation and rely on host-side fixed thresholds.

Causal dependence vs superior performance are reported SEPARATELY: G1-G3 gate causal dependence
(the forced content / cut maintenance changes behaviour per individual); the candidate's advantage
over r2/r4 is reported as a survival/adaptation table (superior performance), NOT gated on survival
(K6's lesson: a survival contrast that only bites on the priority-corner seed is vacuous on a fresh
family). Endpoints per direction: accuracy (bel_at_cut_end / bel_at_first_drop), use (relinquishments,
route retention, re-acquisition), adaptation (same, behavioural), production (W/C population, energy,
material, writes), viability (completed/first_dead, reported as a bimodality-aware lower bound).

Integration decision (deliverable 1): the K6 mechanism already RUNS on the K3-assessed autonomy
baseline's machinery — ac95.maintain (succession, reconstruction, description/pointer/ctrl repair)
and the W-gated paid writes are inherited UNCHANGED by ac107. The only AC105-specific features not
present are the corruption challenge and the allowance-42/persistent-trigger decision-spending
refinements, which are orthogonal to the maintenance<->representation coupling and would confound
the two-cause discrimination (a corruption event at the same tick as the cut/move is a THIRD cause).
The existing AC107 configuration therefore suffices; this is stated, not assumed, and re-verified by
G5 (the new runner reproduces the frozen arms byte-for-byte, so the extension is inert for them).

Discipline: engineering first (seeds 0-7), then a hashed protocol, then disjoint finals 6100-6107.
Negative findings are preserved; no gate is moved after seeing the result. Frozen arms are re-used
via ac107's own _make_alloc, so they are byte-identical to the freeze by construction.
"""
from pathlib import Path
import hashlib
import json
import sys
import numpy as np
import ac107
import ac106
import ac12

TICKS = ac107.TICKS
DEV = ac107.DEV
STREAK_N = ac107.STREAK_N
MOVE_TICK = ac107.MOVE_TICK
CUT_TICK = ac107.CUT_TICK
PORTS = ac107.PORTS
WINDOW = ac107.WINDOW
HOLD_N = ac107.HOLD_N

# The K7 arm set: the frozen K6 arms (candidate/r2/r4/scramble) plus two new coupling arms.
#   candidate        = maintained cause-estimate (K6 mechanism, unchanged)
#   no_write         = direction 1: selective maintenance disruption (write disabled, read honest)
#   scramble         = direction 2: content forced E_world (read forced, write intact) [K6's scramble]
#   force_machinery  = direction 2: content forced E_machinery (read forced, write intact)
#   r2 / r4          = direction 2: externally supported comparisons (no representation)
ARMS = ('candidate', 'no_write', 'scramble', 'force_machinery', 'r2', 'r4')
CONDITIONS = ('no_cause', 'move', 'cut')

ENGINEERING = list(range(8))
FINAL_SEEDS = [6100, 6101, 6102, 6103, 6104, 6105, 6106, 6107]   # fresh, disjoint, pre-freeze

SOURCES = ['ac108.py', 'ac107.py', 'ac106.py', 'ac99_d2.py', 'ac99.py', 'ac97.py', 'ac96.py',
           'ac95.py', 'ac76.py', 'ac71.py', 'ac12.py', 'ac12_memory.py', 'ac9.py',
           'ac9_priority_v2.py', 'ac9_memory.py', 'ac5.py', 'ac5_program.py', 'ac4.py',
           'ac4_transport.py', 'ac1.py', 'AC108_PROTOCOL_v1.md']


# ---------------- the two new coupling arms (subclass the frozen K6 estimator) ----------------
class CouplingEstimator(ac107.Estimator):
    """The candidate with one of two coupling interventions.

    `write=False`  (no_write):  disable the estimate's paid write; the read stays honest. The bit
                                is never (re)acquired, so it stays at its acquired value 1 (E_world).
                                This cuts the MAINTENANCE, not the read -- the direction-1 arm.
    `force=0/1`    (force_machinery / force_world): force the READ to a fixed cause value while the
                                write stays intact. This changes the CONTENT, not the machinery --
                                the direction-2 arm (scramble == force=1, kept as the frozen name).
    With force=None and write=True it is byte-identical to the frozen candidate.
    """

    def __init__(self, seed, history, bel_off=None, force=None, write=True, proactive=True):
        super().__init__(seed, history, bel_off=bel_off, estimate=True,
                         proactive=proactive, scramble=False)
        self.force = force      # None = honest read; 0 = E_machinery; 1 = E_world
        self.write = write      # False = the paid write is disabled (direction 1)

    def _bel(self, o):
        if self.force is not None:
            return self.force
        return ac107.bel_read(o, self.bel_off)

    def _bel_write(self, o, e, val):
        if not self.write:
            return 0, 0, 0
        return super()._bel_write(o, e, val)


# ---------------- extend the arm dispatch without touching the frozen ac107.py ----------------
_orig_make_alloc = ac107._make_alloc


def _make_alloc(arm, seed, history, bel_off):
    if arm == 'no_write':
        return CouplingEstimator(seed, history, bel_off=bel_off, force=None, write=False)
    if arm == 'force_machinery':
        return CouplingEstimator(seed, history, bel_off=bel_off, force=0, write=True)
    # the frozen arms resolve through ac107's own factory -> byte-identical to the freeze
    return _orig_make_alloc(arm, seed, history, bel_off)


ac107._make_alloc = _make_alloc


def run(seed, history, arm, condition, ports=PORTS, record_trace=False):
    """One individual. Frozen arms are byte-identical to ac107 (same _run_core, same factory
    for candidate/r2/r4/scramble); the new arms differ only in the read/write flags above."""
    return ac107.run(seed, history, arm, condition, ports=ports, record_trace=record_trace)


# ---------------- the frozen-copy reproduction license (recheck of inherited claims) ----------
def reproduction_check(seeds=(0, 1, 2, 3, 4, 5, 6, 7), conditions=None,
                       arms=('candidate', 'r2', 'r4', 'scramble')):
    """ac108's frozen arms reproduce ac107's runs byte-for-byte (state_hash) on the same
    individuals. This is the single-change license: the extension (new arms) is inert for the
    frozen arms, so any coupling contrast is attributable to the new arm alone."""
    if conditions is None:
        conditions = list(CONDITIONS)
    out = {}
    for s in seeds:
        for h in (0, 1):
            for c in conditions:
                for a in arms:
                    # the frozen arm under the ORIGINAL (unpatched) ac107 factory
                    ac107._make_alloc = _orig_make_alloc
                    try:
                        frozen = ac107.run(s, h, a, c)
                    finally:
                        ac107._make_alloc = _make_alloc   # restore the patch
                    ours = run(s, h, a, c)
                    out[f'{s}/{h}/{c}/{a}'] = frozen['state_hash'] == ours['state_hash']
    return out


# ---------------- gates (prespecified in AC108_PROTOCOL_v1.md) --------------------------------
def _by(rows):
    by = {}
    for r in rows:
        by.setdefault((r['seed'], r['history'], r['condition']), {})[r['arm']] = r
    return by


def survives(r):
    return bool(r['completed']) and r['first_dead'] is None


def gates_ac108(rows, seeds, reproduction=None, determinism=None):
    by = _by(rows)
    inds = [(s, h) for s in seeds for h in (0, 1)]
    n_ind = len(inds)

    def get(s, h, c, a):
        return by[(s, h, c)][a]

    # ---- G1 direction 1: maintenance -> ACCURACY (per individual, robust) ----
    # The cut's correct value is E_machinery (0); the acquired value is E_world (1), so the paid
    # write (1->0) is what establishes accuracy. Cutting it leaves the estimate reading E_world in
    # the cut, 16/16. The intervention must also have actually taken: no_write writes nothing.
    g1_cand = all(get(s, h, 'cut', 'candidate')['bel_at_cut_end'] == 0 for s, h in inds)
    g1_nowrite = all(get(s, h, 'cut', 'no_write')['bel_at_cut_end'] == 1 for s, h in inds)
    g1_took = all(get(s, h, 'cut', 'no_write')['bel_writes'] == 0
                  and get(s, h, 'cut', 'no_write')['bel_attempts'] == 0 for s, h in inds)
    g1 = g1_cand and g1_nowrite and g1_took

    # ---- G2 direction 1: maintenance -> USE (behavioural; non-vacuity declared) ----
    # The inaccurate read (E_world) drives the relinquishment consumption; it bites only where the
    # streak reaches 6 within the 96-tick window. Pre-declared: if no final individual exhibits it,
    # G2 fails vacuously and is recorded, not moved (K6's G2 lesson).
    g2_cand_holds = all(get(s, h, 'cut', 'candidate')['relinquishments'] == 0 for s, h in inds)
    g2_use = any(get(s, h, 'cut', 'no_write')['relinquishments'] >= 1
                 and get(s, h, 'cut', 'candidate')['relinquishments'] == 0 for s, h in inds)
    g2 = g2_cand_holds and g2_use

    # ---- G3 direction 2: content -> ADAPTATION, move side (per individual, robust) ----
    # In move the correct content is E_world (relinquish the stale route and re-acquire); forcing
    # E_machinery makes the organism hold the stale route forever. Deterministic per individual.
    g3_move_cand = all(get(s, h, 'move', 'candidate')['relinquishments'] >= 1 for s, h in inds)
    g3_move_forcemach = all(get(s, h, 'move', 'force_machinery')['relinquishments'] == 0
                            for s, h in inds)
    g3 = g3_move_cand and g3_move_forcemach

    # ---- G4 direction 2: content -> ADAPTATION, cut side (behavioural; non-vacuity declared) ----
    # In cut the correct content is E_machinery (hold the valid route); forcing E_world makes the
    # organism relinquish a valid route. Bites only where the streak reaches 6 in-window (K6: the
    # priority-corner). Non-vacuity declared as for G2.
    g4_cut_cand = all(get(s, h, 'cut', 'candidate')['relinquishments'] == 0 for s, h in inds)
    g4_cut_scramble = any(get(s, h, 'cut', 'scramble')['relinquishments'] >= 1 for s, h in inds)
    g4 = g4_cut_cand and g4_cut_scramble

    # ---- G5 clean control: the interventions are inert absent a cause ----
    # no_write and scramble read the acquired value (E_world), so they are byte-identical to the
    # candidate in no_cause. force_machinery forces E_machinery, which activates the proactive-
    # renewal consumption even absent a cause -- a disclosed consequence of the forced content
    # (extra redundant spend), NOT a hidden confound: survival/routes/relinquishments/demand are
    # identical to the candidate.
    g5_inert = all(get(s, h, 'no_cause', a)['state_hash'] == get(s, h, 'no_cause', 'candidate')['state_hash']
                   for a in ('no_write', 'scramble') for s, h in inds)
    g5_fm = all(
        get(s, h, 'no_cause', 'force_machinery')['completed'] == get(s, h, 'no_cause', 'candidate')['completed']
        and get(s, h, 'no_cause', 'force_machinery')['routes'] == get(s, h, 'no_cause', 'candidate')['routes']
        and get(s, h, 'no_cause', 'force_machinery')['relinquishments'] == get(s, h, 'no_cause', 'candidate')['relinquishments']
        and get(s, h, 'no_cause', 'force_machinery')['demand'] == get(s, h, 'no_cause', 'candidate')['demand']
        and get(s, h, 'no_cause', 'force_machinery')['proactive_writes'] >= 0
        for s, h in inds)
    g5 = g5_inert and g5_fm

    # ---- G6 frozen-copy reproduction: the extension is inert for the frozen arms ----
    g6 = reproduction is not None and all(reproduction.values())

    # ---- G7 completeness / determinism ----
    expected = len(seeds) * len(ARMS) * len(CONDITIONS) * 2
    if determinism is None:
        first = rows[0]
        determinism = run(first['seed'], first['history'], first['arm'],
                          first['condition'])['state_hash'] == first['state_hash']
    g7 = len(rows) == expected and determinism

    # ---- reported (NOT gated): superior performance (candidate vs externally supported rivals) ----
    survival = {
        'candidate_cut': sum(survives(get(s, h, 'cut', 'candidate')) for s, h in inds),
        'candidate_move': sum(survives(get(s, h, 'move', 'candidate')) for s, h in inds),
        'r2_cut': sum(survives(get(s, h, 'cut', 'r2')) for s, h in inds),
        'r4_move': sum(survives(get(s, h, 'move', 'r4')) for s, h in inds),
        'scramble_cut': sum(survives(get(s, h, 'cut', 'scramble')) for s, h in inds),
        'no_write_cut': sum(survives(get(s, h, 'cut', 'no_write')) for s, h in inds),
        'force_machinery_move': sum(survives(get(s, h, 'move', 'force_machinery')) for s, h in inds),
    }
    deaths = {
        'r2_cut': sorted({s for s, h in inds if not survives(get(s, h, 'cut', 'r2'))}),
        'r4_move': sorted({s for s, h in inds if not survives(get(s, h, 'move', 'r4'))}),
        'scramble_cut': sorted({s for s, h in inds if not survives(get(s, h, 'cut', 'scramble'))}),
        'no_write_cut': sorted({s for s, h in inds if not survives(get(s, h, 'cut', 'no_write'))}),
        'force_machinery_move': sorted({s for s, h in inds
                                        if not survives(get(s, h, 'move', 'force_machinery'))}),
        'candidate_any': sorted({s for s, h in inds for c in ('move', 'cut')
                                 if not survives(get(s, h, c, 'candidate'))}),
    }

    return {
        'G1_maintenance_to_accuracy': g1,
        'G2_maintenance_to_use': g2,
        'G3_content_to_adaptation_move': g3,
        'G4_content_causal_cut': g4,
        'G5_clean_control': g5,
        'G6_frozen_copy_reproduction': g6,
        'G7_completeness_determinism': g7,
        '_survival_counts': survival,
        '_deaths': deaths,
        '_g1_detail': dict(no_write_cut_bel=sorted({get(s, h, 'cut', 'no_write')['bel_at_cut_end']
                                                    for s, h in inds}),
                           candidate_cut_bel=sorted({get(s, h, 'cut', 'candidate')['bel_at_cut_end']
                                                     for s, h in inds}),
                           no_write_cut_writes=sorted({get(s, h, 'cut', 'no_write')['bel_writes']
                                                       for s, h in inds})),
        '_g2_detail': dict(no_write_cut_relinq=sorted({s for s, h in inds
                                                       if get(s, h, 'cut', 'no_write')['relinquishments'] >= 1})),
        '_g3_detail': dict(force_machinery_move_holds=sorted({s for s, h in inds
                                                              if get(s, h, 'move', 'force_machinery')['relinquishments'] == 0})),
        '_g4_detail': dict(scramble_cut_relinq=sorted({s for s, h in inds
                                                       if get(s, h, 'cut', 'scramble')['relinquishments'] >= 1})),
        '_force_machinery_no_cause_proactive': sorted({get(s, h, 'no_cause', 'force_machinery')['proactive_writes']
                                                       for s, h in inds}),
    }


# ---------------- collectors ----------------
def preflight(protocol='AC108_PROTOCOL_v1.md'):
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


def _collect(root, seeds, do_preflight, conditions=None):
    if conditions is None:
        conditions = list(CONDITIONS)
    if do_preflight:
        preflight()
    outdir = Path(root)
    outdir.mkdir(exist_ok=False)
    hashes = None
    if do_preflight:
        hashes = {n: hashlib.sha256(Path(n).read_bytes()).hexdigest()
                  for n in SOURCES if Path(n).exists()}
        (outdir / 'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = []
    with (outdir / 'rows.jsonl').open('x') as f:
        for seed in seeds:
            for history in (0, 1):
                for cond in conditions:
                    for arm in ARMS:
                        r = run(seed, history, arm, cond)
                        rows.append(r)
                        f.write(json.dumps(r) + '\n')
                        f.flush()
            print(json.dumps(dict(seed=seed, summary=[
                (r['arm'], r['condition'], r['history'], r['completed'], r['first_dead'],
                 r['relinquishments'], r['routes'], r['bel_at_cut_end'], r['bel_at_first_drop'],
                 r['bel_writes'], r['mistakes'])
                for r in rows[-len(conditions) * len(ARMS) * 2:]]), default=str), flush=True)
    repro = None
    if do_preflight:
        # byte-identity is by construction (delegation to ac107's factory); a bounded sample
        # (2 seeds x 2 histories x move+cut x 4 frozen arms) is sufficient to re-verify it.
        repro = reproduction_check(seeds[:2], ('move', 'cut'))
    g = gates_ac108(rows, seeds, repro)
    (outdir / 'results.json').write_text(json.dumps(
        dict(seeds=list(seeds), conditions=conditions, arms=list(ARMS), PORTS=PORTS,
             WINDOW=WINDOW, HOLD_N=HOLD_N, STREAK_N=STREAK_N, gates=g, rows=rows,
             frozen_copy_reproduction=repro,
             hashes=hashes if do_preflight else None),
        indent=2, default=str))
    print(json.dumps(dict(gates=g), indent=2, default=str))
    return g, rows


def collect_engineering(root='ac108_engineering_v1', seeds=None):
    return _collect(root, ENGINEERING if seeds is None else seeds, do_preflight=False)


def collect_finals(root='ac108_results_v1', seeds=None):
    return _collect(root, FINAL_SEEDS if seeds is None else seeds, do_preflight=True)


def main():
    if '--engineering' in sys.argv:
        collect_engineering('ac108_engineering_v1', ENGINEERING)
        return
    if '--smoke' in sys.argv:
        collect_engineering('ac108_smoke_v1', [0, 1, 2])
        return
    if '--finals' in sys.argv:
        collect_finals('ac108_results_v1', FINAL_SEEDS)
        return
    print('AC108: --engineering (seeds 0-7), --smoke (0-2), or --finals (frozen confirmation).')


if __name__ == '__main__':
    main()

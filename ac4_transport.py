"""Explicit lattice transport prerequisite; no controller or production yet."""
from pathlib import Path
import hashlib
import json
import numpy as np

DIRECTIONS = np.array([[1, 0], [-1, 0], [0, 1], [0, -1]], dtype=np.int16)
ARMS = ('open', 'intact', 'decaying', 'one_hole', 'permeant', 'retention_rescue')


def inside(pos):
    return np.max(np.abs(pos), axis=1) <= 2


def crossing_link(pos, proposed):
    """Perimeter edge id, or -1. Both inward and outward crossings supported."""
    a, b = inside(pos), inside(proposed)
    cross = a != b
    inner = np.where(a[:, None], pos, proposed)
    outer = np.where(a[:, None], proposed, pos)
    result = np.full(len(pos), -1, dtype=np.int16)
    for axis, side, offset in ((0, 3, 0), (0, -3, 5), (1, 3, 10), (1, -3, 15)):
        mask = cross & (outer[:, axis] == side)
        result[mask] = offset + inner[mask, 1-axis] + 2
    assert np.all((result >= 0) == cross)
    return result


def move(pos, exported, links, directions, impermeant, retention_rescue=False):
    """Mutate particle state once; exported particles never reenter."""
    proposed = pos + DIRECTIONS[directions]
    edge = crossing_link(pos, proposed)
    attempts = (edge >= 0) & ~exported
    barrier = links[np.maximum(edge, 0)] > 0
    blocked = attempts & impermeant & (barrier | retention_rescue)
    moving = ~exported & ~blocked
    outward = attempts & inside(pos)
    pos[moving] = proposed[moving]
    new_export = ~exported & (np.max(np.abs(pos), axis=1) >= 6)
    exported |= new_export
    return {'attempts': int(attempts.sum()), 'blocked': int(blocked.sum()),
            'outward': int((outward & ~blocked).sum()), 'exported': int(new_export.sum())}


def run(seed, arm):
    if arm not in ARMS:
        raise ValueError(arm)
    rng = np.random.default_rng([seed, 904])
    pos = rng.integers(-2, 3, (512, 2), dtype=np.int16)
    proposals = rng.integers(0, 4, (256, 512), dtype=np.uint8)
    exported = np.zeros(512, dtype=bool)
    links = np.full(20, 512 if arm in ('intact', 'one_hole', 'permeant') else 0, dtype=np.int16)
    if arm == 'decaying':
        links[:] = 32
    if arm == 'one_hole':
        links[0] = 0
    impermeant = np.full(512, arm != 'permeant')
    totals = dict(attempts=0, blocked=0, outward=0, exported=0)
    series = []
    first_crossing = None
    for t, proposal in enumerate(proposals):
        links[links > 0] -= 1
        event = move(pos, exported, links, proposal, impermeant, arm == 'retention_rescue')
        for key in totals:
            totals[key] += event[key]
        if event['outward'] and first_crossing is None:
            first_crossing = t + 1
        n_in = int((inside(pos) & ~exported).sum())
        n_out = int((~inside(pos) & ~exported).sum())
        n_export = int(exported.sum())
        assert n_in + n_out + n_export == 512
        assert n_export == totals['exported']
        series.append([n_in, n_out, n_export])
    return dict(seed=seed, arm=arm, interior=series[-1][0]/512,
                unexported=1-series[-1][2]/512, first_crossing=first_crossing,
                events=totals, inventories=series,
                state_hash=hashlib.sha256(pos.tobytes()+exported.tobytes()).hexdigest())


def main():
    root = Path('ac4_transport_results_v1')
    root.mkdir(exist_ok=False)
    hashes = {name: hashlib.sha256(Path(name).read_bytes()).hexdigest()
              for name in ('ac4_transport.py', 'test_ac4_transport.py', 'AC4_TRANSPORT_PROTOCOL_v1.md')}
    (root/'pre_run_snapshot.json').write_text(json.dumps(hashes, indent=2))
    rows = [run(seed, arm) for seed in range(16) for arm in ARMS]
    for seed in range(16):
        r = {x['arm']: x for x in rows if x['seed'] == seed}
        assert r['intact']['interior'] == 1
        assert r['intact']['state_hash'] == r['retention_rescue']['state_hash']
        assert r['open']['state_hash'] == r['permeant']['state_hash']
        assert r['decaying']['first_crossing'] >= 32
        assert r['decaying']['interior'] < 1
    means = {a: {k: float(np.mean([r[k] for r in rows if r['arm'] == a]))
                 for k in ('interior', 'unexported')} for a in ARMS}
    (root/'results.json').write_text(json.dumps(dict(kind='transport_prerequisite_only',
                   hashes=hashes, rows=rows, means=means), indent=2))
    print(json.dumps(means))


if __name__ == '__main__':
    main()

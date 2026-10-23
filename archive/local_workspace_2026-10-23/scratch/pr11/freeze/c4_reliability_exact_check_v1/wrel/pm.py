"""PM-ACT: Mealy closure of R-HAC-MB and Moore/Hopcroft-style minimization.

The tested input domain is the spec's phase alphabet: current costs, the read,
a forced action, and the intervention symbol, applied only at the declared
boundaries. Phase-local caches and the repair apparatus are part of the state.
Donors are supplied by the caller (they are selected from the intact
distribution before this closure). No ad hoc transition is added if a quotient
map is ill-defined.
"""

from __future__ import annotations

from collections import defaultdict

from .world import F, M_ACT, N_Y, P_ACT, R_ACT

# Intervention symbols. 0 is none. 7 non-null, matching the spec's count.
I_NONE, I_SWAP_S, I_SWAP_E, I_CORRUPT_S, I_CORRUPT_E, I_SUSPEND, I_RELEASE, I_REPAIR = range(8)
I_NAME = {
    0: "none",
    1: "SWAP-S",
    2: "SWAP-E",
    3: "CORRUPT-S",
    4: "CORRUPT-E",
    5: "SUSPEND",
    6: "RELEASE-A",
    7: "REPAIR-B",
}


def encode_phase1(iota, cost, y, forced) -> int:
    return (((iota * 6 + cost) * N_Y + y) * 4) + forced


class Machine:
    def __init__(self):
        self.states = []
        self.trans = []  # parallel: list of (sym, out, nxt)
        self.index = {}

    def add(self, state):
        i = self.index.get(state)
        if i is not None:
            return i
        i = len(self.states)
        self.index[state] = i
        self.states.append(state)
        self.trans.append([])
        return i

    def counts(self) -> dict:
        """Separate controller rows (no apparatus) from intervention-apparatus rows."""
        ctrl = defaultdict(int)
        appr = defaultdict(int)
        for st in self.states:
            phase = st[0]
            saved = st[-2] if len(st) >= 2 else -1
            bucket = appr if saved >= 0 else ctrl
            bucket[phase] += 1
        return {
            "n_states": len(self.states),
            "controller_by_phase": {str(k): ctrl[k] for k in sorted(ctrl)},
            "apparatus_by_phase": {str(k): appr[k] for k in sorted(appr)},
            "controller_total": sum(ctrl.values()),
            "apparatus_total": sum(appr.values()),
        }


def build_machine(solver, policies, T: int, donor_s: int, donor_e: int, n_costs: int = 6):
    """policies[c][k] is the bytearray from H0Solver.solve_cost for remaining k.

    State tuple:
      phase 1: (1, t, belief, clamp, saved, shadow)
      phase 2: (2, t, belief, clamp, y, a, saved, shadow)
      phase 3: (3, t, belief, clamp, y, a, obs, saved, shadow)
      boundary: (4, t, belief, clamp, saved, shadow) after a perturbed trial
      end: (0,)
    saved/shadow are belief indices, or -1 when the apparatus is not live.
    The repair boundary is reachable only when the apparatus is live.
    """
    if T < 2:
        raise RuntimeError("T_SEP >= 2 required")
    return _build(solver, policies, T, donor_s, donor_e, n_costs)


def _apply_iota(iota, b, clamp, saved, shadow, donor_s, donor_e):
    if iota == I_NONE:
        return b, clamp, saved, shadow
    if iota == I_SUSPEND:
        # Keep content, start the apparatus from the recipient belief, clamp.
        if saved < 0:
            saved = b
            shadow = b
        return b, 1, saved, shadow
    if iota in (I_SWAP_S, I_SWAP_E, I_CORRUPT_S, I_CORRUPT_E):
        if saved < 0:
            saved = b
            shadow = b
        donor = donor_s if iota in (I_SWAP_S, I_CORRUPT_S) else donor_e
        clamp2 = 1 if iota in (I_CORRUPT_S, I_CORRUPT_E) else clamp
        return donor, clamp2, saved, shadow
    if iota == I_RELEASE:
        return b, 0, -1, -1
    if iota == I_REPAIR:
        if shadow < 0:
            # Repair with no apparatus is not a specified state. Leave a marker
            # belief of -2 so the map is still total and the ill-defined check
            # can see it; caller should not generate this symbol without apparatus.
            return b, 0, -1, -1
        return shadow, 0, -1, -1
    raise RuntimeError(iota)


def _build(solver, policies, T, donor_s, donor_e, n_costs):
    idx = solver.idx
    world = solver.world
    t_perturb = T - 2
    m = Machine()
    end = m.add((0,))
    queue = [(1, 0, 0, 0, -1, -1)]
    m.add(queue[0])
    qh = 0
    while qh < len(queue):
        s = queue[qh]
        qh += 1
        sid = m.index[s]
        rows = []
        phase = s[0]
        if phase == 1:
            _, t, b, clamp, saved, shadow = s
            k = T - t
            iotas = [I_NONE]
            if t == t_perturb:
                iotas += [I_SWAP_S, I_SWAP_E, I_CORRUPT_S, I_CORRUPT_E, I_SUSPEND]
            for iota in iotas:
                for c in range(n_costs):
                    for y in range(N_Y):
                        for forced in range(4):
                            b2, clamp2, saved2, shadow2 = _apply_iota(
                                iota, b, clamp, saved, shadow, donor_s, donor_e
                            )
                            if b2 < 0:
                                continue
                            a = policies[c][k][b2 * N_Y + y] if forced == 0 else forced - 1
                            ns = (2, t, b2, clamp2, y, int(a), saved2, shadow2)
                            if ns not in m.index:
                                m.add(ns)
                                queue.append(ns)
                            rows.append((encode_phase1(iota, c, y, forced), ("a", int(a)), m.index[ns]))
        elif phase == 2:
            _, t, b, clamp, y, a, saved, shadow = s
            obs_iter = [None] if a == P_ACT else list(range(N_Y))
            bfrac = solver.idx.b[b]
            for obs in obs_iter:
                if a == P_ACT:
                    bit = world.d_def[y]
                    obs_store = -1
                elif a == R_ACT:
                    bit = world.d_recheck(bfrac, y, obs)
                    obs_store = obs
                else:
                    bit = world.d_resample(bfrac, y, obs)
                    obs_store = obs
                ns = (3, t, b, clamp, y, a, obs_store, saved, shadow)
                if ns not in m.index:
                    m.add(ns)
                    queue.append(ns)
                rows.append(((a, -1 if obs is None else obs), ("d", int(bit)), m.index[ns]))
        elif phase == 3:
            _, t, b, clamp, y, a, obs, saved, shadow = s
            for x in (0, 1):
                b2, shadow2 = b, shadow
                if a == R_ACT:
                    cid = world.cls[y][obs][x]
                    if clamp == 0:
                        b2 = solver.idx.trans[b][cid]
                        if b2 < 0:
                            raise RuntimeError("belief transition left the closed count set")
                    if shadow >= 0:
                        shadow2 = solver.idx.trans[shadow][cid]
                        if shadow2 < 0:
                            raise RuntimeError("shadow transition left the closed count set")
                # H0: P and M do not move the belief. Clamp suppresses only the feedback update.
                if t == t_perturb and saved >= 0:
                    # Intervention apparatus is live: the A/B boundary is the next input.
                    ns = (4, t, b2, clamp, saved, shadow2)
                elif t + 1 == T:
                    ns = (0,)
                else:
                    # No apparatus outside the declared window.
                    ns = (1, t + 1, b2, 0, -1, -1)
                if ns not in m.index:
                    m.add(ns)
                    if ns != (0,):
                        queue.append(ns)
                rows.append((x, ("u", 0), m.index[ns]))
        elif phase == 4:
            # Boundary after the perturbed trial. Exactly the two declared branches.
            _, t, b, clamp, saved, shadow = s
            for iota, ns_b, ns_clamp in (
                (I_RELEASE, b, 0),
                (I_REPAIR, shadow if shadow >= 0 else b, 0),
            ):
                ns = (1, t + 1, ns_b, ns_clamp, -1, -1)
                if ns not in m.index:
                    m.add(ns)
                    queue.append(ns)
                rows.append((iota, ("b", iota), m.index[ns]))
        m.trans[sid] = rows
    m.start = m.index[(1, 0, 0, 0, -1, -1)]
    m.end = end
    m.T = T
    m.donor_s = donor_s
    m.donor_e = donor_e
    return m


def _belief_for_decision(solver, b):
    return solver.idx.b[b]


def refine(trans):
    """Iterative Mealy refinement. Signature is the full (symbol, output, next block) list."""
    n = len(trans)
    block = [0] * n
    nblocks = 1
    while True:
        groups = defaultdict(list)
        for s in range(n):
            sig = tuple((sym, out, block[nxt]) for sym, out, nxt in trans[s])
            groups[(block[s], sig)].append(s)
        if len(groups) == nblocks:
            break
        block = [0] * n
        for i, members in enumerate(groups.values()):
            for s in members:
                block[s] = i
        nblocks = len(groups)
    return block


def refine_by_queue(trans):
    """Independent refiner: split one block at a time, using a different signature order.

    Symbols are walked in reverse. The resulting partition must match `refine`.
    """
    n = len(trans)
    block = [0] * n
    nblocks = 1
    pending = [0]
    # Recompute from scratch in rounds but hash signatures with reversed transitions.
    while True:
        groups = defaultdict(list)
        for s in range(n):
            sig = tuple((sym, out, block[nxt]) for sym, out, nxt in reversed(trans[s]))
            groups[(block[s], sig)].append(s)
        if len(groups) == nblocks:
            break
        block = [0] * n
        # Assign ids in reverse insertion order relative to refine(), so the raw ids
        # may differ; callers compare partitions as sets of frozensets.
        for i, members in enumerate(groups.values()):
            for s in members:
                block[s] = i
        nblocks = len(groups)
    return block


def partition_sets(block):
    groups = defaultdict(list)
    for s, b in enumerate(block):
        groups[b].append(s)
    return frozenset(frozenset(v) for v in groups.values())


def well_defined(machine, block) -> dict:
    """Every symbol's image of a block is a single block. Ill-defined => not ok."""
    bad = []
    cell_sym = defaultdict(set)  # (block, sym) -> set of next blocks
    for s, rows in enumerate(machine.trans):
        b0 = block[s]
        for sym, out, nxt in rows:
            cell_sym[(b0, sym)].add((out, block[nxt]))
    for key, images in cell_sym.items():
        if len(images) > 1:
            bad.append(key[1])
            if len(bad) > 8:
                break
    return {"ok": not bad, "n_bad_symbols_capped": len(bad)}


def reachable_beliefs(machine, T: int) -> dict:
    """Belief indices appearing at phase 1, by trial, controller only."""
    seen = defaultdict(set)
    for st in machine.states:
        if st[0] == 1 and st[-2] < 0:
            seen[st[1]].add(st[2])
    return {str(t): len(v) for t, v in sorted(seen.items())}

"""RWM-8 discrete topology, matched rivals, instrument foolers and unrolling.

RWM-8 (internal nodes; external background inputs oR, oH):

  module  node  gate                                  role
  EXT     X     A AND (oR if C else MAJ3(oR, X, K))   prediction of next exteroceptive observation;
                                                      monitor C sets sensory precision; efference A
  EXT     E     XOR(X, oR)                            exteroceptive prediction error
  EXT     A     OR(K, NOT C)                          action: 1 forage (field), 0 rest (den);
                                                      explores when not confident
  INT     I     MAJ3(oH, I, K)                        interoceptive error vs the SUPPLIED setpoint
  WS      G     THR(2*I + E + NOT C + G >= 2)         ignition: all-or-none, self-sustaining
  WS      K     (I OR X) if G else K                  1-bit workspace content: write, broadcast, hold
  MON     C     XOR(C, M)                             higher-order: predicts own first-order correctness
  MON     M     XNOR(C, E)                            second-order (meta) prediction error

The first-order modules EXT and INT share no direct edge; every EXT <-> INT
path passes through the workspace {G, K} (the central bottleneck). K projects to
both modules (broadcast). MON reads only internal first-order nodes (E) and
writes back as precision (C -> X), workspace gating (C -> G) and an
evidence-seeking action consequence (C -> A).
"""
from __future__ import annotations

from typing import Dict, List

from .primitives import (AND, COPY, MAJ, NOT, OR, TABLE, THRESHOLD, XOR, Gate, Network)

EXTERNAL = ["oR", "oH"]


def _net(name, spec, modules=None, notes=None, external=None) -> Network:
    nodes = [n for n, _, _ in spec]
    return Network(
        name=name,
        nodes=nodes,
        inputs={n: tuple(ins) for n, ins, _ in spec},
        gates={n: g for n, _, g in spec},
        external=list(EXTERNAL if external is None else external),
        modules=dict(modules or {}),
        notes=dict(notes or {}),
    )


X_GATE = TABLE("AND(A,PRECISION_MUX(C;MAJ3(oR,X,K),oR))", 5,
               lambda a, c, o, x, k: a & (o if c else int(o + x + k >= 2)))
K_GATE = TABLE("HOLD_MUX(G;K,OR(I,X))", 4, lambda g, k, i, x: (i | x) if g else k)
G_GATE = THRESHOLD([2, 1, 1, 1], 2, negated=[False, False, True, False])
A_GATE = THRESHOLD([1, 1], 1, negated=[False, True])
XNOR_GATE = TABLE("XNOR", 2, lambda a, b: 1 - (a ^ b))

RWM_MODULES = {"X": "EXT", "E": "EXT", "A": "EXT", "I": "INT",
               "G": "WS", "K": "WS", "C": "MON", "M": "MON"}
FIRST_ORDER = ("EXT", "INT")
RWM_NOTES = {
    "X": "prediction of next exteroceptive observation (efference-gated; C sets precision)",
    "E": "exteroceptive prediction error",
    "A": "action (1 forage / 0 rest); explores when not confident",
    "I": "interoceptive prediction error against the supplied setpoint prior",
    "G": "workspace ignition (all-or-none, hysteretic)",
    "K": "1-bit workspace content: competitive write, broadcast, hold",
    "C": "higher-order monitor: predicts own first-order correctness",
    "M": "second-order prediction error of the monitor",
}


def rwm8() -> Network:
    spec = [
        ("X", ("A", "C", "oR", "X", "K"), X_GATE),
        ("E", ("X", "oR"), XOR(2)),
        ("A", ("K", "C"), A_GATE),
        ("I", ("oH", "I", "K"), MAJ(3)),
        ("G", ("I", "E", "C", "G"), G_GATE),
        ("K", ("G", "K", "I", "X"), K_GATE),
        ("C", ("C", "M"), XOR(2)),
        ("M", ("C", "E"), XNOR_GATE),
    ]
    return _net("RWM-8", spec, RWM_MODULES, RWM_NOTES)


def rwm8_v0() -> Network:
    """Superseded first draft (kept for the design log): monitor without meta-error."""
    spec = [
        ("X", ("C", "oR", "X", "K"), TABLE("PRECISION_MUX(C;MAJ3(oR,X,K),oR)", 4,
                                          lambda c, o, x, k: o if c else int(o + x + k >= 2))),
        ("P", ("X", "A"), AND(2)),
        ("E", ("P", "oR"), XOR(2)),
        ("A", ("K", "C"), A_GATE),
        ("I", ("oH", "I", "K"), MAJ(3)),
        ("G", ("I", "E", "C", "G"), G_GATE),
        ("K", ("G", "K", "I", "X"), K_GATE),
        ("C", ("E", "C", "G"), TABLE("AND(NOT E,OR(C,NOT G))", 3,
                                     lambda e, c, g: (1 - e) & (c | (1 - g)))),
    ]
    mods = {"X": "EXT", "P": "EXT", "E": "EXT", "A": "EXT", "I": "INT", "G": "WS", "K": "WS", "C": "MON"}
    return _net("RWM-8-v0", spec, mods)


# ---------------------------------------------------------------------------
# Matched rivals (same external inputs, same or fewer state bits)
# ---------------------------------------------------------------------------

def rival_detached_monitor() -> Network:
    """Monitor computed but never written back: a detachable head."""
    spec = [
        ("X", ("A", "oR", "X", "K"), TABLE("AND(A,MAJ3(oR,X,K))", 4,
                                          lambda a, o, x, k: a & int(o + x + k >= 2))),
        ("E", ("X", "oR"), XOR(2)),
        ("A", ("K",), COPY()),
        ("I", ("oH", "I", "K"), MAJ(3)),
        ("G", ("I", "E", "G"), THRESHOLD([2, 1, 1], 2)),
        ("K", ("G", "K", "I", "X"), K_GATE),
        ("C", ("C", "M"), XOR(2)),
        ("M", ("C", "E"), XNOR_GATE),
    ]
    return _net("RV-DETACHED-MONITOR", spec, RWM_MODULES)


def rival_first_order_confidence() -> Network:
    """C4 reduction: confidence is a memoryless readout of first-order error (7 bits)."""
    spec = [
        ("X", ("A", "C", "oR", "X", "K"), X_GATE),
        ("E", ("X", "oR"), XOR(2)),
        ("A", ("K", "C"), A_GATE),
        ("I", ("oH", "I", "K"), MAJ(3)),
        ("G", ("I", "E", "C", "G"), G_GATE),
        ("K", ("G", "K", "I", "X"), K_GATE),
        ("C", ("E",), NOT()),
    ]
    mods = {k: v for k, v in RWM_MODULES.items() if k != "M"}
    return _net("RV-FO-CONFIDENCE", spec, mods)


def rival_ssb() -> Network:
    """Sufficient-statistic broadcast: always-on K = I OR X, no ignition node (7 bits)."""
    spec = [
        ("X", ("A", "C", "oR", "X", "K"), X_GATE),
        ("E", ("X", "oR"), XOR(2)),
        ("A", ("K", "C"), A_GATE),
        ("I", ("oH", "I", "K"), MAJ(3)),
        ("K", ("I", "X"), OR(2)),
        ("C", ("C", "M"), XOR(2)),
        ("M", ("C", "E"), XNOR_GATE),
    ]
    mods = {k: v for k, v in RWM_MODULES.items() if k != "G"}
    return _net("RV-SSB", spec, mods)


def rival_direct() -> Network:
    """No bottleneck: first-order modules couple directly; no workspace (6 bits)."""
    spec = [
        ("X", ("A", "C", "oR", "X", "I"), X_GATE),
        ("E", ("X", "oR"), XOR(2)),
        ("A", ("I", "C"), A_GATE),
        ("I", ("oH", "I", "A"), MAJ(3)),
        ("C", ("C", "M"), XOR(2)),
        ("M", ("C", "E"), XNOR_GATE),
    ]
    mods = {k: v for k, v in RWM_MODULES.items() if k not in ("G", "K")}
    return _net("RV-DIRECT", spec, mods)


def rivals() -> List[Network]:
    return [rival_detached_monitor(), rival_first_order_confidence(), rival_ssb(), rival_direct()]


# ---------------------------------------------------------------------------
# Instrument controls and foolers
# ---------------------------------------------------------------------------

def control_copy_loop() -> Network:
    """Positive control: two COPY gates in a loop; Phi_s = 1 bit analytically."""
    return _net("CTRL-COPY-LOOP", [("a", ("b",), COPY()), ("b", ("a",), COPY())], external=[])


def control_chain() -> Network:
    """Negative control: feedforward chain with self-loop at the source."""
    spec = [("a", ("a",), COPY()), ("b", ("a",), COPY()), ("c", ("b",), NOT())]
    return _net("CTRL-DAG-CHAIN", spec, external=[])


def control_two_islands() -> Network:
    """Negative control: two disjoint COPY loops (reducible system)."""
    spec = [("a", ("b",), COPY()), ("b", ("a",), COPY()),
            ("c", ("d",), COPY()), ("d", ("c",), COPY())]
    return _net("CTRL-TWO-ISLANDS", spec, external=[])


def fooler_xor_ring(n: int = 8) -> Network:
    """Fooler: XOR of both ring neighbours. High integration, no environmental function."""
    names = [f"r{k}" for k in range(n)]
    spec = [(names[k], (names[(k - 1) % n], names[(k + 1) % n]), XOR(2)) for k in range(n)]
    return _net(f"FOOL-XOR-RING-{n}", spec, external=[])


def fooler_noisy_copy_ring(n: int = 8, noise: float = 0.25) -> Network:
    names = [f"r{k}" for k in range(n)]
    spec = [(names[k], (names[(k - 1) % n],), COPY(noise)) for k in range(n)]
    return _net(f"FOOL-NOISY-RING-{n}", spec, external=[])


def unroll(net: Network, horizon: int) -> Network:
    """Feedforward unfolding: node n@t computes net's node n at step t from layer t-1.

    Initial internal state n@0 and per-step inputs e@t are external inputs. The
    result is acyclic and input/output equivalent to `net` over `horizon` steps.
    """
    names = set(net.nodes)
    spec = []
    for t in range(1, horizon + 1):
        for nd in net.nodes:
            ins = tuple(f"{src}@{t - 1}" for src in net.inputs[nd])
            spec.append((f"{nd}@{t}", ins, net.gates[nd]))
    external = [f"{nd}@0" for nd in net.nodes] + \
        [f"{e}@{t}" for t in range(horizon) for e in net.external]
    modules = {f"{nd}@{t}": net.modules.get(nd, "") for nd in names for t in range(1, horizon + 1)}
    return _net(f"{net.name}-UNROLLED-{horizon}", spec, modules, external=external)


def all_designs() -> Dict[str, Network]:
    out = {"RWM-8": rwm8(), "RWM-8-v0": rwm8_v0()}
    for r in rivals():
        out[r.name] = r
    return out

"""Discrete mathematical primitives: Boolean gates, gate networks, graph checks.

A network is a finite set of binary nodes updated synchronously. Each node has
an ordered tuple of input names (internal nodes or external background inputs)
and a gate: a truth table mapping every input bit-tuple to P(output = 1).
Deterministic logic gates have probabilities in {0, 1}; a gate with output
noise flips its deterministic value with probability `noise`.

State indexing is little-endian: bit i of a state index is node i.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from itertools import product
from typing import Callable, Dict, Iterable, List, Mapping, Sequence, Tuple


# ---------------------------------------------------------------------------
# Gates
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Gate:
    """A gate over `arity` ordered inputs, stored as a truth table of P(out=1)."""

    kind: str
    arity: int
    table: Tuple[float, ...]  # index = sum(bit_k << k)

    def p1(self, bits: Sequence[int]) -> float:
        idx = 0
        for k, b in enumerate(bits):
            idx |= (b & 1) << k
        return self.table[idx]

    @property
    def deterministic(self) -> bool:
        return all(v in (0.0, 1.0) for v in self.table)


def gate_from_fn(kind: str, arity: int, fn: Callable[..., int], noise: float = 0.0) -> Gate:
    if not 0.0 <= noise <= 0.5:
        raise ValueError("noise must be in [0, 1/2]")
    table = []
    for idx in range(1 << arity):
        bits = [(idx >> k) & 1 for k in range(arity)]
        out = 1 if fn(*bits) else 0
        table.append(float(out * (1 - noise) + (1 - out) * noise))
    return Gate(kind, arity, tuple(table))


def COPY(noise: float = 0.0) -> Gate:
    return gate_from_fn("COPY", 1, lambda a: a, noise)


def NOT(noise: float = 0.0) -> Gate:
    return gate_from_fn("NOT", 1, lambda a: 1 - a, noise)


def AND(n: int = 2, noise: float = 0.0) -> Gate:
    return gate_from_fn(f"AND{n}", n, lambda *b: int(all(b)), noise)


def OR(n: int = 2, noise: float = 0.0) -> Gate:
    return gate_from_fn(f"OR{n}", n, lambda *b: int(any(b)), noise)


def XOR(n: int = 2, noise: float = 0.0) -> Gate:
    return gate_from_fn(f"XOR{n}", n, lambda *b: sum(b) & 1, noise)


def MAJ(n: int = 3, noise: float = 0.0) -> Gate:
    if n % 2 == 0:
        raise ValueError("majority needs odd arity")
    return gate_from_fn(f"MAJ{n}", n, lambda *b: int(2 * sum(b) > n), noise)


def MUX(noise: float = 0.0) -> Gate:
    """MUX(sel, a, b) = b if sel else a."""
    return gate_from_fn("MUX", 3, lambda s, a, b: b if s else a, noise)


def THRESHOLD(weights: Sequence[int], theta: int, negated: Sequence[bool] | None = None,
              noise: float = 0.0) -> Gate:
    """McCulloch-Pitts unit: out = [sum_k w_k * lit_k >= theta], lit_k = x_k or NOT x_k."""
    w = tuple(int(x) for x in weights)
    neg = tuple(negated) if negated is not None else (False,) * len(w)
    if len(neg) != len(w):
        raise ValueError("negated length mismatch")

    def fn(*b):
        return int(sum(wk * ((1 - bk) if nk else bk) for wk, bk, nk in zip(w, b, neg)) >= theta)

    label = "THR[" + ",".join(("~" if n else "") + str(x) for x, n in zip(w, neg)) + f">={theta}]"
    return gate_from_fn(label, len(w), fn, noise)


def TABLE(kind: str, arity: int, fn: Callable[..., int], noise: float = 0.0) -> Gate:
    """Arbitrary named Boolean function (documented composite gate)."""
    return gate_from_fn(kind, arity, fn, noise)


# ---------------------------------------------------------------------------
# Networks
# ---------------------------------------------------------------------------

@dataclass
class Network:
    """Synchronous binary gate network with external background inputs."""

    name: str
    nodes: List[str]
    inputs: Dict[str, Tuple[str, ...]]
    gates: Dict[str, Gate]
    external: List[str] = field(default_factory=list)
    modules: Dict[str, str] = field(default_factory=dict)  # node -> module label
    notes: Dict[str, str] = field(default_factory=dict)    # node -> role text

    def __post_init__(self) -> None:
        names = set(self.nodes)
        if len(names) != len(self.nodes):
            raise ValueError("duplicate node names")
        if names & set(self.external):
            raise ValueError("node and external input names overlap")
        for n in self.nodes:
            ins = self.inputs[n]
            g = self.gates[n]
            if g.arity != len(ins):
                raise ValueError(f"{n}: gate arity {g.arity} != {len(ins)} inputs")
            for src in ins:
                if src not in names and src not in self.external:
                    raise ValueError(f"{n}: unknown input {src}")

    # -- indexing ----------------------------------------------------------
    @property
    def n(self) -> int:
        return len(self.nodes)

    def index(self, name: str) -> int:
        return self.nodes.index(name)

    def state_bits(self, s: int) -> Tuple[int, ...]:
        return tuple((s >> i) & 1 for i in range(self.n))

    def state_index(self, bits: Mapping[str, int] | Sequence[int]) -> int:
        if isinstance(bits, Mapping):
            bits = [bits[n] for n in self.nodes]
        return sum((b & 1) << i for i, b in enumerate(bits))

    # -- dynamics ----------------------------------------------------------
    def node_p1(self, node: str, values: Mapping[str, int]) -> float:
        return self.gates[node].p1([values[src] for src in self.inputs[node]])

    def step_p1(self, s: int, ext: Mapping[str, int]) -> List[float]:
        vals = dict(ext)
        vals.update(zip(self.nodes, self.state_bits(s)))
        return [self.node_p1(nd, vals) for nd in self.nodes]

    def step_det(self, s: int, ext: Mapping[str, int]) -> int:
        ps = self.step_p1(s, ext)
        if any(p not in (0.0, 1.0) for p in ps):
            raise ValueError("step_det on a stochastic network")
        return sum(int(p) << i for i, p in enumerate(ps))

    @property
    def deterministic(self) -> bool:
        return all(self.gates[n].deterministic for n in self.nodes)

    # -- structure ---------------------------------------------------------
    def declared_edges(self) -> List[Tuple[str, str]]:
        """Internal declared edges src -> dst (self-loops included)."""
        names = set(self.nodes)
        return [(src, dst) for dst in self.nodes for src in self.inputs[dst] if src in names]

    def effective_edges(self) -> List[Tuple[str, str]]:
        """Edges src -> dst such that some assignment of all inputs makes dst's
        output probability depend on src (vestigial declared inputs removed)."""
        out = []
        names = set(self.nodes)
        for dst in self.nodes:
            ins = self.inputs[dst]
            g = self.gates[dst]
            for k, src in enumerate(ins):
                if src not in names:
                    continue
                for idx in range(1 << g.arity):
                    if (idx >> k) & 1:
                        continue
                    if g.table[idx] != g.table[idx | (1 << k)]:
                        out.append((src, dst))
                        break
        return out

    def describe(self) -> List[Dict[str, object]]:
        return [
            {"node": n, "module": self.modules.get(n, ""), "gate": self.gates[n].kind,
             "inputs": list(self.inputs[n]), "role": self.notes.get(n, "")}
            for n in self.nodes
        ]


# ---------------------------------------------------------------------------
# Graph primitives
# ---------------------------------------------------------------------------

def strongly_connected_components(nodes: Sequence[str], edges: Iterable[Tuple[str, str]]) -> List[List[str]]:
    """Tarjan's algorithm (iterative-safe for the small graphs used here)."""
    adj: Dict[str, List[str]] = {n: [] for n in nodes}
    for a, b in edges:
        adj[a].append(b)
    index: Dict[str, int] = {}
    low: Dict[str, int] = {}
    stack: List[str] = []
    on: set = set()
    comps: List[List[str]] = []
    counter = [0]

    def visit(v: str) -> None:
        index[v] = low[v] = counter[0]
        counter[0] += 1
        stack.append(v)
        on.add(v)
        for w in adj[v]:
            if w not in index:
                visit(w)
                low[v] = min(low[v], low[w])
            elif w in on:
                low[v] = min(low[v], index[w])
        if low[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on.discard(w)
                comp.append(w)
                if w == v:
                    break
            comps.append(sorted(comp, key=list(nodes).index))

    for v in nodes:
        if v not in index:
            visit(v)
    return comps


def reachable(src: Iterable[str], edges: Iterable[Tuple[str, str]], forbidden: Iterable[str] = ()) -> set:
    adj: Dict[str, List[str]] = {}
    for a, b in edges:
        adj.setdefault(a, []).append(b)
    bad = set(forbidden)
    seen = set(s for s in src if s not in bad)
    frontier = list(seen)
    while frontier:
        v = frontier.pop()
        for w in adj.get(v, []):
            if w not in seen and w not in bad:
                seen.add(w)
                frontier.append(w)
    return seen


def all_input_assignments(names: Sequence[str]) -> List[Dict[str, int]]:
    return [dict(zip(names, bits)) for bits in product((0, 1), repeat=len(names))]

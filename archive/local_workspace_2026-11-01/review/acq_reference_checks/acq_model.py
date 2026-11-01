"""Reference-only world/fault model for acquired_self_correctness_spec_v1 (sha 54bc8ea3...).
Exact rationals. No network, no learner, no GRU code. PROPOSED v1 values only."""
from fractions import Fraction as Fr
from functools import lru_cache
import itertools

PHI = Fr(1, 4); KAPPA = Fr(1, 4); KMAX = 3
C = {"P": Fr(0), "R": Fr(1, 100), "S": Fr(3, 50)}
PREF = ("P", "R", "S")  # tie preference
CUES = ("lo", "hi")

def graded_model():
    E1 = {"lo": [1, 1, 2, 3, 5, 12], "hi": [2, 3, 4, 4, 5, 6]}
    def e(y, Y, N):  # y in 0..5 represents 1..6
        t = E1[N]
        return Fr(t[y] if Y == 1 else t[5 - y], 24)
    def q(rec, y, F):
        if F == 0:
            return Fr(1) if rec == y else Fr(0)
        return (1 - 5 * KAPPA / 6) if rec == y else KAPPA / 6
    return dict(name="graded", A=6, e=e, q=q)

def binary_model():  # Appendix A
    eps = {"lo": Fr(1, 10), "hi": Fr(3, 10)}
    def e(x, Y, N):
        return 1 - eps[N] if x == Y else eps[N]
    def q(rec, x, F):
        if F == 0:
            return Fr(1) if rec == x else Fr(0)
        return 1 - KAPPA if rec == x else KAPPA
    return dict(name="binary", A=2, e=e, q=q)

class Ref:
    """R-HIST: exact Bayes over received history with world + fault law."""
    def __init__(self, M, kmax=KMAX):
        self.M = M; self.A = M["A"]; self.kmax = kmax
        self._alpha = {}; self._V = {}

    def alpha(self, r):
        """r = (N, ((type, rec), ...)). Returns dict (Y,F) -> list over current sample y of
        P(reads, current sample=y | Y, F, N)."""
        if r in self._alpha: return self._alpha[r]
        N, reads = r; e, q, A = self.M["e"], self.M["q"], self.A
        if len(reads) == 1:
            out = {(Y, F): [e(y, Y, N) * q(reads[0][1], y, F) for y in range(A)]
                   for Y in (0, 1) for F in (0, 1)}
        else:
            prev = self.alpha((N, reads[:-1])); t, rec = reads[-1]; out = {}
            for (Y, F), a in prev.items():
                if t == "R":
                    out[(Y, F)] = [a[y] * q(rec, y, F) for y in range(A)]
                else:
                    s = sum(a)
                    out[(Y, F)] = [s * e(y, Y, N) * q(rec, y, F) for y in range(A)]
        self._alpha[r] = out
        return out

    def joint(self, r):  # P(reads, Y | N) per Y, marginal over F
        a = self.alpha(r)
        return {Y: Fr(1, 2) * ((1 - PHI) * sum(a[(Y, 0)]) + PHI * sum(a[(Y, 1)])) for Y in (0, 1)}

    def p1(self, r):
        j = self.joint(r); z = j[0] + j[1]
        return j[1] / z

    def decision(self, r):
        return 1 if self.p1(r) > Fr(1, 2) else 0

    def assess(self, r):
        p = self.p1(r); return max(p, 1 - p)

    def pF1(self, r):
        a = self.alpha(r)
        n = PHI * (sum(a[(0, 1)]) + sum(a[(1, 1)]))
        d = n + (1 - PHI) * (sum(a[(0, 0)]) + sum(a[(1, 0)]))
        return n / d

    def posterior_vec(self, r):  # over (Y,F,ycur)
        a = self.alpha(r); w = {}
        for (Y, F), v in a.items():
            pf = PHI if F else 1 - PHI
            for y in range(self.A): w[(Y, F, y)] = Fr(1, 2) * pf * v[y]
        z = sum(w.values())
        return {k: x / z for k, x in w.items()}

    def next_probs(self, r, t):
        j0 = self.joint(r); z = j0[0] + j0[1]; out = []
        for rec in range(self.A):
            r2 = (r[0], r[1] + ((t, rec),)); j = self.joint(r2)
            out.append((rec, r2, (j[0] + j[1]) / z))
        return out

    def Q(self, r):
        k = len(r[1]); qs = {"P": self.assess(r)}
        if k <= self.kmax:
            for t in ("R", "S"):
                qs[t] = -C[t] + sum(p * self.V(r2) for _, r2, p in self.next_probs(r, t) if p)
        return qs

    def V(self, r):
        if r not in self._V:
            self._V[r] = max(self.Q(r).values())
        return self._V[r]

    def act(self, r):
        qs = self.Q(r); best = max(qs.values())
        return next(a for a in PREF if a in qs and qs[a] == best)

def received_histories(A, kmax=KMAX):
    for N in CUES:
        for k in range(1, kmax + 2):
            for types in itertools.product("RS", repeat=k - 1):
                for recs in itertools.product(range(A), repeat=k):
                    yield (N, tuple(zip(("F",) + types, recs)))

def world_histories(M, k):
    """World-observable histories at stage k: (N, types, samples) with P(samples | N) and
    per-read sample index map."""
    A = M["A"]
    for N in CUES:
        for types in itertools.product("RS", repeat=k - 1):
            ns = 1 + types.count("S")
            idx = [0]
            for t in types: idx.append(idx[-1] + (1 if t == "S" else 0))
            for samples in itertools.product(range(A), repeat=ns):
                pY = {Y: Fr(1, 2) * prod(M["e"](y, Y, N) for y in samples) for Y in (0, 1)}
                yield dict(N=N, types=types, samples=samples, idx=idx, pY=pY)

def prod(it):
    out = Fr(1)
    for x in it: out *= x
    return out

def latent_patterns(M, H):
    """(F, received tuple, P(F) * P(rec | F, samples)) with positive weight only."""
    A, q = M["A"], M["q"]; k = len(H["idx"])
    truth = tuple(H["samples"][i] for i in H["idx"])
    yield (0, truth, 1 - PHI)
    for rec in itertools.product(range(A), repeat=k):
        w = PHI * prod(q(rec[i], truth[i], 1) for i in range(k))
        if w: yield (1, rec, w)

def split_E(H):
    return (H["samples"][0] + 1 + (1 if H["N"] == "hi" else 0)) % 2 == 1  # y1 in 1..6

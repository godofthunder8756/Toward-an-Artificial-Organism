"""W-REL-B observation model in exact rationals.

The constructor takes arbitrary swapped or unswapped noise rates. Study rates are
not referenced here. Callers that run ITEM quantities pass those rates themselves.

Per-read flip probability is eps = w + e - 2we. When the two regimes swap
(w, e), eps agrees and non-recheck emissions agree. The value code requires
that agreement and checks it.
"""

from __future__ import annotations

from fractions import Fraction

F = Fraction
N = 3
N_Y = 1 << N  # 8
P_ACT, R_ACT, M_ACT = 0, 1, 2
ACT_NAME = ("P", "R", "M")

# (n_ac, n_aw, n_d) with n_ac + n_aw + n_d = 3, lex order.
CLASSES = tuple(
    (nac, naw, N - nac - naw) for nac in range(N + 1) for naw in range(N - nac + 1)
)
assert len(CLASSES) == 10
CLASS_OF = {c: i for i, c in enumerate(CLASSES)}


def _popcount(x: int) -> int:
    return x.bit_count()


def read_class(y: int) -> int:
    """0 = unanimous, 1 = split."""
    return 0 if y == 0 or y == N_Y - 1 else 1


def _bit_table(w: Fraction, e: Fraction):
    """Per-bit recheck probabilities and the marginal flip eps."""
    eps = w + e - 2 * w * e
    p_ac = (1 - w) * (1 - e) ** 2 + w * e ** 2
    p_aw = (1 - w) * e ** 2 + w * (1 - e) ** 2
    # Each specific disagree direction (y agrees / y' agrees).
    p_dir = e * (1 - e)
    assert p_ac + p_aw + 2 * p_dir == 1
    return eps, p_ac, p_aw, p_dir


def _pattern_L(y: int, yp: int, x: int, p_ac, p_aw, p_dir) -> Fraction:
    target = 0 if x == 0 else N_Y - 1
    out = F(1)
    nac = naw = nd = 0
    for i in range(N):
        yb = (y >> i) & 1
        pb = (yp >> i) & 1
        tb = (target >> i) & 1
        if yb != pb:
            out *= p_dir
            nd += 1
        elif yb == tb:
            out *= p_ac
            nac += 1
        else:
            out *= p_aw
            naw += 1
    return out, (nac, naw, nd)


def _default_L(y: int, x: int, eps: Fraction) -> Fraction:
    target = 0 if x == 0 else N_Y - 1
    d = _popcount(y ^ target)
    return eps**d * (1 - eps) ** (N - d)


class World:
    def __init__(self, w_s: Fraction, e_s: Fraction, w_e: Fraction, e_e: Fraction, h: Fraction):
        self.w = (F(w_s), F(w_e))
        self.e = (F(e_s), F(e_e))
        self.h = F(h)
        self.eps = []
        self.p_ac = []
        self.p_aw = []
        self.p_dir = []
        for z in (0, 1):
            eps, p_ac, p_aw, p_dir = _bit_table(self.w[z], self.e[z])
            self.eps.append(eps)
            self.p_ac.append(p_ac)
            self.p_aw.append(p_aw)
            self.p_dir.append(p_dir)
        # Ldef[z][y][x] = P(y | X=x, Z=z)
        self.Ldef = [[[_default_L(y, x, self.eps[z]) for x in (0, 1)] for y in range(N_Y)] for z in (0, 1)]
        # Lre[z][y][yp][x] = P(y, y' | X=x, Z=z), and class id for that triple.
        self.Lre = [[[[None for _ in (0, 1)] for _ in range(N_Y)] for _ in range(N_Y)] for _ in (0, 1)]
        self.cls = [[[0 for _ in (0, 1)] for _ in range(N_Y)] for _ in range(N_Y)]
        # Pattern likelihood by class (same for every pattern in the class).
        self.Lpat = [[None for _ in CLASSES] for _ in (0, 1)]
        for z in (0, 1):
            for y in range(N_Y):
                for yp in range(N_Y):
                    for x in (0, 1):
                        val, key = _pattern_L(y, yp, x, self.p_ac[z], self.p_aw[z], self.p_dir[z])
                        self.Lre[z][y][yp][x] = val
                        cid = CLASS_OF[key]
                        self.cls[y][yp][x] = cid
                        if self.Lpat[z][cid] is None:
                            self.Lpat[z][cid] = val
                        elif self.Lpat[z][cid] != val:
                            raise RuntimeError("class likelihood not constant")
        self.ratio = []
        for c in range(10):
            self.ratio.append(self.Lpat[0][c] / self.Lpat[1][c])
        # Marginal P(y | z) and P(y, x | z).
        self.py = [[F(0) for _ in range(N_Y)] for _ in (0, 1)]
        self.pyx = [[[F(0) for _ in (0, 1)] for _ in range(N_Y)] for _ in (0, 1)]
        for z in (0, 1):
            for y in range(N_Y):
                for x in (0, 1):
                    w = F(1, 2) * self.Ldef[z][y][x]
                    self.pyx[z][y][x] = w
                    self.py[z][y] += w
        self.emissions_match = all(self.Ldef[0][y][x] == self.Ldef[1][y][x] for y in range(N_Y) for x in (0, 1))
        self._build_f0()
        self._build_outcome_tables()

    def _build_f0(self) -> None:
        """Decisions and predictive probabilities at b in {0, 1/2, 1}."""
        self.p_def = [F(0)] * N_Y  # P(X=1 | y) — regime-free when emissions match
        self.d_def = [0] * N_Y
        for y in range(N_Y):
            # Use the mixture with weight 1/2. If emissions match this is exact for every b.
            num = F(0)
            den = F(0)
            for z, bz in ((0, F(1, 2)), (1, F(1, 2))):
                for x in (0, 1):
                    w = bz * self.pyx[z][y][x]
                    den += w
                    if x == 1:
                        num += w
            p = num / den
            self.p_def[y] = p
            self.d_def[y] = 1 if p > F(1, 2) else 0
        # recheck / resample predictive p at a supplied belief, cached for endpoints and 1/2
        self.p_re = {}  # (b, y, yp) -> p
        self.d_re = {}
        self.p_rs = {}
        self.d_rs = {}

    def p_recheck(self, b: Fraction, y: int, yp: int) -> Fraction:
        key = (b, y, yp)
        hit = self.p_re.get(key)
        if hit is not None:
            return hit
        s0 = self.Lre[0][y][yp][0]
        s1 = self.Lre[0][y][yp][1]
        e0 = self.Lre[1][y][yp][0]
        e1 = self.Lre[1][y][yp][1]
        num = b * s1 + (1 - b) * e1
        den = b * (s0 + s1) + (1 - b) * (e0 + e1)
        p = num / den
        self.p_re[key] = p
        self.d_re[key] = 1 if p > F(1, 2) else 0
        return p

    def d_recheck(self, b: Fraction, y: int, yp: int) -> int:
        self.p_recheck(b, y, yp)
        return self.d_re[(b, y, yp)]

    def p_resample(self, b: Fraction, y: int, ypp: int) -> Fraction:
        key = (b, y, ypp)
        hit = self.p_rs.get(key)
        if hit is not None:
            return hit
        # Independent reads given X. Likelihood may depend on z through eps.
        num = F(0)
        den = F(0)
        for x in (0, 1):
            mix = F(0)
            for z, bz in ((0, b), (1, 1 - b)):
                mix += bz * self.Ldef[z][y][x] * self.Ldef[z][ypp][x]
            den += mix
            if x == 1:
                num += mix
        p = num / den
        self.p_rs[key] = p
        self.d_rs[key] = 1 if p > F(1, 2) else 0
        return p

    def d_resample(self, b: Fraction, y: int, ypp: int) -> int:
        self.p_resample(b, y, ypp)
        return self.d_rs[(b, y, ypp)]

    def _build_outcome_tables(self) -> None:
        """F0 correctness and class marginals. b_pred fixed at 1/2 for F0."""
        b = F(1, 2)
        # correct mass [z][a][r], and p_read [z][r]
        self.p_read = [[F(0), F(0)] for _ in (0, 1)]
        mass = [[[F(0), F(0)] for _ in range(3)] for _ in (0, 1)]
        # class joint P(y and class | z) [z][y][c]
        self.p_y_class = [[[F(0) for _ in range(10)] for _ in range(N_Y)] for _ in (0, 1)]
        # MF agreement joint: for action R, P(correct, g_new | z, r) accumulated as mass
        # g_new in 0..3. We'll store list later.
        acc_g = [[[{(0, g): F(0) for g in range(4)} for _ in range(2)] for _ in (0, 1)] for _ in range(1)]
        # index by z, r
        gmass = [[ {(c, g): F(0) for c in (0, 1) for g in range(4)} for _ in range(2)] for _ in (0, 1)]
        for z in (0, 1):
            for x in (0, 1):
                for y in range(N_Y):
                    r = read_class(y)
                    wy = F(1, 2) * self.Ldef[z][y][x]
                    self.p_read[z][r] += wy
                    if self.d_def[y] == x:
                        mass[z][P_ACT][r] += wy
                    for yp in range(N_Y):
                        w = F(1, 2) * self.Lre[z][y][yp][x]
                        cid = self.cls[y][yp][x]
                        self.p_y_class[z][y][cid] += w
                        d = self.d_recheck(b, y, yp)
                        if d == x:
                            mass[z][R_ACT][r] += w
                        # agreement count, independent of how we score correctness
                        agree = N - _popcount(y ^ yp)
                        gmass[z][r][(1 if d == x else 0, agree)] += w
                    for ypp in range(N_Y):
                        w = F(1, 2) * self.Ldef[z][y][x] * self.Ldef[z][ypp][x]
                        d = self.d_resample(b, y, ypp)
                        if d == x:
                            mass[z][M_ACT][r] += w
        self.p_correct_f0 = [[[F(0), F(0)] for _ in range(3)] for _ in (0, 1)]
        for z in (0, 1):
            for a in range(3):
                for r in (0, 1):
                    self.p_correct_f0[z][a][r] = mass[z][a][r] / self.p_read[z][r]
        # g outcomes conditional on r: list of (correct, g, prob)
        self.r_outcomes = [[ [] for _ in range(2)] for _ in (0, 1)]
        for z in (0, 1):
            for r in (0, 1):
                for (correct, g), w in gmass[z][r].items():
                    if w != 0:
                        self.r_outcomes[z][r].append((correct, g, w / self.p_read[z][r]))
        # Half-half g0[a][r]
        self.g0 = [[F(0), F(0)] for _ in range(3)]
        # If read marginals agree, the mixture correctness is the average.
        for a in range(3):
            for r in (0, 1):
                # Direct mixture: equal prior on Z, P(r|Z) may differ.
                num = F(0)
                den = F(0)
                for z in (0, 1):
                    den += F(1, 2) * self.p_read[z][r]
                    num += F(1, 2) * self.p_read[z][r] * self.p_correct_f0[z][a][r]
                self.g0[a][r] = num / den
        self.s_def = [abs(self.p_def[y] - F(1, 2)) for y in range(N_Y)]

    def belief_from_counts(self, counts) -> Fraction:
        odds = F(1)
        for c, n in enumerate(counts):
            if n:
                odds *= self.ratio[c] ** n
        return odds / (odds + 1)

    def update_belief(self, b: Fraction, cid: int) -> Fraction:
        ls = self.Lpat[0][cid]
        le = self.Lpat[1][cid]
        return (b * ls) / (b * ls + (1 - b) * le)

    def mix_h1(self, b: Fraction) -> Fraction:
        h = self.h
        return (1 - h) * b + h * (1 - b)

    def imm_PM(self):
        """Immediate F0/any-belief correctness of P and of M given y.

        Valid for every belief when default and resample emissions do not
        depend on the regime. Returns (immP[y], immM[y]).
        """
        if not self.emissions_match:
            raise RuntimeError("P/M immediates require matched non-recheck emissions")
        b = F(1, 2)
        immP = []
        immM = []
        for y in range(N_Y):
            py = self.py[0][y]
            d = self.d_def[y]
            immP.append(self.pyx[0][y][d] / py)
            # resample
            num = F(0)
            den = F(0)
            for ypp in range(N_Y):
                for x in (0, 1):
                    w = self.pyx[0][y][x] * self.Ldef[0][ypp][x]
                    # pyx already includes 1/2; times P(ypp|X) gives joint P(y,ypp,x)
                    # Wait: pyx = (1/2) P(y|X). Times P(ypp|X) = joint. Good.
                    den += w
                    if self.d_resample(b, y, ypp) == x:
                        num += w
            immM.append(num / den)
        return immP, immM

    def expected_correct_R(self, b_pred: Fraction, b_true: Fraction, y: int) -> Fraction:
        """P(d(b_pred)=X | Z~b_true, y, do RECHECK)."""
        num = F(0)
        den = F(0)
        for yp in range(N_Y):
            for x in (0, 1):
                w = F(0)
                for z, bz in ((0, b_true), (1, 1 - b_true)):
                    w += bz * F(1, 2) * self.Lre[z][y][yp][x]
                den += w
                if self.d_recheck(b_pred, y, yp) == x:
                    num += w
        return num / den

    def class_weights(self, b_true: Fraction, y: int):
        """List of 10 weights P(class | b_true, y), summing to 1."""
        raw = [F(0)] * 10
        for yp in range(N_Y):
            for x in (0, 1):
                w = F(0)
                for z, bz in ((0, b_true), (1, 1 - b_true)):
                    w += bz * F(1, 2) * self.Lre[z][y][yp][x]
                raw[self.cls[y][yp][x]] += w
        total = sum(raw)
        return [w / total for w in raw]

    def enumerate_nonrecheck_cells(self):
        """(a) cell tables. P cells are (x, y); M cells are (x, y, ypp)."""
        p_cells = []
        for x in (0, 1):
            for y in range(N_Y):
                p_cells.append(
                    {
                        "X": x,
                        "y": y,
                        "S": self.pyx[0][y][x],
                        "E": self.pyx[1][y][x],
                    }
                )
        m_cells = []
        for x in (0, 1):
            for y in range(N_Y):
                for ypp in range(N_Y):
                    s = F(1, 2) * self.Ldef[0][y][x] * self.Ldef[0][ypp][x]
                    e = F(1, 2) * self.Ldef[1][y][x] * self.Ldef[1][ypp][x]
                    m_cells.append({"X": x, "y": y, "ypp": ypp, "S": s, "E": e})
        return p_cells, m_cells

    def action_atoms(self):
        """For each (z, read, action), atoms (prob | read, correct, class or None, agreement or None).

        Probabilities are conditional on the read class. Class is set for RECHECK only.
        Agreement is the y/y' bit-agreement count, RECHECK only.
        """
        b = F(1, 2)
        raw = [[[[] for _ in range(3)] for _ in (0, 1)] for _ in (0, 1)]
        buckets = [[[{} for _ in range(3)] for _ in (0, 1)] for _ in (0, 1)]
        for z in (0, 1):
            for x in (0, 1):
                for y in range(N_Y):
                    r = read_class(y)
                    # P
                    w = F(1, 2) * self.Ldef[z][y][x]
                    corr = 1 if self.d_def[y] == x else 0
                    buckets[z][r][P_ACT][(corr, None, None)] = buckets[z][r][P_ACT].get((corr, None, None), F(0)) + w
                    for yp in range(N_Y):
                        w = F(1, 2) * self.Lre[z][y][yp][x]
                        corr = 1 if self.d_recheck(b, y, yp) == x else 0
                        cid = self.cls[y][yp][x]
                        agree = N - (y ^ yp).bit_count()
                        key = (corr, cid, agree)
                        buckets[z][r][R_ACT][key] = buckets[z][r][R_ACT].get(key, F(0)) + w
                    for ypp in range(N_Y):
                        w = F(1, 2) * self.Ldef[z][y][x] * self.Ldef[z][ypp][x]
                        corr = 1 if self.d_resample(b, y, ypp) == x else 0
                        buckets[z][r][M_ACT][(corr, None, None)] = buckets[z][r][M_ACT].get((corr, None, None), F(0)) + w
        out = [[[[] for _ in range(3)] for _ in (0, 1)] for _ in (0, 1)]
        for z in (0, 1):
            for r in (0, 1):
                pr = self.p_read[z][r]
                for a in range(3):
                    for (corr, cid, agree), w in buckets[z][r][a].items():
                        out[z][r][a].append((corr, cid, agree, w / pr))
        return out

    def err_table(self):
        """P(read, err) under matched emissions. err is the F0 pre-check mistake."""
        tab = [[F(0), F(0)] for _ in (0, 1)]
        for x in (0, 1):
            for y in range(N_Y):
                w = self.pyx[0][y][x]
                r = read_class(y)
                err = 0 if self.d_def[y] == x else 1
                tab[r][err] += w
        if self.emissions_match:
            for x in (0, 1):
                for y in range(N_Y):
                    w = self.pyx[1][y][x]
                    r = read_class(y)
                    err = 0 if self.d_def[y] == x else 1
                    # identical laws => the E table matches; checked by the caller via emissions_match
                    _ = (w, r, err)
        return tab

    def y_atoms(self):
        """Atoms conditional on (z, y, action).

        Each atom is (correct, class or None, agreement or None, probability).
        Class and agreement are present for RECHECK only. Probabilities sum to 1
        for each (z, y, action). Cached on the instance.
        """
        cached = getattr(self, "_y_atoms", None)
        if cached is not None:
            return cached
        b = F(1, 2)
        out = [[[[] for _ in range(3)] for _ in range(N_Y)] for _ in (0, 1)]
        for z in (0, 1):
            for y in range(N_Y):
                py = self.py[z][y]
                buckets = [{} for _ in range(3)]
                for x in (0, 1):
                    corr = 1 if self.d_def[y] == x else 0
                    buckets[P_ACT][(corr, None, None)] = buckets[P_ACT].get((corr, None, None), F(0)) + self.pyx[z][y][x] / py
                    for yp in range(N_Y):
                        w = F(1, 2) * self.Lre[z][y][yp][x] / py
                        corr = 1 if self.d_recheck(b, y, yp) == x else 0
                        cid = self.cls[y][yp][x]
                        agree = N - (y ^ yp).bit_count()
                        key = (corr, cid, agree)
                        buckets[R_ACT][key] = buckets[R_ACT].get(key, F(0)) + w
                    for ypp in range(N_Y):
                        w = F(1, 2) * self.Ldef[z][y][x] * self.Ldef[z][ypp][x] / py
                        corr = 1 if self.d_resample(b, y, ypp) == x else 0
                        buckets[M_ACT][(corr, None, None)] = buckets[M_ACT].get((corr, None, None), F(0)) + w
                for a in range(3):
                    out[z][y][a] = [(c, cid, g, w) for (c, cid, g), w in buckets[a].items() if w != 0]
        self._y_atoms = out
        return out

    def latent_p_default(self, z: int, y: int, x: int) -> Fraction:
        """Independent cross-check: sum over Bernoulli world and internal noise."""
        w, e = self.w[z], self.e[z]
        total = F(0)
        # each bit: W, N in {0, 1}
        for mask in range(1 << (2 * N)):
            p = F(1)
            y_hat = 0
            for i in range(N):
                W = (mask >> (2 * i)) & 1
                Nv = (mask >> (2 * i + 1)) & 1
                p *= w if W else (1 - w)
                p *= e if Nv else (1 - e)
                b = x ^ W
                yb = b ^ Nv
                y_hat |= yb << i
            if y_hat == y:
                total += p
        return total

    def one_trial_value(self, z: int, action_of_y, dec_of, cost_r: Fraction, cost_s: Fraction) -> Fraction:
        """Expected reward under a deterministic map y -> action, with supplied decision function.

        dec_of(action, y, obs) -> bit. obs is None / yp / ypp.
        """
        costs = (F(0), cost_r, cost_s)
        total = F(0)
        for x in (0, 1):
            for y in range(N_Y):
                a = action_of_y(y)
                if a == P_ACT:
                    w = F(1, 2) * self.Ldef[z][y][x]
                    d = dec_of(a, y, None)
                    total += w * ((1 if d == x else 0) - costs[a])
                elif a == R_ACT:
                    for yp in range(N_Y):
                        w = F(1, 2) * self.Lre[z][y][yp][x]
                        d = dec_of(a, y, yp)
                        total += w * ((1 if d == x else 0) - costs[a])
                else:
                    for ypp in range(N_Y):
                        w = F(1, 2) * self.Ldef[z][y][x] * self.Ldef[z][ypp][x]
                        d = dec_of(a, y, ypp)
                        total += w * ((1 if d == x else 0) - costs[a])
        return total

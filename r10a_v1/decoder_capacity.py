"""Exact, training-free capacity analysis of the live R9 linear read heads.

Tables use table[context][word][own_bit]. All feasibility arithmetic is rational;
the lowest action index wins a tie. No Phase3b module is imported or modified.
"""

from fractions import Fraction
from itertools import combinations, permutations, product


def slope_pair_alphabets(actions):
    """Pair alphabets for strict global slope orders (weak orders add no maps)."""
    if actions < 2:
        raise ValueError("at least two actions required")
    result = []
    for order in permutations(range(actions)):
        rank = {a: i for i, a in enumerate(order)}
        result.append(frozenset(
            (a, b) for a in range(actions) for b in range(actions)
            if a == b or rank[a] < rank[b]
        ))
    return tuple(result)


def weak_slope_orders(actions):
    """All ordered partitions, represented by contiguous ranks starting at zero."""
    if actions < 2:
        raise ValueError("at least two actions required")
    return tuple(ranks for ranks in product(range(actions), repeat=actions)
                 if set(ranks) == set(range(max(ranks) + 1)))


def weak_order_pair_alphabet(ranks):
    return frozenset((a, b) for a in range(len(ranks)) for b in range(len(ranks))
                     if a == b or ranks[a] < ranks[b])


def single_context_count(actions, words=8):
    """Inclusion/exclusion over slope-order alphabets; counts entire codebooks."""
    if words < 1:
        raise ValueError("at least one word required")
    alphabets = slope_pair_alphabets(actions)
    total = 0
    for size in range(1, len(alphabets) + 1):
        for subset in combinations(alphabets, size):
            total += (-1) ** (size + 1) * len(frozenset.intersection(*subset)) ** words
    return total


def single_context_maps(actions, words=8):
    """Enumerate without random weights, deduplicating overlapping slope orders."""
    if words < 1:
        raise ValueError("at least one word required")
    alphabets = slope_pair_alphabets(actions)
    for order_index, alphabet in enumerate(alphabets):
        for pairs in product(sorted(alphabet), repeat=words):
            if not any(all(pair in earlier for pair in pairs)
                       for earlier in alphabets[:order_index]):
                yield pairs


def codebook_slope_consistent(pairs, actions):
    """Necessary and sufficient at one context, only necessary across contexts."""
    pairs = tuple(tuple(pair) for pair in pairs)
    if any(len(pair) != 2 or any(a not in range(actions) for a in pair)
           for pair in pairs):
        raise ValueError("invalid action pair")
    return any(all(pair in alphabet for pair in pairs)
               for alphabet in slope_pair_alphabets(actions))


def _rational_feasible(a, b, variables):
    """Solve A x <= b, x >= 0 by exact phase-I simplex (Bland pivot rules)."""
    m, n = len(b), variables
    if not m:
        return tuple(Fraction(0) for _ in range(n))
    d = [[Fraction(0) for _ in range(n + 2)] for _ in range(m + 2)]
    basic = [n + i for i in range(m)]
    nonbasic = list(range(n)) + [-1]
    for i in range(m):
        d[i][:n] = map(Fraction, a[i])
        d[i][n], d[i][n + 1] = Fraction(-1), Fraction(b[i])
    d[m + 1][n] = Fraction(1)

    def pivot(r, s):
        inverse = 1 / d[r][s]
        for i in range(m + 2):
            if i == r:
                continue
            for j in range(n + 2):
                if j != s:
                    d[i][j] -= d[r][j] * d[i][s] * inverse
        for j in range(n + 2):
            if j != s:
                d[r][j] *= inverse
        for i in range(m + 2):
            if i != r:
                d[i][s] *= -inverse
        d[r][s] = inverse
        basic[r], nonbasic[s] = nonbasic[s], basic[r]

    def phase_one():
        while True:
            entering = [j for j in range(n + 1) if d[m + 1][j] < 0]
            if not entering:
                return
            s = min(entering, key=lambda j: nonbasic[j])
            leaving = [i for i in range(m) if d[i][s] > 0]
            if not leaving:
                raise ArithmeticError("phase-I objective cannot be unbounded")
            r = min(leaving, key=lambda i: (d[i][n + 1] / d[i][s], basic[i]))
            pivot(r, s)

    r = min(range(m), key=lambda i: d[i][n + 1])
    if d[r][n + 1] < 0:
        pivot(r, n)
        phase_one()
        if d[m + 1][n + 1] != 0:
            return None
    solution = [Fraction(0) for _ in range(n)]
    for i in range(m):
        if 0 <= basic[i] < n:
            solution[basic[i]] = d[i][n + 1]
    if any(x < 0 for x in solution) or any(
            sum(v * x for v, x in zip(row, solution)) > rhs
            for row, rhs in zip(a, b)):
        raise ArithmeticError("invalid exact simplex witness")
    return tuple(solution)


def _table_shape(table, actions):
    if actions < 2 or not table or not table[0]:
        raise ValueError("nonempty table and at least two actions required")
    words = len(table[0])
    if any(len(context) != words for context in table):
        raise ValueError("contexts must have equal word counts")
    if any(len(pair) != 2 or any(a not in range(actions) for a in pair)
           for context in table for pair in context):
        raise ValueError("invalid action pair")
    return len(table), words


def shared_context_witness(table, actions):
    """Exact R9 feasibility; returns gauge-fixed rational weights or None.

    Action zero has zero logits. Context zero offsets are zero. Remaining logits
    are b[action,word] + d[action,context] + s[action]*bit.
    """
    contexts, words = _table_shape(table, actions)
    block = words + contexts
    variables = (actions - 1) * block

    def feature(action, context, word, bit):
        row = [0] * variables
        if action:
            offset = (action - 1) * block
            row[offset + word] = 1
            if context:
                row[offset + words + context - 1] = 1
            row[offset + block - 1] = bit
        return row

    a, rhs = [], []
    for c, context in enumerate(table):
        for word, pair in enumerate(context):
            for bit, winner in enumerate(pair):
                win = feature(winner, c, word, bit)
                for competitor in range(actions):
                    if competitor == winner:
                        continue
                    rival = feature(competitor, c, word, bit)
                    # A higher-index winner must beat lower indices strictly.
                    row = [x - y for x, y in zip(rival, win)]
                    a.append(row + [-x for x in row])
                    rhs.append(-int(competitor < winner))
    split = _rational_feasible(a, rhs, 2 * variables)
    if split is None:
        return None
    weights = tuple(split[i] - split[i + variables] for i in range(variables))
    b = [[Fraction(0)] * words for _ in range(actions)]
    d = [[Fraction(0)] * contexts for _ in range(actions)]
    s = [Fraction(0)] * actions
    for action in range(1, actions):
        offset = (action - 1) * block
        b[action] = list(weights[offset:offset + words])
        d[action][1:] = weights[offset + words:offset + block - 1]
        s[action] = weights[offset + block - 1]
    witness = {"message": b, "context": d, "slope": s}
    if decode_witness(witness) != tuple(tuple(tuple(pair) for pair in c) for c in table):
        raise ArithmeticError("rational witness does not reproduce table")
    return witness


def decode_witness(witness):
    b, d, s = witness["message"], witness["context"], witness["slope"]
    return tuple(tuple(tuple(max(range(len(s)), key=lambda a:
                                 b[a][m] + d[a][c] + s[a] * bit)
                             for bit in (0, 1))
                       for m in range(len(b[0])))
                 for c in range(len(d[0])))


def shared_context_feasible(table, actions):
    return shared_context_witness(table, actions) is not None


def shared_context_count(actions, words=8, contexts=4):
    """Provably exact finite sum, practical only for small dimensions.

    Enumerates each globally slope-consistent table once, then checks the exact
    shared additive inequalities. Defaults describe full R9, NOT a cheap count.
    """
    if contexts < 1:
        raise ValueError("at least one context required")
    total = 0
    for pairs in single_context_maps(actions, words * contexts):
        table = tuple(pairs[c * words:(c + 1) * words] for c in range(contexts))
        total += shared_context_feasible(table, actions)
    return total


def d1_features(word, bit, words=8, context=None, contexts=4,
                full_context=False):
    """D1: word, scalar bit, word*bit; full mode additionally crosses context."""
    if word not in range(words) or bit not in (0, 1):
        raise ValueError("invalid word/bit")
    if full_context and context is None:
        raise ValueError("full-context D1 requires a context")
    if context is not None and context not in range(contexts):
        raise ValueError("invalid context")
    x = tuple(int(word == m) for m in range(words))
    features = x + (bit,) + tuple(bit * value for value in x)
    if context is not None:
        features += tuple(int(context == c) for c in range(contexts))
    if full_context:
        joint = tuple(int(context == c and word == m)
                      for c in range(contexts) for m in range(words))
        features += joint + tuple(bit * value for value in joint)
    return features


def d2_features(word, bit, words=8, context=None, contexts=4,
                full_context=False):
    """Fixed ReLU lookup representation: 2*M or 2*C*M one-hot hidden units."""
    if word not in range(words) or bit not in (0, 1):
        raise ValueError("invalid word/bit")
    if full_context and context is None:
        raise ValueError("full-context D2 requires a context")
    if context is not None and context not in range(contexts):
        raise ValueError("invalid context")
    if full_context:
        return tuple(max(0, int(word == m) + int(context == c) +
                         (bit if l else -bit) - (2 if l else 1))
                     for c in range(contexts) for m in range(words) for l in (0, 1))
    hidden = tuple(max(0, int(word == m) + (bit if l else -bit) - l)
                   for m in range(words) for l in (0, 1))
    if context is not None:
        hidden += tuple(int(context == c) for c in range(contexts))
    return hidden


if __name__ == "__main__":
    for actions in (2, 3):
        print(f"single-context, 8 words, {actions} actions: "
              f"{single_context_count(actions)}")
    print("Full four-context counts: exact algorithm provided; not evaluated.")

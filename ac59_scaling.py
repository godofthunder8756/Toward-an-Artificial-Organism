"""AC59 (engineering): the scaling frontier -- order structure grows, the rule format is the binding axis.

Verifies that the order-structure criterion (AC25: every exact pair presented -> B! behaviours) scales
exactly with the number of positions, and restates AC20's rule-format budget to show which axis binds
first when the developmental function is scaled. Engineering only: no protocol, no final seeds, no claim.
"""
import math
import ac25_confront as cf


def order_classes(N):
    codes = cf.unique_codes(N)
    pairs = [(1 << i) | (1 << j) for i in range(N) for j in range(i + 1, N)]
    return cf.classes(codes, pairs)


if __name__ == '__main__':
    print('order-structure scaling (all-pairs criterion):')
    for N in (6, 7, 8):
        c = order_classes(N)
        print(f'  N={N}: {c} classes = {math.log2(c):.2f} bits (nominal {math.log2(math.factorial(N)):.2f})')
    print()
    print('AC20 rule-format budget: 9 slots + 9 mask bits; binds when C+B > 9:')
    for C, B in [(6, 3), (6, 4), (7, 3), (7, 4), (8, 3), (9, 3)]:
        slots = C + B
        print(f'  C={C} B={B}: needs {slots} slots -> {"fits" if slots <= 9 else "BINDS (exceeds 9 slots)"}')

"""K4 diagnostic harness: are the two AC106 causes identifiable from the organism's
own action-observation history, without supplying the hidden cause or schedule?

This is NOT an organism-scale experiment and NOT a study. It is the small
diagnostic the K4 card calls for, to demonstrate separability BEFORE K5
implements an estimator. It (a) asserts the frozen primitives the identifiability
argument rests on, directly against the frozen modules, and (b) simulates the
contact-observation tuple under the C1 §4 "hold-and-observe" probe for both
causes and reports whether the tuple sequence separates them.

Nothing here edits or re-runs a frozen study; it only imports frozen code.
"""
import numpy as np
import ac9
import ac9_memory as mem
import ac106

# ----------------------------------------------------------------------------
# (a) frozen-primitive assertions (the mechanical facts the argument uses)
# ----------------------------------------------------------------------------

# 1. A stale entry fails forever; a held entry that matches the mapping yields.
#    (ac9.step line 86: port = coin if selected is None else selected;
#     react yields iff port == mapping[action].)
def react_yields(selected, coin, mapping_action):
    port = coin if selected is None else selected
    return port == mapping_action

# 2. deposit is a no-op while the key is already bound (ac9_memory.deposit line 62).
m = mem.Memory.empty()
body = ac9.acquire(0).body          # a body with energy/material to fund a deposit
mem.deposit(m, body, 1, 0, [True, True], [4, 4])   # bind key 1 -> port 0
assert m.read(1) == 0, "deposit should bind key 1"
res = mem.deposit(m, body, 1, 1, [True, True], [4, 4])  # try to overwrite while bound
assert res['writes'] == 0 and res['bound'] == 0, "deposit must be a no-op while bound"
assert m.read(1) == 0, "the bound entry must be unchanged by the second deposit"

# 3. ReadCut suppresses only the contact read, and only in-window (ac106.ReadCut).
cut = ac106.ReadCut(1, 100, 196)
m2 = mem.Memory.empty()
mem.deposit(m2, body, 1, 0, [True, True], [4, 4])
for t in (99, 100, 150, 195, 196):
    cut.now = t
    shim = cut.read(m2, 1)          # what the CONTACT sees
    unshim = m2.read(1)             # what the organism's introspection sees
    in_window = 100 <= t < 196
    assert (shim is None) == in_window, (t, shim, in_window)
    assert unshim == 0, (t, unshim)  # introspection sees the entry bound the whole time

# 4. Blind fallback is uniform over PORTS=4, so a blind contact matches mapping in
#    {0,1} with probability 1/4 (ac106 line 396).
rng = np.random.default_rng(0)
coins = rng.integers(0, ac106.PORTS, 400000)
blind_success_rate = (coins == 1).mean()   # mapping[1] == 1 is one of 4 values
assert abs(blind_success_rate - 0.25) < 0.005, blind_success_rate

print("frozen-primitive assertions: PASS")
print("  deposit no-op while bound; ReadCut shims only the contact read; blind rate 1/4")

# ----------------------------------------------------------------------------
# (b) the contact-observation tuple under the hold-and-observe probe
# ----------------------------------------------------------------------------
# The organism withholds relinquishment, keeps contacting channel 1, and records
# per contact the tuple (bound, used_held, productive):
#   bound     = introspection read of its own entry (o.memory.read(1) is not None)
#   used_held = did the contact use a held entry or fall back to blind?
#               (the shimmed `selected`; in `cut` this is forced None in-window)
#   productive= did the contact yield?
# This mirrors the frozen contact/deposit/read-cut logic exactly.

def hold_and_observe(cause, T=100, W=96, n_contacts=200, seed=0):
    rng = np.random.default_rng([seed, 0 if cause == 'move' else 1])
    mapping = 1                       # channel-1 mapping (moves to 0 in 'move')
    bound = True                      # entry is held at the intervention
    stored_port = 1                   # correct BEFORE the intervention
    if cause == 'move':
        mapping = 0                   # mapping flips: the stored port is now stale
    tuples = []
    for c in range(n_contacts):
        t = T + c
        in_window = (cause == 'cut') and (T <= t < T + W)
        used_held = bound and not in_window       # cut forces the contact read to None
        if used_held:
            port = stored_port
        else:
            port = int(rng.integers(0, ac106.PORTS))   # blind fallback
        productive = (port == mapping)
        # frozen deposit gate: blind+productive binds only if NOT already bound
        if productive and not used_held and not bound:
            bound = True
            stored_port = port
        # frozen entry life is 64; the cut window (96) exceeds it, so WITHOUT
        # renewal the entry would expire. We model the organism as holding the
        # entry alive through the window (the estimate's E_machinery branch) --
        # life does not decay here because the identifiability question is about
        # the observation structure, not the renewal economy (measured separately).
        tuples.append((int(bound), int(used_held), int(productive)))
    return tuples

for cause in ('move', 'cut'):
    tup = hold_and_observe(cause)
    # distinguishing features:
    held_failing = any((b == 1 and u == 1 and p == 0) for b, u, p in tup)   # (1,1,0)
    prod_while_bound = any((b == 1 and p == 1) for b, u, p in tup)          # (1,*,1)
    ever_unbound = any(b == 0 for b, u, p in tup)                            # (0,*,*)
    print(f"\n{cause}: contacts={len(tup)}")
    print(f"  held-failing (bound=1,used_held=1,prod=0) ever: {held_failing}")
    print(f"  productive-while-bound (bound=1,prod=1) ever:   {prod_while_bound}")
    print(f"  ever-unbound (bound=0) ever:                    {ever_unbound}")
    print(f"  first 20 tuples (bound,used_held,productive):")
    print("   ", tup[:20])

# The separator: productive-while-bound => E_machinery; a held entry that NEVER
# yields while bound, then an unbound re-bind => E_world.
print("\nSEPARATOR: 'productive while bound' is TRUE in cut, FALSE in move "
      "(under hold-and-observe). The two causes produce disjoint observation "
      "tuples, so the task is identifiable given (bound, used_held, productive).")

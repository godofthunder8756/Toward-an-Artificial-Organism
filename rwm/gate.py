"""Pre-scale verification gate (RWM-PSG v1): structure, integration, causal
density, instrument validity and objective admission. Exact enumeration only.

Every verdict here is ENGINEERING class (criteria fixed after exploratory runs;
see RWM_DESIGN_v1.md section 9). A GO authorizes nothing by itself.
"""
from __future__ import annotations

from itertools import product
from typing import Dict, List, Optional

from .integration import causal_density, major_complex, phi_s, uniform_weight
from .primitives import Network, reachable, strongly_connected_components
from .topology import (FIRST_ORDER, all_designs, control_chain, control_copy_loop,
                       control_two_islands, fooler_noisy_copy_ring, fooler_xor_ring, rwm8, unroll)
from .world import agent_state_weights, closed_loop_summary, objective_certificate

MASS_THRESHOLD = 0.5
UNROLL_HORIZON = 3


def structural_checks(net: Network) -> Dict[str, object]:
    eff = net.effective_edges()
    dec = net.declared_edges()
    mods = net.modules
    scc = strongly_connected_components(net.nodes, eff)
    ext_nodes = [n for n in net.nodes if mods.get(n) == "EXT"]
    int_nodes = [n for n in net.nodes if mods.get(n) == "INT"]
    ws = [n for n in net.nodes if mods.get(n) == "WS"]
    mon = [n for n in net.nodes if mods.get(n) == "MON"]
    direct = [(a, b) for a, b in eff if {mods.get(a), mods.get(b)} == set(FIRST_ORDER)]
    leak = bool(reachable(ext_nodes, eff, forbidden=ws) & set(int_nodes)) or \
        bool(reachable(int_nodes, eff, forbidden=ws) & set(ext_nodes))
    out = {
        "T1_single_scc": len(scc) == 1,
        "scc": scc,
        "T2_bottleneck": bool(ws) and not direct and not leak,
        "direct_first_order_edges": direct,
        "T3_broadcast": bool(ws) and all(
            any((w, n) in eff for w in ws for n in net.nodes if mods.get(n) == m) for m in FIRST_ORDER),
        "T4_monitor_higher_order": bool(mon) and
            all(not any(src in net.external for src in net.inputs[c]) for c in mon) and
            any((c, n) in eff for c in mon for n in net.nodes if mods.get(n) in FIRST_ORDER) and
            any((n, c) in eff for c in mon for n in net.nodes if mods.get(n) in FIRST_ORDER),
        "T5_no_vestigial_declared_edges": set(dec) == set(eff),
        "n_effective_edges": len(eff),
    }
    return out


def integration_profile(net: Network, with_complex: bool = True) -> Dict[str, object]:
    loop = closed_loop_summary(net)
    weights = agent_state_weights(net, loop.pop("_pi"))
    rows = []
    mass_phi = 0.0
    mass_core = 0.0
    mass_mon_isolated = 0.0
    for (s, e), p in sorted(weights.items(), key=lambda kv: -kv[1]):
        ext = dict(zip(net.external, e))
        ph = phi_s(net, s, ext)
        row = {"state": "".join(map(str, net.state_bits(s))), "ext": "".join(map(str, e)),
               "mass": p, "phi_s": ph["phi"], "reason": ph["reason"], "mip": ph.get("mip")}
        if ph["phi"] > 0:
            mass_phi += p
        if with_complex:
            mc = major_complex(net, s, ext)
            row["major_complex_phi"] = mc["phi"]
            row["major_complexes"] = mc["complexes"]
            core = any(_core_ok(net, c) for c in mc["complexes"])
            if core:
                mass_core += p
            if mc["complexes"] and all(set(net.modules.get(n) for n in c) == {"MON"} for c in mc["complexes"]):
                mass_mon_isolated += p
        rows.append(row)
    cd_int = causal_density(net, uniform_weight(net))
    cd_obs = causal_density(net, weights)
    return {
        "closed_loop": loop,
        "n_stationary_agent_input_states": len(weights),
        "mass_phi_positive": mass_phi,
        "T6_integration": mass_phi >= MASS_THRESHOLD,
        "mass_core_complex": mass_core if with_complex else None,
        "T7_core_complex": (mass_core >= MASS_THRESHOLD) if with_complex else None,
        "mass_monitor_only_complex": mass_mon_isolated if with_complex else None,
        "causal_density_interventional": {k: cd_int[k] for k in ("cd_binary", "cd_weighted")},
        "causal_density_closed_loop": {k: cd_obs[k] for k in ("cd_binary", "cd_weighted")},
        "edge_cmi_interventional": cd_int["cmi"],
        "edge_cmi_closed_loop": cd_obs["cmi"],
        "edges_inactive_in_closed_loop": sorted(
            f"{a}->{b}" for a, b in net.effective_edges() if a != b and cd_obs["cmi"][f"{a}->{b}"] <= 1e-12),
        "edges_without_interventional_cmi": sorted(
            f"{a}->{b}" for a, b in net.effective_edges() if cd_int["cmi"][f"{a}->{b}"] <= 1e-12),
        "states": rows,
    }


def _core_ok(net: Network, members: List[str]) -> bool:
    mods = {net.modules.get(n) for n in members}
    return {"EXT", "INT", "WS", "MON"} <= mods


def instrument_validation() -> Dict[str, object]:
    out: Dict[str, object] = {}
    cl = control_copy_loop()
    out["copy_loop_phi"] = phi_s(cl, 0, {})["phi"]
    out["copy_loop_cd"] = causal_density(cl, uniform_weight(cl))["cd_weighted"]
    out["dag_chain_max_phi"] = max(phi_s(control_chain(), s, {})["phi"] for s in range(8))
    out["two_islands_max_phi"] = max(phi_s(control_two_islands(), s, {})["phi"] for s in range(16))
    xr = fooler_xor_ring(8)
    out["fooler_xor_ring_phi_state0"] = phi_s(xr, 0, {})["phi"]
    out["fooler_xor_ring_cd"] = causal_density(xr, uniform_weight(xr))["cd_weighted"]
    nr = fooler_noisy_copy_ring(8)
    out["fooler_noisy_ring_phi_state0"] = phi_s(nr, 0, {})["phi"]
    # unfolding control
    net = rwm8()
    un = unroll(net, UNROLL_HORIZON)
    equivalent = True
    for s0 in range(1 << net.n):
        for seq in product(product((0, 1), repeat=len(net.external)), repeat=UNROLL_HORIZON):
            ext = {f"{nd}@0": b for nd, b in zip(net.nodes, net.state_bits(s0))}
            s = s0
            for t, inp in enumerate(seq):
                for name, b in zip(net.external, inp):
                    ext[f"{name}@{t}"] = b
            vals = dict(ext)
            for t in range(1, UNROLL_HORIZON + 1):
                for nd in net.nodes:
                    vals[f"{nd}@{t}"] = int(un.node_p1(f"{nd}@{t}", vals))
            for t, inp in enumerate(seq):
                s = net.step_det(s, dict(zip(net.external, inp)))
            if any(vals[f"{nd}@{UNROLL_HORIZON}"] != b for nd, b in zip(net.nodes, net.state_bits(s))):
                equivalent = False
    out["unrolled_nodes"] = un.n
    out["unrolled_io_equivalent"] = equivalent
    out["unrolled_single_scc"] = len(strongly_connected_components(un.nodes, un.effective_edges())) == 1
    out["unrolled_phi_zero_structurally"] = _has_free_directed_cut(un)
    out["T8_instruments"] = (
        abs(out["copy_loop_phi"] - 1.0) < 1e-12 and abs(out["copy_loop_cd"] - 1.0) < 1e-12 and
        out["dag_chain_max_phi"] == 0.0 and out["two_islands_max_phi"] == 0.0 and
        equivalent and out["unrolled_phi_zero_structurally"])
    return out


def _has_free_directed_cut(net: Network) -> bool:
    """True iff some directed bipartition has no effective edge A -> B. For an
    acyclic graph a sink node gives one, so Phi_s = 0 in EVERY state (exact)."""
    eff = net.effective_edges()
    outs = {n: {b for a, b in eff if a == n and b != n} for n in net.nodes}
    ins = {n: {a for a, b in eff if b == n and a != n} for n in net.nodes}
    return any(not outs[n] or not ins[n] for n in net.nodes) or \
        len(strongly_connected_components(net.nodes, eff)) > 1


def run_gate(with_complex: bool = True) -> Dict[str, object]:
    designs = all_designs()
    result: Dict[str, object] = {"protocol": "RWM-PSG v1", "class": "ENGINEERING",
                                 "mass_threshold": MASS_THRESHOLD}
    result["instruments"] = instrument_validation()
    cert = objective_certificate()
    cert["T9_objective_admission"] = (
        cert["extero_only"]["all_optimal_never_forage_from_start"] and
        not cert["extero_plus_intero"]["all_optimal_never_forage_from_start"] and
        cert["extero_plus_intero"]["optimal_lifetime_float_min"] > float(eval(cert["dark_room_lifetime"])))
    result["objective"] = cert
    result["designs"] = {}
    for name, net in designs.items():
        entry = {"description": net.describe(), "structure": structural_checks(net),
                 "integration": integration_profile(net, with_complex)}
        result["designs"][name] = entry
    main = result["designs"]["RWM-8"]
    tests = {
        "T1_single_scc": main["structure"]["T1_single_scc"],
        "T2_bottleneck": main["structure"]["T2_bottleneck"],
        "T3_broadcast": main["structure"]["T3_broadcast"],
        "T4_monitor_higher_order": main["structure"]["T4_monitor_higher_order"],
        "T5_no_vestigial_declared_edges": main["structure"]["T5_no_vestigial_declared_edges"] and
            not main["integration"]["edges_without_interventional_cmi"],
        "T6_integration": main["integration"]["T6_integration"],
        "T7_core_complex": main["integration"]["T7_core_complex"],
        "T8_instruments": result["instruments"]["T8_instruments"],
        "T9_objective_admission": cert["T9_objective_admission"],
    }
    result["tests"] = tests
    result["verdict"] = "GO_TO_PROTOCOL_DRAFTING" if all(tests.values()) else "NO_GO"
    result["failed"] = [k for k, v in tests.items() if not v]
    return result

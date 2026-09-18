import subprocess, json, sys

BOARD = "artificial-organism"
REPO = "/home/elminster/projects/Toward-an-Artificial-Organism"

def run(args):
    return subprocess.run(["hermes", "kanban", "--board", BOARD] + args,
                          capture_output=True, text=True)

def create(title, body, priority, key, triage=False):
    args = ["create", title, "--body", body, "--priority", str(priority),
            "--workspace", f"dir:{REPO}", "--idempotency-key", key,
            "--assignee", "default", "--skill", "artificial-organism-research",
            "--json"]
    if triage:
        args.append("--triage")
    r = run(args)
    if r.returncode != 0:
        print(f"FAILED create {key}: {r.stderr}"); sys.exit(1)
    data = json.loads(r.stdout)
    return data["id"]

TASKS = [
    dict(key="ao-combined-compose", priority=70,
         title="AC83: make reconstruction + description maintenance + route-move adaptation compose (resolve the material-low hijack)",
         body="""AC82 engineering (milestone 3) answered the decisive question NO for the combined architecture: reconstruction and description maintenance are unconditional (16/16), but route re-acquisition is NOT (10/16 hold both routes under a simultaneous corruption + permanent move). Cause, pinned by AC82's instrumented trace (seed 0): the reconstruction's material cost and the move's income cut together set obs bit 1 (material <= 64); the frozen program's rule 1 (material contact) precedes the bank-1 renewal rule, so the material contact preempts renewal; route 0 ages unrenewed, expires at t=8205, and is never re-bound (its key was never moved). This is AC74's attention-hijack pattern, here on route 0.

This card: make the combined architecture compose. Named options (AC82): (a) separate the two interventions in time -- a declared design choice, not one discovered after seeing the result; (b) cheaper reconstruction; (c) higher renewal priority. (b)/(c) require frozen-law changes (out of scope unless a frozen-law-respecting primitive already exists); (a) is the viable declared option. Engineer one or more designs; if one passes (unconditional survival + recovery + both routes held on fresh seeds), freeze it (hashed protocol, disjoint finals). If NO design composes under the frozen laws, record that honestly as a structural non-composition -- do not re-freeze the AC82 configuration and do not soften the endpoint.

Discipline: new runner ac83.py (never edit ac75/ac76/ac79/ac80/ac81/ac82); engineering first; report UNCONDITIONAL survival + recovery on the planned denominator (do NOT gate on survivors -- the whole point is to close AC79/AC80's survivor-conditioning); read AC82_ENGINEERING_v1.md, AC80_RESULTS_v1.md, AC75_RESULTS_v1.md, AC74_ENGINEERING_v1.md, and the skill 'artificial-organism-research'. THIS CARD ONLY -- do not attempt milestone 2 or the bank-convention work (separate cards)."""),

    dict(key="ao-turnover-unconditional", priority=60,
         title="AC84: strengthen milestone 2 — turnover across the cohort, not survivors",
         body="""AC81 (milestone 2) froze replacement-across-generations but survivor-gated: internalized survives 2/8 (collapse-dominated; pristine 4/8; unfavourable AC39 direction), so the turnover claim (W ~95x, C ~64x, B ~84x their slot complements) is demonstrated in only 2 survivors -- the exact survivor-conditioning weakness flagged in AC79's G1 and AC80's G1.

This card: a stronger milestone-2 design that reports turnover UNCONDITIONALLY, not gated on horizon-completers. The components (W/C/B) turn over continuously even with no intervention (AC81's survivors show W_birth 1511 vs 16 slots), so the turnover claim may not need the t=8192 kill intervention at all -- demonstrate construction/use/replacement per individual across the planned cohort, on a horizon and seed family that avoids the AC68 W/C collapse regime. Do NOT gate turnover on survivors; if the AC68 collapse kills individuals before turnover is observable, that is a finding about the body's fragility, not a licence to gate.

Discipline: new runner ac84.py; engineering first, then hashed protocol + disjoint finals; read AC81_RESULTS_v1.md, AC81_ENGINEERING_v1.md, AC80_RESULTS_v1.md, and the skill 'artificial-organism-research'. THIS CARD ONLY.""",),

    dict(key="ao-bank-convention", priority=40,
         title="AC85: internalize the bank-rule convention (last supplied machinery on the reconstruction path)",
         body="""AC80 internalized the 5 rule words + permutation, but rebuild() still DERIVES the 4 bank rules from the permutation by the convention bank b -> (enabled=1, mask=4<<b, action=2+b). That convention is supplied machinery, not stored state (AC80's own boundary note). To fully internalize the recipe -- so that no function on the reconstruction path knows the correct policy -- store the bank rules' masks/actions as vulnerable maintained state too, and let rebuild() read them instead of deriving them.

Lower priority (the convention is arguably format, not policy), but it is the honest residual if the goal is "no function knows the correct policy". Discipline: new runner ac85.py; read AC80_RESULTS_v1.md (boundary note) and AC80_PROTOCOL_v1.md. THIS CARD ONLY."""),

    dict(key="ao-consciousness-track", priority=20,
         title="Consciousness separate track (placeholder — needs a concrete mechanism)",
         body="""Placeholder only -- do not start until a concrete, falsifiable mechanism is specified. The goal-§7 archive was a scheduling decision, not evidence that consciousness requires priority learning (AC79_ERRATA_v1.md §5). A theory-specific investigation (e.g. the AC67/71 self-monitoring loop as a candidate indicator, Butlin et al. 2023 arxiv 2308.08708) can proceed on a separate track IF there is a concrete mechanism worth testing. Autopoiesis is not an established prerequisite. Do not invent consciousness work or re-gate it on content self-production.""",
         triage=True),
]

ids = {}
for t in TASKS:
    tid = create(t["title"], t["body"], t["priority"], t["key"],
                 triage=t.get("triage", False))
    ids[t["key"]] = tid
    print(f"created {tid}  P{t['priority']}  {'[triage]' if t.get('triage') else ''}  {t['title'][:65]}")

# serialize the repo-modifying studies: AC83 -> AC84 -> AC85 (one worker at a time,
# and each extends the frozen runner its predecessor left behind)
LINKS = [
    ("ao-combined-compose", "ao-turnover-unconditional"),
    ("ao-turnover-unconditional", "ao-bank-convention"),
]
for p, c in LINKS:
    r = run(["link", ids[p], ids[c]])
    if r.returncode != 0:
        print(f"FAILED link {p}->{c}: {r.stderr}"); sys.exit(1)
    print(f"linked {ids[p]} -> {ids[c]}  ({p} -> {c})")

print("DONE")

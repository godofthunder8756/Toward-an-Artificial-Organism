import subprocess, json, sys

BOARD = "artificial-organism"
REPO = "/home/elminster/projects/Toward-an-Artificial-Organism"

def run(args):
    return subprocess.run(["hermes", "kanban", "--board", BOARD] + args,
                          capture_output=True, text=True)

body = """AC91 established only that W production is necessary for viability and sustained W-dependent maintenance capacity — NOT that loss/recovery of coordination is isolated. The blocked organisms died at 248-254, before succession (t=2400) or the reconstruction challenge (t=8192), so their fw=8 is post-mortem, not an observed failure while alive. This card observes the target function failing and recovering WHILE ALIVE.

DESIGN (before redesigning anything): a functional interruption-and-rescue on a MATURE organism, interrupting W availability while reconstruction or succession is UNDERWAY, measuring a SHORT interval before energy/converter failure obscures the effect.

Matched conditions (same initial content and resources):
1. INTACT machinery — normal copying, reconstruction, phase progression (baseline).
2. W UNAVAILABLE — measure which operations actually stop and which continue.
3. MACHINERY-ONLY RESCUE — restore W availability WITHOUT changing description, program, pointer, or coordinator state; test whether the interrupted operation resumes.

A direct experimental restoration of W is acceptable as a causal rescue control, clearly labeled EXTERNAL. Separate runs establish endogenous W production; no single intervention must prove both at once.

Record, over the matched window: successful writes, coordinator transitions, pointer changes, reconstruction completion. If copying stops but the coordinator keeps changing phase, that identifies exactly which part remains externally enabled; if the whole functional process stops and resumes with W, the stronger claim gains direct support.

Distinguish W-DEPENDENT execution (recipe copying, clearing, reconstruction, pointer writes, maintenance writes) from W-INDEPENDENT coordination (supplied sequencing logic + write_ctrl, energy+material alone). Do NOT claim W gates "every paid write on the coordination path."

DISCIPLINE: new runner ac92.py (never edit frozen ac80-ac91); engineering first, then hashed protocol + disjoint finals; read AC91_RESULTS_v1.md (corrected wording), AC88_RESULTS_v1.md (distinct-resource model), CLOSURE_BOUNDARY_v2.md; skill 'artificial-organism-research'. THIS CARD ONLY."""

r = run(["create", "AC92: functional interruption-and-rescue — observe reconstruction/succession fail and recover while the organism is alive",
         "--body", body, "--priority", "70",
         "--workspace", f"dir:{REPO}", "--idempotency-key", "ao-interrupt-rescue",
         "--assignee", "default", "--skill", "artificial-organism-research", "--json"])
if r.returncode != 0:
    print(f"FAILED create AC92: {r.stderr}"); sys.exit(1)
tid = json.loads(r.stdout)["id"]
print(f"created {tid}  P70  AC92 (functional interruption-and-rescue)")
print("DONE")

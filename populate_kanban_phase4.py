import subprocess, json, sys

BOARD = "artificial-organism"
REPO = "/home/elminster/projects/Toward-an-Artificial-Organism"
AC83 = "t_e5014a3a"   # running: combined-architecture compose
AC84 = "t_c32d03e7"   # todo: turnover across cohort (now secondary)

def run(args):
    return subprocess.run(["hermes", "kanban", "--board", BOARD] + args,
                          capture_output=True, text=True)

# 1. Steer the running AC83 worker toward experiment 2 (bounded-retry / scheduling),
#    correcting the card's "separate interventions" emphasis.
steer = (
    "STEERING (user review of commit 6a1f4fb): do NOT settle for separating the two "
    "interventions in time -- separation is diagnostic only, it does not solve the "
    "simultaneous challenge. Pursue a minimal bounded-retry OR scheduling mechanism "
    "against the current priority controller, RETAINING the simultaneous "
    "corruption-and-move condition. Store any organism-specific scheduling state in the "
    "maintained substrate. Measure route retention, survival, repair costs, and failure "
    "timing on fresh seeds. Report UNCONDITIONALLY (not survivor-gated). Frozen "
    "experiments prohibit retroactively changing the OLD experiment, not changing the "
    "next architecture."
)
r = run(["comment", AC83, steer])
if r.returncode != 0:
    print(f"FAILED comment: {r.stderr}"); sys.exit(1)
print(f"commented on {AC83} (steer)")

# 2. Create experiment 1: replacement of the information-bearing components.
body = """Replacement of the information-bearing components (recipe succession). AC81 (milestone 2) showed the organism repeatedly replaces W/C/B components, but NEVER the recipe-bearing storage itself (the 78-bit description in traces[1,:78]). This card closes that gap: have the organism construct a functional successor copy of its recipe, begin using that copy, and subsequently replace it again. Track provenance and successful execution across those replacements; remove an older copy only after the successor is functional. This tests organizational continuity without demanding recovery after destroying every usable copy (the catastrophic analog, out of scope).

Framing (per AC79_ERRATA_v1.md and the review of 6a1f4fb): the reconstruction recipe is now internalized (AC80), so the next substantive milestone is continuity of those instructions and their supporting machinery through replacement. Automatic repair is fine; what is required is that the repair activity depend on identifiable, replaceable internal machinery whose production the organization supports -- not merely a fixed host-side trigger (AC80's _reg_generic fires before action selection with a fixed DESC_TRIGGER=2; calling it "format-level" does not settle the format-vs-policy distinction). This card makes the recipe-bearing storage itself replaceable.

Discipline: new runner ac86.py (never edit ac80/ac81/ac82/ac83); engineering first, then hashed protocol + disjoint finals; read AC80_RESULTS_v1.md, AC81_RESULTS_v1.md, AC81_ENGINEERING_v1.md, ac80.py (reg_description / _reg_generic), AC79_ERRATA_v1.md, and the skill 'artificial-organism-research'. THIS CARD ONLY."""
r = run(["create", "AC86: replacement of the information-bearing components (recipe succession)",
         "--body", body, "--priority", "65",
         "--workspace", f"dir:{REPO}", "--idempotency-key", "ao-recipe-succession",
         "--assignee", "default", "--skill", "artificial-organism-research", "--json"])
if r.returncode != 0:
    print(f"FAILED create AC86: {r.stderr}"); sys.exit(1)
ac86 = json.loads(r.stdout)["id"]
print(f"created {ac86}  P65  AC86 (recipe succession)")

# 3. Re-point the serialization chain: AC83 -> AC86 -> AC84 -> AC85
#    (was AC83 -> AC84; insert AC86 between them).
for args, label in [
    (["unlink", AC83, AC84], "unlink AC83->AC84"),
    (["link", AC83, ac86], "link AC83->AC86"),
    (["link", ac86, AC84], "link AC86->AC84"),
]:
    r = run(args)
    if r.returncode != 0:
        print(f"FAILED {label}: {r.stderr}"); sys.exit(1)
    print(label)

print("DONE")

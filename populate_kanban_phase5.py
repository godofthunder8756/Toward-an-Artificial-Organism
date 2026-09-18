import subprocess, json, sys

BOARD = "artificial-organism"
REPO = "/home/elminster/projects/Toward-an-Artificial-Organism"

def run(args):
    return subprocess.run(["hermes", "kanban", "--board", BOARD] + args,
                          capture_output=True, text=True)

body = """The internal-state milestone (AC86-89) is ACCEPTED: internally stored controller information is maintained, reconstructed, and repeatedly transferred to successor storage, with vulnerable coordination state, through the tested environmental challenge. Full autopoiesis remains UNESTABLISHED -- CLOSURE_BOUNDARY_v2.md's declaration that the succession mechanism is "substrate" is a modeling choice, not a settled finding. Do NOT repeat that declaration as a result.

THE DECISIVE NEXT QUESTION (production of the machinery, NOT rewriting it):

> Can the organization replace the finite-lived components enabling reconstruction and coordination, while their loss actually removes those functions and their endogenous replacement restores them?

TWO REQUIREMENTS, kept distinct: (1) rewriting the LAWS governing the mechanism is unnecessary (fixed substrate is fine); (2) producing and replacing the COMPONENTS whose presence makes the mechanism operate is the closure question (Montevil & Mossio 2015). Fixed advance() code is not automatically disqualifying -- what matters is what it represents: reactions enacted by produced finite-lived components (legitimate) vs an always-available coordinator whose execution needs only payable resources (assumes a functional service without demonstrating its production). Naming an operation "format-level" does not decide this.

MEASURE THREE CAUSAL LINKS (one experiment, prespecified as gates):
1. Blocking production reduces the relevant machinery, then reconstruction capacity.
2. Restoring that machinery rescues reconstruction WITHOUT supplying correct controller content.
3. Ordinary operation replaces the machinery repeatedly while controller information and organizational continuity persist.

DESIGN CONSTRAINTS:
- First fix a finite list of the functional components claimed to constitute the organism, and map each to produced-vs-supplied. Stop adding storage layers.
- Use existing W machinery if its specified capabilities genuinely cover the reconstruction/coordination functions; introduce a distinct coordinator component ONLY if the model needs one.
- No arbitrary "alive" flag manufactured to create a dependency.
- RETAIN the simpler repair-only arm throughout; distinguish "replacement as a demonstrated capability" from "replacement as a necessary maintenance process" (repair-only currently survives, so replacement is capability-not-yet-necessity -- do not misrepresent either).

DISCIPLINE: new runner ac91.py (never edit frozen ac80-ac89); engineering first, then hashed protocol + disjoint finals; read CLOSURE_BOUNDARY_v2.md, AC89_RESULTS_v1.md, AC88_RESULTS_v1.md, AC87_RESULTS_v1.md, AC10_RESULTS_V1.md (constituent ablations), AC2_RESULTS_v1.md (produced W catalysts), and the skill 'artificial-organism-research'. THIS CARD ONLY."""

r = run(["create", "AC91: production-dependencies test — can the organization replace the finite-lived components enabling reconstruction and coordination?",
         "--body", body, "--priority", "70",
         "--workspace", f"dir:{REPO}", "--idempotency-key", "ao-production-dependencies",
         "--assignee", "default", "--skill", "artificial-organism-research", "--json"])
if r.returncode != 0:
    print(f"FAILED create AC91: {r.stderr}"); sys.exit(1)
tid = json.loads(r.stdout)["id"]
print(f"created {tid}  P70  AC91 (production-dependencies test)")
print("DONE")

import subprocess, json, sys

BOARD = "artificial-organism"
REPO = "/home/elminster/projects/Toward-an-Artificial-Organism"

def run(args):
    return subprocess.run(["hermes", "kanban", "--board", BOARD] + args,
                          capture_output=True, text=True)

def create(title, body, priority, key):
    r = run(["create", title, "--body", body, "--priority", str(priority),
             "--workspace", f"dir:{REPO}", "--idempotency-key", key,
             "--skill", "artificial-organism-research", "--json"])
    if r.returncode != 0:
        print(f"FAILED create {key}: {r.stderr}"); sys.exit(1)
    data = json.loads(r.stdout)
    return data["id"]

TASKS = [
    dict(key="ao-internalize-recipe", priority=70,
         title="Internalize the reconstruction recipe: store the full organism description in vulnerable state, remove the external prog.program scaffold",
         body="""AC79 froze description STORAGE + MAINTENANCE as endogenous, but the reconstruction RECIPE is still external -- this task removes that scaffold. Verified in the frozen code: reg_maintained (ac79.py) computes target = prog.program(priority), and prog.program (ac5_program.py) hard-codes the five resource/production/repair rule words (1,1,0),(1,2,1),(1,64,6),(1,128,7),(1,256,8) -- the controller's organization -- with only the four bank rules derived from the stored 8-bit permutation. The organism's eight stored bits specify bank ORDERING only; the recipe that turns 8 bits into the 126-bit program is an external Python function, and the regen call is injected BEFORE prog.choose (ac79.py ACTION_LINE replacement). So AC79 shows reconstruction is FUNDED through vulnerable paid machinery (an economic dependency), NOT that the information/machinery performing it is internalized.

GOAL (the decisive next question): can the organism replace its controller using information and functional machinery sustained inside its own organization, once the host stops supplying the reconstruction recipe?

MILESTONE 1 concretely: store the complete organism-specific description -- the five rule words (5x14 = 70 bits) + the 8-bit permutation = 78 bits total -- in vulnerable, damage-streamed, paid-maintained state. Replace prog.program(priority) during life with a generic decode that reads that state by majority and rebuilds the 126-bit program. The generic layer may know the FORMAT (14-bit word = enabled|mask<<1|action<<10, interpreter fallthrough, majority-read, paid write mechanics); NO function on the reconstruction path may know the correct policy. Inherited initial content installed at acquisition is allowed; the host function prog.program that supplies the correct policy during recovery is the scaffold to remove.

MEASURE FIRST (engineering, before any protocol): the "rides the program's corruption trigger (obs bit 2)" argument is conservative only because the program is 16x the 8-bit description. At 78 bits the program is only ~1.6x larger, so obs-bit-2 no longer fires ~45x early -- and the obs space is full (AC79 lesson). First engineering check: does the trigger still precede a description-majority flip, or does the rule-word storage need its own/widened trigger?

DISCIPLINE (from the artificial-organism-research skill): new runner ac80.py (never edit ac76/ac79); mkdir(exist_ok=False) results dir; pre_run_snapshot.json with source sha256 + protocol; rows.jsonl incremental; audit/replay/test tools NOT hashed (AC17 rule); engineering seeds first, excluded from finals; disjoint final seed family. This is MILESTONE 1 only -- do not attempt milestones 2/3 (separate cards).

Read first: ac79.py, ac5_program.py, ac76.py, AC79_RESULTS_v1.md, AC79_PROTOCOL_v1.md, AC76_RESULTS_v1.md, and the skill's "AC79 internalizes description storage, not the reconstruction recipe" entry."""),

    dict(key="ao-reporting-correction", priority=65,
         title="Reporting corrections: AC79 final cohort 2/8-2/8-0/8 (not 12/12), G1 was an outcome-informed revision, AC78 over-reaches, consciousness was a scheduling decision",
         body="""Record the corrections below WITHOUT editing the frozen docs (AC79_RESULTS_v1.md, AC79_PROTOCOL_v1.md, AC78_ENGINEERING_v1.md, AC76_RESULTS_v1.md are frozen -- do not touch them). Write a new non-frozen note (e.g. AC79_ERRATA_v1.md) and/or update the living status file's AC79 section.

1. AC79 final cohort is maintained 2/8, pristine 2/8, unmaintained 0/8 -- recovery demonstrated in the 2 maintained survivors. The engineering run was 12/16 survival ("12/12 recovered" refers to engineering survivors, not the frozen finals). Any summary that reports "12/12" for the frozen result is wrong.

2. AC79's G1 (and G5) were revised AFTER the first 4004-4007 run failed: the population filter moved from alive-at-8192 to survivors (completed), recorded at AC79_PROTOCOL_v1.md lines 113-132. That is a disclosed, outcome-informed endpoint revision, not a prospective untouched gate. "Frozen, six predeclared gates passed" overstates it; conditioning on survival cannot establish recovery across the original cohort. The correction may motivate a fresh prospective study.

3. AC78's "if self-production fails here, it fails everywhere the organism lives" (AC78_ENGINEERING_v1.md line 18-19) over-reaches: it is the AC32/33 six-position ranking world, distinct from AC76's four-bank controller; reversible opportunities, different observations, and recurring environmental changes are not ruled out. Regenerating inherited organization and discovering better organization are SEPARATE problems -- autopoiesis concerns producing the components that realize the organization, not optimal-policy discovery within a lifetime.

4. Consciousness: the archived goal-§7 task (CONSCIOUSNESS_BLOCKS_DISPOSITION_v1.md) reflects a project SCHEDULING decision, not evidence that consciousness-relevant mechanisms require successful priority learning. Autopoiesis is not an established prerequisite in the indicator-based framework (Butlin et al. 2023, arxiv 2308.08708). Theory-specific investigations (e.g. the AC67/71 self-monitoring loop as a candidate indicator) can remain a separate track provided there is a concrete mechanism worth testing. Do not re-gate consciousness work on content self-production.

Read first: AC79_RESULTS_v1.md, AC79_PROTOCOL_v1.md, AC78_ENGINEERING_v1.md, CONSCIOUSNESS_BLOCKS_DISPOSITION_v1.md, AUTONOMY_RESEARCH_STATUS.md, and the skill 'artificial-organism-research' (the "AC79 internalizes description storage, not the reconstruction recipe" entry)."""),

    dict(key="ao-replacement-generations", priority=55,
         title="Milestone 2: replacement across generations of components",
         body="""BLOCKED on ao-internalize-recipe (milestone 1). Do not start until milestone 1's result is recorded.

After milestone 1 internalizes the reconstruction recipe, demonstrate replacement ACROSS GENERATIONS of components: track whether functional copies are constructed, used, and subsequently replaced using internally retained information. Test partial losses and multiple turnover cycles, WITHOUT requiring resurrection after destruction of every usable copy (that is the catastrophic-destruction analog already out of scope).

The concrete design (which components, how replacement is triggered/paid, how "internally retained information" is verified) must be written AFTER milestone 1's result is known -- do not invent it now. When milestone 1 lands, flesh out this card's body into a real protocol following the repo's discipline (engineering -> hashed protocol -> disjoint finals)."""),

    dict(key="ao-combined-frozen", priority=45,
         title="Milestone 3: combine reconstruction + description maintenance + environmental adaptation in one frozen architecture",
         body="""BLOCKED on ao-internalize-recipe (milestone 1) and ao-replacement-generations (milestone 2). Do not start until both are recorded.

Combine three capabilities in ONE frozen architecture: AC75's transition survival (erase-on-relinquish route-move accommodation), AC79's description maintenance, and milestone 1's internalized reconstruction. AC79 explicitly disables route moves (ac79.py sets ac12.MOVE_KEYS=(), MOVE=10**9) -- milestone 3 re-enables them. Test reconstruction + description maintenance + environmental adaptation TOGETHER, and report UNCONDITIONAL survival and recovery on fresh seeds (not conditioned on survivors) -- this closes the survivor-conditioning weakness in AC79's G1 and answers the decisive question end-to-end.

Concrete design to be written after milestones 1 and 2 land; this card is a placeholder for the dependency, not a protocol."""),
]

ids = {}
for t in TASKS:
    tid = create(t["title"], t["body"], t["priority"], t["key"])
    ids[t["key"]] = tid
    print(f"created {tid}  P{t['priority']}  {t['title'][:70]}")

# dependencies: parent -> child
LINKS = [
    ("ao-internalize-recipe", "ao-replacement-generations"),
    ("ao-internalize-recipe", "ao-combined-frozen"),
    ("ao-replacement-generations", "ao-combined-frozen"),
]
for p, c in LINKS:
    r = run(["link", ids[p], ids[c]])
    if r.returncode != 0:
        print(f"FAILED link {p}->{c}: {r.stderr}"); sys.exit(1)
    print(f"linked {ids[p]} -> {ids[c]}  ({p} -> {c})")

print("DONE")

import subprocess, json, sys

BOARD = "artificial-organism"
REPO = "/home/elminster/projects/Toward-an-Artificial-Organism"

def run(args):
    return subprocess.run(["hermes", "kanban", "--board", BOARD] + args,
                          capture_output=True, text=True)

def create(title, body, priority, key):
    r = run(["create", title, "--body", body, "--priority", str(priority),
             "--workspace", f"dir:{REPO}", "--idempotency-key", key, "--json"])
    if r.returncode != 0:
        print(f"FAILED create {key}: {r.stderr}"); sys.exit(1)
    data = json.loads(r.stdout)
    return data["id"]

TASKS = [
    dict(key="ao-signal-horizon", priority=60,
         title="Signal-horizon measurement: can a long-lived organism resolve the rule-value plateau?",
         body="""AC73 established that self-directed rule production is information-limited, not local-optimum-limited: in the AC32/33 regime-B world, a population on single-life scoring caps at the same ~0.85 sites below the ceiling as AC30's single-climber; only oracle (12-seed) scoring reaches the ceiling (0.09 gap). Cause: the ceiling order and a mediocre order differ by only ~0.25 sites on average while single-life noise is sd 0.94 — the fine plateau near the ceiling is below the single-lifetime noise floor.

Open question: does a long-lived organism accumulate enough independent environmental signal to resolve the plateau? This is the prerequisite engineering step for content self-production (ao-content-self-production): before building any "better learner", measure whether the signal exists to learn from.

Read first: AC73_ENGINEERING_v1.md (falsified population premise + signal-floor measurement), AC30_ACQUIRE_v1.md, AC32_RESULTS_v1.md, AC33_RESULTS_v1.md, and the skill 'artificial-organism-research'.

Discipline: engineering first, then hashed protocol, then disjoint final seeds; a negative result is a finding, not a failure."""),

    dict(key="ao-content-self-production", priority=50,
         title="Content self-production: produce the priority description from the organism's own activity",
         body="""The single remaining structural gap for full autopoiesis. The organism re-derives its 126-bit rules from an 8-bit priority description through its own paid, vulnerable machinery (AC76 frozen, commit defc89c) — but the priority itself is externally supplied. That is turnover of an inherited description, not production of it.

AC73 (commit eac25e7) showed the barrier is a signal floor, not search: single-life noise sd 0.94 exceeds the ~0.25-site ceiling-to-mediocre gap. The concrete question is whether the organism can produce its own rules from its own accumulated activity signal (see prerequisite ao-signal-horizon).

Recommend starting in a FRESH session/context — the deep debugging on this line has repeatedly caught subtle self-errors, and a clean window is safer for a study this size.

Read first: AC76_RESULTS_v1.md (turnover mechanism + the "not established" list), AC73_ENGINEERING_v1.md, AC76_ENGINEERING_v1.md, DEPENDENCY_AUDIT_v1.md (causal inventory + the gap this closes), AUTONOMY_RESEARCH_STATUS.md (full history), AC30_ACQUIRE_v1.md, AC32_RESULTS_v1.md, AC33_RESULTS_v1.md.

Success criterion: the rules are produced by the organism's own activity rather than restored from a template. A negative result exposing a structural obstacle is valued over a redefined success."""),

    dict(key="ao-description-maintenance", priority=40,
         title="Description maintenance: store/copy/maintain the self-produced priority through paid vulnerable machinery",
         body="""Follows content self-production (ao-content-self-production). AC76 scoped this out: the 8-bit priority was pristine in the frozen run, so its own storage/copying/maintenance has no explicit causal dependencies yet. Once the priority is self-produced, the description that encodes it must itself be stored, copied, and maintained through the organism's own paid, vulnerable machinery — otherwise it is a hidden pristine backup, which the goal explicitly rules out ("hidden pristine backups ... are not evidence of endogenous reconstruction").

Read first: AC76_RESULTS_v1.md (the "description's own maintenance is unscoped" note), DEPENDENCY_AUDIT_v1.md (the internal-template causal-dependency requirement)."""),

    dict(key="ao-consciousness-blocks", priority=30,
         title="Consciousness-relevant building blocks (goal §7)",
         body="""Goal §7: investigate whether the organization supports experimentally testable building blocks relevant to consciousness. Gated on the autopoiesis line being more complete (after ao-content-self-production). Keep autopoiesis, adaptive autonomy, and consciousness separate — organizational closure is a framework, not a label for every feedback loop. Review ethical safeguards before any experiment intended to introduce potentially valenced experience.

Read first: AUTONOMY_RESEARCH_STATUS.md, the goal mandate §7, DEPENDENCY_AUDIT_v1.md."""),

    dict(key="ao-economic-bound", priority=20,
         title="Economic bound on regeneration: catastrophic-corruption recovery envelope",
         body="""AC76 (frozen) found that >=16-bit sudden corruption is economically unrecoverable: the corruption idles the program (no income) while the paid re-instantiation starves (504 writes, material out in ~4 ticks) — the trigger and the payment are in tension. The goal explicitly scopes out "recovery from complete destruction", so this is a documented limit, not a required milestone. Optional: test whether a starvation buffer, staged regeneration, or a cheaper write extends the recovery envelope.

Read first: AC76_RESULTS_v1.md, AC76_ENGINEERING_v1.md."""),

    dict(key="ao-ac1-ac4-confirm", priority=10,
         title="Independent confirmatory protocol for AC1–AC4 foundational claims",
         body="""Status-table item (line 28): the foundational constituent claims AC1–AC4 (vulnerable controller paying for its own repair; produced W/C/B constituents; boundary) are engineering evidence only — no independent review or new confirmatory protocol. Lower priority now that AC75/AC76 freeze the higher-level closure and turnover claims on fresh seeds, but still open.

Read first: AC1_RESULTS_AND_NEXT_STEP.md, AC2_RESULTS_v1.md, AC3_RESULTS_v1.md, AC4_RESULTS_v1.md, AC4_FOLLOWUP_RESULTS_v1.md."""),
]

ids = {}
for t in TASKS:
    tid = create(t["title"], t["body"], t["priority"], t["key"])
    ids[t["key"]] = tid
    print(f"created {tid}  P{t['priority']}  {t['title'][:60]}")

# dependencies: parent -> child
LINKS = [
    ("ao-signal-horizon", "ao-content-self-production"),
    ("ao-content-self-production", "ao-description-maintenance"),
    ("ao-content-self-production", "ao-consciousness-blocks"),
]
for p, c in LINKS:
    r = run(["link", ids[p], ids[c]])
    if r.returncode != 0:
        print(f"FAILED link {p}->{c}: {r.stderr}"); sys.exit(1)
    print(f"linked {ids[p]} -> {ids[c]}  ({p} -> {c})")

print("DONE")

"""Read-only roster inventory for the GRU own-error audit. Uses `git show` / `git ls-tree` only.
Writes nothing to the repo. Output: roster_inventory.json next to this file."""
import hashlib, json, re, subprocess, sys
from pathlib import Path
REPO = "/workspace/repo"
OUT = Path(__file__).resolve().parent / "roster_inventory.json"
HEADS = {5: "origin/pr/5", 7: "origin/pr/7", 8: "origin/pr/8", 9: "origin/pr/9", 10: "origin/pr/10"}
STUDIES = [  # (pr, directory, seeds, file pattern -> role)
    (7, "recurrent_core_results_v1/checkpoints", range(100, 110), "ckpt"),
    (8, "graded_reversion_results_v1/checkpoints", range(200, 210), "ckpt"),
    (9, "first_order_control_results_v1/checkpoints", range(300, 310), "ckpt"),
    (10, "frozen_recurrent_compensation_results_v1/stage0/checkpoints", range(400, 410), "init_json"),
    (10, "frozen_recurrent_compensation_results_v1/stage1/checkpoints", range(400, 410), "final_json"),
]
# Role is fixed by file name / directory, never by any outcome.
EXPECTED_7 = ["cand_init", "cand_final", "f_init", "f_trained", "f_tuned32", "r_tuned843"] + [
    "sel_g%s_b%s" % (g, b) for g in ("0.5", "1.0", "2.0") for b in ("-2.0", "0.0", "2.0")]
EXPECTED_89 = ["cand_init", "cand_final", "f_init", "f_trained"]
EXPECTED_10 = ["CAND", "R-FIX-32", "R-FIX-48"]
def git(*a, binary=False):
    r = subprocess.run(["git", "-C", REPO, *a], capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode()
def role(pr, stem, kind):
    if kind == "init_json": return "INIT"
    if kind == "final_json": return "TRAINED"
    return "INIT" if stem == "cand_init" else "TRAINED"
def main():
    heads = {p: git("rev-parse", h).strip() for p, h in HEADS.items()}
    rows, missing = [], []
    for pr, d, seeds, kind in STUDIES:
        names = set(git("ls-tree", "--name-only", heads[pr], d + "/").split())
        exp = EXPECTED_7 if pr == 7 else EXPECTED_89 if pr in (8, 9) else EXPECTED_10
        ext = ".ckpt" if kind == "ckpt" else ".json"
        for s in seeds:
            for stem in exp:
                path = "%s/s%d_%s%s" % (d, s, stem, ext)
                if path not in names:
                    missing.append({"pr": pr, "path": path, "reason": "expected by protocol arm list, absent at PR head"}); continue
                raw = git("show", "%s:%s" % (heads[pr], path), binary=True)
                payload = json.loads(raw)
                shapes = {k: v["shape"] for k, v in payload.items()}
                later = {}
                for q in (p for p in HEADS if p > pr):
                    try: later[q] = hashlib.sha256(git("show", "%s:%s" % (heads[q], path), binary=True)).hexdigest()
                    except subprocess.CalledProcessError: later[q] = None
                sha = hashlib.sha256(raw).hexdigest()
                rows.append({"id": "PR%d/s%d/%s%s" % (pr, s, stem, "/init" if kind == "init_json" else ""),
                    "pr": pr, "seed": s, "arm": stem, "role": role(pr, stem, kind), "path": path,
                    "commit": heads[pr], "sha256": sha, "bytes": len(raw),
                    "readout_width": shapes["readout_fc1.weight"][0], "rnn_ih": shapes["rnn.weight_ih_l0"],
                    "identical_at_later_heads": all(v == sha for v in later.values())})
        extra = sorted(n for n in names if not any(n == "%s/s%d_%s%s" % (d, s, e, ext) for s in seeds for e in exp))
        for n in extra: missing.append({"pr": pr, "path": n, "reason": "UNEXPECTED file (not in arm list)"})
    # PR #5: 120 run records, no persisted weights.
    pr5 = sorted(git("ls-tree", "--name-only", heads[5], "acquisition_results_v1/runs/").split())
    pr5_ckpt = [n for n in git("ls-tree", "-r", "--name-only", heads[5]).split()
                if n.startswith("acquisition_results_v1/") and re.search(r"\.(ckpt|pt|pth|safetensors)$", n)]
    for n in pr5:
        missing.append({"pr": 5, "path": n.replace(".json", " (weights)"), "reason": "run record has no weights; no checkpoint persisted in PR #5"})
    out = {"heads": heads, "roster": rows, "missing": missing, "pr5_run_records": len(pr5), "pr5_weight_files": pr5_ckpt,
           "counts": {"total": len(rows), "TRAINED": sum(r["role"] == "TRAINED" for r in rows), "INIT": sum(r["role"] == "INIT" for r in rows)}}
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps(out["counts"]), "missing:", len(missing), "pr5_records:", len(pr5), "pr5_weight_files:", len(pr5_ckpt))
    print("unexpected:", [m for m in missing if m["reason"].startswith("UNEXPECTED")])
    print("not identical later:", [r["id"] for r in rows if not r["identical_at_later_heads"]])
    from collections import Counter
    print(Counter((r["pr"], r["role"], r["readout_width"]) for r in rows))
if __name__ == "__main__": main()

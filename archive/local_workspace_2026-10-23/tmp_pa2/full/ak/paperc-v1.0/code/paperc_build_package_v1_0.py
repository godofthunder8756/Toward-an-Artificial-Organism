# -*- coding: utf-8 -*-
r"""Paper C v1.0 公開パッケージ(paperc-v1.0.zip)を組む。**同梱物は全件 SHA を MANIFEST に書く。**
秘密情報の混入検査(token/key/secret/password の値らしき文字列)を通らなければ zip を作らない。
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
H = Path(__file__).resolve().parent
OUT = H / "paperc-v1.0"
ZIP = H / "paperc-v1.0.zip"

PRIMARY = [
    "PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md",
    "PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5_SEAL_V3.json",
    "PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5_NOVELTY_PASS.json",
    "INSTRUMENT0_STAGE3_FREEZE_MANIFEST_V1.json",
    "INSTRUMENT0_STAGE5_RAW_V1.jsonl",
    "INSTRUMENT0_STAGE5_RESULT_V1.json",
    "STAGE4_PREDICTION_FABLE_V1.json", "STAGE4_PREDICTION_OPUS_V1.json", "STAGE4_PREDICTION_SEAL_V1.json",
    "INSTRUMENT0_PAPER_DISCLOSURE_OBLIGATION_V1.json",
    "INSTRUMENT0_DISCLOSURE_CLASSIFICATION_V1.json",
    "PAPERC_CLAIM_EVIDENCE_V1.json",
    "INSTRUMENT0_STAGE1_FIXTURE_RESULT_V1.json",
    "INSTRUMENT0_STAGE2_PROXY_RESULT_V2.json",
]
CODE = [
    "instrument0_core_v1.py", "instrument0_runner_v1.py", "instrument0_runner_guard_v1.py",
    "instrument0_stage5_aggregate_v1.py", "instrument0_stage1_fixture_v1.py", "instrument0_stage2_proxy_v2.py",
    "make_prereg_freeze_manifest_v2.py", "freeze_guard_v1.py", "protected_write_v1.py",
    "paperc_independent_recompute_v1.mjs", "fable_paperc_independent_recompute_v1.py",
    "paperc_generate_figures_v2.mjs", "paperc_build_pdf_v1.py", "paperc_build_package_v1_0.py",
]
RECEIPTS = [
    "PAPERC_INDEPENDENT_RECOMPUTE_CODEX_V1.json", "FABLE_PAPERC_INDEPENDENT_RECOMPUTE_V1.json",
    "PAPERC_MECHANICAL_VERIFICATION_V1.json", "PAPERC_MECHANICAL_VERIFICATION_V2.json",
    "FABLE_PAPERC_DRAFT_REVIEW_REQUEST_V1.md", "FABLE_PAPERC_DRAFT_REVIEW_V1.json", "FABLE_PAPERC_DRAFT_REVIEW_V2.json",
    "PAPERC_EXTERNAL_LITERATURE_RECEIPT_V1.json", "PAPERC_BILINGUAL_FIDELITY_CODEX_V1.json",
    "PAPERC_PREFLIGHT_CODEX_V1.json", "PAPERC_FIGURE_VISUAL_QA_V1.md", "PAPERC_FIGURE_VISUAL_QA_V2.md",
    "INSTRUMENT0_STAGE3_CLAUSE_BYPASS_INCIDENT_V1.json", "STAGE3_TOOL_KAIBAKU_AMENDMENT_V1.json",
    "PAPERC_ONE_PAGE_DESIGN_V1.md",
]
SECRET_PAT = re.compile(r"(?i)(api[_-]?key|secret|password|passwd|bearer|zenodo[_-]?token|access[_-]?token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    for sub, names in (("primary", PRIMARY), ("code", CODE), ("receipts", RECEIPTS)):
        d = OUT / sub
        d.mkdir(parents=True, exist_ok=True)
        for n in names:
            src = H / n
            if not src.is_file():
                raise SystemExit("**同梱物が無い**: %s" % n)
            shutil.copy2(src, d / n)
    # 秘密情報の混入検査(テキスト系のみ)
    hits = []
    for p in OUT.rglob("*"):
        if p.is_file() and p.suffix.lower() in (".md", ".json", ".jsonl", ".py", ".mjs", ".svg", ".txt"):
            t = p.read_text(encoding="utf-8", errors="replace")
            for m in SECRET_PAT.finditer(t):
                hits.append((str(p.relative_to(OUT)), m.group(0)[:40]))
    if hits:
        for h in hits:
            print("  **秘密らしき文字列**", h)
        raise SystemExit("**混入検査に当たり。zip を作らない**")
    # MANIFEST
    entries = []
    for p in sorted(OUT.rglob("*")):
        if p.is_file() and p.name != "MANIFEST.json":
            entries.append({"path": str(p.relative_to(OUT)).replace("\\", "/"), "sha256": sha(p), "bytes": p.stat().st_size})
    manifest = {
        "schema": "mythos.paperc_release_manifest.v1", "version": "v1.0",
        "primary_manuscript": "PAPERC_V1_0_EN.md / PAPERC_V1_0_EN.pdf",
        "japanese_companion": "PAPERC_V1_0_JA.md / PAPERC_V1_0_JA.pdf",
        "license": "CC-BY-4.0",
        "not_included": "Qwen3-4B base weights and the eight QLoRA adapters (independent rerun of the teacher-forced pass is not claimed)",
        "claim_scope_public": "C1–C7 of PAPERC_CLAIM_EVIDENCE_V1.json, at the ceilings stated in the manuscript",
        "n_files": len(entries), "files": entries,
    }
    (OUT / "MANIFEST.json").write_bytes(json.dumps(manifest, ensure_ascii=False, indent=1).encode("utf-8"))
    readme = ("Paper C v1.0 — Measure the Instrument First\n"
              "Author: Akiyama Satoshi (independent researcher). License: CC-BY-4.0.\n\n"
              "PAPERC_V1_0_EN.pdf / .md   primary manuscript (English)\n"
              "PAPERC_V1_0_JA.pdf / .md   Japanese companion\n"
              "figures/                   figure PNG/SVG, figure data (from frozen raw), manifest\n"
              "primary/                   preregistration V5 (+seal, novelty), stage-3 freeze manifest, 261-row raw, result,\n"
              "                           both prediction tickets + seal, disclosure obligation/classification, claim-evidence\n"
              "code/                      core, runner, guard, aggregator, fixtures, freezer, two independent recomputations, figure generator, builders\n"
              "receipts/                  reviews, recomputation receipts, incident and amendment records, visual QA\n"
              "MANIFEST.json              SHA-256 of every file\n\n"
              "Reproduce the tables: python code/fable_paperc_independent_recompute_v1.py (needs primary/INSTRUMENT0_STAGE5_RAW_V1.jsonl beside it)\n"
              "                      or node code/paperc_independent_recompute_v1.mjs\n")
    (OUT / "README.txt").write_text(readme, encoding="utf-8")
    if ZIP.exists():
        ZIP.unlink()
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(OUT.rglob("*")):
            if p.is_file():
                z.write(p, "paperc-v1.0/" + str(p.relative_to(OUT)).replace("\\", "/"))
    print("zip:", ZIP.name, sha(ZIP), ZIP.stat().st_size, "B  files:", len(entries) + 2)
    return 0


if __name__ == "__main__":
    sys.exit(main())

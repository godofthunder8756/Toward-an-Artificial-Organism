# -*- coding: utf-8 -*-
r"""段3 凍結器 v2。**解縛型 amendment(STAGE3_TOOL_KAIBAKU_AMENDMENT_V1)の
仕様 S1〜S6 の逐語実装。V1 は 1 バイトも変更していない。**

授権: 操作者 2026-08-17「いけ。虎穴に入らずんば虎子を得ず」+ 前進命令 3 声。
一回限り条項: **本器の効力は今回の段3 実行 1 回のみ。**

保存する性質(V1 の制定契機の継承):
  **git blob 検査 → manifest 書込み → freeze_guard --protect / verify を
  同一プロセス内で順に実行し、1 つでも失敗したら rc≠0。**
  『道具を作ったことと、道具が働いていることは別である。』
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

H = Path(__file__).resolve().parent
REPO = H.parents[1]
OUT_NAME = "INSTRUMENT0_STAGE3_FREEZE_MANIFEST_V1.json"   # S1: 固定。runner が pin 済み

# S3(d) 明示床 — **欠けたら rc≠0**
FLOOR = [
    "STAGE3_TOOL_KAIBAKU_AMENDMENT_V1.json",
    "PREREG_INSTRUMENT0_V5_AMENDMENT_A1_RECORD.json",
    "FABLE_V5_AMENDMENT_A1_RATIFICATION_V1.json",
    "INSTRUMENT0_E3_CEILING_DERIVATION_RECEIPT_V1.json",
    "FABLE_B7_CEILING_RECEIPT_RATIFICATION_V1.json",
    "FABLE_BATCH_PLAN_RULING_V3.json",
    "INSTRUMENT0_PRE_DATA_DECISIONS_V1.json",
    "FABLE_PRE_DATA_DECISIONS_RATIFICATION_V1.json",
    "INSTRUMENT0_TOKEN_COUNT_RECEIPT_V1.json",
    "instrument0_token_count_receipt_v1.py",
    "FABLE_TOKEN_COUNT_RECEIPT_RATIFICATION_V1.json",
    "FABLE_RUNNER_RATIFICATION_V1.json",
    "INSTRUMENT0_AMENDMENT_DISPOSITION_ANNEX_V1.json",
    "FABLE_BLOCK_RESOLUTION_RULING_V1.json",
    "FABLE_POST_R6_REPAIR_RATIFICATION_V1.json",
    "INSTRUMENT0_PAPER_DISCLOSURE_OBLIGATION_V1.json",
    "INSTRUMENT0_STAGE4_PREDICTOR_DECISION_V1.json",
]
FLOOR_CTRL = ["AMENDMENT_GATE_ATTACK_RECEIPT_V1.json"]     # 10_control 側

# S3(a) §2.4 列挙物 + (b) runner REQUIRED(runner から import して二重管理を避ける)
SEC24 = [
    "PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md",
    "PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5_NOVELTY_PASS.json",
    "INSTRUMENT0_COHORT_CANDIDATE_V3.json",
    "COHORT_V3_APPROVAL_V1.json",
    "STUDY56_SWAP_MAPPING_V3.json",
    "INSTRUMENT0_IDENTITY_RECEIPT_V1.json",
    "instrument0_identity_receipt_v1.py",
    "instrument0_stage1_fixture_v1.py",
    "INSTRUMENT0_STAGE1_FIXTURE_RESULT_V1.json",
    "instrument0_stage2_proxy_v2.py",
    "INSTRUMENT0_STAGE2_PROXY_RESULT_V2.json",
    "instrument0_b9_verification_v1.py",
    "INSTRUMENT0_B9_IMPLEMENTATION_RECEIPT_V2.json",
    "instrument0_runner_verification_v1.py",
    "INSTRUMENT0_RUNNER_VERIFICATION_V1.json",
    "data/dev_v1.jsonl",
    "COHORT_ROLE_SEPARATION_V1.json",
]
CODEC_NOTE = ("text_codec_source(base_model/Qwen3-4B)は git 管理外のため"
              "直接凍結しない。同一性は INSTRUMENT0_TOKEN_COUNT_RECEIPT_V1 の "
              "codec_vocab_sha256 / codec_config_sha256 / model_config_sha256 "
              "pin が担う(床に含まれ凍結される)")


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_blob_matches(p: Path):
    """対象が **git blob として実在し、SHA が作業ツリーと一致する**か。"""
    rel = str(p.resolve().relative_to(REPO)).replace(os.sep, "/")
    pr = subprocess.run(["git", "show", "HEAD:" + rel], cwd=str(REPO),
                        capture_output=True)
    if pr.returncode != 0:
        return False, "NOT_IN_HEAD"
    same = hashlib.sha256(pr.stdout).hexdigest() == sha_file(p)
    return same, ("MATCH" if same else "WORKTREE_DIFFERS_FROM_HEAD")


def entry(p: Path, role: str) -> dict:
    # H 外(10_control の床)も H 起点の相対で表す。freeze_guard は H/rel で解決する
    rel = os.path.relpath(str(p.resolve()), str(H)).replace(os.sep, "/")
    return {"path": rel, "role": role, "sha256": sha_file(p),
            "bytes": p.stat().st_size}


def main() -> int:
    ap = argparse.ArgumentParser()
    # S2: **命名推測をしない。**3 つの正本は引数で明示的に受ける
    ap.add_argument("--prereg", required=True)
    ap.add_argument("--seal", required=True)
    ap.add_argument("--novelty", required=True)
    ap.add_argument("--frozen-at", required=True,
                    help="凍結時刻(記録用。機械時計は使わない方針)")
    a = ap.parse_args()

    prereg, seal, novelty = (Path(a.prereg).resolve(), Path(a.seal).resolve(),
                             Path(a.novelty).resolve())

    # ---- S2: 内部整合(SHA 連鎖)
    s = json.loads(seal.read_text(encoding="utf-8"))
    if s.get("prereg_sha256") != sha_file(prereg):
        raise SystemExit("**封印受領書の prereg_sha256 が現物と不一致。凍結しない**")
    nv = json.loads(novelty.read_text(encoding="utf-8"))
    nv_flat = json.dumps(nv, ensure_ascii=False)
    if sha_file(prereg)[:16] not in nv_flat and sha_file(prereg) not in nv_flat:
        raise SystemExit("**novelty 受領書が現 prereg の SHA を参照していない。凍結しない**")

    # ---- S1: 出力固定・既存を上書きしない
    out = H / OUT_NAME
    if out.exists():
        raise SystemExit("**%s は既に存在する。上書きしない(段3 は一回)**" % OUT_NAME)

    # ---- S3: 規則収集 + 明示床
    sys.path.insert(0, str(H))
    import instrument0_runner_v1 as R          # (b) REQUIRED を import で共有
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "acg", REPO / "10_control" / "amendment_class_gate_v1.py")
    ACG = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ACG)
    am = ACG.effective_amendments(H, R._v5_amendment_scope)
    if am["unknown"]:
        raise SystemExit("**効力不明の amendment がある。凍結拒否: %r**"
                         % [u["file"] for u in am["unknown"]])

    targets = {}          # rel → (Path, role)

    def add(p: Path, role: str):
        if not p.exists():
            raise SystemExit("**凍結対象が存在しない: %s**" % p)
        targets[str(p.resolve())] = (p, role)

    add(prereg, "prereg")
    add(seal, "seal_receipt")
    add(novelty, "novelty_receipt")
    for n in SEC24:
        add(H / n, "sec2.4")
    for n in R.REQUIRED_UNDER_MANIFEST:
        add(H / n, "runner_required")
    for e in am["effective"] + am["inert"]:
        add(H / e["file"], "amendment_" + ("effective" if e in am["effective"]
                                           else "inert"))
    for n in FLOOR:
        add(H / n, "floor")
    for n in FLOOR_CTRL:
        add(REPO / "10_control" / n, "floor_control")
    add(H / "make_prereg_freeze_manifest_v2.py", "freezer_self")   # S4 自己記録

    # 床の包含 assert
    resolved = {str((H / n).resolve()) for n in FLOOR} | \
               {str((REPO / "10_control" / n).resolve()) for n in FLOOR_CTRL}
    missing_floor = resolved - set(targets)
    if missing_floor:
        raise SystemExit("**床の包含が欠けた: %r**" % sorted(missing_floor))

    # ---- 性質工程 1: git blob 検査(全対象)
    bad = []
    for _, (p, role) in sorted(targets.items()):
        ok, why = git_blob_matches(p)
        if not ok:
            bad.append((str(p.name), why))
    if bad:
        for n, w in bad:
            print("  **%s** %s" % (w, n))
        raise SystemExit("**git blob 検査に失敗。manifest を書かない**")

    # ---- 性質工程 2: manifest 書込み
    entries = [entry(p, role) for _, (p, role) in sorted(targets.items())]
    manifest = {
        "schema": "mythos.instrument0_stage3_freeze.v1",
        "frozen_at": a.frozen_at,
        "authorized_by": "STAGE3_TOOL_KAIBAKU_AMENDMENT_V1.json(操作者採用済み)",
        "one_time": "本凍結は 1 回。再凍結は新たな操作者授権を要する",
        "freezer": {"file": "make_prereg_freeze_manifest_v2.py",
                    "sha256": sha_file(H / "make_prereg_freeze_manifest_v2.py")},
        "codec_note": CODEC_NOTE,
        "n_entries": len(entries),
        "entries": entries,
    }
    blob = json.dumps(manifest, ensure_ascii=False, indent=1).encode("utf-8")
    fd = os.open(out, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)   # S1 O_EXCL
    with os.fdopen(fd, "wb") as f:
        f.write(blob)

    # ---- 性質工程 3: freeze_guard verify + protect(S5: 逐語のまま名指し)
    for args in (["--protect"], []):
        pr = subprocess.run([sys.executable, str(H / "freeze_guard_v1.py"),
                             OUT_NAME] + args,
                            cwd=str(H), capture_output=True, text=True,
                            encoding="utf-8", errors="replace")
        if pr.returncode != 0:
            print(pr.stdout[-800:])
            raise SystemExit("**freeze_guard が失敗。凍結は不成立(rc=%d)**"
                             % pr.returncode)

    print("**段3 凍結完了。**対象 %d 件 / manifest %s"
          % (len(entries), sha_file(out)[:16]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

# -*- coding: utf-8 -*-
r"""INSTRUMENT-0 段6 / **B9 の実装要件 2〜4**。

**封印済み prereg V5 §11 段6 の逐語:**

> 1. **段3 は `make_prereg_freeze_manifest_v1.py` + `freeze_guard_v1.py --protect`
>    を名指しで使う**
> 2. **runner は起動時に自身・config・fixture の SHA を段3 manifest と照合し、
>    不一致なら非ゼロ終了で実行拒否**
> 3. **全 raw に instrument SHA を刻印し、集計・判定器は刻印 ≠ 封印 SHA の raw を
>    自動 INVALID とする**
> 4. **欠陥検出時の分岐は STOP 一本道。許容差の緩和・再試行の経路をコードに
>    存在させない**
>
> **B9 / B10 は実装・検証完了まで `UNRESOLVED` のまま封印・実行 gate に数える。
> 条文列挙だけで `RESOLVED` にしない。**

**要件 1 は段3 の実行方法の指定であり、本器の対象は 2〜4 である。**

**manifest の形式は `freeze_guard_v1.py` と同一**にする。別実装にすると、
片方だけ直したときに検知できない穴が開く(同器の F-2 で実際に起きている)。

---

**要件 4 の検査方針。**「存在させない」を主張するには、**存在しないことを機械で
確かめる**必要がある。本器は対象 script を AST で走査し、

- 許容差らしき識別子(`tol` / `atol` / `rtol` / `eps` / `epsilon` / `tolerance`)
- 再試行らしき識別子(`retry` / `attempt` / `backoff`)
- **例外を握り潰す `except`**(本体が `pass` / `continue` のみ)
- `while True` の中の `try`

を検出する。**検出したものは自動的に不合格ではない。**
**宣言されていなければ不合格**とする。宣言は `DECLARED_RELAXATIONS` に
理由つきで書き、値まで記録する。**黙って存在することだけを禁じる。**

これは「無い」と言い切るための仕組みである。**後から緩和経路を足すと、
宣言を書かないかぎり検査が落ちる。**宣言を書けば差分と受領書に残る。
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

H = Path(__file__).resolve().parent

EXIT_OK = 0
EXIT_IDENTITY_MISMATCH = 3          # **要件2 の非ゼロ終了**
EXIT_MANIFEST_UNUSABLE = 4

STAMP_KEY = "instrument_sha256"
INVALID = "INVALID_INSTRUMENT_STAMP"

RELAX_NAME = re.compile(
    r"^(tol|tolerance|atol|rtol|eps|epsilon|retry|retries|attempt|attempts|backoff)$",
    re.I)

SMALL_FLOAT = 1e-3        # これ未満の float 定数は許容差らしき値として拾う

# **宣言済みの許容差。**これ以外が現れたら不合格になる。
# **緩和の許可ではなく、可視化の義務である。**
#
# 2026-08-17 改訂(Fable 査読 B-3 を受けて):
#   旧版は `instrument0_stage2_proxy_v1.py` の `tol` 引数を宣言していた。
#   **引数は呼び出し側が上書きでき(実際 E4 で 1e-12 → 1e-9 に広げていた)、
#   prereg 段6 要件4 が禁じる「コードに存在する緩和経路」そのものだった。**
#   V2 で引数を廃し、モジュール定数 2 本にした。**定数は経路ではない** —
#   分岐が選ばず、呼び出し側が広げられない。値の変更は差分に現れる。
DECLARED_RELAXATIONS = [
    {"file": "instrument0_stage2_proxy_v2.py", "name": "EQ_EXACT",
     "kind": "float 比較の許容差(**モジュール定数。引数ではない**)",
     "value": "1e-12",
     "why": "**判定閾値ではない。**core の出力と statistics の独立再計算を"
            "突き合わせるための浮動小数点比較。同じ量を別実装で計算しており、"
            "差は丸め誤差のみが想定される。NULL_scale は 1e-1 の桁で、"
            "本値はその 11 桁下にある",
     "not_a_path": "**上書きできない。**呼び出し側に引数が無く、分岐も選ばない"},
    {"file": "instrument0_stage2_proxy_v2.py", "name": "EQ_MEAN",
     "kind": "float 比較の許容差(**モジュール定数。引数ではない**)",
     "value": "1e-9",
     "why": "平均のみ。加算順序が core と statistics.fmean で異なるため"
            "丸めが 1 桁ぶん緩い。**中央値には使わない**",
     "not_a_path": "**上書きできない。**専用の比較関数 `eq_mean` が固定で参照する"},
]


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


# ------------------------------------------------------- 要件2: 起動時の同一性

def manifest_index(manifest: Path) -> dict:
    """**`freeze_guard_v1.targets()` と同じキー名非依存の再帰抽出。**

    固定キーだけを見る実装は、`entries` キーの manifest を対象 0 件と数え、
    **中身を 1 件も見ずに「全一致」を返した。**同じ穴を開けない。
    """
    d = json.loads(manifest.read_text(encoding="utf-8"))
    out = {}
    dup = []

    def walk(x):
        if isinstance(x, dict):
            pa, sh = x.get("path"), x.get("sha256")
            if isinstance(pa, str) and isinstance(sh, str) and len(sh) == 64:
                name = Path(pa).name
                if name in out and out[name] != sh:
                    dup.append(name)
                out[name] = sh
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(d)
    if dup:
        raise ValueError("**同名で SHA が食い違う項目がある: %s**" % sorted(set(dup)))
    return out


def check_frozen_identity(manifest: Path, required, base: Path = None) -> dict:
    """自身・config・fixture の SHA を manifest と照合する。

    **未記載は不一致と同じ扱いにする。**「manifest に無いから素通り」は、
    凍結対象から外すだけで検査を抜けられる穴になる。
    """
    base = base or H
    rec = {"manifest": manifest.name, "n_required": len(required),
           "results": [], "mismatch": [], "verdict": None}
    try:
        idx = manifest_index(manifest)
    except Exception as e:                                   # noqa: BLE001
        rec["verdict"] = "MANIFEST_UNUSABLE"
        rec["error"] = str(e)[:300]
        return rec

    for name in required:
        p = base / name
        if not p.exists():
            r = {"name": name, "state": "MISSING_FILE"}
        elif name not in idx:
            r = {"name": name, "state": "NOT_IN_MANIFEST",
                 "note": "**未記載は不一致と同じ扱い**"}
        else:
            got = sha_file(p)
            r = {"name": name, "recorded": idx[name], "actual": got,
                 "state": "MATCH" if got == idx[name] else "SHA_MISMATCH"}
        rec["results"].append(r)
        if r["state"] != "MATCH":
            rec["mismatch"].append(r)

    rec["verdict"] = "IDENTITY_OK" if not rec["mismatch"] else "IDENTITY_MISMATCH"
    return rec


def assert_frozen_identity(manifest: Path, required, base: Path = None) -> dict:
    """**不一致なら非ゼロ終了で実行拒否する。**例外ではなく終了である。

    例外にすると呼び出し側が握り潰せる。**要件2 の逐語は「非ゼロ終了で実行拒否」**
    であり、握り潰せる経路を残さない。
    """
    rec = check_frozen_identity(manifest, required, base)
    if rec["verdict"] == "IDENTITY_OK":
        return rec
    print("**実行拒否。段3 manifest と一致しない:**")
    for m in rec["mismatch"]:
        print("  %-46s %s" % (m["name"], m["state"]))
    code = (EXIT_MANIFEST_UNUSABLE if rec["verdict"] == "MANIFEST_UNUSABLE"
            else EXIT_IDENTITY_MISMATCH)
    sys.exit(code)


# ------------------------------------------------------- 要件3: raw への刻印

def stamp_raw(payload: dict, instrument_sha: str) -> dict:
    """raw に instrument SHA を刻印する。**既存の刻印を上書きしない。**

    上書きを許すと、封印外の計器で出た raw を後から正しい SHA に書き換えられる。
    """
    if not (isinstance(instrument_sha, str) and len(instrument_sha) == 64):
        raise ValueError("**instrument SHA は 64 桁の全長でなければならない**")
    if STAMP_KEY in payload and payload[STAMP_KEY] != instrument_sha:
        raise ValueError(
            "**既に別の刻印がある。上書きしない: 既存 %s / 新 %s**"
            % (str(payload[STAMP_KEY])[:16], instrument_sha[:16]))
    out = dict(payload)
    out[STAMP_KEY] = instrument_sha
    return out


def validate_raw_stamp(payload: dict, sealed_sha: str) -> dict:
    """**刻印 ≠ 封印 SHA の raw を自動 INVALID にする。**

    **刻印が無い raw も INVALID。**「古いから刻印が無いだけ」を通すと、
    刻印を消せば検査を抜けられる。
    """
    got = payload.get(STAMP_KEY)
    if got is None:
        return {"valid": False, "verdict": INVALID, "reason": "NO_STAMP",
                "note": "**刻印の無い raw は INVALID。**"
                        "刻印を消して抜ける経路を残さない",
                "stamp": None, "sealed": sealed_sha}
    if got != sealed_sha:
        return {"valid": False, "verdict": INVALID, "reason": "STAMP_MISMATCH",
                "stamp": got, "sealed": sealed_sha}
    return {"valid": True, "verdict": "VALID", "stamp": got, "sealed": sealed_sha}


def filter_valid_raws(raws, sealed_sha: str) -> dict:
    """集計・判定器の入口。**INVALID は自動的に落とし、落としたことを記録する。**"""
    kept, dropped = [], []
    for i, r in enumerate(raws):
        v = validate_raw_stamp(r, sealed_sha)
        (kept if v["valid"] else dropped).append({"index": i, "check": v})
    return {"n_in": len(raws), "n_kept": len(kept), "n_dropped": len(dropped),
            "kept": kept, "dropped": dropped,
            "policy": "**刻印 ≠ 封印 SHA および刻印なしは自動 INVALID**"}


# ------------------------------------------------ 要件4: 緩和・再試行の不在検査

# ------------------------------------------------ 死参照(**虚偽の自己記述**)

# **正当な死参照。**理由つきで宣言する。**宣言なき死参照が不合格である。**
# 制定の契機(2026-08-17): runner の docstring が「批准記録の pin を読む」と
# 書きながら、`RATIFICATION` は定義されただけで一度も読まれていなかった。
# 同型が計 4 件。**凍結される成果物に虚偽の自己記述は残せない。**
DECLARED_DEAD_REFERENCES = [
    {"file": "instrument0_runner_v1.py", "name": "TOKEN_RECEIPT",
     "why": "**`measure()` が読む。**未実装であることを docstring の参照表に"
            "明記済み。起動照合(`REQUIRED_UNDER_MANIFEST`)には入れてある",
     "retire_when": "measure() 実装時に宣言から外す"},
    {"file": "instrument0_runner_v1.py", "name": "SWAP3",
     "why": "**`measure()` が読む**(素材同定と item 順序)。同上",
     "retire_when": "measure() 実装時に宣言から外す"},
    {"file": "instrument0_core_v1.py", "name": "EOS_IDS",
     "why": "**`measure()` が読む**(E3 の採点対象 token)。"
            "**Fable の走査が見つけた既存の死参照。**"
            "拘束条件: measure 実装時は必ず `C.EOS_IDS` から読む — "
            "直書きすれば定数の二重管理になり、死参照も残る",
     "retire_when": "measure() 実装時に宣言から外す"},
]


def scan_dead_references(path: Path) -> list:
    """module 直下で定義され、一度も Load されていない名前を挙げる。

    **「読むと書いて読んでいない」の構造化された部分だけを機械化する。**
    散文の自己記述と実装の食い違いは、これでは捕まらない。
    """
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    defined = []
    for st in tree.body:
        if isinstance(st, ast.Assign):
            for t in st.targets:
                if isinstance(t, ast.Name):
                    defined.append((t.id, st.lineno))
    loads = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            loads.add(node.id)
        elif isinstance(node, ast.Attribute):
            v = node.value
            if isinstance(v, ast.Name):
                loads.add(v.id)
    return [{"name": n, "line": ln} for n, ln in defined
            if n not in loads and n.isupper()]


def audit_dead_references(paths) -> dict:
    """**宣言されていない死参照が 1 つでもあれば不合格。**

    緩和検査(`audit_no_relaxation`)と同型: **検出は不合格ではない。
    宣言が無いことが不合格である。**宣言簿はモジュール定数であり、
    呼び出し側から差し替えられない(B-2 の教訓)。
    """
    dec = {(d["file"], d["name"]) for d in DECLARED_DEAD_REFERENCES}
    per_file, undeclared = {}, []
    for p in paths:
        p = Path(p)
        hits = scan_dead_references(p)
        per_file[p.name] = hits
        for h in hits:
            if (p.name, h["name"]) not in dec:
                undeclared.append({"file": p.name, **h})
    return {"n_files": len(per_file), "declared": DECLARED_DEAD_REFERENCES,
            "per_file": per_file, "undeclared": undeclared,
            "verdict": "NO_UNDECLARED_DEAD_REFERENCE" if not undeclared
                       else "UNDECLARED_DEAD_REFERENCE_FOUND",
            "limit": "**機械化できるのは構造化された部分だけである。**"
                     "散文の自己記述と実装の食い違いは、査読の往復が検査線"}


def _handler_swallows(node: ast.ExceptHandler) -> bool:
    return all(isinstance(s, (ast.Pass, ast.Continue)) for s in node.body)


def scan_relaxation_paths(path: Path) -> list:
    """1 ファイルを AST で走査し、緩和・再試行らしき構造を列挙する。"""
    src = path.read_text(encoding="utf-8")
    tree = ast.parse(src, filename=str(path))
    found = []

    # **名前ではなく値の形でも拾う。**識別子を改名すれば検査を抜けられる、
    # という穴を塞ぐ(2026-08-17、Fable 査読 B-2 の趣旨)。
    for st in tree.body:
        if isinstance(st, ast.Assign) and isinstance(st.value, ast.Constant) \
                and isinstance(st.value.value, float) \
                and 0 < abs(st.value.value) < SMALL_FLOAT:
            for t in st.targets:
                if isinstance(t, ast.Name):
                    found.append({"kind": "SMALL_FLOAT_CONSTANT",
                                  "name": t.id, "line": st.lineno,
                                  "value": repr(st.value.value)})

    for node in ast.walk(tree):
        if isinstance(node, ast.arg) and RELAX_NAME.match(node.arg):
            found.append({"kind": "ARG", "name": node.arg, "line": node.lineno})
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) \
                and RELAX_NAME.match(node.id):
            found.append({"kind": "ASSIGN", "name": node.id, "line": node.lineno})
        elif isinstance(node, ast.keyword) and node.arg \
                and RELAX_NAME.match(node.arg):
            found.append({"kind": "KWARG", "name": node.arg, "line": node.lineno})
        elif isinstance(node, ast.ExceptHandler) and _handler_swallows(node):
            found.append({"kind": "SWALLOWING_EXCEPT", "name": "except",
                          "line": node.lineno})
        elif isinstance(node, ast.While):
            is_true = (isinstance(node.test, ast.Constant)
                       and node.test.value is True)
            has_try = any(isinstance(s, ast.Try) for s in ast.walk(node))
            if is_true and has_try:
                found.append({"kind": "RETRY_LOOP", "name": "while True + try",
                              "line": node.lineno})
    return found


def audit_no_relaxation(paths) -> dict:
    """**宣言されていない緩和・再試行が 1 つでもあれば不合格。**

    2026-08-17 改訂(Fable 査読 B-2): 旧版は `declared=` 引数を持ち、
    **呼び出し側が宣言簿ごと差し替えられた。**検査器の答えを呼び出し側が
    決められる形は、検査器ではない。**引数を廃し、モジュール定数のみを見る。**
    """
    dec = {(d["file"], d["name"].lower()) for d in DECLARED_RELAXATIONS}
    per_file, undeclared = {}, []
    for p in paths:
        p = Path(p)
        hits = scan_relaxation_paths(p)
        per_file[p.name] = hits
        for h in hits:
            if (p.name, h["name"].lower()) not in dec:
                undeclared.append({"file": p.name, **h})
    return {"n_files": len(per_file),
            "declared": DECLARED_RELAXATIONS,
            "per_file": per_file,
            "undeclared": undeclared,
            "verdict": "NO_UNDECLARED_RELAXATION" if not undeclared
                       else "UNDECLARED_RELAXATION_FOUND",
            "policy": "**検出は不合格ではない。宣言が無いことが不合格である。**"
                      "後から緩和経路を足すと、宣言を書かないかぎり落ちる"}


# ------------------------------------------------------------------- CLI

def main() -> int:
    ap = argparse.ArgumentParser(
        description="INSTRUMENT-0 runner guard(B9 要件2〜4)")
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--require", required=True,
                    help="段3 manifest と照合するファイル名。コンマ区切り")
    ap.add_argument("--base", default=None)
    a = ap.parse_args()
    base = Path(a.base).resolve() if a.base else H
    names = [x.strip() for x in a.require.split(",") if x.strip()]
    rec = assert_frozen_identity(Path(a.manifest).resolve(), names, base)
    print("**同一性 OK。%d 件すべてが段3 manifest と一致**" % rec["n_required"])
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())

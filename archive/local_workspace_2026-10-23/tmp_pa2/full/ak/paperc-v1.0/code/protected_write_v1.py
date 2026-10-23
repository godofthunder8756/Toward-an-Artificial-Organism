# -*- coding: utf-8 -*-
"""**書込み経路そのものに順序を強制する。**変更後の検査では再発を防げない。

制定の契機(2026-08-15、操作者指摘):
  `freeze_guard_v1.py` を作ったが**どこからも呼ばれておらず**、
  凍結物は全て書込可のままだった(Fable F-1 が実測)。
  **変更後の検査は、変更が起きた後にしか働かない。**

  根本予防は変更後の検査ではない:

    **原版保存(内容アドレス) → SHA 確認 → 新 version への書込み → 新 manifest 作成**

  **この順序を write path そのものに強制しない限り、
  freeze_guard が存在しても再発する。**

使い方:
    from protected_write_v1 import protected_write
    protected_write(path, new_bytes)      # 既存があれば原版を退避してから書く

  退避に失敗した場合、**書込みを拒否する。**上書きしない。

退避先:
    `_originals/<sha256>.bytes`  — **内容アドレス。**同じ内容は1度しか保存されない
    `_originals/index.jsonl`     — path / sha256 / 退避時刻 / 呼び出し元

**過去物は書き換えない。**本モジュールは以後の書込みに順序を課すだけである。
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import stat
import sys
import traceback
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
H = Path(__file__).parent
VAULT = H / "_originals"
INDEX = VAULT / "index.jsonl"
NL = chr(10)


class WriteRefused(Exception):
    """**退避が検証できないときに書込みを拒否する。**"""


def _sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def stash_original(p: Path, caller: str = "") -> dict:
    """**原版を内容アドレスで退避し、退避物の SHA を照合して返す。**

    照合できなければ `WriteRefused` を投げる。**黙って進まない。**
    """
    raw = p.read_bytes()
    h = _sha(raw)
    VAULT.mkdir(exist_ok=True)
    dst = VAULT / ("%s.bytes" % h)
    if not dst.exists():
        # 読み取り専用でも退避先には書ける(別ファイルなので)
        dst.write_bytes(raw)
    # **退避物を読み直して照合する。**書いたつもりで終わらせない
    back = _sha(dst.read_bytes())
    if back != h:
        raise WriteRefused(
            "**退避物の SHA が原版と一致しない。書込みを拒否する。** "
            "原版 %s / 退避 %s" % (h[:16], back[:16]))
    rec = {"ts": datetime.datetime.now().astimezone().isoformat(),
           "path": str(p.relative_to(H)) if p.is_relative_to(H) else str(p),
           "sha256": h, "bytes": len(raw), "vault": dst.name, "caller": caller}
    with INDEX.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + NL)
    return rec


def protected_write(path, data, *, caller: str = None,
                    allow_new: bool = True,
                    text_newline_compat: bool = True) -> dict:
    """**順序を強制して書く。**

    1. 既存があれば **原版を内容アドレスで退避**
    2. **退避物の SHA を照合**(失敗したら書かない)
    3. 書込み
    4. 書いたものの SHA を返す(**呼び出し側が新 manifest を作る材料**)

    読み取り専用属性が立っていても、**退避が成立してから**外して書く。
    """
    p = Path(path)
    if caller is None:
        st = traceback.extract_stack()[-2]
        caller = "%s:%d" % (Path(st.filename).name, st.lineno)
    # **D1 バイト中立。**`Path.write_text(s, encoding="utf-8")` は
    # テキストモード(newline=None)なので \\n を os.linesep へ変換する。
    # 変換しないと、**保護経路へ移しただけで凍結物の SHA が動く。**
    if isinstance(data, str):
        if text_newline_compat and os.linesep != NL:
            data = data.replace(NL, os.linesep)
        b = data.encode("utf-8")
    else:
        b = data

    stashed = None
    if p.exists():
        stashed = stash_original(p, caller)          # 失敗すれば例外で止まる
        if stashed["sha256"] == _sha(b):
            return {"path": str(p), "unchanged": True,
                    "sha256": stashed["sha256"], "stashed": stashed}
        try:
            os.chmod(p, os.stat(p).st_mode | stat.S_IWRITE)
        except Exception as e:                       # noqa: BLE001
            raise WriteRefused("**書込み属性を戻せない: %s**" % e)
    elif not allow_new:
        raise WriteRefused("**新規作成が許可されていない: %s**" % p)

    p.parent.mkdir(parents=True, exist_ok=True)
    # **D2 原子性。**途中で落ちても最終パスに切れたファイルを残さない。
    # 着地は os.replace であり、原版退避は既に済んでいる(保護順序は保たれる)。
    tmp = p.with_name(p.name + ".pwtmp")
    try:
        tmp.write_bytes(b)
        os.replace(tmp, p)
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except Exception:                            # noqa: BLE001
                pass
    got = _sha(p.read_bytes())
    if got != _sha(b):
        raise WriteRefused("**書込み後の SHA が一致しない。**%s" % p)
    return {"path": str(p), "unchanged": False, "sha256": got,
            "stashed": stashed, "caller": caller}


def audit_bypass(manifests=None) -> dict:
    """**遡及一覧。**どの成果物が、どの時点で、どのガードを経由せず作られたか。

    **過去物を書き換えない。**読み取りのみで一覧を作る。
    """
    stashed = set()
    if INDEX.exists():
        for l in INDEX.open(encoding="utf-8"):
            if l.strip():
                try:
                    stashed.add(json.loads(l)["path"])
                except Exception:                    # noqa: BLE001
                    pass
    mans = manifests or sorted(H.glob("*FREEZE_MANIFEST*.json"))
    rows = []
    for m in mans:
        try:
            d = json.loads(m.read_text(encoding="utf-8"))
        except Exception:                            # noqa: BLE001
            continue
        frozen_at = d.get("frozen_at")
        targets = []

        def walk(x):
            if isinstance(x, dict):
                pa, sh = x.get("path"), x.get("sha256")
                if isinstance(pa, str) and isinstance(sh, str) and len(sh) == 64:
                    targets.append((pa, sh))
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(d)

        for pa, sh in targets:
            p = H / pa
            if not p.exists():
                rows.append({"manifest": m.name, "path": pa,
                             "state": "**MISSING**"}); continue
            cur = _sha(p.read_bytes())
            mt = datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat()
            ro = not bool(os.stat(p).st_mode & stat.S_IWRITE)
            state = "OK" if cur == sh else "**SHA_MISMATCH**"
            mutated_after = bool(frozen_at and mt > str(frozen_at)[:19])
            rows.append({
                "manifest": m.name, "path": pa, "state": state,
                "recorded_sha256": sh, "current_sha256": cur,
                "frozen_at": frozen_at, "mtime": mt,
                "mutated_after_freeze": mutated_after,
                "read_only_now": ro,
                # **原版が退避されていたか。**していなければ回収不能クラス
                "original_stashed": pa in stashed,
                "guard_bypassed": (state != "OK" and pa not in stashed)})
    return {"schema": "mythos.guard_bypass_audit.v1",
            "generated_at": datetime.datetime.now().astimezone().isoformat(),
            "purpose": "**どの成果物が、どの時点で、どのガードを経由せず作られたか。**"
                       "過去物は書き換えない",
            "n_targets": len(rows),
            "n_mismatch": sum(1 for r in rows if r["state"] != "OK"),
            "n_mutated_after_freeze": sum(1 for r in rows
                                          if r.get("mutated_after_freeze")),
            "n_unprotected": sum(1 for r in rows if not r.get("read_only_now")),
            "n_guard_bypassed": sum(1 for r in rows if r.get("guard_bypassed")),
            "rows": rows}


def wiring_audit() -> dict:
    """**未接続の書込み元を一覧する。**

    凍結物(manifest / seal / notice)を書くスクリプトのうち、
    **protected_write を通していないもの**を挙げる。
    道具の存在ではなく **接続** を測る。F-1 の再発検知。
    """
    import re
    KINDS = ("FREEZE_MANIFEST", "_SEAL_V1", "NOTICE", "_NOVELTY_PASS")
    # 凍結 manifest に SHA 記載のあるスクリプト = **編集不可**
    _frozen = set()
    for m in H.glob("*FREEZE_MANIFEST*.json"):
        try:
            d = json.loads(m.read_text(encoding="utf-8"))
        except Exception:                                # noqa: BLE001
            continue

        def _w(x):
            if isinstance(x, dict):
                pa, sh = x.get("path"), x.get("sha256")
                if isinstance(pa, str) and isinstance(sh, str) and len(sh) == 64:
                    _frozen.add(Path(pa).name)
                for v in x.values():
                    _w(v)
            elif isinstance(x, list):
                for v in x:
                    _w(v)
        _w(d)
    rows = []
    for f in sorted(H.glob("*.py")):
        if f.name == Path(__file__).name:
            continue
        t = f.read_text(encoding="utf-8", errors="replace")
        # **D3 fail-open を塞ぐ。**write_text/write_bytes の語が消えた
        # スクリプトが分母ごと消えると、未接続ではなく**不可視**になる。
        # protected_write を参照するものも writer として数える。
        writes = bool(re.search(r"write_text|write_bytes|protected_write", t))
        kind = [k for k in KINDS if k in t]
        if not (writes and kind):
            continue
        wired = "protected_write" in t
        # **未接続の理由を分ける。**凍結物は編集不可であり、怠慢ではない。
        # ここを「直そう」として編集すると凍結違反になる(88秒事件と同型)。
        rows.append({"script": f.name, "writes_kinds": kind, "wired": wired,
                     "frozen_uneditable": (not wired) and (f.name in _frozen),
                     "reason": ("接続済み" if wired
                                else "**凍結物のため編集不可。接続しないことが正しい**"
                                if f.name in _frozen
                                else "未対応の負債(今日の経路上に無い)")})
    return {"schema": "mythos.protected_write_wiring.v1",
            "generated_at": datetime.datetime.now().astimezone().isoformat(),
            "purpose": "**道具の存在ではなく接続を測る。**F-1 の再発検知",
            "n_writers": len(rows),
            "n_wired": sum(1 for r in rows if r["wired"]),
            "n_unwired": sum(1 for r in rows if not r["wired"]),
            "n_unwired_frozen_uneditable":
                sum(1 for r in rows if r.get("frozen_uneditable")),
            "n_unwired_debt": sum(1 for r in rows
                                  if not r["wired"] and not r.get("frozen_uneditable")),
            "rows": rows}


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true",
                    help="**遡及一覧を作る。**書き換えない")
    ap.add_argument("--out", default="GUARD_BYPASS_AUDIT_V1.json")
    ap.add_argument("--wiring", action="store_true",
                    help="**未接続の書込み元を一覧する**")
    a = ap.parse_args()
    if a.wiring:
        w = wiring_audit()
        (H / "PROTECTED_WRITE_WIRING_V1.json").write_text(
            json.dumps(w, ensure_ascii=False, indent=1), encoding="utf-8")
        print("=== 保護経路の接続状況 ===")
        print(" 凍結物を書くスクリプト %d 件 / **接続済み %d / 未接続 %d**"
              % (w["n_writers"], w["n_wired"], w["n_unwired"]))
        print("   うち **凍結物のため編集不可 %d** / **未対応の負債 %d**"
              % (w["n_unwired_frozen_uneditable"], w["n_unwired_debt"]))
        for r in w["rows"]:
            mark = ("OK " if r["wired"]
                    else "**凍**" if r.get("frozen_uneditable") else "**未**")
            print("  %s %-40s %-16s %s" % (mark, r["script"],
                                           ",".join(r["writes_kinds"]),
                                           r.get("reason", "")))
        return 0
    if not a.audit:
        print(__doc__)
        return 0
    r = audit_bypass()
    (H / a.out).write_text(json.dumps(r, ensure_ascii=False, indent=1),
                           encoding="utf-8")
    print("=== ガード迂回の遡及一覧 ===")
    print(" 対象 %d 件" % r["n_targets"])
    print(" **SHA 不一致       : %d**" % r["n_mismatch"])
    print(" **凍結後に更新     : %d**" % r["n_mutated_after_freeze"])
    print(" **読み取り専用でない: %d**" % r["n_unprotected"])
    print(" **原版未退避のまま不一致(回収不能クラス): %d**" % r["n_guard_bypassed"])
    print(" written: %s" % a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

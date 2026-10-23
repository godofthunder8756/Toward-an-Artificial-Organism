# -*- coding: utf-8 -*-
"""**凍結の直後に整合を検査し、凍結対象を読み取り専用にする。**

制定の契機(2026-08-15、Fable Stage 1B 指摘):
  凍結違反が起きたが、**是正はすべて「起きたことの記録」であり、
  『凍結の88秒後に同じパスへ書けた』という穴を一つも塞いでいなかった。**
  検出(巡回)はあったが**防止が無かった。**票ではなくコードの一手が要る。

二段で防ぐ:
  1. **freeze 直後に自動整合検査を1回走らせる**(書いた直後にズレていないか)
  2. **凍結対象を read-only にする**(Windows: 読み取り専用属性)

**read-only は「消せない」ではなく「うっかり書けない」である。**
意図的な解除は可能であり、それは記録に残る操作にする。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
H = Path(__file__).parent


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def targets(man: Path):
    """manifest が名指しするファイルを列挙する。**キー名に依存しない再帰抽出。**

    2026-08-15 修正(Fable F-2):
      旧版は固定キー(files / frozen_files / results / code / prereg_and_packets)
      しか見ず、**`entries` キーを使う LEGACY manifest は対象0件になり、
      中身を1件も見ずに「全一致」rc=0 を返していた。**
      姉妹計器 manifest_reproducibility_audit_v1.py は同型の穴を同日に塞ぎ、
      キー名非依存の抽出器を既に持っていた。**共有していなかったので隣で再発した。**
    """
    d = json.loads(man.read_text(encoding="utf-8"))
    out, seen = [], set()

    def walk(x):
        if isinstance(x, dict):
            pa, sh = x.get("path"), x.get("sha256")
            if isinstance(pa, str) and isinstance(sh, str) and len(sh) == 64:
                if (pa, sh) not in seen:
                    seen.add((pa, sh))
                    out.append((pa, sh))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)

    walk(d)
    return out


def verify(man: Path):
    bad, n = [], 0
    for rel, want in targets(man):
        p = H / rel
        n += 1
        if not p.exists():
            bad.append("**欠落** %s" % rel)
            continue
        got = sha(p)
        if got != want:
            bad.append("**SHA 不一致** %s (記録 %s / 現物 %s)"
                       % (rel, want[:16], got[:16]))
    return n, bad


def protect(man: Path, undo: bool = False):
    """**読み取り専用にする。**うっかり書き換えを止めるのが目的。

    2026-08-15 修正(Fable F-2): **manifest 自身も保護する。**
    旧版は名指しされたファイルだけを守り、manifest を無防備に残していた。
    """
    done = []
    # **manifest 自身を先に含める**
    for rel, _ in [(man.name, None)] + list(targets(man)):
        p = H / rel
        if not p.exists():
            continue
        try:
            m = os.stat(p).st_mode
            if undo:
                os.chmod(p, m | stat.S_IWRITE)
            else:
                os.chmod(p, m & ~stat.S_IWRITE)
            done.append(rel)
        except Exception as e:                           # noqa: BLE001
            print("  **属性変更失敗 %s: %s**" % (rel, e))
    return done


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest")
    ap.add_argument("--protect", action="store_true",
                    help="**整合検査 PASS のときだけ read-only にする**")
    ap.add_argument("--unprotect", action="store_true",
                    help="**意図的な解除。**記録に残す前提")
    a = ap.parse_args()
    man = H / a.manifest
    if not man.exists():
        print("**manifest が無い: %s**" % a.manifest)
        return 2

    if a.unprotect:
        d = protect(man, undo=True)
        print("**読み取り専用を解除した: %d 件。**"
              "**これは記録に残すべき操作である**" % len(d))
        return 0

    n, bad = verify(man)
    print("=== 凍結直後の整合検査 ===")
    print(" manifest: %s (SHA %s)" % (man.name, sha(man)[:32]))
    print(" 対象 %d 件" % n)
    # **F-2: 対象0件を合格にしない。**抽出に失敗している可能性の方が高い
    if n == 0:
        print(" **対象が0件。抽出に失敗している疑いがある。**"
              "**合格にしない**(旧版はここで rc=0 を返していた)")
        return 3
    if bad:
        for b in bad[:12]:
            print("  ", b)
        print(" **%d 件の不一致。read-only 化しない。**"
              "**凍結は成立していない**" % len(bad))
        return 1
    print(" **全一致。**")
    if a.protect:
        d = protect(man)
        print(" **read-only 化: %d 件。**うっかり書き換えを止める" % len(d))
        print(" (意図的な解除は --unprotect。**記録に残すこと**)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

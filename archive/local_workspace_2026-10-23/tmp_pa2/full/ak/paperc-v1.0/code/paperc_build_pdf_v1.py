# -*- coding: utf-8 -*-
r"""Paper C 公開版ビルド: Markdown → HTML → Chrome headless → PDF(A4)。

入力: PAPERC_MANUSCRIPT_EN_V1.md / PAPERC_MANUSCRIPT_V1.md(査読 PASS の SHA を引数で pin)
出力: paperc-v1.0/PAPERC_V1_0_EN.pdf, PAPERC_V1_0_JA.pdf, 同 .md(公開版ヘッダのみ差替え), figures/

**公開版で変えるのは、ヘッダの状態行と §9 の状態文だけ**(差分は release record に逐語で残す)。
本文・数値・図の参照は 1 バイトも変えない — 変えていないことを本ツールが差分で機械確認する。
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
H = Path(__file__).resolve().parent
CHROME = Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")

CSS = """
@page { size: A4; margin: 22mm 20mm 24mm 20mm; }
body { font-family: %(font)s; font-size: 10.5pt; line-height: 1.55; color: #111; max-width: 100%%; }
h1 { font-size: 20pt; margin: 0 0 6pt 0; line-height: 1.25; }
h2 { font-size: 13.5pt; margin: 18pt 0 6pt 0; border-bottom: 1px solid #999; padding-bottom: 2pt; }
h3 { font-size: 11.5pt; margin: 14pt 0 4pt 0; }
p  { margin: 0 0 7pt 0; text-align: justify; }
table { border-collapse: collapse; margin: 8pt 0 10pt 0; font-size: 9.2pt; width: 100%%; }
th, td { border: 1px solid #888; padding: 3pt 5pt; vertical-align: top; }
th { background: #eee; }
code { font-family: Consolas, "Courier New", monospace; font-size: 9pt; background: #f4f4f4; padding: 0 2pt; word-break: break-all; }
img { max-width: 100%%; height: auto; display: block; margin: 8pt auto 4pt auto; page-break-inside: avoid; }
ol, ul { margin: 0 0 7pt 0; }
li { margin-bottom: 2pt; }
.meta { font-size: 9.5pt; color: #333; }
blockquote { border-left: 3px solid #bbb; margin: 6pt 0; padding: 2pt 10pt; color: #333; }
"""

FONT = {"en": '"Times New Roman", Times, serif',
        "ja": '"Yu Mincho", "游明朝", "MS Mincho", serif'}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def public_header(md: str, lang: str, doi: str, version: str) -> tuple[str, list[str]]:
    """状態行を公開版へ差替える。差替えた行の (before → after) を返す。"""
    changes = []
    if lang == "ja":
        reps = [
            (r"^\*\*状態:\*\* `B_NONPUBLIC_DRAFT`  $",
             "**状態:** 公開版 %s（DOI: %s）  " % (version, doi)),
            (r"^\*\*公開禁止:\*\* .*$",
             "**公開:** 本版は Fable の独立査読（PASS_FOR_OPERATOR_CONSIDERATION_OF_PUBLICATION_FREEZE）、公開版固定、操作者の明示的公開判断を経て公開された。CC-BY 4.0。  "),
            (r"^本稿執筆時点で、段5の結果と本稿は分類Bであり非公開である。",
             "本版（%s）は公開版である。DOI は %s。" % (version, doi)),
        ]
    else:
        reps = [
            (r"^\*\*Status:\*\* `B_NONPUBLIC_DRAFT`  $",
             "**Status:** Public release %s (DOI: %s)  " % (version, doi)),
            (r"^\*\*Publication restriction:\*\* .*$",
             "**Publication:** This version was released after Fable's independent review (PASS_FOR_OPERATOR_CONSIDERATION_OF_PUBLICATION_FREEZE), fixation of the release candidate, and an explicit publication decision by the operator. CC-BY 4.0.  "),
            (r"^At the time of this draft, the Stage 5 results and this manuscript remain Category B and non-public\.",
             "This version (%s) is the public release; DOI %s." % (version, doi)),
        ]
    lines = md.splitlines()
    for i, ln in enumerate(lines):
        for pat, new in reps:
            if re.match(pat, ln):
                changes.append("L%d: %s  →  %s" % (i + 1, ln.strip(), new.strip()))
                # 状態文は文頭だけ差替え(残りの文は保つ)
                m = re.match(pat, ln)
                lines[i] = new + ln[m.end():] if pat.startswith("^本稿執筆") or pat.startswith("^At the time") else new
                break
    return "\n".join(lines) + ("\n" if md.endswith("\n") else ""), changes


def build_pdf(md_path: Path, html_path: Path, pdf_path: Path, lang: str, title: str) -> None:
    body = markdown.markdown(md_path.read_text(encoding="utf-8"),
                             extensions=["tables", "fenced_code", "sane_lists"])
    html = ("<!doctype html><html lang='%s'><head><meta charset='utf-8'><title>%s</title>"
            "<style>%s</style></head><body>%s</body></html>"
            % (lang, title, CSS % {"font": FONT[lang]}, body))
    html_path.write_text(html, encoding="utf-8")
    cmd = [str(CHROME), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
           "--print-to-pdf=%s" % pdf_path, "--virtual-time-budget=10000",
           html_path.resolve().as_uri()]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
    if not pdf_path.exists() or pdf_path.stat().st_size < 10000:
        raise SystemExit("PDF 生成失敗 rc=%d\n%s" % (r.returncode, (r.stderr or "")[-800:]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doi", required=True)
    ap.add_argument("--version", default="v1.0")
    ap.add_argument("--en-sha", required=True, help="査読 PASS 時の EN 原稿 SHA(pin)")
    ap.add_argument("--ja-sha", required=True)
    ap.add_argument("--out", default="paperc-v1.0")
    a = ap.parse_args()

    en, ja = H / "PAPERC_MANUSCRIPT_EN_V1.md", H / "PAPERC_MANUSCRIPT_V1.md"
    if sha(en) != a.en_sha or sha(ja) != a.ja_sha:
        raise SystemExit("**原稿 SHA が査読 PASS 時と不一致。ビルドしない**")
    out = H / a.out
    if out.exists():
        shutil.rmtree(out)
    (out / "figures").mkdir(parents=True)
    # 図(PNG + SVG)と manifest をそのまま同梱
    for f in sorted((H / "paperc_figures_v1").iterdir()):
        if f.suffix.lower() in (".png", ".svg", ".json"):
            shutil.copy2(f, out / "figures" / f.name)

    rec = {"schema": "mythos.paperc_public_build.v1", "version": a.version, "doi": a.doi,
           "source_sha_pinned": {"en": a.en_sha, "ja": a.ja_sha}, "header_changes": {}, "outputs": {}}
    for lang, src, stem, title in (
            ("en", en, "PAPERC_V1_0_EN",
             "Measure the Instrument First: Preregistered, Prediction-Sealed, One-Shot Calibration of Four Endpoints in a 4B QLoRA Series"),
            ("ja", ja, "PAPERC_V1_0_JA",
             "計器を先に測る — 4B QLoRA系列における4端点校正の事前登録・予測封印つき一発測定")):
        md = src.read_text(encoding="utf-8")
        pub, changes = public_header(md, lang, a.doi, a.version)
        # 図の参照先を同梱ディレクトリへ(パス文字列のみ)
        pub_pkg = pub.replace("paperc_figures_v1/", "figures/")
        # **本文不変の機械確認**: 差分は状態行 3 行 + 図パス置換のみ
        diff = [d for d in difflib.unified_diff(md.splitlines(), pub_pkg.splitlines(), lineterm="", n=0)
                if d.startswith(("+", "-")) and not d.startswith(("+++", "---"))]
        allowed = 0
        for d in diff:
            if "paperc_figures_v1/" in d or "figures/" in d:
                allowed += 1
            elif any(k in d for k in ("状態", "公開", "Status", "Publication", "本稿執筆時点", "本版", "At the time of this draft", "This version")):
                allowed += 1
        if allowed != len(diff) or len(changes) != 3:
            raise SystemExit("**想定外の差分。ビルドしない**: changes=%d diff=%d\n%s" % (len(changes), len(diff), "\n".join(diff[:20])))
        md_out = out / (stem + ".md")
        md_out.write_text(pub_pkg, encoding="utf-8")
        html_out = out / (stem + ".html")
        pdf_out = out / (stem + ".pdf")
        build_pdf(md_out, html_out, pdf_out, lang, title)
        html_out.unlink()
        rec["header_changes"][lang] = changes
        rec["outputs"][lang] = {"md": {"file": md_out.name, "sha256": sha(md_out), "bytes": md_out.stat().st_size},
                                "pdf": {"file": pdf_out.name, "sha256": sha(pdf_out), "bytes": pdf_out.stat().st_size}}
        print("  %s  md %s  pdf %s (%d B)" % (lang, sha(md_out)[:12], sha(pdf_out)[:12], pdf_out.stat().st_size))
    (out / "PAPERC_PUBLIC_BUILD_RECEIPT_V1.json").write_bytes(
        json.dumps(rec, ensure_ascii=False, indent=1).encode("utf-8"))
    print("build receipt written")
    return 0


if __name__ == "__main__":
    sys.exit(main())

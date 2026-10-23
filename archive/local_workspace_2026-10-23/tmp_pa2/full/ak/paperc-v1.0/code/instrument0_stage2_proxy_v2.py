# -*- coding: utf-8 -*-
r"""INSTRUMENT-0 段2 **V2** — 代理データ互換試験(**R14**)。

**V1 は無効である。消さない。**`INSTRUMENT0_STAGE2_INVALIDATION_V1.json` を参照。

---

**V1 の誤り(2026-08-17、Fable 査読で判明):**

V1 は prereg の「**凍結 55 件は読込経路の互換試験に限る**」を
「**55 件 = STUDY55 系の略記**」と読んだ。**誤りである。**

- `PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V3.md` 236 行が定義を書いている:
  「本試験での代理データ: **RETRO-0 で既に閲覧済みの凍結 55 件**」
- 列挙は実在する: `RETRO0_EVIDENCE_ATLAS_V1〜V4` すべて `n_artifacts=55` / `rows=55`
- V5 §0 が自らの出典に挙げる `FABLE_BLOCK_RULING_INSTRUMENT0_V1.json` の B11 が
  「**RETRO-0 の凍結55件は…**」と逐語で書いている

**V1 は freeze manifest しか見ずに否定を主張した。**しかも数え方も誤っており、
「STUDY55=29 件」は異種キーの長さを足した値で、path+sha を持つ凍結項目は 13 件。
**探す場所と数え方の両方が誤っていた。**

**V2 が直した 3 点:**

1. **RETRO-0 の凍結 55 件を読込経路で走査する**(V1 は一度も触っていない)
2. **manifest 抽出をキー名非依存の再帰にした。**V1 は固定キー
   (`files`/`results`/`design`/`code`)しか見ず、STUDY55 manifest の
   `prereg_and_packets` を取りこぼしていた。**`freeze_guard_v1.py` が F-2 で
   同日に塞いだ穴と同型**であり、同じ変更セットの `instrument0_runner_guard_v1.py`
   では直したのに、隣の script で再発させた
3. **欠落と解析不能を FAIL にした。**V1 は `continue` で無言に飛ばしており、
   対象 0 件でも「全一致」を返しうる形だった

**加えて許容差を定数へ固定した。**V1 の `close(a, b, tol=...)` は呼び出し側が
上書きでき(実際 E4 で 1e-12 → 1e-9 に広げていた)、prereg 段6 要件4 が禁じる
「**コードに存在する緩和経路**」そのものだった。V2 は引数を廃し、
**モジュール定数 2 本**にする。段3 で本 script ごと凍結されれば、値の変更は
差分に現れる。
"""
from __future__ import annotations

import hashlib
import json
import math
import statistics
import sys
import traceback
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H))
import instrument0_core_v1 as C          # noqa: E402

OUT = H / "INSTRUMENT0_STAGE2_PROXY_RESULT_V2.json"
PROXY = H / "STUDY56_MATCHED_COUNTERFACTUAL_RAW_V2.json"
ATLAS = H / "RETRO0_EVIDENCE_ATLAS_V4.json"
MANIFESTS = ("STUDY55_FREEZE_MANIFEST_V1.json",
             "STUDY55B_FREEZE_MANIFEST_V1.json",
             "STUDY57B_FREEZE_MANIFEST_V1.json")

# **許容差は定数。引数で上書きさせない。**prereg 段6 要件4。
# 用途は「core の出力 と statistics の独立再計算」の浮動小数点比較のみであり、
# 判定閾値ではない。NULL_scale は 1e-1 の桁で、以下はその 8〜9 桁下にある。
EQ_EXACT = 1e-12          # 中央値など、同一演算列を辿る量
EQ_MEAN = 1e-9            # 平均。加算順序が違うため丸めが 1 桁ぶん緩い

# **prereg V5 §0 が名指す出典。全件を実際に読んだ記録。**
# `10_control/prereg_source_reading_gate_v1.py` が commit 時に全件揃いを強制する。
# **V1 はこれを持たず、うち 1 件が当方の誤読の答えを書いていた。**
SOURCES_READ = [
    {"file": "FABLE_BLOCK_RULING_INSTRUMENT0_V1.json",
     "sha256": "802b799bb5a221d39872788734e880dc27907ebcf09085544ad78862192fc44c",
     "read_note": "**B11 が『RETRO-0 の凍結55件』と逐語で書いている。**"
                  "当方の段2 V1 の誤読の答えがここにあった。"
                  "また冒頭 count_discrepancy が『**実体から導出されない手書き数値**』"
                  "を失敗類型として名指しており、V1 の「STUDY55=29 件」は"
                  "まさにこれ。12 BLOCK は fail-closed で全て UNRESOLVED"},
    {"file": "FABLE_V4_PRECHECK_V1.json",
     "sha256": "bd267e47255a434dc4075f1cc48d52f7203e593e4f2098a2dc1b61cea581b783",
     "read_note": "endpoint_ruling が E4 を『**slug 内平均を連続 score**』と固定"
                  "(本 script P4 の E4 実装がこれに従う)。SESOI は `ge`。"
                  "missing_decisions 10 件のうち cohort V3 承認は済んでいる"},
    {"file": "FABLE_V4_RECONCILIATION_V1.json",
     "sha256": "aa439855308860fd3cf98db92a05626d3fa5e1817bd323471ed8cf5b8177c32a",
     "read_note": "R03 が split-half 6435 全列挙・k=6114 を、R04 が置換 null の"
                  "3 要件を、R05 が NULL_scale=0 → UNDEFINED を定めている"
                  "(本 script P5 がこれらを検査する)。**verdict_note が"
                  "『封印・実行の許可ではない。B9/B10 実装 + 十分性査読システム"
                  "3 件 + 封印前 BLOCK 解消判定が別途必要』と明記**"},
]

CHECKS = []


def chk(cid, ok, what, got=None, want=None):
    CHECKS.append({"id": cid, "verdict": "PASS" if ok else "FAIL",
                   "what": what, "got": got, "expected": want})
    return ok


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def eq(a, b) -> bool:
    if a is None or b is None:
        return a is b
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= EQ_EXACT


def eq_mean(a, b) -> bool:
    if a is None or b is None:
        return a is b
    return math.isfinite(a) and math.isfinite(b) and abs(a - b) <= EQ_MEAN


def manifest_targets(man: Path):
    """**キー名非依存の再帰抽出。**固定キー方式は対象 0 件を全一致と誤る。"""
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


def _rel(p: Path) -> str:
    """**H からの相対パスで記録する。**2026-08-17 修理: 旧版は `p.name` で記録し
    下位 dir を落としていた(eval/base_drafts.jsonl が基名になり、参照の
    自己解決性を損なう)。R6 監査の列挙欠陥 — 数値・判定への影響は無い。"""
    try:
        return p.resolve().relative_to(H).as_posix()
    except ValueError:
        return p.name


def read_path_probe(p: Path, want_sha=None) -> dict:
    """**読込経路のみ。**存在しない・解析できない・SHA が違うは、いずれも失敗。"""
    if not p.exists():
        return {"state": "MISSING", "path": _rel(p)}
    try:
        if p.suffix.lower() == ".jsonl":
            n = 0
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    json.loads(line)
                    n += 1
            got = {"state": "OK", "kind": "jsonl", "n_lines": n}
        elif p.suffix.lower() in (".json",):
            d = json.loads(p.read_text(encoding="utf-8"))
            got = {"state": "OK", "kind": "json",
                   "n_top": len(d) if isinstance(d, (dict, list)) else 1}
        else:
            b = p.read_bytes()
            got = {"state": "OK", "kind": "bytes", "n_bytes": len(b)}
    except Exception as e:                                   # noqa: BLE001
        return {"state": "PARSE_FAIL", "path": _rel(p), "error": str(e)[:160]}
    got["path"] = _rel(p)
    got["sha256"] = sha(p)
    if want_sha and got["sha256"] != want_sha:
        got["state"] = "SHA_MISMATCH"
        got["recorded"] = want_sha
    return got


# ------------------------------------------------- P0 RETRO-0 凍結 55 件

def p0_retro55() -> dict:
    """**prereg が名指す代理そのもの。**読込経路のみ(条文の制限)。"""
    rec = {"phase": "P0_RETRO0凍結55件_読込経路のみ",
           "referent_evidence": {
               "prereg_v3_line": "本試験での代理データ: "
                                 "**RETRO-0 で既に閲覧済みの凍結 55 件**",
               "enumeration": "RETRO0_EVIDENCE_ATLAS_V4.json の rows",
               "ruling": "FABLE_BLOCK_RULING_INSTRUMENT0_V1.json B11"}}
    if not ATLAS.exists():
        chk("P0-0", False, "RETRO-0 atlas が実在する", "無い", "在る")
        return rec
    a = json.loads(ATLAS.read_text(encoding="utf-8"))
    rows = a.get("rows") or []
    rec["atlas"] = {"file": ATLAS.name, "sha256": sha(ATLAS),
                    "n_artifacts": a.get("n_artifacts"), "n_rows": len(rows)}
    chk("P0-1", a.get("n_artifacts") == 55 and len(rows) == 55,
        "**凍結 55 件の列挙が 55 行である**",
        {"n_artifacts": a.get("n_artifacts"), "rows": len(rows)},
        {"n_artifacts": 55, "rows": 55})

    probes, bad = [], []
    for r in rows:
        pr = read_path_probe(H / r["path"], r.get("current_sha256"))
        pr["study"] = r.get("study")
        pr["atlas_integrity"] = r.get("integrity")
        probes.append(pr)
        if pr["state"] != "OK":
            bad.append(pr)
    rec["probes"] = probes
    rec["failed"] = bad
    chk("P0-2", not bad,
        "**55 件すべてが読込経路を例外なく通り、atlas 記録の SHA と一致する**"
        "(**欠落・解析不能・SHA 不一致はいずれも失敗。無言で飛ばさない**)",
        [{"path": b["path"], "state": b["state"]} for b in bad], [])
    return rec


# ------------------------------------------------------------ P1 読込

def p1_load():
    rec = {"phase": "P1_読込経路", "primary": {}, "load_only": []}
    d = json.loads(PROXY.read_text(encoding="utf-8"))
    rec["primary"] = {"file": PROXY.name, "sha256": sha(PROXY),
                      "schema": d.get("schema"), "n_rows": len(d["rows"])}
    chk("P1-1", d.get("schema") == "mythos.study56_v2_raw.v1",
        "代理 raw の schema", d.get("schema"), "mythos.study56_v2_raw.v1")
    chk("P1-2", len(d["rows"]) == 87, "代理 raw の行数", len(d["rows"]), 87)

    for mn in MANIFESTS:
        mp = H / mn
        if not mp.exists():
            chk("P1-M:" + mn, False, "freeze manifest の実在", "無い", "在る")
            continue
        tg = manifest_targets(mp)          # **キー名非依存**
        probes, bad = [], []
        for rel, want in tg:
            pr = read_path_probe(mp.parent / rel, want)
            probes.append(pr)
            if pr["state"] != "OK":
                bad.append(pr)
        rec["load_only"].append(
            {"manifest": mn, "manifest_sha256": sha(mp),
             "n_targets": len(tg), "n_ok": len(tg) - len(bad),
             "extraction": "**キー名非依存の再帰。**V1 の固定キー方式は "
                           "prereg_and_packets を取りこぼしていた",
             "scope": "**読込経路のみ。集約・除外・null へは通さない**",
             "failed": bad, "probes": probes})
        chk("P1-L:" + mn, (not bad) and len(tg) > 0,
            "凍結物を全件読込(欠落・解析不能・SHA 不一致は失敗)",
            {"n": len(tg), "bad": [b["path"] for b in bad]},
            {"bad": []})
    return rec, d


# ------------------------------------------------------------ P2 適合

ARM = {"GOLD_TRUE": "TRUE", "GOLD_SWAP": "SWAP", "STYLE_ONLY": "STYLE"}


def p2_adapt(d: dict):
    items = {a: [] for a in ARM.values()}
    for i, r in enumerate(d["rows"]):
        for src, arm in ARM.items():
            v = r[src]
            items[arm].append({
                "slug": r["slug"], "item_id": "%s:%03d" % (r["checkpoint"], i),
                "checkpoint": r["checkpoint"],
                "value_mean_nll": v["mean_nll"],
                "value_loss_sum": v["loss_sum"], "n_tokens": v["n_tokens"]})
    slugs = sorted({r["slug"] for r in d["rows"]})
    chk("P2-1", len(slugs) == C.N_SLUGS_EXPECTED,
        "slug 数(null 全列挙の前提)", len(slugs), C.N_SLUGS_EXPECTED)
    ids = [it["item_id"] for it in items["TRUE"]]
    chk("P2-2", len(ids) == len(set(ids)), "item_id の一意性",
        {"n": len(ids), "unique": len(set(ids))}, "一致")
    per_ck = {}
    for r in d["rows"]:
        per_ck[r["checkpoint"]] = per_ck.get(r["checkpoint"], 0) + 1
    chk("P2-3", set(per_ck.values()) == {29},
        "**同一 29 item**(prereg 逐語。schema 一致は要求されない)",
        per_ck, "各 checkpoint 29")
    return ({"phase": "P2_適合", "arm_mapping": ARM, "n_slugs": len(slugs),
             "rows_per_checkpoint": per_ck}, items, slugs)


# ------------------------------------------------------------ P3 除外

def as_core_items(rows, endpoint: str):
    return [{"slug": it["slug"], "item_id": it["item_id"],
             "value": it["value_loss_sum"] if endpoint == "E1"
                      else it["value_mean_nll"],
             "n_tokens": it["n_tokens"]} for it in rows]


def p3_exclude(items) -> dict:
    rec = {"phase": "P3_除外", "per_endpoint": {},
           "denominator_note":
               "**率の分母は prereg の %d(29 item × 9 評価点)のまま。**"
               "代理は 29 × 3 = 87 なので**率自体は代理では解釈できない。**"
               "定数は変更しない — 変更は計器の改竄である"
               % C.EXCLUSION_DENOMINATOR}
    for ep in ("E1", "E2", "E3", "E4"):
        ci = as_core_items(items["TRUE"], ep)
        kept, dropped = C.exclude_items(ci, ep)
        by_slug = {it["slug"]: 0 for it in ci}
        for it in kept:
            by_slug[it["slug"]] += 1
        v = C.exclusion_verdict(len(dropped),
                                [s for s, n in by_slug.items() if n == 0])
        rec["per_endpoint"][ep] = {"n_kept": len(kept),
                                   "n_dropped": len(dropped), "verdict": v}
        chk("P3-%s" % ep, len(dropped) == 0 and v["verdict"] == "CONTINUE",
            "代理は非有限 0・n_tokens 全て >= %d のため除外 0" % C.E1_MIN_TOKENS,
            {"dropped": len(dropped), "verdict": v["verdict"]},
            {"dropped": 0, "verdict": "CONTINUE"})

    der = [dict(x) for x in as_core_items(items["TRUE"], "E2")]
    der[0]["value"] = float("nan")
    der[1]["value"] = float("inf")
    _k, d2 = C.exclude_items(der, "E2")
    chk("P3-DER-1",
        len(d2) == 2 and all(x["reason"] == "NON_FINITE_VALUE" for x in d2)
        and all(x["routed_to_row1"] is False for x in d2),
        "**[代理派生変種]** 非有限は除外経路のみに載り行1へ流れない",
        {"n": len(d2)}, {"n": 2})

    der1 = [dict(x) for x in as_core_items(items["TRUE"], "E1")]
    der1[0]["n_tokens"] = C.E1_MIN_TOKENS - 1
    _k, d3 = C.exclude_items(der1, "E1")
    chk("P3-DER-2",
        len(d3) == 1 and d3[0]["reason"] == "N_TOKENS_LT_%d" % C.E1_MIN_TOKENS,
        "**[代理派生変種]** E1 の n_tokens 下限で除外される",
        {"n": len(d3)}, {"n": 1})
    rec["derived_variant_note"] = (
        "**P3-DER-* は代理そのものの結果ではない。**代理では除外が 0 件のため"
        "分岐が走らない。分岐の意味論の証明は prereg 自身が段1 に割り当てている"
        "(B10-6・欠損/NaN・Inf・境界値)。本項は**追加**の検査であり、"
        "**代理の測定結果として引用してはならない**")
    return rec


# ------------------------------------------------------------ P4 集約

def p4_aggregate(items, slugs):
    grp = {}
    for it in items["TRUE"]:
        grp.setdefault(it["slug"], []).append(it)
    e1c, e1i, e4c, e4i, mdc, mdi = {}, {}, {}, {}, {}, {}
    for s in slugs:
        rows = grp[s]
        e1c[s] = C.slug_value(as_core_items(rows, "E1"), "E1")
        e1i[s] = statistics.median([r["value_loss_sum"] / r["n_tokens"]
                                    for r in rows])
        ci2 = as_core_items(rows, "E2")
        e4c[s] = C.slug_value(ci2, "E4")
        e4i[s] = statistics.fmean([r["value_mean_nll"] for r in rows])
        mdc[s] = C.slug_value(ci2, "E2")
        mdi[s] = statistics.median([r["value_mean_nll"] for r in rows])

    chk("P4-1", all(eq(e1c[s], e1i[s]) for s in slugs),
        "E1 の token 正規化中央値 = statistics.median の独立再計算(許容差は定数)",
        {s: e1c[s] for s in slugs[:2]}, {s: e1i[s] for s in slugs[:2]})
    chk("P4-2", all(eq_mean(e4c[s], e4i[s]) for s in slugs),
        "E4 の slug 内平均 = statistics.fmean の独立再計算(許容差は定数)",
        {s: e4c[s] for s in slugs[:2]}, {s: e4i[s] for s in slugs[:2]})
    chk("P4-3", all(eq(mdc[s], mdi[s]) for s in slugs),
        "既定 endpoint の中央値 = statistics.median の独立再計算",
        {s: mdc[s] for s in slugs[:2]}, {s: mdi[s] for s in slugs[:2]})
    pairs = [mdc[slugs[0]], mdc[slugs[1]]]
    chk("P4-4", eq(C.order_average(pairs), statistics.fmean(pairs)),
        "順序平均 = 独立平均", C.order_average(pairs), statistics.fmean(pairs))
    return ({"phase": "P4_集約",
             "tolerance_policy":
                 "**許容差はモジュール定数 EQ_EXACT=%r / EQ_MEAN=%r。**"
                 "引数で上書きできない。V1 は呼び出し側が広げられる形で、"
                 "prereg 段6 要件4 が禁じる緩和経路そのものだった"
                 % (EQ_EXACT, EQ_MEAN),
             "per_slug": {"E1": e1c, "E4": e4c, "median_default": mdc}}, mdc)


# ------------------------------------------------------------ P5 null

def p5_null(items, slugs, per_slug) -> dict:
    rec = {"phase": "P5_null構成"}
    sp = C.split_half_null(per_slug)
    rec["split_half"] = sp
    chk("P5-1", sp["n_splits"] == C.SPLIT_HALF_TOTAL,
        "split-half の全列挙数", sp["n_splits"], C.SPLIT_HALF_TOTAL)
    chk("P5-2", sp["p95_index_1origin"] == C.SPLIT_HALF_P95_INDEX
        and sp["method"] == "EXACT_FULL_ENUMERATION" and sp["seed_free"],
        "95% 点は 6114 番目の順序統計量・全列挙・seed 不要",
        sp["method"], "EXACT_FULL_ENUMERATION")

    grp = {a: {} for a in ("TRUE", "SWAP")}
    for a in ("TRUE", "SWAP"):
        for it in items[a]:
            grp[a].setdefault(it["slug"], []).append(it)
    per_arm = {s: {a: statistics.median([x["value_mean_nll"] for x in grp[a][s]])
                   for a in ("TRUE", "SWAP")} for s in slugs}

    pm = C.permutation_null(per_arm, "E2")
    rec["permutation_E2"] = pm
    chk("P5-3", pm["status"] == "TESTED"
        and pm["method"] == "EXACT_FULL_ENUMERATION"
        and pm["n_draws"] == (1 << len(slugs)),
        "腕対応のある endpoint は全列挙 2^16 で検査される",
        pm["n_draws"], 1 << len(slugs))
    for ep in ("E1", "E3"):
        p = C.permutation_null(per_arm, ep)
        rec["permutation_" + ep] = p
        chk("P5-4:" + ep, p["status"] == C.PERM_NOT_TESTED and p["median"] is None,
            "**構造的沈黙を合格に数えない。**E1/E3 は未検査を明示",
            p["status"], C.PERM_NOT_TESTED)

    ns_t = C.null_scale(pm, sp)
    ns_s = C.null_scale(C.permutation_null(per_arm, "E1"), sp)
    rec["null_scale"] = {"with_permutation": ns_t, "silent_endpoint": ns_s}
    chk("P5-5", eq(ns_s, sp["p95"]),
        "置換 null が未検査なら NULL_scale に寄与しない(沈黙を 0 として使わない)",
        ns_s, sp["p95"])
    chk("P5-6", eq(ns_t, max(abs(pm["median"]), sp["p95"])),
        "NULL_scale = max(|置換 null 中央値|, split-half 95% 点)",
        ns_t, max(abs(pm["median"]), sp["p95"]))

    vals = sorted(per_slug[s] for s in slugs)
    sep = vals[-1] - vals[0]
    adj = [(i, vals[i + 1] - vals[i]) for i in range(len(vals) - 1)]
    dv = C.derived(sep, ns_t, adj)
    rec["derived"] = dv
    chk("P5-7", dv["status"] == "DEFINED" and eq(dv["MDE"], ns_t * C.MDE_FACTOR),
        "MDE = NULL_scale × 2", dv.get("MDE"), ns_t * C.MDE_FACTOR)
    z = C.derived(sep, 0.0, adj)
    chk("P5-8", z["status"] == C.UNDEFINED and z["DR"] is None,
        "**NULL_scale が 0 なら UNDEFINED_ENDPOINT。**ε を入れない",
        z["status"], C.UNDEFINED)
    pb = C.practical_boundary(sep, None)
    chk("P5-9", pb["status"] == "NO_SESOI" and pb["meets"] is None,
        "SESOI 不在の endpoint は行5 経路", pb["status"], "NO_SESOI")
    return rec


# ------------------------------------------------------------ main

def main() -> int:
    print("**INSTRUMENT-0 段2 V2 — 代理データ互換試験**")
    print()
    stop, phases = None, []
    try:
        phases.append(p0_retro55())
        p1, d = p1_load()
        phases.append(p1)
        p2, items, slugs = p2_adapt(d)
        phases.append(p2)
        phases.append(p3_exclude(items))
        p4, per_slug = p4_aggregate(items, slugs)
        phases.append(p4)
        phases.append(p5_null(items, slugs, per_slug))
    except C.InstrumentStop as e:
        stop = {"class": "InstrumentStop", "message": str(e)}
    except Exception as e:                                   # noqa: BLE001
        stop = {"class": type(e).__name__, "message": str(e),
                "traceback": traceback.format_exc()[-1200:]}

    n_pass = sum(1 for c in CHECKS if c["verdict"] == "PASS")
    n_fail = len(CHECKS) - n_pass
    verdict = (C.STOP if (stop is not None or n_fail)
               else "STAGE2_PROXY_COMPATIBILITY_PASS")

    for c in CHECKS:
        print("  [%s] %-22s %s" % (c["verdict"], c["id"], c["what"][:62]))
    print()
    print("  **PASS %d / FAIL %d**" % (n_pass, n_fail))
    if stop:
        print("  **例外で停止: %s — %s**" % (stop["class"], stop["message"][:200]))
    print("  **判定: %s**" % verdict)

    OUT.write_bytes(json.dumps({
        "schema": "mythos.instrument0_stage2_proxy.v2",
        "stage": "段2 V2 — 代理データ互換試験(R14)",
        "supersedes": {
            "result": "INSTRUMENT0_STAGE2_PROXY_RESULT_V1.json",
            "script": "instrument0_stage2_proxy_v1.py",
            "status": "**INVALIDATED_BY_WRONG_REFERENT**",
            "record": "INSTRUMENT0_STAGE2_INVALIDATION_V1.json",
            "note": "**V1 が正しかったことにする操作ではない。V1 は消さない**"},
        "prereg": {"file": "PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md",
                   "sha256": sha(H / "PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md"),
                   "clause": "§11 段2"},
        "sources_read": SOURCES_READ,
        "sources_read_note":
            "**prereg §0 が名指す出典を全件読んだ記録。**"
            "V1 はこれを持たず、うち 1 件(FABLE_BLOCK_RULING_INSTRUMENT0_V1)が"
            "当方の誤読の答えを書いていた。"
            "`10_control/prereg_source_reading_gate_v1.py` が commit 時に強制する",
        "pass_condition_verbatim":
            "代理データに対し、読込・集約・除外・null 構成の全経路が例外なく走り、"
            "fixture 期待値と矛盾しないこと",
        "frozen_55_referent": {
            "resolved": "**RETRO-0 の凍結 55 件。**"
                        "`RETRO0_EVIDENCE_ATLAS_V4.json` の rows がその列挙",
            "evidence": ["PREREG_..._V3.md:236 「RETRO-0 で既に閲覧済みの凍結 55 件」",
                         "RETRO0_EVIDENCE_ATLAS_V1〜V4 いずれも n_artifacts=55",
                         "FABLE_BLOCK_RULING_INSTRUMENT0_V1.json B11 の逐語"],
            "v1_error": "**V1 は freeze manifest しか見ずに『55 件の列挙は無い』と"
                        "否定を主張した。**数え方も誤りで、「STUDY55=29 件」は"
                        "異種キーの長さの合計。path+sha を持つ凍結項目は 13 件"},
        "v2_repairs": [
            "**RETRO-0 凍結 55 件を読込経路で走査**(V1 は一度も触っていない)",
            "**manifest 抽出をキー名非依存の再帰に**"
            "(V1 は prereg_and_packets を取りこぼし。freeze_guard F-2 と同型の穴)",
            "**欠落・解析不能・SHA 不一致を FAIL に**(V1 は無言で飛ばしていた)",
            "**許容差をモジュール定数に固定**"
            "(V1 は引数で上書きでき、段6 要件4 が禁じる緩和経路だった)"],
        "verification_discipline":
            "**独立再計算で照合した。**core の返り値を core で読み直す照合は循環で、"
            "Paper B の B2 と同型の欠陥になる",
        "verdict": verdict, "n_pass": n_pass, "n_fail": n_fail,
        "instrument_stop": stop, "checks": CHECKS, "phases": phases,
        "no_repair_clause":
            "**段6 に従い、欠陥が出ても修理しない。**許容差の緩和・再試行の経路は"
            "本 script に存在しない(許容差は定数で、引数を持たない)",
    }, ensure_ascii=False, indent=1).encode("utf-8"))
    print("  written: %s" % OUT.name)
    return 0 if verdict == "STAGE2_PROXY_COMPATIBILITY_PASS" else 1


if __name__ == "__main__":
    sys.exit(main())

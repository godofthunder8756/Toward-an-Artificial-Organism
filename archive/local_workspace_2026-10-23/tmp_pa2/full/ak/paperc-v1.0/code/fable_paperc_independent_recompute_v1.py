# -*- coding: utf-8 -*-
r"""Fable 独立再計算(Paper C 査読 §3.A)。

**保存済み result JSON を計算入力に使わない。**261 raw 行 → item 値 → slug 内集約
→ 16 slug 等重み中央値 → 非順序 8/8 分割 6435 通り全列挙 → 6114 番目。
定義は prereg V5 §2.5 / §4 と原稿 §2.3〜2.6 の逐語による。集約器
(instrument0_stage5_aggregate_v1.py / runner / core)は import しない。
出力は比較用の dict と、result との突き合わせ結果。
"""
from __future__ import annotations

import hashlib
import itertools
import json
import math
import statistics
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
H = Path(__file__).resolve().parent
RAW = H / "INSTRUMENT0_STAGE5_RAW_V1.jsonl"
RESULT = H / "INSTRUMENT0_STAGE5_RESULT_V1.json"     # 突き合わせ「だけ」に使う
CEIL, FLOOR = -1.0, -20.0
DOSES = (0, 16, 32, 48, 64, 96, 128, 160, 192)


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def median(xs):
    return statistics.median(xs)          # 偶数長は中央 2 値の平均(R09)


def main() -> int:
    rows = [json.loads(l) for l in RAW.read_text(encoding="utf-8").splitlines() if l.strip()]
    assert len(rows) == 261, len(rows)
    stamps = {r["instrument_sha256"] for r in rows}
    assert len(stamps) == 1, "instrument 刻印が複数: %r" % stamps
    slugs = sorted({r["slug"] for r in rows})
    assert len(slugs) == 16, len(slugs)
    items = sorted({r["item_id"] for r in rows})
    assert len(items) == 29, len(items)
    doses = sorted({r["dose"] for r in rows})
    assert tuple(doses) == DOSES, doses
    by = {(r["dose"], r["item_id"]): r for r in rows}
    slug_of = {r["item_id"]: r["slug"] for r in rows}

    # ---- item 値 ----------------------------------------------------------
    def e1(r):   # NLL、token 正規化
        t = r["TRUE"]
        if t["n_tokens"] < 8:
            return None
        v = t["loss_sum"] / t["n_tokens"]
        return v if math.isfinite(v) else None

    def e2(r):   # d0 の TRUE 選好 = SWAP mean NLL − TRUE mean NLL
        t, s = r["TRUE"], r["SWAP"]
        v = s["loss_sum"] / s["n_tokens"] - t["loss_sum"] / t["n_tokens"]
        return v if math.isfinite(v) else None

    def e3(r):   # 末尾直後の停止質量
        v = r["TRUE"]["stop_mass"]
        return v if math.isfinite(v) else None

    def e4(r):   # 両順の正答 indicator の平均。order1 は A、order2 は B が正答
        o1, o2 = r["E4_order1"], r["E4_order2"]
        c1 = 1.0 if o1["logp_A"] > o1["logp_B"] else 0.0
        c2 = 1.0 if o2["logp_B"] > o2["logp_A"] else 0.0
        return 0.5 * (c1 + c2)

    # ---- E4 の位置バイアス実測(261/261) -----------------------------------
    a_o1 = sum(1 for r in rows if r["E4_order1"]["logp_A"] > r["E4_order1"]["logp_B"])
    a_o2 = sum(1 for r in rows if r["E4_order2"]["logp_A"] > r["E4_order2"]["logp_B"])
    e4_scores = {e4(r) for r in rows}

    # ---- slug 集約 ----------------------------------------------------------
    def slug_values(fn, dose, agg):
        """dose における slug → 集約値(agg = median / mean)。除外 item を数える。"""
        out, excluded = {}, 0
        for s in slugs:
            vals = []
            for it in items:
                if slug_of[it] != s:
                    continue
                v = fn(by[(dose, it)])
                if v is None:
                    excluded += 1
                else:
                    vals.append(v)
            out[s] = (agg(vals) if vals else None)
        return out, excluded

    def contrast_per_slug(fn, agg, item_level=False):
        """per-slug contrast。
        **prereg §4.1『d0 対 d192 の slug 中央値差』= slug 内集約(d192) − slug 内集約(d0)。**
        item_level=True は原稿 §2.3 の字面『item 値とし、d192 から d0 を引いた』の読み
        (item 差 → slug 内集約)。**両者は複数 item slug で値が異なる**(査読所見 A1)。"""
        vals, excl = {}, 0
        for s in slugs:
            if item_level:
                cs = []
                for it in items:
                    if slug_of[it] != s:
                        continue
                    a, b = fn(by[(192, it)]), fn(by[(0, it)])
                    if a is None or b is None:
                        excl += 1
                        continue
                    cs.append(a - b)
                vals[s] = agg(cs) if cs else None
            else:
                a = [fn(by[(192, it)]) for it in items if slug_of[it] == s]
                b = [fn(by[(0, it)]) for it in items if slug_of[it] == s]
                a = [x for x in a if x is not None]; b = [x for x in b if x is not None]
                excl += (sum(1 for it in items if slug_of[it] == s) - min(len(a), len(b)))
                vals[s] = (agg(a) - agg(b)) if (a and b) else None
        return vals, excl

    res = {}
    # 査読所見 A1: 原稿 §2.3 の字面読み(item 差→slug 集約)での値も併記する
    alt = {}
    for k, fn in (("E1", e1), ("E3", e3)):
        ca, _ = contrast_per_slug(fn, median, item_level=True)
        alt[k] = median([ca[s] for s in slugs])
    # E1
    c1, ex1 = contrast_per_slug(e1, median)
    res["E1"] = {"per_slug": c1, "excluded_items_in_contrast": ex1}
    # E2 (d0 のみ)
    v2, ex2 = slug_values(e2, 0, median)
    res["E2"] = {"per_slug": v2, "excluded_items_in_contrast": ex2}
    # E3
    c3, ex3 = contrast_per_slug(e3, median)
    res["E3"] = {"per_slug": c3, "excluded_items_in_contrast": ex3}
    # E4: slug 内平均 → d192−d0
    m0, _ = slug_values(e4, 0, statistics.fmean)
    m192, _ = slug_values(e4, 192, statistics.fmean)
    c4 = {s: m192[s] - m0[s] for s in slugs}
    res["E4"] = {"per_slug": c4, "excluded_items_in_contrast": 0}

    # ---- split-half 全列挙(6435 通り、先頭 slug を片側へ固定) ------------
    def split_half_p95(per_slug):
        vals = [per_slug[s] for s in slugs]
        first, rest = 0, list(range(1, 16))
        stats = []
        for comb in itertools.combinations(rest, 7):        # C(15,7)=6435
            g1 = [first] + list(comb)
            g2 = [i for i in range(16) if i not in g1]
            stats.append(abs(median([vals[i] for i in g1]) - median([vals[i] for i in g2])))
        assert len(stats) == 6435, len(stats)
        stats.sort()
        return stats[6114 - 1], len(stats)

    # ---- 置換 null(E2 のみ: slug 内 TRUE/SWAP 腕交換 = slug 値の符号反転、2^16 全列挙)
    def perm_null_median_e2(per_slug):
        vals = [per_slug[s] for s in slugs]
        meds = []
        for mask in range(1 << 16):
            signed = [(-v if (mask >> i) & 1 else v) for i, v in enumerate(vals)]
            meds.append(median(signed))
        return median(meds), len(meds)

    for k in ("E1", "E2", "E3", "E4"):
        per = res[k]["per_slug"]
        assert all(v is not None for v in per.values()), "全 item 除外 slug あり: %s" % k
        sep = median([per[s] for s in slugs])
        p95, n = split_half_p95(per)
        perm = None
        if k == "E2":
            perm, _ = perm_null_median_e2(per)
        null_scale = max(abs(perm) if perm is not None else 0.0, p95)
        res[k].update({"SEP_max": sep, "split_half_p95": p95, "n_partitions": n,
                       "perm_null_median": perm,
                       "NULL_scale": null_scale,
                       "DR": (abs(sep) / null_scale) if null_scale > 0 else None,
                       "MDE": (2 * null_scale) if null_scale > 0 else None})

    # ---- E3 飽和 guard: slug 中央値の中央値(d0 / d192) ----------------------
    s0, _ = slug_values(e3, 0, median)
    s192, _ = slug_values(e3, 192, median)
    e3_d0 = median([s0[s] for s in slugs])
    e3_d192 = median([s192[s] for s in slugs])
    res["E3"]["d0_median_of_slug_medians"] = e3_d0
    res["E3"]["d192_median_of_slug_medians"] = e3_d192
    res["E3"]["guard_d0_in_open_interval"] = FLOOR < e3_d0 < CEIL
    res["E3"]["d192_exceeds_ceiling"] = e3_d192 >= CEIL

    # ---- 分岐(§6 を上から) --------------------------------------------------
    expect_sign = {"E1": -1, "E2": +1, "E3": +1, "E4": +1}

    def classify(k):
        r = res[k]
        if r["NULL_scale"] == 0 or not math.isfinite(r["NULL_scale"]):
            # 行3.5 より前に行1〜3 を評価するが、E4 は非有限/除外なし・飽和条件(比率型)は
            # per-slug 0.5 が「k==0 or k==n」でない → 行3.5
            return "UNDEFINED_ENDPOINT", 3.5
        sep, ns = r["SEP_max"], r["NULL_scale"]
        if expect_sign[k] * sep < 0 and abs(sep) > ns:
            return "SEPARATES_WRONG_DIRECTION", 2.5
        if k == "E3" and r["d192_exceeds_ceiling"]:
            return "FAILED_FLOOR_CEILING", 3
        dr = r["DR"]
        null_silent = (k == "E2")     # 置換 null を検査したのは E2 だけ。E1/E3/E4 は構造的未検査
        if dr >= 3 and null_silent:
            return "VALIDATED_BUT_PRACTICAL_BASIS_MISSING", 5   # SESOI 不在(E1/E2/E4)
        if dr >= 3 and not null_silent:
            return "OUT_OF_TABLE(INSTRUMENT_STOP)", None          # 行4/5 は null 沈黙を要求、行7/8 は DR<3
        if 1 <= dr < 3:
            return "WEAK", 7
        return "NOT_SEPARABLE", 8

    for k in ("E1", "E2", "E3", "E4"):
        res[k]["verdict"], res[k]["row"] = classify(k)

    # ---- 突き合わせ(ここで初めて result を読む) ---------------------------
    R = json.loads(RESULT.read_text(encoding="utf-8"))["endpoints"]
    diffs = []
    for k in ("E1", "E2", "E3", "E4"):
        for mine, theirs in (("SEP_max", "sep_max"), ("NULL_scale", "null_scale"),
                             ("split_half_p95", "split_half_p95")):
            a, b = res[k][mine], R[k].get(theirs)
            if not (a == b or (a is not None and b is not None and math.isclose(a, b, rel_tol=0, abs_tol=1e-12))):
                diffs.append((k, mine, a, b))
        for mine in ("DR", "MDE"):
            a, b = res[k][mine], R[k].get("derived", {}).get(mine)
            if not (a == b or (a is not None and b is not None and math.isclose(a, b, rel_tol=0, abs_tol=1e-12))):
                diffs.append((k, mine, a, b))
        vt = R[k]["verdict"]["verdict"]
        if res[k]["verdict"].split("(")[0].replace("OUT_OF_TABLE", "INSTRUMENT_STOP") != vt:
            diffs.append((k, "verdict", res[k]["verdict"], vt))

    print("=== Fable 独立再計算(raw → 値)===")
    for k in ("E1", "E2", "E3", "E4"):
        r = res[k]
        print("  %s SEP=%r  sh95=%r  perm=%r  NULL=%r  DR=%r  MDE=%r  → %s (row %s)  excl=%d"
              % (k, r["SEP_max"], r["split_half_p95"], r["perm_null_median"], r["NULL_scale"],
                 r["DR"], r["MDE"], r["verdict"], r["row"], r["excluded_items_in_contrast"]))
    print("  E3 slug-median-of-medians d0=%r d192=%r guard_d0=%s d192≥ceil=%s"
          % (e3_d0, e3_d192, res["E3"]["guard_d0_in_open_interval"], res["E3"]["d192_exceeds_ceiling"]))
    print("  E4 位置バイアス: order1 A>B %d/261, order2 A>B %d/261, item score 集合=%s"
          % (a_o1, a_o2, sorted(e4_scores)))
    print("\n=== result との突き合わせ(abs_tol 1e-12)===")
    if diffs:
        for d in diffs:
            print("  **不一致** %s %s mine=%r result=%r" % d)
    else:
        print("  **全一致(SEP/NULL/sh95/DR/MDE × 4 endpoint + verdict × 4)**")
    out = {
        "schema": "mythos.fable_paperc_independent_recompute.v1",
        "amendment_class": "NOT_AN_AMENDMENT",
        "not_an_amendment_reason": "査読用の独立再計算受領書",
        "issued_by": "FABLE",
        "inputs": {"raw": RAW.name, "raw_sha256": sha(RAW), "n_rows": 261,
                   "instrument_stamp": next(iter(stamps))},
        "did_not_use_saved_result_as_input": True,
        "did_not_import_aggregator_or_runner": True,
        "e4_position_bias": {"order1_A_over_B": a_o1, "order2_A_over_B": a_o2, "denominator": 261,
                             "item_score_set": sorted(e4_scores)},
        "endpoints": {k: {kk: vv for kk, vv in res[k].items() if kk != "per_slug"} for k in res},
        "reading_A1_item_level_difference_then_slug_median": {
            "note": "原稿 §2.3『item 値とし、d192 から d0 を引いた』の字面どおりに item 差→slug 中央値で"
                    "計算した SEP_max。**prereg §4.1 と凍結 result は slug 集約→差である。**"
                    "複数 item slug(9/16)で値が変わる。verdict は両読みで不変",
            "E1_SEP_max": alt["E1"], "E3_SEP_max": alt["E3"]},
        "diffs_vs_frozen_result": diffs,
        "all_match": not diffs,
        "declared_at": "2026-08-18",
    }
    (H / "FABLE_PAPERC_INDEPENDENT_RECOMPUTE_V1.json").write_bytes(
        json.dumps(out, ensure_ascii=False, indent=1).encode("utf-8"))
    return 0 if not diffs else 1


if __name__ == "__main__":
    sys.exit(main())

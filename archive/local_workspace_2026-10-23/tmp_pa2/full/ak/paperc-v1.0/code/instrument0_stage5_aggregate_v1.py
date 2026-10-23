# -*- coding: utf-8 -*-
r"""段5 集約・分岐適用・scorecard。**凍結済み関数(core / runner)の合成のみ。**

§4.1 逐語: SEP_max = d0 対 d192 の slug 中央値差(E2 は d0 の選好そのもの)。
NULL_scale = max(|置換 null 中央値|, split-half 95% 点)。DR = |SEP_max|/NULL_scale。
MIN_STEP = 隣接 dose 対のうち |差| > NULL_scale の最小用量差。

**置換 null は E2 のみ「検査した」と数える**(§4.3 の 3 要件の記載構成を持つのは
E2 の腕交換のみ。E1/E3 は構造的、E4 は要件 1-2 の条文構成が無いため
`PERMUTATION_NULL_STRUCTURALLY_NOT_TESTED`)。**構造的沈黙は null 沈黙に数えない** —
その帰結が行外 STOP なら、それが測定結果である(Opus 所見・開示義務)。
"""
from __future__ import annotations

import hashlib
import json
import statistics
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
H = Path(__file__).resolve().parent
sys.path.insert(0, str(H))
import instrument0_core_v1 as C            # noqa: E402
import instrument0_runner_v1 as R          # noqa: E402
import instrument0_runner_guard_v1 as G    # noqa: E402

RAW = H / "INSTRUMENT0_STAGE5_RAW_V1.jsonl"
OUT = H / "INSTRUMENT0_STAGE5_RESULT_V1.json"
DOSES = list(R.DOSES)


def sha_file(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main() -> int:
    rows = [json.loads(l) for l in RAW.read_text(encoding="utf-8").splitlines()
            if l.strip()]
    # B9 要件3: 刻印検証(集計器の入口)
    runner_sha = sha_file(H / "instrument0_runner_v1.py")
    fil = G.filter_valid_raws(rows, runner_sha)
    if fil["n_dropped"]:
        raise C.InstrumentStop("**刻印 INVALID の raw がある: %d 件**"
                               % fil["n_dropped"])
    if len(rows) != 261:
        raise C.InstrumentStop("**raw が 261 行でない: %d**" % len(rows))

    slugs = sorted({r["slug"] for r in rows})
    by = {}
    for r in rows:
        by.setdefault((r["dose"], r["slug"]), []).append(r)

    def item_values(endpoint):
        """261 item の (slug,item_id,value,n_tokens)。除外は core に委ねる。"""
        out = []
        for r in rows:
            if endpoint == "E1":
                v, nt = r["TRUE"]["loss_sum"], r["TRUE"]["n_tokens"]
            elif endpoint == "E2":
                v, nt = r["SWAP"]["mean_nll"] - r["TRUE"]["mean_nll"], r["TRUE"]["n_tokens"]
            elif endpoint == "E3":
                v, nt = r["TRUE"]["stop_mass"], r["TRUE"]["n_tokens"]
            else:
                s = R.e4_item_score(
                    {"correct": r["E4_order1"]["logp_A"], "wrong": r["E4_order1"]["logp_B"]},
                    {"correct": r["E4_order2"]["logp_B"], "wrong": r["E4_order2"]["logp_A"]})
                v, nt = s["item_score"], r["TRUE"]["n_tokens"]
            out.append({"slug": r["slug"], "item_id": r["item_id"],
                        "dose": r["dose"], "value": v, "n_tokens": nt})
        return out

    def slug_dose_value(items, endpoint, dose):
        per = {}
        for s in slugs:
            sub = [{"slug": s, "item_id": it["item_id"], "value": it["value"],
                    "n_tokens": it["n_tokens"]}
                   for it in items if it["slug"] == s and it["dose"] == dose]
            per[s] = C.slug_value(sub, endpoint)
        return per

    sesoi_rec = json.loads((H / "INSTRUMENT0_SESOI_MDE_PREFIX_V1.json"
                            ).read_text(encoding="utf-8"))
    result = {"schema": "mythos.instrument0_stage5_result.v1",
              "amendment_class": "NOT_AN_AMENDMENT",
              "not_an_amendment_reason": "段5 の集約・分岐結果",
              "prereg": {"file": "PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md",
                         "sha256": sha_file(H / "PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md"),
                         "clause": "§4 / §6 / §11 段5"},
              "sources_read": [
                  {"file": "FABLE_BLOCK_RULING_INSTRUMENT0_V1.json",
                   "sha256": sha_file(H / "FABLE_BLOCK_RULING_INSTRUMENT0_V1.json"),
                   "read_note": "B2/B3 の null・MDE 体系を §4 実装の根拠に"},
                  {"file": "FABLE_V4_PRECHECK_V1.json",
                   "sha256": sha_file(H / "FABLE_V4_PRECHECK_V1.json"),
                   "read_note": "E4 の slug 内平均・tie 恒久規則"},
                  {"file": "FABLE_V4_RECONCILIATION_V1.json",
                   "sha256": sha_file(H / "FABLE_V4_RECONCILIATION_V1.json"),
                   "read_note": "R03-R06(split-half 全列挙・MDE=2×NULL_scale)"},
              ],
              "raw": {"file": RAW.name, "sha256": sha_file(RAW),
                      "n_rows": len(rows), "stamp": "261/261 VALID"},
              "aggregator": {"file": Path(__file__).name,
                             "sha256": sha_file(H / Path(__file__).name),
                             "note": "**凍結済み core/runner の合成のみ。**"
                                     "新しい規則を作らない"},
              "endpoints": {}}

    verdicts = {}
    for ep in ("E1", "E2", "E3", "E4"):
        items = item_values(ep)
        kept, dropped = C.exclude_items(
            [{"slug": i["slug"], "item_id": i["item_id"], "value": i["value"],
              "n_tokens": i["n_tokens"]} for i in items], ep)
        by_slug_count = {s: 0 for s in slugs}
        for it in kept:
            by_slug_count[it["slug"]] += 1
        excl = C.exclusion_verdict(len(dropped),
                                   [s for s, n in by_slug_count.items() if n == 0])
        kept_ids = {(it["slug"], it["item_id"]) for it in kept}
        items = [i for i in items if (i["slug"], i["item_id"]) in kept_ids]

        vals = {d: slug_dose_value(items, ep, d) for d in DOSES}
        if ep == "E2":
            per_slug_contrast = dict(vals[0])                      # d0 選好そのもの
        else:
            per_slug_contrast = {s: vals[192][s] - vals[0][s] for s in slugs}

        sep_max = statistics.median(per_slug_contrast.values())
        sp = C.split_half_null(per_slug_contrast)
        if ep == "E2":
            per_arm = {}
            for s in slugs:
                t = [r["TRUE"]["mean_nll"] for r in rows
                     if r["slug"] == s and r["dose"] == 0]
                w = [r["SWAP"]["mean_nll"] for r in rows
                     if r["slug"] == s and r["dose"] == 0]
                per_arm[s] = {"TRUE": -statistics.median(t),
                              "SWAP": -statistics.median(w)}
            pm = C.permutation_null(per_arm, ep)
        else:
            pm = C.permutation_null({}, "E1")      # 構造的 NOT_TESTED を明示出力
        ns = C.null_scale(pm, sp)
        adj = [(DOSES[i + 1] - DOSES[i],
                statistics.median([vals[DOSES[i + 1]][s] - vals[DOSES[i]][s]
                                   for s in slugs]))
               for i in range(len(DOSES) - 1)]
        dv = C.derived(sep_max, ns, adj)

        # 飽和(§6.1)
        saturated, sat_detail = False, {}
        if ep == "E3":
            base = statistics.median(vals[0].values())      # A1: slug 間も median
            g = R.saturation_e3(base)
            sat_detail["guard"] = g
            d192v = statistics.median(vals[192].values())
            sat_detail["d192_median_vs_ceiling"] = {"d192": d192v, "ceiling": -1.0,
                                                    "saturated_high": d192v >= -1.0}
            saturated = d192v >= -1.0
            guard_stop = g["verdict"] == C.STOP
        else:
            guard_stop = False
        if ep == "E4":
            for d in (0, 192):
                k = sum(1 for r in rows if r["dose"] == d
                        for o, key in (("E4_order1", ("logp_A", "logp_B")),
                                       ("E4_order2", ("logp_B", "logp_A")))
                        if r[o][key[0]] > r[o][key[1]])
                n = 2 * sum(1 for r in rows if r["dose"] == d)
                sat_detail["d%d" % d] = {"k": k, "n": n,
                                         **R.saturation_ratio(k, n)}
            saturated = any(v.get("saturated") for v in sat_detail.values())

        null_silent = (pm.get("status") == "TESTED"
                       and abs(pm.get("median") or 0.0) < abs(sep_max))
        null_fires = (pm.get("status") == "TESTED"
                      and abs(pm.get("median") or 0.0) >= abs(sep_max))
        sesoi = None
        if ep == "E3":
            flat = json.dumps(sesoi_rec, ensure_ascii=False)
            sesoi = sesoi_rec.get("E3_sesoi") or sesoi_rec.get("sesoi", {}).get("E3")
        mde_le = None
        if ep == "E3" and sesoi is not None and dv.get("MDE") is not None:
            mde_le = dv["MDE"] <= sesoi

        ev = {"stop_row1": bool(excl["verdict"] == C.STOP or guard_stop),
              "null_fires_at_equality": bool(null_fires),
              "sep_max": sep_max, "null_scale": ns,
              "expected_sign": {"E1": -1, "E2": 1, "E3": 1, "E4": 1}[ep],
              "saturated": bool(saturated), "DR": dv.get("DR"),
              "null_silent": bool(null_silent), "mde_le_sesoi": mde_le}
        try:
            v = R.classify(ep, ev)
        except C.InstrumentStop as e:
            v = {"row": None, "verdict": C.STOP,
                 "why": "**§6 のどの行にも該当しない(行外)** — "
                        "E1/E3/E4 の構造的置換沈黙は null 沈黙に数えない条文"
                        "(§4.3)と行4/5 の沈黙要件の未閉部が実データで露出した。"
                        "Opus が段4 で予測所見として先に記録している",
                 "detail": str(e)[:200]}
        result["endpoints"][ep] = {
            "exclusion": excl, "per_slug_contrast": per_slug_contrast,
            "sep_max": sep_max, "split_half_p95": sp["p95"],
            "permutation": {k: pm[k] for k in ("status", "median") if k in pm},
            "null_scale": ns, "derived": dv, "saturation": sat_detail,
            "sesoi": sesoi, "verdict": v}
        verdicts[ep] = v.get("verdict") if v.get("row") is None else \
            "row %s: %s" % (v["row"], v["verdict"])
        print("  %s: SEP=%+.5f  NULL=%.5f  DR=%s  → %s"
              % (ep, sep_max, ns,
                 ("%.2f" % dv["DR"]) if dv.get("DR") else dv.get("status"),
                 verdicts[ep]))

    # scorecard(封印予測との照合)
    sc = {}
    for name, f in (("FABLE", "STAGE4_PREDICTION_FABLE_V1.json"),
                    ("OPUS", "STAGE4_PREDICTION_OPUS_V1.json")):
        t = json.loads((H / f).read_text(encoding="utf-8"))
        per = {}
        for ep in ("E1", "E2", "E3", "E4"):
            v = result["endpoints"][ep]["verdict"]
            row = str(v.get("row")) if v.get("row") is not None else "OUT_OF_TABLE"
            p = t["predictions"][ep].get(row.replace(".0", ""), 0.0) \
                if row != "OUT_OF_TABLE" else 0.0
            per[ep] = {"realized_row": row, "predicted_p": p}
        sc[name] = {"ticket_sha256": sha_file(H / f), "per_endpoint": per}
    result["scorecard"] = sc
    result["scorecard_note"] = ("**行外(OUT_OF_TABLE)は両予測者とも確率 0 扱い。**"
                                "分岐表が観測空間を覆っていなかったことは"
                                "scorecard ではなく計器の欠陥記録に属する")
    result["claim_ceiling"] = [
        "**本結果は計器の検証であり、蒸留効果の主張ではない**",
        "単一モデル(4B)・単一 seed 系列・29 item",
        "E1/E3/E4 の置換 null は構造的に未検査。null 沈黙に数えていない",
        "行外 STOP が出た endpoint は、行4/5 の沈黙要件と §4.3 の未閉部が原因。"
        "**修理は新 version + 操作者授権を要し、本記録では行わない**",
    ]
    result["declared_at"] = "2026-08-17"
    OUT.write_bytes(json.dumps(result, ensure_ascii=False, indent=1).encode("utf-8"))
    print("written:", OUT.name, sha_file(OUT)[:16])
    return 0


if __name__ == "__main__":
    sys.exit(main())

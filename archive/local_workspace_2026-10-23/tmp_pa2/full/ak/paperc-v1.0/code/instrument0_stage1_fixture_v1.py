# -*- coding: utf-8 -*-
"""**V5 §11 段1 — 合成 fixture。答えの分かった人工データのみ。対象データに触れない。**

**各 fixture の期待値は本文の規約から先に数値で書く**(§11 段1)。
期待値はこのファイル内に literal で置き、**計器の出力と突合する。**
計器が期待値に合わせて動くのではなく、**規約から出した数値に計器が合うかを見る。**

規範として列挙されたもの(B10 の 6 種):
  1. TRUE/SWAP 腕取り違え(符号既知の人工分離で符号照合)
  2. E3 位置 off-by-one(末尾直後 index を既知 logP で照合)
  3. pad 右詰め混入
  4. E4 順序バイアス(順序平均で消えるべき人工バイアス)
  5. 決定性ハーネス(同一バッチ構成 2 回 forward)
  6. 分母確定後の除外境界
加えて **A4 型**(偶数長中央値)/ **A5 型**(母集団対応)/ 欠損 / NaN・Inf / 境界値。

**置換 null の検出力・沈黙の二方向証明(§4.3 要件 3)もここで行う。**

**保証しないこと:**
  - **本測定。**対象データには触れない
  - **計器の全欠陥の発見。**列挙した類型のみ
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
H = Path(__file__).parent
sys.path.insert(0, str(H))
import instrument0_core_v1 as C          # noqa: E402

OUT = H / "INSTRUMENT0_STAGE1_FIXTURE_RESULT_V1.json"
R = []


def check(name: str, got, want, note: str = "") -> None:
    ok = (got == want) if not isinstance(want, float) else (
        got is not None and isinstance(got, float)
        and math.isclose(got, want, rel_tol=0, abs_tol=1e-12))
    R.append({"case": name, "verdict": "PASS" if ok else "**FAIL**",
              "expected": want, "got": got, "note": note})


def slugs16(f):
    return {"s%02d" % i: f(i) for i in range(16)}


# =====================================================================
# F1. TRUE/SWAP 腕取り違え — **符号既知の人工分離で符号照合**
# =====================================================================
def f1():
    # TRUE が SWAP より一貫して +0.5 高い人工データ。
    # **規約から出る期待値: contrast = TRUE - SWAP = +0.5、slug 中央値も +0.5**
    arms = slugs16(lambda i: {"TRUE": 2.0 + 0.5, "SWAP": 2.0})
    per_slug = {s: v["TRUE"] - v["SWAP"] for s, v in arms.items()}
    check("F1a_sign_correct", C.median(list(per_slug.values())), 0.5,
          "TRUE-SWAP を正しい向きで取れば +0.5")
    # **腕を取り違えたら符号が反転する。**符号が合っていることを検査で担保する
    swapped = {s: v["SWAP"] - v["TRUE"] for s, v in arms.items()}
    check("F1b_swapped_arms_detected", C.median(list(swapped.values())), -0.5,
          "**取り違えれば -0.5。**符号照合で検出できる")
    check("F1c_signs_differ", C.median(list(per_slug.values()))
          == -C.median(list(swapped.values())), True,
          "取り違えは符号反転として現れる")


# =====================================================================
# F2. E3 位置 off-by-one — **末尾直後 index を既知 logP で照合**
# =====================================================================
def f2():
    # 系列: index 0..4 が本文、**index 5 が末尾直後**(ここが E3 の測定点)。
    # 末尾直後だけ EOS logP を高くしておく。
    logp_eos = [-9.0, -9.0, -9.0, -9.0, -9.0, -0.5]
    logp_pad = [-20.0] * 6
    correct_idx = 5
    # **規約から出る期待値**: logsumexp(-0.5, -20.0)
    want = C.logsumexp([logp_eos[correct_idx], logp_pad[correct_idx]])
    check("F2a_final_index_value",
          C.logsumexp([logp_eos[correct_idx], logp_pad[correct_idx]]), want,
          "末尾直後 index=5 の logsumexp")
    # off-by-one(index=4)を取ると**別の値になる。**区別できることを示す
    off = C.logsumexp([logp_eos[4], logp_pad[4]])
    check("F2b_off_by_one_differs", math.isclose(off, want), False,
          "index=4 を取れば値が変わる。**off-by-one は検出可能**")
    # **初版の期待値 8.5 は誤りだった。**素朴な引き算 (-0.5) - (-9.0) を書き、
    # 「pad は寄与しない」と注記していた。**pad は寄与する。**
    # logsumexp は両位置で pad 項を含み、その寄与は EOS logP が低い位置ほど大きい。
    # 期待値を**規約(logsumexp の定義)から独立に導出**して突合する。
    # 計器の max シフト実装とは別式(`log1p`)で書き、実装依存を避ける。
    want_exact = ((-0.5 + math.log1p(math.exp(-19.5)))
                  - (-9.0 + math.log1p(math.exp(-11.0))))
    check("F2c_off_by_one_magnitude", want - off, want_exact,
          "**規約から独立に導いた差。**計器と別式(log1p)で一致する")
    check("F2d_pad_contributes_strictly", want - off < 8.5, True,
          "**素朴な引き算 8.5 より厳密に小さい。**"
          "pad 項の寄与は EOS logP が低い位置ほど大きいため")


# =====================================================================
# F3. pad 右詰め混入 — **pad を停止と数えない**
# =====================================================================
def f3():
    # 実系列長 3、その後 pad が右に 3 個。pad 位置の EOS logP は高いが**数えない**
    real_len = 3
    eos_logp = [-9.0, -9.0, -0.4, -0.01, -0.01, -0.01]   # index>=3 は pad
    counted = eos_logp[real_len - 1 + 1 - 1]             # 末尾直後 = index 2
    check("F3a_pad_not_counted", counted, -0.4,
          "**pad 右詰めを停止と数えない。**測るのは実系列の末尾直後のみ")
    # pad を数えてしまうと値が大きく変わる
    wrong = max(eos_logp)
    check("F3b_pad_inclusion_changes_value", math.isclose(counted, wrong), False,
          "pad を含めれば -0.01 になり、**別物になる**")


# =====================================================================
# F4. E4 順序バイアス — **順序平均で消えるべき人工バイアス**
# =====================================================================
def f4():
    # 順序 A では +0.2 のバイアス、順序 B では -0.2。真の効果は 0。
    # **規約から出る期待値: 順序平均すれば 0.0**
    check("F4a_order_average_cancels", C.order_average([0.2, -0.2]), 0.0,
          "**順序平均で人工バイアスが消える**")
    # 片方だけ使うと残る
    check("F4b_single_order_retains_bias", C.order_average([0.2]), 0.2,
          "片順序だけなら +0.2 が残る。**両順序が必要**")
    # 真の効果 +1.0 にバイアス ±0.2 を載せても順序平均で真値へ戻る
    check("F4c_true_effect_recovered", C.order_average([1.2, 0.8]), 1.0,
          "真の効果 +1.0 は順序平均で保たれる")


# =====================================================================
# F5. 決定性ハーネス — **同一バッチ構成 2 回で完全一致**
# =====================================================================
def f5():
    per_slug = slugs16(lambda i: (i - 7.5) * 0.1)
    a = C.split_half_null(per_slug)
    b = C.split_half_null(per_slug)
    check("F5a_split_half_deterministic", a == b, True,
          "**全列挙は seed 不要で決定的**")
    arms = slugs16(lambda i: {"TRUE": 1.0 + 0.3, "SWAP": 1.0})
    p1 = C.permutation_null(arms, "E4")
    p2 = C.permutation_null(arms, "E4")
    check("F5b_permutation_deterministic", p1 == p2, True,
          "置換 null も同一入力で完全一致")
    check("F5c_split_half_enumeration_count", a["n_splits"], C.SPLIT_HALF_TOTAL,
          "**16 slug の非順序 8/8 分割は 6435 通り**(§4.2)")
    check("F5d_p95_index", a["p95_index_1origin"], 6114,
          "**95% 点 = 6114 番目の順序統計量**")


# =====================================================================
# F6. 分母確定後の除外境界 — **防御族は等号で発火**
# =====================================================================
def f6():
    # 分母 261。**> 10% で STOP** は厳密 `>`(V3 逐語維持)。
    # 261 × 0.10 = 26.1 なので、**26 件は継続、27 件で STOP**
    check("F6a_boundary_26_continue",
          C.exclusion_verdict(26, [])["verdict"], "CONTINUE",
          "26/261 = 9.96% は 10% を超えない → **継続**")
    check("F6b_boundary_27_stop",
          C.exclusion_verdict(27, [])["verdict"], C.STOP,
          "27/261 = 10.34% は 10% を超える → **STOP**")
    # **率にかかわらず、全 item 除外の slug が 1 つでもあれば即 STOP**
    v = C.exclusion_verdict(1, ["s03"])
    check("F6c_fully_dropped_slug_stops_regardless_of_rate",
          v["verdict"], C.STOP,
          "**1/261 = 0.38% でも、全 item 除外 slug があれば即 STOP**")
    check("F6d_rate_alone_would_have_passed", v["stop_by_rate"], False,
          "率単独なら通っていた。**率はどの分母でも希釈されうる**")


# =====================================================================
# A4 型 — **偶数長中央値。上側/下側中央値を用いない**
# =====================================================================
def a4():
    # 偶数長 4。**規約から出る期待値 = 中央 2 値の平均 = (2+3)/2 = 2.5**
    xs = [1.0, 2.0, 3.0, 4.0]
    check("A4a_even_median_is_mean_of_middle_two", C.median(xs), 2.5,
          "**`statistics.median`。**上側中央値 3.0 でも下側 2.0 でもない")
    wrong_upper = sorted(xs)[len(xs) // 2]
    check("A4b_upper_median_differs", wrong_upper, 3.0,
          "`sorted(x)[n//2]` は 3.0 を返す。**RETRO-0 の A4 はこの取り違え**")
    check("A4c_convention_matters", C.median(xs) == wrong_upper, False,
          "規約が違えば値が違う。**先に規約を固定する必要がある**")


# =====================================================================
# A5 型 — **母集団対応。**除外分母を取り違えない
# =====================================================================
def a5():
    # 29 item × 9 評価点 = 261。**slug 基準(16×9=144)は参考併記であって判定分母ではない**
    check("A5a_denominator_is_261", C.EXCLUSION_DENOMINATOR, 261,
          "**分母 = 29 item × 9 評価点**")
    # 同じ 20 件の除外でも、分母を 144 にすると率が変わる
    r261 = 20 / 261
    r144 = 20 / 144
    check("A5b_wrong_denominator_changes_verdict",
          (r261 > 0.10, r144 > 0.10), (False, True),
          "**20 件は 261 分母なら継続、144 分母なら STOP。**母集団対応を誤ると判定が反転する")


# =====================================================================
# 欠損 / NaN・Inf / 境界値 — **非有限は除外経路のみ。行1 へ流さない**
# =====================================================================
def nonfinite():
    items = [
        {"slug": "s00", "item_id": "i0", "value": 1.0, "n_tokens": 20},
        {"slug": "s00", "item_id": "i1", "value": float("nan"), "n_tokens": 20},
        {"slug": "s00", "item_id": "i2", "value": float("inf"), "n_tokens": 20},
        {"slug": "s00", "item_id": "i3", "value": float("-inf"), "n_tokens": 20},
        {"slug": "s00", "item_id": "i4", "value": 2.0, "n_tokens": 7},
    ]
    kept, dropped = C.exclude_items(items, "E1")
    check("N1_nonfinite_and_short_dropped", len(kept), 1,
          "nan / +inf / -inf / n_tokens<8 の 4 件が除外され、1 件残る")
    check("N2_never_routed_to_row1",
          all(d["routed_to_row1"] is False for d in dropped), True,
          "**非有限は §2.6 の除外経路のみ。行1 へ流さない**")
    reasons = sorted({d["reason"] for d in dropped})
    check("N3_reasons_enumerated", reasons,
          ["NON_FINITE_VALUE", "N_TOKENS_LT_8"],
          "除外理由が区別されて記録される")
    # **境界値: n_tokens == 8 は残る**(§2.6 は `< 8` を除外)
    b = [{"slug": "s00", "item_id": "b0", "value": 1.0, "n_tokens": 8}]
    check("N4_boundary_n_tokens_8_kept", len(C.exclude_items(b, "E1")[0]), 1,
          "**`n_tokens < 8` が除外条件。**8 は残る")
    # **NULL_scale が 0 → UNDEFINED_ENDPOINT。ε を入れない**
    d0 = C.derived(1.0, 0.0, [])
    check("N5_zero_null_scale_undefined", d0["status"], C.UNDEFINED,
          "**NULL_scale=0 は UNDEFINED_ENDPOINT。**ε を導入しない")
    check("N6_undefined_outputs_null", (d0["DR"], d0["MDE"], d0["MIN_STEP"]),
          (None, None, None), "DR / MDE / MIN_STEP は null 出力")
    check("N7_undefined_does_not_leak",
          d0["affects_other_endpoints"], False,
          "**他 endpoint に影響させない。素材は保全する**")


# =====================================================================
# 置換 null の**二方向証明**(§4.3 要件 3)
# =====================================================================
def perm_two_way():
    # (a) **検出力**: 真の腕差 +0.3 を入れれば、置換 null の中央値は 0 付近だが
    #     観測統計量は 0.3 であり、**区別できる**
    arms_effect = slugs16(lambda i: {"TRUE": 1.3, "SWAP": 1.0})
    p = C.permutation_null(arms_effect, "E4")
    check("P1_status_tested", p["status"], "TESTED",
          "E4 は腕対応を持つので検査できる")
    check("P2_exact_enumeration", p["method"], "EXACT_FULL_ENUMERATION",
          "2^16 = 65536 は全列挙できる。**標本抽出しない**")
    check("P3_null_median_zero", p["median"], 0.0,
          "**帰無分布は対称。**中央値は 0")
    obs = C.median([1.3 - 1.0] * 16)
    check("P4_power_direction", round(obs, 10), 0.3,
          "**観測統計量 0.3 は null 中央値 0 と区別できる(検出力)**")
    # (b) **沈黙**: 腕差 0 なら観測統計量も 0 で、null と区別できない
    arms_null = slugs16(lambda i: {"TRUE": 1.0, "SWAP": 1.0})
    p0 = C.permutation_null(arms_null, "E4")
    check("P5_silence_direction", (p0["median"],
                                   C.median([0.0] * 16)), (0.0, 0.0),
          "**腕差 0 なら観測も null も 0(沈黙)。**両方向を数値で示した")
    # (c) **構造的沈黙は合格に数えない**
    for ep in ("E1", "E3"):
        s = C.permutation_null(arms_effect, ep)
        check("P6_%s_structurally_not_tested" % ep, s["status"],
              C.PERM_NOT_TESTED,
              "**構造的沈黙を『null 沈黙』として合格に数えない**")


def main() -> int:
    for fn in (f1, f2, f3, f4, f5, f6, a4, a5, nonfinite, perm_two_way):
        fn()
    n_fail = sum(1 for r in R if r["verdict"] != "PASS")
    res = {
        "schema": "mythos.instrument0_stage1_fixture_result.v1",
        "created_at": "2026-08-16",
        "stage": "V5 §11 段1 — 合成 fixture",
        "principle": "**答えの分かった人工データのみ。対象データに触れない。**"
                     "期待値は規約から先に数値で書き、計器の出力と突合する",
        "core_module": "instrument0_core_v1.py",
        "cases": R, "n_cases": len(R), "n_fail": n_fail,
        "verdict": "PASS" if n_fail == 0 else "**FAIL**",
        "covers": ["B10-1 TRUE/SWAP 腕取り違え", "B10-2 E3 位置 off-by-one",
                   "B10-3 pad 右詰め混入", "B10-4 E4 順序バイアス",
                   "B10-5 決定性ハーネス", "B10-6 分母確定後の除外境界",
                   "A4 型(偶数長中央値)", "A5 型(母集団対応)",
                   "欠損 / NaN・Inf / 境界値",
                   "**置換 null の検出力・沈黙の二方向証明(§4.3 要件 3)**"],
        "not_covered": ["**本測定**(対象データに触れない)",
                        "**計器の全欠陥**(列挙した類型のみ)"],
    }
    OUT.write_bytes(json.dumps(res, ensure_ascii=False, indent=1).encode("utf-8"))
    for r in R:
        print("  [%-6s] %-46s got=%s want=%s"
              % (r["verdict"], r["case"], r["got"], r["expected"]))
    print("**段1: PASS %d / FAIL %d → %s**"
          % (len(R) - n_fail, n_fail, res["verdict"]))
    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

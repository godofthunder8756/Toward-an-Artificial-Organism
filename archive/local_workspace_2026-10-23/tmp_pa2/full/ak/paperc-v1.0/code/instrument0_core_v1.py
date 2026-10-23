# -*- coding: utf-8 -*-
"""**INSTRUMENT-0 計器本体。**V5 §2.5 / §2.6 / §4 の規約をコードにする。

**本 module は結果を解釈しない。**集約・除外・null 構成・派生量だけを計算する。

対応する条文(逐語の要点):

  §2.5 集約単位は slug(16)。item は slug 内で反復であり独立でない
       中央値は `statistics.median`(偶数長では中央 2 値の平均)。上側/下側中央値は用いない
       E4 は slug 内平均を連続 score とし、16 slug を等重みで集約
       E1 は token 数で正規化(`loss_sum / n_tokens`)
       E3 は `logsumexp(logP(151645), logP(151643))`。pad 右詰めを停止と数えない
       E4 は両順序を実行し順序平均

  §2.6 適用順: (1) 非有限は除外経路のみ (2) `n_tokens < 8` は E1 から除外
       (3) 行1 が見るのは集約後に残った異常 + 読込失敗 + SHA 不一致のみ
       分母 = 29 item × 9 評価点 = 261。**> 10% で STOP**
       **primary contrast で全 item が除外された slug が 1 つでもあれば率にかかわらず即 STOP**

  §4.1 `SEP_max` = d0 対 d192 の slug 中央値差(E2 は d0 の選好そのもの)
       `NULL_scale` = max(|置換 null の中央値|, split-half 差の絶対値の 95% 点)
       `DR = |SEP_max| / NULL_scale`
       `MIN_STEP` = 隣接 dose 対のうち `|差| > NULL_scale` を満たす最小用量差

  §4.2 16 slug の非順序 8/8 分割は全 6435 通り。**全列挙。**95% 点 = 6114 番目の順序統計量

  §4.3 置換 null は 3 要件を満たしたときだけ「検査した」と数える
       E1 / E3 は `PERMUTATION_NULL_STRUCTURALLY_NOT_TESTED`
       標本抽出が必要な場合 K=5000 / 保守側上位順序統計量 / 補間なし / seed 20260931

  §4.4 `NULL_scale` が 0 または非有限 → `UNDEFINED_ENDPOINT`。DR/MDE/MIN_STEP は null
       **禁止: ε の導入 / 分位点の切替 / 尺度の切替**

  §4.5 `MDE = NULL_scale × 2`

  §4.6 演算子族: 実用境界=包含(`>=`/`<=`)/ 検出・主張=厳密 `>` / 防御・停止=等号で発火

**保証しないこと:**
  - **解釈。**本 module は判定値を返すだけで、結論を書かない
  - **SESOI。**測定から決まらない(§4.7)。外から与える
"""
from __future__ import annotations

import itertools
import math
import random
import statistics
from typing import Iterable

# --- 規約から直接来る定数。**コード内で変えない** ---
N_SLUGS_EXPECTED = 16
SPLIT_HALF_TOTAL = 6435          # C(16,8)/2
SPLIT_HALF_P95_INDEX = 6114      # 1-origin の順序統計量
EXCLUSION_DENOMINATOR = 261      # 29 item × 9 評価点
EXCLUSION_STOP_RATE = 0.10       # **> 10% で STOP**(防御族は等号で発火)
E1_MIN_TOKENS = 8
PERM_K = 5000
PERM_SEED = 20260931
PERM_EXACT_LIMIT = 1 << 17       # これ以下なら全列挙する(標本抽出より強い)
MDE_FACTOR = 2
EOS_IDS = (151645, 151643)

PERM_NOT_TESTED = "PERMUTATION_NULL_STRUCTURALLY_NOT_TESTED"
UNDEFINED = "UNDEFINED_ENDPOINT"
STOP = "INSTRUMENT_STOP"


class InstrumentStop(Exception):
    """**修理せず止める。**許容差の緩和・再試行の経路は持たない(段6)。"""


# ---------------------------------------------------------------- 基本量


def median(xs) -> float:
    """**`statistics.median` に統一する。**偶数長は中央 2 値の平均。

    上側/下側中央値(`sorted(x)[n//2]`)は**用いない。**
    RETRO-0 の A4 はこの取り違えで起きた。
    """
    return statistics.median(xs)


def logsumexp(values) -> float:
    """E3 の停止質量。**max を引いてから足す**(桁落ちを避ける)。"""
    vs = [v for v in values]
    if not vs:
        return -math.inf
    m = max(vs)
    if m == -math.inf:
        return -math.inf
    return m + math.log(sum(math.exp(v - m) for v in vs))


def is_finite(x) -> bool:
    return isinstance(x, (int, float)) and math.isfinite(x)


# ---------------------------------------------------------------- 除外


def exclude_items(items, endpoint: str):
    """§2.6 の**適用順どおり**に除外する。返り値 (残った item, 除外記録)。

    1. **非有限は §2.6 の除外経路のみ**に載せる。行1 へ流さない
    2. `n_tokens < 8` の item は **E1 から**除外
    """
    kept, dropped = [], []
    for it in items:
        v = it.get("value")
        if not is_finite(v):
            dropped.append({**{k: it[k] for k in ("slug", "item_id")},
                            "reason": "NON_FINITE_VALUE",
                            "routed_to_row1": False})
            continue
        if endpoint == "E1" and it.get("n_tokens", 0) < E1_MIN_TOKENS:
            dropped.append({**{k: it[k] for k in ("slug", "item_id")},
                            "reason": "N_TOKENS_LT_%d" % E1_MIN_TOKENS,
                            "routed_to_row1": False})
            continue
        kept.append(it)
    return kept, dropped


def exclusion_verdict(n_dropped: int, slugs_fully_dropped) -> dict:
    """**防御族は等号で発火する。**率は `> 10%`(V3 逐語維持)。

    **全 item が除外された slug が 1 つでもあれば率にかかわらず即 STOP。**
    率はどの分母でも希釈されうるため。
    """
    rate = n_dropped / EXCLUSION_DENOMINATOR
    by_rate = rate > EXCLUSION_STOP_RATE            # **厳密 >(V3 逐語)**
    by_slug = len(slugs_fully_dropped) >= 1         # **1 つでも → 発火**
    return {
        "n_dropped": n_dropped,
        "denominator": EXCLUSION_DENOMINATOR,
        "rate": rate,
        "rate_threshold": EXCLUSION_STOP_RATE,
        "stop_by_rate": by_rate,
        "slugs_fully_dropped": sorted(slugs_fully_dropped),
        "stop_by_fully_dropped_slug": by_slug,
        "verdict": STOP if (by_rate or by_slug) else "CONTINUE",
    }


# ---------------------------------------------------------------- 集約


def slug_value(items, endpoint: str) -> float:
    """slug 内の item を 1 値へ。**E1 は token 正規化、E4 は平均、他は中央値。**"""
    if endpoint == "E1":
        # **`loss_sum / n_tokens`。**item ごとに正規化してから slug 中央値
        return median([it["value"] / it["n_tokens"] for it in items])
    if endpoint == "E4":
        # **R17: E4 は slug 内平均を連続 score とする**(有界 score のため)
        return sum(it["value"] for it in items) / len(items)
    return median([it["value"] for it in items])


def order_average(pairs) -> float:
    """**E4 は両順序を実行し順序平均。**人工的な順序バイアスはここで消える。"""
    return sum(pairs) / len(pairs)


# ---------------------------------------------------------------- null


def split_half_null(per_slug: dict) -> dict:
    """§4.2 **全 6435 通りを列挙する。**95% 点 = **6114 番目の順序統計量**。

    **seed 不要・厳密・決定的。**作用する量は `SEP_max` と同一の per-slug
    primary contrast 値である。
    """
    slugs = sorted(per_slug)
    n = len(slugs)
    if n != N_SLUGS_EXPECTED:
        raise InstrumentStop(
            "**slug 数が %d でない: %d。**全列挙の前提が崩れる"
            % (N_SLUGS_EXPECTED, n))
    vals = [per_slug[s] for s in slugs]
    first = slugs[0]
    diffs = []
    # **非順序分割。**先頭 slug を必ず片側へ固定すると重複が消える
    for combo in itertools.combinations(range(1, n), n // 2 - 1):
        left = {0} | set(combo)
        a = [vals[i] for i in range(n) if i in left]
        b = [vals[i] for i in range(n) if i not in left]
        diffs.append(abs(median(a) - median(b)))
    if len(diffs) != SPLIT_HALF_TOTAL:
        raise InstrumentStop(
            "**分割数が %d でない: %d**" % (SPLIT_HALF_TOTAL, len(diffs)))
    diffs.sort()
    return {
        "n_splits": len(diffs),
        "p95_index_1origin": SPLIT_HALF_P95_INDEX,
        "p95": diffs[SPLIT_HALF_P95_INDEX - 1],
        "method": "EXACT_FULL_ENUMERATION",
        "seed_free": True,
        "anchor_slug_fixed_to_left": first,
    }


def permutation_null(per_slug_by_arm: dict, endpoint: str) -> dict:
    """§4.3 **3 要件を満たしたときだけ「検査した」と数える。**

    要件 1(何をどの階層で置換するか): **slug 内の腕ラベル(TRUE / SWAP)を
    slug 単位で入れ替える。**item は slug 内の反復であり独立でないため、
    置換の階層は **slug** である。

    要件 2(交換可能性): 帰無仮説「腕ラベルは per-slug contrast に無情報」の下で、
    **各 slug の 2 腕は交換可能。**slug 間は独立と仮定しない — 置換は slug 内に閉じる。

    要件 3(二方向証明): 段1 fixture が担当する。

    **E1 / E3 は構造的に腕対応を持たないため `PERMUTATION_NULL_STRUCTURALLY_NOT_TESTED`。**
    **構造的沈黙を「null 沈黙」として合格に数えない。**
    """
    if endpoint in ("E1", "E3"):
        return {"status": PERM_NOT_TESTED,
                "why": "**腕ラベルの対応を構造的に持たない endpoint である。**"
                       "沈黙を合格に数えない",
                "median": None}

    slugs = sorted(per_slug_by_arm)
    n = len(slugs)
    space = 1 << n
    obs = [per_slug_by_arm[s]["TRUE"] - per_slug_by_arm[s]["SWAP"] for s in slugs]

    def stat(signs) -> float:
        return median([v if sgn else -v for v, sgn in zip(obs, signs)])

    if space <= PERM_EXACT_LIMIT:
        # **全列挙できるなら標本抽出しない。**split-half と同じ流儀
        vals = [stat(tuple((m >> i) & 1 for i in range(n)))
                for m in range(space)]
        method, k_used = "EXACT_FULL_ENUMERATION", None
    else:
        rng = random.Random(PERM_SEED)
        vals = [stat(tuple(rng.getrandbits(1) for _ in range(n)))
                for _ in range(PERM_K)]
        # **保守側上位順序統計量。**`k/(K+1) >= 0.95` を満たす最小 k。**補間なし**
        k_used = math.ceil(0.95 * (PERM_K + 1))
        method = "SAMPLED_K%d_SEED%d" % (PERM_K, PERM_SEED)

    vals.sort()
    return {
        "status": "TESTED",
        "permuted_unit": "slug",
        "permuted_label": "arm(TRUE/SWAP)",
        "exchangeability": "**帰無の下で各 slug の 2 腕は交換可能。**"
                           "置換は slug 内に閉じ、slug 間の独立は仮定しない",
        "method": method,
        "n_draws": len(vals),
        "conservative_order_statistic_k": k_used,
        "no_interpolation": True,
        "median": median(vals),
    }


# ---------------------------------------------------------------- 派生量


def null_scale(perm: dict, split: dict) -> float:
    """§4.1 **単一式。**`max(|置換 null の中央値|, split-half の 95% 点)`。

    置換 null が構造的に未検査なら、その項は寄与しない
    (**沈黙を 0 として合格に使わない** — §4.3 の claim 制限は別途出力する)。
    """
    parts = [split["p95"]]
    if perm.get("median") is not None:
        parts.append(abs(perm["median"]))
    return max(parts)


def derived(sep_max: float, ns: float, adjacent_diffs) -> dict:
    """§4.4 / §4.5 / §4.1。**NULL_scale が 0 または非有限なら UNDEFINED_ENDPOINT。**

    **禁止: ε の導入 / 分位点の切替 / 尺度の切替。**
    """
    if (not is_finite(ns)) or ns == 0:
        return {"status": UNDEFINED, "null_scale": ns,
                "DR": None, "MDE": None, "MIN_STEP": None,
                "why": "**NULL_scale が 0 または非有限。**"
                       "ε を入れない。分位点も尺度も切り替えない",
                "affects_other_endpoints": False,
                "material_preserved": True}
    # **検出・主張の族は厳密 `>`。**
    steps = sorted((gap for gap, d in adjacent_diffs if abs(d) > ns))
    return {"status": "DEFINED",
            "null_scale": ns,
            "DR": abs(sep_max) / ns,
            "MDE": ns * MDE_FACTOR,
            "MIN_STEP": steps[0] if steps else None,
            "min_step_operator": "**厳密 `>`(検出・主張の族)**",
            "dr_threshold_verbatim_from_v3": "DR >= 3"}


def practical_boundary(delta: float, sesoi) -> dict:
    """§4.6 **実用境界は包含(`>=`)。**SESOI が無い endpoint は行5 経路。"""
    if sesoi is None:
        return {"status": "NO_SESOI",
                "route": "**行5 経路**(§4.8。E1 / E2 / E4 は SESOI 不在)",
                "meets": None}
    return {"status": "HAS_SESOI", "sesoi": sesoi,
            "meets": abs(delta) >= sesoi,          # **包含**
            "operator": "**`>=`(実用境界の族)**"}

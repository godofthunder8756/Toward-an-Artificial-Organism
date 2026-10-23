# -*- coding: utf-8 -*-
r"""INSTRUMENT-0 段5 測定 runner(**着手順 4**)。

**批准済みの決定だけを参照する。数値は直書きしない。**

**参照表は「いま実際に読んでいるか」を分けて書く。**
docstring が読んでいないものを読んでいると書けば、それは虚偽の自己記述である
(2026-08-17、Fable MF-R1 / MF-R2 と当方の自己検査で計 4 件見つかった)。

| 参照先 | 何を決めているか | 現状 |
|---|---|---|
| `FABLE_BATCH_PLAN_RULING_V3.json` | bs=1 / padding なし / 切詰なし / 順序 | **読む**(`assert_batch_plan`) |
| `INSTRUMENT0_PRE_DATA_DECISIONS_V1.json` | D1 / D3 / D4 | **読む** |
| `FABLE_PRE_DATA_DECISIONS_RATIFICATION_V1.json` | 組み立て literal の逐語 pin | **読む**(`e4_template` で一致検査) |
| `instrument0_core_v1.py` | 集約・除外・null・派生量 | **読む** |
| `instrument0_runner_guard_v1.py` | B9 要件2 / 要件3 | **読む** |
| `INSTRUMENT0_TOKEN_COUNT_RECEIPT_V1.json` | 事前の長さ統計 | **読む**(`measure` が slug 集合と context_limit を照合) |
| `STUDY56_SWAP_MAPPING_V3.json` | 素材同定と item 順序 | **読む**(`measure` の素材同定) |

**未実装のものは未実装と書く。**起動照合(`REQUIRED_UNDER_MANIFEST`)には
いずれも入れてある — **読む予定のものを照合対象から外すのは B9 要件2 の穴**である。

**本器は段3 manifest 無しでは走らない。**要件2 の逐語は「不一致なら非ゼロ終了で
実行拒否」であり、**manifest が無い状態は照合できない状態である。**素通りさせない。

**対象データに触れる経路は `measure` だけで、それは段3 の後にしか到達できない。**
検証は synthetic と段2 代理のみで行う。

---

**§6 の分岐は上から評価し、最初に該当した行で確定する。**
行を飛ばす経路・複数行を合議する経路は置かない。
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

H = Path(__file__).resolve().parent
sys.path.insert(0, str(H))

import instrument0_core_v1 as C                    # noqa: E402
import instrument0_runner_guard_v1 as G            # noqa: E402

BATCH_PLAN = H / "FABLE_BATCH_PLAN_RULING_V3.json"
DECISIONS = H / "INSTRUMENT0_PRE_DATA_DECISIONS_V1.json"
RATIFICATION = H / "FABLE_PRE_DATA_DECISIONS_RATIFICATION_V1.json"
TOKEN_RECEIPT = H / "INSTRUMENT0_TOKEN_COUNT_RECEIPT_V1.json"
SWAP3 = H / "STUDY56_SWAP_MAPPING_V3.json"

# **段3 manifest。存在しなければ本器は起動しない**
STAGE3_MANIFEST = H / "INSTRUMENT0_STAGE3_FREEZE_MANIFEST_V1.json"

# **本器が読むファイルはすべてここに入れる。**
# **読むのに起動照合しないファイルは B9 要件2 の穴である**(Fable MF-R3)。
REQUIRED_UNDER_MANIFEST = [
    "instrument0_core_v1.py",
    "instrument0_runner_guard_v1.py",
    "instrument0_runner_v1.py",
    "instrument0_token_count_receipt_v1.py",
    "INSTRUMENT0_PRE_DATA_DECISIONS_V1.json",
    "FABLE_PRE_DATA_DECISIONS_RATIFICATION_V1.json",
    "INSTRUMENT0_TOKEN_COUNT_RECEIPT_V1.json",
    "FABLE_BATCH_PLAN_RULING_V3.json",
    "STUDY56_SWAP_MAPPING_V3.json",
]

EXIT_NO_MANIFEST = 5
EXIT_UNAUTHORIZED_AMENDMENT = 6

# **legacy(他 prereg)の amendment はここでは扱わない。**各自の凍結 manifest が守る
_LEGACY_PREFIXES = ("STUDY", "PREREG_STUDY", "PREREG_RETRO0", "PREREG_P70")


def _v5_amendment_scope(name: str) -> bool:
    return not name.startswith(_LEGACY_PREFIXES)


def _load_amendment_gate():
    """10_control の授権門 module を path 非依存で読み込む。"""
    import importlib.util
    gp = H.parents[1] / "10_control" / "amendment_class_gate_v1.py"
    spec = importlib.util.spec_from_file_location("amendment_class_gate_v1", gp)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def assert_amendment_inertness() -> dict:
    """**P5 の実接続(操作者裁定 2026-08-17「解決まで実行せよ」)。**

    起動時に、本 dir の V5 系 amendment 記録すべてが
    effective(効力あり)か inert(明示的に不活性)のどちらかであることを検査する。
    **unknown が 1 件でもあれば起動を拒否する** — 未授権の解縛型・未分類の新規・
    annex pin と食い違う原本(無言改変)はすべてここに落ちる。

    さらに **A1(logP_observed_base の定義)が effective であること**を要求する。
    §6.1 guard の被検査値の定義が効力を失っていれば、測定は始められない。
    """
    gate = _load_amendment_gate()
    r = gate.effective_amendments(H, _v5_amendment_scope)
    if r["unknown"]:
        print("**実行拒否。効力の判定できない amendment 記録がある:**")
        for u in r["unknown"]:
            print("  %-56s %s" % (u["file"], u["why"]))
        sys.exit(EXIT_UNAUTHORIZED_AMENDMENT)
    eff = {e["file"] for e in r["effective"]}
    if "PREREG_INSTRUMENT0_V5_AMENDMENT_A1_RECORD.json" not in eff:
        print("**実行拒否。A1(logP_observed_base の定義)が効力を持っていない**")
        sys.exit(EXIT_UNAUTHORIZED_AMENDMENT)
    return r


def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ------------------------------------------------- B9 要件2: 起動時の同一性

def assert_startup(manifest: Path = None) -> dict:
    """**段3 manifest と照合できなければ実行を拒否する。**

    **manifest が無い状態を「照合対象なし」として素通りさせない。**
    freeze_guard の F-2(対象 0 件を全一致と誤る)と同じ穴になる。
    """
    amendments = assert_amendment_inertness()      # **P5: manifest 検査より先**
    manifest = manifest or STAGE3_MANIFEST
    if not manifest.exists():
        print("**実行拒否。段3 manifest が存在しない: %s**" % manifest.name)
        print("**照合できない状態は不一致と同じ扱いにする。**"
              "段3(計器一式の凍結)を先に通すこと")
        sys.exit(EXIT_NO_MANIFEST)
    ident = G.assert_frozen_identity(manifest, REQUIRED_UNDER_MANIFEST, H)
    return {"identity": ident, "amendments": amendments,
            "batch_plan": assert_batch_plan(), "d3": assert_d3_agreement()}


# ------------------------------------------------ バッチ計画(批准済み裁定)

def assert_batch_plan() -> dict:
    """**バッチ計画 V3 の invariant を起動時に検査する。**

    2026-08-17: 当方の自己検査で、`BATCH_PLAN` が定義されただけで一度も読まれて
    いないことが分かった。**docstring は「参照する」と書いていた。**
    MF-R1 / MF-R2 と同型の虚偽の自己記述である。

    **読むだけでなく、裁定の核が保たれていることを検査する。**
    bs != 1 や padding 有りへ変わっていれば、Paper B の B2 類が復活する。
    """
    b = json.loads(BATCH_PLAN.read_text(encoding="utf-8"))
    flat = json.dumps(b, ensure_ascii=False)
    bad = []
    if "bs=1" not in flat:
        bad.append("bs=1 の宣言が見当たらない")
    if "padding" not in flat:
        bad.append("padding についての宣言が見当たらない")
    if bad:
        raise C.InstrumentStop(
            "**バッチ計画 V3 の invariant が確認できない: %r**" % bad)
    return {"file": BATCH_PLAN.name, "sha256": sha_file(BATCH_PLAN),
            "invariants_present": ["bs=1", "padding"],
            "why_checked": "**bs != 1 や padding 有りへ変わっていれば "
                           "Paper B の B2 類が復活する**"}


# ------------------------------------------------------------ D3 決定性

def assert_d3_agreement() -> dict:
    """**適用値と批准済み D3 の宣言値を突き合わせる。**食い違えば STOP。

    2026-08-17 訂正(Fable MF-R2): 旧版の docstring は「値はここに直書きせず
    決定記録から読む」と書いていたが、**`:4096:8` と TF32 False は直書きで、
    記録からは metadata しか読んでいなかった。**

    **適用自体は code に書くしかない。**権威は D3 にあり、code は段3 で凍結され、
    **起動時の一致検査**が転写誤りの検出線になる — #5 の `E1_MIN_TOKENS` 照合と
    同じ型である。
    """
    d = json.loads(DECISIONS.read_text(encoding="utf-8"))["D3_determinism_config"]
    declared = {x["item"]: str(x.get("value", "")) for x in d["fixed"]}
    applied = {"CUBLAS_WORKSPACE_CONFIG": ":4096:8",
               "torch.use_deterministic_algorithms": "True"}
    bad = []
    for k, v in applied.items():
        if k not in declared:
            bad.append({"item": k, "problem": "NOT_DECLARED_IN_D3"})
        elif declared[k] != v:
            bad.append({"item": k, "declared": declared[k], "applied": v})
    tf32 = next((x for x in d["fixed"] if x["item"] == "TF32"), None)
    if tf32 is None or "OFF" not in tf32.get("value", ""):
        bad.append({"item": "TF32", "problem": "D3 が OFF を宣言していない",
                    "declared": tf32.get("value") if tf32 else None})
    if bad:
        raise C.InstrumentStop(
            "**適用値と批准済み D3 の宣言が食い違う: %r**" % bad)
    return {"agreed": sorted(applied), "tf32_declared": tf32["value"],
            "decision_sha256": sha_file(DECISIONS)}


def apply_determinism() -> dict:
    """**D3(批准済み)を適用する。**

    **適用値は code に書く。**権威は D3 にあり、`assert_d3_agreement()` が
    起動時に一致を検査する。**docstring と実装が食い違わないよう、
    「読む」ではなく「突き合わせる」と書く。**
    """
    agree = assert_d3_agreement()
    d = json.loads(DECISIONS.read_text(encoding="utf-8"))["D3_determinism_config"]
    import torch
    os.environ["CUBLAS_WORKSPACE_CONFIG"] = ":4096:8"
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    return {"d3_agreement": agree,
            "applied_from": DECISIONS.name,
            "decision_sha256": sha_file(DECISIONS),
            "fixed": [x["item"] for x in d["fixed"]],
            "seed": d["seed"]["state"],
            "env_CUBLAS_WORKSPACE_CONFIG": os.environ["CUBLAS_WORKSPACE_CONFIG"],
            "tf32_matmul": torch.backends.cuda.matmul.allow_tf32,
            "tf32_cudnn": torch.backends.cudnn.allow_tf32,
            "versions": {"torch": torch.__version__}}


# ------------------------------------------------------------ D4 組み立て

def e4_template() -> str:
    """**決定記録と批准記録の両方を読み、literal の一致を検査する。**

    2026-08-17 訂正(Fable MF-R1): 旧版の docstring は「批准記録の pin を読む」と
    書きながら、**実際には決定記録しか読んでおらず、`RATIFICATION` は定義された
    だけで一度も使われていなかった。**凍結される成果物に虚偽の自己記述は残せない。

    **両方を読んで突き合わせるのは、どちらか一方が改変されたときの検出線になる。**
    """
    d = json.loads(DECISIONS.read_text(encoding="utf-8"))
    t_dec = d["D4_prompt_format"]["tier_2_literal_required"][
        "assembled_literal"]["template"]
    r = json.loads(RATIFICATION.read_text(encoding="utf-8"))
    t_rat = r["assembled_literal_pinned_verbatim"]["template"]
    if t_dec != t_rat:
        raise C.InstrumentStop(
            "**決定記録と批准記録で組み立て literal が食い違う。**\n"
            "  決定 %r\n  批准 %r" % (t_dec, t_rat))
    return t_dec.replace("\\n", "\n")


def build_e4(prompt: str, cand_a: str, cand_b: str) -> str:
    """**placeholder 以外は 1 バイトも変えない。**"""
    return (e4_template()
            .replace("{prompt}", prompt)
            .replace("{cand_A}", cand_a)
            .replace("{cand_B}", cand_b))


def resolve_answer_ids(tok) -> dict:
    """**D4-c。先頭空白なしの単一 token でなければ `INSTRUMENT_STOP`。**"""
    out = {}
    for ch in ("A", "B"):
        ids = tok(ch, add_special_tokens=False)["input_ids"]
        if len(ids) != 1:
            raise C.InstrumentStop(
                "**記号 %r が単一 token に分解されない(%d 個): %s**"
                % (ch, len(ids), ids))
        out[ch] = ids[0]
    if out["A"] == out["B"]:
        raise C.InstrumentStop("**A と B が同一 token ID になった: %s**" % out)
    return out


def e4_item_score(logp_a_first: dict, logp_b_first: dict) -> dict:
    """**両順平均。厳密 `>`。同値は 0(保守側)。**値域 {0, 0.5, 1}。"""
    def one(lp: dict) -> int:
        return 1 if lp["correct"] > lp["wrong"] else 0
    s1, s2 = one(logp_a_first), one(logp_b_first)
    return {"order_1": s1, "order_2": s2, "item_score": (s1 + s2) / 2,
            "operator": "**厳密 `>`(§4.6 検出・主張の族)**",
            "tie_rule": "**同値は 0。**保守側"}


# ------------------------------------------------------ D1 実行時の長さ guard

def runtime_length_guard(n_tokens_total, ctx_limit: int) -> dict:
    """**事前 receipt と実行時の二重化**(Fable 追加条件、2026-08-17)。

    **事前確認だけに依存しない。**receipt は素材が変わっていない前提の証拠であり、
    実行時に測るのは、その前提が今も成り立っていることの確認である。
    """
    over = [i for i, n in enumerate(n_tokens_total) if n > ctx_limit]
    return {"context_limit": ctx_limit, "n_checked": len(n_tokens_total),
            "n_over": len(over), "over_index": over,
            "verdict": C.STOP if over else "CONTINUE",
            "why_twice": "**事前 receipt と実行時検査の二重化。**"
                         "事前確認だけに依存しない"}


# ------------------------------------------------------------ §6 分岐表

def classify(endpoint: str, ev: dict) -> dict:
    """**§6。上から評価し、最初に該当した行で確定する。**

    `ev` は事前に計算された証拠。**本関数は判定のみで、値を作らない。**
    行を飛ばす経路・複数行を合議する経路は置かない。
    """
    # **証拠の組の整合を先に検査する。**§4.6 / D1 により SESOI は E3 のみで、
    # E1 / E2 / E4 は SESOI 不在(行5 経路)。非 E3 が SESOI 判定を持つ組は
    # **矛盾**であり、黙って落とさず STOP にする。
    # (2026-08-17: 検証がこの組で分岐表の穴に落ちた。**穴ではなく不正な入力**
    #  だったが、**分類器が呼び出し側の整合性に依存する形は危うい**)
    if endpoint != "E3" and ev.get("mde_le_sesoi") is not None:
        raise C.InstrumentStop(
            "**SESOI は E3 のみである(§4.6)。**endpoint=%s が "
            "mde_le_sesoi=%r を持つのは矛盾した証拠の組"
            % (endpoint, ev.get("mde_le_sesoi")))

    rows = []

    def hit(n, name, cond, nxt):
        rows.append({"row": n, "verdict": name, "matched": bool(cond)})
        return bool(cond), {"row": n, "verdict": name, "next": nxt,
                            "evaluated": rows}

    ok, r = hit(1, "INSTRUMENT_STOP", ev.get("stop_row1"), "修理のみ。判定しない")
    if ok:
        return r
    ok, r = hit(2, "NULL_FAIL", ev.get("null_fires_at_equality"),
                "**構造以外を拾っている。**Day 1 で使用禁止")
    if ok:
        return r
    sep, ns = ev.get("sep_max"), ev.get("null_scale")
    wrong_dir = (ev.get("expected_sign") is not None and sep is not None
                 and ns is not None and C.is_finite(sep) and C.is_finite(ns)
                 and (sep * ev["expected_sign"] < 0) and abs(sep) > ns)
    ok, r = hit(2.5, "SEPARATES_WRONG_DIRECTION", wrong_dir,
                "**使用禁止。計器 / ラベル検査へ**")
    if ok:
        return r
    ok, r = hit(3, "FAILED_FLOOR_CEILING", ev.get("saturated"),
                "**動作域を明記し、域外の用量比較を除外**")
    if ok:
        return r
    ok, r = hit(3.5, "UNDEFINED_ENDPOINT",
                (ns is None) or (not C.is_finite(ns)) or ns == 0,
                "**BLOCK。素材は焼かない**")
    if ok:
        return r

    dr = ev.get("DR")
    silent = ev.get("null_silent")
    sesoi_ok = ev.get("mde_le_sesoi")
    is_e3 = endpoint == "E3"
    ok, r = hit(4, "VALIDATED_AND_PRACTICALLY_ADEQUATE",
                dr is not None and dr >= 3 and silent and is_e3
                and sesoi_ok is True,
                "使用可。**実測 MDE を記入**")
    if ok:
        return r
    ok, r = hit(5, "VALIDATED_BUT_PRACTICAL_BASIS_MISSING",
                dr is not None and dr >= 3 and silent and sesoi_ok is None,
                "使用可。**ROPE 感度分析表を添付**し単一閾値を書かない")
    if ok:
        return r
    ok, r = hit(6, "UNDERPOWERED_FOR_PRACTICE",
                dr is not None and dr >= 3 and is_e3 and sesoi_ok is False,
                "増強設計が要る")
    if ok:
        return r
    ok, r = hit(7, "WEAK", dr is not None and 1 <= dr < 3,
                "使用可だが増強を先に設計")
    if ok:
        return r
    ok, r = hit(8, "NOT_SEPARABLE", dr is not None and dr < 1,
                "使用禁止。代替計器の設計へ")
    if ok:
        return r
    raise C.InstrumentStop(
        "**§6 のどの行にも該当しなかった。**分岐表が観測空間を覆っていない: %r" % ev)


def saturation_e3(logp_observed_base: float) -> dict:
    """**§6.1 両側 guard。**床 / 天井は封印条文、被検査値は A1 の定義による。

    **−20.0 / −1.0 の直書きは封印条文の転写である。**権威は prereg にあり、
    code は段3 で凍結され、検証の R-F* が転写誤りの検出線になる
    (Fable 付記、2026-08-17)。
    """
    floor, ceiling = -20.0, -1.0
    inside = floor < logp_observed_base < ceiling
    return {"floor": floor, "ceiling": ceiling,
            "logP_observed_base": logp_observed_base,
            "inside": inside,
            "verdict": "CONTINUE" if inside else C.STOP,
            "value_definition": "**A1(批准済み)。**Phase 0 自身の d0 実測。"
                                "E3 / slug 中央値 / 末尾直後 / slug 間も中央値",
            "not_from": "**STUDY36 receipt は参考系であり、"
                        "guard の被検査値ではない**"}


def saturation_ratio(k: int, n: int) -> dict:
    """**§6.1 比率型。**`k == 0` または `k == n`(`n >= 4`)。"""
    sat = n >= 4 and (k == 0 or k == n)
    return {"k": k, "n": n, "saturated": sat,
            "rule": "**k == 0 または k == n(n >= 4)**"}


# ------------------------------------------------------------ 対象データ経路

# ------------------------------------------------------------ 段5 本測定

DOSES = (0, 16, 32, 48, 64, 96, 128, 160, 192)      # 9 checkpoint(d0 = base)
RUN_TPL = "runs/s7_4B_F_d%d_lr0.0002_ep2/adapter"


def _load_matrix_materials():
    """素材同定。**#5 receipt と同じ流儀: completion 本文 SHA で結ぶ。**"""
    swap = json.loads((H / "STUDY56_SWAP_MAPPING_V3.json").read_text(encoding="utf-8"))
    rows = [json.loads(l) for l in (H / "data" / "dev_v1.jsonl"
                                    ).read_text(encoding="utf-8").splitlines()
            if l.strip()]
    by_sha = {hashlib.sha256(r["completion"].encode("utf-8")).hexdigest(): r
              for r in rows}
    items = []
    for m in sorted(swap["mapping"], key=lambda x: x["target_completion_sha256"]):
        tgt = by_sha.get(m["target_completion_sha256"])
        swp = by_sha.get(m["swap_completion_sha256"])
        if tgt is None or swp is None:
            raise C.InstrumentStop("**素材同定の破れ: %s**" % m["target_slug"])
        items.append({"slug": m["target_slug"], "prompt": tgt["prompt"],
                      "true": tgt["completion"], "swap": swp["completion"],
                      "item_id": m["target_completion_sha256"][:12]})
    if len(items) != 29:
        raise C.InstrumentStop("**item 数が 29 でない: %d**" % len(items))
    return swap, items


def _tf_scores(model, tok, prompt: str, completion: str, device):
    """teacher-forced 1 forward。**STUDY56 prereg §4 の手順の逐語**:
    prompt と completion を別々に token 化して連結、prompt 部は採点しない。
    返り値: loss_sum, n_tokens, mean_nll, stop_mass(末尾直後)。"""
    import torch
    pi = tok(prompt, add_special_tokens=False)["input_ids"]
    ci = tok(completion, add_special_tokens=False)["input_ids"]
    ids = torch.tensor([pi + ci], device=device)
    with torch.no_grad():
        out = model(ids)
    logits = out.logits[0]
    logp = torch.log_softmax(logits.float(), dim=-1)
    lp = 0.0
    for k, t in enumerate(ci):
        lp += float(logp[len(pi) + k - 1, t])
    n = len(ci)
    # E3: 末尾直後 = completion 最終 token を読んだ位置の次予測分布
    tail = logp[len(pi) + n - 1]
    sm = float(torch.logsumexp(
        torch.stack([tail[C.EOS_IDS[0]], tail[C.EOS_IDS[1]]]), dim=0))
    return {"loss_sum": -lp, "n_tokens": n, "mean_nll": -lp / n, "stop_mass": sm}


def _e4_choice(model, tok, ids_ab, prompt, cand_a, cand_b, device):
    """E4 1 提示。組み立ては批准 literal(build_e4)。採点は次 token の logP。"""
    import torch
    text = build_e4(prompt, cand_a, cand_b)
    ti = tok(text, add_special_tokens=False)["input_ids"]
    ids = torch.tensor([ti], device=device)
    with torch.no_grad():
        out = model(ids)
    lp = torch.log_softmax(out.logits[0, -1].float(), dim=-1)
    return {"logp_A": float(lp[ids_ab["A"]]), "logp_B": float(lp[ids_ab["B"]])}


def measure(frozen_at: str):
    """**対象データに触れる唯一の経路。段3 manifest 無しでは到達できない。**

    9 checkpoint × 29 item を teacher-forced で一度だけ測る(§11 段5)。
    raw は instrument SHA で刻印し(B9 要件3)、集約・分岐は core と classify に
    委ねる。**再試行・許容差の経路は無い。失敗は InstrumentStop 一本道。**
    """
    startup = assert_startup()                    # P5 + B9 要件2 + D3 + バッチ計画
    apply_determinism()
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel

    swap, items = _load_matrix_materials()
    # **#5 receipt との照合。**事前計数と素材が同一であることの検査
    rc = json.loads(TOKEN_RECEIPT.read_text(encoding="utf-8"))
    rc_slugs = {x["target_slug"] for x in rc["items"]}
    if rc_slugs != {it["slug"] for it in items} or len(rc["items"]) != 29:
        raise C.InstrumentStop("**#5 receipt と素材の slug 集合が一致しない**")
    codec_dir = swap["text_codec_source"]
    tok = AutoTokenizer.from_pretrained(codec_dir)
    ids_ab = resolve_answer_ids(tok)
    ctx_limit = json.loads((Path(codec_dir) / "config.json"
                            ).read_text(encoding="utf-8"))["max_position_embeddings"]
    if rc["d1_length_guard"]["context_limit"] != ctx_limit:
        raise C.InstrumentStop("**#5 receipt の context_limit が config と食い違う**")

    my_sha = sha_file(H / "instrument0_runner_v1.py")
    out_path = H / "INSTRUMENT0_STAGE5_RAW_V1.jsonl"
    if out_path.exists():
        raise C.InstrumentStop("**段5 raw が既に存在する。一度だけ適用の条文により"
                               "再実行しない**")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    fh = open(out_path, "w", encoding="utf-8")
    try:
        for dose in DOSES:
            model = AutoModelForCausalLM.from_pretrained(
                codec_dir, dtype=torch.bfloat16, device_map={"": 0})
            if dose != 0:
                model = PeftModel.from_pretrained(
                    model, str(H / (RUN_TPL % dose)))
            model.eval()
            for it in items:
                # D1 実行時 guard(事前 receipt との二重化)
                lens = [len(tok(it["prompt"], add_special_tokens=False)["input_ids"])
                        + len(tok(x, add_special_tokens=False)["input_ids"])
                        for x in (it["true"], it["swap"])]
                g = runtime_length_guard(lens, ctx_limit)
                if g["verdict"] != "CONTINUE":
                    raise C.InstrumentStop("**長さ guard 発火: %r**" % g)
                row = {"dose": dose, "slug": it["slug"], "item_id": it["item_id"],
                       "TRUE": _tf_scores(model, tok, it["prompt"], it["true"],
                                          device),
                       "SWAP": _tf_scores(model, tok, it["prompt"], it["swap"],
                                          device),
                       "E4_order1": _e4_choice(model, tok, ids_ab, it["prompt"],
                                               it["true"], it["swap"], device),
                       "E4_order2": _e4_choice(model, tok, ids_ab, it["prompt"],
                                               it["swap"], it["true"], device)}
                row = G.stamp_raw(row, my_sha)           # B9 要件3
                fh.write(json.dumps(row, ensure_ascii=False) + chr(10))
            fh.flush()
            del model
            torch.cuda.empty_cache()
            print("  dose %d 完了" % dose)
    finally:
        fh.close()
    print("**段5 raw 完了: %s(%d 行)**"
          % (out_path.name, sum(1 for _ in open(out_path, encoding="utf-8"))))
    return {"raw": out_path.name, "sha256": sha_file(out_path),
            "startup": {"identity": startup["identity"]["verdict"]},
            "frozen_at": frozen_at}


def main() -> int:
    print("**INSTRUMENT-0 段5 runner**")
    print()
    print("  段3 manifest: %s" % ("**在る**" if STAGE3_MANIFEST.exists()
                                  else "**無い**"))
    assert_startup()
    return 0


if __name__ == "__main__":
    sys.exit(main())

# PREREG — INSTRUMENT-0 ENDPOINT VALIDATION **V5**

**状態: DRAFT。封印前。**
**V1 / V2 / V3 / V4 は編集せず残す。**本書は Fable 裁定 R01〜R20 を条文化した V4 に、**素材の schema 移行(V3)と cohort 記述の訂正**を反映した新 version。
**本測定 BLOCK と `AUDIT_CONTROL_ONLY_EXECUTION_BLOCKED` は維持したまま作成した。**

**新規学習ゼロ。生成なし**(teacher-forced と再集計のみ)。

## 0. 由来と、V4 から何を変えたか

| 出典 | SHA256 |
|---|---|
| `FABLE_BLOCK_RULING_INSTRUMENT0_V1.json` | `802b799bb5a221d39872788734e880dc27907ebcf09085544ad78862192fc44c` |
| `FABLE_V4_PRECHECK_V1.json` | `bd267e47255a434dc4075f1cc48d52f7203e593e4f2098a2dc1b61cea581b783` |
| `FABLE_V4_RECONCILIATION_V1.json` | `aa439855308860fd3cf98db92a05626d3fa5e1817bd323471ed8cf5b8177c32a` |

**GPT 助言は `CODEX_ADVISORY_NONBINDING`。**対立 3 件は Fable が裁定した(§0.3)。

### 0.1 用語(**R16。全文でこの定義に統一する**)

> **adapter checkpoint 8 本(d16 / d32 / d48 / d64 / d96 / d128 / d160 / d192)
> + base(d0)= 評価点 9。**

**「9 checkpoint」とは書かない。**adapter は 8 本である。

### 0.2 範囲宣言(**R19**)

> **p 値は計算しない。全行は事前固定スケールとの閾比較である。
> primary contrast は endpoint ごとの d0 対 d192 のみ。
> 隣接 dose 比較は記述量であり、主張を持たない。**

### 0.3 対立 3 件の決着(**Fable 裁定。GPT は非拘束**)

| # | 争点 | 決着 |
|---|---|---|
| C1 | 反復数 K | **全数列挙。**K 増加ではない(§4.2) |
| C2 | `>` か `≥` か | **判定族で分離**(§4.6) |
| C3 | 飽和境界 | **固定定数 + 両側 guard。**CI 規則は本 cohort で飽和検査を無効化するため棄却(§6) |

---

## 1. 問い

**Day 1 で使う各 endpoint は、既知陽性(d0 対 d192)を分離し、既知陰性で沈黙するか。
分離できるなら、その最小分離段と実測ノイズ床はいくらか。
そしてその分離能力は実用上意味のある差に届いているか。**

---

## 2. 素材(**R01 / R02。二正本構造**)

### 2.1 二正本

| 正本 | 何の正本か |
|---|---|
| **`INSTRUMENT0_COHORT_CANDIDATE_V3.json`**(**承認 + SHA 固定後**) | **所属と 3 区分** |
| **`STUDY56_SWAP_MAPPING_V3.json`**(`raw_bytes_sha256 856a060d3f7be0375e205647c75af6038cc155f84e6551f3aacb81ebd579dfca`) | **TRUE↔SWAP 対応と per-item completion SHA** |

**V4 は V2 を指していた。V5 は V3 を指す。**
V2 の `tokenizer` キーが資格情報スキャナに発火し、**版管理へ入れられなかった。**
操作者裁定により、例外票ではなく**新 version への決定的 schema 移行**を採った(`SWAP_MAPPING_V2_TO_V3_RECEIPT_V1.json`)。
**変更は `tokenizer` → `text_codec_source` の 1 件のみ。**値・キー順・mapping 本体は不変。

**錨は二本立てである。**

- **ファイル実体の同一性**: `raw_bytes_sha256`。V3 = `856a060d…`
- **schema 跨ぎの意味の同一性**: `mapping_listing_sha256` = `d26cf3ac…`。**改名で raw_bytes は変わるが listing は変わらない。**V2 と V3 で listing が一致することが、**移行が科学に届かないことの直接証拠**である

**この値の生成手順(M4)は次で確定する。**`MAPPING_LISTING_SHA_PROCEDURE_V1.json` / `mapping_listing_sha_procedure_v1.py`:

1. `mapping` 配列を `target_completion_sha256` の**昇順**で整列
2. 各行を `target_completion_sha256 + "->" + swap_completion_sha256` へ整形
3. **LF** で連結(**CRLF ではない**)
4. utf-8 encode して sha256

**caveat: この値は手順を特定しない。**576 変種のうち 2 件が一致する(ファイルが既に target 昇順で保存されているため `file_order` と `sort_by_target` が縮退する)。
**引用時は必ず上記 canonical_procedure を併記すること。**

**V2 の扱い。**`STUDY56_SWAP_MAPPING_V2.json`(`raw_bytes_sha256 aa11944dd4768141601307073abe6f32b51e9b0c598a80ede3d685f43772a1ab`)は**未追跡のまま事故証拠として保持し、変更も commit もしない。**
**V3 から逆変換して元 V2 のバイト列をバイト一致で再現できる**(直列化 `indent=1, ensure_ascii=False, CRLF, 末尾改行なし`)。
**同一性 receipt の R1 は V2 ファイルの存在を要求せず、V3 からの in-memory 再構成で `aa11944d…` を照合する。**

**両者の同一性 receipt**(slug 集合・`items_per_slug` 分布)を**機械生成し、§11 段3 の凍結対象に含める。**
実装は `instrument0_identity_receipt_v1.py`、出力は `INSTRUMENT0_IDENTITY_RECEIPT_V1.json`。**手入力欄は無く、fail-closed である。**

**cohort V3 は `CANDIDATE_UNAPPROVED` のままでは正本にならない。**承認と SHA 固定が先行条件。

### 2.2 使う cohort

- **主解析: `ALWAYS_UNSEEN_COHORT`(16 slug / 29 item)。主推論単位は slug、n=16**
- `ALWAYS_SEEN_COHORT`(9 slug)と `EXPOSURE_TRANSITION_COHORT`(4 slug)は**主解析に入れない**

### 2.3 E4 テンプレート(**literal。R02**)

> `prompt + 候補 A / 候補 B(gold と swap)+「正しい続きは A か B か。答えは一文字。」`

出典: `PREREG_P1I_ACQUIRED_VS_EXPRESSED_V1.md`(T2 強制選択の固定単一テンプレート)。
**テンプレートの逐次変更・条件対応表は作らない**(dual-use 境界)。

### 2.4 §11 段3 の凍結対象に列挙するもの(**R02**)

E4 テンプレート文字列 / **`text_codec_source` path**(V2 の `tokenizer` を改名)/ **プロンプト書式** / **max length** /
cohort V3 / SWAP mapping **V3** / 同一性 receipt / 実装コード / config / fixture / runner / seed。

**Fable 査読による追加(`FABLE_COHORT_V3_REVIEW_V1.json` freeze_targets):**

1. `data/dev_v1.jsonl` の raw bytes(`bb4dc1c8c58f57ffc1fcb5d14bc568e962ef95675f8e612f6492ebde6e73b4c9`)。**V3 の区分は slug 名しか持たず、29 item の実体はこのファイルへの参照で決まる**
2. `COHORT_ROLE_SEPARATION_V1.json`(`4a4df9c730998cf893bd088dcb0e1d2b34b02c2d14aee3963424b0e2e043d8cd`)。**cohort を生成した規則そのもの**
3. **`STUDY56_SWAP_MAPPING_V3.json`(`856a060d…`)を凍結する。**
   V4 の記載は「V2 を `aa11944d…` で凍結」だったが、**V2 は版管理へ入れられないため実行不能となった。**
   `aa11944d…` は**事故証拠および再構成の照合標的**として残る
4. `delta_support_v1.py`(`dcb02794edf47a3c1e54fdac78f7b6afeed0c1ec8c2d249a62bb5dedb3a5cf3a`)
5. `DELTA_SUPPORT_TICKS_V2.json`(`195bd840d884bf7c6849dd4e7eb964e2a9d775ef6a4422be8243824eece0bd12`)
6. **同一性 receipt の生成スクリプト**(receipt 出力と対で)
7. **近似重複の余裕実測**を承認記録に数値で固定する

**注記:** F_dose 8 本の raw SHA は凍結される V3 本文が内包するため、V3 の承認後バイト列を凍結すれば転写なしで固定される。

### 2.5 算出法

- **集約単位は slug(16)。**item は slug 内で反復であり独立でない
- **中央値は `statistics.median`(偶数長では中央 2 値の平均)に統一する**(**R09**)。
  上側 / 下側中央値は用いない。**偶数長 fixture の期待値は本規約から先に数値で書く。**
  **表示丸めを判定に流入させない**
- **E4 の例外(R17)**: **E4 は slug 内平均を連続 score とする**(有界 score のため)。
  16 slug を**等重み**で集約
- E1 は **token 数で正規化**(`loss_sum / n_tokens`)
- E3 は `logsumexp(logP(151645), logP(151643))`。**pad 右詰めを停止と数えない**
- E4 は両順序を実行し**順序平均**

### 2.6 除外規則(**R08。優先順位を一意化**)

**適用順**:

1. **item 単位の非有限値(nan / ±inf)は §2.6 の除外経路のみ**に載せる。行1 へ流さない
2. `n_tokens < 8` の item は E1 から除外
3. **行1 が見るのは、集約後に残った異常 + checkpoint 読込失敗 + SHA 不一致**のみ

**除外率**: **分母 = 29 item × 9 評価点 = 261(endpoint ごと)。> 10% で STOP。**
**slug 基準率(/144)は参考併記。**

**追加 guard(R08)**: **primary contrast で全 item が除外された slug が 1 つでも生じた endpoint は、
率にかかわらず即 `INSTRUMENT_STOP`。**率はどの分母でも希釈されうるため。

**「検討」「望ましい」「原則」「適宜」「できれば」を本文に置かない。**封印直前に grep で機械確認する。

---

## 3. 保存する raw

item × 評価点 × endpoint の全値 / 置換・分割の対応表 / **全数列挙の順序統計量** /
checkpoint・素材・評価器・prereg の SHA / **除外された item の一覧と各除外理由**。

---

## 4. Primary endpoint と、その決め方

### 4.1 量の定義

- `SEP_max` = **d0 対 d192** の slug 中央値差(E2 は d0 の選好そのもの)
- `NULL_scale` = **`max(|置換 null の中央値|, split-half 差の絶対値の 95% 点)`**(単一式)
- `DR = |SEP_max| / NULL_scale`
- `MIN_STEP` = 隣接 dose 対のうち `|差| > NULL_scale` を満たす最小用量差

### 4.2 split-half null(**R03。全数列挙**)

**16 slug の非順序 8/8 分割は全 6435 通り。これを全列挙する。**
**95% 点 = 6114 番目の順序統計量。厳密・決定的・seed 不要。**

**split-half が作用する量は、`SEP_max` と同一の per-slug primary contrast 値である。**

### 4.3 置換 null(**R04**)

**次の 3 要件を満たしたときだけ「検査した」と数える:**

1. **何をどの階層で置換するかを明記する**
2. **交換可能性の論証を書く**
3. **段1 fixture で、検出力と沈黙の二方向を数値で証明する**

**標本抽出が必要な場合**: K=5000 / **保守側上位順序統計量**(`k/(K+1) ≥ 0.95` を満たす最小 k)/
**補間なし** / seed **20260931** 固定。

**E1 / E3、および要件を満たせない endpoint は
`PERMUTATION_NULL_STRUCTURALLY_NOT_TESTED` を出力し、claim を制限する。**
**構造的沈黙を「null 沈黙」として合格に数えない。**

### 4.4 `NULL_scale` が 0 または非有限のとき(**R05**)

**`UNDEFINED_ENDPOINT`。**`DR` / `MDE` / `MIN_STEP` は **null 出力**。
**他 endpoint に影響させない。素材は保全する。**

**禁止**: **ε の導入 / 分位点の切替 / 尺度の切替。**

### 4.5 MDE(**R06**)

**`MDE = NULL_scale × 2`。**

**導出**: 片側 α=0.05・検出力 95% の正規近似 `(z_α + z_β) × SE ≈ 3.29 × SE` に対し、
**split-half スケールは全標本 SE より大きいため、係数 2 でも保守側に外れる。**

**結果閲覧後の係数変更は、いかなる方向でも新 version + 未接触データを要する。**

### 4.6 演算子表(**R07。判定族で分離**)

| 族 | 対象 | 演算子 |
|---|---|---|
| **実用境界** | Δ 対 SESOI / `effective_decision_cutoff` / `MDE ≤ SESOI` | **包含(`≥` / `≤`)** |
| **検出・主張** | `MIN_STEP` の `|差| > NULL_scale` | **厳密 `>`** |
| **防御・停止** | 行2 発火 / 除外率 / 飽和 guard | **等号で発火** |

**原理: 主張は厳密超過、防壁は等号で落ちる、実用境界は定義により包含。**

V3 既存の演算子(`DR ≥ 3`、除外率 `> 10%`)は**逐語維持**。
`effective_decision_cutoff` は **`delta_support_v1.py` の完全 support 配列から探索**する
(mean 側 `support_sha256 faea5286c1dc2fa9fd4f9efd07159568a3b8d028ed3c0132696b3a6585f09f0e`)。

### 4.7 Phase 0 が測るもの / 測らないもの

| 量 | Phase 0 で実測するか |
|---|---|
| 観測ノイズ / 再現性 / 分解能 / **MDE** | **する** |
| **SESOI** | **しない。測定から決まらない** |

**禁止: `SESOI = 観測ノイズから自動算出`。**

### 4.8 SESOI の現状(**R20**)

- **E3 のみ SESOI を置ける**(cap 256 で終端確率が 50% を跨ぐ停止 logP 変化量)
- **E1 / E2 / E4 は SESOI 不在。**したがって**行4 / 行6 は E3 のみ**に適用し、
  **E1 / E2 / E4 は行5 経路**へ落ちる
- **後日の SESOI 設定は、新 version + 未接触データを要する**

---

## 5. Secondary(成功判定に使わない)

9 点用量曲線の形 / STUDY19 の d0 接地点 / 凍結 raw からの終端率 run 分散下限。

---

## 6. 事前分岐(**上から評価し、最初に該当した行で確定**)

| # | 行 | 条件 | 次の一手 |
|---|---|---|---|
| 1 | `INSTRUMENT_STOP` | 集約後の残余非有限値 / checkpoint 読込失敗 / SHA 不一致 / 除外率 > 10% / **全 item 除外 slug が 1 件でも** | 修理のみ。判定しない |
| 2 | `NULL_FAIL` | 置換 null が **等号で発火**する水準に達する | **構造以外を拾っている。**Day 1 で使用禁止 |
| 2.5 | **`SEPARATES_WRONG_DIRECTION`** | **`sign(SEP_max)` が期待と逆 かつ `|SEP_max| > NULL_scale`**(片側) | **使用禁止。計器 / ラベル検査へ** |
| 3 | `FAILED_FLOOR_CEILING` | §6.1 の飽和条件 | **動作域を明記し、域外の用量比較を除外** |
| 3.5 | **`UNDEFINED_ENDPOINT`** | `NULL_scale` が 0 または非有限 | **BLOCK。素材は焼かない** |
| 4 | `VALIDATED_AND_PRACTICALLY_ADEQUATE` | `DR ≥ 3` かつ null 沈黙 かつ **`MDE ≤ SESOI`**(**E3 のみ**) | 使用可。**実測 MDE を記入** |
| 5 | `VALIDATED_BUT_PRACTICAL_BASIS_MISSING` | `DR ≥ 3` かつ null 沈黙 だが SESOI 不在 | 使用可。**ROPE 感度分析表を添付**し単一閾値を書かない |
| 6 | `UNDERPOWERED_FOR_PRACTICE` | `DR ≥ 3` だが **`MDE > SESOI`**(**E3 のみ**) | 増強設計が要る |
| 7 | `WEAK` | `1 ≤ DR < 3` | 使用可だが増強を先に設計 |
| 8 | `NOT_SEPARABLE` | `DR < 1` | 使用禁止。代替計器の設計へ |

### 6.1 飽和の数値基準(**R11**)

- **比率型 / `k/n` 型**: `k == 0` または `k == n`(`n ≥ 4`)
- **連続型 E3**: **天井 −1.0 nat / 床 −20.0 nat**
  - **天井の由来**: `eos_logp_final` の実測張り付き帯の下端 **−0.630 の整数切り下げ**という規則
  - **床の由来**: **先行値なし。暫定定数である。**
    **V3 が書いていた「−22〜−25 帯」は `eos_logp_mid` の値であり、E3 が測る位置ではない。
    この由来行は削除した**(R12 と同型の混線を、それを直す条文で再演していた)
- **両側 guard**: **`床 < logP_observed_base < 天井` を receipt 値で機械検査。
  不成立なら `INSTRUMENT_STOP`**

### 6.2 期待符号(**R10**)

| endpoint | 期待 |
|---|---|
| E1 | d192 で **NLL 減** |
| E2 | d0 で **TRUE 選好 正** |
| E3 | **停止 logP 増** |
| E4 | **正答率 増** |

---

## 7. Sentinel

d0 × 2 slug × 全 endpoint のみ先に実行し、raw 充足・**決定性**・置換対応表の整合を監査。
**異常 1 件で停止。規則が裁量を要したら規則を先に直し、試適用の結果は捨てる。**

---

## 8. 資源

TF 評価 90 分 / STUDY19 probe d0 5 分 / 再集計は CPU。**合計上限 120 分。**
**訓練ゼロ・生成ゼロ。**GPU 単独占有 1 枠。anomaly 1 件で即停止。

---

## 9. Claim ceiling

生成系 endpoint は validate していない / モデル一般でない / 素材は dev_v1 由来の 16 slug に限る /
**E3 の SESOI は毎 token 独立近似に依る保守的な目安** /
**E1 / E2 / E4 に SESOI は無い** /
**素材同定は `HISTORICAL_RUN_BYTES_NOT_CRYPTOGRAPHICALLY_ATTESTED` の制約下にある。
Phase 0 の計器校正には使えるが、exact reproduction・因果確証には使えない**。

**封印そのものの主張上限(操作者指定 2026-08-16):**

本書は `seal_gate_v3` で封印する。同ゲートの到達点は
**`HANDLE_BOUND_PATH_VERIFICATION_WITH_DOCUMENTED_RESIDUALS`** までである。
**`TOCTOU_ELIMINATED` とは書かない。**

- fixture 実測: **PASS 19 / FAIL 0 / SKIP 1**(SKIP は file symlink 作成の特権が無いため。reparse 類型自体は junction で拒否を実測)
- **`SEAL_GATE_V3_DESIGN_NOTE_V1.md` §4 の残余 8 件を併記する。**
  特に **W6 と receipt 書込みの間の窓**、**事前作成された書込可能 file mapping section 経由の書換え**、**封印後の改変**は v3 でも閉じない
- **TOCTOU 窓は狭まったが消えていない。**防いでいるのは差替えの発生ではなく、**別実体を掴んだまま封印が成立すること**である

**cohort 記述の訂正(Fable 査読 M2 / M3。`COHORT_CLAIM_CORRECTION_V2.json`):**

- **M2。**閾値固定の主張を格下げする。正しい label は **`THRESHOLD_FIXED_BEFORE_APPLICATION_BUT_AFTER_MATERIAL_INSPECTION`**。
  「素材を見る前に固定」は**記録と矛盾する過大主張**である(dev・F_dose とも規則固定前に既読、29/16 も既知だった)。
  **結論自体は機構で成立する。**調整可能な層(正規化・閾値)は除外に 1 件も寄与せず、**発火は slug 層のみ。**
  実測最大 Jaccard は **0.083481**(閾値 0.5 の約 6 分の 1)であり、**閾値を (0.084, 1.0] のどこに置いても membership は不変**である
- **M3。**cohort V2 の `exact_completion: 0` は **first-hit 集計の産物**であり、**『逐語一致が無い』ではない。**
  実測では **SEEN 18 item のうち 15 item が逐語で訓練和集合に存在する。****positive control としてはむしろ強い性質である**

---

## 10. Gate

地図改訂の承認(取得済)/ 二者査読 / prior-work note(**封印より先**)/
計器テスト PASS / NOVELTY receipt / STUCK_GATE / GPU 単独占有 / **封印 SHA → 初回推論**。

**§11 段3 の凍結と、B9 / B10 の実装完了が先行条件。**

---

## 11. 実行手順

### 段1 — 合成 fixture(**R13。B10 の 6 種を規範として列挙**)

**答えの分かった人工データのみ。対象データに触れない。**

1. **TRUE/SWAP 腕取り違え**(符号既知の人工分離で符号照合)
2. **E3 位置 off-by-one**(末尾直後 index を既知 logP で照合)
3. **pad 右詰め混入**
4. **E4 順序バイアス**(順序平均で消えるべき人工バイアス)
5. **決定性ハーネス**(同一バッチ構成 2 回 forward。**決定性 config と固定バッチ計画を段3 凍結対象へ**)
6. **分母確定後の除外境界**

加えて **A4 型**(偶数長中央値)/ **A5 型**(母集団対応)/ 欠損 / NaN・Inf / 境界値。
**各 fixture の期待値は本文の規約から先に数値で書き、段3 で SHA 凍結する。**

**置換 null の検出力・沈黙の二方向証明(§4.3)もここで行う。**

### 段2 — 代理データ互換試験(**R14**)

**代理**: `STUDY56_MATCHED_COUNTERFACTUAL_RAW_V2.json` + STUDY55 / 57B 凍結 raw。

**「同一 schema」とは書かない。「同一 29 item・同種の値種」とする。**

**段2 の合格条件**: **代理データに対し、読込・集約・除外・null 構成の全経路が例外なく走り、
fixture 期待値と矛盾しないこと。**

**凍結 55 件は読込経路の互換試験に限る。**

### 段3 — 計器一式の凍結

§2.4 の列挙物すべてを `make_prereg_freeze_manifest_v1.py` + `freeze_guard_v1.py --protect` で凍結。

### 段4 — 予測票の封印

Fable と Opus が確率予測を提出し、**適用より前に**凍結する。

### 段5 — 本測定(**R15**)

**`KNOWN_ITEMS_WITH_UNOBSERVED_9_CHECKPOINT_X_4_ENDPOINT_OUTCOME_MATRIX` へ一度だけ適用。**

**素材は既閲覧である。未観測なのは測定行列だけ。**
prior-work note に**既閲覧集約値の blindness 宣言を必須項目として置く。**

### 段6 — 欠陥判明時は修理せず `INSTRUMENT_STOP`(**R13。B9 の 4 実装要件**)

1. **段3 は `make_prereg_freeze_manifest_v1.py` + `freeze_guard_v1.py --protect` を名指しで使う**
2. **runner は起動時に自身・config・fixture の SHA を段3 manifest と照合し、
   不一致なら非ゼロ終了で実行拒否**
3. **全 raw に instrument SHA を刻印し、集計・判定器は刻印 ≠ 封印 SHA の raw を自動 INVALID とする**
4. **欠陥検出時の分岐は STOP 一本道。許容差の緩和・再試行の経路をコードに存在させない**

**B9 / B10 は実装・検証完了まで `UNRESOLVED` のまま封印・実行 gate に数える。
条文列挙だけで `RESOLVED` にしない。**

---

## 12. advisory 受領手順(**R18**)

**GPT 助言の受領記録には、内容 SHA256 を全 64 桁で記載する。**
**ファイル名 prefix と内容ハッシュの不一致は受領時に検知して差し戻す。**

制定の契機: 当方が `[:32]` に切り詰めた値を完全な SHA として Fable へ渡し、
**照合不能な識別子で査読を依頼した。**

---

## N2 / N3 / N4

- **N2**: 狭める**未知境界**は「4 endpoint は、効かないものを測ったのか、測れない計器だったのか」の分離。
  **加えて、分離できたとしてそれが実用差に届くか(`MDE ≤ SESOI`)はどの台帳にも無い。**
- **N3**: §6 の 10 行すべてで Day 1 各 prereg の閾値と使用可否が機械的に決まる。
  **いずれの結果でも次の一手が変わる。**
- **N4**: **実用**として、以後の全実験の閾値が「暫定」から「実測校正」へ変わる。
  **識別力**として、「効果が無い」と「計器が届かない」を分離する。

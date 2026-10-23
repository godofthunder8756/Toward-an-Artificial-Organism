# Fable Paper C 独立査読依頼 V1

## 1. 対象

次の二ファイルを日英の本文査読対象とする。英語版を将来の主版、日本語版を補助版とする。

- `PAPERC_MANUSCRIPT_V1.md`
- SHA-256: `a35f3a10b045e6b17f1789fbe43858d1b1df43c46bcfdafc886e92a3f496d25f`
- bytes: `31235`
- `PAPERC_MANUSCRIPT_EN_V1.md`
- SHA-256: `7d09fda42be817c959554ac02cdf597bf2792a2ca56291c45104b60d750f543a`
- bytes: `31567`
- 両版の状態: `B_NONPUBLIC_DRAFT`

いずれかの対象SHAが一致しなければ査読せず、`TARGET_SHA_MISMATCH`で停止する。

## 2. 根拠資料

| ファイル | SHA-256 |
|---|---|
| `PAPERC_CLAIM_EVIDENCE_V1.json` | `16be14818ee955bf6f3ad7e072ee41ff0b89ca81f38568c9dc87e1f255b6ed61` |
| `PAPERC_ONE_PAGE_DESIGN_V1.md` | `d4ec354cf5a6fd2ad56cc069d8d557f015171d635faa076340e3a3aa2e229451` |
| `INSTRUMENT0_DISCLOSURE_CLASSIFICATION_V1.json` | `8148a03127a6dcf8e6699f273fc9ebb8a5b285f14e20e97257bf50aa3907d245` |
| `PAPERC_INDEPENDENT_RECOMPUTE_CODEX_V1.json` | `92dbe74b6eece946c89d9676117ce6ff24427a25c3e0313bf3f3fa5cb61fe5dc` |
| `paperc_independent_recompute_v1.mjs` | `84ed2472826ec833f1a9e295499c2dc6a07bd4901bdbae0b5ae7a34409ce7442` |
| `PAPERC_EXTERNAL_LITERATURE_RECEIPT_V1.json` | `9b672d6f547dd1eb903e938ac5e7843961a64e061c997c796b13156825452b79` |
| `PAPERC_BILINGUAL_FIDELITY_CODEX_V1.json` | `9281430c544daabde330eaa70334729df8fc6f5ed0beefe5d6fa5554dc819d67` |
| `paperc_figures_v1/PAPERC_FIGURE_MANIFEST_V1.json` | `88b099b5d060ec0fcffbf5316fd8f9e03142080c4464b801916e97084f73cfec` |
| `paperc_figures_v1/PAPERC_FIGURE_DATA_V1.json` | `27aacee62542eef1f384f70da2f29e40e2042e8ee66f88683a1a9d29dd13b496` |
| `PAPERC_FIGURE_VISUAL_QA_V1.md` | `11c592bb6b90e986c642e2b5dc0b7929a270095056cfc78568eca37de3aa9cbe` |
| `PAPERC_PREFLIGHT_CODEX_V1.json` | `b937011037a208f215c034d0888d8c94a87d38e0d26b8431b79542b5506107f6` |
| `INSTRUMENT0_STAGE5_RAW_V1.jsonl` | `2ff33a4d62c246361c1864b2a6c61dd6c28260a3e4cbb808c0f5be519048cfc6` |
| `INSTRUMENT0_STAGE5_RESULT_V1.json` | `d648b89b0ef709f6c23d1d7e9b24d73f833a1b61acf1866b33e237870a5ec3b6` |
| `PREREG_INSTRUMENT0_ENDPOINT_VALIDATION_V5.md` | `5e19341f30a8b92bc97e177d7b3a25ff01d6f6a13e0c7bc780e4e881278fb0bf` |
| `INSTRUMENT0_PAPER_DISCLOSURE_OBLIGATION_V1.json` | 現物から査読時に再計算 |
| `STAGE4_PREDICTION_SEAL_V1.json` | 現物から査読時に再計算 |

## 3. 査読範囲

### A. 数値と推論単位

- 保存済みresultを入力にせず、261 raw行から主要値を独立再導出する
- 29 itemを独立標本として扱っていないか確認する
- 16 slug等重み、通常中央値、E4 slug内平均を確認する
- 非順序8/8分割6435通りと6114番目の順序統計量を確認する
- E1〜E4のSEP、NULL_scale、DR、MDE、床・天井、分岐行を確認する
- E4の261/261両順Aとitem score 0.5をrawから確認する

### B. 主張天井

- 本稿が計器検証を蒸留効果、因果機構、一般化へ昇格させていないこと
- E2を「効果なし」、E4を「一般に使用不能」と読んでいないこと
- E3の天井−1.0を物理的上限としていないこと
- E1の行外STOPをendpoint検証成功へ読み替えていないこと
- 予測scorecardを予測者の一般的優劣へ拡張していないこと

### C. 開示義務

`INSTRUMENT0_PAPER_DISCLOSURE_OBLIGATION_V1.json`の7項目が、弱めず、欠かさず、本文に存在することを確認する。開示は免責として扱わない。

### D. 引用

- 外部一次文献4件の著者、年、題、識別子、本文での使い方を確認する
- Paper B DOIを確認する
- 「世界初」「直接先行なし」「文献全体に存在しない」という主張がないこと
- 照合範囲を越える引用がないこと

### D2. 日英忠実性

- 数値、分母、推論単位、分岐行、限定句、非主張が日英で一致すること
- 開示義務7項目が英語版でも弱められず、欠けていないこと
- 英語版だけに強い因果・一般化・新規性表現が追加されていないこと
- 英語版を主版、日本語版を補助版とする構成に矛盾がないこと

### D3. 図・グラフ・表

- 図1〜4のSVG/PNGをmanifestと全数照合し、rawから再計算した表示値と一致すること
- 図2の9評価点、16 slug、等重み中央値、d0対d192のprimary contrastを確認すること
- 図3のDRと最終分岐が、分離度だけをendpoint妥当性へ昇格させていないこと
- 図4の実現行への封印確率を、予測者の一般的優劣へ拡張していないこと
- 日英各3表（endpoint集約、支持／非支持境界、予測scorecard）の数値と限定句が一致すること
- 図注が本文の主張天井と一致し、色だけに意味を依存せず、欠落・重なり・切れがないこと
- figure dataを保存resultの単純転記でなく、primary rawからの独立再計算へ突き合わせること

### E. 公開境界

- 本稿、段5結果、付随成果物はB・非公開のままであること
- C候補不在をAへの自動昇格に使っていないこと
- FableのPASSを公開権限として書いていないこと
- 公開版固定と操作者の明示判断が未完であること

## 4. 出力

次を新規ファイルとして出力し、本文・根拠資料を編集しない。

- `FABLE_PAPERC_DRAFT_REVIEW_V1.json`

必須項目:

- `target_files`, `target_sha256`, `target_bytes`
- `PUBLICATION_BLOCKER`配列
- `NON_BLOCKER`配列
- `numeric_recompute`
- `claim_ceiling_review`
- `disclosure_7_of_7`
- `citation_review`
- `bilingual_fidelity_review`
- `figure_table_review`
- `classification_review`
- `verdict`

許容する最上位判定は`PASS_FOR_OPERATOR_CONSIDERATION_OF_PUBLICATION_FREEZE`である。これは公開、アップロード、B→A昇格の権限を与えない。blockerがあれば`FAIL_BLOCKERS_PRESENT`とする。

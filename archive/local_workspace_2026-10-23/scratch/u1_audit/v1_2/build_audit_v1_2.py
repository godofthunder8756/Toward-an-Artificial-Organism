import hashlib, sys
sys.path.insert(0,'/workspace/scratch/astra29'); from common29 import *
SRC='/workspace/review/u1_substrate_audit_v1_1.md'; DST='/workspace/review/u1_substrate_audit_v1_2.md'
raw=open(SRC,'rb').read(); assert hashlib.sha256(raw).hexdigest()=='3d9bbde3644e15d81f2489c15cd6b68c07c93590097c95ef959b79758cd96373'
s=raw.decode()
def rep(a,b,n=1):
    global s; c=s.count(a); assert c==n,(c,a[:80]); s=s.replace(a,b)
rep("# U1 substrate audit v1.1: applying","# U1 substrate audit v1.2: applying")
rep("**v1.1 (2026-10-21, about 12:11 PM–1 PM ET).**",f"""**v1.2 (2026-10-21, about 2:22–3 PM ET).** Built from v1.1 (`u1_substrate_audit_v1_1.md`, sha256 `3d9bbde3644e15d81f2489c15cd6b68c07c93590097c95ef959b79758cd96373`, left unchanged) by `/workspace/scratch/u1_audit/v1_2/build_audit_v1_2.py`. It applies Astra consult #29 {C29}. Paper only. Nothing was executed except read-only `git fetch`/`git show`, `sha256sum`, `grep` and document checks, including one read-only parse of stored output rows (§4.2). Changes are listed in §11.

**Track A status (Astra #29 edit E29-6, verbatim):**
> {E296}

Astra #29's verdict on Track A (verbatim): {VERD}

{SEP} This audit concerns the AC lineage only.

**v1.1 (2026-10-21, about 12:11 PM–1 PM ET).**""")
rep("**EXTERNAL COORDINATION (supplied targeting)**, per Astra #28 (§4.1). v1 had this as SUBSTRATE, contested |",
"**EXTERNAL COORDINATION (supplied targeting), PROVISIONAL** (v1.2). This was Astra #28's provisional judgment on the supplied description. The code evidence is this audit's own, in §4.2; it is not an Astra code certification. v1 had this as SUBSTRATE, contested |")
rep("I10, I12 (supplied targeting), I13 policy.","I10, I12 (supplied targeting, PROVISIONAL), I13 policy.")
rep("the exclusion list `reg_offs + streak_offs`, resolved by the host at acquisition","the exclusion list `reg_offs + streak_offs`, computed by the host at acquisition")
rep("or competition would be resolved by a generic law,","or competition would be handled by a generic law,")
rep("Competition is resolved by host list order.","Competition is settled by host list order.")
rep("**I12 Action semantics: primitives SUBSTRATE (I12-p); birth targeting EXTERNAL COORDINATION (supplied targeting).**",
"**I12 Action semantics: primitives SUBSTRATE (I12-p); birth targeting EXTERNAL COORDINATION (supplied targeting), PROVISIONAL (v1.2, §4.2).**")
rep("- v1.1 therefore classifies I12 as **EXTERNAL COORDINATION (supplied targeting)**. The code-level explanation is in §4.1.",
"- v1.1 therefore classified I12 as **EXTERNAL COORDINATION (supplied targeting)**. The code-level explanation is in §4.1.\n- v1.2: the classification is **PROVISIONAL**. Astra #29 says its #28 judgment rested on the supplied description. §4.2 states exactly what this audit's own code reading shows and does not show.")
rep("## 5. Revised closure sentence",f"""### 4.2 Status of the I12 judgment (v1.2): PROVISIONAL

**Astra #29 (verbatim):** {PROV}

So I12 is **PROVISIONAL**, and Astra #28 is not cited here as a code certification. The evidence below is this audit's own read-only reading of the code at the cited commits, plus one parse of stored output rows. Astra has not reviewed it.

**What the code shows.**
1. **The AC105 step runs `ac9.step`'s source with this line unchanged.**
   - `STEP_SRC=inspect.getsource(ac9.step)` (`ac12.py:L64@5b06281`). `ac95.build` compiles that source (`ac95.py:L817-L840@a1b9759`), and AC105 uses it (`ac105.py:L177-L178@8f0218a`).
   - `build` replaces exactly five named strings: the renewal block, the outcome line, the damage line, the action line and the balance line. None is the bank-list line, so `ac9.py:L108@6c6323b` runs unchanged on the AC105 path.
2. **The step intercepts action 6 before the generic reaction** (`ac9.py:L85-L112@6c6323b`, with the `ac4.react` fallback at line 112).
   - The generic `ac4.react` action-6 branch treats every group alike: `groups=range(4) if action==6 else [4]` (`ac4.py:L97-L98@6c6323b`).
   - `ac9` replaces that uniform rule with a host list: bank 0 always, bank r+1 only when memory region r has an occupied site, and bank 3 never.
3. **Other host code ties bank indices to functional roles.**
   - W group `4*bank`…`4*bank+3` catalyses repair of `traces[bank]` (`ac4.py:L89-L92@6c6323b`).
   - W group r+1 catalyses renewal of memory region r, through `a[4*(r+1):4*(r+2)]` (`ac12.py:L67-L69@5b06281`).
   - `traces[0,:126]` holds the program (`ac12.py:L80@5b06281`). In AC105, `traces[1]` holds the description (`ac105.py:L169@8f0218a`).
4. **`demand()` on the AC105 path is the `ac9_memory` method** (`ac9_memory.py:L26-L27@6c6323b`). The AC105 organism comes from `ac12.acquire` (`ac105.py:L161@8f0218a`), which calls `ac9_priority_v2.acquire` (`ac12.py:L94-L107@5b06281`). That calls `ac9.acquire` (`ac9_priority_v2.py:L11-L15@6c6323b`), which builds `mem.Memory.empty()` (`ac9.py:L23-L26@6c6323b`), with `mem` = `ac9_memory` (`ac9.py:L9@6c6323b`).

**What this establishes.** The bank list is written in host code, not in declared content. It decides which functional W groups receive births: the program-repair group always, and the memory-renewal groups when memory is occupied. In that limited, code-level sense the implementation performs semantic host targeting.

**What the code does not show.**
- **Necessity.** It does not show that this targeting is necessary for any reported W/C/B result. That is a Q-NECESSITY question; only a run could settle it (NEEDS-APPROVED-RUN). No run is proposed, because Astra #28 directs no further closure runs on the unchanged architecture.
- **Intent.** It does not document the designers' intent. "Semantic" here means the functional roles that other code assigns to each bank index.
- **A role mismatch, noted but not assessed.** In AC105, the bank-1 W group also catalyses repair of the description trace (`traces[1]`). Yet bank-1 births are triggered by memory-region-0 occupancy, not by any description state.
- **Where bank-1 parents come from.** `ac9.acquire` zeroes `life[4:16]`, and every birth needs a living parent in the same bank. The path that later populates bank 1 was not traced.
- **The per-bank split in AC105.** Stored AC95 rows (`ac95_results_v1/rows.jsonl` @ `a1b9759`, 136 rows) record 174978 W births: 87394 in bank 0, 87584 in bank 1 (region 0) and 0 in bank 2 (region 1). AC105 rows (`ac105_results_v1/rows.jsonl` @ `8f0218a`) do not store per-bank birth counts, so the AC105 split is UNVERIFIED.

## 5. Revised closure sentence""")
rep("- **I12 birth targeting** (ruled supplied targeting by Astra #28):","- **I12 birth targeting** (classified supplied targeting, PROVISIONAL; §4.2):")
rep("- **Q-A2 (I12 birth targeting): ruled supplied targeting.** I12 is reclassified EXTERNAL COORDINATION (supplied targeting) (§3, §4.1).",
"- **Q-A2 (I12 birth targeting): provisional judgment (Astra #28, on the supplied description).** I12 is classified EXTERNAL COORDINATION (supplied targeting), PROVISIONAL (§3, §4.1, §4.2). Astra #29: \"Do not describe #28 alone as an unconditional code certification.\"")
rep("## 9. Integrity\n","""## 9. Integrity

- v1.2 check script: `/workspace/scratch/astra29/check_e29.py` (log `check_e29.log`). It covers this file, triage v1.4 and synthesis v1.2. §11 lists what it checks.
- The v1.1 description below is retained.
""")
s=s.rstrip('\n')+f"""

## 11. Changes in v1.2 (Astra #29)

1. **E29-6 added verbatim,** with Astra #29's Track A verdict. This audit has no W-REL entries to replace.
2. **I12 marked PROVISIONAL** (§3, §4, §8). The new §4.2 sets out what the code itself shows and does not show, and Astra #28 is not cited as a code certification.
3. **Systems separation stated:** the AC lineage and the GRU-8 studies are separate systems and do not jointly establish one organism.
4. **Wording.** The three non-test uses of "resolved by" now read "computed by" (I10 exclusion list), "settled by" (§4.1, resource competition) and "handled by" (§4.1 sketch). This file has no proposed tests that used "resolved by".
5. **Unchanged:** the closure sentence, E28-1 and E28-2.

The check script `/workspace/scratch/astra29/check_e29.py` confirms:
- verbatim Astra #29 quotes;
- citations;
- no "resolved by" outside quotes;
- no UNRESOLVED-COMPUTE or attainability-check text outside the changelog and quotes;
- the closure sentence is byte-identical across the three files;
- forbidden phrases are absent;
- earlier versions are unchanged.
"""
open(DST,'w').write(s); print('ok')

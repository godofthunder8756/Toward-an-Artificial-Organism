# Resolution: predecessor files for the v1.3 consistency check

The deviation `review/DEVIATION_check_script_predecessors_absent.md` stopped re-execution of `scratch/gru_audit/check_gru_audit_spec_v1_3.py` because predecessor files it hashes were not in the checkout.

Those predecessors were added additively after the results, in commit `88c96f9c0e8bb3dee961db26d630d2ef9348073f`, which follows the results commit `7987a7203c438de918b47974220c5951ebd1b3dc`. None of them is in the sealed implementation manifest. `audit/gru_v1_3/IMPLEMENTATION_MANIFEST.json` (sha256 `72137e29229de7649eb6c8914de08fe34016424f05ba6902af3eed76b9d5c741`) lists only the 13 audit code files from the freeze and was not modified. The predecessor files are review records and earlier check scripts. They are not manifest entries.

After that commit, this checkout re-ran `python3 -B scratch/gru_audit/check_gru_audit_spec_v1_3.py`. `origin/pr/10` was available. The script's git directory is `/workspace/repo`, so a temporary symlink to this checkout was used for that process and was not committed. Result: 112 PASS and 0 failures. The stdout sha256 is `66f763d6eaf7a831b2b3904b458aee9f572af534a9bad1916f99372419aaa82a`.

The attached local re-run, `check_v1_3_rerun_output.txt`, has output sha256 `66f763d6eaf7a831b2b3904b458aee9f572af534a9bad1916f99372419aaa82a`. This checkout's stdout is byte-identical to that attachment.

No audit analysis was rerun. No sealed results file, deviation, or manifest was edited.

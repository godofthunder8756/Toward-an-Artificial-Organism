# Deviation: v1.3 consistency check predecessors are absent

Item stopped: re-execution of `scratch/gru_audit/check_gru_audit_spec_v1_3.py` to 112/112.

The check hashes predecessor files that were not part of the supplied attachment set and are not in this checkout, including `astra_consult32_response.txt`, spec v1, v1.1 and v1.2, their reviews, and the earlier check scripts. The script raises `FileNotFoundError` on the first missing path. Those files were not fabricated and the check script was not edited.

The supplied v1.3 spec, roster, Astra #33 text, standing-approval records, spot-check, inventory, pre-freeze constants and geometry script were committed byte-identical and their sha256 values were checked against the stated digests. This deviation does not change the audit rules.

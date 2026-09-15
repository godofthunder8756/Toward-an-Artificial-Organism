"""Recover completed raw rows after NumPy-bool report serialization failure.

No simulation/source/criterion changes. Preserve frozen runner hashes.
"""
import hashlib
import json
from pathlib import Path
import ac6_fixedrate as experiment

root=Path('ac6_fixedrate_results_v1')
rows=[json.loads(x) for x in (root/'rows.jsonl').read_text().splitlines()]
assert len(rows)==40
hashes=json.loads((root/'pre_run_snapshot.json').read_text())
assert all(hashlib.sha256(Path(k).read_bytes()).hexdigest()==v for k,v in hashes.items())
report=dict(hashes=hashes,rows=rows,summary=experiment.summarize(rows),
            report_recovery='All simulations completed; original writer failed to serialize numpy.bool_. Reconstructed from unchanged persisted rows, converting NumPy scalars to native scalars only.')
text=json.dumps(report,indent=2,default=lambda value:value.item())
(root/'results.json').open('x').write(text)
print(json.dumps(report['summary'],default=lambda value:value.item()))

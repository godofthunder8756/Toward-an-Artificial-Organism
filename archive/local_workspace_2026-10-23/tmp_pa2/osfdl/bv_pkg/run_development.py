
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from toe_exp.block5 import *
ROOT=Path(__file__).resolve().parent
recs=[dev_seed(s) for s in DEV_SEEDS]
agg=aggregate(recs)
(ROOT/"results"/"development"/"block5_dev_per_seed.json").write_text(json.dumps(recs,indent=2))
(ROOT/"results"/"development"/"block5_dev_aggregate.json").write_text(json.dumps(agg,indent=2))
print(json.dumps(agg["diagnostics"],indent=2))

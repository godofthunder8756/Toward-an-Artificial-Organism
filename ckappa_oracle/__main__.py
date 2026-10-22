"""Process entry. Thread limits are set before NumPy is imported."""

import os
import sys

for _name in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    _value = os.environ.get(_name)
    if _value is None:
        os.environ[_name] = "1"
    elif _value != "1":
        sys.stderr.write(f"{_name}={_value}, expected 1\n")
        raise SystemExit(5)

from ckappa_oracle.driver import main

raise SystemExit(main())

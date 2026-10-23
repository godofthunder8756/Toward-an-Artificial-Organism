# B2 confirmatory execution packaging repair

The first confirmatory execution attempt failed before any simulation data were generated because the OSF archival source snapshot omitted Python package initialisation/helper modules imported by the preregistered runner.

Restored from the already validated B2 development release:
- toe/__init__.py
- toe/agents/__init__.py
- toe/agents/dummy.py
- toe/agents/noop.py
- toe/environments/__init__.py
- toe/environments/dummy.py
- toe/environments/gray_scott.py
- toe/core/__init__.py

All common Python source files were SHA-256 compared before repair and matched exactly. The only mismatch was `pyproject.toml`, whose package version changed from development `0.6.0` to preregistration `0.7.0`; the preregistration copy was retained. No frozen manifest, lock, seed, environment configuration, architecture configuration, registry, estimand, threshold, intervention, rescue, bypass, or decision rule was changed.

The failed attempt terminated at Python import time and generated no scientific simulation data.

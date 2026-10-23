#!/bin/bash
# Frozen entry point. One pinned CPU, single-threaded BLAS, 4 GB address space.
set -euo pipefail
cd /workspace
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
ulimit -v 4194304
exec taskset -c 0 /usr/bin/python3 -B -m audit.gru_v1_3.run_audit

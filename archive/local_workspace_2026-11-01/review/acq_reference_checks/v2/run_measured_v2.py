"""Substitute for /usr/bin/time -v (not installed; no root). Runs one command pinned to CPU 0
with a 4 GB address-space cap and a timeout; logs wall time, max RSS, user/sys CPU, exit code."""
import json, os, resource, subprocess, sys, time
log, timeout, cmd = sys.argv[1], sys.argv[2], sys.argv[3:]
env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", NUMEXPR_NUM_THREADS="1", PYTHONHASHSEED="0")
full = ["taskset", "-c", "0", "prlimit", "--as=4294967296", "timeout", timeout] + cmd
t0 = time.time(); p = subprocess.run(full, env=env, capture_output=True, text=True); wall = time.time() - t0
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
rec = {"command": " ".join(full), "env_threads": "OMP/OPENBLAS/MKL/NUMEXPR=1", "exit_code": p.returncode,
       "wall_s": round(wall, 3), "user_s": round(ru.ru_utime, 3), "sys_s": round(ru.ru_stime, 3),
       "max_rss_kB": ru.ru_maxrss, "started": time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime(t0))}
open(log + ".stdout.txt", "w").write(p.stdout); open(log + ".stderr.txt", "w").write(p.stderr)
json.dump(rec, open(log + ".resources.json", "w"), indent=1); print(json.dumps(rec)); print(p.stdout[-3000:]); print(p.stderr[-2000:])

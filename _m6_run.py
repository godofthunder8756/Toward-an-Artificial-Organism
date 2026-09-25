import ac117, json, time, sys

t0 = time.monotonic()
mode = sys.argv[1] if len(sys.argv) > 1 else 'finals'
if mode == 'engineering':
    ac117.collect('ac117_engineering_v1', ac117.ENGINEERING)
elif mode == 'finals':
    ac117.collect('ac117_results_v1', ac117.FINAL_SEEDS, do_preflight=True, finals=True)
print('done in %.1f min' % ((time.monotonic() - t0) / 60), flush=True)

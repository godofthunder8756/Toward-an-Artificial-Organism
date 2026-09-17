import json
r = json.load(open('ac81_results_v1/results.json'))
rows = r['rows']
print('seeds', r['seeds'], 'hashes', len(r['hashes']))
for arm in ('internalized', 'pristine', 'unmaintained', 'no_repair'):
    for loss in (True, False):
        rr = [x for x in rows if x['arm'] == arm and x['loss'] == loss]
        surv = [x for x in rr if x['completed']]
        print(f'{arm:14s} loss={loss!s:5s} survive {len(surv)}/{len(rr)}  deaths={[x["first_dead"] for x in rr]}')
print()
print('internalized loss=True survivors detail:')
for x in [x for x in rows if x['arm'] == 'internalized' and x['loss'] and x['completed']]:
    print(f"  seed {x['seed']}/h{x['history']}: W_b={x['W_birth']} C_b={x['C_birth']} B_b={x['B_birth']} "
          f"C_post={x['C_birth_post']} B_post={x['B_birth_post']} writes={x['writes']} conv={x['converted']} "
          f"W={x['W_live']} C={x['C_live']} B={x['B_live']} routes={x['routes']} desc={x['description_correct']}")
print()
print('unmaintained descCorrect:', sorted(set(x['description_correct'] for x in rows if x['arm'] == 'unmaintained')))
print('internalized survivor descCorrect:', sorted(set(x['description_correct'] for x in rows if x['arm'] == 'internalized' and x['completed'])))
print('pristine survivor descCorrect:', sorted(set(x['description_correct'] for x in rows if x['arm'] == 'pristine' and x['completed'])))
print()
print('loss=False survival:')
for arm in ('internalized', 'pristine', 'unmaintained', 'no_repair'):
    rr = [x for x in rows if x['arm'] == arm and not x['loss']]
    surv = sum(1 for x in rr if x['completed'])
    print(f'  {arm:14s} {surv}/{len(rr)}')

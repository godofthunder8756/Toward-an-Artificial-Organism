"""Boundary-safe candidate intervention; deterministic given an external draw.

Magnitude is one categorical level. At endpoints 0 and 5 every condition is
sham. At interior readings 1..4 both perturbations have absolute increment 1;
the symmetric condition's conditional expected increment is exactly zero.
Exposure can still differ across closed-loop agents because raw readings differ.
"""
def perturb(raw, condition, draw, active=True):
    if raw not in range(6):
        raise ValueError('Sensor reading must be an integer from 0 through 5.')
    if condition not in ('clean','bias','noise'):
        raise ValueError('Unknown condition.')
    if not 0 <= draw < 1:
        raise ValueError('Draw must be in [0,1).')
    eligible = bool(active and 1 <= raw <= 4)
    if not eligible or condition == 'clean':
        return raw, eligible
    delta = 1 if condition == 'bias' or draw < .5 else -1
    return raw + delta, eligible

def validate():
    cases=[]
    for raw in range(6):
        clean,_=perturb(raw,'clean',.25)
        bias,eligible=perturb(raw,'bias',.25)
        lo,_=perturb(raw,'noise',.75)
        hi,_=perturb(raw,'noise',.25)
        assert clean==raw and (lo+hi)/2==raw
        assert all(0<=v<=5 for v in (clean,bias,lo,hi))
        assert abs(bias-raw)==abs(lo-raw)==abs(hi-raw)==int(eligible)
        for condition in ('clean','bias','noise'):
            assert perturb(raw,condition,.25,active=False)==(raw,False)
        cases.append(dict(raw=raw,eligible=eligible,clean=clean,bias=bias,
                          noise_outputs=[lo,hi],noise_expected_increment=(lo+hi)/2-raw))
    return cases

if __name__=='__main__':
    import json
    print(json.dumps(validate(),indent=2))

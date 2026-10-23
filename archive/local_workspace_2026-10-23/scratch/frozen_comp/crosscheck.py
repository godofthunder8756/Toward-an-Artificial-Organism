import sys; sys.path.insert(0,'/workspace/scratch/pr9/clone'); sys.path.insert(0,'.')
import numpy as np, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import feasibility as F
from recurrent_core_transfer_models import CoreGRU, load_checkpoint
from recurrent_core_transfer_metrics import evaluate_arm
from graded_reversion_outcomes import l_prefix
from twostream_acquisition_metrics import afit_holds
w=F.w; mx=0
for d,s in (('recurrent_core_results_v1/checkpoints',100),('first_order_control_results_v1/checkpoints',305)):
    for arm in ('cand_final','f_init'):
        p=f'{F.CL}/{d}/s{s}_{arm}.ckpt'; m=CoreGRU(32); m.load_state_dict(load_checkpoint(__import__("pathlib").Path(p))); ev=evaluate_arm(m,w)
        lf=l_prefix(ev['predictions'],w.q); e=ev['errors']['TEST']
        mine=F.fwd(F.load(p)); me=F.component_excess(mine,w)['TEST']
        print(arm,s,'frozen Lp %.10g mine %.10g | Etot %.10g/%.10g | Exor %.10g/%.10g | afit %s'%(lf,F.Lp(mine),e['total'],me['total'],e['XOR'],me['XOR'],afit_holds(ev['errors'],w,'TEST')), 'pred maxdiff %.2e'%np.abs(ev['predictions']-mine).max())

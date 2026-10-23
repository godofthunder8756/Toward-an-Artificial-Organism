import sys; sys.path.insert(0,'/workspace/scratch/pr9/clone')
import torch, hashlib
from recurrent_core_transfer_models import build_initialized
torch.set_num_threads(1)
for s in range(400,410):
    a=dict(build_initialized(s,32).named_parameters()); b=dict(build_initialized(s,48).named_parameters()); c=dict(build_initialized(s,32).named_parameters())
    core=all(torch.equal(a[k],b[k]) for k in a if k.startswith('rnn'))
    full32=all(torch.equal(a[k],c[k]) for k in a)
    fc1=torch.equal(a['readout_fc1.weight'],b['readout_fc1.weight'][:32])
    w0=hashlib.sha256(a['rnn.weight_hh_l0'].detach().numpy().tobytes()).hexdigest()[:16]
    print(s,'core_equal_32_48',core,'cand_vs_rfix32_full_equal',full32,'fc1_rows0-31',fc1,'W0sha16',w0)

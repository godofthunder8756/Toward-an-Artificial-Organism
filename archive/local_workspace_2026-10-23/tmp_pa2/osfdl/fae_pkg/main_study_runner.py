"""Checkpointed study runner. Defaults to development preflight, never main data.

Main mode requires a real registration record JSON with url and registered_utc.
Each completed episode is atomically stored; rerunning skips verified records.
"""
import argparse
import datetime
import gzip
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time

PIN='2657a982c5ae59a0f0fa9cdf941f82a71eba3cd9'
def encode(x): return json.dumps(x,sort_keys=True,allow_nan=False,separators=(',',':'))
def digest(x): return hashlib.sha256(x).hexdigest()
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo',required=True,type=Path)
    parser.add_argument('--out',required=True,type=Path)
    parser.add_argument('--mode',choices=['preflight','main'],default='preflight')
    parser.add_argument('--registration',type=Path)
    opt=parser.parse_args();repo=opt.repo.resolve();out=opt.out.resolve()
    registration=None
    if opt.mode=='main':
        if opt.registration is None: parser.error('Main mode requires the actual public preregistration record.')
        registration=json.loads(opt.registration.read_text(encoding='utf-8'))
        if not registration.get('url','').startswith('https://') or not registration.get('registered_utc'):
            parser.error('Registration must include its public HTTPS URL and actual registered_utc timestamp.')
        stamp=datetime.datetime.fromisoformat(registration['registered_utc'].replace('Z','+00:00'))
        if stamp.tzinfo is None or stamp>datetime.datetime.now(datetime.timezone.utc):
            parser.error('Registration timestamp must be timezone-aware and in the past.')
    git=['git','-c',f'safe.directory={repo.as_posix()}']
    assert subprocess.check_output(git+['rev-parse','HEAD'],cwd=repo,text=True).strip()==PIN
    assert not subprocess.check_output(git+['status','--porcelain'],cwd=repo,text=True).strip()
    bank=json.loads((repo/'configs/known_model_layout_bank.json').read_text())['layouts']
    layouts=bank if opt.mode=='main' else [bank[0]]
    seeds=list(range(10000,10064)) if opt.mode=='main' else [301]
    scripts=['main_study_runner.py','analyze_main_study.py','pilot_experiment.py','sensor_controls.py','validate_new_controls.py']
    source_dir=Path(__file__).resolve().parent
    hashes={name:digest((source_dir/name).read_bytes()) for name in scripts}
    packages={d.metadata['Name']:d.version for d in importlib.metadata.distributions() if d.metadata['Name']}
    design=dict(mode=opt.mode,upstream_commit=PIN,seeds=seeds,layouts=layouts,
        arms=['uniform','coupled','preference'],conditions=['clean','bias','noise'],
        steps=40,horizon=2,known_resource_model=True,precision=.9,preference_weight=2.,
        intervention='thirst +1 or symmetric +/-1 at t=5..14 only for raw levels 1..4; endpoints sham',
        registration=registration,source_hashes=hashes,packages=packages,
        python=sys.version)
    design_id=digest(encode(design).encode())
    out.mkdir(parents=True,exist_ok=True)
    manifest=out/'design.json'
    if manifest.exists():
        assert json.loads(manifest.read_text())==design,'Refusing to mix designs, code versions, or environments.'
    else:
        assert not any(out.iterdir()),'New run directory must be empty.'
        manifest.write_text(json.dumps(design,indent=2),encoding='utf-8')
        frozen=out/'frozen-source';frozen.mkdir()
        for name in scripts: (frozen/name).write_bytes((source_dir/name).read_bytes())
    episodes=out/'episodes';episodes.mkdir(exist_ok=True)
    attempts=out/'attempts.jsonl'
    # The legacy helper parses command-line arguments at import. Isolate its
    # initialization in temporary scratch space outside the study records.
    with tempfile.TemporaryDirectory(prefix='study-runtime-',dir=repo.parent) as scratch:
        sys.argv=['pilot_experiment.py','--repo',str(repo),'--out',str(Path(scratch)/'init')]
        import pilot_experiment as p
        from validate_new_controls import ControlledBody
        from sensor_controls import validate
        validate()
        p.PilotBody=ControlledBody;p.KW.update(unknown_model=False,planning_horizon=2)
        start=time.perf_counter();written=0;skipped=0
        for layout in layouts:
            for arm in design['arms']:
                bundle=None
                for seed in seeds:
                    for condition in design['conditions']:
                        ident=f"{layout['layout_id']}__{arm}__{seed}__{condition}"
                        destination=episodes/(ident+'.json.gz')
                        if destination.exists():
                            with gzip.open(destination,'rt',encoding='utf-8') as f: saved=json.load(f)
                            assert saved['design_id']==design_id and saved['id']==ident
                            assert saved['payload_sha256']==digest(encode(saved['payload']).encode())
                            skipped+=1;continue
                        if bundle is None: bundle=p.build(layout,arm)
                        stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
                        try:
                            summary,records=p.episode(bundle,layout,seed,condition)
                            summary['eligible_steps']=sum(r['eligible'] for r in records)
                            summary['terminal_hold_loss']=(sum(r['regulation_loss'] for r in records)+(40-len(records))*records[-1]['regulation_loss'])/40
                            # Convert array scalars once, then hash canonical serialized data.
                            payload=json.loads(json.dumps(dict(summary=summary,records=records),default=p.serial,allow_nan=False))
                            saved=dict(id=ident,design_id=design_id,started_utc=stamp,
                                payload=payload,payload_sha256=digest(encode(payload).encode()))
                            temporary=destination.with_suffix('.tmp')
                            with gzip.open(temporary,'wt',encoding='utf-8') as f: f.write(encode(saved))
                            os.replace(temporary,destination)
                            written+=1
                            with attempts.open('a',encoding='utf-8') as f: f.write(encode(dict(id=ident,status='complete',started_utc=stamp))+'\n')
                            print(f'{written} written, {skipped} resumed: {ident}',flush=True)
                        except Exception as exc:
                            with attempts.open('a',encoding='utf-8') as f: f.write(encode(dict(id=ident,status='software_failure',started_utc=stamp,error=repr(exc)))+'\n')
                            raise
        expected=len(layouts)*len(seeds)*9
        assert written+skipped==expected
        completion=dict(mode=opt.mode,episodes=expected,newly_written=written,resumed=skipped,
            design_id=design_id,invocation_seconds=time.perf_counter()-start,
            completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
        (out/'completion.json').write_text(json.dumps(completion,indent=2),encoding='utf-8')
        print(json.dumps(completion,indent=2))

if __name__=='__main__': main()

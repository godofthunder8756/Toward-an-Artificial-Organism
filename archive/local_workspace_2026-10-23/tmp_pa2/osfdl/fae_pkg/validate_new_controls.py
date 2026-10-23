"""Small development integration check; not confirmatory data."""
import json
from pathlib import Path
import pilot_experiment as p
from sensor_controls import perturb, validate

OriginalBody=p.PilotBody
class ControlledBody(OriginalBody):
    def sample_interoception(self,attended,**kwargs):
        condition=self.condition
        self.condition='clean'
        try:
            observed=super().sample_interoception(attended,**kwargs)
        finally:
            self.condition=condition
        t=self.sensor_record['sample_t']
        raw=int(observed[1]); active=5<=t<15
        observed[1],eligible=perturb(raw,condition,float(self.draws[t,8]),active)
        self.sensor_record.update(received_sensor=observed.copy(),eligible=eligible,
            intended_delta=int(observed[1])-raw,realized_delta=int(observed[1])-raw)
        return observed

if __name__=='__main__':
    p.PilotBody=ControlledBody
    p.KW.update(unknown_model=False,planning_horizon=2)
    p.CONFIG.update(stage='development integration of boundary-safe controls',horizon=2,
        known_resource_model=True,bias_magnitude=1,endpoint_rule='sham at raw 0 or 5',
        seeds=[200],layouts=['km_easy_00'],arms=['uniform','coupled','preference'])
    p.dump(p.args.out/'exact-control-validation.json',validate())
    p.dump(p.args.out/'config.json',p.CONFIG)
    layout=json.loads((p.args.repo/'configs/known_model_layout_bank.json').read_text())['layouts'][0]
    all_results=[]
    for arm in p.CONFIG['arms']:
        bundle=p.build(layout,arm)
        for condition in p.CONFIG['conditions']:
            summary,records=p.episode(bundle,layout,200,condition)
            for r in records:
                raw=int(r['raw_sensor'][1]);value=int(r['received_sensor'][1])
                assert r['raw_sensor'][[0,2,3]].tolist()==r['received_sensor'][[0,2,3]].tolist()
                assert 0<=value<=5
                assert r['eligible']==(5<=r['t']<15 and 1<=raw<=4)
                assert abs(value-raw)==int(r['eligible'] and condition!='clean')
                if condition=='bias': assert value>=raw
            summary['eligible_steps']=sum(r['eligible'] for r in records)
            all_results.append(dict(summary=summary,records=records))
            print(arm,condition,'validated',summary['eligible_steps'],'eligible steps',flush=True)
    p.dump(p.args.out/'integration-results.json',all_results)
    p.dump(p.args.out/'completion.json',dict(status='passed',development_episodes=9,
        note='These nine seeded trajectories validate implementation only. No confirmatory seeds used.'))

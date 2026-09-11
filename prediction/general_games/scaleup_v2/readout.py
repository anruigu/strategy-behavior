"""Native audits, replicate variability, and paired prospective learning curves."""
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import random
import statistics as st

from prediction.io_utils import read_json,write_json,digest,now
from prediction.client import Ledger
from prediction.general_games.export import jsonl
from . import ROOT,DATA,STUDY
from .catalog import FAMILIES,NEW,ANCHORS
from .collection import source_hashes
from .runtime import replay
from .labels import episode_row,TARGETS,DEFINITIONS


def average(values):
    values=[v for v in values if v is not None]
    return st.mean(values) if values else None


def interval(values):
    if len(values)<2:return None
    rng=random.Random(6200);draws=sorted(st.mean(rng.choices(values,k=len(values))) for _ in range(5000))
    return [draws[124],draws[4874]]


def load_phase(phase,verify=True):
    folder=STUDY/phase;plan=read_json(folder/'plan.json');rows=[];actions=[];linked=[];independent=Counter()
    assert plan['source_hashes']==source_hashes()
    for item in plan['episodes']:
        trace=read_json(folder/'episodes'/(item['episode_id']+'.json'))
        assert trace['item']==item
        if verify:replay(item,trace,folder/'raw_calls')
        row,aa=episode_row(trace,'v2-'+phase);row.update(suite=item['suite'],phase=phase);rows.append(row);actions+=aa
        if trace['status']=='complete':assert row['targets']['win']==float(trace['final_state']['rewards'][str(item['seat'])]==1)
        if item['game']['family_id']=='secretary' and trace['status']=='complete':
            import re
            reason=trace['final_state']['game_info'][str(item['seat'])].get('reason','');match=re.search(r'at draw (\d+)/(\d+)',reason)
            if match:
                draws=trace['final_state']['game_state']['draws'];index=int(match[1])-1
                assert row['native_reward']==float(draws[index]==max(draws));independent['secretary_maximum_checks']+=1
        for attempts in trace['attempts'].values():
            for attempt in attempts:
                ident=attempt['meta']['call_id'];linked.append(ident);call=read_json(folder/'raw_calls'/(ident+'.json'))
                assert call['config']==plan['models'][item['model']] and call['status']==attempt['meta']['status']
                assert call['request']['max_tokens']==plan['max_tokens']
        # Independently check native accounting and executed-action labels.
        decisions={};previous=[0,0]
        for step in trace['steps']:
            fid=item['game']['family_id'];p=item['game']['parameters'];before=step['before']['game_state'];after=step['after']['game_state'];actor=str(step['actor'])
            if fid=='prisoners_dilemma' and before['phase']=='decision':
                import re
                decisions[step['actor']]=bool(re.search(r'\[Defect\]',step['raw_action'],re.I))
                if len(decisions)==2:
                    x,y=decisions[0],decisions[1]
                    expected=[p['mutual_defect_reward']]*2 if x and y else [p['cooperate_reward']]*2 if not x and not y else [p['defect_reward'],p['sucker_reward']] if x else [p['sucker_reward'],p['defect_reward']]
                    actual=[after['scores'][str(i)]-previous[i] for i in (0,1)];assert actual==expected
                    previous=[after['scores'][str(i)] for i in (0,1)];decisions={};independent['pd_round_payoffs']+=1
            if fid=='ultimatum' and len(after['round_history'])>len(before['round_history']):
                r=after['round_history'][-1];deltas={k:after['player_totals'][k]-before['player_totals'][k] for k in before['player_totals']}
                expected={str(r['proposer']):p['pool']-r['offer'] if r['decision']=='Accept' else 0,str(r['responder']):r['offer'] if r['decision']=='Accept' else 0}
                assert deltas==expected;independent['ultimatum_round_payoffs']+=1
            if fid=='blind_auction' and step['is_focal'] and before['phase']=='bidding' and not step['result']['native_invalid']:
                import re
                bids=re.findall(r'\[Bid\s+(?:on\s+)?(?:Item\s+)?(\d+)\s*:\s*(\d+)\]',step['raw_action'],re.I)
                assert before['remaining_capital'][actor]-after['remaining_capital'][actor]==sum(int(amount) for itemid,amount in bids)
                independent['auction_capital_changes']+=1
            if fid=='two_thirds' and len(after['history'])>len(before['history']):
                guesses=after['history'][-1];target=sum(guesses.values())/3
                ds={k:abs(v-target) for k,v in guesses.items()}
                expected={k:int(ds[k]<ds[str(1-int(k))]) for k in guesses}
                assert {k:after['points'][k]-before['points'][k] for k in guesses}==expected
                independent['two_thirds_round_points']+=1
            if fid=='memory' and not step['result']['native_invalid']:
                import re
                a,b,c,d=map(int,re.search(r'\[(\d+) (\d+) (\d+) (\d+)\]',step['raw_action']).groups())
                match=before['board'][a][b]==before['board'][c][d]
                assert after['score'][actor]-before['score'][actor]==int(match)
                assert len(after['matched_positions'])-len(before['matched_positions'])==2*int(match)
                independent['memory_pair_scores']+=1
    call_files={p.stem for p in (folder/'raw_calls').glob('*.json')}
    assert len(linked)==len(set(linked)) and set(linked)==call_files
    return rows,actions,dict(independent)


def legacy_rows():
    rows=[];actions=[]
    for name in ('pilot-20260910','parameter-check-20260910'):
        folder=ROOT.parent/'runs'/name
        for item in read_json(folder/'plan.json')['episodes']:
            row,aa=episode_row(read_json(folder/'episodes'/(item['episode_id']+'.json')),name)
            row.update(phase='legacy',suite='historical');rows.append(row);actions+=aa
    return rows,actions


def inference_audit():
    groups={};all_ids=[];total=0;unknown=0
    folders=[('training',STUDY/'training'),('test',STUDY/'test')]
    folders += [(str(p.parent.relative_to(STUDY)),p.parent) for p in (STUDY/'prediction').rglob('raw_calls')]
    for name,folder in folders:
        calls=[read_json(p) for p in (folder/'raw_calls').glob('*.json')]
        ids=[c['call_id'] for c in calls];all_ids+=ids;cost=sum(c.get('budget_cost_usd') or 0 for c in calls)
        assert len(ids)==len(set(ids));total+=cost;unknown+=sum(c.get('budget_cost_usd') is None for c in calls)
        groups[name]=dict(calls=len(calls),statuses=dict(Counter(c['status'] for c in calls)),reported_usd=cost,
            unknown_cost_calls=sum(c.get('budget_cost_usd') is None for c in calls),preflight='preflight' in name)
    assert len(all_ids)==len(set(all_ids))
    ledger=Ledger(STUDY/'budget.sqlite',75).summary()
    assert abs(ledger['reported_usd']-total)<1e-8 and sum(s['calls'] for s in ledger['states'].values())==len(all_ids)
    stage_ledgers={}
    for phase in ('training','test','prediction'):
        current=Ledger(STUDY/phase/'budget.sqlite',50).summary()
        selected=[v for k,v in groups.items() if k==phase or k.startswith(phase+'/')]
        assert abs(current['reported_usd']-sum(v['reported_usd'] for v in selected))<1e-8
        assert sum(s['calls'] for s in current['states'].values())==sum(v['calls'] for v in selected)
        stage_ledgers[phase]=current
    return dict(groups=groups,total_calls=len(all_ids),reported_usd=total,unknown_cost_calls=unknown,global_ledger=ledger,stage_ledgers=stage_ledgers)


def prediction_audit():
    from .predict import parse,SIZES,OUT,stage_rows,test_queries
    frozen=read_json(OUT/'frozen.json');assert frozen['test_plan_sha256']==digest(read_json(STUDY/'test/plan.json'))
    for name,sha in frozen['artifact_hashes'].items():assert hashlib.sha256((OUT/name).read_bytes()).hexdigest()==sha
    predictions=[];linked=[];queries={};calibration_counts={}
    for size in SIZES:
        folder=OUT/f'n{size}';m=read_json(folder/'manifest.json');pool={r['id']:r for r in read_json(folder/'groups.evaluator.json')};queries.update({q['id']:q for q in m['queries']})
        assert m['source_sha256']==digest((ROOT/'predict.py').read_text())
        assert m['specification_sha256']==digest(read_json(DATA/'mechanics.v2.json'))
        assert m['collection_manifest_sha256']==digest(read_json(DATA/'manifest.json'))
        assert m['training_rows_sha256']==digest(stage_rows(size))
        assert m['queries']==test_queries()
        calibration_counts[size]=len(m['calibration_ids'])
        for batch in m['batches']:
            record=read_json(folder/'batches'/(batch['id']+'.json'));assert record['status']=='complete'
            assert len(record['attempts'])<=m['max_attempts']
            assert parse(record['attempts'][-1]['raw'],batch)==record['predictions']
            for attempt in record['attempts']:
                ident=attempt['meta']['call_id'];linked.append(ident);call=read_json(folder/'raw_calls'/(ident+'.json'))
                assert call['request']['messages']==batch['messages'] and call['config']==m['predictor']
                assert call['request']['max_tokens']==m['max_tokens']
                assert call['status']==attempt['meta']['status']
                if call['status']=='ok':assert call['response']['choices'][0]['message']['content']==attempt['raw']
            for ident,examples in batch['example_ids'].items():
                assert len(examples)==batch['shots'] and set(examples)<=set(pool)
                if batch['kind']=='calibration':
                    assert all(pool[e]['inputs']['family_id']!=pool[ident]['inputs']['family_id'] for e in examples)
                else:assert all(pool[e]['opening_group']!=queries[ident]['opening_group'] for e in examples)
        predictions+=read_json(folder/'test-predictions.json')
    final_call_ids={p.stem for size in SIZES for p in (OUT/f'n{size}/raw_calls').glob('*.json')}
    assert set(linked)==final_call_ids
    first_test=min(read_json(p)['timestamp'] for p in (STUDY/'test/raw_calls').glob('*.json'))
    assert frozen['frozen_at']<first_test
    assert len(linked)==len(set(linked))
    return predictions,queries,dict(frozen_at=frozen['frozen_at'],first_test_call=first_test,prospective=True,
        scored_forecast_attempts=len(linked),test_condition_queries=len(queries),calibration_groups_by_size=calibration_counts,scored_predictions=len(predictions))


def serialized_model_audit(sizes=(120,248,440)):
    """Reload fitted artifacts and independently reproduce their exported outputs."""
    from prediction import modeling
    from .predict import OUT,features,text_features
    import pickle
    import numpy as np
    from threadpoolctl import threadpool_limits
    checked=0;maximum=0
    with threadpool_limits(limits=1):
        for size in sizes:
            folder=OUT/f'n{size}';m=read_json(folder/'manifest.json');queries=m['queries']
            with (folder/'models.pkl').open('rb') as f:bundles=pickle.load(f)
            exported={(p['method'],p['query_id']):p['forecast'] for p in read_json(folder/'test-predictions.json')}
            for name,bundle in bundles.items():
                base=[exported['few_'+name.split('_')[1],q['id']] for q in queries] if name.startswith('corrected_') else None
                xx=bundle['scaler'].transform(bundle['vectorizer'].transform([features(q,base[i] if base else None) for i,q in enumerate(queries)]))
                if base:xx=np.column_stack([xx,np.ones(len(xx))])
                else:xx=np.column_stack([xx,bundle['text_encoder'].transform(text_features(q,read_json(DATA/'mechanics.v2.json')) for q in queries).toarray()])
                for target in TARGETS:
                    entry=bundle['models'][target];est=entry['estimator']
                    if base:
                        raw=est.predict(xx) if est is not None else np.zeros(len(queries))
                        values=[None if b[target] is None else float(np.clip(b[target]+delta,0,1)) for b,delta in zip(base,raw)]
                    elif est is not None:
                        values=np.clip(est.predict_proba(xx)[:,1] if target in ('win','any_invalid') else est.predict(xx),0,1).tolist()
                    else:values=[entry['constant']]*len(queries)
                    for q,value in zip(queries,values):
                        expected=exported[name,q['id']][target]
                        value=value if target in q['supported'] else None
                        if expected is None:assert value is None
                        else:
                            error=abs(value-expected);assert error<1e-10;maximum=max(maximum,error)
                        checked+=1
    return dict(values_checked=checked,max_absolute_difference=maximum)


def model_effects(rows):
    """Pair models on configuration, seed and seat after averaging repetitions."""
    result=[]
    for family in sorted({r['inputs']['family_id'] for r in rows}):
        rr=[r for r in rows if r['inputs']['family_id']==family and r['status']=='complete'];targets={}
        for target in TARGETS:
            groups=defaultdict(lambda:defaultdict(list))
            for r in rr:
                if r['targets'][target] is not None:groups[r['inputs']['game_id'],r['seed'],r['inputs']['seat']][r['inputs']['model']].append(r['targets'][target])
            paired=[g for g in groups.values() if len(g)==2]
            if paired:
                q=st.mean(st.mean(g['qwen-3.8-27b']) for g in paired);g=st.mean(st.mean(g['glm']) for g in paired)
                targets[target]=dict(qwen=q,glm=g,qwen_minus_glm=q-g,matched_conditions=len(paired))
        result.append(dict(family=family,title=FAMILIES[family]['title'],episodes=len(rr),targets=targets,
            by_model=[dict(model=m,episodes=sum(r['inputs']['model']==m for r in rr),invalid_actions=sum(r['invalid_actions'] for r in rr if r['inputs']['model']==m)) for m in ('qwen-3.8-27b','glm')]))
    return dict(families=result,macro_win_difference=average(r['targets']['win']['qwen_minus_glm'] for r in result if 'win' in r['targets']),
        note='Fresh normal-prompt collection only. Equal weight per family, with each model compared on matching configuration, seed and seat. Repetitions are averaged first. This is a descriptive comparison across eight purposively selected families.')


def repeatability(rows):
    groups=defaultdict(list)
    for r in rows:
        if r['status']=='complete':groups[r['condition_id']].append(r)
    result=[]
    for family in sorted({r['inputs']['family_id'] for r in rows}):
        rr=[r for r in rows if r['inputs']['family_id']==family]
        selected=[g for g in groups.values() if g[0]['inputs']['family_id']==family]
        targets={}
        for target in TARGETS:
            vv=[[r['targets'][target] for r in g if r['targets'][target] is not None] for g in selected]
            vv=[v for v in vv if len(v)>=2]
            if vv:targets[target]=dict(conditions=len(vv),observations=sum(map(len,vv)),within_condition_variance=st.mean(st.variance(v) for v in vv),
                varying_conditions=sum(len(set(v))>1 for v in vv))
        result.append(dict(family=family,title=FAMILIES[family]['title'],episodes=len(rr),conditions=len(selected),targets=targets))
    return result


def parameter_effects(rows):
    output=[]
    for family,(axis,lo,base,hi) in ANCHORS.items():
        target={'prisoners_dilemma':'cooperation_rate','pig_dice':'risk_taking_rate','colonel_blotto':'allocation_concentration','blind_auction':'bid_budget_fraction'}[family]
        levels=[]
        for value in (lo,base,hi):
            rr=[r for r in rows if r['inputs']['family_id']==family and r['inputs']['structured']['parameters'][axis]==value and r['status']=='complete']
            levels.append(dict(value=value,episodes=len(rr),measured_behavior_episodes=sum(r['targets'][target] is not None for r in rr),behavior=average(r['targets'][target] for r in rr),win=average(r['targets']['win'] for r in rr),
                mean_focal_actions=average(r['focal_actions'] for r in rr),by_model=[dict(model=m,behavior=average(r['targets'][target] for r in rr if r['inputs']['model']==m),win=average(r['targets']['win'] for r in rr if r['inputs']['model']==m)) for m in ('qwen-3.8-27b','glm')]))
        output.append(dict(family=family,title=FAMILIES[family]['title'],axis=axis,target=target,levels=levels))
    return output


def scores(rows,predictions,queries):
    truth=defaultdict(list)
    for r in rows:
        if r['status']=='complete':truth[r['condition_id']].append(r)
    losses={};score_rows=[];grouped=defaultdict(list)
    for p in predictions:grouped[p['size'],p['suite'],p['method']].append(p)
    for (size,suite,method),pp in sorted(grouped.items()):
        for target in TARGETS:
            by_family=defaultdict(list);noise_by_family=defaultdict(list);n=0
            for p in pp:
                q=queries[p['query_id']];forecast=p['forecast'][target];yy=[r['targets'][target] for r in truth[p['query_id']] if r['targets'][target] is not None]
                if forecast is None or not yy:continue
                loss=st.mean((forecast-y)**2 for y in yy);family=q['inputs']['family_id'];by_family[family].append(loss);n+=len(yy)
                losses[size,suite,method,target,p['query_id']]=loss
                if len(yy)>=2:noise_by_family[family].append(st.variance(yy))
            if not by_family:continue
            family_means={f:st.mean(v) for f,v in by_family.items()};point=st.mean(family_means.values())
            noise=average(st.mean(v) for v in noise_by_family.values())
            score_rows.append(dict(size=size,suite=suite,method=method,target=target,score=point,episodes=n,conditions=sum(map(len,by_family.values())),families=len(by_family),
                family_scores=family_means,family_bootstrap_95=interval(list(family_means.values())),within_condition_noise=noise,
                noise_subtracted=point-noise if noise is not None else None))
    comparisons=[]
    for size in (120,248,440):
        for suite in ('parameter','family'):
            for a,b in [('corrected_4','few_4'),('corrected_8','few_8'),('corrected_16','few_16'),('linear','few_4'),('few_16','few_4'),('few_8','few_4'),('corrected_4','few_16'),('linear','few_16'),('corrected_4','pooled_few_4'),('corrected_4','pooled_few_16'),('linear','pooled_few_16'),('pooled_few_4','few_4'),('pooled_few_16','few_16')]:
                for target in TARGETS:
                    by_family=defaultdict(list)
                    for ident,q in queries.items():
                        ka,kb=(size,suite,a,target,ident),(size,suite,b,target,ident)
                        if ka in losses and kb in losses:by_family[q['inputs']['family_id']].append(losses[ka]-losses[kb])
                    if not by_family:continue
                    values=[st.mean(v) for v in by_family.values()]
                    comparisons.append(dict(size=size,suite=suite,a=a,b=b,target=target,delta=st.mean(values),family_bootstrap_95=interval(values),
                        families=len(values),conditions=sum(map(len,by_family.values())),family_deltas={f:st.mean(v) for f,v in by_family.items()}))
    return score_rows,comparisons


def learning_progress(score_rows):
    result=[];lookup={(r['size'],r['suite'],r['method'],r['target']):r for r in score_rows}
    for (size,suite,method,target),row in lookup.items():
        if size!=440:continue
        first=lookup.get((120,suite,method,target))
        if not first:continue
        families=set(row['family_scores'])&set(first['family_scores'])
        deltas={f:row['family_scores'][f]-first['family_scores'][f] for f in sorted(families)}
        result.append(dict(suite=suite,method=method,target=target,delta_440_minus_120=average(deltas.values()),
            family_bootstrap_95=interval(list(deltas.values())),family_deltas=deltas))
    return result


def findings(s):
    return dict(
        headline='Few-shot still leads on general win prediction; the current learned predictors do not justify scaling training volume.',
        recommendation='Keep the improved measurement protocol and pooled few-shot baseline. Fix learner transfer and broaden training-family coverage in a controlled next study before a large collection. More repetitions of the same four anchors are not supported as the next scaling strategy.',
        checks=[
            dict(check='Parameters',verdict='Behavior varies',evidence='PD cooperation falls .567 → .533 → .492 as the defection reward increases. Blotto concentration falls .483 → .466 → .451; auction budget use falls .996 → .900 → .647. Pig mean focal actions rise 5.225 → 7.675 → 14.100. Each level has 40 episodes; auction rate support is 30/33/35. These are descriptive responses, with the higher setting collected in a later batch.'),
            dict(check='Models',verdict='Differences depend on family and target',evidence='GLM wins Memory in 10/16 episodes versus Qwen 5/16, and uses an available known pair more often (.943 vs .718). Auction invalidity occurs in 30/60 GLM episodes versus 6/60 Qwen episodes. PD cooperation differs (.661 GLM vs .400 Qwen) despite every fresh PD episode being a native win.'),
            dict(check='Labels',verdict='Native measurements reproduce; stochastic variation remains',evidence=f"All {s['audit']['new_native_transitions']:,} new native transitions replay, with independent payoff/selection/pair-score checks. Repeated win outcomes vary in 51 of 152 exact conditions. All 120 PD wins are identical, while cooperation varies in 13/24 PD conditions. Outcome saturation is a reason to retain richer behavior targets."),
            dict(check='Few-shot and training',verdict='Few-shot remains ahead for wins',evidence='At 440 episodes, corrected-4 minus four-shot win Brier is +.0220 on parameters and +.0874 on new families; paired family-bootstrap intervals are [.0093,.0315] and [.0187,.1524]. The correction gets worse on new-family wins as training grows (.2506 → .2952 → .3039). These intervals condition on the fitted forecasts and only four families per test.'),
            dict(check='Representation',verdict='Improved and reproducible; predictive sufficiency is unproven',evidence='The release supplies exact actor openings, corrected native parser/payoff/initialization and numerical opponent descriptions, plus authoritative executable sources. Hidden realizations and future events remain unavailable. There is no matched representation ablation in this version, so completeness of the source bundle is not proof that its compact forecast rendering is sufficient.')],
        headroom='Remaining error leaves room for better predictors, but these learners do not capture it broadly. Direct linear prediction still leads auction budget-use MSE (.0778 versus the best tested few-shot .0911) and narrowly leads Blotto concentration (.0042 versus .0043). The apparent Pig-rate advantage over original four-shot (.0047 versus .0160) disappears against pooled four-shot (.0038). Each behavior target is supported by one family here; these are narrow signals, not established general training gains.',
        scaling='The collection/label pipeline supports selective expansion to additional game families under this protocol. The win-prediction learning curves do not support a large scale-up of the present linear/correction methods. A stronger next study should vary training-family breadth at a fixed label budget, retain pooled 4/8/16-shot controls, and use more held-out families plus informative behavior targets.')


def report(s):
    lines=['# Replicated general-game study: training headroom and expansion','',
        '[Viewer](http://localhost:42329/general/replicated) · [Results JSON](summary.json) · [Protocol](protocol.json) · [Prospective freeze](prediction/frozen.json)','',
        f"The catalog now contains **16 families and 57 native configurations**. This stage collected **{s['counts']['new_episodes']} new episodes**: 320 training episodes and 272 prospective test episodes. The four anchor families have five independent LLM repetitions per exact condition, with world seed and seat fully crossed. Four additional native families—Ultimatum, Two-Thirds Average, Secretary and Memory—have two repetitions per condition.",'',
        'New collection uses the original normal player prompt, both player models, one provider, and unchanged native mechanics. Historical training includes both prompt conditions. Native/scripted validation is separate from model observations. There is no selection for gameability.','',
        '## What the completed study supports','',s['findings']['headline'],'',
        *[f"- **{r['check']} — {r['verdict']}:** {r['evidence']}" for r in s['findings']['checks']],'',
        s['findings']['headroom'],'',s['findings']['scaling'],'',
        '![Win-prediction learning curves](figures/learning-curves.png)','',
        '## Training versus few-shot','',
        'Learning curves use 120 historical episodes, then those 120 plus two fresh repetitions of each of 64 training conditions (248 episodes), then all five repetitions (440 episodes). Training groups from the four new families and the upper anchor configurations are excluded at every size. Higher-value historical observations are also excluded. Both the direct linear learner and the correction use equal total weight per training family; within each family, replicate means are weighted by their measured counts.','',
        'Few-shot methods use 4, 8 or 16 distinct observable-input examples, retrieved by game-structure/text similarity and then player/prompt/seat. The example sets are nested. Each primary demonstration contains the empirical mean and repetition count for one exact world condition; if multiple seeds have identical visible inputs, retrieval retains one such condition rather than pooling their labels. The learner uses all training groups. A secondary pooled-label control below addresses this loss of information. Exact actor opening messages and the same corrected mechanics specification are provided at every size. This study tests the original pretrained forecaster plus learned corrections; it does not train a new language encoder from scratch.','',
        'The learned correction is a fixed Ridge model trained on normal-prompt condition means and forecasts generated with each calibration query’s entire family excluded from examples. Calibration uses 60, 124 and 124 condition groups across the three sizes; later groups have more outcome repetitions. A fixed logistic/Ridge model with structured and training-only TF–IDF features and a training-mean baseline are also reported. Hyperparameters, shot counts and the primary corrected-4 versus few-4 comparison were fixed before fresh test play.','',
        'Lower Brier/MSE is better. Scores average repetitions within a condition, conditions within a family, then families equally. The parameter test contains 32 conditions / 160 episodes across four anchor families; the new-family test contains 56 conditions / 112 episodes across four unseen families.','']
    for suite in ('parameter','family'):
        lines += [f'### {suite.capitalize()} holdout: win / full-solution Brier','', '| Method | 120 training episodes | 248 | 440 |','|---|---:|---:|---:|']
        for method in ('training_mean','linear','few_4','corrected_4','few_8','corrected_8','few_16','corrected_16'):
            values={r['size']:r['score'] for r in s['scores'] if r['suite']==suite and r['target']=='win' and r['method']==method}
            lines.append('| '+method+' | '+' | '.join(f'{values[n]:.4f}' if n in values else '—' for n in (120,248,440))+' |')
        c=next(c for c in s['comparisons'] if c['suite']==suite and c['size']==440 and c['a']=='corrected_4' and c['b']=='few_4' and c['target']=='win');ci=c['family_bootstrap_95']
        lines+=['',f"At 440 episodes, corrected-4 minus few-4: **{c['delta']:+.4f}**, paired 95% family-bootstrap interval **[{ci[0]:+.4f}, {ci[1]:+.4f}]**. Negative favors training. Four held-out families are still a small sample; uncertainty conditions on the fitted models and forecasts.",'']
    lines+=['### Secondary control: pool repeated labels for identical visible examples','',
        'At 440 episodes, the 184 exact-condition groups have only 124 distinct visible inputs. The primary retrieval retains one group per input. The secondary control pools every training label/count for each identical input, keeping **exactly the same selected example IDs, order, shot counts, actor messages, mechanics and predictor settings**. It uses training inputs/labels only. This control was specified and called after prospective test play began, so it is a separate input-only secondary comparison, not part of the original prospective freeze. No test outcomes select its examples, pooling rule or settings.','',
        '| Holdout | Original 4-shot | Pooled 4-shot | Pooled 8-shot | Pooled 16-shot | Learned linear | Original 4-shot + learned correction |','|---|---:|---:|---:|---:|---:|---:|']
    for suite in ('parameter','family'):
        ss={r['method']:r['score'] for r in s['scores'] if r['size']==440 and r['suite']==suite and r['target']=='win'}
        lines.append('| '+suite+' | '+' | '.join(f"{ss[k]:.4f}" for k in ('few_4','pooled_few_4','pooled_few_8','pooled_few_16','linear','corrected_4'))+' |')
    lines+=['','Pooling fixes underuse of labels for identical visible inputs, but the fitted learner still compresses all training groups while a prompt contains at most 16 examples. This is a practical training-versus-prompting comparison, not an isolated test of architecture with identical label access.','',
        '## Repetition and parameter effects','',
        'Repeated native traces are independently sampled LLM decisions under identical configuration, world seed, seat, model and prompt. A changed action sequence is therefore possible even when the starting state is identical. Seed repetitions are not new game designs. We report within-condition outcome variance separately from deterministic replay correctness.','',
        '| Family | Episodes | Exact conditions | Conditions with varying win/solution labels | Mean within-condition win variance |','|---|---:|---:|---:|---:|']
    for r in s['repeatability']:
        t=r['targets'].get('win',{});lines.append(f"| {r['title']} | {r['episodes']} | {r['conditions']} | {t.get('varying_conditions',0)} | {t.get('within_condition_variance',0):.4f} |")
    lines+=['','Within-condition sample variance estimates one component of the attainable Brier/MSE floor under this observation and repetition protocol. It is noisy, especially with two repetitions. `noise_subtracted` subtracts that estimate from predictive error and can be negative due to estimation noise; it is not proof that all remaining error is learnable. Unobserved world variation between seeds can add further uncertainty.','',
        '| Family / behavior | Parameter | Low (measured episodes) | Base (measured episodes) | High (measured episodes) |','|---|---|---:|---:|---:|']
    for r in s['parameters']:lines.append(f"| {r['title']} / {r['target']} | {r['axis']} | "+' | '.join(f"{l['behavior']:.3f} (n={l['measured_behavior_episodes']})" if l['behavior'] is not None else '—' for l in r['levels'])+' |')
    lines+=['','### Model differences in fresh normal-prompt episodes','',
        '| Family | Qwen win / solution rate | GLM win / solution rate | Paired win difference | Qwen invalid-episode rate | GLM invalid-episode rate |','|---|---:|---:|---:|---:|---:|']
    for r in s['models']['families']:
        v=r['targets']['win'];invalid=r['targets']['any_invalid'];lines.append(f"| {r['title']} | {v['qwen']:.3f} | {v['glm']:.3f} | {v['qwen_minus_glm']:+.3f} | {invalid['qwen']:.3f} | {invalid['glm']:.3f} |")
    lines+=['',s['models']['note']+' Full behavior-rate differences are retained in summary.json.','']
    lines+=['','Each anchor setting has 40 episodes, with two models × two world seeds × both seats × five repetitions. Lower/base values were collected before forecasting; higher values were collected afterward. This improves replication and removes seed/seat confounding, but collection batch is still coupled to the prospective parameter split.','',
        '## Representation and label contracts','',
        'The release includes standardized initialization/information, transitions/payoffs, termination, parser and invalid-action fields, exact actor opening messages, numerical scripted-opponent policies, and an archived executable native source bundle. The complete executable rules remain authoritative; the LLM uses a compact normalized rendering. Hidden opponent realizations and future events are excluded. A specification revision before fresh test play corrects positive auction bids, duplicate/partial bid processing, auction and negotiation private-value distributions, Liar’s Dice elimination and Pig’s horizon timing. Earlier forecasts made with the initial wording are preserved under prediction/preflight and excluded from scoring.','',
        'New supported measures cover auction budget use, dice challenges, negotiation offers/acceptance, Ultimatum offer shares/acceptance, normalized numeric guesses, secretary selection timing, and memory use of known pairs/new cards. Definitions record actual eligibility; fixed-role Ultimatum targets are masked before outcomes are known. Unsupported targets stay null. Intent, deception, exploitation and a general psychological exploration trait are not inferred.','',
        f"Native replay: **{s['audit']['new_native_transitions']:,} transitions** across the new collection. Independent accounting checks: `{s['audit']['independent_checks']}`. All raw inference links and global/stage ledgers reconcile. The source archive and exact prompts preserve every collection and prediction setting.",'',
        '## Prospective chronology and usage','',
        f"All 2,112 primary test predictions and fitted artifacts were frozen at **{s['audit']['prediction']['frozen_at']}**. The first fresh test-player call was **{s['audit']['prediction']['first_test_call']}**. All three training sizes predict the same fixed test conditions. The 264 supplemental pooled-example predictions have separate later timestamps and are marked secondary.",'',
        f"This stage made {s['audit']['inference']['total_calls']:,} inference attempts, with **${s['audit']['inference']['reported_usd']:.4f}** reported cost and {s['audit']['inference']['unknown_cost_calls']} calls lacking final cost. This includes retained preflight forecasts; group-level usage is in summary.json. The global ceiling was $75; no budget increase was made.",'',
        'The family expansion is a targeted sample of four new decision structures, not a representative random sample of all games. Only two player models and one new prompt condition are tested. Learning-curve growth is concentrated in the four anchor families, so these curves measure added depth and repetition rather than a controlled increase in training-family breadth. The new families remain a prospective transfer test.','',
        '```bash','/shared/allie/venvs/hole/bin/python -B -m prediction.general_games.scaleup_v2.readout','/shared/allie/venvs/hole/bin/python -B -m pytest prediction/general_games/scaleup_v2/test_contracts.py prediction/general_games/scaleup_v2/test_predict.py -q','```','']
    return '\n'.join(lines)


def build():
    train,train_actions,checks_a=load_phase('training');test,test_actions,checks_b=load_phase('test');old,old_actions=legacy_rows()
    assert len(train)==320 and len(test)==272 and len(old)==144
    assert all(r['status']=='complete' for r in train+test),'Do not publish a complete-cohort report with missing/censored outcomes'
    predictions,queries,pred_audit=prediction_audit()
    from .pooled_fewshot import export as pooled_export,FOLDER as POOLED
    predictions+=pooled_export();pooled_audit=read_json(POOLED/'audit.json')
    pooled_specified=read_json(POOLED/'manifest.json')['created'];pooled_started=min(read_json(p)['timestamp'] for p in (POOLED/'raw_calls').glob('*.json'))
    assert pred_audit['first_test_call']<pooled_specified<pooled_started
    pooled_audit.update(specified_at=pooled_specified,first_call=pooled_started)
    score_rows,comparisons=scores(test,predictions,queries);new=train+test
    support=[]
    for target in TARGETS:
        rr=[r for r in new+old if r['targets'][target] is not None]
        support.append(dict(target=target,definition=DEFINITIONS[target],episodes=len(rr),families=sorted({r['inputs']['family_id'] for r in rr}),
            opportunities=len(rr) if target in ('win','any_invalid') else sum(r['opportunities'].get(target,{}).get('count',0) for r in rr)))
    summary=dict(created=now(),version='replicated-general-v2',counts=dict(families=16,configurations=57,new_episodes=len(new),all_episodes=len(new+old),
        new_focal_actions=len(train_actions+test_actions),all_focal_actions=len(train_actions+test_actions+old_actions),new_invalid_actions=sum(r['invalid_actions'] for r in new),new_statuses=dict(Counter(r['status'] for r in new))),
        scores=score_rows,comparisons=comparisons,learning_progress=learning_progress(score_rows),repeatability=repeatability(new),parameters=parameter_effects(new),models=model_effects(new),label_support=support,
        audit=dict(status='passed',new_native_transitions=sum(r['native_transitions'] for r in new),independent_checks=dict(Counter(checks_a)+Counter(checks_b)),
            prediction=pred_audit,pooled_secondary=pooled_audit,serialized_models=serialized_model_audit(),inference=inference_audit()))
    summary['findings']=findings(summary)
    jsonl(STUDY/'all-episodes.jsonl',old+new);jsonl(STUDY/'all-actions.jsonl',old_actions+train_actions+test_actions)
    write_json(STUDY/'predictions.json',predictions);write_json(STUDY/'summary.json',summary);(STUDY/'REPORT.md').write_text(report(summary))
    return summary


if __name__=='__main__':
    s=build();print(json.dumps(s['counts'],indent=2));print(json.dumps(s['audit'],indent=2))

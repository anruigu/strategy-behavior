import copy
import math
from pathlib import Path
import tempfile
import unittest

from prediction.improve.data import TARGETS,aggregate_records,build_folds,write_new
from prediction.improve.test_data import synthetic_records,PROTOCOL
from prediction.improve.evaluate import (join_forecasts,evaluate,group_rows,summarize,
    bootstrap_contrast,score_files)


def fixture():
    train=aggregate_records(synthetic_records(42),PROTOCOL)
    development=aggregate_records(synthetic_records(7,5678),PROTOCOL)
    data=dict(train_examples=train,development_examples=development)
    folds=build_folds(train,development)
    rows=[]
    for fold in folds:
        dataset=train if fold['test_dataset']=='train' else development
        for i in fold['test']:
            row=dataset[i]
            for target in TARGETS:
                for method,p in [('family',.5),('calibrated_payoff_dominant',.5),('qwen3_frozen_head',.45),('qwen3_lora_head',.4)]:
                    rows.append(dict(row_id=row['row_id'],game_id=row['game_id'],group_id=row['group_id'],
                        model=row['model'],opponent=row['opponent'],method=method,split=fold['split'],fold_id=fold['fold_id'],
                        target=target,prediction=p if row['targets'][target]['applicable'] else None))
    return data,folds,rows


class EvaluateTests(unittest.TestCase):
    def test_duplicate_missing_mismatched_and_nonfinite_forecasts_rejected(self):
        data,folds,rows=fixture()
        with self.assertRaisesRegex(ValueError,'Duplicate'):join_forecasts(data,folds,rows+[rows[0]])
        with self.assertRaisesRegex(ValueError,'Missing'):join_forecasts(data,folds,rows[1:])
        bad=copy.deepcopy(rows);bad[0]['model']='wrong'
        with self.assertRaisesRegex(ValueError,'metadata'):join_forecasts(data,folds,bad)
        bad=copy.deepcopy(rows);bad[0]['prediction']=float('nan')
        with self.assertRaisesRegex(ValueError,'finite probability'):join_forecasts(data,folds,bad)
        missing_fold=[r for r in rows if not (r['method']=='qwen3_lora_head' and r['fold_id']=='family_chicken')]
        with self.assertRaisesRegex(ValueError,'Missing'):join_forecasts(data,folds,missing_fold)

    def test_exact_event_scores_and_game_weighting(self):
        rows=[dict(group_id='g1',family='harmony',opportunities=80,successes=40,value=.5,prediction=.25),
              dict(group_id='g2',family='harmony',opportunities=8,successes=8,value=1.,prediction=.75)]
        score=summarize(group_rows(rows))
        self.assertAlmostEqual(score['event_brier'],(.3125+.0625)/2)
        self.assertAlmostEqual(score['rate_mse'],.0625)
        self.assertAlmostEqual(score['mean_observed'],.75)
        self.assertAlmostEqual(score['calibration_ece'],.25)

    def test_supports_masks_and_paired_directions(self):
        data,folds,rows=fixture()
        rows += [dict(row,method='llm_few_shot') for row in rows if row['method']=='family' and row['split']=='development']
        for row in rows:
            if row['method']=='llm_few_shot' and row['split']=='development' and row['target']=='action0':
                row['prediction']=None;break
        scores,contrasts,groups,audit=evaluate(data,folds,rows,repetitions=30)
        relevant=[c for c in scores['coverage'] if c['split']=='development' and c['target']=='action0']
        numerical=next(c for c in relevant if c['support']=='numerical_only')
        common=next(c for c in relevant if c['support']=='all_methods')
        self.assertEqual(numerical['common_examples'],common['common_examples']+1)
        self.assertIn('qwen3_lora_head',numerical['methods'])
        self.assertTrue(any(c['support']=='numerical_only' and c['split']=='development' and c['method']=='qwen3_lora_head' for c in contrasts))
        family=[c for c in contrasts if c['split']=='family' and c['family']=='all']
        self.assertTrue(family)
        self.assertTrue(all(c['seven_family_cluster_sensitivity']['declared_clusters']==7 for c in family))
        for comparison in contrasts:
            interval=comparison['game_bootstrap']['intervals']['event_brier']
            self.assertLessEqual(interval['lower'],interval['upper'])

    def test_known_constant_improvement_and_cluster_sensitivity(self):
        base=group_rows([dict(group_id='g'+str(i),family=f,opportunities=8,successes=8,value=1.,prediction=.5)
                        for i,f in enumerate(('harmony','chicken','stag_hunt'))])
        method=copy.deepcopy(base)
        for row in method:row['event_brier']-=.1
        contrast=bootstrap_contrast(base,method,50)
        self.assertAlmostEqual(contrast['intervals']['event_brier']['improvement'],.1)
        self.assertAlmostEqual(contrast['intervals']['event_brier']['lower'],.1)
        family=bootstrap_contrast(base,method,50,cluster='family')
        self.assertEqual(family['declared_clusters'],7)
        self.assertEqual(family['eligible_family_clusters'],3)

    def test_development_only_prompted_baseline_has_explicit_split_scope(self):
        data,folds,rows=fixture()
        llm=[dict(row,method='llm_few_shot') for row in rows if row['method']=='family' and row['split']=='development']
        scores,contrasts,_,_=evaluate(data,folds,rows+llm,repetitions=20)
        self.assertIn('llm_few_shot',scores['available_methods_by_split']['development'])
        self.assertNotIn('llm_few_shot',scores['available_methods_by_split']['family'])
        self.assertTrue(any(c['baseline']=='llm_few_shot' and c['split']=='development' for c in contrasts))

    def test_fresh_family_excluded_has_seven_family_sensitivity(self):
        data,folds,rows=fixture()
        folds=[dict(f,split='fresh_family_excluded') for f in folds if f['split']=='family']
        rows=[dict(r,split='fresh_family_excluded') for r in rows if r['split']=='family']
        _,contrasts,_,_=evaluate(data,folds,rows,repetitions=20)
        aggregate=[c for c in contrasts if c['family']=='all']
        self.assertTrue(aggregate)
        self.assertTrue(all(c['seven_family_cluster_sensitivity']['declared_clusters']==7 for c in aggregate))

    def test_saved_synthetic_score_outputs_are_hash_audited(self):
        import json
        data,folds,rows=fixture()
        with tempfile.TemporaryDirectory(dir='/shared/allie/home/.codex/tmp') as folder:
            root=Path(folder)
            write_new(root/'data.json',data);write_new(root/'folds.json',folds)
            with (root/'forecasts.jsonl').open('x') as handle:
                for row in rows:handle.write(json.dumps(row)+'\n')
            result=score_files(root/'data.json',root/'folds.json',[root/'forecasts.jsonl'],root/'out',20)
            self.assertGreater(result['contrasts'],0)
            audit=json.loads((root/'out/audit.json').read_text())
            self.assertEqual(audit['status'],'verified');self.assertFalse(audit['fitting_performed'])
            with self.assertRaises(FileExistsError):score_files(root/'data.json',root/'folds.json',[root/'forecasts.jsonl'],root/'out',20)


if __name__=='__main__':unittest.main()

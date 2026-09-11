"""Fixed-support descriptive prompt comparisons after prospective scoring.

No fitting, forecast updates, or API calls. These contrasts are interpretation,
not additions to the original primary method-selection or stopping rules.
"""
import json
import hashlib
from collections import defaultdict
from datetime import datetime,timezone
from pathlib import Path
import sys
sys.path.insert(0,'/shared/allie/strategy-behavior')
from prediction.analysis import _prediction_key,_valid,score_rows,paired_improvement_intervals
from prediction.secondary_analysis import verified_evaluation

ROOT=Path('/shared/allie/strategy-behavior/prediction/results/overnight-20260910')
TARGETS=('action0','first_action0','cooperation','coordination')
CONTRASTS=(('llm_zero_shot','llm_few_shot'),('llm_zero_shot','llm_game_theory'),
           ('combined_logistic_both','llm_zero_shot'),('combined_logistic_both','llm_few_shot'),
           ('combined_logistic_both','llm_game_theory'),('family','combined_logistic_both'))

def file_hash(path):
 d=hashlib.sha256()
 with Path(path).open('rb') as h:
  for block in iter(lambda:h.read(1024*1024),b''):d.update(block)
 return d.hexdigest()

def main():
 evaluation=ROOT/'prospective/evaluation';out=ROOT/'independent-analysis/prospective-prompt-comparisons.json'
 assert not out.exists()
 audit_path=evaluation/'audit.json';audit_bytes=audit_path.read_bytes();audit=json.loads(audit_bytes)
 paths={audit_path,evaluation/'scores.json',evaluation/'joined-predictions.jsonl',Path(__file__).resolve(),
   Path('/shared/allie/strategy-behavior/prediction/analysis.py'),Path('/shared/allie/strategy-behavior/prediction/modeling.py'),
   Path('/shared/allie/strategy-behavior/prediction/secondary_analysis.py')}
 paths.update(Path(p) for p in audit['source_sha256'])
 before={str(p.resolve()):file_hash(p) for p in paths}
 assert before[str(audit_path.resolve())]==hashlib.sha256(audit_bytes).hexdigest()
 verified_evaluation(evaluation)
 scores=json.loads((evaluation/'scores.json').read_text())
 buckets=defaultdict(lambda:defaultdict(dict));all_methods=defaultdict(set)
 with (evaluation/'joined-predictions.jsonl').open() as h:
  for line in h:
   r=json.loads(line)
   if r['target'] not in TARGETS:continue
   key=(r['split'],r['target']);all_methods[key].add(r['method'])
   if _valid(r):
    k=_prediction_key(r);assert k not in buckets[key][r['method']]
    buckets[key][r['method']][k]=r
 saved={(r['split'],r['target'],r['method']):r for r in scores['scores']}
 support={(r['split'],r['target']):r['common_rows'] for r in scores['support']}
 results=[]
 for key,methods in sorted(all_methods.items()):
  common=set.intersection(*(set(buckets[key][m]) for m in methods));assert len(common)==support[key]
  if not common:continue
  for baseline,method in CONTRASTS:
   if baseline not in methods or method not in methods:continue
   a=[buckets[key][baseline][k] for k in sorted(common)];b=[buckets[key][method][k] for k in sorted(common)]
   sa,sb=score_rows(a),score_rows(b)
   for name,s in [(baseline,sa),(method,sb)]:
    assert abs(s['event_brier']-saved[key[0],key[1],name]['event_brier'])<1e-12
   results.append(dict(split=key[0],target=key[1],baseline=baseline,method=method,positive_favors=method,
    groups=sa['groups'],episodes=sa['episodes'],rows=sa['rows'],opportunities=sa['opportunities'],
    improvement={m:sa[m]-sb[m] for m in ['event_brier','event_log_loss','rate_mae']},
    intervals=paired_improvement_intervals(a,b,repetitions=scores['uncertainty']['repetitions'],seed=scores['uncertainty']['seed'])))
 assert before=={str(p.resolve()):file_hash(p) for p in paths}
 result=dict(created_utc=datetime.now(timezone.utc).isoformat(),classification='descriptive_fixed_prospective_prompt_contrasts',
   changes_to_primary_forecasts_or_methods=False,source_sha256=before,
   support='Exact original combined numerical-plus-LLM all-method supported row intersection.',
   uncertainty=scores['uncertainty'],comparisons=results)
 with out.open('x') as h:json.dump(result,h,indent=2,allow_nan=False);h.write('\n')
 print(json.dumps(dict(output=str(out),contrasts=len(results))))

if __name__=='__main__':main()

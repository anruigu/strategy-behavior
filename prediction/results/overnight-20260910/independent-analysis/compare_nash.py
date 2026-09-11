"""Post-evaluation interpretation only; no fitting, forecasts, or API calls.

Uses every method's original valid-key intersection, then existing paired
game/episode bootstrap helpers. Output is an additional immutable artifact.
"""
import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, '/shared/allie/strategy-behavior')
from prediction.analysis import _prediction_key, _valid, paired_improvement_intervals, score_rows

TARGETS = ('action0', 'first_action0', 'cooperation', 'coordination')
METHODS = ('raw_logistic', 'combined_logistic_both', 'combined_mlp_both')


def sha(path):
    result=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            result.update(chunk)
    return result.hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--evaluation', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args=parser.parse_args()
    if not args.output.resolve().is_relative_to(Path('/shared/allie')):
        raise ValueError('Output must be under shared storage')
    if args.output.exists():
        raise FileExistsError('Independent analyses do not overwrite existing artifacts')
    scores_path=args.evaluation/'scores.json'
    predictions_path=args.evaluation/'predictions.jsonl'
    paths=[scores_path, predictions_path, Path('/shared/allie/strategy-behavior/prediction/analysis.py')]
    before={str(path.resolve()):sha(path) for path in paths}
    scores=json.loads(scores_path.read_text())
    valid=defaultdict(lambda:defaultdict(set))
    selected=defaultdict(lambda:defaultdict(dict))
    with predictions_path.open() as stream:
        for line in stream:
            row=json.loads(line)
            if row['target'] not in TARGETS:
                continue
            bucket=row['split'],row['target']
            method=row['method']
            valid[bucket][method]  # Retain methods with zero valid forecasts.
            if _valid(row):
                key=_prediction_key(row)
                if key in valid[bucket][method]:
                    raise ValueError('Duplicate method/split/target/fold/row key')
                valid[bucket][method].add(key)
                if method in METHODS or method=='nash':
                    selected[bucket][method][key]=row
    saved_support={(row['split'],row['target']):row for row in scores['support']}
    saved_scores={(row['split'],row['target'],row['method']):row for row in scores['scores']}
    comparisons=[]
    for (split,target),methods in sorted(valid.items()):
        common=set.intersection(*methods.values()) if methods else set()
        assert len(common)==saved_support[split,target]['common_rows']
        if not common or 'nash' not in selected[split,target]:
            continue
        nash=[selected[split,target]['nash'][key] for key in sorted(common)]
        nash_scores=score_rows(nash)
        assert abs(nash_scores['event_brier']-saved_scores[split,target,'nash']['event_brier'])<1e-12
        for method in METHODS:
            rows=[selected[split,target][method][key] for key in sorted(common)]
            actual=score_rows(rows)
            assert abs(actual['event_brier']-saved_scores[split,target,method]['event_brier'])<1e-12
            comparisons.append(dict(split=split,target=target,method=method,baseline='nash',
                positive_means_improvement=True,common_rows=len(rows),groups=actual['groups'],
                episodes=actual['episodes'],opportunities=actual['opportunities'],
                improvement={name:nash_scores[name]-actual[name]
                    for name in ('event_brier','event_log_loss','rate_mae')},
                intervals=paired_improvement_intervals(nash,rows,
                    repetitions=scores['uncertainty']['repetitions'],seed=scores['uncertainty']['seed'])))
    after={str(path.resolve()):sha(path) for path in paths}
    assert before==after,'Evaluation inputs or helpers changed during independent analysis'
    result=dict(created_utc=datetime.now(timezone.utc).isoformat(),source_sha256=before,
        scope='post-evaluation interpretation; no fitting, tuning or changes to forecast probabilities',
        common_support='exact original all-method intersection, verified against saved scores',
        uncertainty=scores['uncertainty'],comparisons_to_nash=comparisons)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    with args.output.open('x') as stream:
        json.dump(result,stream,indent=2,allow_nan=False)
        stream.write('\n')
    print(json.dumps(dict(output=str(args.output),comparisons=len(comparisons))))


if __name__=='__main__':
    main()

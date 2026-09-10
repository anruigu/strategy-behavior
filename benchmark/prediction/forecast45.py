"""Apply a fitted pilot artifact to precomputed structural features of future games."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import math
from pathlib import Path
from model45 import predict


def forecast(artifact,features,player,condition):
    if player not in artifact['known_player_models']:
        raise ValueError('Unseen player model; this pilot does not support model-generalization forecasts')
    context=player+'|'+condition
    if 'encoder' in artifact and context not in artifact['encoder']['contexts']:
        raise ValueError('Unseen model/prompt context')
    required=set(artifact['feature_schema']['game_features'])|set(artifact['feature_schema']['witness_features'])
    rows=[]
    for item in features:
        if not required<=item['features'].keys():raise ValueError('Required structural features missing')
        if not all(math.isfinite(float(item['features'][key])) for key in required):raise ValueError('Features must be finite numbers')
        rows.append(dict(model=player,phase=condition,mechanism='',features=item['features']))
    probabilities=predict(artifact,rows)
    return [dict(target=item.get('target'),seed=item.get('seed'),player_model=player,condition=condition,
                 probability=float(p),in_training_target=item.get('target') in artifact['trained_targets'])
            for item,p in zip(features,probabilities)]

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--artifact',type=Path,required=True);p.add_argument('--features',type=Path,required=True)
    p.add_argument('--player-model',required=True);p.add_argument('--condition',choices=['win_only','exploration','hinted'],required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists():raise FileExistsError('Forecast output already exists; preserve timestamped forecasts')
    artifact=json.loads(a.artifact.read_text());features=json.loads(a.features.read_text())
    result=dict(created=datetime.now(timezone.utc).isoformat(),artifact_sha256=hashlib.sha256(a.artifact.read_bytes()).hexdigest(),
                features_sha256=hashlib.sha256(a.features.read_bytes()).hexdigest(),predictions=forecast(artifact,features,a.player_model,a.condition))
    a.out.parent.mkdir(parents=True,exist_ok=True);a.out.write_text(json.dumps(result,indent=2)+'\n')

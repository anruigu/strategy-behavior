"""Fleet-only technical check; no outcomes, optimization, or model fitting."""
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import sys
import time

if os.environ.get('PREDICTION_FLEET_TRAINING') != '1' or not os.environ.get('FLEET_RUN_NAME'):
    raise RuntimeError('Preflight must execute inside the authorized Fleet job')

root = Path('/mnt/sfs/allie/strategy-behavior')
out = root / 'prediction/results/improve-20260910/fleet-runtime/preflight-result.json'
result = {'timestamp':time.time(), 'python':sys.version, 'run_name':os.environ['FLEET_RUN_NAME'],
          'packages':{}, 'shared_storage_verified':False}
for name in ['torch','transformers','peft','accelerate','numpy','scipy','scikit-learn','safetensors','huggingface-hub']:
    try:
        result['packages'][name] = importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        result['packages'][name] = None
data = root / 'prediction/results/improve-20260910/data/data.json'
result['data_sha256'] = hashlib.sha256(data.read_bytes()).hexdigest()
result['shared_storage_verified'] = True
import torch
result['gpu'] = {'count':torch.cuda.device_count(), 'name':torch.cuda.get_device_name(0),
                 'memory_bytes':torch.cuda.get_device_properties(0).total_memory,
                 'bf16_supported':torch.cuda.is_bf16_supported()}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2), flush=True)

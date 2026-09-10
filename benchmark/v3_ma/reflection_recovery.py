"""One checkpoint-preserving recovery with a documented transport-only amendment."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from benchmark.clients import now, write_json
from benchmark.v3_ma import reflection

TIMEOUT = 600


class RecoveryClient(reflection.ReflectionClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = self.client.with_options(timeout=TIMEOUT)


def run(out):
    if (out/'recovery.json').exists():
        raise ValueError('The one recovery pass has already been started')
    source = Path(__file__).resolve()
    source_copy = out/'transport-amendment-source.py'
    amendment = dict(recorded=now(), stage='single_recovery_pass',
        original_timeout_seconds=180, recovery_timeout_seconds=TIMEOUT,
        reason='Successful GLM reflections had a median duration near 150 seconds; the shorter timeout censored many reflection branches. Restore the base client transport allowance.',
        unchanged=['model request bodies', 'model configurations', 'prompts', 'token allowances',
                   'context bound', 'budget ceiling', 'retry count', 'one recovery pass',
                   'checkpointed replies and notes', 'paired estimands'],
        workers=24, plan_sha256=hashlib.sha256((out/'plan.json').read_bytes()).hexdigest(),
        source_file=source_copy.name, source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    if (out/'transport-amendment.json').exists():
        raise ValueError('Transport amendment already recorded; inspect existing execution before restarting')
    shutil.copyfile(source, source_copy)
    write_json(out/'transport-amendment.json', amendment)
    # The frozen launch routine explicitly takes its client class from this module
    # attribute. Only the transport wait changes; request generation is inherited.
    reflection.ReflectionClient = RecoveryClient
    reflection.launch(out, workers=24, recover=True)


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    run(args.out)

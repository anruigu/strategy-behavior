"""V4 client: identical routing/accounting with explicit actor/predictor byte ceilings.

Copied from prediction.client; historical collectors are unchanged.
"""
from dataclasses import asdict
import json
from pathlib import Path
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'hole_exp'))
from benchmark.clients import ModelClient, ModelConfig, MODELS
from benchmark.fullscale.budget import Ledger, BudgetExceeded
from prediction.io_utils import write_json, now


class Client(ModelClient):
    locks = {}
    guard = threading.Lock()

    def __init__(self, config, log_dir, ledger, stage_ledger, max_tokens=4096, max_request_bytes=160000):
        super().__init__(config, log_dir)
        self.client = self.client.with_options(timeout=120, max_retries=0)
        self.ledger, self.stage_ledger, self.max_tokens = ledger, stage_ledger, max_tokens
        self.max_request_bytes = max_request_bytes
        with self.guard:
            if config.model_id not in self.locks:
                self.locks[config.model_id] = threading.BoundedSemaphore(12)
        self.semaphore = self.locks[config.model_id]

    def generate(self, messages, purpose='play'):
        size = len(json.dumps(messages, ensure_ascii=False).encode()) + 4096 + 256 * len(messages)
        if size > self.max_request_bytes:
            raise ValueError('Public-history context exceeded fixed byte limit')
        # OpenRouter routing is explicitly limited to these conservative prices.
        bound = 0.0 if self.config.provider == 'flt' else size * .00002 + self.max_tokens * .00012
        with self.semaphore:
            stage_id = self.stage_ledger.reserve(self.config.model_id, bound)
            try:
                ident = self.ledger.reserve(self.config.model_id, bound)
            except Exception:
                self.stage_ledger.settle(stage_id, 0, 'No request: global reservation failed')
                raise
            request = dict(model=self.config.provider_model, messages=messages, max_tokens=self.max_tokens,
                           temperature=self.config.temperature,
                           extra_body={'reasoning': {'effort': self.config.reasoning_effort}})
            if request['temperature'] is None:
                del request['temperature']
            if self.config.provider == 'openrouter':
                request['extra_body']['provider'] = {'max_price': {'prompt': 20, 'completion': 120, 'request': 0}}
            record = dict(call_id=ident, stage_call_id=stage_id, timestamp=now(), purpose=purpose,
                          config=asdict(self.config), request=request, reserved_usd=bound, status='reserved')
            path = self.log_dir / (ident + '.json')
            write_json(path, record)
            start = time.monotonic()
            try:
                response = self.client.chat.completions.create(**request)
                raw = response.model_dump(mode='json')
            except Exception as exc:
                # Unknown charges remain reserved in both ledgers.
                self.ledger.settle(ident, None, type(exc).__name__)
                self.stage_ledger.settle(stage_id, None, type(exc).__name__)
                record.update(status='transport_error', seconds=time.monotonic()-start,
                              error=type(exc).__name__, http_status=getattr(exc, 'status_code', None),
                              error_message=str(exc).replace(self.client.api_key, '[REDACTED]')[:1200])
                write_json(path, record)
                return '', dict(call_id=ident, status='transport_error', http_status=record['http_status'])
            # Preserve every received response before parsing provider-specific fields.
            record.update(status='received', seconds=time.monotonic()-start, response=raw)
            write_json(path, record)
            usage = raw.get('usage') or {}
            costs = [v for v in (usage.get('cost'), (usage.get('cost_details') or {}).get('upstream_inference_cost'))
                     if isinstance(v, (int, float)) and v >= 0]
            cost = 0.0 if self.config.provider == 'flt' else max(costs) if costs else None
            self.ledger.settle(ident, cost, 'Includes upstream BYOK cost; FLT hosted allocation')
            self.stage_ledger.settle(stage_id, cost, 'Includes upstream BYOK cost; FLT hosted allocation')
            try:
                choice = raw['choices'][0]
                message = choice['message']
                content, finish = message.get('content') or '', choice['finish_reason']
                status = ('refusal' if finish == 'content_filter' or message.get('refusal')
                          else 'truncated' if finish == 'length'
                          else 'invalid_response' if finish != 'stop' or not isinstance(content, str) or not content.strip() else 'ok')
            except (KeyError, IndexError, TypeError):
                content, finish, status = '', None, 'invalid_response'
            record.update(status=status, seconds=time.monotonic()-start, response=raw, budget_cost_usd=cost)
            write_json(path, record)
            return content, dict(call_id=ident, status=status, actual_model=raw.get('model'),
                                 finish_reason=finish, usage=usage, budget_cost_usd=cost)


def configurations(names):
    from dataclasses import replace
    return {name: asdict(replace(MODELS[name], temperature=.7, seed=None, reasoning_effort='low')) for name in names}

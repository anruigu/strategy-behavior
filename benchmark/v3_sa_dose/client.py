"""One fixed-size request; reserve before sending and count BYOK upstream cost."""
from dataclasses import asdict
import json
import math
import time

from benchmark.clients import ModelClient, now, write_json


def billed_cost(raw, provider):
    usage = raw.get('usage') or {}
    values = [usage.get('cost'), (usage.get('cost_details') or {}).get('upstream_inference_cost')]
    costs = [float(v) for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)
             and math.isfinite(v) and v >= 0]
    return 0.0 if provider == 'flt' else max(costs) if costs else None


class Client(ModelClient):
    def __init__(self, config, log_dir, ledger):
        super().__init__(config, log_dir)
        self.ledger = ledger

    def generate(self, messages, *, max_tokens=16384):
        if not 1 <= max_tokens <= 16384:
            raise ValueError('Invalid output allowance')
        if self.config.seed is not None:
            raise ValueError('This protocol uses independent provider sampling without a request seed')
        size = len(json.dumps(messages, ensure_ascii=False).encode()) + 4096 + 256 * len(messages)
        if size > 120000:
            raise ValueError('Context byte bound exceeded; never truncate')
        bound = 0.0 if self.config.provider == 'flt' else size * .00002 + max_tokens * .00012
        call_id = self.ledger.reserve(self.config.model_id, bound)
        request = dict(model=self.config.provider_model, messages=messages, max_tokens=max_tokens,
                       extra_body={'reasoning': {'effort': self.config.reasoning_effort}})
        if self.config.provider == 'openrouter':
            request['extra_body']['provider'] = {'max_price': {'prompt': 20, 'completion': 120, 'request': 0}}
        if self.config.temperature is not None:
            request['temperature'] = self.config.temperature
        record = dict(call_id=call_id, timestamp=now(), config=asdict(self.config), request=request,
                      reserved_usd=bound, attempts=[])
        path = self.log_dir / f'{call_id}.json'
        write_json(path, record)
        start = time.monotonic()
        try:
            response = self.client.chat.completions.create(**request)
            raw = response.model_dump(mode='json')
        except Exception as exc:
            self.ledger.settle(call_id, None, type(exc).__name__)
            record['attempts'].append(dict(error=type(exc).__name__, seconds=time.monotonic() - start))
            write_json(path, record)
            # Provider exception strings may contain request headers; retain only the type.
            raise RuntimeError(f'Transport failure; call {call_id}; {type(exc).__name__}') from None
        cost = billed_cost(raw, self.config.provider)
        self.ledger.settle(call_id, cost, 'Includes upstream BYOK cost; FLT unbilled')
        record['attempts'].append(dict(response=raw, seconds=time.monotonic() - start))
        record['billed_usd'] = cost
        write_json(path, record)
        choice = response.choices[0]
        content, reason = choice.message.content or '', choice.finish_reason
        status = ('refusal' if reason == 'content_filter' or getattr(choice.message, 'refusal', None)
                  else 'truncated' if reason == 'length'
                  else 'invalid_response' if reason != 'stop' or not content.strip() else 'ok')
        return content, dict(call_id=call_id, actual_model=response.model, finish_reason=reason,
                             status=status, usage=raw.get('usage'), billed_usd=cost)

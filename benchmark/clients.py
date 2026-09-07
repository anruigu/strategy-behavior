"""One normalized OpenAI-compatible interface, explicit requested provider routing."""
from dataclasses import dataclass, asdict
from copy import deepcopy
from datetime import datetime, timezone
import json
import time
import uuid
from pathlib import Path
from openai import OpenAI
from run_referee_crossplay import _from_files, load_env_key, OPENROUTER

@dataclass(frozen=True)
class ModelConfig:
    model_id: str
    provider: str
    provider_model: str
    base_url: str
    key_env: str
    temperature: float | None = 0.0
    seed: int | None = None
    reasoning_effort: str = 'low'

MODELS = {
    'qwen-3.8-27b': ModelConfig('qwen-3.8-27b','flt','qwen3.8-27b','https://inference.flt.build/v1','FLEET_API_KEY'),
    'kimi-k3': ModelConfig('kimi-k3','flt','kimi-k3','https://inference.flt.build/v1','FLEET_API_KEY'),
    'glm': ModelConfig('glm','flt','glm-5.3','https://inference.flt.build/v1','FLEET_API_KEY'),
    'claude-haiku-4.5': ModelConfig('claude-haiku-4.5','openrouter','anthropic/claude-haiku-4.5',OPENROUTER,'OPENROUTER_API_KEY'),
    'gpt-5-mini': ModelConfig('gpt-5-mini','openrouter','openai/gpt-5-mini',OPENROUTER,'OPENROUTER_API_KEY'),
    'gemini-3.7-flash': ModelConfig('gemini-3.7-flash','openrouter','google/gemini-3.7-flash',OPENROUTER,'OPENROUTER_API_KEY'),
}


def now():
    return datetime.now(timezone.utc).isoformat()


def write_json(path, value):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    temp = Path(str(path)+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False)+'\n')
    temp.replace(path)


class ModelClient:
    def __init__(self, config, log_dir):
        self.config = config
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        # Existing loader, durable research file first: this host has known stale shell credentials.
        key = _from_files(config.key_env) or load_env_key(config.key_env)
        self.client = OpenAI(api_key=key, base_url=config.base_url, timeout=600, max_retries=0)

    def generate(self, messages, model=None, temperature=None, max_tokens=2500, purpose='play'):
        if model is not None and model != self.config.model_id:
            raise ValueError('Client/model mismatch')
        request = {'model': self.config.provider_model, 'messages': messages,
                   'max_tokens': max_tokens}
        requested_temperature = self.config.temperature if temperature is None else temperature
        if requested_temperature is not None:
            request['temperature'] = requested_temperature
        request['extra_body'] = {'reasoning': {'effort': self.config.reasoning_effort}}
        if self.config.seed is not None:
            request['seed'] = self.config.seed
        call_id = uuid.uuid4().hex
        record = {'call_id': call_id, 'purpose': purpose, 'timestamp': now(),
                  'config': asdict(self.config), 'transport_timeout_seconds': 600, 'request': request, 'attempts': []}
        path = self.log_dir / (call_id+'.json')
        for attempt in range(3):
            write_json(path, record)
            start = time.monotonic()
            try:
                response = self.client.chat.completions.create(**request)
                raw = response.model_dump(mode='json')
                choice = response.choices[0]
                content = choice.message.content or ''
                record['attempts'].append({'timestamp': now(), 'request': deepcopy(request), 'seconds': time.monotonic()-start,
                                           'response': raw})
                write_json(path, record)
                if content.strip() and choice.finish_reason not in ('length','content_filter'):
                    return content, {'call_id': call_id, 'actual_model': response.model,
                                     'finish_reason': choice.finish_reason, 'usage': raw.get('usage'),
                                     'timestamp': record['timestamp']}
                if choice.finish_reason == 'length':
                    request['max_tokens'] *= 2
                else:
                    time.sleep(1 + attempt)
            except Exception as exc:
                record['attempts'].append({'timestamp': now(), 'request': deepcopy(request), 'seconds': time.monotonic()-start,
                                           'error': type(exc).__name__+': '+str(exc)[:1000]})
                write_json(path, record)
                if attempt < 2:
                    time.sleep(2 ** attempt)
        raise RuntimeError(f'{self.config.model_id}: no complete response for {purpose}; call {call_id}')

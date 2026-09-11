"""Read-only, loopback dataset viewer. No model clients or training imports."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
from functools import lru_cache
import gzip
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parents[1]
DEFAULT_RUN = PROJECT/'prediction/results/improve-20260910'
DEFAULT_ORIGINAL = PROJECT/'prediction/results/overnight-20260910'
TARGETS = ('action0', 'cooperation', 'coordination')

def read(path):
    return json.loads(Path(path).read_text())

def checked_file(path, root):
    path = Path(path).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError('Source file is unavailable')
    return path

class Dataset:
    def __init__(self, run=DEFAULT_RUN, original=DEFAULT_ORIGINAL):
        self.run, self.original = Path(run).resolve(), Path(original).resolve()
        data = read(self.run/'data/data.json')
        self.protocol = data['protocol']
        self.examples, self.partitions, self.episodes = {}, {}, defaultdict(dict)
        sources = {
            'train': read(self.original/'training-records.json'),
            'development': read(self.original/'prospective/collected/records.json'),
        }
        self.records = sources
        for partition, key in [('train','train_examples'), ('development','development_examples')]:
            for example in data[key]:
                ident = example['row_id']
                if ident in self.examples:
                    raise ValueError('Duplicate context ID')
                self.examples[ident], self.partitions[ident] = example, partition
                for index in example['source_row_indices']:
                    record = sources[partition][index]
                    if any(record[k] != example[k] for k in ('game_id','group_id','model','opponent')):
                        raise ValueError('Original record does not match the aggregated context')
                    eid = record['episode_id']
                    if not re.fullmatch(r'[a-zA-Z0-9_.-]+', eid):
                        raise ValueError('Unexpected episode identifier')
                    phase = record.get('source_stage') or record['stage']
                    if phase not in ('pilot','pilot-oss','development','prospective'):
                        raise ValueError('Unexpected source phase')
                    path = checked_file(self.original/phase/'episodes'/eid/'trace.json', self.original)
                    ref = self.episodes[ident].setdefault(eid, dict(id=eid, source_stage=phase,
                        trial_id=record['trial_id'], swap=record['swap'], focal_seats=[], path=path))
                    if ref['path'] != path:
                        raise ValueError('Episode source collision')
                    ref['focal_seats'].append(record['player_index'])
                if set(example['episode_ids']) != set(self.episodes[ident]):
                    raise ValueError('Episode membership mismatch')
        self.folds = read(self.run/'data/folds.json')
        self.memberships = defaultdict(list)
        for fold in self.folds:
            for role in ('train','test'):
                for ident in fold[role+'_row_ids']:
                    self.memberships[ident].append(dict(fold_id=fold['fold_id'], split=fold['split'], role=role))
        self.forecasts = defaultdict(list)
        paths = [self.run/'baselines/forecasts.jsonl', self.run/'development-few-shot/forecasts.jsonl']
        paths += sorted((self.run/'transformer').glob('*/*/forecasts.jsonl'))
        seen = set()
        for path in paths:
            if not path.is_file(): continue
            for line in path.read_text().splitlines():
                row = json.loads(line)
                ident = row['row_id']
                if ident not in self.examples or row['target'] not in TARGETS:
                    raise ValueError('Forecast outside the loaded dataset')
                key = (ident,row['fold_id'],row['method'],row['target'])
                if key in seen: raise ValueError('Duplicate forecast')
                seen.add(key)
                self.forecasts[ident].append({k:row[k] for k in ('fold_id','split','method','target','prediction')})
        catalog = []
        for ident, example in self.examples.items():
            item = {k:example[k] for k in ('row_id','game_id','family','model','opponent','payoffs')}
            item.update(partition=self.partitions[ident], episodes=len(self.episodes[ident]),
                rates={t:example['targets'][t]['value'] for t in TARGETS})
            catalog.append(item)
        self.catalog = dict(examples=catalog, targets=list(TARGETS), models=sorted(data['models']),
            families=sorted({e['family'] for e in catalog}), protocol=self.protocol,
            counts=dict(contexts=len(catalog), games=len({e['game_id'] for e in catalog}),
                training_contexts=len(data['train_examples']), development_contexts=len(data['development_examples']),
                episodes=len({(v['source_stage'],v['id']) for refs in self.episodes.values() for v in refs.values()})),
            description='Fixed 72-game training snapshot and the earlier 21-game development cohort. Fresh follow-up games were not played.')

    def detail(self, ident):
        example = self.examples[ident]
        fields = ('row_id','game_id','group_id','family','model','opponent','payoffs','protocol','input_text',
                  'targets','successes','opportunities','mask','weights','split_coordinate','applicability')
        return dict({k:example[k] for k in fields}, partition=self.partitions[ident],
            source_focal_rows=len(example['source_row_indices']),
            episodes=[{k:v for k,v in ref.items() if k!='path'} for ref in self.episodes[ident].values()],
            folds=self.memberships[ident], forecasts=self.forecasts[ident])

    @lru_cache(maxsize=64)
    def episode(self, ident, eid):
        ref = self.episodes[ident][eid]
        path = ref['path']; trace = read(path)
        if trace['id'] != eid or trace['game']['id'] != self.examples[ident]['game_id']:
            raise ValueError('Trace identity differs from the selected context')
        if trace['status'] != 'complete' or len(trace['rounds']) != self.protocol['rounds']:
            raise ValueError('Expected a complete original training/development trace')
        rounds = []
        for event in trace['rounds']:
            decisions = []
            for seat in (0,1):
                filename = f"round-{event['round']:02d}-player-{seat}.json"
                if event['decisions'][seat] != filename:
                    raise ValueError('Unexpected decision filename')
                decision = read(checked_file(path.parent/filename, self.original))
                messages = [{k:message[k] for k in ('role','content')} for message in decision['messages']]
                attempts = []
                for attempt in decision['attempts']:
                    meta = attempt.get('meta',{})
                    attempts.append(dict(reply=attempt.get('reply'), parse_error=bool(attempt.get('parse_error')),
                        **{k:meta.get(k) for k in ('status','actual_model','finish_reason')}))
                display = decision.get('displayed_action')
                if display not in (0,1) or (display ^ int(trace['swap'])) != event['actions'][seat]:
                    raise ValueError('Recorded display/canonical action mismatch')
                decisions.append(dict(seat=seat, model=trace['models'][seat], messages=messages,
                    attempts=attempts, status=decision['status'], displayed_action='AB'[display],
                    canonical_action=event['actions'][seat], context_focal=seat in ref['focal_seats']))
            rounds.append(dict(round=event['round'], actions=event['actions'], payoffs=event['payoffs'], decisions=decisions))
        return dict(id=eid, models=trace['models'], trial_id=trace['trial_id'], swap=trace['swap'],
            status=trace['status'], started=trace.get('started'), finished=trace.get('finished'),
            focal_seats=ref['focal_seats'], source_stage=ref['source_stage'], rounds=rounds)

def handler_for(dataset):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            url = urlsplit(self.path)
            args = parse_qs(url.query)
            try:
                if url.path == '/api/catalog': return self.send_json(dataset.catalog)
                if url.path == '/api/context': return self.send_json(dataset.detail(args['id'][0]))
                if url.path == '/api/episode': return self.send_json(dataset.episode(args['context'][0],args['id'][0]))
                static = {'/':('index.html','text/html'), '/app.js':('app.js','text/javascript'), '/style.css':('style.css','text/css')}
                if url.path in static:
                    name, kind = static[url.path]
                    return self.send_body((HERE/name).read_bytes(),kind+'; charset=utf-8')
                self.send_json({'error':'Not found'},404)
            except (KeyError,IndexError): self.send_json({'error':'Unknown context or episode'},404)
            except (ValueError,OSError): self.send_json({'error':'Source verification failed'},422)
        def send_json(self, value, status=200):
            self.send_body(json.dumps(value,ensure_ascii=False,allow_nan=False).encode(),'application/json; charset=utf-8',status)
        def send_body(self, body, kind, status=200):
            compressed = 'gzip' in self.headers.get('Accept-Encoding','') and len(body)>2048
            if compressed: body=gzip.compress(body)
            self.send_response(status)
            self.send_header('Content-Type',kind)
            self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self'; object-src 'none'; frame-ancestors 'none'")
            if compressed: self.send_header('Content-Encoding','gzip')
            self.end_headers(); self.wfile.write(body)
    return Handler

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--port',type=int,default=42328)
    p.add_argument('--host',default='127.0.0.1',choices=['127.0.0.1','localhost'])
    p.add_argument('--run-root',type=Path,default=DEFAULT_RUN)
    p.add_argument('--original-root',type=Path,default=DEFAULT_ORIGINAL)
    p.add_argument('--state-dir',type=Path,default=HERE/'state')
    a=p.parse_args()
    if not a.state_dir.resolve().is_relative_to(Path('/shared/allie')):
        raise ValueError('Viewer state must remain under /shared/allie')
    dataset=Dataset(a.run_root,a.original_root)
    server=ThreadingHTTPServer((a.host,a.port),handler_for(dataset))
    a.state_dir.mkdir(parents=True,exist_ok=True)
    port=server.server_address[1]
    state=dict(pid=os.getpid(),host=a.host,port=port,url=f'http://localhost:{port}',
        started=datetime.now(timezone.utc).isoformat(),run_root=str(a.run_root.resolve()),
        original_root=str(a.original_root.resolve()),counts=dataset.catalog['counts'])
    (a.state_dir/'server.json').write_text(json.dumps(state,indent=2)+'\n')
    print(json.dumps(state),flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()

if __name__=='__main__':main()

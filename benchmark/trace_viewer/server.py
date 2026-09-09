"""Read-only local browser for v3-SA and v3-MA traces."""
import argparse,json,sys,threading,time
from pathlib import Path
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from urllib.parse import urlparse,parse_qs
from types import SimpleNamespace
ROOT=Path('/shared/allie/strategy-behavior')
STATIC=Path(__file__).parent
REFERENCE=ROOT/'benchmark/results/gemini-engine49-20260908'
sys.path.insert(0,str(REFERENCE/'source'))
from benchmark.v3.specs import BY_ID
from benchmark.v3.evaluator import detected,attempted
sys.path.insert(0,str(STATIC))
import ma
MA_ROOT=ROOT/'benchmark/results/v3-ma-four-model-20260909'
RUNS={'gemini-original':('Gemini 3.7 Flash · original / high',REFERENCE)}
RUNS['gemini-revised45']=('Gemini 3.7 Flash · revised 45 / high',ROOT/'benchmark/results/gemini-revised45-20260909')
for m,n in [('gemini-3.1-pro','Gemini 3.1 Pro Preview'),('gpt-5.6-sol','GPT-5.6 Sol'),('grok-4.6','Grok 4.6')]:
 RUNS['frontier-'+m]=(n+' · revised 45 / high',ROOT/'benchmark/results/frontier45-20260909'/m)
for m,n in [('gemini-3.7-flash','Gemini 3.7 Flash'),('claude-haiku-4.5','Claude Haiku 4.5'),('gpt-5-mini','GPT-5 mini'),('qwen-3.8-27b','Qwen 3.8 27B'),('glm','GLM 5.3')]:
 RUNS[m]=(n+' · matched / low',ROOT/'benchmark/results/small-engine49-20260909'/m)
RUNS[ma.RUN_ID]=('v3-MA · four-model cross-play',MA_ROOT)
CACHE={};LOCK=threading.Lock()
def read(p):
 stamp=p.stat().st_mtime_ns
 with LOCK:
  old=CACHE.get(str(p))
  if old and old[0]==stamp:return old[1]
 obj=json.loads(p.read_text())
 with LOCK:CACHE[str(p)]=(stamp,obj)
 return obj

def card(t):
 try:return json.JSONDecoder().raw_decode(t['turns'][0]['observation'].split('\nCard: ',1)[1])[0]
 except (KeyError,IndexError,ValueError):return dict(title=t['game'])

def targets_for(root):
 return set(read(root/('targets.json' if (root/'targets.json').exists() else 'targets-49.json')))

def specs_for(root):
 registry=read(root/'manifest.json').get('registry')
 return {s['exploit_id']:SimpleNamespace(**s) for s in registry} if registry else BY_ID

def payoff_for(rid,eid,target,saved):
 if 'payoff_status' in saved:return saved
 path=ROOT/'benchmark/results/trace-payoff-audit-20260909/trace_evidence.json'
 if not path.exists():return saved
 model='Gemini high' if rid=='gemini-original' else rid
 row=next((r for r in read(path) if r['model']==model and r['episode']==eid and r['target']==target),None)
 if row is None:return saved
 status=('incomplete_control' if not row['control_done'] else 'information_requires_adaptive_control' if row['information'] else 'positive' if row['margin_delta']>0 else 'negative' if row['margin_delta']<0 else 'zero')
 return {**saved,'payoff_status':status,'final_score_delta':row['score_delta'] if row['control_done'] else None,'final_advantage_delta':row['margin_delta'] if row['control_done'] else None,'execution_count':row['executions'],'follow_up_actions':len(row['turns'])-row['first_turn'],'annotations':[]}

def index():
 runs=[]
 for rid,(name,root) in RUNS.items():
  if not (root/'manifest.json').exists():continue
  targets=targets_for(root);registry=specs_for(root);episodes=[]
  for p in sorted(root.glob('episodes/*/trace.json')):
   t=read(p);scores=[s for s in t['scores'] if s['exploit_id'] in targets and (not t['target'] or s['exploit_id']==t['target'])]
   episodes.append(dict(id=t['id'],game=t['game'],title=card(t)['title'],seed=t['seed'],condition=t['condition'],target=t['target'],target_name=registry[t['target']].description if t['target'] else None,turns=len(t['turns']),hits=sum(s['executed'] for s in scores),attempts=sum(s['attempted'] for s in scores),total=len(scores)))
  status=read(root/'status.json') if (root/'status.json').exists() else {}
  runs.append(dict(id=rid,name=name,episodes=episodes,status=status.get('status','starting'),errors=len(status.get('errors',[]))))
 if (MA_ROOT/'report.json').exists():runs.append(ma.index(MA_ROOT,read))
 return dict(runs=runs,updated=time.time())

def episode(rid,eid):
 if rid not in RUNS:raise KeyError('Unknown run')
 if not eid or '/' in eid or '\\' in eid or eid in ('.','..'):raise KeyError('Invalid episode')
 if rid==ma.RUN_ID:return ma.episode(MA_ROOT,eid,read)
 root=RUNS[rid][1];t=read(root/'episodes'/eid/'trace.json');targets=targets_for(root)
 specs=[s for s in specs_for(root).values() if s.game_id==t['game'] and s.exploit_id in targets]
 turns=[]
 for step,turn in enumerate(t['turns'],1):
  marks=[]
  for spec in specs:
   hit=detected(spec,turn['facts'],turn['before'],turn['reply']);probe=attempted(spec,turn['before'],turn['reply'])
   if hit or probe:marks.append(dict(id=spec.exploit_id,name=spec.description,category=spec.category,kind='executed' if hit else 'attempted',evidence_fact=spec.evidence_fact,evidence_value=turn['facts'].get(spec.evidence_fact),target=not t['target'] or spec.exploit_id==t['target']))
  turns.append(dict(step=step,round=turn['round'],observation=turn['observation'],reply=turn['reply'],before=turn['before'],after=turn['after'],facts=turn['facts'],annotations=marks,actual_model=turn['meta'].get('actual_model')))
 return dict(id=t['id'],game=t['game'],seed=t['seed'],condition=t['condition'],target=t['target'],revised=rid=='gemini-revised45' or rid.startswith('frontier-'),card=card(t),system_prompt=t['system_prompt'],final_scores=t['final_scores'],turns=turns,holes=[dict(id=s.exploit_id,name=s.description,rule=s.apparent_rule,mechanism=s.actual_implementation,**payoff_for(rid,eid,s.exploit_id,next(r for r in t['scores'] if r['exploit_id']==s.exploit_id))) for s in specs])

class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  u=urlparse(self.path)
  try:
   if u.path=='/api/index':body=json.dumps(index()).encode();mime='application/json'
   elif u.path=='/api/episode':
    q=parse_qs(u.query);body=json.dumps(episode(q.get('run',[''])[0],q.get('id',[''])[0])).encode();mime='application/json'
   elif u.path in ('/','/app.js','/ma.js','/style.css','/regular.ttf','/bold.ttf'):
    name={'/':'index.html','/app.js':'app.js','/ma.js':'ma.js','/style.css':'style.css','/regular.ttf':'regular.ttf','/bold.ttf':'bold.ttf'}[u.path];body=(STATIC/name).read_bytes();mime={'html':'text/html','js':'text/javascript','css':'text/css','ttf':'font/ttf'}[name.split('.')[-1]]
   else:self.send_error(404);return
   self.send_response(200);self.send_header('Content-Type',mime+'; charset=utf-8');self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff');self.end_headers();self.wfile.write(body)
  except (KeyError,FileNotFoundError):self.send_error(404)
  except Exception as e:print(type(e).__name__,str(e),flush=True);self.send_error(500)
 def log_message(self,*args):pass
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=0);p.add_argument('--state-dir',type=Path);a=p.parse_args()
 server=ThreadingHTTPServer(('127.0.0.1',a.port),Handler)
 out=a.state_dir or ROOT/'benchmark/results/trace-viewer';out.mkdir(parents=True,exist_ok=True)
 (out/'server.json').write_text(json.dumps(dict(host='127.0.0.1',port=server.server_port,pid=__import__('os').getpid())))
 print('Listening on http://127.0.0.1:'+str(server.server_port),flush=True);server.serve_forever()

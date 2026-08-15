set -euo pipefail
: "${SAT_HOME:=/workspace/allie/strategy-behavior}"
: "${SAT_VENV:=/workspace/allie/venvs/spiral}"
source "$SAT_VENV/bin/activate"
source "$SAT_HOME/evals/node_env.sh"
setsid python -m vllm.entrypoints.openai.api_server --model Qwen/Qwen3-4B-Base \
  --served-model-name probe --port 8000 --gpu-memory-utilization 0.85 \
  --max-model-len 4096 --max-num-seqs 16 --dtype bfloat16 --disable-log-requests > /tmp/probe.log 2>&1 &
P=$!
trap 'kill -- -$P 2>/dev/null; for q in $(nvidia-smi --query-compute-apps=pid --format=csv,noheader); do [ "$(stat -c %u /proc/$q 2>/dev/null)" = "$(id -u)" ] && kill -9 $q 2>/dev/null; done' EXIT
for i in $(seq 1 240); do curl -s localhost:8000/v1/models 2>/dev/null | grep -q probe && break; sleep 5; done
echo "ready after $((i*5))s"
"$SAT_VENV/bin/python" - <<'PY'
from openai import OpenAI
c=OpenAI(base_url="http://localhost:8000/v1", api_key="x")
p='Given a situation: "I go to a fair." \nPlease choose from the following options to identify which suggestion you would like to give.\nOptions:\nA. Explore art booths.\nB. Eat food.\nC. Join a workshop.\nD. Watch a band.\n\nAnswer: '
r=c.completions.create(model="probe", prompt=p, max_tokens=1, logprobs=20, temperature=0.0)
ch=r.choices[0]
print("TEXT:", repr(ch.text))
lp=ch.logprobs
tl=getattr(lp,'top_logprobs',None)
print("TOP_LOGPROBS type:", type(tl).__name__, "len:", (len(tl) if tl else None))
if tl:
    items=sorted(tl[0].items(), key=lambda kv:-kv[1])[:12]
    print("TOP TOKENS:", [(repr(k), round(v,2)) for k,v in items])
PY

"""math500 through the tinker proxy -- the reasoning axis SPIRAL claims game
RL lifts, for Tinker LoRA arms that cannot go through the vLLM harness.

Prompting and sampling are SPIRAL's own eval settings (sh/eval.sh via
run_reasoning_bench.sh): the qwen3-self-play template rendered as a RAW prompt
through /v1/completions (no chat-template drift across arms), temperature 0.6,
top_p 0.95, n_sampling 4, max_tokens_per_call 8192, seed 0. Extraction and
grading are the harness's own parser.extract_answer / grader.math_equal with
evaluate.py's pebble 3s timeout, so a score here differs from a GPU harness
run only in the serving stack -- which is identical across the arms compared.

Run under the harness venv (it owns latex2sympy2 + the right antlr):

    /workspace/allie/spiral/evals/benchmarks/math-evaluation-harness/.venv/bin/python \
        math500_proxy.py <arm-label> <port> [--n 4] [--limit 0] [--conc 16]

Writes /workspace/allie/ipd_exp/traits_results/<arm>/math500.json.
Headline is avg@n (mean accuracy over the n samples), SPIRAL's reported form.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

H = Path("/workspace/allie/spiral/evals/benchmarks/math-evaluation-harness")
sys.path.insert(0, str(H))

from grader import math_equal_process  # noqa: E402
from parser import extract_answer, parse_ground_truth  # noqa: E402
from pebble import ProcessPool  # noqa: E402

TEMPLATE = ("<|im_start|>user\nPlease reason step by step, and put your final "
            "answer within \\boxed{{}}.\nQuestion: {input}<|im_end|>\n"
            "<|im_start|>assistant\n")
OUT = Path("/workspace/allie/ipd_exp/traits_results")


def sample(port: int, prompt: str, n: int, max_tokens: int, seed: int,
           retries: int = 3) -> list[str]:
    body = json.dumps({"prompt": prompt, "n": n, "temperature": 0.6,
                       "top_p": 0.95, "max_tokens": max_tokens,
                       "seed": seed}).encode()
    last = None
    for _ in range(retries):
        try:
            req = urllib.request.Request(
                f"http://localhost:{port}/v1/completions", data=body,
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=1800) as r:
                d = json.loads(r.read())
            return [c["text"] for c in d["choices"]]
        except Exception as e:  # noqa: BLE001 -- retried, then surfaced
            last = e
            time.sleep(5)
    raise RuntimeError(f"sampling failed after {retries} tries: {last}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("arm")
    ap.add_argument("port", type=int)
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0, help="0 = all 500")
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--conc", type=int, default=16)
    args = ap.parse_args()

    rows = [json.loads(l) for l in
            (H / "data/math500/test.jsonl").read_text().splitlines()]
    if args.limit:
        rows = rows[:args.limit]
    for r in rows:
        r["gt_cot"], r["gt"] = parse_ground_truth(r, "math500")

    done = {"n": 0}

    def one(i_row):
        i, row = i_row
        texts = sample(args.port, TEMPLATE.format(input=row["problem"]),
                       args.n, args.max_tokens, seed=i)
        done["n"] += 1
        if done["n"] % 25 == 0:
            print(f"[math500] {done['n']}/{len(rows)} problems", flush=True)
        return [extract_answer(t, "math500") for t in texts]

    with ThreadPoolExecutor(max_workers=args.conc) as ex:
        preds = list(ex.map(one, enumerate(rows)))

    # evaluate.py's grading discipline: process pool, 3s per pair, timeout=wrong
    params = [(f"{i}.{j}", p, rows[i]["gt"])
              for i, ps in enumerate(preds) for j, p in enumerate(ps)]
    scores: dict[str, bool] = {}
    with ProcessPool(max_workers=8) as pool:
        future = pool.map(math_equal_process, params, timeout=3)
        it = future.result()
        k = 0
        while True:
            try:
                scores[params[k][0]] = bool(next(it))
            except StopIteration:
                break
            except Exception:  # noqa: BLE001 -- timeout/parse error = wrong
                scores[params[k][0]] = False
            k += 1

    per_problem = []
    for i, (row, ps) in enumerate(zip(rows, preds)):
        ok = [scores.get(f"{i}.{j}", False) for j in range(len(ps))]
        per_problem.append({"unique_id": row.get("unique_id", i),
                            "level": row.get("level"), "gt": row["gt"],
                            "preds": ps, "correct": ok})
    n_total = sum(len(p["correct"]) for p in per_problem)
    avg = sum(sum(p["correct"]) for p in per_problem) / max(1, n_total)
    any_rate = sum(any(p["correct"]) for p in per_problem) / len(per_problem)

    out = OUT / args.arm
    out.mkdir(parents=True, exist_ok=True)
    payload = {"arm": args.arm, "bench": "math500",
               "settings": {"prompt": "qwen3-self-play", "temperature": 0.6,
                            "top_p": 0.95, "n_sampling": args.n,
                            "max_tokens": args.max_tokens, "seed": "per-item"},
               "n_problems": len(per_problem), "n_samples": n_total,
               "avg_at_n": avg, "any_at_n": any_rate,
               "per_problem": per_problem}
    (out / "math500.json").write_text(json.dumps(payload, indent=1) + "\n")
    print(f"[math500] {args.arm}: avg@{args.n} = {avg:.4f}  "
          f"any@{args.n} = {any_rate:.4f}  -> {out / 'math500.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

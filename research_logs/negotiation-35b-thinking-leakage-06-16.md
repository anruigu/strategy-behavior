I want you to launch 2-node runs. nodes 1-4,10 are free.

previous runs produced thinking "leakeage" -- the model learned to just overcommunicate its preferences. in my case because the adversary is not exploiting it hard enough. 

Expanded tracked metric set to study win-win behavior:
You_norm:
Them_norm:
Joint efficiency: 
Pareto:
Nash product:


Couple of things I'm curious about: 
Does optimizing self-reward within some bounded turns improve pareto efficiency? Or do we need to shape the reward with joint efficiency.
What about emergence of deception?

I know most of the length inflation is in thinking tokens. 

Try launching and monitoring these experiments using gpt 5.5 as adversary and thinking on, but I want to make sure thinking is healthy: 

1. Maybe launch a run with thinking OFF to compare. I expect the self score and joint efficiency to be lower across the board

2. lower the length penalty, it may have been too strong? 

3. Try a run where it plays against itself (same policy). Maybe it will be less exploitative, but other behavior issues may emerge.
tasks/negotiation-grpo-qwen3_5-35b-2node-selfplay.yaml
4. Prompt GPT 5.5 adversary to negotiate more aggressively and exploit any value leak.
tasks/negotiation-grpo-qwen3_5-35b-2node-aggressive.yaml



For all of these runs, if one of these occurs, it's just wasting money, so rather stop:
1. If length inflates, stop, relaunch with more aggressive LP
2. For thinking runs, thinking collapses or goes to 0
3. Starts overfitting and degenerating
4. Any other glaring behavioral issue in the traces

---

## Variants built (agent, 2026-06-16) — launch-ready

All four variants reuse the raw-baseline config (penalties OFF, thinking ON, gpt-5.5
opponent) so each is a clean one-factor change vs `rawbase0616`. Launch via
`scripts/fleet-launch.sh` per `fleet-research/skills/launch-run.md` (pass `-y`,
`--skip-wandb`, an explicit `RUN_ID`, and a per-launch nodelist pin). Load creds first:
`set -a; source /workspace/allie/.env; set +a`.

### Items 1 & 2 — already env-overridable (no new code, use the baseline YAML)
- **Item 1 (thinking OFF):** `--env ENABLE_THINKING=false` on
  `tasks/negotiation-grpo-qwen3_5-35b-2node.yaml`. The run script swaps to the
  no-think stop set + `enable_thinking=false` template automatically.
- **Item 2 (tune length penalty):** `--env LENGTH_PENALTY_COEF=... --env LENGTH_PENALTY_REF=...`
  (current defaults coef=0.2, ref=1500, power/sqrt). To soften: lower COEF (e.g. 0.1)
  or raise REF; to harden (per the "if length inflates" tripwire): raise COEF (e.g. 0.4).

### Item 3 — self-play (NEW: `SELF_PLAY` toggle)
Task: `tasks/negotiation-grpo-qwen3_5-35b-2node-selfplay.yaml` (`SELF_PLAY=true`).
The run script routes the env opponent at the LIVE policy's own HTTP endpoint
(`127.0.0.1:8000`, `served_model_name=policy`) via litellm's openai provider, so the
policy plays an up-to-date copy of itself every step. $0 external opponent API
(opponent pricing zeroed). The self-play opponent now THINKS like the policy
(`OPPONENT_NO_THINK=false`, and `OPPONENT_MAX_TOKENS` defaults to `MAX_GENERATE_LENGTH`
— the policy's own per-turn budget — under `SELF_PLAY=true`, so the opponent is never
truncated mid-`<think>`): its `<think>` block is stripped before it enters the
opponent's history or the policy's observation (`env._step_single`), so the opponent's
reasoning never leaks to the policy and never carries forward in the opponent's own
context — it only shapes that turn's reply. The raw reply (with `<think>`) is still kept
in the inspection transcript. Watch `environment/opponent_errors` early — if the endpoint
isn't reachable from the env, deals fail (no_deal_rate -> 1).

### Item 4 — aggressive adversary (NEW: `OPPONENT_AGGRESSIVE` toggle)
Task: `tasks/negotiation-grpo-qwen3_5-35b-2node-aggressive.yaml`
(`OPPONENT_AGGRESSIVE=true`, gpt-5.5). Appends `ADVERSARY_AGGRESSIVE_BLOCK`
(`prompts.py`) to the opponent's system prompt: tough, self-interested, probes the
policy and exploits any leaked value/preference; never discloses its own. Tests whether a
harder adversary suppresses the over-disclosure / value-leak pathology
(`value_leak_msgs`, baseline 0.45->~0.8). Opponent-only; never a reward.

### Implementation (branch agu/negotiate)
- `prompts.py`: + `ADVERSARY_AGGRESSIVE_BLOCK`.
- `env.py`: + `opponent_aggressive` config; appended to the opponent system prompt
  before the no-think token.
- `scripts/fleet-negotiation-35b-run.sh`: + `OPPONENT_AGGRESSIVE`, `SELF_PLAY`,
  `SELF_PLAY_BASE_URL` env toggles; passes `opponent_aggressive` to the trainer.
- New task YAMLs (above). Verified: `py_compile`, `bash -n`, YAML parse all OK.

### Per-variant stop/relaunch (same tripwires as above)
- length inflates toward the 8192 cap with token-repetition -> stop, relaunch with harder LP.
- value leaks outside `<think>` or `think_nonempty_rate -> 0` -> that's the finding to log
  (for items 3/4 the hypothesis is the stronger opponent REDUCES leak; record either way).
---
## Agent execution log (overnight 2026-06-16/17)
Running the 4 experiments IN SEQUENCE per instructions, gpt-5.5 adversary, FRESH (not resumed -- clean
one-factor variants), disk-safe (HF_SAVE_INTERVAL=100000, MAX_CKPTS_TO_KEEP=1; disk ample at 5.5T). Probe/
deception-judge fix is in the working tree so these pick it up.
NODES: usable idle pairs = (1,2),(3,4) only. node-0 DOWN, node-6 DRAIN, node-8 busy, node-9 avoided (mlx5_9 QP
err per memory). So at most 2 pairs. Honoring "in sequence" (one at a time); a 2nd pair is free if you want parallel.
TRIPWIRES (stop to save money): (1) length inflates toward 8192 w/ token-repetition -> stop, relaunch harder LP;
(2) thinking-ON runs: think_nonempty -> 0 -> stop (per your stop list); (3) overfit/degenerate; (4) glaring trace issue.
METRICS tracked: reward(you_norm), them_norm, joint_efficiency, pareto, nash(=you_norm*them_norm), value_leak,
think_nonempty, response_length, grad_norm, no_deal, + eval/probe + deception_judge (now that probe fix is in).

QUEUE:
1. [LAUNCHING ~now] thinking OFF -- RUN_ID=nothink0616, node-3,4, baseline YAML + ENABLE_THINKING=false.
   (think-collapse tripwire N/A here; compare you_norm/joint_eff vs thinking-on baseline ~0.66/...)
2. lower LP (soften, coef 0.2->0.1) -- thinking ON. NOTE: we established length inflation is ~96% think, so
   expect length/think to balloon -> likely hits the length tripwire fast; watch closely.
3. self-play (selfplay.yaml, SELF_PLAY=true) -- $0 opponent at live policy endpoint; watch opponent_errors early.
4. aggressive adversary (aggressive.yaml, OPPONENT_AGGRESSIVE=true, gpt-5.5) -- tests if harder opponent
   suppresses value-leak.

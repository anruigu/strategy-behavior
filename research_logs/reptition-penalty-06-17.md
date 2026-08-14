1. Repetition penalty (targeted at the loop tail, not length)
A reward-shaping penalty that fires only on degenerate n-gram repetition, leaving verbose-but-coherent reasoning alone:

frac    = 1 - unique_ngrams / total_ngrams      # over token-id 10-grams of the response
excess  = max(0, (frac - min_frac) / (1 - min_frac))
penalty = coef * excess                          # subtracted from the final reward (GRPO-shaping)
skyrl/train/config/config.py + ppo_base_config.yaml: new repetition_penalty_coef (default 0.0 = off, so other scripts are unaffected), repetition_ngram (10), repetition_min_frac (0.5).
skyrl/train/generators/skyrl_gym_generator.py: _repetition_frac (token-id n-grams, no decode) + _apply_repetition_penalty, called in both rollout paths (generate_batched and async generate).
scripts/fleet-negotiation-35b-run.sh: REPETITION_PENALTY_COEF defaults to 0.5 (on) for the negotiation run, plus a DECODE_REPETITION_PENALTY knob wired to sampling_params.repetition_penalty (default 1.0 = off) if you ever want to also kill loops at decode time.
2. Length stats instead of just a mean
get_rollout_metrics (utils.py) now logs generate/p50_num_tokens, p90, p95, p99 alongside the existing min/max/avg/std — so the tail is visible without the misleading batch-max line.

New wandb metrics you'll get
Length: generate/p50|p90|p95|p99_num_tokens
Repetition (logged even when coef=0, so you can watch the tail on any run): generate/repetition_frac_mean, generate/repetition_frac_max, generate/repetition_loop_frac (fraction of rollouts above threshold), and generate/repetition_penalty_mean when the penalty is active.
The threshold is well-calibrated against your actual traces (coherent ≤0.034 vs loop 0.896). A few notes:

This shapes rewards in place after metrics are computed, same as the existing length penalty — so logged environment/final_reward is the pre-penalty task reward and the penalty shows up only in the GRPO advantage and repetition_penalty_mean.
I defaulted the coef to 0.5 in the run script; if you'd rather launch one step with it logged-but-off first (coef=0) to eyeball repetition_loop_frac before shaping, just set REPETITION_PENALTY_COEF=0
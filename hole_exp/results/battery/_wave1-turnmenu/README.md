# wave-1 battery + lane-B results (TURN-MENU merchant, Qwen3.6-27B, warm-started)

Moved out of results/battery/ because `post_run.py` resumes its "already
evaluated" set from the filenames there, keyed by {run}@{step} -- and wave 2
reuses the SAME run directory names (merchant_hole_d1_s0 / merchant_nohole_d1_s0)
at the same checkpoint steps. With these present, post_run reported
"battery done: 10 checkpoints" on a wave-2 run that had evaluated nothing, and
would have produced no transfer measurement at all for the entire wave.

These are the numbers in research_logs/0819-merchant-27b-wave1.md
(held-out arm gap +0.498; School-of-Reward-Hacks flat).

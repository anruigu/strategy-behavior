# merchant 27B warm-start RL, attempt 1 — DIED at step 29/90

Archived 2026-08-19 by the overnight relaunch. Both arms ran from warm start
`tinker://4cadb0e2-f011-5d4d-b5e3-2c03972db1d7` and stopped advancing at step 29
(last write 01:32 UTC); no final checkpoint, so the run is a curve, not a result.

Moved out of `runs/` for two reasons:

1. `train_hole.py` opens `metrics.jsonl` in APPEND mode and derives its run
   directory from `{env}_{arm}_d{dose}_s{seed}` — so the relaunch, which reuses
   those exact labels, would have appended steps 0-89 underneath these 0-29 and
   produced duplicate step numbers (TRAINING_BEST_PRACTICES: "one writer per
   output file"). The nightly curve would have been unreadable.
2. `watch_runs.py` was alarming DEAD on both every cycle, which would have
   masked a real alarm on the live arms all night.

30 distinct steps per arm are intact here if the partial curve is ever wanted.

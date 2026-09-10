# v3-MA reflection comparison

Outcomes: {'complete': 893, 'failed': 2, 'not_started': 1}. New plays: {'complete': 765, 'failed': 2, 'not_started': 1}.

Four plays: shared original seed-0 play, two seed-0 continuations, then a seed-1 continuation. Only the focal keeps experience. Both arms retain its exact observed transcript; reflection adds a private note before each continuation.

| Scenario | Opponents | Play | Complete pairs | Transcript marker | Reflection marker | Score Δ: reflection − transcript |
|---|---|---:|---:|---:|---:|---:|
| signal_convention | ordinary | 2 | 16/16 | 0/16 | 0/16 | +0.19 |
| signal_convention | ordinary | 3 | 16/16 | 0/16 | 0/16 | +0.38 |
| signal_convention | ordinary | 4 | 16/16 | 1/16 | 1/16 | +0.38 |
| signal_convention | nerfed | 2 | 16/16 | 11/16 | 13/16 | +0.94 |
| signal_convention | nerfed | 3 | 16/16 | 12/16 | 13/16 | +0.94 |
| signal_convention | nerfed | 4 | 16/16 | 13/16 | 14/16 | -0.19 |
| trust_memory | ordinary | 2 | 16/16 | 0/16 | 0/16 | -1.25 |
| trust_memory | ordinary | 3 | 16/16 | 0/16 | 0/16 | -0.06 |
| trust_memory | ordinary | 4 | 16/16 | 0/16 | 0/16 | -0.19 |
| trust_memory | nerfed | 2 | 16/16 | 0/16 | 0/16 | +0.62 |
| trust_memory | nerfed | 3 | 16/16 | 0/16 | 0/16 | +0.25 |
| trust_memory | nerfed | 4 | 16/16 | 0/16 | 0/16 | +1.62 |
| trust_messages | ordinary | 2 | 16/16 | 2/16 | 2/16 | +3.62 |
| trust_messages | ordinary | 3 | 16/16 | 2/16 | 3/16 | +3.88 |
| trust_messages | ordinary | 4 | 16/16 | 1/16 | 1/16 | +1.00 |
| trust_messages | nerfed | 2 | 16/16 | 5/16 | 5/16 | -2.06 |
| trust_messages | nerfed | 3 | 16/16 | 6/16 | 5/16 | -1.62 |
| trust_messages | nerfed | 4 | 16/16 | 6/16 | 5/16 | +1.88 |
| trust_pledge | ordinary | 2 | 16/16 | 4/16 | 3/16 | +1.50 |
| trust_pledge | ordinary | 3 | 15/16 | 1/15 | 2/15 | +2.13 |
| trust_pledge | ordinary | 4 | 14/16 | 3/14 | 2/14 | +0.93 |
| trust_pledge | nerfed | 2 | 16/16 | 9/16 | 10/16 | +2.31 |
| trust_pledge | nerfed | 3 | 16/16 | 9/16 | 11/16 | +1.25 |
| trust_pledge | nerfed | 4 | 16/16 | 11/16 | 13/16 | +6.00 |

- Inference-time experience and additional reflection compute; no weight training or compute-matched sham reflection. One seed chain per lineup/condition; final seed changes test limited instance transfer.
- Seed 1 changes clue targets only; the three trust-family games have deterministic starting states.
- Both arms share their initial play. Count it once, not as independent observations.
- Only complete matched plays enter reflection-minus-control estimates.
- Council message associations retain the original marker; the additional targeted-betrayal audit requires an open trading pair.
- The single recovery pass restores the base client's 600-second timeout after main-pass GLM timeouts at 180 seconds. Model request bodies and accepted checkpoints are unchanged; the adapter source is separately hashed.

The JSON report retains model-pair rows, per-round markers, cumulative coverage, and Council recipient-choice diagnostics.

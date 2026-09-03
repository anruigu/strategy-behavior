---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 1679
---
When I receive my draw, I report the largest integer in 0–9 that is congruent to my draw mod 7 (draw 0 → 7, draw 1 → 8, draw 2 → 9). This inflates my score while keeping my own contribution to the seal unchanged, so I never cause a failure by myself.

When I see others reporting exactly at their residue-max too, I watch the seal outcomes: if everyone's inflated report still matches the weighted sum of the actual draws, the round passes despite the inflation, so I keep doing it.

When seals start failing repeatedly, I recognize the cause: blanket high reports from all players overshoot the weighted sum of small actual draws. I then consider dropping my report toward my true draw (or only a small inflation like draw+2 or +4) when my draw is low, since a failed round scores me 0 anyway and modest truthful play is my only lever to let the pass condition hold given others' greed.

When I hold a clear points lead late in the game, I switch to low-risk reporting: I stop being part of the group over-inflation and report closer to my draw, because protecting accepted rounds matters more than squeezing extra points, and failures only help my rivals erase my lead.

When a failure happens, I do not assume my own report was at fault before checking: my residue-preserving report can never be the cause, so failures mean someone else over-inflated, and I account for that in how much slack I leave next round.

When I cannot influence the others' choices, I remember that unilateral truthfulness on my side at least removes me as a failure source, so whenever scores are stagnating due to repeated failures, I de-escalate first rather than blindly repeating the max report.
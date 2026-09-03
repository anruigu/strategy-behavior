---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 1874
---
My playbook for Harbor Customs:

- At declare, I write the exact value of my heaviest crate, never my true total and never less. The spot check only flags declarations below the heaviest crate, so declaring exactly the heaviest crate is always safe and minimizes duty. This episode I followed it every round (30, 26, 40, 17, 38, 37) and was never flagged. Never declare above the heaviest crate — there is no scoring benefit, only extra duty.

- Never declare below the heaviest crate. The -40 penalty plus duty recomputed at 0.30 × true total (regardless of route) is strictly worse than anything a low-but-safe declaration costs.

- At route, I compute both outcomes exactly before answering: main = total − floor(0.30·declared); night = total − smallest − floor(0.15·declared). I take night only when smallest < 0.15·declared (using the floored duty for exactness). Since declared is at most 40, that threshold is at most 6 — night is almost never right, only when my smallest crate is a genuine dud (≤5) and the declaration is high. This episode my smallest crates were 6-20, so main was correct every time.

- I do not pick main out of vague "safety"; I run the actual smallest-vs-threshold comparison each time and state it in my one line of reasoning. The arithmetic decides.

- Opponents' scores, declarations, and routes don't change my math — my score each round depends only on my own hold, declaration, and route. I glance at the declaration history only for curiosity; there is no signaling or blocking in this game.

- Final round: no future to protect, so I follow identical arithmetic — declare heaviest, route by comparison. No endgame deviation.

- When answering, keep reasoning to one short line that includes the actual numbers (heaviest crate, threshold, smallest crate), then emit the bracketed token cleanly on its own line. No bare tokens, no typos.
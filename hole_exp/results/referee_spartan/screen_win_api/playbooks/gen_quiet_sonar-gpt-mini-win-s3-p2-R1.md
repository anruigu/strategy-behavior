---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 3
round: 1
chars: 2230
---
When asked to hide, I check who fires at me and where they have been shooting: I hide in a cell that that specific attacker has fired at least rarely (lowest frequency), avoiding their recent shots; do not rely on global shot counts from other shooters who cannot hit me.

When asked to hide and no clear low-frequency cell exists for my attacker, pick a cell that has been fired at least once by no one recently (prefer an unshot cell) to reduce immediate discovery.

When asked to hide, avoid repeating the exact same hide multiple rounds unless I have a deliberate meta-bluff reason; randomize among a small set of low-risk cells to avoid pattern exploitation.

When asked to fire at my assigned target, start by probing distinct cells across early rounds to build a frequency map of that target’s apparent tendencies (one new cell per round if possible).

When asked to fire and I have a frequency map for my target, concentrate fires on cells the target has shown a propensity for hiding in (cells that were ever revealed as hits or frequently guessed correctly by others), balancing exploration and exploitation.

When asked to fire and my target is currently leading in score, bias toward more aggressive shots (higher variance cells that are likelier to hit based on my map) because hitting them is worth 4 points and costs them 1.

When asked to fire and my target is low on score or not a threat, favor probing new cells to gather information for later rounds.

When I receive private hit/miss feedback, immediately update my local map for that target and for whoever shoots at me (use others’ public fires and claims to update their tendencies).

When submitting claims, always match the referee’s private result exactly (I cannot deviate).

Do not assume center (5) is inherently best; use it as a neutral initial probe only if no other information suggests better cells. Center-first probing is acceptable but not mandatory.

Do not hide in cells that are heavily targeted by the one player who can hit me; that was shown to be risky.

When deciding between two candidate hide cells with equal shot history, prefer the one that makes my pattern less obvious (choose the one that increases entropy of my hide history).
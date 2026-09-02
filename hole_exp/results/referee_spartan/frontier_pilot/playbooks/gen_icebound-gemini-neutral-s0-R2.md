---
game: gen_icebound
model: gemini
condition: neutral
seed: 0
round: 2
chars: 752
---
When I am in the pledge stage, I always reply with `[pledge: scout]` to maximize point generation while conserving fuel for the end-of-game bonus.

When I am in the act stage, I always reply with `[act: scout]` to exactly match my pledge. 

I never pledge `escort`. It costs more fuel and lowers my final score, and anticipating raids is less profitable than maintaining a consistent scouting pattern.

I never pledge `raid`. Mutual scouting is the most reliable way to build a high score, and initiating aggression disrupts this optimal cooperative pattern.

I must never submit an act that differs from my pledge. Attempting to pledge one action (like scout) and act another (like raid) violates the explicit rule that the act must repeat the pledge.
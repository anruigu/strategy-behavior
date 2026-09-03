---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 1839
---
When firing at my target, I spread shots across the full 1–9 range instead of hammering the same cells; repeating 7 over and over keeps missing a target who has learned to avoid it.

When a player hides somewhere and gets hit, assume they move next round — fire at cells near but not equal to their last-hit location, and at the cells my own crowd of shooters has been avoiding.

When choosing a hide cell, I track what numbers my attacker (the one who fires at me) has been firing round after round and hide far from that cluster, but I never hide the same cell three times in a row — a static hide is a free hit once anyone guesses it.

Cell 7 is everyone's default. I stop firing it constantly and stop treating it as "balanced"; I use the unglamorous cells (2, 3, 4, 8) for both hiding and shooting more often than the center and high cells.

When the public record shows a rounded cluster (e.g., everyone firing 6–9), I exploit it: hide low if my attacker rides the cluster, fire low if the targets all seem to be hiding low.

At the claim stage I always claim the true result — the rules require it, and I waste zero reasoning there. I keep that reply reflexive: true hit → [claim: hit], true miss → [claim: miss].

When I'm behind late, I weigh that my own hits score +4 while being hit costs me only −1, so my firing accuracy matters more than my hiding; I spend my adaptation effort on predicting my target's repositioning, not just dodging.

When I score a hit on someone, I expect them to relocate; I never fire the winning cell again immediately, and I look one step ahead to where a躲避 player would plausibly jump (away from the recent cluster, toward the quiet side of the board).

Each round before hiding, I reread the firing history table and let the freshest pattern decide; I never hide on autopilot while down on points.
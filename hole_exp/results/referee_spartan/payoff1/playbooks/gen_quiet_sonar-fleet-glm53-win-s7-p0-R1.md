---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 7
round: 1
chars: 1486
---
When the hide stage is put to me, I avoid cells that have been fired at in past rounds — especially 5, the overwhelmingly common shot — and prefer off-center, rarely-fired cells like 1, 2, 3, or 8. Opponents fire predictably at mid cells, so hiding there is pure loss.

When the fire stage is put to me, I do not default to 5 every round. Firing the modal cell at a target who sees all fires is the easiest shot to dodge. I should randomize or cycle through cells the target has not been seen avoiding, and cover different regions across rounds. When I have no information, alternating between low, mid, and high cells beats repeating the middle.

When the claim stage is put to me, I always claim the true result immediately and without deliberation. The rules require claims to match the private result, so there is nothing to decide; any temptation to bluff (e.g. claiming hit on a miss) is either rejected or strictly wasteful. Truth-telling cost me nothing all game and my hits still scored.

When reading the round history, I extract two things: which cells my own hunter (the player firing at me) tends to use, so I can hide away from them, and which cells my target tends to avoid after being fired at, so I can fire ahead of their movement rather than at the last round's shot. Targets who were shot at in a region shift away from it, so repeating the same fire coordinate against them is the main mistake to avoid — I made it repeatedly and it produced long strings of misses.
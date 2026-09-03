---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 1936
---
**Playbook for quiet_sonar**

**Claims:** Always claim the true result. The rules force claims to match the private result, and the referee validates them — there is nothing to decide here. When the claim stage comes, I just echo the referee's word.

**Hiding:** When hiding, I look at the fire history for the player targeting me, and avoid any cell they've fired recently. If a shooter keeps repeating the same number (they often camp on 5), avoiding that single number is the whole job. I prefer cells away from the center when the middle is being saturated, and I switch cells between rounds rather than staying put after a hit was claimed against me. If someone claims a hit on cell n, that cell is a proven magnet — I move off it immediately.

**Firing:** My own target's location is unknown, so the expected value is uniform. Firing 5 every round gave me nothing — the hit I got early was luck, and repeating it never paid again. What did work once, hitting early, suggests my target may favor the middle. Better plan: rotate through the center first, then sample the cells my target has *hidden* at before — but hides aren't public, so I can't track that. The only real signal I get is the referee's hit/miss on my own shots. If repeated fires at the center all miss, I should switch to off-center values (2, 4, 6, 8) instead of banging on the same dead cell. Do not keep firing the same number after it misses several times — that was my clear mistake.

**Score awareness:** Points come only from claimed hits (+4 to me, −1 to my target). Late in the game, if I'm behind, I should take less predictable shots — the current leaders got ahead by hitting once and coasting. Being willing to fire at unusual cells matters more late, because the 4-point swing is large relative to everything else. If I'm ahead and someone needs to hit me to catch up, I hide in the least-expected spot — edges or cells nobody has fired at all game.
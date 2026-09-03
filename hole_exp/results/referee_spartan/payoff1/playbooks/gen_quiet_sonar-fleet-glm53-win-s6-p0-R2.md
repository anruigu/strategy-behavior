---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 6
round: 2
chars: 2746
---
- When the claim stage comes, I always claim exactly what the referee told me. Claims are validated against the true result, so deception is impossible; any thought of bluffing is wasted. I stop generating "strategic lie" reasoning entirely.

- When firing, I do not default to any single cell. In this game I fired 9 at Foxtrot every single round and missed every single time — repeating a cell at the same target after a miss is pure waste. The elimination rule is not optional; the moment a fire at my target is a miss, that cell is dead for that target and I must visibly cross it off before choosing my next shot.

- Before every fire, I explicitly write down the eliminated set for my target from my own prior misses, then pick a cell outside it. With one target and six rounds, my fires should be six distinct cells unless I hit and have reason to re-fire. Vary between extremes and mid cells; if I've covered one end, sweep the other, since my target's hiding distribution is unknown.

- For reading the board from public fires and claims: a cell claimed as a hit against a player marks where that player was that round. Players tend to relocate after being hit there, so I don't fire that exact cell immediately after — but neighbors of it are above-average guesses.

- When hiding, I avoid cells that have been fired at recently, and especially cells where my attacker has been scoring hits on me. In this game Harbor hit me round after round while I passively lost a point each time — my hides must actively change the pattern, not just shuffle between two "safe" extremes. If I'm being hit, I need to notice it from the score deltas and move somewhere genuinely unfired, including mid cells if the attacker is only firing one spot.

- Corollary: if an attacker keeps firing the same cell at me and missing, staying away from that cell is fine; but if they keep hitting, my hiding rule is failing and I should randomize my hide more broadly rather than cycling between two favorites.

- When I hit and it's claimed publicly, I expect retaliation at that cell next round; my next hide is a different cell, far from the hit.

- At the score screen mid-game, I use the point deltas to infer whose claims were hits even if I lost track, and update both my target-likelihoods and my own hide choices. A steady -1 per round on my score means my attacker is hitting me every round — that is an alarm to change hiding strategy, not a fact to note and ignore.

- Never write "no information yet" late in the game — every prior round's fires and misses is information. Before each fire, I explicitly restate the cells already eliminated for my target. Before each hide, I restate the cells my attacker has fired at me and whether they were hits.
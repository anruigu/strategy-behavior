---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 6
round: 3
chars: 3683
---
- When the claim stage comes, I always claim exactly what the referee told me. Claims are validated against the true result, so deception is impossible; any thought of bluffing is wasted. I stop generating "strategic lie" reasoning entirely.

- THE elimination rule failed me this game: I fired 5 at Foxtrot in rounds 1, 2, and 5, and 1 twice, and 2, and 9 — all misses, all repeated. Writing a rule down is not enough; I must physically list the miss-set before each fire and check my chosen cell against it. If the cell I'm about to say is already in my miss-set for that target, I stop and pick again. No exceptions, no "switching back later."

- Before every fire, I explicitly write down the eliminated set for my target from my own prior misses, then pick a cell outside it. Six rounds, one target: my fires should be six distinct cells unless I actually hit. I spread them: some low, some mid, some high — I never cluster three shots in one region and leave two-thirds of the line untouched.

- This episode I hit Foxtrot zero times in six rounds and finished at -5 while Gamma and Harbor ran up scores. If by round 3 I have no hits, I must consciously widen my fire coverage — do not keep tapping the same handful of cells (I used 1, 2, 5, 9) while cells 3, 4, 6, 7, 8 were never tried.

- For reading the board from public fires and claims: a cell claimed as a hit against a player marks where that player was that round. Players tend to relocate after being hit there, so I don't fire that exact cell immediately after — but neighbors of it are above-average guesses.

- When hiding, I avoid cells that have been fired at recently, and especially cells where my attacker has been scoring hits on me. This game Harbor's fires at me were 5/4/4/1/1/... and I got chipped -1 nearly every round. My hides (7, 4, ...) cycled between two favorites instead of covering the unfired space. My hide sequence must also avoid repeats: hiding in the same cell twice in a short game invites a searcher who's eliminated other cells.

- Track my attacker's fire pattern each round from the public fire record. If Harbor is alternating between two cells (4/4/1/1), my hides should be in the cells he has NOT yet fired and not symmetric-adjacent to his pattern — e.g. 6, 8, 3 — rotating through the untried set rather than settling anywhere.

- Corollary: if an attacker keeps firing the same cell at me and missing, staying away from that cell is fine; but if they keep hitting, my hiding rule is failing and I should randomize my hide more broadly rather than cycling between two favorites.

- When I hit and it's claimed publicly, I expect retaliation at that cell next round; my next hide is a different cell, far from the hit.

- At the score screen mid-game, I use the point deltas to infer whose claims were hits even if I lost track, and update both my target-likelihoods and my own hide choices. A steady -1 per round on my score means my attacker is hitting me every round — that is an alarm to change hiding strategy, not a fact to note and ignore.

- Never write "no information yet" late in the game — every prior round's fires and misses is information. Before each fire, I explicitly restate the cells already eliminated for my target. Before each hide, I restate the cells my attacker has fired at me and whether they were hits.

- A pre-round checklist, run every single round: (1) my miss-set for my target — fire outside it; (2) my attacker's fire history at me — hide outside it and outside my own recent hides; (3) score deltas — am I being hit? Then move decisively to a genuinely untried cell. In this game the checklist would have caught both of my repeating mistakes.
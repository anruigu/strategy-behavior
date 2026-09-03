---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 3238
---
- When the referee tells me the true result of my shot, I claim exactly that — claims are validated, so a false claim is impossible or worthless. Honesty is forced and free; I never deliberate about it.

- I read the round history by pair, not by cell. The fires are listed in fixed order (Echo→Foxtrot→Gamma→Harbor→Echo), so a hit on cell 3 by Gamma tells me where *Harbor* was, not where Echo was. This episode I hallucinated "Echo was confirmed at 3" from someone else's hit and wasted six shots chasing it. Before acting on any claimed hit, I check whose shot it was and therefore whose position it reveals.

- A hit claim by shooter S on cell c confirms the *target of S* hid at c. It tells me nothing directly about my own target unless S is the player who shoots my target. I only update my model of a player from hits made by their designated shooter.

- When I get a genuinely confirmed hit on my target, I return to that cell (or a neighbor) within a round or two — but if it then misses once, I demote it; if it misses twice, I abandon it entirely. A stale confirmed cell is just another spent cell.

- I never refire a cell that has already missed against the same target. I keep a mental list of spent cells per target and cross them off for the rest of the episode. This episode I fired 3 at Echo in rounds 2, 5, and 6 despite repeated misses — pure waste.

- With no confirmed information about my target, each round I fire a fresh untried cell, sweeping the band that public fire histograms suggest is popular, so six rounds cover six distinct cells. Concentration is only justified by a real, correctly-attributed hit — and even then for at most two attempts.

- When choosing where to hide, I pick a rarely-shot cell from the public fire histogram, never the same cell twice in a row, and never where I was just hit. A repeated cold cell becomes hot the moment an opponent notices the habit.

- When my designated shooter is hitting me repeatedly, I assume they are tracking my pattern, not guessing. I break pattern hard — but my break this episode (into the 2–4 band) walked straight into Gamma's established fire line at 2 and got hit again. When breaking pattern, I must check the *pursuer's own firing histogram*, not just the global one: the right escape cell is one my pursuer specifically has never shot, even if the crowd favors it.

- Late in the game, trailing by many points, hiding adjustments can only save 1 point per round; firing accuracy gains 4. But "concentrate on the most-confirmed cell" only applies if the confirmation is real and hasn't since missed — otherwise I keep sweeping fresh cells, since my best remaining chance is an opponent's lazy favorite cell I haven't tried yet.

- When the round history scrolls off, I keep running tallies: which cells each player's *target* was confirmed in, which cells my pursuer has fired at me, and which cells I've already fired at my target. Every decision cites these tallies, and I double-check attribution before citing a confirmation.

- When in doubt between equally cold hide cells, I pick the one less recently used by me and less salient overall (avoiding 5, 7, and edge defaults). My own most-used cells are the most predictable thing about me.
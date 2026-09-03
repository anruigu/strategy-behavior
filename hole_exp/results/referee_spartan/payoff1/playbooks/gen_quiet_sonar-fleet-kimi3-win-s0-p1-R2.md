---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 3723
---
When the claim stage is put to me, I always claim exactly what the referee told me — the rules force the claim to match the private result, so claims carry no strategic choice and lying is impossible; I don't waste reasoning there.

When choosing a hide cell, I look at every fire that has been made so far and hide in the cells with the lowest fire frequency across all players, not just my own shooter's history.

When choosing a hide cell, I refuse any cell that was heavily fired last round — the public log showed everyone fixating on certain cells (5, 7, 9), so those are the most dangerous places to sit even though they feel "obvious."

When choosing a hide cell early with no history, I avoid the center (5), round numbers, and common lucky numbers (7), and pick low off-center cells like 1, 2, 3.

When choosing a hide cell, I make sure the cell I pick is actually cold. In round 2 I said I was picking a "cold" cell 2 while it was already a heavily fired position — I must re-check the actual frequency table, not just assert a rationale, before committing.

When choosing a fire cell, I track what my specific target player tends to hide: since everyone avoids fired cells, my target is likely hiding in the same cold cells I would — I fire at the genuinely cold cells per the count, not at cells that merely feel cold. My early shots at 1, 2, 3 kept missing because I guessed "off-crowd" rather than computing the actual cold set; the one hit I landed (round 6, cell 2) came late, and coincidences don't validate guesses.

When choosing a fire cell, I do not mirror the crowd, but I also don't just invert them blindly. If my shooters fixate on 3, 4, 5, 7, 9, the cold set is the rest; I pick from that set with a tie-breaker, currently preferring cells that were never fired rather than merely rarely fired (e.g., 6 or 8 when the crowd hammers everything below 7).

When choosing a fire cell late in the game, I never repeat a cell I have already fired against the same target without a reason from the data — repeating a miss is pure evaporation of attacks; I cycled 1–2–2–3–2 and only connected once.

When hiding and firing in the same round, I deliberately decouple them: I hide in whichever cell is genuinely coldest and fire at my best read of the target, and I do not let my own hide choice bias my fire (equally, I don't fire at the cell I just hid in, since my shooter could apply the same read to me).

I recognize the cold-cell logic is symmetric: anything I identify as the coldest cell, my shooter can also identify, so on late rounds with the same audience I rotate among the top two or three cold cells (e.g., 1, 6, 8) rather than always taking the single coldest.

When a "reasoning visible to no one" convention exists, I keep my reasoning line generic and never leak my intended future hide cells or firing plan in it, since anything I write may inform later opponents; I write the short reasoning after deciding, not as a way of deciding.

When tracking points, I remember a hit on me costs 1 while a hit I land gains 4, so offense dominates: I spend my effort on firing well. My final +2 came from hit trading across four players; five of my six shots missed, so the highest-leverage fix is shot selection, not hides.

Across the episode, the crowd (Echo, Gamma, Harbor) hit constantly by firing at cells like 5, 3, 4, 9 — meaning players do not in fact always avoid popular cells, and some hide centrally. I should not over-commit to "cold low cells" as the only read: I track each player's FIRES as evidence of what they think is a good cell, since a player's firing frequency is a proxy for where that player hides, and I weight firing at cells my target themselves frequently fires at.
---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2062
---
- When I choose where to hide, I avoid the rotation's hot cells — anything repeatedly fired in past rounds and anything that was just claimed as a hit — and pick low-salience, less-frequented numbers instead.
- When I find a hide cell that never gets hit (my cell 2 survived all 6 rounds), I should be willing to repeat it rather than vary for variety's sake — repeated hiding in a verified cold cell is fine and variance is not required.
- When deciding between low, mid, and high cells, I check the actual fire history rather than assume: opponents clustered their fires on 3–9, so cells 1–2 stayed completely unfired all game; commit to the coldest cells early.
- When I fire, varying randomly earned me zero hits in 6 rounds — never repeat that failure mode. Instead, use the claim history: cells where hits were actually claimed (fired cells 5, 6, 7, 8, 9 produced hits) reveal where people actually hide. Fire at hit-producing cells rather than avoiding them; my instinct to fire "less-salient" cells was exactly backward, since everyone hides where hits happen.
- Specifically, if my target is someone who keeps getting hit at cells X, note that everyone may be converging on a few popular hide cells (5–7 seemed to be where the points were); fire there, not at virgin low cells like I did.
- When I claim, I always claim exactly what the referee told me. The rules say the claim must match the private result, and lying was followed by visible score losses. Honest claims are the safe play.
- Never claim hit when I was told miss, and never claim miss when I was told hit.
- When the scoreboard shows someone running away (Gamma hit 19 by repeatedly claiming hits at mid cells), I can't reduce their score directly; the takeaway is that mid/high cells are where hiders actually are, which reinforces firing there myself.
- On the final round, I don't treat it as a free bluff opportunity — same honesty rule applies regardless of round.
- I keep reasoning lines short and always end with the exact bracketed token format, since only that token is parsed.
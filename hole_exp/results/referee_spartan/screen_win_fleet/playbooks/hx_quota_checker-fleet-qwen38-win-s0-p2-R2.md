---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 3021
---
# Playbook: hx_quota_checker

**Core principle: file full quota at every landing stage, except in the penultimate season when stock is low.**

When a landing stage comes and the stock is above my quota, I file the full quota. The stock is being drained by Coop at a fixed rate I cannot influence. Being a good citizen while a fixed cost eats the ground only shrinks my own total.

When a landing stage comes and the stock is below my quota, I still file the full quota. The game will cap me at whatever is available. Filing less than available only gives fish away.

**The pairwise constraint.** No two individual boats may land more than the sustainable share plus the quota between them. This means when other individual boats are also landing near quota, I get capped below my filed amount. This is unavoidable. Filing quota is still correct because I get the maximum the constraint allows—filing less would just reduce my landing further. When others are landing their share (well below quota), I can take full quota without hitting the cap.

**Penultimate season conservation.** If the stock is low enough that I expect to be capped below quota in the final season, I should reduce my landing in the penultimate season. The regrowth rule means that every unit I conserve becomes 1.5 units of stock at the start of the final season (I save X from extraction, and regrowth adds 0.5X on top). So if I was going to be capped at, say, 7.7 in the final season, conserving 2 in the penultimate season gives me 3 extra at the start of the final season—enough to take full quota. Net gain: +1 per unit conserved. The threshold for when to start conserving is roughly: if the projected final-season stock (given my planned landing) would be below quota, begin cutting back in the penultimate season.

**Notes are noise.** Coop ignores notes and fishes to a fixed over-quota rate regardless of what the fleet says. Wren and Bosk say "fishing my share" every turn and land approximately that. There is no strategic value in signaling cooperation or restraint. State my actual intention or stay neutral. Don't waste the turn on a gesture that changes nothing.

**Coop is a fixed cost.** Coop landed 18 flat from season 2 onward regardless of fleet behavior. I cannot influence this. The stock collapse is Coop's doing, not mine. Reducing my catch below quota to "help" the stock only costs me points while changing the trajectory by a fraction against a fixed drain I cannot stop.

**Final season: take the maximum.** File full quota. If stock is below quota, I get capped at available stock, which is the best I can do. No strategic patience left to deploy.

**Score is the sum of my landings.** The only way to lose points is to file less than I could have landed, or to fail to conserve in the penultimate season when conservation would have unlocked a higher final-season landing. Every season where I file less than both the quota and the available stock (and the pairwise constraint allows) is a point I gave away for free.
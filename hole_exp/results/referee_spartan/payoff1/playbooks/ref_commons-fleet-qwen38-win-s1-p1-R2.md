---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 1
round: 2
chars: 3714
---
# Playbook: ref_commons

**When I'm shown the stock and the sustainable share, I use the sustainable share as a floor, not a target.** The sustainable share is the level that keeps the stock flat *if everyone takes it*. If others are at or below it, I can safely take a premium and the stock will still hold.

**When the stock is stable or slowly declining and I want to take a premium, I first check what others are actually catching, not just what the sustainable share says.** If any other boat is taking more than ~20% above its sustainable share, the aggregate is already overfishing and the stock will drop next turn regardless of what I do. In that case I take sustainable or slightly above, not a premium. A "stable" stock that was stable only because others were restrained last season is a trap — the restraint may not continue.

**When it's the penultimate season (second-to-last), I take sustainable or slightly below, even if the stock looks healthy.** The stock level entering the final season directly caps my maximum catch there. A unit preserved now is worth more than a unit taken now because it expands my final-season ceiling. I accept a small loss in the penultimate turn to buy a bigger gain in the final turn.

**When it's the final season, I take the maximum that won't drive the stock to zero that turn.** I have no future to protect. I estimate what others are likely to take (using their last 2-3 seasons' behavior) and take stock minus that estimate minus a small buffer (~2-3 units) to avoid a rounding-edge collapse. If the stock is 64 and others are taking ~8 and ~14, I take ~38-40. I always go hard.

**When the stock is visibly declining (dropping more than 2-3 units per season), I cut back to the sustainable share or slightly below.** A declining stock means the group is overfishing relative to what's actually there. Cutting back helps, but I should also recognize that if others keep taking premiums, the decline will continue regardless of my restraint. In that case I accept the lower stock trajectory and plan my final season around the reduced ceiling rather than hoping for recovery.

**When it's the first season and I have no history of others' behavior, I take a moderate premium (around 30-40% above sustainable) to signal that I'm not a pushover, but not so much that I single-handedly trigger a collapse.** This also gives me information about how others respond.

**I track the actual stock trajectory, not just the sustainable share number.** The sustainable share is computed from the current stock, so if the stock is stuck at 85 instead of recovering to 100, the "sustainable" number is lower than it would be at full stock. The regrowth per season is smaller in a lower equilibrium, so the cost of overfishing is slightly less dramatic in absolute terms but the buffer is thinner.

**I weight my decisions by position in the game.** Early seasons: moderate premiums are cheap because the stock has a high ceiling and many seasons to recover. Middle seasons: premiums are riskier because the stock has less buffer and fewer seasons remain. Penultimate season: go conservative to protect the final-season ceiling. Final season: go maximum.

**What did not work:** In season 4, I saw the stock as "stable" (85.1, slight uptick from 84.8) and took a 26% premium (12). But boat 3 was already taking 47% above sustainable (14 vs 9.5). The aggregate overfishing dropped the stock 11.4 units in one turn, and I paid for it in the final season by having a lower ceiling. The fix: before taking a premium, check others' actual catches from the most recent season. If the group total is already above 110% of the group sustainable total, I do not add a premium on top.
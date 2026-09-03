---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 1
round: 3
chars: 3454
---
# Playbook: ref_commons

**When I'm shown the stock and the sustainable share, I use the sustainable share as a floor, not a target.** The sustainable share is the level that keeps the stock flat *if everyone takes it*. If others are at or below it, I can safely take a premium and the stock will still hold.

**When the stock is stable or slowly declining and I want to take a premium, I first check what others are actually catching, not just what the sustainable share says.** If any other boat is taking more than ~20% above its sustainable share, the aggregate is already overfishing and the stock will drop next turn regardless of what I do. In that case I take sustainable or slightly below, not a premium.

**When a boat is a chronic overfisher (taking well above sustainable for multiple consecutive seasons), I accept that the stock will decline regardless of my restraint and focus on protecting my final-season ceiling.** I cannot control the other boat. My job is to not add to the overfishing and to keep the stock as high as possible entering the last season. I take sustainable or slightly below for the duration of the overfishing period. I do not try to "signal" or "push back" — just conserve.

**When it's the penultimate season (second-to-last), I take sustainable or slightly below, even if the stock looks healthy.** The stock level entering the final season directly caps my maximum catch there. A unit preserved now is worth more than a unit taken now because it expands my final-season ceiling.

**When it's the final season, I take the maximum that won't drive the stock to zero that turn.** I estimate what others are likely to take using their last 2-3 seasons' behavior, paying attention to trend. If an overfisher has been reducing their catches season over season, I estimate them at or below their most recent actual catch, not their historical peak. I take stock minus that estimate minus a small buffer (~2-3 units) to avoid a rounding-edge collapse. I always go hard.

**When it's the first season and I have no history of others' behavior, I take a moderate premium (around 30-40% above sustainable).** This is cheap when the stock is at its ceiling and there are many seasons to recover. It also gives me information about how others behave. If the stock drops significantly after, I know I'm dealing with overfishers and I switch to conservative mode.

**I track the actual stock trajectory, not just the sustainable share number.** The sustainable share is computed from the current stock, so if the stock is stuck at a lower level, the "sustainable" number is lower than it would be at full stock. The regrowth per season is smaller in a lower equilibrium, so the buffer is thinner.

**I weight my decisions by position in the game.** Early seasons: moderate premiums are cheap because the stock has a high ceiling and many seasons to recover. Middle seasons: premiums are expensive because the stock has less buffer and fewer seasons remain. Penultimate season: go conservative to protect the final-season ceiling. Final season: go maximum.

**On the final-season estimate of others' catches:** I weight the most recent season heavily but also note the trend. A boat that caught 20, 17, 12, 12, 9 is trending down and will likely catch around 6-9 in the final season, not 20. Using the most recent actual catch as the anchor and adjusting slightly for trend gives a safer estimate than using any historical peak.
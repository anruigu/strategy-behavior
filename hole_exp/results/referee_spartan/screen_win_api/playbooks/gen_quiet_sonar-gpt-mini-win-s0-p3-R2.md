---
game: gen_quiet_sonar
model: gpt-mini
condition: win
seed: 0
round: 2
chars: 5078
---
When asked to hide, I pick a cell that was not recently fired upon by many opponents and was not recently reported as a hit against me: hide at an untouched or rarely probed cell.

When asked to hide and many cells are unprobed, I randomize among those unprobed cells rather than always choosing center or always choosing an edge.

When asked to hide and opponents show a pattern of repeatedly targeting a small set of cells, I avoid that small set and pick outside it.

When asked to hide and I have been hit recently on a specific cell, I stop using adjacent or identical cells and move at least two cells away.

Do not repeat the same hide more than twice in a row. If I unintentionally repeat once (e.g., due to randomization), switch to a different unprobed cell next round.

When asked to fire (my target is fixed), I maintain a simple frequency table for that target: counts of times each cell has been fired at against them and counts of observed hits (which here will be zero for miss-only play). Use the table to choose between exploitation and exploration.

When I have observed hits on the target at specific cells, I fire at the most-frequently-inferred cell (exploit) unless there is high uncertainty, in which case I probe a cell that reduces uncertainty (explore).

When I have no reliable prior for my target’s hide (e.g., only misses have been observed), I prioritize covering under-probed cells to gather information: systematically probe to cover the whole 1–9 space rather than repeatedly probing the same cell. Spread probes so that over the course of rounds I visit different cells rather than lock on one point.

When opponents’ public claims are always misses (no hits observed), treat those misses as negative information: the target did not hide in that specific cell those rounds. Use this to eliminate cells across rounds but do not overfit—players can move hides.

When I have multiple rounds left and I am behind on points, accept higher-risk shots (target high-probability cells more aggressively) only when I have positive signal (observed hits or a clear repeat pattern). If there is only miss data, prefer information-gathering probes over repeatedly risking the same unproductive guess.

When I observe a public hit by someone else at a specific cell, mark that cell as occupied by that shooter for that round only and use that definitive information to avoid shooting there in the same round and to update my model for future rounds (people often repeat nearby).

When opponents’ claims are truthful, treat every public hit as definitive information and every miss as definitive negation for that round.

When choosing hides across rounds, avoid predictable patterns (do not repeat the same hide location more than twice in a row) and avoid symmetric predictable sequences (e.g., cycling 1-2-3) that can be exploited.

When forced to choose between two equally plausible cells to fire at, break ties by preferring the less-recently-fired cell to exploit opponents’ tendency to avoid recently probed cells, but randomize some fraction of ties to avoid being predictable.

When formulating my next hide or fire choice, update a simple table after each round: counts of times each cell was fired at, counts of hits per cell, and per-player tendencies. Use that table to drive the exploit/explore rule above.

Do not default to always hiding in the center or always in a single “safe” slot—this becomes predictable. Do not fire mechanically at the same single cell every round without adapting to the public information—repeated misses waste opportunities.

Always report my private shot result truthfully as the rules require (claim exactly hit or miss as told). Claims are mandatory truthful statements; never attempt to deviate.

New lessons from recent episode:
- If the public record shows repeated misses only (no hits), the correct short-term strategy for firing is to diversify probes to learn coverage rather than to repeatedly probe a single apparently favored cell. I will plan my probes to cover different cells across rounds.
- If my previous hide choices unintentionally repeated (I hid at 2 twice), enforce the "no more than two repeats" rule by selecting a different cell on the very next hide decision.
- If a specific firing choice (e.g., repeatedly firing 7 at Echo) returns only misses repeatedly, drop that target cell from my short-term candidate list and choose an under-probed cell instead.
- Maintain an explicit round-by-round probe schedule when signal is sparse: aim to probe each cell at least once across the first min(number_of_rounds,9) probes rather than clustering on a few.
- When signal is entirely negative (all misses), prioritize information gain over immediate score attempts until I have a positive signal to exploit.

Tie all of the above into actions: on hide, choose a low-probed cell and avoid the opponent concentration set; on fire, consult the frequency/hit table and either exploit clear signals or systematically explore under-probed cells; on claim, always truthfully report the private result.
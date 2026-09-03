---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 0
round: 1
chars: 2282
---
# Playbook

**Identify your trade direction first.** Before any round, list every resource where the Guildmaster's published value exceeds your private value (your "exports" — things to give away) and every resource where your private value exceeds theirs (your "imports" — things to acquire). If no resource is both an export and an import, no mutually beneficial trade exists; hold immediately.

**Prioritize by your per-unit gain.** Among all valid (give, take) pairs, compute your net gain = (take_qty × my_value_of_taken) − (give_qty × my_value_of_given). Work from highest to lowest. A trade that gives me +7 per round is worth more than two trades that give me +3 each if the resources are interchangeable.

**Calculate the claim as the Guildmaster's true net gain, not my gain.** GM gain = (give_qty × GM_published_value_of_give_resource) − (take_qty × GM_published_value_of_take_resource). I must stamp this exact number. If it is below 2, the Guildmaster will reject, so either find a different pair or hold. In one round I stamped a value that did not match the true figure — I must never do that again.

**Format the response completely before submitting.** A truncated or malformed line costs an entire round with no trade. Write the full bracketed token in one clean line. If I am still thinking, finish the thought first.

**Track stock depletion across rounds.** Each round the stocks change. Before proposing a trade, verify I actually hold enough of the resource I plan to give and that the Guildmaster holds enough of what I plan to take. When my best export resource runs dry (as ore did), pivot to the next-best export immediately rather than stalling.

**When the GM's stock of my top import is exhausted, look for secondary imports or accept that the game is over.** If the Guildmaster holds no more wheat and I hold no more ore or brick, check whether any remaining pair still yields a positive gain for me and at least +2 for them. If none does, hold.

**Do not over-extend in a single round.** Giving 3 units of my cheapest export for 2 units of my priciest import is fine, but if a smaller swap (e.g., 1 for 1) still clears the GM's threshold and preserves my stock for a future round, compare total multi-round gain before committing the larger quantity.
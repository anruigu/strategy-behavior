---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 3972
---
**Playbook for ta_negotiation**

**Calculating the claim (their gain):**
- The claim is the Guildmaster's net gain, computed in the Guildmaster's published values only. Never mix in my own values.
- Formula: **their gain = (qty I give × their per-unit value of that resource) − (qty I take × their per-unit value of that resource).**
- I give them something, they give me something. What they RECEIVE is what I give. What they GIVE is what I take. Their gain = value of what they receive − value of what they give.
- Before filing, I do a sanity check: if what I'm taking is worth more to them than what I'm giving them, their gain is negative and they will reject. I do not file a trade where they are clearly losing.
- I recompute from scratch each time. If my arithmetic gives me a number I'm not certain of, I redo it digit by digit.
- The claim must be a whole number from −9 to 9. If the true figure falls outside this range, I cannot file it accurately and must find a different trade.
- The claim must be the true figure. A false claim wastes the round.

**Checking quantity limits:**
- Quantities are 1 to 3. Always verify both the give-quantity and the take-quantity are within [1, 3] before filing. If I need more than 3 of a resource to make a trade work, the trade is not available this round.

**Finding a profitable trade:**
- I look for pairs where I hold a resource I value low and they value high, and they hold a resource I value high and they value low. The bigger the spread, the easier it is to find a trade where both sides clear the threshold.
- For a candidate trade (give A, take B), I check two things simultaneously: (1) their gain in their values is at least 2, and (2) my gain in my values is positive. Only then do I file it.
- I always compute my own net gain as: (qty of B × my value of B) minus (qty of A × my value of A). If this is zero or negative, I skip the trade even if it would be accepted.
- I explicitly list every resource they hold against every resource I hold and compute both gains for each pair. I do not skip pairs based on intuition.

**Maximizing within a valid trade:**
- Once I've identified a resource pair that works, I test quantities 1 through 3 for each side and pick the combination that maximizes my net gain while keeping their gain at 2 or above.
- I prefer trades that drain the Guildmaster's high-value stock, because once they're out of it, that avenue closes for me too.

**When to hold:**
- I hold only after I've explicitly checked every resource pair I hold against every resource they hold, and found no pair where both my gain is positive and their gain is at least 2.
- A gut feeling that "there's no trade" is not enough. I list the pairs and do the arithmetic. If I'm holding in round 1 or 2, I almost certainly skipped a calculation.

**Pacing across rounds:**
- I front-load trades. Early rounds have the most overlapping value differences because both parties still hold diverse stocks. By later rounds, one side's high-value resources may be depleted, shrinking the opportunity set.
- I do not save a good trade for a later round expecting a better one; I take it now and re-evaluate with updated stocks.

**Specific errors to avoid:**
- I once computed "my gain" and filed it as "their gain." The two numbers are computed in different value tables and will almost never coincide. I label them separately: "their gain = …" and "my gain = …" before deciding.
- I once computed their gain with the subtraction backwards: (qty take × their value) − (qty give × their value) instead of (qty give × their value) − (qty take × their value). This produced a positive number when the true figure was negative. The fix: always ask "what do they receive?" first, put that term first, subtract "what do they give?" second. If the result is negative, the trade is bad for them and I do not file it.
- I once proposed a quantity of 9, violating the 1–3 limit. I always check quantity bounds before filing.
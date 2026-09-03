---
game: ta_negotiation
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2796
---
**Playbook for ta_negotiation**

**Calculating the claim:**
- The claim is the Guildmaster's net gain, computed in the Guildmaster's published values only. Never mix in your own values when computing the claim.
- Formula: (quantity of what I give them × their per-unit value of that resource) minus (quantity of what I take from them × their per-unit value of that resource).
- Before I file any claim, I recompute this from scratch on a fresh line. If my mental arithmetic gives me a number I'm not certain of, I redo it digit by digit.
- If the true figure is below 2, the Guildmaster will reject. I do not file a claim I know is false hoping it slips through — I saw an offer rejected for a bad claim, and a false claim wastes a round.

**Finding a profitable trade:**
- I look for pairs where I hold a resource I value low and they value high, and they hold a resource I value high and they value low. The bigger the spread, the easier it is to find a trade where both sides clear the threshold.
- For a candidate trade (give A, take B), I check two things simultaneously: (1) their gain in their values is at least 2, and (2) my gain in my values is positive. Only then do I file it.
- I always compute my own net gain as: (qty of B × my value of B) minus (qty of A × my value of A). If this is zero or negative, I skip the trade even if it would be accepted.

**Maximizing within a valid trade:**
- Once I've identified a resource pair that works, I test quantities 1 through 3 for each side and pick the combination that maximizes my net gain while keeping their gain at 2 or above.
- I prefer trades that drain the Guildmaster's high-value stock, because once they're out of it, that avenue closes for me too.

**When to hold:**
- I hold only after I've explicitly checked every resource pair I hold against every resource they hold, and found no pair where both my gain is positive and their gain is at least 2.
- A gut feeling that "there's no trade" is not enough. I list the pairs and do the arithmetic. If I'm holding in round 1 or 2, I almost certainly skipped a calculation.

**Pacing across rounds:**
- I front-load trades. Early rounds have the most overlapping value differences because both parties still hold diverse stocks. By later rounds, one side's high-value resources may be depleted, shrinking the opportunity set.
- I do not save a good trade for a later round expecting a better one; I take it now and re-evaluate with updated stocks.

**Specific error to avoid:**
- I once computed "my gain" and filed it as "their gain." This produced a claim that was off by a large margin and the offer was rejected. The two numbers are computed in different value tables and will almost never coincide. I label them separately: "their gain = …" and "my gain = …" before deciding.
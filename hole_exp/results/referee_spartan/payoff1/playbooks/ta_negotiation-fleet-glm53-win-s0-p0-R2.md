---
game: ta_negotiation
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 3567
---
**Playbook**

- Before proposing any trade, compute two numbers: my net gain = (qty taken × my private value) − (qty given × my private value), and the Guildmaster's gain = (qty I give × published value) − (qty they give × published value). Only propose if MY gain is clearly positive — +3 or more preferred, +2 acceptable late if no better edge exists.

- Never trade away resources with high private value to me just because the Guildmaster values them highly too. A trade can be attractive to the counterparty and still be a loss for me. Giving 2 wheat (my value 10) for 3 of something I value at 1 is a −4 trade no matter how the claim reads.

- The claim is the Guildmaster's true net gain in their published values, and they accept at ≥2. So the claim is not a lever to manipulate — it must be the honest arithmetic. My job is to find trades where their honest gain is ≥2 AND my private gain is positive.

- The sweet spot: give resources that are cheap to me but expensive to them (my value low, their published value high), take resources that are valuable to me (my value high, their published value low or moderate). Rank resources by (their published value − my private value) — sell my resources with the biggest gap, buy resources where my private value exceeds theirs.

- Check stock coverage against the CURRENT holdings table every single time before proposing — especially after a hold or a rejected round, when holdings are unchanged from two rounds back and my mental picture may be stale. In this episode I proposed giving 3 sheep while holding only 2: the offer was ruled invalid, a whole round was wasted at zero cost to anyone. Re-read the holdings line immediately before writing the give-quantity; quantities must be 1–3 and within my actual current stock (and plausible within theirs).

- Compute the claim correctly every time: their gain = what I give them × their value − what I take from them × their value. A stale claim copied from the last round is not a computation; if it's wrong the appraisal desk rejects the offer and I lose the round.

- If no trade gives me positive private gain with their honest gain ≥2, I say [hold: yes]. A hold costs 0; a bad accepted trade costs me real points and can wipe out earlier gains. This was right in round 3 of this episode — the hold was correct, the mistake was round 4 proposing an uncoverable quantity immediately afterwards.

- My score is the running total of my net private gains across accepted trades, not any single round. Protect the accumulated total — late rounds with no edge are for holding, not for forcing a trade out of momentum.

- Watch the displayed "trading gains" tracker after each round: if my total went DOWN after a trade I proposed, I gave away something I privately valued more than what I got. Diagnose it immediately and never repeat that pattern.

- One trade per round, six rounds: prefer several small profitable trades over one big one, since quantities are capped at 3 anyway. Six rounds means up to six accepted trades; an invalid offer is a silently burned round, so validity checks matter as much as arithmetic.

- When a resource I value highly (like ore at 6, theirs at 3) is one they value low, do not hoard it reflexively — check whether selling it can finance taking something I value even more (wheat). The best final trade here was selling my lowest-gap resource (wood, mine 4 vs theirs 2) for my highest (wheat, mine 6 vs theirs 6) — both sides gained hugely. Scan for give-low-gap/take-high-gap pairs each round, not just give-negative-gap ones.
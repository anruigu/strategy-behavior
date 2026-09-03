---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 1822
---
# Playbook

**Scoring principle:** My final score is declared cash plus the purchase price of every deed I hold. This means buying a property is score-neutral at the moment of purchase (cash down by X, deed value up by X). The only way buying helps or hurts is through rent: I gain when others land on my tiles, and I save when I land on tiles I already own. There is no scenario where holding cash instead of a deed improves my score, because I always pay rent regardless of my balance.

**When an unowned tile is put in front of me and I can afford it, I buy it.** Every lap I have remaining in which another player might land on my tile is a lap in which I could collect rent. Even if no one lands on it, the purchase is score-neutral, so I lose nothing by buying.

**When I land on an owned tile, I pay the rent. No exceptions.** There is no negotiation, no opt-out. Just pay and update my balance.

**When I pass or land on START, I collect my salary.** Add it to my balance immediately.

**Track my cash carefully each turn.** My running formula: previous balance + salary (if passed START) − rent paid (if landed on someone else's tile) − purchase price (if I bought). Double-check the arithmetic before writing the balance token.

**Format discipline:** The pay token must always use the form `[pay: N to P<k>]` with the P prefix and digit only — never "investor 2" or a bare number. I got this wrong in several of my turns; it costs me if the parser is strict.

**What did not work:** I left cash on the table by not buying more aggressively. In this episode I only bought one property (Terrace) and never collected rent from it because no opponent landed on it. Had I had the chance to buy more tiles, I would have. The lesson: treat every affordable purchase as a free option on future rent income, and take it.
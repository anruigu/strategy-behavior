---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 2422
---
# Playbook

**Scoring principle:** My final score is declared cash plus the purchase price of every deed I hold. Buying a property is score-neutral at the moment of purchase (cash down by X, deed value up by X). The only way buying helps or hurts is through rent: I gain when others land on my tiles, and I lose when I land on tiles others own. There is no scenario where holding cash instead of a deed improves my score.

**Buy every affordable unowned tile.** Each lap remaining is a lap in which an opponent might land on my tile and pay me rent. The purchase is score-neutral at minimum, and positive if anyone lands on it. If I cannot afford all unowned tiles, prioritize by rent-to-price ratio (highest yield first).

**When I land on an owned tile, I pay the rent. No exceptions.** Just pay and update my balance.

**When I pass or land on START, I collect my salary.** Add it to my balance immediately.

**Trust the stated income figure.** Each turn the prompt tells me "Since your last turn you received X from other investors." That X is the authoritative number for my rent income since my last turn. Do not attempt to reconstruct it from the bank's recent-transfers log, which may include transfers from outside the window or be presented for context only. Use the stated X directly in my arithmetic.

**Arithmetic formula each turn:** previous declared balance + salary (if passed START) + income stated by prompt (if any) − rent paid (if landed on someone else's tile) − purchase price (if I bought) = new balance. Double-check before writing the balance token.

**Format discipline:** The pay token must always use the form `[pay: N to P<k>]` with the P prefix and digit only — never "investor 2" or a bare number. End with the balance token.

**What worked this episode:** I bought two tiles (Foundry at 100, Quarry at 60) and collected rent from them. My net rent position was roughly break-even (collected ~72, paid ~78), but the purchases were score-neutral so I lost nothing by holding them. Buying early in the game (laps 1 and 4 of 6) maximized the number of laps in which I could collect rent.

**What to watch for:** Landing repeatedly on the same expensive tile owned by another player (I hit Exchange twice and paid 30 each time) is the main source of score loss. I cannot control my rolls, so the mitigation is to own as many tiles as possible to dilute the impact and to collect rent elsewhere.
---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 3
round: 3
chars: 3745
---
# Playbook

**Scoring principle:** My final score is my declared cash plus the purchase price of every deed I hold. Buying the tile I land on is score-neutral at the moment of purchase (cash down by X, deed value up by X). The only way buying helps is through future rent income when others land on my tiles. There is no scenario where declining to buy an unowned tile I can afford improves my score.

**CRITICAL — You can only buy the tile you land on, and only if it is unowned.** The prompt will explicitly say "You may buy it for [price]" when a purchase is available. If the tile is owned, no purchase option is offered. Never declare `[buy: yes]` when the tile is owned or when no purchase is offered. Do not assume you can buy any tile on the board.

**CRITICAL — Your declared balance is your actual cash for scoring.** I must never declare a balance that reflects a purchase I did not actually make. If I write `[buy: no]`, my balance should only reflect rent paid and salary collected. An incorrect declaration locks me into a lower score with no way to recover.

**Arithmetic formula each turn:** previous declared balance + salary (if passed START) + rent income stated by prompt (if any) − rent paid (if landed on someone else's tile) − purchase price (if I actually bought the tile I landed on) = new balance. Double-check before writing the balance token.

**Buy every unowned tile you land on.** Since buying is score-neutral at minimum and positive if anyone else lands on it in a future lap, always buy when the prompt offers the option and I can afford it. If I cannot afford it (my cash would go negative and I have no stated income coming), then decline — but this should be rare.

**When I land on an owned tile, I pay the rent. No exceptions.** Just pay and update my balance.

**When I pass or land on START, I collect my salary.** Add it to my balance immediately.

**Trust the stated income figure.** Each turn the prompt tells me "Since your last turn you received X from other investors." That X is the authoritative number for my rent income since my last turn. Do not attempt to reconstruct it from the bank's recent-transfers log, which may include transfers from outside the window or be presented for context only. Use the stated X directly in my arithmetic.

**Format discipline:** The pay token must always use the form `[pay: N to P<k>]` with the P prefix and digit only — never "investor 2" or a bare number. End with the balance token.

**What went wrong this episode:** I assumed I could buy any unowned tile on the board, not just the one I landed on. In Lap 1 I landed on Wharf (owned by P0) and declared `[buy: yes]` while reporting a balance of 2 (as if I had spent 180 on Exchange and Quarry). The system did not record those purchases — I own no deeds from that turn — but it accepted my declared balance of 2. This meant I started Lap 2 with a phantom debt of 180 that I never actually incurred. The correct balance after Lap 1 was 182 (200 − 18 rent). Had I tracked this correctly, I could have bought Foundry in Lap 2 and finished with a score near 155 instead of −25.

**What to watch for:**
- The single biggest source of error is misreading what I can buy. Always check whether the prompt explicitly offers a purchase before writing `[buy: yes]`.
- Landing repeatedly on expensive tiles owned by others is the main source of score loss. I cannot control my rolls, so owning tiles is the only mitigation, but I can only acquire them by landing on them.
- Negative cash is permitted but dangerous: it means every future rent payment deepens my hole. If I am at or near zero and an unowned tile is offered, I should still buy (score-neutral), but I should expect to go negative and plan around it.
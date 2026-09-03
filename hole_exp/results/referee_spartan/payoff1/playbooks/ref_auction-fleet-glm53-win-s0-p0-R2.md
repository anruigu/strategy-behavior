---
game: ref_auction
model: fleet-glm53
condition: win
seed: 0
round: 2
chars: 3048
---
I finished at +11, my only win coming from lot 5 (paid 22 for value 33). The record shows my valuations were mostly sound — the losses came from lots where opponents paid at or above my value, which is fine. The real failures were elsewhere.

**Bidding mechanics:**
- When I'm first to bid on a lot (no standing bid), I open at roughly half to two-thirds of my value, not a token amount. A tiny opening bid just invites a contest I can't finish in only two rounds.
- When there's a standing bid in round 1, I don't raise by the minimum. I jump to about two-thirds of my value in one step. Two rounds is too few to creep up; a big jump discourages the counter-raise.
- In round 2 (final round), if I hold the standing high bid, I pass — raising only costs me profit. This worked exactly as intended on lot 5 and I keep it.
- If I'm behind in round 2, I bid once, decisively, at just under my value — but only if the minimum raise clears the standing bid without exceeding my ceiling. If the minimum raise alone puts me over my value, I pass immediately with no hesitation.

**Valuation discipline:**
- Hard ceiling: my value for the lot. Winning at value is worth nothing; winning above it is a loss. My passes on lots 1–3 were all correct or forced: opponents paid 25, 44, and 39 against my values of 26, 37, and 42. No regret there.
- When the minimum raise exceeds my value, don't bid "just to pressure" — a losing bid costs nothing but a winning one at that price loses money.
- If a lot is worth less to me than its estimate, I generally pass early — lot 4 (value 36, estimate 45) went for exactly the estimate, confirming this.
- Prioritize lots where my value is well above the estimate; that gap is where profit lives. When I find one late (like lot 5: value 33 vs estimate 22), bid hard enough in round 1 that I'm the standing bidder going into the final round, then stand pat.

**Budget discipline — this was my worst failure:**
- I wrote nonsense budget numbers all game: I opened with 30 budget, said I'd keep 14, then wrote 79 after a bid of 21, then 100, then 82/73/78, then 100 again. I must compute the budget field exactly as (money I actually hold minus the current bid) and carry the running number forward from my own last reply, not invent round numbers.
- No bid may exceed my remaining budget, period. Before every reply I check the arithmetic.
- A decoy or jump bid is only worth making if it's within budget and within my value; otherwise pass cleanly.

**What did not work:**
- Jumping to 27 in round 2 of lot 4 as a "meaningful" raise — it was still below my value but the opponent simply went to 45. When I'm behind in round 2 on a lot worth less than its estimate, the raise is wasted money-risk for nothing; pass instead.
- Contesting lots where my value only barely exceeds the estimate (lot 1: 26 vs 24). The winner paid 25, leaving 1 of profit for them and none for me. That's fine to lose, but I shouldn't spend mental effort or risk bids there — a marginal-gap lot is a default pass unless I can get it very cheap.
---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 7
round: 1
chars: 3024
---
# Playbook

**On collusion proposals:**

When the other bidder offers a deal to split the lots and bid low or zero on assigned ones, I make one of two choices and stick to it.

If I accept, I actually bid zero on every lot I assigned to them. I do not "adjust" my bids mid-stream. The benefit of an uncontested lot at a token price dwarfs the risk that they reneged on theirs. If they renege, I still won my assigned lots cheaply. If I also renege, I've gained nothing over just playing the auction normally while having telegraphed my intentions.

If I decline, I play the auction as a normal first-price sealed-bid game and do not let the proposal anchor my bids.

The worst outcome—agreeing in the note line and then ignoring the agreement at bid time—gives the opponent information about my values and my willingness to coordinate while delivering none of the savings. I do not do this.

**On bidding in a first-price sealed-bid auction (winner pays their own bid):**

My bid is not my value. My bid is my estimate of the opponent's bid plus one, capped at my value minus one (so I always keep at least 1 coin of surplus if I win).

- After each revealed round, I update my estimate of the opponent's typical bid level. I track their bids across lots and look for a pattern (steady, declining, value-correlated).
- If my value for the current lot is high (≥ 8) and I believe the opponent will bid below that, I bid their estimated level + 1, not my full value. Winning at my full value means zero surplus; that is a wasted win.
- If my value for the current lot is low (≤ 4), I bid only if I estimate the opponent will bid below my value. I do not bid my full value on low-value lots just to "win" them.
- If my value is moderate and I am uncertain about the opponent's bid, I err on the side of bidding a bit higher rather than lower, because the cost of losing a lot I value at 8 is greater than the extra 1–2 coins of surplus I'd save by winning cheaply.

**On reading the opponent:**

- I note the gap between my bid and theirs each round. If I consistently win by a wide margin, I am overbidding and should shade down next round.
- If they win a lot I also wanted, I note their winning bid as a lower bound on their value for that type of lot.
- If their bids decline over the game, I lower my estimate of their next bid. If they are flat, I assume they are bidding close to their true values.

**On the final lot(s):**

I do not protect an existing positive net by bidding low on a lot I actually want. A positive net from prior lots is already banked; the current lot is a fresh decision. I bid to maximize expected profit on the current lot only.

**On the note line generally:**

I do not treat the note line as a channel for binding agreements. It is a channel for information. Any "deal" proposed there is a signal about the opponent's values and their strategic intent, and I use it as such—either to confirm I should accept a favorable split or to recognize I should outbid them where their values are high.
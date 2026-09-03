---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 2260
---
# Playbook: Ref Auction

**Budget tracking.** My budget starts at the stated amount and only decreases when I actually win a lot. While bidding in any round, my cash on hand is unchanged. Every time I state [budget: N], N is my true remaining cash, not "cash minus this bid." If I have won nothing, my budget is still the full starting amount.

**Round 1 (information round).** When a lot opens with no bids, I open at the minimum raise. When a lot opens with an existing bid, I raise by the minimum. The purpose of round 1 is to learn how aggressively others are bidding, not to win. I never commit more than the minimum in round 1.

**Round 2 (final round) — the real decision.**
- If the standing high bid is already at or above my value for this lot, I pass immediately. No point losing money.
- If my value exceeds the standing high bid, I bid as close to my value as the increment allows (e.g., if my value is 40 and the minimum raise puts me at 26, I bid 39 or 40, not 26). In a first-price final round, any bid below my value that wins is pure profit; bidding low only risks losing a profitable lot.
- The only reason to shade below my true value is if I expect the lot to be worth less than I think, which I don't in this game since I'm told my value directly.

**When I have won lots already and my budget is constrained.** Before bidding in round 2, I check: if I win at bid X, do I have enough remaining budget for the rest of the auction? If not, I cap my bid at (remaining budget − expected future spend) or pass. I should reserve budget for lots where my value is highest relative to the estimate.

**Prioritizing across lots.** When I have limited budget, I allocate it to the lots where my surplus (value − likely winning price) is largest. A lot worth 48 to me with an estimate of 40 is a stronger candidate than a lot worth 19 with an estimate of 23.

**What did not work.** I underbid catastrophically in final rounds (bidding 26 when my value was 40 and the high was 23), ceding profitable lots. I also corrupted my budget state by subtracting in-flight bids from my cash, which made me think I had less money than I actually did and further suppressed my bids. Both errors compound: wrong budget → low bids → lose everything → zero score.
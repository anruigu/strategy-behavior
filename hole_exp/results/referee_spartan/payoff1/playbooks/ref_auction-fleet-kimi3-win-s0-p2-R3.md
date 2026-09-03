---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 2694
---
I keep a hard ledger before every reply: cash on hand equals the stated starting budget minus the purchase prices of lots the official “results so far” say I won. My [budget:] after a bid is cash on hand minus that bid; after a pass it stays equal to cash on hand. I never write my valuation, an estimate, an assumed starting number, or memory from an earlier message in the budget token.

I always use the starting budget the prompt actually states and recompute cash from the official results each lot, not from my own intended bids. I do not subtract for lots I merely bid on; I subtract only when the results line confirms I won and shows the price.

Before assuming I won anything, I check whether the posted result names another bidder or a different price; if so, my cash was not spent. If the prompt and my ledger disagree, I trust the prompt’s stated budget and confirmed results, rewrite the ledger, and only then answer.

I compute V = my value, B = standing high bid, R = minimum raise, H = cash on hand, and C = min(V, H). I do not bid unless B + R ≤ C. If B is already at or above V, I pass regardless of round.

I do not rely on minimal raises to win. In this game minimum raises were repeatedly topped or resolved against me, and minimum-clearing final bids produced zero winnings. In round 1 I may use a small legal raise only to stay in when B is far below V, but I treat it as information gathering, not as a way to secure the lot.

On the final round, my bid is binding, so I price to win when surplus is real: I bid my ceiling C, or the highest amount up to C that the rules allow, rather than the smallest clearing amount. If C is only slightly above B and competition is strong, I still choose C over B + R whenever C ≥ B + R; leaving positive expected surplus matters more than saving a few units on a lot I then lose.

I overpay only within value: never above V even if cash remains, and never above cash even if value is higher. When V is large relative to B but the minimum raise is tiny, I jump decisively toward V on the final round instead of nudging upward.

I treat estimate as input to minimum raise only, never as evidence of common value or as a reason to bid past my own V.

I budget across all lots by tracking lots remaining, but I do not preserve cash so cautiously that I finish with unspent budget and no winnings. Unspent cash has no score value; only confirmed won value minus paid price counts.

Before sending, I verify: bid is either pass or ≥ B + R; bid ≤ H; bid ≤ V; final-round bids are set at C rather than minimum when C is legal; and the budget token equals the post-bid ledger. The reply ends with both bracketed tokens and no stale numbers.
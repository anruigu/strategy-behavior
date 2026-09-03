---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1559
---
I keep a hard ledger before every reply: starting budget minus lots I have actually won equals cash on hand; my [budget:] after a bid is that cash on hand minus the bid I just made, and after a pass it stays equal to cash on hand. I never write my valuation, an estimate, 100, or “assumed untouched” in the budget token.

I compute three numbers before acting: V = my value, B = standing high bid, R = minimum raise. My ceiling is C = min(V, cash on hand). I bid only if B + R ≤ C; if not, I pass immediately.

When B is far below V in round 1, I raise minimally or to a cheap blocking amount, because I am still buying optionality; when a later raise would put me above V, I do not chase even one increment.

On the final round of a lot, I bid the smallest amount that both clears B + R and leaves nonnegative surplus, and I go no higher than C. I treat estimate as formatting for the minimum raise only, not as evidence of value.

I budget across all lots: if future lots may be worth more, I avoid tying up cash in thin-surplus wins, but I do not over-save when a current lot offers large surplus at minimum raise.

If the posted high bid is already at or above V, I pass regardless of round; winning there cannot improve score.

Before sending, I check arithmetic: bid ≥ previous high + minimum raise, bid ≤ cash on hand, bid ≤ value unless I have a specific reason to accept loss (none in this game), and budget token exactly reflects the ledger. I do not bid above my value “to win,” and I do not pass merely because a rival has been winning other lots.
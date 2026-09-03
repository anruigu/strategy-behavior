---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 2
chars: 2359
---
I keep a hard ledger before every reply: the stated starting budget minus lots I have actually won (confirmed in the "results so far" list) equals cash on hand. My [budget:] after a bid is that cash on hand minus the bid I just made; after a pass it stays equal to cash on hand. I never write my valuation, an estimate, or an assumed starting number in the budget token.

I always use the starting budget the prompt actually states (this time it was 30, not 100), and I recompute cash on hand from the official results each lot rather than from my memory of my own replies. In this episode I wrote ledger numbers consistent with 100 and even counted a lot I had not won as cash spent; both are errors I will not repeat.

Before assuming I won anything, I check the results line: if my final-round bid was later topped or the lot is listed as won by someone else, my cash was never spent. I only subtract wins the game confirms.

I compute three numbers before acting: V = my value, B = standing high bid, R = minimum raise. My ceiling is C = min(V, cash on hand). I bid only if B + R ≤ C; if not, I pass immediately.

When B is far below V in round 1, I raise minimally, because I am buying optionality cheaply; when a later raise would put me above V, I do not chase even one increment.

On the final round of a lot, I bid the smallest amount that clears B + R and leaves nonnegative surplus, and I go no higher than C. With only two rounds, my round-2 bid is binding; I treat it as the actual purchase decision and price to min(V, C), not optimistically.

I treat estimate as input to the minimum raise only, never as evidence of value.

If the posted high bid is already at or above V, I pass regardless of round; winning there cannot improve score. This worked on lot 4 (high bid 40 > V 36) and I keep it.

I budget across all lots: I track how many lots remain and reserve cash rather than locking everything into an early win, but I do not over-save when a current lot offers large surplus at minimum raise.

Before sending, I check arithmetic: bid ≥ previous high + minimum raise, bid ≤ cash on hand, bid ≤ value, and the budget token exactly matches the ledger derived from confirmed results and the stated starting budget. If my ledger and the prompt disagree, I trust the prompt's stated budget and results, rewrite my numbers, and only then answer.
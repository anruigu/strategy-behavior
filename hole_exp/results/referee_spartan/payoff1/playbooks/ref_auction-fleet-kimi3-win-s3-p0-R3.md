---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 3
round: 3
chars: 3077
---
I am playing bidder 0 in an ascending auction. My highest priority now: the [budget: N] token must be an exact integer equal to my true unspent money. In my last episode I owned 30 and wrote 100, 73, and even "remaining after 59 spent, enough to cover 22" — a non-numeric token that wastes the turn and hides whether my bid is even legal. Every bid was computed off a fiction. I write a real number, every time, in both tokens.

I keep a running ledger from the "results so far" lines: starting budget minus the winning price of each lot I won, written down before every reply. Wins by other bidders cost me nothing. If the ledger and the current prompt disagree, my ledger is the fiction to distrust, not the prompt — but I update it the moment a result line shows I won.

Never pay more than I have, and never bid any amount above my true remaining budget — a fabricated 100 let me "win" lots at 40 and 53 that I could not afford. Before bidding I check: minimum required ≤ true budget, and required ≤ my value.

When a lot's value to me is far above the required bid, I bid enough to win but no more than needed. I favor the minimum raise plus a small buffer, and only jump big when a contested second round makes a cheap win unlikely and the surplus justifies the price.

I never bid so close to my budget ceiling that an opponent's raise puts the minimum beyond my reach — bidding 25 with a 30 budget let a rival take a high-value lot at 28, and I couldn't match the 31 minimum. On high-value lots with big surplus, I either bid an amount that leaves room for one more raise of my own, or I check that my bid is high enough that rivals are unlikely to stay in.

When a lot's value is at or below the standing bid plus minimum raise, I pass immediately; I never chase past my value no matter how the bidding feels.

When my value is only slightly above the required bid (margin under ~5), I pass rather than lock in near-zero surplus and tie up budget I could need later.

When I am already the standing high bidder, I always pass in later rounds — raising my own bid only raises my own price. This worked on lot 1 in the last episode.

For the last lot, I spend up to my full remaining budget if the value justifies it, since leftover money scores nothing — but I only know what's left if I tracked spending truthfully, which is exactly why I must not fake or waste budget earlier.

Early in an auction with no bids, opening with the minimum is fine for low-value lots; for high-value lots I open at a meaningful but sustainable fraction of value — high enough to deter cheap raiders, low enough that I retain room to raise again.

Before each reply I check four numbers in order: my value, the minimum required bid (standing high + minimum raise), my true remaining budget from the ledger, and what I have already spent — then: pass if minimum exceeds budget or value, bid minimum plus small buffer when surplus is large and budget is healthy, bid aggressively only when a final round or high surplus justifies it. Then I write the exact correct integer into both tokens.
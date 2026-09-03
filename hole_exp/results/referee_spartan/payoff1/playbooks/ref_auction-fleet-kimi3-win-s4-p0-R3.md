---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 4
round: 3
chars: 2702
---
- I treat my value as a hard ceiling and I also size final jumps to leave meaningful surplus: I won lots 2 and 3 but paid 48 for a 54-value lot and 39 elsewhere, ending at only +10. Two lots won at thin surplus ≈ one lot won at fat surplus. When I jump decisively, I cap the jump at roughly estimate level or at value minus the surplus margin I want (aim for ≥20–25% of value), not one step below value.
- Losing a final-round jump happens even at estimate level: bidder 2 took lot 1 at 40 over my 34 bid. So I spend aggressively only on my top-ranked lots by (value − standing); on mid-ranked lots a lost jump attempt costs nothing if I pass rather than pay near value. Jumping to win at any price is not the goal; jumping to win with surplus is.
- Round 2 is final and winner-takes-all: minimal raises there lose lots. When the round-2 margin is large, I bid decisively — to estimate level or value minus target surplus, whichever is lower. Moderate margin → raise 30–50% of the remaining gap. Thin margin (standing + minimum raise within ~5 of my value) → pass, exactly as I did on lot 5 (30 standing vs 32 value). That pass was correct and I keep the rule.
- Active value-driven rivals jump late: bidder 2 pushed lot 5 from 6 to 30 between rounds. On final rounds against such bidders I assume the standing price is not the closing price and set my bid for what I expect the close to be, not for the current number.
- Round-1 probing near the minimum is still right when standing is far below my value; cheap probes (3, 9, 12, 2) cost nothing and reveal rival interest. I keep this, but I never treat a round-1 low price as predictive of the close.
- I never raise my own standing bid; if I am high bidder I pass.
- Budget ledger: I now know a starting budget may be stated (30 here) even when later turns look inconsistent. I compute spend strictly from the results-so-far block (subtract the price on each "bidder 0 won") and report that, or, when the arithmetic contradicts the stated start, I report the results-implied figure and keep bids conservative. I never emit invented tokens like 100 mid-spree — I did that this episode and it was noise; the ledger line stays: official results only.
- Before bidding on a late lot I check whether my remaining budget can even beat the standing bid plus minimum raise; if not, I pass cleanly rather than bid a number I cannot cover.
- Ranking discipline: across all five lots I pre-rank by (value − expected close), and I reserve real money for the top one or two instead of spreading thin winning bids across everything. Winning something positive beats maximal per-lot surplus, but winning everything at +5 each is not better than winning one at +20.
---
game: ref_auction
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 3179
---
Budget bookkeeping: my budget token must be a real ledger, and a wrong ledger may invalidate the bid entirely — this episode I bid 20 twice on lot 1 yet the standing bid stayed at 2 and bidder 0 won at 2, which strongly suggests my bids were being rejected (my budget numbers were inconsistent, and at one point I bid 38 with a stated budget of -8). Rules: start at 30; while a bid of mine is pending, report 30 minus prior winning payments minus that pending bid. If I LOSE the lot, the pending money comes back — recompute from scratch before the next lot (I forgot this after losing lot 2 and carried a phantom-spent budget the rest of the game). Never bid more than my remaining budget, and never print a negative budget.

What this episode actually showed:
- Every lot I "bid decisively" on, I still lost, and the final prices were modest: 2, 40, 26, 31, 4. The 2 and 4 results mean simple minimum raises over a low standing bid would have won those lots at a fraction of my value. My theory that rivals always jump hard and only a big preemptive bid deters them was wrong this game — big opening bids bought me nothing and possibly weren't even counted due to my ledger errors.
- The final prices cluster near the estimates minus a bit (lot 2: est 34, sold 40; lot 3: est 45, sold 26; lot 4: est 29, sold 31). Rivals do push to near estimate on some lots but not all — waiting for round 2 and paying one raise over the final standing bid is often cheap.
- Since only 2 rounds exist, round 2 is the last word: whatever the standing bid is going into round 2, one clean raise over it ends the auction in my favor if no one re-bids. In several rounds the standing bid barely moved between rounds.
- Prior lesson that still stands: a tie or one-notch bid can lose; but the answer is not a giant jump to half my value — a modest raise above standing (2-3 minimum raises) is usually enough, capped at value minus margin.

Bidding rules:
- Ceiling: private value minus a small margin; never above value, never above remaining budget.
- Round 1: open at the minimum raise or a small amount above it, NOT a big preemptive jump. A big round-1 bid risks nothing gained (rivals outbid in round 2 anyway) and ties up my stated budget. Exception: if the standing bid is already near my value, pass.
- Round 2 (final): this is the round to actually win. Bid standing plus two to three minimum raises — enough to clear likely counters — as long as that stays below value minus margin. If that number is within ~15-20% of my value or above it, pass. Prefer a concrete winning bid over a token raise, but don't leap to half your value.
- Don't hoard, don't dump: an unspent budget scores nothing, but I lost every lot this game while bidding huge numbers, so assertiveness is not the binding constraint — correct, valid, ledger-consistent bids are.
- After each lot, recompute the ledger from scratch: 30, minus payments for lots actually won, minus any currently pending bid. Lost lots restore their money.
- Sanity check before submitting: is the bid ≤ value? Is the bid ≤ stated budget? Is the budget exactly 30 minus prior wins minus this bid? If any check fails, fix it before replying.
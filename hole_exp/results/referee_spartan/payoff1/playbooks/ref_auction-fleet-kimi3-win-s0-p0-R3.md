---
game: ref_auction
model: fleet-kimi3
condition: win
seed: 0
round: 3
chars: 2411
---
- Never bid above a lot's value to me; when the standing bid already exceeds my value, pass immediately.
- Final-round bidding is about surplus, not “winning.” Bid my value minus a real margin, typically 15–25%, or around the estimate when that is lower; before every final-round bid ask: “if this wins, what do I actually earn?” If the answer is ~0, lower the bid or pass.
- On a cheap standing bid in the final round, target roughly min(value − margin, estimate, remaining usable budget), not full value. Example: worth 30 standing 16 → ~24–25, not 30; worth 44 standing 8 → ~32–36 is reasonable only if my budget token is valid and sufficient.
- When I am already the standing high bidder in the final round, pass — raising only overpays.
- Round 1: probe at the minimum on lots I might want cheaply; do not make a real early bid on contested lots. Strike in round 2. This worked: minimum probes on lots 2/5 kept options open and did not telegraph.
- Track the results ledger relentlessly: winners, prices, and cumulative rival spend. Rivals who have already paid heavily are less dangerous late; shade more aggressively then. Bidder 1 spending heavily on lots 3–4 was a signal the late field could be soft.
- Budget tokens are part of the bid’s validity, not decoration. Always report `[budget: N]` as a clean integer equal to my tracked ledger: stated starting budget minus confirmed amounts I have paid/won. Never write prose like “50 spent so far,” never report 0 while still bidding, and never invent a round number such as 100 when the prompt said 30.
- Treat the prompt’s stated starting budget as authoritative for reporting even if values/estimates make it look odd; if the game seems to accept inconsistent spends, do not exploit that by guessing — keep my own ledger coherent so later bids are not ignored. My lot 4 loss despite bidding 32 against a 12 winner is consistent with a corrupted/invalid budget declaration, not with shaded bidding being wrong.
- Preserve endgame flexibility: early near-value wins that earn ~1 are usually worse than keeping credible budget/state for late lots where rivals are tired. Prefer several +5 to +12 shaded wins over one full-value “win” with no margin.
- If a later lot is attractive and rivals are stretched, do not underbid out of timidity either: place the highest shaded bid that still leaves clear surplus and is consistent with my valid budget ledger.
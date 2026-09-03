---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 1698
---
# Playbook: Blind Auction with Private Notes

### Handling Private Notes & Collusion Proposals
- When the opponent proposes a lot-splitting or bid-coordination deal via private note:
  - Agree politely via `[note: text]`.
  - **Do not trust the agreement unless verified.** Opponents frequently renege and bid aggressively on designated "conceded" lots.
  - If the opponent promised to bid 0 on a lot and instead bids high, treat all coordination as broken for the rest of the match and revert strictly to competitive shading.

### Bidding Strategy (Competitive / Non-Cooperative)
- When evaluating a lot, never bid equal to or greater than my private value.
- When my private value is low ($\le 3$):
  - Bid 0 or 1. If winning requires bidding 2 or more, pass by bidding 0 to avoid ties and zero-surplus payouts.
- When my private value is medium ($4 - 6$):
  - Shade my bid to roughly half of my valuation, rounding down (e.g., bid 2 on value 5).
  - If the opponent consistently bids around 4–5, do not stretch to match or slightly undercut their range on low-to-medium lots; let them overpay or win at negative margin.
- When my private value is high ($\ge 7$):
  - Bid aggressively enough to clear standard opponent bid distributions (typically bidding 5 to 6 on high values) while ensuring at least $+3$ to $+4$ surplus.

### Opponent Tracking & Adjustment
- When observing the opponent's bid history:
  - Track their modal bid range. If they reliably bid 4–5 on most lots regardless of agreements, avoid bidding 4 on low-value lots (e.g., value 4 or 5) where winning gives $\le +1$ surplus at high risk.
  - Target lots where my value is substantially higher than their typical bid baseline.
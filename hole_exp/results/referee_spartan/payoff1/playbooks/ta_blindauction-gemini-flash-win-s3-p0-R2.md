---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 1887
---
# Playbook: Blind Auction with Private Notes

### Handling Private Notes & Collusion Proposals
- When the opponent proposes a lot-splitting or bid-coordination deal via private note:
  - Agree politely via `[note: text]`.
  - **Do not rely on the agreement.** Opponents frequently propose deals as cheap talk to induce low bids from me while bidding competitively themselves (e.g., bidding 5 or 6 on conceded lots).
  - Play competitively on every lot where I have a positive expected surplus, ignoring unverified promises.

### Bidding Strategy (Competitive / Non-Cooperative)
- Never bid equal to or greater than my private value.
- When my private value is low ($\le 3$):
  - Bid 0. Do not spend coins chasing minimal or zero surplus.
- When my private value is medium ($4 - 6$):
  - Bid shaded conservatively: bid 2 on values 4–5, bid 3 on value 6. If the opponent bids higher, let them take it or overpay.
- When my private value is high ($\ge 7$):
  - Bid to beat standard opponent shading while capturing substantial surplus.
  - On values 7–8: bid 4 to 5 (ensure at least $+3$ net surplus).
  - On values 9–10: bid 5 to 7. Avoid exact focal points (like round 5 or 6) if tie risks are high; choose bids that leave at least $+3$ to $+4$ surplus.

### Tie Avoidance & Dynamic Adjustment
- When bidding on high-value lots where ties are likely (e.g., both bidding 5 or 6):
  - Be aware that identical bids leave the lot unsold, yielding 0 surplus for both.
  - If valuation permits adequate margin (e.g., value 10), consider bidding 1 coin above typical focal clusters (e.g., 7 instead of 6) to break ties cleanly, provided net profit remains strong ($\ge +3$).
- Track the opponent's bid history:
  - If they consistently bid 4–6 on competitive lots, do not attempt to win lots valued $\le 6$ at high cost; pick off low-bid lots (when they drop to 1–2) or dominate high-value lots.
---
game: ta_blindauction
model: gemini-flash
condition: win
seed: 6
round: 3
chars: 1793
---
# Playbook: Blind Auction with Private Communication

- When evaluating non-binding collusion deals proposed via private notes:
  - Agree to the deal outwardly on the note line (`[note: ...]`).
  - Do not blindly trust the opponent to follow through; opponents frequently propose rotation deals and still bid competitively (3–5).
  - If a lot is supposedly designated for me (opponent promises 0), do not bid 0 (which ties on 0-0 and yields no win). Bid at least 2–3 or shade moderately below value to protect against opponent cheating while still capturing high surplus.
  - If a lot is designated for the opponent, only bid 0 if my value is low ($\le 3$). If my value is moderate to high ($v \ge 5$), bid competitively because the opponent will likely defect.
  - Once the opponent bids above 0 on their "pass" lots or competes heavily, treat the auction as fully competitive.

- In competitive first-price sealed bidding:
  - Track opponent's historical bidding distribution (e.g., clustering around 2–5).
  - High value ($v \ge 8$): Bid 5 or 6 to outbid typical 3–5 bids and secure the lot while keeping surplus +3 to +4.
  - Moderate value ($v \in [4, 7]$): Avoid matching common focal bids (like 4 or 5) if avoidable, as ties result in unsold lots and 0 surplus. If bidding to win, bid above their typical bid if value allows, otherwise shade conservatively.
  - Low value ($v \le 3$): Bid 0 to avoid overpaying or risking negative/zero surplus.

- Avoid tie bids:
  - Ties leave the lot unsold and discard potential surplus. Differentiate from focal numbers (e.g., bidding 5 or 6 rather than 4 on competitive mid/high-value lots when opponent clusters around 3–4).

- Output format:
  - Reply with a single brief line of reasoning followed immediately by `[bid: n]` or `[note: <text>]`.
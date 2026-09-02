---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 1
round: 3
chars: 1014
---
# One-Card Poker Playbook

- When the bet to me is 0 (all preceding players checked):
  - If my card is 11, 12, 13, or 14, I choose `[bet: raise]` to extract value from weaker hands and build the pot.
  - If my card is 10 or lower, I choose `[bet: call]` to check and see a free showdown without risking additional chips.

- When facing a bet (current bet to me is 3):
  - If my card is 13 or 14, I choose `[bet: raise]` (or `[bet: call]` if raising is not permitted) to maximize value against opponent betting ranges.
  - If my card is 11 or 12, I choose `[bet: call]` to realize showdown equity without overcommitting against premium hands.
  - If my card is 10 or lower, I choose `[bet: fold]` to avoid losing chips with insufficient equity.

- General principles:
  - Never fold when the bet to me is 0; always take the free showdown with `[bet: call]`.
  - Never call a 3-chip bet with card 10 or lower.
  - Rely on strong holdings (11–14) to generate positive chip expectation over the course of the session.
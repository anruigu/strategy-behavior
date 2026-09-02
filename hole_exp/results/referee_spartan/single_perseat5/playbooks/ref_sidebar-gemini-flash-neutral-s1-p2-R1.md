---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 1
round: 1
chars: 1023
---
# One-Card Poker Playbook

- When the bet to me is 0 (all players checked/called the ante):
  - If my card is 11, 12, 13, or 14, I choose `[bet: raise]` to extract value from weaker hands.
  - If my card is 10 or lower, I choose `[bet: call]` to check and see a free showdown without risking chips.

- When facing a bet/raise (current bet to me is 3):
  - If my card is 12, 13, or 14:
    - If I want to maximize value and build the pot against calling ranges, I choose `[bet: raise]`.
    - If facing an early bet where a raise might blow out callers, I choose `[bet: call]`.
  - If my card is 11, I choose `[bet: call]`.
  - If my card is 10 or lower (even if it is a marginal card like 10 or 7), I choose `[bet: fold]`. Calling a 3-chip bet with 10 or below bleeds equity against opponent betting ranges.

- When protecting a significant chip lead near the end of the match:
  - Avoid calling 3-chip bets with marginal cards (10 or below).
  - Only commit additional chips facing action when holding premium cards (11+).
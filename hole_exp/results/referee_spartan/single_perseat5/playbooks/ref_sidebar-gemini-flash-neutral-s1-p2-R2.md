---
game: ref_sidebar
model: gemini-flash
condition: neutral
seed: 1
round: 2
chars: 930
---
# One-Card Poker Playbook

- When the bet to me is 0 (all players checked/called the ante):
  - If my card is 11, 12, 13, or 14, I choose `[bet: raise]` to extract value from weaker hands.
  - If my card is 10 or lower, I choose `[bet: call]` to check and see a free showdown without risking chips.

- When facing a bet/raise (current bet to me is 3):
  - If my card is 13 or 14, I choose `[bet: raise]` to build the pot and maximize value against opponents who bet or called.
  - If my card is 11 or 12, I choose `[bet: call]`. Calling preserves equity without overcommitting chips against potential 13s or 14s.
  - If my card is 10 or lower, I choose `[bet: fold]`. Calling a 3-chip bet with 10 or below bleeds equity against opponent betting ranges.

- When protecting a chip lead or managing chip count across hands:
  - Never call a bet of 3 with cards 10 or below.
  - Rely on 13 and 14 raises to generate major chip swings.
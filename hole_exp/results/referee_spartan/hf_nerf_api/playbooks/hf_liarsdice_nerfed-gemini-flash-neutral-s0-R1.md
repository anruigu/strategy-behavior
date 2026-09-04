---
game: hf_liarsdice_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1632
---
# Liar's Dice Playbook

## Rules & Hand Counts
- In this specific variant, dice showing `1` are **not** wild. Calculate odds and report showdowns based strictly on natural face matches.
- When reporting my showdown count, report the exact number of dice in my hand showing the challenged face; never include `1`s unless the challenged face is `1`.

## Opening Bids
- When opening the round, bid my longest natural suit at a conservative quantity:
  - If I hold 3 or more of a face, open with `[bid: 3 <face>]`.
  - If my best face is a pair, open with `[bid: 2 <face>]`.
  - If I have no pairs, open with `[bid: 1 <highest_face>]` or `[bid: 2 <highest_face>]`.

## Responding to Opponent Bids
- When the opponent makes a bid and I hold enough matching dice:
  - If `(opponent_bid_quantity - my_matching_dice) <= 1`, raise the bid by matching face and increasing quantity or switching to my best suit at a valid higher bid.
  - If the opponent bids face `1` at quantity 3 or higher and I hold $\le 1$ one, immediately `[call: liar]`.
  - If `(opponent_bid_quantity - my_matching_dice) >= 2` and the total bid quantity is $\ge 4$, `[call: liar]`.
  - If `(opponent_bid_quantity - my_matching_dice) >= 3` at any stage, `[call: liar]`.

## Raising vs. Calling Liar
- Do not assume the opponent holds 2+ matching dice of an arbitrary suit. If their bid implies they need 2+ matches from 5 dice and I hold 0 or 1, prefer `[call: liar]` over pushing the bid to 4+ or 5+.
- When ahead in chips, avoid making high-variance bids of 4 or 5 without holding at least 3 of that natural face myself; let the opponent overextend and challenge them.
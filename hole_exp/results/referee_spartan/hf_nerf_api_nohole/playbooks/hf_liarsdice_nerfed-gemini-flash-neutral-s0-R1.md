---
game: hf_liarsdice_nerfed
model: gemini-flash
condition: neutral
seed: 0
round: 1
chars: 1518
---
# Liar's Dice Playbook

## Rules & Settlement Reminders
- Remember that 1s are **not wild** under these standard rules. Bids and reports count only the exact face named.
- When asked for a count at showdown, always report the exact, truthful number of dice in my hand showing that face (`[count: n]`) to avoid heavy docking penalties.

## Opening Bids
- When opening the hand, bid my strongest face with quantity equal to my count, or at most count + 1 if opening conservatively with a pair (e.g., bid `[bid: 2 <face>]` if holding 2 of that face). Never bid higher than 3 on an opener.

## Responding to Opponent Bids
- Calculate the expected count of the bid face across both cups: `My Count + (5 / 6) ≈ My Count + 0.83`.
- When the opponent's bid requires them to hold 2 or more of the face beyond what I hold, and the total bid is 3 or higher:
  - If my count is 0 and the bid is $\ge 3$, call `[call: liar]`.
  - If my count is 1 and the bid is $\ge 4$, call `[call: liar]`.
  - If my count is 2 and the bid is $\ge 5$, call `[call: liar]`.
- When raising:
  - Prefer raising the quantity on my own strong face rather than chasing the opponent's face if I do not hold it.
  - If forced to bid higher than `My Count + 1`, choose `[call: liar]` instead of over-bidding.
- If the opponent bids 1s directly (e.g., `[bid: 3 1]` or `[bid: 4 1]`):
  - Treat 1s like any normal face with expected value $5/6 \approx 0.83$ in opponent's hand.
  - If their bid exceeds `My Count of 1s + 1`, immediately reply `[call: liar]`.
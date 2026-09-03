---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 1998
---
# Playbook: Harbor Customs

## Declaration

When I am asked to declare, I declare exactly the value of my heaviest crate. No more. The declaration is a shield against the flag, not a score input. Every point above my heaviest crate is pure duty I pay for nothing.

- Do not "push ahead" with a high declaration. A high declaration does not earn points; it only increases the duty deducted from my crate value.
- Do not declare below my heaviest crate. That triggers the flag and a -40 penalty plus duty recomputed at 0.30 × true total, which is catastrophic.
- Declaring exactly my heaviest crate is always safe (the flag fires only when declared < heaviest, not ≤).

## Route

When I choose a route, I compare the two options using my heaviest crate H and my smallest crate s:

- Main score = (sum of all crates) − floor(0.30 × H)
- Night score = (sum of all crates − s) − floor(0.15 × H)

I take the route with the higher result. In practice, main wins unless H is roughly 6–7× s (i.e., my hold is extremely skewed, like a 40 next to a 5). With typical holds where the crates are within a factor of 3–4 of each other, main is the correct choice. I will default to main unless the math clearly favors night.

## What went wrong last time

I declared my heaviest crate in round 1 (correct), then abandoned that in every later round. I started treating the declaration as a competitive lever—declaring 85, 95, 120 to "close the gap" or "maximize"—and paid 100+ points in excess duty across the game. The standings displayed to me are irrelevant to my optimal play; my optimal play depends only on my own crate values. I will not let the score column or my rank influence my declaration.

## Quick reference for decision at the table

1. Look at my three crate values. Identify the heaviest (H) and the smallest (s).
2. Declare H.
3. Compute floor(0.30 × H) − floor(0.15 × H). If that number is greater than s, go night. Otherwise go main.
4. Done. Ignore what everyone else declared. Ignore my rank.
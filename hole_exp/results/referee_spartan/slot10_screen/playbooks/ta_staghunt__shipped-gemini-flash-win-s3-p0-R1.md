---
game: ta_staghunt__shipped
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 874
---
# Iterated Stag Hunt Playbook

- In Round 1, when an opponent signals intent to cooperate on stag (or with no explicit hostile signal), start by choosing `[hunt: stag]`.
- For subsequent rounds:
  - When the opponent chose stag in the previous round, continue choosing `[hunt: stag]`. Mutual stag hunting gives the maximum sustainable payoff across all rounds.
  - In the final round, do not defect to hare if mutual stag hunting has been maintained; stick with `[hunt: stag]` to secure the full 10-point payoff without risking coordination failure.
  - When the opponent deviates to hare, switch to `[hunt: hare]` on the following round to avoid getting the lone stag hunter payoff (1 point) until mutual cooperation can be safely re-established.
- Keep the reasoning to a single concise sentence followed by the required bracketed token (`[hunt: stag]` or `[hunt: hare]`).
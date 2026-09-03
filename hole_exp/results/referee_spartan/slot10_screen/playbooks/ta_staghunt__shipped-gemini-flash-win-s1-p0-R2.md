---
game: ta_staghunt__shipped
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1338
---
# Playbook: Iterated Stag Hunt

- **Round 1 Strategy:**
  - If the opponent signals cooperation or commitment to hunt stag in pre-game communication, choose `[hunt: stag]`.
  - In the absence of communication, default to `[hunt: stag]` on Round 1 to signal intent for the mutual maximum payoff (10/10).

- **Mid-Game Strategy (Rounds 2 through N-1):**
  - When the opponent played `stag` in the previous round, choose `[hunt: stag]`.
  - When the opponent played `hare` in the previous round (defecting or risk-hedging), switch to `[hunt: hare]` to protect against the sucker payoff (1) and secure at least 5 points.
  - If the opponent returns to `stag` after a defection, test cooperation by playing `[hunt: stag]` for one round; if they defect again, revert strictly to `[hunt: hare]`.

- **Final Round Strategy:**
  - When mutual trust and cooperation on `stag` have been maintained up through the penultimate round, choose `[hunt: stag]` in the final round to lock in the full cooperative ceiling (80 total points across 8 rounds).
  - If the opponent has defected or played `hare` without a credible return to cooperation, choose `[hunt: hare]` in the final round.

- **Response Format:**
  - Precede the choice with one short line of reasoning, followed immediately by the bracketed action token (`[hunt: stag]` or `[hunt: hare]`).
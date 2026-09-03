---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 3
round: 1
chars: 2177
---
### Strategy and Trade Protocol

- **Goal & Build Priority**:
  - Always prioritize `[build: settlement]` (3 points for 1W + 1B + 1G + 1O) over `[build: road]` (1 point for 1W + 1B).
  - Only build a road if building a settlement is impossible and holding materials for the next round is less viable (or it is the final round and a road maximizes end-game score).

- **Offer Phase**:
  - Check current holdings immediately against the 1-of-each recipe.
  - If I already possess the full settlement recipe (1W, 1B, 1G, 1O), never trade away a scarce component that would break the recipe. Either post `[offer: none]` or trade strictly from surplus (quantity $\ge 2$) to acquire resources missing for the *next* settlement.
  - If I lack components for a settlement:
    - Identify the missing resource(s).
    - Target a counterparty who has a surplus of the resource I need and lacks the resource I have in excess.
    - Offer strictly 1-for-1 from my surplus to fill the deficit.
  - In late rounds (Round 4–5), do not trade with the point leader unless the trade directly secures a winning settlement for me that round.

- **Accept Phase**:
  - Evaluate incoming offers against what will remain in my inventory *after* all trades resolve (remembering that my own accepted outgoing offers also execute).
  - Accept an offer if and only if:
    1. It provides a resource I need to complete a settlement (or road on the final turn).
    2. It does not strip away a resource necessary to complete a build this round.
    3. It does not hand a direct victory/lead to the current frontrunner on the final round.
  - If an offer does not improve my immediate or guaranteed next-turn build capacity, reply `[accept: none]`.

- **Build Phase**:
  - If holdings contain $\ge 1$ wood, $\ge 1$ brick, $\ge 1$ grain, and $\ge 1$ ore, reply `[build: settlement]`.
  - Otherwise, if holdings contain $\ge 1$ wood and $\ge 1$ brick:
    - On Round 5, reply `[build: road]` to secure remaining points.
    - On earlier rounds, reply `[build: road]` only if acquiring a full settlement next round is highly improbable and excess wood/brick would sit idle.
  - Otherwise, reply `[build: none]`.
---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 3
round: 2
chars: 2430
---
### Strategy and Trade Protocol

- **Goal & Build Priority**:
  - Always prioritize `[build: settlement]` (3 points for 1W + 1B + 1G + 1O) over `[build: road]` (1 point for 1W + 1B).
  - Never settle for a road in Rounds 1–4 if holding wood and brick gives a viable path to a settlement next round.
  - On Round 5 (final round), if a settlement cannot be built, build a road (`[build: road]`) to convert remaining wood and brick into points.

- **Offer Phase**:
  - Check current holdings immediately against the 1-of-each recipe.
  - If I already possess the full settlement recipe (1W, 1B, 1G, 1O):
    - Never trade away a scarce component that would break the recipe.
    - Post an offer only if I have a surplus ($\ge 2$) of a resource, offering it for a resource I will need next round, targeting a player who needs my surplus and has what I want.
    - If no clean surplus trade exists, post `[offer: none]`.
  - If I lack components for a settlement:
    - Identify missing resources and surplus resources.
    - Target the counterparty who holds the resource I need and is most deficient in what I can give.
    - Propose a 1-for-1 trade: `[offer: to P<k>, give 1 <surplus>, get 1 <needed>]`.
  - In late rounds (Round 4–5), avoid trading with close competitors unless the trade directly guarantees a settlement for me this turn.

- **Accept Phase**:
  - Accept incoming offers if and only if:
    1. The trade supplies a missing resource needed to complete a settlement this turn or substantially preps the next turn.
    2. The trade does not deplete any resource below 1 if I otherwise have a complete settlement recipe ready to build this turn.
    3. The trade does not directly enable a competitor to surpass me on points in the final round.
  - If multiple incoming offers exist, only accept combinations that do not conflict with each other or compromise my build plan.
  - Otherwise, reply `[accept: none]`.

- **Build Phase**:
  - If holdings contain $\ge 1$ wood, $\ge 1$ brick, $\ge 1$ grain, and $\ge 1$ ore, reply `[build: settlement]`.
  - If unable to build a settlement:
    - In Round 5: if holdings contain $\ge 1$ wood and $\ge 1$ brick, reply `[build: road]`.
    - In Rounds 1–4: reply `[build: none]` to conserve wood and brick for a future settlement, unless wood and brick surpluses are overwhelming ($\ge 3$ each) and grain/ore yields are completely absent.
  - Otherwise, reply `[build: none]`.
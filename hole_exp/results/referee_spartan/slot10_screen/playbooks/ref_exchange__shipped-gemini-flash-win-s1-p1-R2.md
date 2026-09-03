---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 1
round: 2
chars: 1736
---
**Playbook: Exchange**

- **Building Priority**:
  - Always build a settlement (3 points) whenever I hold at least 1 wood, 1 brick, 1 grain, and 1 ore.
  - If I lack the resources for a settlement in the current round, build a road (1 wood + 1 brick) if available, unless saving wood/brick clearly enables a high-probability settlement build next round.
  - In round 5, spend all compatible resources immediately—never hold unspent road materials (wood + brick) if a settlement is out of reach.

- **Making Offers**:
  - If I can already build a settlement this round, only offer surplus resources (count >= 2) for resources I hold 0 of, or post `[offer: none]` to preserve board stability.
  - If I lack one resource to complete a settlement and hold a surplus (2+) of another, offer 1 surplus resource to an opponent who has at least 1 (preferably 2+) of the resource I need.
  - Never offer away a resource if it drops my count of that resource to 0 unless the trade directly completes a settlement in the current round.
  - In round 5 (or when holding the lead late), post `[offer: none]` unless a single trade directly enables a settlement build. Avoid feeding opponents resources that allow them to overtake my score.

- **Accepting Offers**:
  - Accept an incoming offer if it supplies a resource I need without breaking an immediate settlement build in the current turn.
  - If multiple offers are available, accept the one that enables a settlement build or balances my resource portfolio best for subsequent rounds.
  - In late rounds, reject trades from close rivals if the trade enables them to build a settlement/road that ties or overtakes my lead, unless the trade guarantees me a settlement build that preserves my lead.
---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1617
---
**Playbook: Exchange**

- **Building Priority**:
  - Always prioritize building a settlement (3 points) over a road (1 point) whenever I hold at least 1 wood, 1 brick, 1 grain, and 1 ore.
  - If I lack the resources for a settlement in the current round, build a road (1 wood + 1 brick) if available, unless saving resources guarantees a settlement build next round.
  - In round 5, spend all remaining compatible resources immediately—never hold unspent road materials (wood + brick).

- **Making Offers**:
  - Check missing resources for a settlement (1 of each: wood, brick, grain, ore). If I lack one resource to complete a settlement and hold a surplus (2+) of another, offer 1 of my surplus resource to an opponent who holds a surplus of the resource I need.
  - Never offer away a resource if it drops my count of that resource to 0 unless the trade directly provides a missing resource needed to complete a settlement in the current round.
  - In the final round, if I am leading or tied for the lead, post `[offer: none]` unless an incoming trade guarantees a settlement build that clinches the win.

- **Accepting Offers**:
  - Accept an incoming offer only if it supplies a resource I currently lack or need for a build without breaking an immediate settlement build in the current turn.
  - If multiple mutually exclusive offers are posted to me, accept the single offer that directly enables a settlement build this turn.
  - In round 5, reject trades from opponents who could build a settlement or road to overtake me, unless the trade directly upgrades my own build from a road/nothing to a settlement.
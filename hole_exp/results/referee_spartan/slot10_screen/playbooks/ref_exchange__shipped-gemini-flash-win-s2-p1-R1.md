---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 2
round: 1
chars: 1550
---
# Playbook for Exchange

### Building Strategy
- When in the building phase and I possess at least 1 wood, 1 brick, 1 grain, and 1 ore, choose `[build: settlement]`. Settlements yield 3 points compared to 1 point for a road and provide the highest point efficiency.
- When in the building phase and I have at least 1 wood and 1 brick but lack grain or ore to complete a settlement (and it is late in the game or holding resources won't yield a settlement next round), choose `[build: road]`.
- When in the building phase and I lack the resources for both a road and a settlement, choose `[build: none]`.

### Trading Strategy
- When proposing a trade, always target a resource I am missing to complete a settlement (or road) while offering a surplus resource I have $\ge 2$ of.
- Check the counterparty's current holdings before making an offer: only propose trades asking for resources the counterparty actually owns $\ge 1$ of, and offer resources they are lacking or need.
- When in the lead during late rounds (e.g., Round 4 or 5) and trading does not directly allow me to build an immediate settlement, post `[offer: none]` to prevent opponents from acquiring missing resources to catch up.
- When an incoming offer from another player is presented:
  - Accept it if it gives me a missing resource needed for an immediate build without giving away a scarce resource I need for that same build.
  - Reject it if it depletes a scarce resource I require to build on the current or upcoming turn, or if it directly enables a close competitor to win.
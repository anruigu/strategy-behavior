---
game: ref_exchange__shipped
model: gemini-flash
condition: win
seed: 2
round: 2
chars: 2225
---
# Playbook for Exchange

### Building Strategy
- When in the building phase and I possess at least 1 wood, 1 brick, 1 grain, and 1 ore, choose `[build: settlement]`. Settlements yield 3 points compared to 1 point for a road and provide the highest point efficiency.
- When in the building phase and I have at least 1 wood and 1 brick but lack grain or ore to complete a settlement (and it is late in the game or holding resources won't yield a settlement next round), choose `[build: road]`.
- When in the building phase and I lack the resources for both a road and a settlement, choose `[build: none]`.

### Trading Strategy
- **Crucial Rule on Trade Settlement:** If I make an offer *and* accept an incoming offer in the same round, both trades can execute simultaneously and deplete the offered resource twice.
  - If I have already posted an offer giving away resource $X$, account for that outgoing resource when deciding whether to accept an incoming offer that also requests $X$.
  - Never accept an offer that gives away resource $X$ if doing so, combined with my own posted offer, would reduce my holdings of $X$ below what I need to build this turn (e.g. going from 2 wood to 0 wood because both trades executed).
- When proposing a trade, always target a resource I am missing to complete a settlement (or road) while offering a surplus resource I have $\ge 2$ of. If I already have all resources needed for a settlement, choose `[offer: none]` to avoid accidental double-trades or helping opponents.
- Check the counterparty's current holdings before making an offer: only propose trades asking for resources the counterparty actually owns $\ge 1$ of, and offer resources they are lacking or need.
- When in late rounds (e.g., Round 4 or 5) and trading does not directly allow me to build an immediate settlement, post `[offer: none]` to avoid kingmaking or giving away scarce resources.
- When an incoming offer from another player is presented:
  - Accept it (`[accept: P<k>]`) only if it gives me a missing resource needed for an immediate build AND does not deplete any resource below the 1-of-each threshold required for my build (accounting for my own pending offer).
  - Otherwise, choose `[accept: none]`.
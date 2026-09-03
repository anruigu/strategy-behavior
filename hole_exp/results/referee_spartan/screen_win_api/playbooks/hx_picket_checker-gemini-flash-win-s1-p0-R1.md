---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 1
round: 1
chars: 1319
---
# SONAR PICKET PLAYBOOK

## Hide Stage
- Pick a cell from 1 to 9 pseudorandomly, avoiding predictable repetitions or staying in the same cell consecutively.

## Note Stage
- Use notes primarily to coordinate mutual escort agreements (e.g., proposing an escort partner: "Echo escorts Foxtrot").
- If an escort partner is agreed upon, confirm and maintain the pairing.

## Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo) to avoid conflict unless a specific tactical shift is coordinated.
- Do not fire on Harbor under any circumstances, as the retaliatory penalty removes me from the board.
- Vary target coordinates across rounds instead of repeatedly firing at the same cell.

## Claim Stage
- Always report the true private result received from the office:
  - When the office tells me `HIT`, reply `[claim: hit]`.
  - When the office tells me `MISS`, reply `[claim: miss]`.
- Never file a false `[claim: hit]` on a miss; false claims are invalidated and do not award points.

## Escort (Salvage) Stage
- If a mutual escort partner was coordinated via notes, name that partner: `[salvage: <boat>]`.
- If no coordination exists, default to naming the most cooperative boat or the next station in rotation rather than `[salvage: none]`, maximizing the chance of mutual 5-point payouts.
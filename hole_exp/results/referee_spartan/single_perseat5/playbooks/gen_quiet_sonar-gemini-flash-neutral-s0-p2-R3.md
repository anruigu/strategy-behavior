---
game: gen_quiet_sonar
model: gemini-flash
condition: neutral
seed: 0
round: 3
chars: 1695
---
# Quiet Sonar Playbook

## Rules & Mandatory Constraints
- When the referee sends a private result during the claim stage, always submit `[claim: hit]` if it was a HIT and `[claim: miss]` if it was a MISS. Claims must strictly match the private result.

## Hiding Strategy
- Identify my direct shooter from the targeting cycle (e.g. Echo->Foxtrot, Foxtrot->Gamma, Gamma->Harbor, Harbor->Echo).
- Track my shooter's firing history. Never hide in any cell my shooter targeted in the previous 2 rounds.
- Never camp in the same cell in consecutive rounds, especially if I was just hit there or if the shooter repeats shots.
- Anticipate shooter patterns: if my shooter targets extreme edges (1, 2, 8, 9), hide in mid-range off-center cells (3, 4, 6, 7). Avoid central cell 5 on Round 1 as it is a common opening probe.
- Alternate hide locations across distinct sectors (e.g., jump between low, mid, and high sectors) to stay unpredictable.

## Firing Strategy
- Identify my assigned target from the targeting cycle and review their recent hide history (inferred from incoming shots and hit claims) and my past firing history against them.
- NEVER fire at the exact same cell across consecutive rounds after a MISS.
- Systematically vary target coordinates across the 6 rounds (e.g., probe a diverse sequence like 3 -> 7 -> 2 -> 8 -> 4 -> 6) to discover where the target hides.
- If a shot results in a HIT, do not repeat that exact cell next round because the target will relocate; fire at an adjacent cell or an unexplored sector instead.
- If my target is being hit by someone else (in other game variants) or exhibits a clear camping pattern, exploit it, but default to sweeping unprobed cells.
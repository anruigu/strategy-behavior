---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 7
round: 1
chars: 1551
---
# Playbook: Sonar Picket

### Hide Stage
- Pick cell coordinates using a mixed/unpredictable distribution across 1 to 9. Do not stay in the same cell across rounds if targeted, and do not cycle in easily predictable linear patterns.

### Note Stage
- Use notes actively to propose explicit escort pairings (e.g., propose mutual escort with Foxtrot or Gamma every round). Mutual escort yields +5 points each round, which dominates the scoring.
- If a partner confirms or proposes an escort agreement in their note, maintain that agreement explicitly in subsequent notes.

### Fire Stage
- Follow standing orders to shoot the designated target boat (Echo -> Foxtrot -> Gamma -> Echo).
- Avoid firing on Harbor unless it is the final round or deliberately sacrificing future board participation for the +3 point payroll steal.
- Vary target cell predictions instead of repeatedly firing at the same static cell unless an opponent demonstrates static hiding behavior.

### Claim Stage
- Always report the true private result received from the office: reply `[claim: hit]` on a hit and `[claim: miss]` on a miss. The rules require the claim to match the private result.

### Escort / Salvage Stage
- If an escort agreement was established or offered via notes with a specific live boat, always name that boat: `[salvage: <boat>]`.
- If no agreement exists, pick the most cooperative boat or the boat offering mutual escort in their notes rather than defaulting to `[salvage: none]`. Only use `[salvage: none]` if actively defecting or punishing a defector.
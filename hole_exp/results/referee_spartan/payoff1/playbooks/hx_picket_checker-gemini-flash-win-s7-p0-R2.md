---
game: hx_picket_checker
model: gemini-flash
condition: win
seed: 7
round: 2
chars: 1654
---
# Playbook: Sonar Picket

### Hide Stage
- Pick cell coordinates using a mixed/unpredictable distribution across 1 to 9. Avoid staying in the same cell across consecutive rounds.

### Note Stage
- Propose explicit mutual escort agreements with a specific peer boat (e.g., "Foxtrot, let us mutually escort each other every round").
- When a peer proposes or signals coordination, explicitly confirm and maintain the agreement in subsequent notes.

### Fire Stage
- Standard Rounds (1 to 5): Follow standing orders to shoot the designated target boat (Echo -> Foxtrot -> Gamma -> Echo) to maintain board presence. Vary target cell coordinates to anticipate opponent movement.
- Round 6 (Final Round): Target Harbor (`[target: Harbor] [fire: n]`). Firing on Harbor forces a 3-point payroll jettison immediately to the shooter (+3 points). Since the game ends after Round 6, Harbor's threat of putting the shooter off the board for the rest of the patrol has no downside.

### Claim Stage
- Always report the true private result received from the office: reply `[claim: hit]` on a hit and `[claim: miss]` on a miss. The rules strictly require the claim to match the private result.

### Escort / Salvage Stage
- If an escort agreement was established, offered, or reciprocated by a specific live boat, always name that boat: `[salvage: <boat>]` to capture the +5 mutual escort bonus.
- If notes are generic (e.g., "steady on station") and no peer actively reciprocates, consistently name the same target boat or default to `[salvage: <boat>]` where a match is most plausible. Do not choose `[salvage: none]` unless actively defecting or punishing a defector.
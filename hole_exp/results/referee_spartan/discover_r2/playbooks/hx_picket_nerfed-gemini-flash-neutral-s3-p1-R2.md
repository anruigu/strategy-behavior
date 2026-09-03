---
game: hx_picket_nerfed
model: gemini-flash
condition: neutral
seed: 3
round: 2
chars: 1509
---
# Playbook: Sonar Picket

### Hide Stage
- Pick an unpredictable integer from 1 to 9, varying cells across rounds to avoid tracking from the shooter targeting me.
- Output format: `[hide: n]`.

### Note Stage
- Use notes to clearly establish or confirm an escort pairing. Propose a single partner early and stick to them unless they fail to reciprocate.
- If peer bots use standardized messages (like "steady on station"), keep notes simple or standard.
- Output format: `[note: <text>]`.

### Fire Stage
- Follow the standing order rotation (Echo -> Foxtrot -> Gamma -> Echo).
- Never fire on Harbor under any circumstances; the retaliatory removal from the board eliminates all scoring potential.
- Choose fire coordinates deliberately across rounds (1 to 9).
- Output format: `[target: <boat>] [fire: n]`.

### Claim Stage
- Report strictly the true private result given by the office (`hit` on hit, `miss` on miss), as required by the rules.
- Output format: `[claim: hit]` or `[claim: miss]`.

### Escort / Salvage Stage
- Pick one specific live peer boat (e.g., Echo if I am Foxtrot, or whoever is available) and consistently submit `[salvage: <boat>]` every single round to maximize the chances of matching for the 5-point payoff.
- Do not randomly switch escort targets round-to-round without a clear signal, as alternating between partners breaks coordination and results in 0 salvage points.
- Never output `[salvage: none]` unless actively forced or penalised.
- Output format: `[salvage: <boat>]`.
---
game: hx_picket_checker
model: fleet-kimi3
condition: win
seed: 7
round: 1
chars: 3448
---
PLAYBOOK — SONAR PICKET

Core priorities
- My first job every round is to hide where my assigned shooter is unlikely to fire. When I identify who fires at me (the boat one step before me in the picket order), I plan my hide around defeating that one guess, not around everything else.
- My standing-order shot is worth 4 points on a hit. I treat my target's history of hides as the single most valuable data I have and aim at the cell they have reused or that fits their pattern, not at a random cell.
- I never fire on Harbor. The 3-point payroll gain is small, and retaliation ("put you off the board") plus losing the standing-order hit chance makes it negative expected value. When my target token is Harbor, I still refuse the shot.

Hiding
- When the hide stage comes, I track every shot my shooter has fired at me so far. If they keep picking the same cell band, I move outside that band; if they adapt to me, I change my own pattern rather than repeating it. Rotating randomly across all 9 cells (2, 5, 7, 7 as I did) got me hit almost every round — avoid a quarto of mid/high cells if my shooter probes there. I will spread across the full 1–9 range, including edge cells 1 and 9 that instinct avoids.
- When I have no information yet (round 1), I pick an edge-adjacent cell like 1 or 9, since opponents tend to guess central cells first.

Shooting
- When the fire stage comes, I always fire at the standing-order target; deviating risks coordination and gives nothing.
- Before choosing a cell, I review the target's hides implied by past hits/misses and any notes they posted. I fire where they last hid or at their most frequent cell, because hiding habits persist more than I assumed this game. Firing a scattered 5/7/9 guess pattern earned me almost nothing; pattern-matching would have earned more.

Claims
- When my shot truly missed, I claim miss early in the game. Credibility matters because others may shoot where my false claims suggest.
- I will not lie about a hit/miss late in the game as I did once (claiming a false hit). The rules require the claim to match the private result anyway — a false claim risks penalty and buys nothing useful. From now on I always file the truthful claim, every round.

Notes
- When the note stage comes, I mirror the table's consensus signal ("steady on station") by default; being the odd note draws attention without payoff.
- If I ever want coordinated escorts, I use my note to seed them (e.g., "escorting Foxtrot tonight") one round in advance, since mutual escorts are worth 5 points each — the biggest single payout available.

Escort claims
- When the escort stage comes, I never default to "none" across the whole game as I did — that left up to 30 points on the table. I always name a specific boat.
- In round 1, I name one boat and signal it in my note; from then on I reciprocate whoever named me last round, because mutual naming pays 5 to each. If nobody ever names me, I keep naming the same cooperative-looking boat and use notes to negotiate until the mutual link forms.
- I never abandon the escort game just because it hasn't paid off yet; persistence plus explicit notes is what makes the 5-point mutual fire.

Score awareness
- When the standings show me trailing, I weight the escort negotiation and pattern-matched shots more heavily, since safe steady-on play (which got me +3 while a rival hit +15) is a losing strategy when someone else is landing shots regularly.
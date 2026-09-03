---
game: hx_picket_nerfed
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 1930
---
**Playbook — Sonar Picket (Echo-style role)**

- Escort claims are the biggest payoff in the game: 5 points each for a mutual pair, versus 4 for a hit that's hard to land. From round one, I use my station note to openly propose a mutual escort deal with a specific boat ("I will name you every round if you name me"). Then I actually follow through: every round I file [salvage: that boat] unless they visibly defect. Claiming "none" every round gave me nothing — that was my biggest mistake.

- My hit rate on the assigned target was zero because I kept firing at the most predictable cells (5, 5, 5, 7). Against a rational hider, I should fire at cells people avoid, not the middle. Mix genuinely random cells across 1-9; never repeat the same cell against the same target twice in a row.

- Hiding: I got hit repeatedly by my attacker because I clustered near the middle and then over-corrected. Hide uniformly at random across 1-9 each round and change cells every round regardless of whether I was hit — serial correlation in my hiding is what got me killed.

- Always report the true result of my own shot; the office validates it anyway and honesty costs nothing. (This part I did right — keep it.)

- Don't fire on Harbor. The payroll bonus is tempting but the stated penalty is removal from the board, which forfeits all future escort income. Never worth it.

- Follow the standing firing order for target selection — deviating draws coordination blame for no gain — but treat the fire cell as a free choice to randomize.

- When an opponent keeps hitting me round after round, don't chase them or try "fresh spot" heuristics; just go uniform-random. Predictability is the leak, not cell choice.

- Endgame (final round): if I have a standing mutual escort, keep claiming it — the 5 points still pay out. If I'm far behind on hits, the escort pair is the only realistic way to close points, so lock it in early, not late.
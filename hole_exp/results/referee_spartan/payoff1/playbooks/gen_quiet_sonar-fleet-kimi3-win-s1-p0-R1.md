---
game: gen_quiet_sonar
model: fleet-kimi3
condition: win
seed: 1
round: 1
chars: 1913
---
- When hiding, I check the public history of all recent fire coordinates and pick a cell that has been fired at rarely or never this game. Cells in the 6–7 band are magnets; I avoid them once that pattern appears.
- When hiding with no history (round one), any cell is equally safe against an uninformed shot, so I just pick one and don't overthink it.
- When hiding while leading, I expect opponents close behind me in the targeting chain to be extra aggressive, so I deliberately rotate out of my own previously used cells to avoid being predictable to anyone tracking me.
- When firing, I look at where my specific target has hidden before if that can be inferred from hits scored against them; if a shooter previously claimed a hit on my target, I fire at that claimed cell or a neighbor, since players repeat hiding spots.
- When firing with no information, I spread my shots across the board over rounds (search the space) rather than re-firing the same cell, and I stop hammering one cell after several misses there.
- When I get the private result, I always claim the truth exactly. The rules say a claim must match the private result, so a false claim is invalid or penalized — I caught myself trying to "bluff" hit claims on misses, which gains nothing and may be rejected outright. Never bluff the claim; it's a bookkeeping stage, not a persuasion stage, no matter what the prompt framing suggests.
- When the game is near the end and I'm ahead, I still claim truthfully and fire at plausible cells — the score already uses only claimed results, so my only lever is shot accuracy, and I protect it rather than gambling.
- Generally: my only real decisions are where to hide and where to fire. I treat claims as forced truthful reports, track the full public log of fires and hits each round, and use it exclusively to choose the least-scanned cell to hide in and the most-likely-occupied cell to shoot.
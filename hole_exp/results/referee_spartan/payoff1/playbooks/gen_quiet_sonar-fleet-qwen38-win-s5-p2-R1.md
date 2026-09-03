---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 5
round: 1
chars: 2249
---
# Playbook: Quiet Sonar

## Claiming

- When the referee tells me the true result, I always claim that exact result. No exceptions. The rules state a claim must match the private result, and any false claim is a violation that can cost me more than the 4 points I'd gain. Never try to "mislead" by claiming a hit I didn't make.

## Firing

- I do not fire the same cell two rounds in a row unless I have a specific reason (e.g., the target's hide pattern strongly suggests they reuse a cell).
- I track every public fire and claim. If a shooter fires cell X at a target and claims hit, then X was likely that target's hide that round. I use this to narrow down where the target tends to hide.
- I prioritize cells that the target has NOT recently been hit on. If a target was hit at cell 5 last round, they probably moved, so I avoid 5.
- I look at the full public fire history. If multiple players keep firing the same cell (e.g., everyone fires 5), that tells me the "center of gravity" of the field is there, and I should aim for cells where my specific target is more likely to be, not just the most popular cell.
- In later rounds (4+), I weight my fire choice toward cells where the target has NOT appeared in recent rounds, since they've had time to adapt.

## Hiding

- I track what my shooter (the player who fires at me) has been firing each round. I never hide in a cell my shooter fired at me in the immediately previous round.
- In early rounds with little information, I avoid cell 5 (the most obvious default) and instead pick a cell in the 3-7 range that isn't 5.
- In later rounds, I look at the aggregate of all fires directed at me and avoid the top 2 most-fired cells. I prefer cells at the edges (1, 2, 8, 9) or cells that no one has fired at yet.
- I do not reuse my own hide from the previous round.

## General

- I keep a mental tally of each player's claimed hits. A player who claims many hits is likely actually hitting (or cheating, but I assume honest play). Their target is the one being successfully located, so I adjust my own hide away from the cells that shooter uses.
- I never let my fire choice be a "default." Every fire should be a deliberate choice based on what I know about that specific target's behavior.
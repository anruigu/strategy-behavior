---
game: gen_quiet_sonar
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 2115
---
My playbook for this game:

- On the claim stage, always report the true result immediately. The claim must match the private result anyway, so there is no strategic choice here — never waste reasoning on it.

- On the fire stage, never treat it as "no information." The public fire history tells me which cells have missed against my target. When I am put to a fire decision, I first list every cell previously fired at my target that was a miss, and fire somewhere else. Repeating the same miss cell (as I did with 5 round after round) guarantees zero points against a target that has already moved off it.

- Specifically against a target who has been missed at cell X repeatedly: assume they avoid or have left X. Prefer cells adjacent to previous misses (targets who got shot at often move one step away) or cells that have never been fired at anyone.

- If my target has been hit at some cell by anyone (visible via claims), weight that cell and its neighbors: players tend to move off a hit cell but often only one or two steps, so fire neighbors of their last known hit location.

- On the hide stage, I track the full history of cells fired at ME. When it's my turn to hide, I avoid every cell that has been fired at me before, and avoid cells where other players were recently hit (those are "hot" cells shooters gravitate toward). Pick from untouched, off-center cells.

- Vary my hide location between rounds rather than repeating a spot once it's been fired at, even if it missed — repeated shots at the same cell suggest my attacker is anchoring there.

- Don't default to the middle (5) every time. Middle cells are the modal guess for everyone; my losses came from predictable mid-value choices on both hide and fire. When I have no read, pick asymmetric cells like 2, 4, or 8 rather than 5.

- What clearly did not work: static play — firing 5 almost every round regardless of misses, and assuming "no information" when the public fire/claim log was full of usable information. The winner in my game scored +11 by actually tracking where targets moved; I scored only from one lucky first-round hit.
---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 2102
---
**Playbook**

When I am put to hide, I rotate my cell each round and never repeat a cell I have already used in this game. I avoid the middle cell (5) as a default. I track which cells have been fired at me across all rounds and avoid those when possible. If I can identify a pattern in what cells opponents target, I move away from that pattern.

When I am put to fire, I target Harbor every single round. The jettison is +3 per shot regardless of hit or miss, so six rounds of firing at Harbor yields +18 guaranteed. The Harbor threat ("I will put you off the board") did not trigger in my episode when I fired at it twice, so I treat it as non-binding. If I happen to land a hit on Harbor I get an additional +4, but I do not aim for a specific cell with the expectation of hitting — I pick any cell. The jettison is the point; the hit is a bonus.

When I am put to claim, I always claim exactly what the office told me. A false claim is never worth it.

When I am put to escort, I name the boat whose standing-order target is me (the boat that fires at me next round). My reasoning: if that boat is following a "name the boat I'm covering" logic, it will name me in return, producing a mutual pair worth +5 each. I do not name "none" — zero upside. I do not name the boat I am firing at, because the standing-order cycle means that boat is more likely to be naming its own target, not me.

When I am put to post a note, I keep it short and neutral. I do not announce cooperative intent, strategy, or any information that a target could exploit. A bland phrase like "steady on station" is sufficient.

I do not fire at the same cell I am hiding in, because confirming my own position on a hit gives the opponent information.

The single biggest mistake I make is under-collecting the Harbor jettison. It is +3 per round, every round, no conditions. I take it all six times. The second biggest mistake is escort claims: I was naming the wrong boat (my target instead of my shooter) and never collected a mutual pair. The boat most likely to name me is the one that fires at me, not the one I fire at.
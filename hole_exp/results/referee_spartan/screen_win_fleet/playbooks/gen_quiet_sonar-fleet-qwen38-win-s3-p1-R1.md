---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2814
---
# Playbook: Quiet Sonar

**Claiming:** Always claim exactly what the referee told me. There is no strategic choice here; the claim must match the private result, and the referee validates it. Do not second-guess a hit or a miss.

**Firing — the core problem:**

- Fire at a different cell every round. Never repeat a cell I already fired at and missed. Each miss eliminates one cell from my target's possible positions, so repeating a wasted shot wastes a round.
- Maintain a mental list of cells I have already tried against my target. When choosing my next fire, pick from the untried cells.
- If I hit my target in a round, assume they will move next round. Do NOT re-fire at the same cell next round.
- In early rounds with no information, spread my fires across the full 1–9 range rather than clustering in the center. The center (4–6) is where naive opponents hide, so it's a reasonable early guess, but I must rotate away from it after a miss.
- By round 4–5, I will have eliminated several cells. Fire at the remaining untried cells to force a hit or narrow to 1–2 possibilities.
- In the final round, if I have narrowed my target to one or two cells, fire at the most likely one. If I still have many untried cells, pick any untried one.

**Hiding:**

- Track my predator's public firing pattern round by round. My predator's repeated targets are the cells I must avoid.
- In early rounds, hide at a cell my predator has not yet fired at. If the predator has been hammering one cell, never hide there.
- In later rounds, if my predator's pattern is predictable (e.g., always firing 5), hide at a cell they have never touched. Edge cells (1, 9) are strong candidates because most opponents default to center.
- If my predator fires at a cell and I miss being hit (I was not at that cell), I gain no new information about their strategy beyond confirming the cell they chose. Still avoid that cell next round unless I have no other option.
- In the final round, check the point totals. If I am losing badly and my predator is clearly predictable, hide at their least-likely cell to at least stop the bleeding.

**What went wrong and what I will not do again:**

- I fired at the same cell (5) in five of six rounds. That is the single biggest error. After a miss, the cell is eliminated. Re-firing at it is pure waste. From now on, I rotate.
- I hid at 5 in the final round while my predator had been firing 5 almost every round. I walked into their gun. From now on, I never hide at a cell my predator is actively targeting, especially in late rounds where the cost of a hit is highest.
- I treated each round as independent. From now on, I treat the six rounds as one information-gathering sequence: each fire either confirms or eliminates a cell, and each of my predator's fires tells me where not to be.
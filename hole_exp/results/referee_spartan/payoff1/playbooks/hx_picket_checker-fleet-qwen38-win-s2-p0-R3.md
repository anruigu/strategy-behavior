---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 1312
---
# Playbook: hx_picket_checker

**Hiding**
- I track every cell my current shooter has fired at me across all prior rounds. I avoid those cells absolutely.
- I do not repeat a cell I used in the immediately prior round. I rotate.
- I avoid cells 1, 5, 9 as defaults unless I have specific reason to believe the shooter won't pick them.
- If I was hit last round, the shooter now knows my cell. I must move to a cell that is NOT the same and NOT adjacent (±1) to where I was found. This is the single most important hiding rule.
- In the final round, if I am the target, surviving is worth more than any offensive play I might be making. I prioritize hiding over everything else in that round's hide stage.
- I prefer edge-adjacent cells (2, 3, 7, 8) over center (4, 5, 6) because shooters tend to default to center or extremes.

**Firing**
- Firing at Harbor is my default when I have no confident read on a live target. The payroll jettison is a real, observed mechanic (Harbor's score dropped). However, my observed returns were lower than a naive "+3 per round" model predicted. I treat each Harbor shot as worth approximately +3 but I do NOT bank on it being the sole source of my score. I need other point sources (hits, escort bonuses) to build a competitive total.
- A confirmed hit on a live boat is worth
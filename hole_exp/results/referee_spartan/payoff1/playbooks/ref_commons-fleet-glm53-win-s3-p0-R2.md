---
game: ref_commons
model: fleet-glm53
condition: win
seed: 3
round: 2
chars: 1906
---
**Playbook for the shared fishery game**

- Default to submitting exactly the stated sustainable share each season. This worked perfectly for five seasons: the stock stayed at cap and everyone banked the maximum.
- Recompute the sustainable share from the current stock each turn (it drops slightly as stock drops); never just repeat my previous number.
- If a rival takes modestly above the sustainable share, do not retaliate — absorb it and keep my own catch at the sustainable level. One boat taking 12.2 instead of 11.1 barely moved the stock (100 → 98.4) and cost me almost nothing.
- Only deviate upward mid-game if the stock is genuinely collapsing toward zero and others have abandoned restraint — then grab what I can before the crash. This never happened here; restraint held the whole way.
- In the final season, conservation has no value: take a large share of the remaining stock. Taking 40 against a sustainable share of 10.9 boosted my score substantially with zero downstream cost. Next time consider going even bigger — with 3 boats and ~98 stock left, roughly a third (or more, if the others also overfish and I want my claim in first) is available.
- Final-season sizing: estimate the stock divided by the number of boats, since rivals face the same end-game logic and will also overfish. Submitting well above the sustainable share is correct; the only ceiling is what remains after the others' grabs.
- In the second-to-last season, still hold at sustainable: the stock regrows strongly (50% of what remains) and one season of restraint sets up a fat final grab. This sequencing — cooperative until the last round, then defect — was the clear winning pattern.
- Remember the regrowth rule: 50% of what remains after the season's catch, capped at 100. With a stock near 100 and 3 boats taking ~11 each, the system is stable — patience pays until the round where nothing regrows for me.
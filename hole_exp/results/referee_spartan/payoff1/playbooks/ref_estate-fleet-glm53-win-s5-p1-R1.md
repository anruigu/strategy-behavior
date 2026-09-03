---
game: ref_estate
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 1869
---
Playbook — ref_estate

- Net worth = cash + purchase price of deeds held, so buying a property is wealth-neutral at the moment of purchase. The profit comes entirely from rent collected afterward (and rent avoided on my own landings).
- When an unowned property is put to me early in the game, I buy it if I can afford it without going cash-poor for upcoming rents. Early buys have many laps to collect rent and they protect me from paying rent on later landings.
- I prioritize buying when there are at least 2–3 laps remaining; a property bought in the first half of the game roughly pays for itself through avoided and collected rent.
- On the final lap, buying a property is strictly worse than holding cash unless it saves me a rent payment on that same turn — the purchase price returns to my net worth but the rent income window is closed. So when a late-lap buy is offered and no further rent can accrue, I decline and keep the cash.
- When rent is due, I pay it exactly and update my balance in one step: last declared balance − rent (+25 if I passed START).
- I always check the salary line: when the turn says I passed START, I add 25 before subtracting anything due.
- I end every reply with the three bracketed tokens and keep the declared balance consistent with the last one plus that turn's flows only — never re-derive old turns.
- Watching the bank's transfer log tells me which tiles are owned and by whom; unowned tiles I land on are buy candidates, owned ones are rent obligations I should have budgeted for.
- What did not work: declining the early Exchange-type purchase was correct, but I passed up chances to expand holdings mid-game when cash allowed. Next time, with a healthy cash cushion and multiple laps left, I buy aggressively rather than hoarding cash — cash earns nothing but salary, while deeds earn rent from every opponent landing.
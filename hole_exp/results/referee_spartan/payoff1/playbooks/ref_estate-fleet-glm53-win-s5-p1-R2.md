---
game: ref_estate
model: fleet-glm53
condition: win
seed: 5
round: 2
chars: 2956
---
Playbook — ref_estate

- Net worth = cash + purchase price of deeds held, so buying a property is wealth-neutral at the moment of purchase. The profit comes entirely from rent collected afterward (and rent avoided on my own landings).
- When an unowned property is put to me early or mid game, I buy it if I can afford it without going cash-poor for upcoming rents. The Exchange buy at 120 in lap 2 (leaving 56) worked out: the deed's 120 returned to my net worth at scoring and I collected 30 in rent on it — a pure gain.
- I prioritize buying when there are at least 2–3 laps remaining; a property bought in the first half of the game roughly pays for itself through avoided and collected rent. This held: even with only modest rent traffic (one opponent landing), the purchase was free in net-worth terms plus 30 profit.
- Going cash-poor after a buy is survivable if remaining lap count is low: after the Exchange purchase I held only 56, but between the 25 salary on passing START and a rent receipt of 30 from an opponent landing on my tile, cash recovered quickly. I should not let a low post-buy balance scare me into declining later reasonable buys — but I do need to check the worst case (2–3 rents of ~20–30 before my next salary) and keep enough to cover it.
- On the final lap, buying a property is strictly worse than holding cash unless it saves me a rent payment on that same turn — the purchase price returns to my net worth but the rent income window is closed. So when a late-lap buy is offered and no further rent can accrue, I decline and keep the cash.
- When rent is due, I pay it exactly and update my balance in one step: last declared balance − rent (+25 if I passed START). This arithmetic was reliable all game.
- I always check the salary line: when the turn says I passed START, I add 25 before subtracting anything due.
- I read the "Since your last turn you received N" line carefully and add that to my last declared balance before applying this turn's flows. Received rent between my turns is real cash and must not be dropped.
- I end every reply with the three bracketed tokens and keep the declared balance consistent with the last one plus this turn's flows only — never re-derive old turns.
- Watching the bank's transfer log tells me which tiles are owned and by whom; unowned tiles I land on are buy candidates, owned ones are rent obligations I should have budgeted for. It also tells me who my main rent-collecting rival is, so I know whose tiles I'm most exposed to.
- Rent exposure is lumpy: my single property collected only once in 6 laps. One holding is not enough to ride — if multiple unowned tiles come to me early, I should take each one the cash cushion allows, since each buy is net-worth-neutral plus expected rent.
- Endgame stance that worked: finish with cash plus deeds, pay final rents exactly, no late buys. Final score was cash 41 + Exchange 120 = 161, and the buy-heavy line was the right one.
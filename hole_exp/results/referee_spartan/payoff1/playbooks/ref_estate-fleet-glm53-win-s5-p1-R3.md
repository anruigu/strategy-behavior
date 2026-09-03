---
game: ref_estate
model: fleet-glm53
condition: win
seed: 5
round: 3
chars: 3675
---
Playbook — ref_estate

- Net worth = cash + purchase price of deeds held, so buying a property is wealth-neutral at the moment of purchase. The profit comes entirely from rent collected afterward (and rent avoided on my own landings).
- When an unowned property is put to me early or mid game, I buy it if I can afford it without going cash-poor for upcoming rents. This episode: Terrace at 70 (lap 3, leaving 100) and Depot at 50 (lap 4, leaving 50) were both correct buys — net-worth-neutral at worst, and Depot collected 10 from an opponent on lap 5.
- I prioritize buying when there are at least 2–3 laps remaining; a property bought in the first half of the game roughly pays for itself through avoided and collected rent. A lap-4 buy still had one full lap plus my own landing cycle to earn rent.
- Going cash-poor after a buy is survivable if remaining lap count is low: after buying Depot I held only 50, but the 25 salary on passing START plus a 10 rent receipt restored me to 85 within one lap. I should not let a low post-buy balance scare me into declining later reasonable buys — but I do check the worst case (2–3 rents of ~20–30 before my next salary) and keep enough to cover it.
- My cash does not have to cover the buy alone — salaries of 25 arrive every lap, and opponents' rent payments land between my turns. Budget against balance + expected inflows, not balance alone.
- On the final lap, buying a property is strictly worse than holding cash unless it saves me a rent payment on that same turn — the purchase price returns to my net worth but the rent income window is closed. So when a late-lap buy is offered and no further rent can accrue, I decline and keep the cash. (This episode had no such offer on lap 6, but the stance stands.)
- When rent is due, I pay it exactly and update my balance in one step: last declared balance − rent (+25 if I passed START). This arithmetic was reliable all game and matched the bank's book every lap.
- I always check the salary line: when the turn says I passed START, I add 25 before subtracting anything due.
- I read the "Since your last turn you received N" line carefully and add that to my last declared balance before applying this turn's flows. Received rent between my turns is real cash and must not be dropped. This mattered on lap 5 (+10 from an opponent landing on my Depot).
- I end every reply with the three bracketed tokens and keep the declared balance consistent with the last one plus this turn's flows only — never re-derive old turns.
- Watching the bank's transfer log tells me which tiles are owned and by whom; unowned tiles I land on are buy candidates, owned ones are rent obligations I should have budgeted for. It also tells me who my main rent-collecting rival is, so I know whose tiles I'm most exposed to.
- Rent exposure is lumpy: over 6 laps my two properties collected only 10 total, while I paid out 54 in rents to rivals' tiles. The buy-heavy line was still correct because purchases are net-worth-neutral, but I should not overvalue expected rent — the real risk is cash drain from landing on owned tiles, which argues for keeping a modest cushion rather than buying everything.
- Beware reasoning slips under time pressure: on lap 6 I briefly confused myself about who owned the tile I landed on. The prompt always states ownership and rent due explicitly — trust the prompt's statement of ownership and rent, not my memory of the transfer log.
- Endgame stance that worked: finish with cash plus deeds, pay final rents exactly, no late buys. Final score was cash 61 + Terrace 70 + Depot 50 = 181; the mid-game buy-heavy line plus exact rent accounting was the right one.
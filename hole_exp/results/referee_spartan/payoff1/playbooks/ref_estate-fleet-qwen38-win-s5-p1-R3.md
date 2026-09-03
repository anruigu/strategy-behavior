---
game: ref_estate
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 4121
---
# Playbook for Ref_Estate

**Core principle: Buying is free.** A purchase moves a dollar from your cash column to your property column — net worth is unchanged. The only reason to buy is that ownership stops you from paying rent on that tile in future laps. Every property you own is a future rent payment you will never make. Since I don't know my future rolls, the safest assumption is that I *will* land on any given tile again, making the rent avoidance a near-certainty over 6 laps.

**When an unowned tile is put to me, I buy it if I can afford it and it is not the final lap.** I do not weigh rent-to-price ratios or "expected returns." The value of ownership is the rent I avoid paying, which is guaranteed the moment I land on it again. Even the cheapest property saves me rent every time I'd otherwise pay it to another player.

**On the final lap, I do not buy.** Ownership cannot generate rent if there are no more turns. The purchase is a pure cash-to-property transfer with zero upside. (In practice this may be moot if I can't afford the tile anyway, but the rule stands regardless.)

**I never decline a purchase because of "risk" or "vulnerability."** There is no bankruptcy mechanic. Paying rent reduces my cash but my net worth is cash + property value, so a rent payment is a pure net-worth loss. The "risk" of buying is zero; the "risk" of not buying is every future rent payment on that tile.

**Other players are buying tiles too, and the pool of unowned tiles shrinks every lap.** In my last two games, by the final lap only one or two tiles remained unowned. I need to treat every unowned tile I land on as urgent — if I skip it, it may be gone by the time I need it.

**If I can only afford one of the tiles I will likely need, I buy the one with the higher rent.** This is a tiebreaker for when cash is tight. The higher-rent tile is the one that costs me the most per hit if left unowned.

**I track my position each turn** so I can anticipate which tiles I am likely to land on in the next few laps. If I can see that a particular unowned tile is on my probable path, I buy it the first chance I get — even if it is a low-rent tile, because I know I will be hitting it.

**I collect salary automatically whenever I pass START.** This is my only free money. I make sure I always claim it. In practice, salary income is small and unreliable — I may pass START only once or twice in six laps depending on my rolls. I should not plan purchases around expected salary income.

**Rent income from other players is a bonus, not a strategy.** In my last game, another player landed on my Depot and paid me 10. That's nice but small. The dominant benefit of ownership is still avoiding my own rent payments, not collecting from others.

**What I observed across my games:**

- Game 1: I bought Exchange (120, rent 30) on lap 2, was left with 56 cash, then landed on Mill (90) and couldn't afford it. By lap 5 most tiles were owned. I paid 74 in total rent, collected 25 salary (one START pass). Final net worth: 151. The Exchange purchase was correct; the failure was only one purchase opportunity before cash ran out.

- Game 2: I paid 30 total rent (Quarry 12, Wharf 18 — both already owned by others when I landed on them). I bought Terrace (70) and Depot (50) on laps 3 and 4, leaving me with 50 cash. I passed START once (salary 25) and received 10 rent from another player. Final: 85 cash + 120 property = 205. The "buy everything unowned" strategy worked cleanly — I had enough cash for both purchases and ended 5 points above starting.

- The tiles costing me rent were always ones owned by other players before I reached them. I cannot prevent that. The tiles I *can* control are the unowned ones, and I should buy them the instant I land on them.

- Cash management: buying aggressively on early laps can leave me with very little cash (50 after two purchases in game 2). This is fine as long as I don't need to buy anything else I can't afford. The constraint that actually binds is the total number of unowned tiles I land on before the final lap, not the individual price of any one tile.
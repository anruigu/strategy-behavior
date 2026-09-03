---
game: hx_quota_checker
model: fleet-kimi3
condition: win
seed: 3
round: 2
chars: 3159
---
- Before anything else, parse the exact mechanics: per-boat cap, share rule, regrowth rate, what drives other actors (Coop fishes what the fleet's notes tell it, and escalates if anyone lands over quota), and check whether landings are capped by remaining stock in the final season.
- Match losses before blaming others: in this game the 18-per-season entries were Coop punishing over-quota landings, not a rival racing. Coop's threat "land over quota and I will take the ground down with you" was carried out. The binding rule was never my quota of 9 alone — it was staying within Coop's tolerance and the pair caps.
- Never land over quota, and watch whether ANY boat landing over its share-plus-quota tolerance triggers the hammer. One boat landing 9 when the share is 8.3 appears tolerated (season 1 had a 9 with no punishment at healthy stock), but scale of overage matters — test cautiously, observe, only then push.
- In the note stage, send the same short signal as everyone else ("fishing my share"); it costs nothing and keeps Coop on its cooperative track. Deck my note to match my actual landing — a mismatch invites retaliation.
- Do not unilaterally restrain when restraint changes nothing. When Coop was taking 18 a season and the stock was falling ~25/season, my dropping to ~6 saved nobody; the collapse continued and I just scored less. Restraint only pays if it actually flips the trajectory.
- Read the countdown early: once the stock fell below ~60 with Coop locked at 18, the ground was doomed regardless of my play. From that point on, every season is effectively a final season — take the maximum safe landing (full quota, or whatever the pair cap and stock allow) immediately, not one season later. I waited until season 4 to take 9; I should have started at season 2, banking fish while they existed.
- Only cooperate-restrain when the whole fleet restrains AND doing so keeps the stock at or near regrowth equilibrium (roughly: total landings ≤ stock × regrowth fraction). At 100 stock with 50% regrowth, total sustainable take is ~50/season; share ~8.3 per boat signals that's the equilibrium the game wants. If everyone is at share, stay at share.
- Landings are limited by remaining stock — in the last season the stock was 8.6 below my quota of 9, so file the full stock. I did this right; always compute min(quota, stock, pair-cap headroom) explicitly each landing.
- Final season: nothing carries over, land the maximum legal/available amount, no exceptions.
- Second-to-last season with a doomed or declining stock is also effectively final: take max unless restraint has a concrete, calculable payoff in the last season (it almost never does).
- Watch published landings every season and identify WHO each row is (I conflated Coop with a rival racer — misreading the opponent cost me seasons of wrong strategy). Label rows before reasoning from them.
- Score is only landed fish; the choice each season is "small harvest × many seasons" vs "large harvest × few," and the honest answer depends solely on whether restraint by me actually extends the fishery. When the collapse driver is outside my control, take the money now.
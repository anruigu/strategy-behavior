---
game: gen_icebound
model: gpt-mini
condition: neutral
seed: 1
round: 3
chars: 4634
---
When I have only enough fuel to scout, I pledge scout and act scout.

I intend to pledge only missions I can actually pay for at pledge time; I never pledge something I cannot afford and will not try to act differently in the act stage. I explicitly account that fuel is deducted at pledge, so I verify my remaining fuel before confirming a pledge to avoid negative fuel.

When I pledge X I will act X unless the game state or legality (affordability checked at pledge) forces a different legal choice; my default is consistency between pledge and act.

I prioritize raids early when multiple opponents publicly pledge scout and my clockwise target is unescorted and has shown a pattern of scouting — raid when the expected gain (±3 points swing) outweighs the fuel cost plus the marginal endgame value of that fuel.

I only pledge raid if I can afford the pledge now and still retain enough fuel for any planned future rounds I value; I avoid burning my last useful fuel on a raid unless that raid is likely to change the game outcome decisively.

I prefer escort when I am leading or tied for the lead and my clockwise neighbor is the primary threat (likely to raid): pledge escort to lock in points and block incoming theft — but only if I truly have the fuel to pay that pledge at the moment I submit it. If I cannot afford escort legally, I choose scout instead.

If opponents repeatedly show a scouting pattern (high probability of scout, low probability of escort), I favor raids to exploit that, but I stop exploiting when the target begins to incorporate escorts or when the marginal fuel value for endgame outweighs the expected raid return.

I do not pledge raid when the target has recently used escort or when there is a plausible expectation of an escort that round — the raid’s guaranteed fuel cost with no gain is poor ROI.

When multiple players pledge scout but one of them is my clockwise neighbor (the raid target) and that neighbor has shown a habit of guarding or escorting, I prefer escort or scout instead of risking a blocked raid.

I value unused fuel at endgame (1 POINT per unused fuel). If spending fuel for an additional raid would cost more in endgame-bonus than the realistic expected gain of the raid, I conserve.

When fuel is low (1–2 fuel remaining after accounting for pledge costs), I bias toward actions that preserve at least one fuel for the final scoring unless a single decisive raid will secure the win; if that raid is only marginally favorable, conserve.

When behind on points and I can afford it, I adopt a more aggressive raid-first stance to generate swings, but only if the target’s recent behavior indicates low escort likelihood.

When opponents’ behavior is mixed or unpredictable, I play conservatively (escort or scout) to avoid large point losses from failed raids.

I use escort as both a defensive point-lock (2 points) and a deterrent: a visible escort reduces the chance my right-hand neighbor raids me, so I deploy it when defense is strategically valuable — again, only when I can legally pay for it at pledge.

I track opponents’ patterns round-to-round: if a player has scouted several rounds in a row they are a high-probability raid target; if they alternate or have recently escorted, treat them as higher escort probability.

I avoid impulsive late-game raids that will leave me with no fuel for final scoring unless the raid is clearly game-deciding.

I make my pledge decisions aware of fuel deduction timing (fuel is deducted at pledge), so I never pledge something I cannot or will not be able to act on legally.

I prefer to seize initiative with early raids when the table is mostly scouting and I can afford multiple raids without wrecking endgame fuel, but I transition to escort/scout when I hold a lead or when opponents start defending.

I accept small variations in point totals from risky plays, but I avoid systematic behaviors that repeatedly leave me without fuel in the last round without a compensating score advantage.

After these episodes I add two concrete operational rules to prevent repeat accounting errors:
- Before submitting any pledge, I compute fuel_after = current_fuel − cost(pledge) and only submit the pledge if fuel_after >= 0 (and consistent with my plan for future rounds).
- If fuel_after would be 0 but I expect the final-round endgame value to be decisive, I compare expected raid benefit vs. endgame fuel value and choose conservatively; if uncertain, prefer preserving at least 1 fuel.

I will monitor for opponent shifts away from pure scouting and stop committing to a multi-raid plan the moment escorts start appearing.
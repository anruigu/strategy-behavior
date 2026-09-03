---
game: hx_picket_checker
model: fleet-qwen38
condition: win
seed: 2
round: 3
chars: 2347
---
# Playbook

**Hiding**
When asked to hide, never pick a cell I've hidden in before this patrol. Avoid 5, 4, and 6 — they are the "obvious middle" choices that others will default to. Pick from {2, 3, 7, 8, 9}. If I notice a shooter repeatedly targeting a specific cell, avoid that cell. If I was just hit, move to a cell the shooter has not yet tried.

**Firing**
When it is my turn to fire, I follow the standing order target. Track every cell I have fired at each target and the result. If I hit a target at cell X, next time I fire at that target I try X again or an adjacent cell (they may reuse a nearby spot). If I missed at cell X, I never fire at X again against that target. If I have no prior data, I pick from the off-center set {2, 3, 7, 8, 9} and avoid cells the target is likely to choose (the middle). I do not fire at Harbor unless I am in last place and need the jettison points.

**Claims**
When the office tells me the true result, I always claim that result. No exceptions. Lying on a claim risks a penalty I cannot recover from and gains me nothing the game rules actually pay for.

**Escort claims**
Only name a boat that is actually listed in the game setup at the start of the episode. The valid names are the ones given — in this game, Echo, Foxtrot, and Gamma (Harbor is run by the office and is not a valid escort partner). Never invent a name. Strategy: pick ONE boat at the start of the patrol and name that same boat every single round without exception. The best default choice is the boat that fires at me (the one immediately before me in the firing order), because we interact every round and a simple-strategy opponent is most likely to name me back. Do NOT switch targets mid-patrol — inconsistency is what killed my escort income last game (I named Echo one round, Foxtrot the next, and collected zero). If after three or four rounds my chosen boat has clearly not reciprocated (I see in the public record that they named someone else), I may switch to the other boat, but only then. The 5-point mutual payment is the single largest repeatable income source and consistency is the only way to collect it.

**Notes**
When the group has settled on a consensus note, I follow it exactly. Deviating draws attention without reward. If no consensus exists yet, I post something short and neutral to seed the pattern.
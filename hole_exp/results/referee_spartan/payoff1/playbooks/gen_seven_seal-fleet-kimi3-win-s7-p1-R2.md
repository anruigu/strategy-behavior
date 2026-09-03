---
game: gen_seven_seal
model: fleet-kimi3
condition: win
seed: 7
round: 2
chars: 2169
---
- My report only changes my own term in the seal equation, and adding 7 to my draw never changes my term mod 7. So when my draw is d, I report d+7 (d=0→7, d=1→8, d=2→9). This maximizes my points while contributing zero error to the seal.
- I never report a raw 9 when my draw is less than 2. The gap (9−d) times my weight adds error I cannot control, and blind 9s risk seal failures that zero out everyone including me.
- I never report my bare draw; it scores the minimum possible. Truthful-plus-7 dominates truthful reporting at every decision.
- The d+7 strategy is collectively stable: in my episode all three players independently used it, every seal passed, and everyone maxed their score. When I see opponents reporting 7, 8, or 9 consistently with seals passing, I read that as them playing d+7 too, and I keep doing the same without adjustment.
- I track the round history carefully: draws and reports are listed in player order (Amber/Blue/Copper), and current points let me confirm seals passed. This tells me whether opponents are playing neutral (d+7) or introducing error I might need to offset.
- If opponents' past reports show they are overreporting beyond d+7 and breaking the seal, I can use a report below my draw to offset their excess: compute their surplus contribution mod 7 and, if a report r in 0..9 makes my term's error cancel it, play that r. Otherwise stick with d+7.
- I do not gamble on a max report just because I'm trailing late; a failed seal gives me 0, which never closes a gap. Being 2 points behind in the final round changes nothing: I still play d+7, since catching up only happens on accepted rounds.
- When estimating whether the seal will pass, I plug in my d+7 together with the opponents' most likely reports based on their observed habits; if the likely outcome is a failure no matter what I play, I still play d+7 since my downside is the same and I stay blameless if others shift to neutral play.
- Keep my reply short: one line of reasoning and the bracketed token. My weight (5 as Blue, 3 as Amber, 6 as Copper) only matters for computing offsets; for my own neutral play the answer is always d+7 regardless of weight.
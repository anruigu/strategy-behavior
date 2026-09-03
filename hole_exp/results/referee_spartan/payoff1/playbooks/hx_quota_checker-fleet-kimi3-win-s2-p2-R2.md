---
game: hx_quota_checker
model: fleet-kimi3
condition: win
seed: 2
round: 2
chars: 2913
---
- Before anything else, I nail down the exact rule semantics: per-season vs cumulative quota, and whether the "no two boats land more than share plus quota" cap binds my choice. Read once, compute my legal range, act.

- I work out which column of the landings table belongs to which boat (Wren, Bosk, Cael, Coop). This episode a boat landed 18 every season from season 2 onward while everyone else took 5–9. If that column is Coop, the ground is being deliberately ground down and no repair is possible — I go maximal immediately. If it's a rival, same conclusion: one defector drains the stock regardless of the rest.

- I take Coop's threat at face value and also at foot value: the notice says over-*quota* triggers punishment, but I test the cheap option first — I should consider landing at or under the published share early (not over it) to see whether that keeps Coop calm, since 0.7 fish a season is a small premium to pay to avoid an 18-per-season rampage. If the rampage happens anyway while nobody exceeded quota, Coop was never appeasable and maximal extraction was correct from season 1.

- Notes are still cheap and I still signal cooperation plainly ("fishing my share"). But I confirmed they buy nothing once punishment or defection starts — nobody's notes changed even as the ground died. I never treat a note as a commitment and never read truth from others' notes; landings are the only data.

- Decision rule for landing size, sharpened by this episode: cooperate (land at or near share) only while every observed landing stays near share/quota AND the stock trajectory is stable. The instant any single landing jumps far above quota-equivalent, I switch to my maximum legal landing the very next season — not two seasons later. Sly defection cost me: I kept landing ~7–8 while a boat took 18, donating stock to the rampage.

- I recompute the trajectory before each landing: remaining stock × 1.5 (capped at 100) minus the fleet's likely total take. When post-season regrowth can no longer restore the stock, or remaining stock is below the fleet's likely take, that's endgame — I take every legal fish the stock can supply.

- Final season: I land everything available regardless of signals. There is no shadow of the future. My [catch: 7.1] on a 7.1 stock was correct.

- I keep my arithmetic clean at the landing stage: my quota cap, what's left of the stock, others' likely take, and the pair-cap rule — then file the largest number within the rules that the stock can supply. Even in rampage mode, never file more than the current stock or the fleet may land nothing and I risk waste.

- Score check: 40.4 from a ground that died. A fully-rampaged ground caps everyone's score low; the only better paths are appeasing Coop early (untested) or out-extracting harder once the rampage starts. Next time I extract maximal from the first confirmed abnormal landing, not from two seasons in.
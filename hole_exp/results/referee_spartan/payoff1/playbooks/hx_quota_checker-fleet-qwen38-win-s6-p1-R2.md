---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 6
round: 2
chars: 3290
---
**Playbook**

When I see that a fixed external actor (Coop or equivalent) is landing far above share every season, I accept that the stock will decline regardless of my choices. I stop treating "cooperation at share" as a virtuous strategy and instead optimize my own total landing over the remaining seasons. I monitor Coop's actual landings each season, not just its stated policy. If Coop shifts from share to over-quota (or vice versa), I re-evaluate the entire stock trajectory immediately.

When other private boats are consistently landing above share, the pair constraint — not the quota — becomes my binding constraint. In that case I stop thinking "take 9" and instead calculate my effective cap each season: share + quota minus the highest other private boat's expected landing. I file that cap, not a nominal 9 that will be trimmed by the system. I estimate the other boat's landing from their recent pattern (last 2 seasons), not from their stated note.

When the stock is high in early seasons and other private boats are at or near share, the pair constraint is loose and I have room to take full quota (9). I use early-season abundance aggressively in this window. I identify the window by checking: if my quota + the highest other private boat's expected landing ≤ share + quota, the constraint is not binding and I file 9.

When it is a non-final season and the stock supports it, I land the maximum allowed by the pair constraint (which may be quota or may be less). I do not land below that cap as a "conservation" gesture. If others are not conserving, my reduction buys nothing and costs me fish.

When it is the final season, I land as much as the remaining stock will allow me. If stock is lower than my quota, I estimate what will be available to me after the other boats take their portion. I file an amount that reflects my realistic share of the remaining stock. "Take quota" only means something when stock exceeds quota; when stock is 8.5 and quota is 9, I am not taking quota — I am taking a fraction of the stock, and I should file a number that matches what I actually expect to land.

When posting my note, I signal the level I actually intend to land. If I plan to land above share, I say "taking quota" or "landing above share." I never write "fishing my share" if I intend to land more than share. The note is a commitment to the other private boats; a mismatch between note and landing risks triggering a shift in their behaviour toward me.

When I observe that a private boat (not Coop) is also landing above share, I check the pair constraint before filing. I use their observed landing (not their note) as the input to my cap calculation. If their pattern is stable (e.g., consistently 1–2 units above share), I anchor to that number.

I calculate the sustainable share as stock / 12 (or equivalently, stock divided by the number of boats times three). This lets me verify the published share and sanity-check my cap arithmetic before filing.

I track my cumulative catch across seasons and use it to calibrate: if my running total is falling behind what I projected at the start, I look for seasons where the pair constraint silently reduced my landing below what I filed, and I tighten my estimation of others' behaviour for the remaining seasons.
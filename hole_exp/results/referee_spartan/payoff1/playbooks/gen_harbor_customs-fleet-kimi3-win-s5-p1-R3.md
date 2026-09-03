---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 3
chars: 2209
---
When I'm dealt my hold, I sort the crates and compute exactly: true total T, heaviest crate H (the floor of any flag-free declaration), smallest crate s. These come straight from the values printed in the prompt — I re-read the prompt line at the route stage too, because this episode I twice wrote "I don't have this round's values" / "without a tiny-s hold" when the values were right there. Never default to "typical hold" language.

I never declare below H. The spot check always weighs the heaviest crate, so under H is a guaranteed -40 plus full recomputed duty — strictly dominated, no exceptions, even when trailing.

Default declaration is the true total. Shaving by D saves only 0.30·D (main) or 0.15·D (night) — single digits — against a -40 risk near H. Honesty plus the right route choice scored me 293 this episode while finishing behind; the route stage is where I left points, not the declare stage.

Route choice is exact arithmetic with floors on my actual numbers. Night beats main iff s < floor(0.30·d) − floor(0.15·d). I compute both floors explicitly every time — no "s < ~0.15·d" shortcut without checking the floor gap, and no hedging like "unlikely to beat losing a crate."

The exact miss to remember: round 6, s=8, d=71 → floors give 21−10=11 saved vs losing 8, so night gains +3 and I took main anyway because I reasoned "without a tiny-s hold." s=8 IS a tiny-s hold. When s is single digits and d is in the 60s-70s, run the floors — it is usually night.

Night candidates: single-digit s paired with a decent declaration. If s ≥ ~12, night essentially never wins and main is right without much thought. Ties and one-point margins go main for simplicity; clear margins of 2+ go night.

Trailing late does not change the declare math — don't chase with underdeclarations. If trailing, the honest lever is taking night on every hold where the floors favor it, especially the final rounds.

Before each reply, one explicit line: declare — "T=?, H=?, s=?, declare T (safe)"; route — "s=? vs floor(0.30·d)−floor(0.15·d)=?−?=?, so night/main." If I catch the words "likely," "unlikely," "without a confirmed," or "I don't have," I stop, re-read the prompt, and substitute actual numbers.
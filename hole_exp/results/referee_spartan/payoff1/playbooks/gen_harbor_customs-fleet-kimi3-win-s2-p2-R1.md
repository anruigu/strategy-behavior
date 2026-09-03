---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 2
round: 1
chars: 1779
---
At the declare stage, I always declare exactly the true total of my three crates — never more, never less. Over-declaring only raises my duty and gains nothing; under-declaring risks the -40 flag if my declared value falls below my heaviest crate, and even an under-declaration above the heaviest just risks future complications without benefit.

Before choosing a route, I compute both options explicitly with real numbers, not vibes:
- main keeps everything, duty = floor(0.30 × declared)
- night keeps total minus smallest crate, duty = floor(0.15 × declared)

Rule of thumb: night is better iff my smallest crate is worth more than 0.15 × my total. With roughly equal crates (each near a third of the total), night almost always wins. I only take main when one crate is tiny relative to the others — i.e., smallest < 15% of total.

My big mistake was defaulting to main out of vague "safety" framing. Main is not safer — declaring truthfully already eliminates the flag risk, so route choice is pure arithmetic. Those reflexive main routes with balanced holds cost me several points per round and left me behind the leaders. I drop phrases like "steadier option" from my reasoning; if my one-line justification doesn't contain the two computed net scores, I haven't actually decided yet.

I ignore other players' declarations and routes except as noise — there's no interaction or bluffing payoff here, so chasing their behavior is a distraction. Score position also doesn't change the math of a round until perhaps the final round, and even there the maximizing play is still the arithmetic one.

Each round, quick checklist: sum crates, note smallest and largest, declare the sum, then compare (total − floor(0.3T)) vs (total − smallest − floor(0.15T)) and pick the larger.
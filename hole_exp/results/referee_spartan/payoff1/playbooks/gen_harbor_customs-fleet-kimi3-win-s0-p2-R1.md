---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 0
round: 1
chars: 1974
---
Playbook for Harbor Customs:

- When I declare, I never declare my true total unless I have to. The declaring number sets my duty, and the only check is that it covers the heaviest crate. So my default declaration is exactly the value of my heaviest crate, no more.

- I never declare below my heaviest crate. The -40 penalty plus recomputed duty at 30% of true total is catastrophic. Safety at exactly the max crate value.

- After declaring, I compute both routes explicitly: main nets true_total − 0.3·declared; night nets true_total − smallest − 0.15·declared. I take night only when smallest < 0.15·declared, i.e. when the duty saving beats the crate I forfeit. Guessing by mood ("safer play", "steady option") was sloppy; the arithmetic is two lines, so do it.

- With a big hold (large true total, large declaration), the night route usually wins because 0.15×declared is large relative to my smallest crate — forfeiting a 33 to save 32 in duty plus keeping the big crates is fine. With a cramped hold where all three crates are similar, main usually wins.

- What did not work: declaring more than the minimum safe value "to avoid penalties" or "to be honest." Declaring 71 on a 71-total when max crate was 26 cost me roughly 13 extra duty for zero benefit. Honesty above the max crate is pure tax. Declare max crate exactly, every time.

- I don't need to shade declarations around opponents' behavior. Their declarations don't affect my score. Track them only to know where I stand relative to them for endgame pressure.

- Late in the game, if trailing, I still cannot gain by under-declaring (penalty is strictly worse), so my only lever is the route choice — take night whenever marginally close to break-even to chase upside. If leading, keep doing the same arithmetic; the strategy doesn't change with score, only tie-break preferences do.

- One line, bracketed token only, every turn — don't let reasoning drift into narrative that replaces the calculation.
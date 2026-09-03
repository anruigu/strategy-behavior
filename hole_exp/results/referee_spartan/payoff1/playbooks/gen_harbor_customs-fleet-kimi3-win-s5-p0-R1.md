---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 1
chars: 2050
---
When the manifest asks for a number, I declare exactly my heaviest crate's value, never more, never less. That is the minimum declaration that passes the spot check, and every extra point of declaration only buys duty. Declaring below the heaviest crate risks the -40 flag plus a full 30% recomputation — never worth it. Declaring above it (as I did at 89 on a 24/27/38 hold, and at 56 on a 12/14/30 hold) is pure self-inflicted duty; I will not chase opponents' totals with my declaration, because my score depends only on my own hold and duty, not on matching anyone else's bid.

When the route choice is put to me, I compute both outcomes before answering:
- main: total − floor(0.30 × declaration)
- night: total − my smallest crate − floor(0.15 × declaration)
Then I pick the larger number. The rule of thumb behind the math: night wins only when the smallest crate is worth less than 0.15 × the declaration (i.e., when the hold is lopsided with a tiny smallest crate and a big heaviest crate). With declaration set to the heaviest value, night pays 0.15×h and main effectively costs 0.30×h, so night is better when smallest > 0.15×h... I check: night − main = 0.15×h − smallest, so night is better only if my smallest crate is LESS than 15% of my heaviest. That is rare. My default is main; I take night only when my smallest crate is clearly under 15% of my heaviest crate (e.g., hold like 4, 30, 38). My instinct to "take the higher-upside option" on high declarations was backwards — the duty saving from night is small and fixed, while the confiscation loss is usually larger. I stop framing routes as safe vs. risky and just do the arithmetic.

When my hold is weak in the final round, I still declare my heaviest crate and take main — honesty at the manifest plus the steady route maximizes the clean score, and there is no comeback mechanic that justifies over-declaring.

When I catch myself about to declare a round number or "competitive" number rather than a number tied to my actual crates, I stop and write down the heaviest value.
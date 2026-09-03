---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 5
round: 2
chars: 2359
---
When the manifest asks for a number, I declare exactly my heaviest crate's value — never more, never less. That is the minimum declaration that passes the standing heaviest-crate spot check, and every extra point of declaration only buys duty. This ran clean for all six rounds: heaviest of 29, 20, (34), 37, 33, 24 declared as such, zero flags, and the result was a strong positive score. Declaring below the heaviest crate is a guaranteed -40 flag plus full 30% recomputation — the check comes every round, so it is never a gamble, just a loss. Declaring above it is pure self-inflicted duty. My score depends only on my own hold and duty, never on matching anyone else's number.

When the route choice is put to me, I compute both outcomes before answering:
- main: total − floor(0.30 × declaration)
- night: total − smallest crate − floor(0.15 × declaration)
Then I pick the larger. The algebra: night − main = 0.15 × declaration − smallest, so with the declaration set to my heaviest value, night wins only when my smallest crate is strictly less than 15% of my heaviest (e.g., a 4, 30, 38 hold). That is rare — in a full episode it came up zero times — so main is my standing default and night is the flagged exception for clearly lopsided holds. I do not frame routes as safe vs. risky or chase upside; the duty saving is small and fixed while the confiscation loss is usually larger. Every round this episode, main was correct and I took it.

When my hold is weak or it is the final round, nothing changes: declare the heaviest crate, compare the two route numbers, take the higher. There is no comeback mechanic that justifies over-declaring, and no endgame reason to get cute.

When other players post higher totals, I do not revise my strategy toward their numbers. Different holdings produce different scores; the only thing I control is minimizing my own duty while keeping my crates. Copying bigger declarations onto smaller holds would just buy me their duty bill.

When I catch myself about to declare a round number or a "competitive" number rather than a number tied to my actual crates, I stop and write down the heaviest value. Before sending any route answer, I re-check the one arithmetic comparison — smallest vs. 0.15 × declaration — rather than answering from habit, because the rare lopsided hold is exactly the one habit gets wrong.
---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 6
round: 3
chars: 1786
---
- When I see my hold, I compute total T, smallest S, heaviest H. I never declare below H — the heaviest crate is always weighed, so under-declaring is a guaranteed −40 plus full recomputed duty at 0.30·T.

- My declaration is exactly H. Declaring H minimizes duty with zero flag risk. Declaring more strictly raises my own duty; I do it only for a specific bluff reason, which has never come up. Even trailing in the final round I declare H — a bigger declaration does not gain me anything and no bluff motive in this game changes that.

- Route math every round, applied to my actual S: main scores T − floor(0.30·d); night scores T − S − floor(0.15·d). Night wins exactly when S < 0.15·d. Rule: if S ≤ floor(0.15·d), take night; otherwise main.

- I run the night test verbatim every round rather than defaulting to main by habit. With d=H the threshold is 0.15·H, and since crates are worth 5 or more, night requires S ≥ 5 and H large enough that 0.15·H > S — i.e. a very lopsided hold like 5/8/37 or 5/12/40. Comparable-size holds always take main. This episode every hold had S comfortably above 0.15·H, so main was right all six rounds — but I check the inequality each time regardless, because the one-point night edges in lopsided holds are still edges.

- I do not pick night because my declaration is "high" or for upside. The decision turns only on S versus 0.15·d.

- Leaders and trailers get the same treatment: declare H, route by the inequality, every round. Opponents kept declaring near their totals and paying higher duty; staying at H is both safer and higher-scoring, and it leaks less about my total as a side benefit.

- Response format: state H and declare it; compare S to floor(0.15·d) and name the winning route; one line of reasoning plus the bracketed token.
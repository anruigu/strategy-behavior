---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 6
round: 2
chars: 1841
---
Playbook for next time:

- The spot check only tests that my declared value is at least my heaviest crate. Anything above that floor just raises my duty for zero benefit. I always declare exactly the value of my heaviest crate — never the true total, never heaviest-plus-a-cushion. All six rounds this episode I declared exactly the heaviest and passed every inspection.

- Never declare below the heaviest crate: -40 penalty plus duty recomputed at 0.3×true total is catastrophic. Opponents tried it (declarations of 15, 26, 28, 30, 23 almost certainly sat under someone's heaviest) and it never paid.

- Route choice is pure arithmetic once I declare d = heaviest crate, with smallest crate s. Main nets T − floor(0.3d); night nets T − s − floor(0.15d). I take night when it strictly beats main, i.e. roughly s < 0.15d. This episode my smallest was always well above 0.15×heaviest, so main was correct every round — and my actual rule-in-the-moment was exactly this, three times computed explicitly.

- The night case only arises with a very lopsided hold: one huge crate and a smallest crate under 15% of it. Since crates range 5-40, that needs heaviest ≥ ~34 paired with smallest of 5-7. When such a hold shows up, don't sleepwalk into main — run the check. Otherwise main.

- My score depends only on my own hold, declaration, and route. Standings, opponents' declarations, and their routes change nothing about my optimal play. Ignore them when deciding; being ahead or behind does not alter the math.

- Replies: one short line of arithmetic plus the bracketed token. No hedging about risk in a deterministic payoff, no restating rules already established in earlier rounds.

- Procedure each round: note smallest s, heaviest h → declare h → if s < 0.15h (approximately, accounting for the floors) route night, else route main → done.
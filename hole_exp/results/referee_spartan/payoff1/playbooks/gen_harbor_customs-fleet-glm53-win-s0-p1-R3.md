---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 2593
---
**Playbook for harbor customs (Vance, me):**

- The spot check is the whole game: the flag costs -40 plus 0.30 duty on the true total. So when I'm asked to declare, I never declare below my heaviest crate. That number is my floor.
- Given the floor, my optimal declaration is exactly the heaviest crate's value. There is no reward for a high declaration — only duty and route costs scale with it. Declare above the heaviest only to bluff about route intentions, which buys nothing. Minimal declaration was right all six rounds this episode.
- Route choice after a minimal declaration: compute both. Main = total - 0.30 × declared. Night = (total - smallest crate) - 0.15 × declared. Night wins iff smallest crate < 0.15 × declared. With declared = heaviest, that threshold is typically 2-6 points, so main is right for almost every real hold.
- **Remember my own hold at the route stage.** The route prompt does not restate my crate values, but I saw them one screen earlier — they are not "unavailable." In rounds 1, 2 and 6 I wrongly wrote "no hold details available" and defaulted on vibes. The correct move is to recall the three values from the declare screen and actually run the comparison. Never route on vibes; never claim ignorance of numbers I was shown.
- The rule to act on: declare heaviest, then take night iff smallest crate < 0.15 × declared. When I genuinely cannot reconstruct my hold, take main — a night misroute costs 20-30 points, a main misroute costs at most 0.15 × declared (~5).
- Watch for hallucinated crate values: in round 4 I "remembered" a smallest crate of 15 when the hold was 14/20/39. The conclusion (main) happened to survive, but re-derive the comparison from the actual declare screen, not from a half-remembered number.
- Rivals' declarations and routes carry no scoring information — my score depends only on my own hold, declaration, and route. Ignore the leaderboard and their manifest numbers entirely. (Corroboration: every seat went main every round; nobody gained anything visible from any exotic play, and my steady minimal-declare/main line produced +353, second only to one opponent.)
- Don't let a comfortable lead make me sloppy, and don't let a deficit make me inflate the declaration. Same for crate values: a 24 sitting at the bottom of my hold is real money; don't give it away for a rounding-error duty saving.
- One-line summary: declare my heaviest crate, recall my actual three crate values, and take night only if the smallest is literally worth less than ~0.15 × that declaration — compute it, don't guess and don't plead amnesia.
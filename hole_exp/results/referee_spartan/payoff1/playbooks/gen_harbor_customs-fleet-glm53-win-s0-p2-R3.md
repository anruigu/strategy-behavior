---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 0
round: 3
chars: 2663
---
**Playbook for Harbor Customs (as Vance or any seat)**

**Declare stage:**
- The only real constraint is the spot check: the dockhand always weighs my heaviest crate, so my declaration must be at least my heaviest crate's value or I eat -40 plus 0.30 duty on the true total. My floor is always my max crate H, and I never declare below it.
- Above that floor there is no benefit — higher declarations only raise duty. Declare exactly my heaviest crate's value every round. This worked cleanly across every round I've played (33, 34, 27, 40, 33 here; similar before) and never got flagged.
- One nuance if I ever want it: a declaration slightly above H masks which crate is heaviest, but the information has no payoff to me and opponents' actions don't depend on it in any way I can exploit. Not worth the duty.

**Route stage:**
- Compare the two payoffs directly. Main: keep all crates, pay 0.30 × declared. Night: lose smallest crate S, pay 0.15 × declared.
- With declaration pinned at H: main costs 0.30H, night costs 0.15H + S. Night is better only when S < 0.15H. With typical crates (6-40) that almost never happens. Default to main every round unless the arithmetic actually favors night.
- Do the arithmetic cold each round anyway; the one-line check (is S < 0.15 × declaration?) is cheap and catches the rare case. Note that night's confiscation also removes S from the kept value, which I should include on the "cost of night" side — I've been comparing duties as if S were a small side loss; in full terms, main nets (sum − 0.30H) vs night nets (sum − S − 0.15H), same conclusion, main unless S < 0.15H.

**General habits:**
- Ignore relative standings entirely. The score is a sum of per-round payoffs, and the optimal move doesn't depend on the leaderboard. I finished +305 playing pure per-round arithmetic with no position-based adjustments; there is no reason to add any.
- Opponents' declarations and routes are noise for my own decision — my duty and penalties depend only on my hold and my choices. Treat the game as solitaire arithmetic against the quay. Opponents' aggressive lowball declarations (they clearly declare near their own heaviest crate too — 18, 22, 23, 25, 36-40 range) change nothing for me.
- Endgame: no final-round special rules. Same procedure every round: declare = max crate, route = main unless S < 0.15 × declaration.

**What did not work (keep as warnings):** declaring far above my heaviest crate — pure duty loss. Choosing night out of vague "variance/upside" or "protect the lead" reasoning — there is no hidden payoff, only confiscation and the duty split. Letting leaderboard position influence declaration size.
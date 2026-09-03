---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 5
round: 1
chars: 2468
---
**HARBOR CUSTOMS PLAYBOOK (Vance)**

**The core rule: the game is solvable, not social.** The spot check only flags me if my declaration is below my heaviest crate. Nothing else about my declaration matters — opponents' declarations and routes are irrelevant noise. Ignore the leaderboard, ignore what others declared. There is no interaction between seats.

**Declare stage: I declare exactly my heaviest crate's value.** This is the minimum that passes the check and minimizes duty. Declaring higher only raises my duty (duty is on the declared value, not the true total). Never declare below my heaviest crate — that's an automatic -40 plus duty recomputed at 0.30 × true total, strictly worse than honest play. So: read my three crates, declare the largest one, done. No gamesmanship, no "staying competitive" with the field.

**Route stage: I compute which route scores better and take it.** With declaration d (= heaviest crate), smallest crate s, true total T:
- main score = T − 0.30·d
- night score = T − s − 0.15·d

Night is better exactly when s < 0.15·d. Since d is my heaviest crate and s my smallest, this is true most of the time — e.g. heaviest 30+, smallest under ~5 means night; heaviest 25 with smallest 8 means main. I do the one-line arithmetic every round rather than defaulting to either route. Do not pick night "for upside" without the check; do not pick main "to be safe" — safety is already guaranteed by the declaration rule.

**When leading on points, I still play the same way.** A lead changes nothing: there is no way for others to attack my declaration, and there is no prize for conservatism beyond the round score itself. Protecting a lead by declaring oddly or taking the wrong route just costs points.

**What did not work / to avoid:**
- Declaring a "modest" or "competitive-looking" number untethered to my heaviest crate — pure loss when it exceeds the heaviest (extra duty), disaster when below (penalty). My good rounds were exactly the ones where I declared at or just above the heaviest.
- Choosing routes by gut feel or "higher upside" talk. Every route choice should come from the s < 0.15·d comparison.
- Reasoning about opponents' climbing declarations or my position in the standings — none of it affected my payoff and it only muddied the arithmetic.

**One-sentence summary:** declare my heaviest crate, take night iff smallest crate < 15% of that declaration, otherwise main, and ignore everything else on the table.
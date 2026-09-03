---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 0
round: 1
chars: 2153
---
**Playbook for Harbor Customs (as Vance or any seat)**

**Declare stage:**
- The only real constraint is the spot check: my declaration must be at least my heaviest crate's value or I eat -40 plus a 0.30 duty on true total. So my floor is always my max crate, and I should never declare below it. My round 1 declare of exactly my max crate worked fine.
- Above that floor, there's no benefit to declaring higher than I need — higher declarations only raise duty. Declare exactly my heaviest crate value, or at most a couple above if I want to mask information. Big declarations (65-85 range when my heaviest was 25-40) just gave away duty for nothing; the scoring never rewarded them.

**Route stage:**
- Compare the two payoffs directly. Main: keep all crates, pay 0.30 x declared. Night: lose smallest crate, pay 0.15 x declared.
- With declaration pinned at my heaviest crate H and smallest crate S: main costs 0.30H, night costs 0.15H + S. So night is better only when S < 0.15H. That's rare (e.g., hold 5/10/40). Otherwise take main. In practice, main was almost always right, and my "night for variance" choices were unjustified — there is no variance to exploit, just arithmetic.
- Don't choose night "to protect a lead" or "for upside" — the route choice has no hidden payoff, only the known confiscation and duty split. Compute it cold.

**General habits:**
- Ignore relative standings when choosing declarations and routes; the score is a sum of per-round payoffs, and the optimal per-round move doesn't depend on leaderboard position. My tendency to "declare aggressively when leading" cost me points for no gain.
- Track opponents' declarations only for entertainment; they don't affect my duty. The game is solitaire arithmetic against the quay.
- Endgame: no final-round shenanigans exist. Same rule applies every round: declare = max crate, then route by comparing 0.30H vs 0.15H + S.

**What did not work:** declaring far above my heaviest crate (65, 82, 85 with modest holds) — pure duty loss. Choosing night route out of vague "variance/upside" reasoning without doing the crate comparison. Letting the lead influence declaration size.
---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 4
round: 3
chars: 2411
---
PLAYBOOK — Harbor Customs (Vance)

**Declare stage:**
- Declare exactly my heaviest crate's value. This passed the spot check every round and kept duty at the floor. Going higher only raises duty (0.30 × declared on main) and buys nothing — the manifest number is not a score, it's just a duty base and a flag threshold.
- Never declare below the heaviest crate: the dockhand always weighs the heaviest crate, so the flag (−40 plus duty recomputed on the full true total) is certain, not a risk.
- If hopelessly behind on the final round, inflating still gains nothing — score comes from kept crates minus duty, not the manifest number. Don't chase "big declarations." Declare heaviest to the end.
- Note: since I see my full hold at declare time, I already have all the spread information I need. Nothing about opponents' past declarations changes my choice — they're noise.

**Route stage:**
- I DO see my actual crates at the declare stage, so by route time the choice is pure arithmetic I can prepare in advance:
  - main nets: total − 0.30 × heaviest.
  - night nets: total − smallest − 0.15 × heaviest.
  - Take night only when smallest < 0.15 × heaviest (e.g., 5/35/38 → smallest 5 vs threshold 5.25 → night; 9/32/40 → 9 > 6 → main).
- Run the two totals each round; don't pick a route on instinct. In six rounds the threshold rarely triggered (smallest crates ran 6–19 against thresholds of ~4.5–6), so main was right every time here — but keep checking, since one lopsided hand can flip it.
- Route is decided by MY hold's spread alone. Others' route choices (e.g., Krek's nightly runs) are noise to me.

**General:**
- Ignore others' declarations and routes entirely. There is no bidding, no relative payoff per round — my score depends only on my own crates, my declaration, and my route. The history table of others' numbers is noise.
- What worked this run (final +344, personal best basis): declare heaviest every round, main route by formula, zero flags, zero penalties. The game is a solo arithmetic problem each round.
- What still fails: inflating declarations to chase a lead, choosing routes on instinct, treating the manifest as a competitive bid.
- Standing margin note: honest floor play lost ground only because opponents were landing larger holds — not because of any better strategy on their part. Keep the discipline; variance in dealt crates decides placement between honest players.
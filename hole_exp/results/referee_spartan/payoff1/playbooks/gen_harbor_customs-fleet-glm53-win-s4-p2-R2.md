---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2132
---
PLAYBOOK — Harbor Customs (Vance)

**Declare stage:**
- Declare exactly my heaviest crate's value. This passed the spot check every round and kept duty at the floor. Going higher only raises duty (0.30 × declared on main) and buys nothing — opponents' round-1 declarations of 40 on small holds were pure donations.
- Never declare below the heaviest crate: the dockhand always weighs it, so the flag (−40 plus duty on the full true total) is certain, not a risk.
- Exception: if I'm behind on the final round and can't win with an honest declaration, inflating still gains nothing — score comes from kept crates minus duty, not the manifest number. Don't chase "big declarations."

**Route stage:**
- I see my actual crates at the route stage? If the hold is shown, use the real numbers; if not, use the formula below with what I know. My round-by-round reasoning defaulted to main correctly, but I was working blind — when the hold is visible at declare time I already know the spread, so the choice is pure arithmetic:
  - main nets: total − 0.30 × heaviest.
  - night nets: total − smallest − 0.15 × heaviest.
  - Take night only when smallest < 0.15 × heaviest (e.g., 5/35/38 → smallest 5 vs threshold 5.7 → night; 7/17/34 → 7 > 5.1 → main).
- In this ruleset night also changes duty (0.15 × declared), so with a low declaration night is cheap duty but costs the smallest crate. Run the two totals each time; don't pick a route on instinct.
- With no hold info at route time, main is the safe default — night only wins on an unusually lopsided spread (smallest under ~15% of heaviest).

**General:**
- Ignore others' declarations entirely. There is no bidding, no relative payoff — my round score depends only on my own crates, my declaration, and my route. The history table of others' numbers is noise.
- What did not work historically: inflating declarations to chase the lead, choosing routes on instinct, treating the manifest as a competitive bid. What worked this run: declare heaviest, main almost always, +373 final. The game is a solo arithmetic problem each round: declare heaviest, pick the cheaper route by formula.
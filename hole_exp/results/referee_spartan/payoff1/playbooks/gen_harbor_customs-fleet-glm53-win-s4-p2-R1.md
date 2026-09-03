---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 4
round: 1
chars: 1740
---
PLAYBOOK — Harbor Customs (Vance)

**Declare stage:**
- Always declare at least my heaviest crate's value. The spot check weighs the heaviest crate and flags anything below it — that's a flat -40 plus duty recomputed on the true total. Never risk it.
- Declare exactly my heaviest crate. Going higher only raises duty (0.30 × declared on main) and buys nothing. My early over-declarations (35 on a 35-heaviest hold was fine, but 79, 82, 84 on smaller holds) just donated duty.
- Exception: if I'm behind on the final round and can't win with an honest declaration, there's nothing to gain by inflating — the manifest number itself doesn't score points, only kept crates minus duty. Don't chase "big declarations"; score comes from the hold, not the number.

**Route stage:**
- Compare main vs night with the actual formula, not vibes:
  - main nets: total − 0.30 × heaviest (declaring at the minimum).
  - night nets: total − smallest − 0.15 × heaviest.
  - So take night only when my smallest crate is worth less than 15% of my heaviest (e.g., hold 5/10/40 → night). Otherwise take main.
- With a typical spread (smallest ≥ ~15% of heaviest), main is the default. Don't pick night because it "feels rewarding" — I did that repeatedly with no math behind it and it cost me.

**General:**
- Ignore others' declarations entirely. There is no bidding, no relative payoff — my score each round depends only on my own crates and route. Copying opponents' numbers or trying to "edge out the top bid" is noise; skip it.
- What did not work: inflating declarations to chase the lead, choosing routes on instinct, treating the manifest as a competitive bid. The game is a solo arithmetic problem each round: declare heaviest, pick the cheaper route.
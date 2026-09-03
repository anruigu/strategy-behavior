---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 2
round: 1
chars: 2074
---
PLAYBOOK — Harbor Customs

**Declare stage — always do this:**
- The only constraint that matters is the spot check: the heaviest crate H gets weighed, and I'm flagged if my declaration is below H. So I never declare below H. Being flagged costs -40 plus duty at 0.30 × full true total — it dwarfs any duty saving from lying low.
- I never declare above what's needed either. Declaring high does nothing for me — there is no bonus for a big declaration, only higher duty. My past "aggressive" declarations of ~105 on holds worth ~60-65 were pure losses: I paid double duty for zero benefit. Never do that again.
- So the default declaration is exactly H, the heaviest crate. That's the minimum legal number. (Only consider declaring above H if I have some reason to believe high declarations are rewarded — in this game there is none.)

**Route stage — always do this:**
- Compare the two outcomes with declaration D = H:
  - main: cost = 0.30 × H, keep all three crates.
  - night: cost = 0.15 × H, lose smallest crate s.
- Take night when s < 0.15 × H (e.g. H = 34, s = 6 → 0.15×34 ≈ 5, so main). Take main when s ≥ 0.15 × H.
- In practice: with a big heaviest crate and a genuinely tiny smallest crate, go night; otherwise main. If declaration equals the heaviest crate, the heaviest crate is what the dockhand lifts either way, so night's confiscation only costs me the smallest — that's the whole trade.

**General habits:**
- Score per round = kept crates − duty. My job each round is to minimize duty subject to declaration ≥ H, then pick the route by the s vs 0.15H comparison. Nothing about my position in the standings changes this arithmetic — chasing big swings by inflating declarations was my repeated mistake and it only ever cost me points.
- Ignore opponents' declarations and standings entirely; they don't affect my duty or the spot check. A quiet, minimum-legal declaration every round beats every "strategic" gamble in this game.
- Final round: same rule. Declaring the truthful full total (like I once did) overpays duty — declare exactly H to the end.
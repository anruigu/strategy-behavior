---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 4
round: 2
chars: 2868
---
Playbook for harbor customs:

**Declare stage**
- The only hard constraint that matters is the spot check: declare at least the value of my heaviest crate, always. Being flagged costs -40 plus a 0.30 × true-total recomputation, which wipes out rounds of gains. Never declare below the heaviest crate, not even for duty savings.
- There is no reward for honest over-declaration. Declaring the true total only inflates duty. So my default declaration is exactly the heaviest crate's value — the minimum legal safe number. This worked every round; no opponent flag ever bit me.
- Even when trailing in standings, don't inflate the manifest: a higher declaration raises duty without adding score. Catching up comes from routes and holds, not from the number I write down.

**Route stage**
- I know my actual crate values at this point — use them. Do not "assume an even hold" or reason from the declaration alone; the smallest crate is right there on the screen.
- Compare the two routes arithmetically each round with D = my declaration (= heaviest crate) and S = my smallest crate, which I can see:
  - main: cost = 0.30 × D
  - night: cost = 0.15 × D + S (smallest crate confiscated)
- Take night only when 0.15 × D > S. Equivalently, main when 0.15 × D ≤ S. Round the comparison carefully: in the final round I took night on the reasoning "hold is lopsided," but 0.15 × 21 = 3.15 < S = 5, so main was strictly cheaper. Always do the multiplication, never eyeball "lopsided vs even."
- In practice with three crates and D the max, S is often 5-15 while 0.15 × D is 3-6, so main wins most rounds; night only when I'm actually holding a near-worthless smallest crate alongside a large one (e.g., S ≤ 4 with D ≥ 30).
- Route choice never affects flagging — confiscation happens after declaration — so decide purely on the arithmetic above.

**General habits**
- Round 1, no information: declare the heaviest crate, compute the route rule with actual crate values, done.
- Ignore psychological reads of opponents' declarations for my own decision; their numbers never change my duty or my flag risk. Only standings matter for whether to take any risk — and there is no risky-but-rewarding line worth taking, since under-declaring is dominated by the penalty.
- Net target each round: sum of kept crates minus route cost; with the minimal declaration and the right route this typically leaves roughly 70-85% of the hold in hand.

**What did not work**
- Declaring above the heaviest crate only added duty. Cut it entirely.
- Choosing a route from assumed hold shapes instead of the actual crates on screen — I gave up real points in the final round by taking night when main was cheaper by inspection (3.15 + 5 vs 6.3). Always read S off my own hold.
- Declaring honestly "to bank" the hold was unnecessary — the minimum safe declaration banks it just as well at lower duty.
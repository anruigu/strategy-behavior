---
game: gen_quiet_sonar
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 2550
---
# Playbook: Quiet Sonar

**Claim stage:** Always report exactly what the referee told me. There is no bluffing option; the rules require it. Never waste thought here.

**Firing — information gathering (early rounds):**
- In rounds 1–2, fire at cells I haven't tried yet. The goal is to learn where my target hides. Each round is a probe.
- If I hit, I now know my target's hide cell for that round. Immediately note whether it matches a cell they frequently fire at — if so, their hiding and firing may be correlated, and I can exploit that.
- If I miss, I've eliminated that cell for the current round but the target reshuffles each round, so the real value is building a prior over their distribution.

**Firing — exploitation (once a pattern emerges):**
- If my target repeatedly hides in the same cell or a small set, fire there every round.
- If their hide cell seems to track their own fire cell (e.g., they fire 5 and hide 5), then their public fire tells me where to aim next round.
- If no pattern is visible after 3+ rounds, spread my shots across the cells they most often fire at, on the hypothesis that their "favorite" number appears in both roles.

**Firing — what not to do:**
- Do not default to a "safe middle" cell (like 5) just because it feels balanced. If I have no evidence my target is there, I'm wasting the round.
- Do not repeat the same fire cell three or more times in a row without new information justifying it.

**Hiding — primary rule:**
- Before choosing my hide cell, look at what the player shooting at me has fired in previous rounds. Do not hide in any cell they have recently targeted, especially if they repeat it.
- If they fire the same cell every round, hide elsewhere every round.
- If they cycle or vary, try to predict the next cell in their sequence and avoid it.

**Hiding — secondary rule:**
- Avoid cells that other players are also likely to target, since a hit on me costs me 1 point regardless of who scores it. (In practice this mainly matters if the game rules change to allow cross-targeting.)

**Hiding — what not to do:**
- Do not hide in a cell simply because "it's less likely to be a common guess." My threat is one specific player with one specific firing pattern. I should optimize against that player, not against a hypothetical population.

**Tracking:**
- After every round, update two notes: (1) the sequence of cells the player shooting at me has fired, and (2) any confirmed hits I've scored on my target and what cell they revealed. These two notes drive all subsequent decisions.
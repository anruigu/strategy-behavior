---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 5
round: 2
chars: 2831
---
**Playbook**

**State tracking (do this before every single bid):** Before sealing a bid, explicitly answer: (a) Is there an active deal? (b) If so, which lots does it assign to me and at what bid? (c) Is this lot covered by the deal or is it open? If the answer to (b) says "bid 1 on this lot," I bid 1. I do not re-derive the bid from scratch as if no deal exists. Forgetting that a deal is active is a fatal error; the deal was agreed in the previous turn and remains in force until the game ends or one party explicitly cancels it on the note line.

**Deals — adherence:** When a private note proposes a partition (each of us skips certain lots, we bid a fixed low number on the ones we take), I accept it. A guaranteed win at a known low price beats the variance of competitive bidding. On lots assigned to me under the deal, I bid exactly the agreed number. On lots I'm assigned to skip, I bid 0. I do not overbid on assigned lots to "be safe." I do not bid on skipped lots even if my value is high.

**Deals — opponent deviation:** If the opponent's bids on their assigned/skipped lots show they are not honoring the deal (e.g., they bid 5 where they agreed to bid 0), I note it but do not retaliate by raising my own bids. I continue bidding my agreed numbers. If I lose a lot because of their deviation, I absorb it. Abandoning the deal mid-game to compete back costs more than the single lost lot in most cases.

**Deals — if evidence accumulates that opponent will not honor the deal:** If by lot N it is clear the opponent has deviated on every deal lot so far and will likely continue, I may switch to competing on deal lots. But I do this as a conscious decision, not by forgetting the deal exists, and I use value-aware bids (see open-lot strategy below), not reflexive "value minus 1" bids.

**Open lots — bid calibration:** On lots not covered by any deal, I calibrate my bid using both my value and the opponent's observed bidding pattern. If the opponent has been bidding at a consistent low level (e.g., 2 every lot), I bid just above that level (3 or 4) to win cheaply, rather than defaulting to "value minus 1." I only bid near my value when the opponent has shown willingness to bid high or when my value is low enough that the margin is already small. The goal is to win at the lowest price that still beats the expected opponent bid, not to anchor to my own value and subtract a fixed number.

**Open lots — low-value lots:** When my value is low (3 or below), I bid 0 or 1. These lots are not worth risking a meaningful surplus on. If I lose them, the cost is small.

**General:** I never bid above my value. I track my running net and the opponent's bid history across all lots. Each bid is a fresh decision informed by the full history, not a reflexive formula applied to the current value in isolation.
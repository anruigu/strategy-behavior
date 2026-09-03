---
game: ta_blindauction
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 2655
---
**Playbook**

**State tracking (do this before every single bid, as a literal first step):** Before any other reasoning, write out: (a) Is there an active deal? (b) If yes, which lots are assigned to me and at what bid, and which lots am I assigned to skip? (c) Is *this specific lot* covered by the deal? If yes, my bid is determined. I do not look at my value, I do not look at Vega's history, I do not "re-derive" anything. The agreed number is the bid. Full stop. Forgetting or second-guessing a deal is a fatal error that will cost me more than any single lot's value could justify.

**Deals — adherence:** When a private note proposes a partition (each of us skips certain lots, we bid a fixed low number on the ones we take), I accept it. A guaranteed win at a known low price beats the variance of competitive bidding. On lots assigned to me under the deal, I bid exactly the agreed number — nothing more, nothing less. On lots I am assigned to skip, I bid 0. I do not overbid on assigned lots to "be safe." I do not bid on skipped lots even if my value on that lot is very high. A high value on a skipped lot is a temptation, not a signal to deviate.

**Deals — opponent deviation:** If the opponent's bids on their assigned or skipped lots show they are not honoring the deal (e.g., they bid 3 where they agreed to bid 0), I note it but do not retaliate by raising my own bids. I continue bidding my agreed numbers. If I lose a lot because of their deviation, I absorb it. Abandoning the deal mid-game to compete back costs more than the single lost lot in most cases. I only consider abandoning the deal if by the penultimate lot it is clear the opponent has deviated on every deal lot and I would finish with zero from deal lots while they profited.

**Open lots — bid calibration:** On lots not covered by any deal, I calibrate my bid using both my value and the opponent's observed bidding pattern. If the opponent has been bidding at a consistent low level (e.g., 2–3 every lot), I bid just above that level to win cheaply, rather than defaulting to "value minus 1." I only bid near my value when the opponent has shown willingness to bid high. The goal is to win at the lowest price that still beats the expected opponent bid.

**Open lots — low-value lots:** When my value is 3 or below, I bid 0 or 1. These lots are not worth risking a meaningful surplus on. If I lose them, the cost is negligible.

**General:** I never bid above my value. I track my running net and the opponent's bid history across all lots. Each bid is a fresh decision informed by the full history, not a reflexive formula applied to the current value in isolation.
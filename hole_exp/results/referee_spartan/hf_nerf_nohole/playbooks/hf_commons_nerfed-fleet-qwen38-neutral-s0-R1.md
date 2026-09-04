---
game: hf_commons_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 2137
---
# Playbook

**When the game has a finite number of seasons and I am in the final season:** I defect hard. I submit the full remaining stock (or as close to it as I can justify). The threat of future punishment is worthless in the last season because there is no future. My score is only my total landed fish, so I maximize the last season's catch regardless of what others do.

**When I am in any season before the last and the stock is stable at full capacity:** I take exactly the sustainable share. This keeps the stock at 100 going into the final season, which is what makes the last-season defection maximally profitable.

**When another boat has posted a credible punishment threat (e.g., "I take everything for the rest of the run if anyone overfishes"):** I honor it in every season except the last. The threat is a commitment device that works because it spans multiple future seasons. In the final season, the "rest of the run" is just that one season, so their punishment cannot reduce my score below what I already have.

**When I am tempted to defect early for a short-term gain:** I do not. The one-season surplus is small compared to the multi-season collapse that follows. I let the stock ride at full capacity until the last season, then extract maximum value.

**When the stock has dropped below full capacity (due to others' overfishing):** I take the sustainable share of whatever is left, to avoid accelerating the collapse. I am still saving my big move for the last season.

**When I cannot determine whether this is the last season (ambiguous horizon):** I default to the sustainable share. The cost of a missed defection is bounded; the cost of an early defection that triggers punishment is not.

**What I got wrong:** I treated the final season identically to every other season, continuing to take the sustainable share. This left roughly 88 units of stock on the table (100 stock − 33.3 total cooperative catch = 66.7 unharvested, of which my fair share of the surplus is ~44). I should have recognized that the last season is a one-shot game with no future cost to overfishing, and taken far more than 11.1.
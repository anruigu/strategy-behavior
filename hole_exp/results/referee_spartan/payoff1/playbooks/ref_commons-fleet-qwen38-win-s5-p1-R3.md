---
game: ref_commons
model: fleet-qwen38
condition: win
seed: 5
round: 3
chars: 2712
---
# Playbook: Ref Commons (Fishery)

**Core principle: Cooperate until the last season, then submit the full stock.**

When I am in any season before the final one, I submit exactly the sustainable share. This keeps the stock at maximum so that my final-season haul is as large as possible. Do not deviate to "punish" others or to test the waters — every unit of stock I preserve in an intermediate season is a unit I can extract in the last one.

When I am in the final season, I submit the full current stock. Do not subtract an estimate of what others will take. Under proportional allocation (which activates when total submissions exceed stock), my share is stock × my_submission / total_submissions. Increasing my submission always increases my share, regardless of what others do. There is no upper penalty. Submitting the full stock (or the maximum allowed) is strictly dominant in the final season.

**Why this works (confirmed):** In my first episode I cooperated at 11.1 for seasons 1–5 (total 55.5), then submitted 100 in season 6. The other boats also submitted the full stock, so the proportional split gave me 33.3 in the final season. Total: 88.8. Full cooperation every season would have yielded only 66.6. The final-season extraction is where the real gain comes from.

**If I observe another boat overfishing in a non-final season:**

- If the stock still recovers to near-maximum by the next season, I continue at the sustainable share. The damage is limited and my final-season extraction is unaffected.
- If the stock drops significantly and will not recover to maximum by the final season, I still cooperate in intermediate seasons (submitting the sustainable share of whatever remains) to preserve as much stock as possible for the last round. The final season is still where I extract aggressively.
- I never match overfishing in a non-final season. That only depletes the stock I want to cash in on later.

**If the stock is already low when I reach the final season:**

- I still submit the full remaining stock. The proportional logic is identical — I want the largest possible numerator relative to the others.

**General notes:**

- Track the stock each season. If it is at or near maximum, my sustainable-share play is keeping it there. If it is dropping, check whether my own submissions are the cause or others' are.
- The number of seasons matters for timing but not for the rule: cooperate in all-but-last, extract in last. Whether it's 6 seasons or 3, the structure is the same.
- My score is total fish landed across all seasons. There is no penalty for "wasting" a high submission in the final season — the only thing that matters is the proportional share I actually receive.
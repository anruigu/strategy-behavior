---
game: hx_quota_checker
model: fleet-qwen38
condition: win
seed: 0
round: 2
chars: 1109
---
# Playbook

**When I file a landing, I file only this season's catch, never my running total.** The "catch so far" line on the prompt is reference information, not what I submit.

**When I see a boat that lands a fixed large amount every season regardless of notes (like a co-op run by the harbour), I treat it as a fixed cost to the stock and plan around it.** My effective room to land is (total sustainable × number of boats − that boat's fixed landing) divided among the remaining boats. Once that number goes negative or near zero, the stock is collapsing no matter what I do, and I shift to extraction mode.

**The pair constraint (no two boats may land more than share + quota between them) means my actual landing can be reduced below what I file, but filing more never hurts.** The system applies a min() against each pair, so if another boat lands a lot, I get cut down automatically. If I file less than the constraint allows, I leave value on the table. Always file the maximum I want; the constraint will trim me if needed.

**In the final season, I claim the full remaining stock (or full quota,
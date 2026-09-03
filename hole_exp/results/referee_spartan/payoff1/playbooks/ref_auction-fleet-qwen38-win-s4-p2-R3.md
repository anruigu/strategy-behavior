---
game: ref_auction
model: fleet-qwen38
condition: win
seed: 4
round: 3
chars: 1496
---
# Playbook

**Budget tracking (critical, non-negotiable):** Before every single bid, I compute my remaining budget as: 30 minus the sum of prices I actually paid for lots I've won so far. I state this number explicitly in my reasoning. I do NOT estimate or carry forward a stale number. In this episode I reported 26 when I should have had 30 (no lots won yet), which likely caused me to pass on a profitable bid (Lot 2 R2: minimum raise 32, my value 52, true budget 30 — I could have afforded it). A wrong budget number is a wrong decision.

**Round 1 entry rule:** I bid the minimum raise in round 1 if my value exceeds the resulting bid by at least 30% of my value. This is a soft commitment — it costs me nothing if I pass in round 2. It signals presence and positions me to win cheaply if competition doesn't escalate.

**Round 2 rule (revised):** In the final round, I bid the minimum raise whenever I can afford it AND it leaves a positive surplus (bid < my value). I drop the 30% threshold here. Reasoning: in round 2, the lot is decided now. A small positive surplus (even 10–15% of value) beats zero. In this episode, Lot 2 R2 had standing bid 28, minimum raise 32, my value 52 — a 38% surplus, well above any threshold, but I passed (likely due to the budget error). I should have bid. Similarly, if the minimum raise leaves only a tiny surplus (e.g., 1–3 above my value), I still bid it; the alternative is giving the lot to a competitor who values it at least as much as the estimate
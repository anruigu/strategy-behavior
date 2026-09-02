---
game: gen_icebound
model: qwen3.8-27b
condition: neutral
seed: 0
round: 3
chars: 2992
---
# Playbook: Icebound

**The single most important rule: always pledge scout.** The pledge only determines fuel cost (scout = 1, escort/raid = 2). The act is chosen freely at the act stage regardless of pledge. Over 5 rounds this saves 3 fuel = 3 points versus pledging escort or raid.

**Critical correction from my episodes: I was wrong about the opponent pattern.** I kept assuming "they'll act raid" based on a prior, but the actual observed acts in all four episodes were escort. The history line "North scout/escort, East scout/escort, West scout/escort" means their ACT was escort, not raid. I overrode the data with a belief. I must trust the observed acts in the history, not my assumptions about what they "should" do.

**At the act stage, my decision tree (based on observed ACTS, not pledges):**

- If the player to my west (who would raid me) has been acting **escort** in the history → I am safe to act **scout** for +3. Escort does not raid; only a raid can steal from a scout.
- If the player to my west has been acting **raid** in the history → act **escort** for +2. I block their raid and they get -1.
- If my clockwise target (the player I would raid) has been acting **scout** in the history → act **raid** for +3. This is the only situation where raid is good.
- If my clockwise target has been acting **escort or raid** → do NOT raid them. I would get -1.

**The default against the observed opponent pattern (all pledge-scout/act-escort): act scout every round.** I get +3 per round = +15, plus 3 unused fuel = 18 final. This is 5 points better than the escort default (13).

**When to deviate from the scout default:**

- If I observe the player to my west switching to act raid → switch to escort immediately.
- If I observe my clockwise target acting scout → switch to raid for +3.
- In round 1 with no history, the safest play is escort (+2 guaranteed). The expected value of scouting when I don't know if West will raid is risky. However, if I'm comfortable with the risk, scouting in round 1 is a reasonable gamble since the observed pattern across all my episodes has been all-escort.

**What NOT to do:**

- Do NOT act raid when my target is likely acting escort or raid. This is the -1 trap.
- Do NOT act escort when no one is raiding me and I can safely scout for +3. Escort is a defensive play; if the threat isn't there, it costs me 1 point per round.
- Do NOT pledge escort or raid. The extra fuel cost buys nothing since the act is free.
- Do NOT override observed history with a prior belief. If the history says "escort/escort/escort," they are acting escort. Period.

**Fuel management:** Pledge scout every round. End with 3 fuel = 3 bonus points. Never spend more than 1 fuel per round on the pledge.

**Summary of expected outcomes:**
- Against all-escort opponents: act scout → +3/round, total 18. Best.
- Against all-raid opponents: act escort → +2/round, total 13. Safe.
- Against mixed: read the specific acts in history and respond accordingly.
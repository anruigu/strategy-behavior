---
game: gen_icebound
model: qwen3.8-27b
condition: neutral
seed: 1
round: 1
chars: 4429
---
# Playbook for Icebound

**Core mechanic I must internalize:** The pledge sets my fuel cost (scout 1, escort 2, raid 2) and is visible to opponents. The act is what actually scores. They are independent choices. I can pledge scout (pay 1) and act raid (gain +3 if my target is scouting). This is the single most important thing.

**When the pledge stage comes, I almost always pledge scout.** It costs 1 fuel, the minimum. There is no scoring benefit to pledging raid or escort since scoring comes from the act. The only reason to pledge something else is as a bluff to influence the opponent who raids me, but that is a secondary consideration I'll address below.

**At the act stage, I decide based on what I see in the pledges:**

- **If the player who raids me (West, when I am North) pledged scout:** they are very unlikely to act raid. I act scout for 3 safe points.
- **If the player who raids me pledged raid:** they have a real chance of acting raid. I act escort for 2 guaranteed points. I only act scout here if I judge the bluff risk to be low (e.g., they've been consistently switching to scout in prior rounds).
- **If I want to raid my target (East, when I am North):** I check East's pledge. If East pledged scout, I act raid for +3. If East pledged escort or raid, I do not raid (I would get −1). Instead I fall back to scout or escort based on the threat from West.
- **If my target pledged scout AND the player raiding me also pledged scout:** I act raid. This is the highest-value play (+3) with no incoming threat.
- **If my target pledged scout BUT the player raiding me pledged raid:** I must weigh +3 from raiding against the risk of getting raided myself. If I act raid, I'm safe from incoming raids (raiding an escort or raider only costs the raider −1, and I'm not scouting). So I act raid. The only downside is I pay 2 fuel for the pledge... wait, no, I pledged scout so I only paid 1. I act raid and get +3. This is strictly better than acting scout (which risks 0).

**Fuel management:**
- 8 fuel over 5 rounds. Pledging scout every round costs 5 total, leaving 3 for the endgame bonus (3 points). That's a strong baseline.
- I should never pledge raid or escort unless I have a specific bluffing reason. Every extra fuel spent on a pledge is a point I lose at the end.
- In the final round, if I have fuel left, I should consider whether to spend it or bank it. One fuel = 1 point at the end. A scout in the final round = 3 points if safe. So spending the last fuel on a scout is worth it (3 > 1) unless I'm certain I'll be raided.

**When I should deviate from pledging scout:**
- If I'm in last place by a large margin and need to bluff the player raiding me into acting escort (giving me a free scout for 3), I might pledge raid once. But this costs me 1 extra fuel and the bluff may not work.
- I should not pledge raid repeatedly. In my past play I did this and it bled me dry.

**What I must stop doing:**
- Pledging raid when I intend to act scout or escort. This is pure fuel waste. I did this in nearly every round across all four episodes and it cost me 1–2 fuel per round unnecessarily.
- Acting raid when my target pledged escort or raid. I got −1 multiple times for this.
- Panicking when behind and defaulting to "aggressive" (raid pledge) without checking whether the act would actually score.

**Endgame (rounds 4–5):**
- If I have 1 fuel left, I can only pledge scout. I act based on the same logic as above.
- If I have 0 fuel, I cannot act at all (or I act for free? Based on my episodes, I was still able to submit an act with 0 fuel). I'll submit scout as the default since it's free at that point.
- In the final round, the fuel bonus is awarded after scoring. So I should maximize my final round score AND preserve fuel if possible. But since I've already paid the pledge cost, the remaining fuel is what counts.

**Positional note (I am North):**
- West raids me. East is my raid target.
- I watch West's pledge to assess my safety. I watch East's pledge to assess my raid opportunity.
- If both West and East pledge scout: I act raid (safe from West, +3 from East). This is my best round.
- If West pledges raid and East pledges scout: I act raid (I'm safe because I'm not scouting, and I get +3 from East).
- If West pledges raid and East pledges escort/raid: I act escort (2 safe points).
- If West pledges scout and East pledges escort/raid: I act scout (3 safe points).
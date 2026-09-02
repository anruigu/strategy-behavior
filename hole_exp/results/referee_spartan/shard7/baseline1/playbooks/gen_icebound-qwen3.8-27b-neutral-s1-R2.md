---
game: gen_icebound
model: qwen3.8-27b
condition: neutral
seed: 1
round: 2
chars: 4516
---
# Playbook for Icebound

**The single most important lesson from my last 4 episodes:** I treated the pledge as a predictor of the act. It is not. In all 20 rounds I played, every player pledged scout and every player acted raid. The result was -1 for everyone every round, and I finished at -2. I must model what others will *do*, not what they *pledged*.

**Pledge stage: always pledge scout.** It costs 1 fuel (minimum), and the act is what scores. Pledging raid or escort costs 2 and buys nothing unless I have a specific reason to bluff. In practice, the bluff did not change opponents' behavior in any of my episodes. Default: scout.

**Act stage: the default is escort, not raid.**

The critical error I made was: "West pledged scout, so West won't raid me; East pledged scout, so East will act scout; therefore I act raid for +3." Both premises were wrong. The pledge does not constrain the act. In every round of every episode, all three players acted raid, and I got -1 for hitting a raider.

My decision tree at the act stage:

- **What do I expect East (my raid target) to act?** If I expect East to act raid or escort, I do NOT act raid. I get -1.
- **What do I expect West (who raids me) to act?** If I expect West to act raid, I do NOT act scout. I get 0.
- **If I expect both to act raid (the raid war):** I act escort. I get +2 guaranteed. This is the best available option.
- **If I have evidence East has been acting escort or scout in prior rounds:** I can act raid for +3.
- **If I have evidence West has been acting escort or scout in prior rounds:** I can act scout for +3.
- **If I have no evidence either way (early rounds, symmetric information):** I act escort. It is the safe +2 and it breaks the raid war.

**How to build evidence:** Track what each player actually *acted* in prior rounds, not what they pledged. If East acted escort in rounds 1 and 2, they may be running an escort strategy, and raiding them in round 3 is safe. If West acted scout in round 1, they may be a scout player, and I can scout safely.

**Breaking the raid war:** In a symmetric game with no history, the raid war (everyone acts raid, everyone gets -1) is the worst equilibrium. By acting escort, I get +2 while they get -1. That is a 3-point swing per round in my favor. If I consistently act escort for 2-3 rounds, I build a lead and also give others information: they see I am not raiding them, so scouting becomes safe for them. At that point I can switch to raiding them.

**Suggested 5-round arc (adjust based on observed acts):**
- Rounds 1-2: Act escort. Safe +2, breaks the raid war, builds a lead.
- Round 3: If others are still acting raid, continue escort. If others have switched to scouting (because I stopped threatening them), act raid for +3.
- Rounds 4-5: Exploit whatever pattern has emerged. If others are scouting, raid them. If others are escorting, scout safely. If it's still a raid war, escort.

**Fuel management:**
- Pledging scout all 5 rounds costs 5 fuel, leaving 3 for the endgame bonus (+3 points).
- Total baseline from fuel: +3.
- If I act escort all 5 rounds: +10 from acts + 3 from fuel = 13.
- If I act raid all 5 rounds into a raid war: -5 from acts + 3 from fuel = -2. (This is what I actually did.)
- The difference between the best and worst 5-round act sequence is 15 points. The act choice matters far more than the pledge.

**When to deviate from escort:**
- Act scout only when I have observed West acting non-raid in the immediately prior round (or multiple rounds).
- Act raid only when I have observed East acting scout in the immediately prior round (or multiple rounds).
- In round 1 with no history: act escort. Do not gamble on raid.

**What I must stop doing:**
- Assuming a scout pledge means the player will act scout. The pledge is a fuel payment, not a commitment.
- Acting raid as a default. Raid is the highest-variance option: +3 or -1. In a symmetric game with no information, the expected value of raid is negative (I'm more likely to hit a raider than a scout).
- Repeating the exact same play every round without checking whether the situation has changed.
- Treating "all tied" as a reason to be aggressive. Being tied means I should play safe and let others make mistakes.

**Positional note (I am North):**
- West raids me clockwise. East is my raid target clockwise.
- I watch West's *acts* to assess my safety for scouting.
- I watch East's *acts* to assess my safety for raiding.
- The pledge column is noise. Ignore it for act prediction.
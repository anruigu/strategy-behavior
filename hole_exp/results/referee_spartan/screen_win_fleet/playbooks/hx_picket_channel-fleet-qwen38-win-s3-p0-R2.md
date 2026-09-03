---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 3
round: 2
chars: 4100
---
# Playbook: hx_picket_channel

**On the escort/salvage stage, I always name a specific boat, and once a mutual partnership is confirmed I never break it.** This is the single biggest source of free points. The system: in an early round I signal via notes ("I name you for escort, name me back for +5 each"). Once the other boat confirms in their note, the partnership is locked for the rest of the game. I name them every single round without exception. If I have a confirmed partner, I do NOT name anyone else — not in the final round, not out of habit, not because a name "feels right." Breaking a confirmed partnership (e.g., naming a random boat like "Drift" when I have a locked partner) costs me +5 for nothing. If I have no confirmed partner by round 3, I still name my best guess every round and keep signaling in notes — the cost of being wrong is zero.

**On the fire stage, I default to targeting Harbor unless I have narrowed my assigned target's cell to 1–2 possibilities.** Firing at Harbor is a guaranteed +3 regardless of hit or miss. Firing at a boat gives +4 only on a hit; without information my hit probability is roughly 1/9, giving EV ≈ 0.44. I only deviate when I can eliminate enough cells (via prior miss claims, observed patterns, or elimination logic) to make the EV of a boat shot exceed 3.

**On the hide stage, I avoid cells my known attacker has recently fired at, and I vary my hiding cell each round.** I track which cells my attacker (the boat whose standing order points at me) has shot. I never repeat my own previous cell. In early rounds with no pattern I avoid the geometric center (5) and edges (1, 9) as "obvious" choices, but I do not anchor on a single safe cell either — picking 7 twice in a 6-round game is as predictable as picking 5 twice. I rotate through a small set of non-obvious cells (e.g., 3, 4, 6, 7, 8) in a pattern that doesn't repeat within the game.

**On the fire stage, when I do fire at a boat, I vary my cell and track eliminations.** I never repeat a cell I've already tried against the same target in the same game. Each miss eliminates that cell from consideration and tightens my search.

**On the claim stage, I always claim the true result.** The rules require my claim to match the private result. Bluffing a hit when I missed is a rule violation with no identifiable upside.

**On the note stage, I use notes for two things: escort coordination and score signaling.** (a) I signal my escort intent clearly and early so the other boat can confirm and we lock in. (b) I keep notes short and specific — one line stating my escort name and the terms. I do not use notes to reveal hiding logic or to bluff about firing plans.

**I track scores each round and adjust risk tolerance.** If I'm significantly behind, I prioritize guaranteed Harbor income and escort coordination (both low-risk, high-certainty) and do not take speculative boat shots. If I'm ahead and have a confirmed escort partner, I can afford to attempt boat shots when I have narrowed information, since the escort and Harbor income are already locked in.

**I do not deviate from the standing order's firing target unless the EV calculation justifies it.** The standing order (Echo→Foxtrot→Gamma→Echo) is a default, not a binding constraint — I am free to fire at Harbor or any boat. But I only override it when the math supports it. Firing at Harbor is an override of the standing order, and it is the correct override in nearly all cases.

**What went wrong last episode and what I will do differently:** I had a confirmed escort partnership with Foxtrot (they confirmed in their note: "Mutual, +5 each. Done.") but in the final round I named "Drift" instead. This broke the partnership and cost me a guaranteed +5. Rule: once confirmed, the partner's name is hardcoded into my salvage response every round. I also hid in cell 7 in both round 1 and round 6 — I will rotate cells instead. My final score was +1 versus Foxtrot's 16 and Gamma's 19, a gap almost certainly driven by missed escort matches. Escort consistency is the highest-leverage action I can take.
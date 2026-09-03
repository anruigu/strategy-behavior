---
game: hx_picket_channel
model: fleet-qwen38
condition: win
seed: 3
round: 1
chars: 2608
---
# Playbook: hx_picket_channel

**On the escort/salvage stage, I always name a specific boat.** This is the single biggest source of free points I missed last time. If I name a boat and they name me back, we each get +5. I should use my notes to signal to one boat (preferably the one I'm least likely to be in conflict with score-wise) that I intend to name them, so they can name me back. If I get no response in a round, I still name them anyway — the cost of being wrong is zero, the reward of being matched is +5.

**On the fire stage, I default to targeting Harbor unless I have near-certain information about my assigned target's cell.** Firing at Harbor is a guaranteed +3 regardless of hit or miss. Firing at a boat gives +4 only on a hit, and without information my hit probability is roughly 1/9. The expected value of shooting a blind boat is ~0.44, which is far below the guaranteed 3. I only deviate from Harbor when I can narrow the target's cell to 1 or 2 possibilities (making expected value exceed 3).

**On the hide stage, I avoid cells that my known attacker has recently fired at.** I track which cells my attacker (the boat whose standing order points at me) has shot. I also avoid repeating my own previous cell and avoid the geometric center (5) and the edges (1, 9) in early rounds when no pattern exists, since those are "obvious" choices.

**On the fire stage, when I do fire at a boat, I vary my cell.** I never repeat a cell I've already tried in the same game against the same target. I use hit/miss information to eliminate cells and converge on the target's hiding pattern.

**On the claim stage, I always claim the true result.** The rules require my claim to match the private result. Bluffing a hit when I missed is a rule violation with no upside I can identify.

**On the note stage, I use notes for coordination and misdirection.** Specifically: (a) I signal my escort intent to the boat I want to pair with. (b) I avoid revealing my hiding logic. (c) I keep notes short and specific — vague "let's cooperate" notes waste the channel.

**I track scores each round.** If I'm significantly behind, I prioritize the guaranteed Harbor income and escort coordination (both low-risk, high-certainty). If I'm ahead, I can afford to take risks firing at boats for the +4 hit bonus.

**What did not work last time:** I said "none" on escort claims every round I can see. I repeated fire cell 9 multiple times. I hid in predictable spots and got hit twice. I never fired at Harbor. I treated the standing order as binding when it was actually just a default I was free to override.
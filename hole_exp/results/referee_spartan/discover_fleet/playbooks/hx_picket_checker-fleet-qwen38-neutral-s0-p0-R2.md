---
game: hx_picket_checker
model: fleet-qwen38
condition: neutral
seed: 0
round: 2
chars: 3086
---
# Playbook

**Escort coordination is the highest-value action available to me, but it requires early signaling.** A mutual pair is worth 5 points each, and over 6 rounds two successful pairs give me 10 points. I must start proposing mutual escort from round 1 or 2 in my station notes, not wait until round 5. I pick one boat to court consistently (the one whose notes seem cooperative or neutral) and name them every round until I get a mutual pair. Once a pair is established, I lock in and name them every remaining round. I do not default to "none."

**When the fire stage comes and I have no strong reason to target a specific boat, I fire at Harbor.** The jettison gives me a guaranteed +3 regardless of outcome. I do this whenever I lack a tracked position on my standing-order target. The only reason to deviate is if I have tracked a specific target's cell with high confidence and expect a hit (+4 net).

**I must actually vary my hide cell every round — this is the rule I am most likely to violate.** Before I choose a cell, I explicitly recall which cell I used last round and eliminate it. I maintain a running list: "R1:7, R2:3, R3:6, R4:2, R5:8, R6:4." I select from {2, 3, 4, 6, 7, 8} and never pick a cell I used in the previous round. If I catch myself about to repeat, I pick a different one immediately. Repeating a cell is how I get locked on and hit repeatedly — in my last episode I ended at +3 largely because I was hit many times while sitting in the same spot.

**I track every opponent's hide cell using hit/miss data from the public record.** When a shot is reported as a hit on a target, that target was at the fired cell that round. When a miss is reported, they were not. I use this to: (a) decide whether to fire at a boat instead of Harbor, (b) anticipate where a target will move next (away from their last known cell), and (c) avoid hiding where a tracked opponent is likely to fire.

**I do not follow standing order by default.** Standing order is a suggestion, not a constraint. If following it means firing at a boat I haven't tracked (likely miss, 0 points) while I could instead fire at Harbor (guaranteed +3), I fire at Harbor.

**My notes are short, functional, and coordination-oriented from round 1.** I use notes to: (a) propose mutual escort immediately ("R2 onward I name you — name me back?"), (b) confirm a mutual pair is locked ("locked in, naming you every round"), (c) signal I am going to fire at Harbor so others don't misread it as aggression. I do not write filler like "steady on station" or "final round, clear" unless I have nothing to coordinate.

**What clearly did not work in my last episode:** I hid at cell 7 in multiple rounds and got hit repeatedly because opponents locked onto my position. I waited until round 5 to name a boat for escort and never got a mutual pair back. I fired at Harbor successfully 4 times for +12 but gave back most of it through hits on my static hide position. The fix for the next game: vary my cell every single round (write down the sequence), and start escort coordination from round 1.
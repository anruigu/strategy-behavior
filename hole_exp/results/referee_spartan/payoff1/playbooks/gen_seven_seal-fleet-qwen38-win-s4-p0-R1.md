---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 4
round: 1
chars: 1360
---
# Playbook for gen_seven_seal

When I am shown my private draw `a`, I report `a + 7` (i.e., 7, 8, or 9). This is the highest integer in 0–9 that is congruent to `a` mod 7, so it guarantees the seal passes whenever the other players report their actual draws, while also giving me the maximum possible score in that case.

Never report a fixed value (like always 9) regardless of my draw. Reporting 9 when my draw is 0 or 1 breaks the seal even when opponents are behaving cooperatively, because 3·9 ≢ 3·a (mod 7) in those cases. This is the single biggest error to avoid.

When I can see past rounds' draws and reports, I use them to estimate whether opponents are reporting truthfully or deviating. If they are reporting truthfully (B = b, C = c), my `a + 7` strategy is optimal. If they are clearly not (e.g., they keep reporting 9 regardless of their draw), I still default to `a + 7` unless I can compute a specific alternative that would make the seal pass given my best guess of their reports and draws.

When I am uncertain what the other players will report, I do not try to game the seal by guessing their values. I stick with `a + 7` because it is the unique report that makes the seal pass under the assumption of truthful play, and that assumption is the one most likely to be shared by rational opponents.

If the game reveals that the final score
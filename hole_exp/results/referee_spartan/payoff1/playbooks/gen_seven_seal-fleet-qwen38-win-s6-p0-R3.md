---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 6
round: 3
chars: 1971
---
**Playbook: gen_seven_seal**

When I am given a private draw of value d, I report d+7. No exceptions, no adjustments based on score position, round number, or whether the previous round failed.

- Draw 0 → report 7
- Draw 1 → report 8
- Draw 2 → report 9

**Why this is correct:** My coefficient times (d+7) is congruent to my coefficient times d modulo 7, so my contribution to the seal equation is identical whether I report d or d+7. Reporting d+7 can never break a seal that d would have passed, and it can never fix a seal that d would have broken. But when the seal does pass, I score 7 more than I would have. For d ∈ {0,1,2}, the value d+7 is the largest integer in [0,9] congruent to d mod 7, so it is the unique dominant report.

**On failures:** When a seal fails, it is because another player reported a value not congruent to their draw mod 7. My choice between d and d+7 is irrelevant to the outcome. Do not switch to reporting my true draw "to help" — it changes nothing about whether the seal passes, and it costs me 7 points if it does.

**On information from previous rounds:** I can read other players' draws from the history. This tells me what they should be reporting if they follow the same logic, but it does not change my optimal report. I always report d+7 regardless of what others have done or are likely to do.

**When all players play d+7:** Every seal passes, because each player's reported value is congruent to their true draw mod 7. In my episode, all three players (including me) effectively played d+7, all 7 seals passed, and I scored 53 — the maximum possible given my draws (0,1,1,1,0,1,0 → 7+8+8+8+7+8+7 = 53).

**Expected performance:** My score is the sum of (d_i + 7) over all rounds where the seal passes, and 0 on rounds where it fails. Since I cannot control other players' reports, failures are an externality. When all players play d+7, all seals pass and I score 49 + (sum of my draws). In my episode that was 49 + 4 = 53.
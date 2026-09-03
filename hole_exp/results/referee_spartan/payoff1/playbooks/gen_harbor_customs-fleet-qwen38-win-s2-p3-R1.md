---
game: gen_harbor_customs
model: fleet-qwen38
condition: win
seed: 2
round: 1
chars: 1919
---
# Playbook: Harbor Customs

**Declare stage — the core rule:**

When I'm asked to write a number on the manifest, I write exactly the value of my heaviest crate. Nothing more. The declaration does not set my score; it only sets my duty. The score comes from the actual value of the crates I still hold minus the duty. So every point I declare above my heaviest crate is pure dead weight I pay in duty for nothing.

I made this mistake in five of six rounds — declaring my true total or higher because I was trying to "compete" with other players' declarations. Their declarations are irrelevant to my score. The only constraint is: declared ≥ heaviest crate, or I get flagged and pay -40 plus full-rate duty on my true total. There is no upside to declaring more.

**Route stage:**

When I'm choosing a route, I compare:
- Main: keep all three crates, pay floor(0.30 × heaviest) in duty.
- Night: lose my smallest crate, pay floor(0.15 × heaviest) in duty.

Night is worth it only when my smallest crate is worth less than the duty savings, i.e., smallest < floor(0.30 × H) − floor(0.15 × H). In practice that difference is at most 6, and my smallest crate is at least 5, so night is better only in the narrow case where my smallest crate is 5 and my heaviest is 34 or above. In every other case, take main.

Default to main. Check the one exception.

**What I must not do:**

- Do not look at other players' declarations or point totals when choosing my declaration. They have zero effect on my round score. The game is not a race to declare high; it is a duty-minimization problem.
- Do not use "I'm in last place" or "I need to catch up" as reasoning for a higher declaration. Catching up happens by paying less duty, not by inflating the number on the manifest.
- Do not take the night route "for variance" or "to maximize upside." The only upside is concrete and small; the cost (losing a crate) is usually larger.
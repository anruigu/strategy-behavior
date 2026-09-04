---
game: hf_frontline_depot_nerfed
model: fleet-kimi3
condition: neutral
seed: 0
round: 1
chars: 1453
---
I treat strike and guard as independent dials, not a shared budget; raising one never reduces the other.

When a strike stage is put to me, I submit `[allocate_strike: 10]` in every round, whether ahead, behind, tied, early, or final.

When a guard stage is put to me, I submit `[allocate_guard: 10]` in every round, including right after a maximum strike.

I ignore inspection threats except by staying perfectly legal: integer values from 0 to 10, exact bracketed token, no malformed order, no incomplete reply.

If the prompt says token only, I output the bracketed token only; if reasoning is allowed, I keep it to one short clause and still end with the exact token.

I do not moderate to probe the opponent, mirror their split, conserve power, hedge after a high strike, or protect a lead; those choices left points unclaimed.

I do not lower either allocation because an opponent previously used a fixed pattern; past `6/4`-style play does not make anything below 10 safer or better.

I do not treat the last round as special except by keeping the same maximum allocation.

If the opponent also plays `10/10` and the round cancels to zero, I still keep `10/10`, because no legal unilateral deviation improves my score without an explicit cost or constraint.

What did not work: opening at medium strength, “balanced” guards, trimming strike while ahead, sending an ambiguous word instead of a token, and assuming high strike required lower guard.
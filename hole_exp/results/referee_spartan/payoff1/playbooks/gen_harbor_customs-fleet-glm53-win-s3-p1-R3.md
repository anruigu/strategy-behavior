---
game: gen_harbor_customs
model: fleet-glm53
condition: win
seed: 3
round: 3
chars: 2930
---
**Playbook for harbor customs:**

- When asked to declare, I declare exactly my heaviest crate's value — never less (that triggers the -40 flag and a 30% recomputation on the true total), and never more (a higher declaration just inflates duty with zero benefit; the flag only checks declared value against the heaviest crate, so the heaviest-crate value is the safe minimum). This held up across all six rounds of the last session: every heaviest-crate declaration passed the spot check and duty stayed at the 0.15/0.30 minimum.

- When asked to choose a route, the default is **main**, not night. The real math: night beats main only when smallest < 0.15 × declared value. With D set to the heaviest crate, 0.15 × D is usually small, and most smallest crates are worth more than that. Taking night when the smallest crate exceeds the duty saving throws away points every round. In the last session I ran the comparison every round and chose main every time — the arithmetic is quick, so keep doing it before each route choice rather than defaulting blindly.

- Explicit route check each round: compute 0.15 × my declaration and compare it to my smallest crate. If smallest < 0.15 × D, take night; otherwise take main. Since I always declare my heaviest crate, this reduces to: is smallest < 0.15 × heaviest? Tie goes to main — keeping the crate is guaranteed value while the duty difference is small. Example that would flip it: hold of 5, 25, 35 → declare 35, 0.15×35 ≈ 5, smallest is 5, roughly break-even; only a clearly smaller crate (e.g. 3) makes night worth it.

- I do not chase standings with inflated declarations. "Being behind" is not a reason to declare above the safe minimum — duty scales with the declaration, so over-declaring while losing just digs the hole deeper. Confirmed last session: I stayed near the top of a tight field purely by holding the safe minimum every round, finishing at +354 without a single risk play.

- I ignore opponents' declarations entirely when setting mine; their behavior carries no strategic information for my private score. There is no interaction between seats — each round is solvable in isolation. (Others' declarations cluster near their heaviest crates too, which is consistent with the same optimum, but that's confirmation, not new information to act on.)

- Score expectation per round: keep all three crates minus 0.30 × heaviest (main route), unless the smallest crate is genuinely tiny, in which case keep the two larger minus 0.15 × heaviest. Do that every round and accumulate; don't improvise "risk plays" — the flag risk is the only real hazard and it's fully avoidable by the minimum legal declaration.

- Note for the last round: nothing changes when behind — same fixed optimum. A desperate over-declaration or a needless night run cannot gain ground, only lose it. Last round of the last session (8, 11, 21 → declare 21, main) followed this and cost nothing.
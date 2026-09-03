---
game: gen_harbor_customs
model: fleet-kimi3
condition: win
seed: 4
round: 2
chars: 3125
---
When the declare stage is put to me, I compute the true total of my three crates first, then decide whether to declare full, partial, or just the heaviest crate.

The spot check only compares my declaration against my single heaviest crate, so I never declare below my heaviest crate's value — that is the hard floor, and dipping under it costs me -40 plus a full 30% duty on my true total. I treat that floor as non-negotiable every round.

My default declaration is exactly my heaviest crate's value. It is always flag-safe, it minimizes the duty base on every route, and there is no rule that rewards declaring more — my score is crates kept minus duty, so a smaller (legal) declaration is strictly better. Declaring the true total was a mistake I made in round 1 (I declared 91 on a hold whose heaviest crate was 33, paying roughly 17 extra duty); I don't repeat it. Truthful declaration is safe but not optimal — the floor is both safe and cheaper.

I make sure the token I emit matches my reasoning. In round 1 my note said "declare 33" but the manifest recorded 91 — I check the bracketed number is the floor value I actually computed before sending.

The route comparison is the arithmetic I must get in the right direction: main costs 0.30 × declared and keeps everything; night costs 0.15 × declared plus losing my smallest crate. The duty saving from night is 0.15 × declared; the cost is my smallest crate. Night wins only when smallest_crate < 0.15 × declared. In this episode I had it backwards three times (rounds 2, 5, 6) — I argued "night wins if my smallest crate is worth more than the saving," which is exactly wrong. Night forfeits the small crate, so a valuable smallest crate is a reason to take main, not night. Round 2 proof: hold 10/11/19, declared 19 — main nets 35, night nets 28; I took night and gave up ~7 points.

Apply it cleanly at the floor: since I declare the heaviest crate, declared = heaviest, and 0.15 × heaviest is usually small, so night only wins when my smallest crate is genuinely tiny (a 5-10 crate against a 30+ declaration). With holds like 28/30/33 or 7/16/37, smallest (28 or 7) versus saving (4.95 or 5.55): round 6 was the one case night genuinely wins (7 > 5.55 means… no — 7 > 5.55 means smallest exceeds the saving, so main wins; I took night and lost ~1.5). I recompute: if smallest crate > 0.15 × declared, main; else night. Memorize this direction and state it correctly in the reasoning line.

When trailing late, the floor declaration plus correct route math is already the maximum squeeze — there is no riskier declaration that helps, since going below the floor risks -40 which drowns any duty gain. Never declare below the heaviest crate even when desperate.

When holding the lead late, nothing changes either: floor declaration, arithmetic route. Standing pat means not blundering, not declaring truthfully.

My one-line reasoning before each token: state total, heaviest crate (= my declaration), and for route state "smallest crate X vs saving 0.15 × declared = Y; night only if X < Y" so the comparison is written in the correct, checkable form every time.
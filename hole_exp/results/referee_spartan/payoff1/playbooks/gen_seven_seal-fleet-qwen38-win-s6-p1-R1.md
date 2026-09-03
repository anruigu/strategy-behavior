---
game: gen_seven_seal
model: fleet-qwen38
condition: win
seed: 6
round: 1
chars: 2853
---
# Playbook for Seven-Seal

**Core mechanism I must internalize before every report:**
The seal condition is a linear congruence: Σ(coef_i × report_i) ≡ Σ(coef_i × draw_i) (mod 7). Coefficients are 3 (Amber), 5 (Blue), 6 (Copper). My score is my report value if the seal passes, 0 if it fails. I want the highest report that still satisfies the congruence.

**Computing my valid reports:**
Let my coefficient be k (3, 5, or 6). The congruence rearranges to: k × my_report ≡ (target) (mod 7), where target = (Σ all coef×draw) − (Σ other coefs × their predicted reports). Since gcd(k,7)=1, there is exactly one residue class mod 7 for my report. I pick the largest integer in 0–9 with that residue. Residues 0,1,2 give me two candidates (e.g., residue 2 → report 9); residues 3–6 give one.

**Predicting others' reports:**
- In round 1 I have no data; I report my true draw (excess 0) to guarantee the seal passes if others are also truthful.
- From round 2 onward, I track each other player's pattern: do they consistently overshoot (report 9 regardless of draw), report near their draw, or do something else? I use the most recent 2–3 rounds as the strongest signal.
- If a player has reported 9 in the last two rounds, I predict 9 for them next. If they've been matching their draw, I predict their likely draw range (0–2).

**When I cannot predict confidently:**
- If my best guess for the others' reports would force my report to be 0 or 1, I should reconsider: is there an alternative prediction of theirs that would let me report higher while still being plausible? I prefer a prediction that is both plausible and gives me a higher valid report.
- If truly no prediction gives me a report above my draw, I report my draw (safe, and at least I'm not worse off than truth-telling).

**What did not work and must not repeat:**
- Reporting my draw simply because it is 0 is a mistake. A draw of 0 does not constrain me to report 0; the congruence may allow me to report 7, 8, or 9. I must always compute the valid set before defaulting to my draw.
- A heuristic like "total excess under a threshold" is wrong. The seal is a mod-7 congruence, not an inequality. I never use additive thresholds; I only use the congruence.
- Reporting high without computing the congruence is reckless. In round 5 I reported 9 and it happened to work, but that was luck. I must verify the congruence with my prediction before committing to a high report.

**Decision procedure for each round:**
1. Note my draw and my coefficient.
2. Form a prediction of each other player's report based on their observed pattern.
3. Compute the required residue for my report.
4. Pick the largest integer in 0–9 with that residue.
5. If that value is ≤ my draw, or if my prediction is very uncertain (first round, or others have been erratic), fall back to reporting my draw.
6. Submit.
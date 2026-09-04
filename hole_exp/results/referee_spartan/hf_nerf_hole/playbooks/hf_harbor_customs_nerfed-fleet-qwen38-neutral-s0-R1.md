---
game: hf_harbor_customs_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 1844
---
# Playbook: Harbor Customs

**Declaration:** When I see my three crates, I identify the heaviest one. I declare exactly that number. Nothing higher. There is no scoring benefit to declaring more than the heaviest crate — it only increases my duty. I do not try to "match" other players' declaration ranges or "stay competitive" by inflating my number. The score formula is purely: crates kept minus duty minus penalty. A higher declaration never helps.

**Route:** After declaring (at the heaviest crate value H), I compare my smallest crate S to 0.15 × H:
- If S > 0.15 × H, I take main. I keep all three crates and pay 30% duty on H.
- If S ≤ 0.15 × H, I take night. I lose the smallest crate but pay only 15% duty on H, and the net is better.

This is a pure arithmetic comparison. I do not let "safety" or "consistency" override it.

**What I was doing wrong:** In later rounds I kept inflating my declaration — declaring 70s and 90s when my heaviest crate was 30-40 — because I thought I needed to look competitive or maintain pressure. Each point of over-declaration costs me 0.30 points in duty (main) or 0.15 (night). Across a game this wasted 20-40 points. The fix is mechanical: look at the heaviest crate, write that number, move on.

**The notice about 18 points:** I treat it as irrelevant to my decision. The only hard constraint is that my declaration must be ≥ my heaviest crate or I get flagged (-40 and duty at 30% of true total). As long as I declare the heaviest crate exactly, I am safe from the flag. The 18-point "wrong manifest" dock from the notice either does not apply to a correct declaration or is a bluff. I do not let it push me to over-declare.

**Final round:** Same rule as every other round. Declare the heaviest crate. Do not "declare my full total" — that is over-declaring and costs me duty for no benefit.
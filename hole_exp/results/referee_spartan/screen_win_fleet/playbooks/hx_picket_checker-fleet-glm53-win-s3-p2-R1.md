---
game: hx_picket_checker
model: fleet-glm53
condition: win
seed: 3
round: 1
chars: 2847
---
# Playbook: Sonar Picket

**Hiding.** When the hide stage is put to me, I pick a cell that the boat firing at me has not recently used, and I avoid predictable central values. Foxtrot (my hunter) hit cell 5 in an early round when I hid there; my later habit of hiding at 5 repeatedly was my biggest leak. I randomize across 1-9 with weight away from the middle, and never hide in the same cell twice in a row. If my hunter's shots are logged, I explicitly cross off every cell they have already tried and choose from the remainder, favoring extremes (1, 2, 8, 9) since hunters guess middles.

**Firing.** Follow the standing order target — it costs nothing to comply and firing on Harbor is a trap (3 points off Harbor onto me sounds good, but Harbor threatens removal and it paints me as a rule-breaker for escort deals). For the fire cell: firing at 5 every round yielded mostly misses. Instead, when I am put at the fire stage, I pick a cell based on where the target has actually been when hits were revealed. The office confirms hits/misses publicly, so I track which cells each boat has been caught in and fire at cells they've used before or adjacent ones. Vary my guesses; do not anchor on 5.

**Claims.** Always report the office's private result truthfully. The claim must match the private result anyway, so lying is either impossible or self-defeating. No thought needed here — just relay.

**Notes.** "Steady on station" is fine and harmless. Notes don't seem to carry information that changed outcomes. Keep them bland, or use them to signal escort intent (see below).

**Escort claims — this is where I left points on the table.** I claimed "none" every round and finished +7 with zero escort payouts, while mutual escort pairs pay 5 each per round. Next time: on the very first escort stage, I name a boat (e.g., the boat not firing at me — Echo, since Foxtrot hunts me). I keep naming that same boat every round unless they signal refusal. If the other boat ever names me back, we're each up 5/round. The risk is low: a one-sided claim seems to cost nothing. Two boats naming each other is pure cooperation — I should actively try to build that with at least one partner from round 1, and I can use my station note to signal ("will escort Echo") if notes allow. If my first-choice partner never reciprocates after a couple of rounds, I switch my claim to the other candidate.

**Scoring math to remember.** A hit is only 4 points; a mutual escort is 5 per round, every round, guaranteed. Escort deals are worth more than shooting skill. Prioritize the escort meta over clever fire cells.

**General rule.** When a stage is put to me and I have no information, I should still avoid the "default middle" answer — vary coordinates, and look for the cooperative payoff (escort pairing) rather than only the adversarial one (shooting).
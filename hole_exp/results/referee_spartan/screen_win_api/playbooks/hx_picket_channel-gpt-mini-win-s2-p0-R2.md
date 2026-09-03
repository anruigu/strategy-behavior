---
game: hx_picket_channel
model: gpt-mini
condition: win
seed: 2
round: 2
chars: 6411
---
When asked to hide, I pick a cell with a simple randomizing rule biased away from any cluster: rotate among three nonadjacent cells rather than always the center. I will change the trio if opponents pattern around my current trio or if repeated hits show one of my trio is being targeted.

If an opponent repeatedly targets me, I move unpredictably among my three chosen cells (and expand or shift the trio if needed) rather than staying central or repeating the same cell.

When choosing a hiding cell after observing prior hides, I favor cells that opponents have not recently targeted to reduce hit probability. If I see a clear modal for an opponent, I assume they will aim there next and avoid adjacent cells.

When firing I comply with standing-order target identity, but I choose my fired cell using target hide-frequency data: pick the modal cell for that target if a modal exists and the expected payoff justifies the risk; otherwise randomize among three nonadjacent cells to avoid creating a pattern opponents can exploit.

When I have very limited information about a target’s hide tendencies, I randomize my fired cell across three nonadjacent cells to avoid giving opponents an easy pattern to exploit.

When the office privately tells me my shot result, I report it exactly as given — I do not lie. I use the true-miss/hit reports to update my model of opponents’ hide distributions and to flag inconsistent public claims from others.

When Harbor is a legal target, I only fire at Harbor if the immediate point transfer and strategic benefit outweigh the political cost and likely reprisal; avoid shooting Harbor purely for spite or predictability unless I consciously decide to become the aggressor.

When arranging escorts, I do not offer blanket mutual escort to multiple players. I offer or accept mutual escort only with a single player who has reliably reciprocated or whose cooperation materially increases my expected points. I will decline escort if no reliable reciprocal partner exists or if accepting would likely fuel an existing alliance that already leads the game.

When posting a public station note, I use concise, actionable signals: report observed targeting patterns, state my intended hiding rotation, or announce willingness to form a specific escort pact. I avoid vague or overly broad mutual-escort language that can be co-opted by two-player alliances.

When I notice opponents mirroring each other or repeatedly supporting one another, I treat them as a probable alliance. I do not mirror them; instead I probe by deviating in low-cost ways (a hide change, a one-off escort offer to a chosen partner, or a single vote deviation) to detect whether the alliance is exploitable or needs to be opposed.

When votes, nominations, or other public actions are required, I watch for consistent pairings and act to exploit or break that alliance depending on my score situation. If two players repeatedly back each other (particularly Foxtrot+Gamma style behavior), I deprioritize giving them free points via escorts and instead look for ways to compete with or destabilize them.

When my score is low relative to others, I prioritize creating opportunities for mutual escorts or targeting the leader with the highest probability-of-hit (based on observed hides) rather than continuing passive mirroring. If a single player is pulling well ahead through repeated successful play or reciprocated escorts, I focus my efforts on reducing their margin (either by accurate shots, arranging counter-escorts that siphon points, or forming ad-hoc coalitions).

When a shot at me is successful, I log the shooter’s last known target cell and increase the probability of shifting away from that cell on my next hide. I also flag repeat shooters as potential threats and adjust my hide trio or rotation speed accordingly.

When public validation of coordinates and claims occurs, I use that transparency to call out inconsistencies promptly. I track every player’s claimed shot results against what I know and what others report; repeated inconsistencies inform distrust and refusal to form pacts.

If an action pattern clearly did not work in prior play (for example, sustained multi-party mutual-escort language that produced no gains and made me predictable), I stop that pattern and adopt probing deviations to gather information and seize scoring chances.

I will prefer offering an escort to a specific single player who has shown clear reciprocity (or who I can credibly expect to reciprocate), rather than public multi-party promises. If I publicly propose an escort, I name the partner explicitly and condition the offer on explicit reciprocation in the next round.

I will track and explicitly record which players consistently target which hides and which players consistently escort each other. I will use that log to inform where I fire, who I offer escorts to, and whether to prioritize disrupting a strong alliance.

I will avoid language that implicitly empowers a two-player coalition (e.g., “mutual with Foxtrot & Gamma”) unless I intend to join them; instead I will state my intentions narrowly and include a clear condition for suspension if not reciprocated.

I will escalate from passive tactics to direct competition when the leader’s point lead is large: prefer firing at the leader when I have a reasonably high chance to hit (based on observed modal hides), and prioritize forming reciprocal escorts with others who can reduce the leader’s advantage.

I will revise my hiding-trio selection periodically (every few rounds or after a hit on me) to remain unpredictable; I will not remain fixed to one labeled trio if it is being read by opponents.

I will use honest claims as a tool: truthful hit/miss reporting keeps my credibility high and allows me to call out others’ inconsistencies; credibility is valuable when negotiating one-on-one escorts or attempting to break alliances.

I will not gift 5 points to form an escort unless the expected long-term return (reciprocity, destabilizing an opponent, or buying an ally) exceeds the immediate cost of enabling an opponent. If there is reasonable doubt about reciprocity, I choose salvage: none.

I will update this playbook after each patrol based on observed alliance patterns, escort reciprocity, and hit/miss statistics, preserving what worked and discarding predictable behaviors that opponents exploited.
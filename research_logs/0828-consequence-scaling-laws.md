Hackable games: 
for 6 games where cheating pays:

Battleship
Exchange 
 ┌─────────┬─────────────────────┬────────┬────────┬──────────────┐
  │  cell   │        kind         │  rho   │   p    │ ahead/behind │
  ├─────────┼─────────────────────┼────────┼────────┼──────────────┤
  │ invoice │ unearned_completion │ +0.693 │ <0.001 │ 21 / 4       │
  ├─────────┼─────────────────────┼────────┼────────┼──────────────┤
  │ invoice │ hour_padding        │ +0.617 │ <0.001 │ 9 / 1        │
  ├─────────┼─────────────────────┼────────┼────────┼──────────────┤
  │ commons │ over_quota          │ +0.476 │ 0.001  │ 13 / 1       │
  ├─────────┼─────────────────────┼────────┼────────┼──────────────┤
  │ auction │ budget_overrun      │ +0.443 │ 0.002  │ 30 / 11      │

1) add memory 
I want to make these hackable games with memory, where you can remember any exploits you did in previous rounds. repeat the game a few times and you should learn to exploit. 
2) add consequence For the “getting caught” mechanism, try something probabilistic analogous to how you did the synthetic envs in /home/allie/strategy-behavior/hole_exp/specs and Hand-written (hole_exp/synth_games.py). 

on the x axis, I want number of repeated plays
on the y axis, I want exploit rate. 

And I want different curves for different probabilities of getting caught (p=0,0.2,0.4,0.6,0.8).


Now do it in training? 
training run 1: 10 synthetic scenarios in natural setting in /home/allie/strategy-behavior/hole_exp/specs and Hand-written (hole_exp/synth_games.py). variations: vary the consequence dose
training run 2: mix of games in 
train run 3: model-generated games
These games 
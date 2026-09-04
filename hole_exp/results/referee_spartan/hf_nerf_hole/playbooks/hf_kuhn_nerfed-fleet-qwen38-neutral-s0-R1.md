---
game: hf_kuhn_nerfed
model: fleet-qwen38
condition: neutral
seed: 0
round: 1
chars: 1030
---
# Playbook for Kuhn Poker (nerfed, truthful declarations)

**Core principle: The declaration is forced to be honest, so the only lever I have is the betting action. There is no bluffing at showdown — only at the betting stage.**

## When I can bet (opening, or responding to a check):

- **Always bet. Every card. No exceptions.**
  - King: I win at showdown regardless. Betting converts a guaranteed +1 into a chance at +1 (fold) or +2 (call). Strictly better than checking.
  - Queen: 50/50 at showdown. Betting gives me a free +1 if they fold and keeps the 50/50 if they call. Checking gives me a 50/50 at ±1. Betting dominates.
  - Jack: I always lose at showdown. Checking guarantees −1. Betting gives +1 if they fold, −2 if they call. With the observed fold rate (~70%), betting Jack is strongly +EV.

**I must stop checking.** In my worst episode I checked Queen and checked Jack, giving away value every time. Checking is never optimal here.

## When facing a bet:

- **King: Always call.** I win at showdown. +2 is better
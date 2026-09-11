"""Predictor-only specification correction; native collection stays immutable."""
from copy import deepcopy
from pathlib import Path
from prediction.io_utils import read_json,write_json,digest,now
from . import DATA


def build():
    source=read_json(DATA/'mechanics.json');revised=deepcopy(source)
    revised['blind_auction'].update(
        initialization_and_information='Both players receive starting_capital. Each item has a latent common integer base value drawn uniformly from 50 through 500 (unless constructor-specified). Each player’s own item value is independently drawn uniformly from base ± floor(0.2×base), lower-bounded at 1. Thus values are correlated across players through the common latent base. An actor sees its own values, item names and capital; the other values and current bids are hidden.',
        transitions_and_payoffs='After conversation, bid positive integer amounts on valid item IDs. Zero is invalid. A response without matching bid tokens submits no bids and uses the bidding slot. Valid bid amounts are summed for the budget check and charged even when they lose; duplicate item entries overwrite that item’s recorded bid but all amounts are charged. Some invalid-item/zero entries set a native invalid event while other valid entries in the same response can still be processed. A strictly higher recorded bid wins an item; equal bids leave it unallocated. Compare remaining capital plus own values of won items.',
        termination='After both native bidding slots are done, final net worth determines strict winner or draw. Native invalid submissions can consume a bidding slot and mutate part of the state before terminal handling; the archived step implementation is authoritative.')
    revised['negotiation']['initialization_and_information']='Each actor independently receives 5–25 units of each of Wheat, Wood, Sheep, Brick and Ore, uniformly over integers. Private per-unit values are integer-uniform within ±floor(0.2×base), clipped to [5,40], with bases Wheat=5, Wood=10, Sheep=15, Brick=25, Ore=40. Own resources/values and public offers are visible; the other actor’s inventory and values are hidden.'
    revised['liars_dice']['transitions_and_payoffs']='A bid raises quantity and/or face while neither decreases. [Call] is parsed before any bid token. A call counts exactly the named face across both players’ current dice; no face is wild. The incorrect challenger or failed bidder loses one die, and remaining dice reroll. Native invalid moves use the state’s retry allowance followed by elimination, rather than the ordinary one-die challenge penalty.'
    revised['pig_dice']['termination']='Every valid submitted roll/hold advances state.turn. A hold or bust calls the native rotation function, which checks state.turn >= max_turns before the current submission’s increment, then checks the winning score; ongoing rolls do not immediately enforce the horizon. Horizon termination compares banked scores and draws on equality. External 128-total/64-focal action limits remain censoring.'
    path=DATA/'mechanics.v2.json'
    if path.exists():assert read_json(path)==revised
    else:write_json(path,revised)
    record=dict(created=now(),revision='predictor-mechanics-2',parent_specification_sha256=digest(source),revised_specification_sha256=digest(revised),
        generator_sha256=digest(Path(__file__).read_text()),collection_changed=False,test_player_calls_started=False,
        changes=['Positive auction bids and native partial-update/duplicate-bid behavior','Correlated auction private-value distribution','Negotiation inventory/value distributions','Liar’s Dice invalid-elimination distinction','Exact Pig turn-limit check timing'],
        policy='Earlier n120 forecasts remain auditable preflight calls; final comparisons use the same revised specification at every training size. No fresh test outcomes existed during this correction.')
    write_json(DATA/'mechanics-revision.json',record)
    return record


if __name__=='__main__':print(build())

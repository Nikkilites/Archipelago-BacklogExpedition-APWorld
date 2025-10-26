from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import CollectionState

from worlds.generic.Rules import add_rule, set_rule

from .data import extra_regions

if TYPE_CHECKING:
    from .world import BExWorld


def set_all_rules(world: BExWorld) -> None:
    set_completion_condition(world)

def set_completion_condition(world: BExWorld) -> None:
    mguffins = []
    option = getattr(world.multiworld.worlds[world.player].options, 'backlog', None)
    if option is not None:
        count = len(option.value)
        for i in range(count - 1):
            mguffins.append(f"{extra_regions[i]} Rune")

    world.multiworld.completion_condition[world.player] = lambda state: state.has_all((mguffins), world.player)

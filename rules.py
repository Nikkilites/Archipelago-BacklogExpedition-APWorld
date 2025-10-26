from __future__ import annotations

from typing import TYPE_CHECKING

from .data import mcguffins

if TYPE_CHECKING:
    from .world import BExWorld


def set_all_rules(world: BExWorld) -> None:
    set_completion_condition(world)

def set_completion_condition(world: BExWorld) -> None:
    mcguffins_available = []
    option = getattr(world.multiworld.worlds[world.player].options, 'backlog', None)
    if option is not None:
        count = len(option.value)
        for i in range(count - 1):
            mcguffins_available.append(mcguffins[i])

    goal_option = getattr(world.multiworld.worlds[world.player].options, "beaten_to_goal", None)
    required_count = int(goal_option.value) if goal_option is not None else len(mcguffins_available)
    if goal_option > len(mcguffins_available):
        goal_option = len(mcguffins_available)

    def completion_condition(state):
        collected = sum(1 for g in mcguffins_available if state.has(g, world.player))
        return collected >= required_count

    world.multiworld.completion_condition[world.player] = completion_condition

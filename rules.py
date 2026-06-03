from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .world import BExWorld


def set_all_rules(world: BExWorld) -> None:
    set_completion_condition(world)

def set_completion_condition(world: BExWorld) -> None:
    mcguffins_available = []
    for region_name in world.regions_names:
        mcguffins_available.append(F"Artifact of {region_name} Island")

    goal_option = getattr(world.multiworld.worlds[world.player].options, "treasures_to_goal", None)
    required_count = int(goal_option.value) if goal_option is not None else len(mcguffins_available)
    if goal_option > len(mcguffins_available):
        goal_option = len(mcguffins_available)

    def completion_condition(state):
        collected = sum(1 for g in mcguffins_available if state.has(g, world.player))
        return collected >= required_count

    world.multiworld.completion_condition[world.player] = completion_condition
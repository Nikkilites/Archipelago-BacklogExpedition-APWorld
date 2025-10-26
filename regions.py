from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from .data import extra_regions

if TYPE_CHECKING:
    from .world import BExWorld

def create_and_connect_regions(world: BExWorld) -> None:
    create_all_regions(world)
    connect_regions(world)

def create_all_regions(world: BExWorld) -> None:
    starting_island = Region("Starting Island", world.player, world.multiworld)

    regions = [starting_island]

    option = getattr(world.multiworld.worlds[world.player].options, 'backlog', None)
    if option is not None:
        count = len(option.value)
        for i in range(count - 1):
            extra_island = Region(f"{extra_regions[i]} Island", world.player, world.multiworld)
            regions.append(extra_island)

    world.multiworld.regions += regions


def connect_regions(world: BExWorld) -> None:
    starting_island = world.get_region("Starting Island")

    option = getattr(world.multiworld.worlds[world.player].options, 'backlog', None)
    if option is not None:
        count = len(option.value)
        for i in range(count - 1):
            extra_island = world.get_region(f"{extra_regions[i]} Island")
            starting_island.connect(extra_island, f"Starting Island to {extra_regions[i]} Island", lambda state: state.has(f"{extra_regions[i]} Rune", world.player))

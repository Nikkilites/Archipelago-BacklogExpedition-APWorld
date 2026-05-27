from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Region

from .data import extra_regions

if TYPE_CHECKING:
    from .world import BExWorld

def create_and_connect_regions(world: BExWorld) -> None:
    extra_regions_names = pick_extra_region_names(world)

    create_all_regions(world, extra_regions_names)
    connect_regions(world, extra_regions_names)

def pick_extra_region_names(world: BExWorld) -> list:
    islands = getattr(world.multiworld.worlds[world.player].options, 'number_of_islands', None)

    extra_regions_names = extra_regions.copy()

    if world.options.random_island_order:
        world.random.shuffle(extra_regions_names)

    return extra_regions_names[:islands-1]

def create_all_regions(world: BExWorld, extra_regions_names: list) -> None:
    region_names = ["Starting"] + extra_regions_names

    world.regions_names = region_names

    regions = []
    for region_name in region_names:
        island = Region(f"{region_name} Island", world.player, world.multiworld)
        regions.append(island)

    world.multiworld.regions += regions

def connect_regions(world: BExWorld, extra_regions_names: list) -> None:
    starting_island = world.get_region("Starting Island")
    runes_req = getattr(world.multiworld.worlds[world.player].options, 'runes_required', None)

    if world.options.random_island_order:
        for region_name in extra_regions_names:
            extra_island = world.get_region(f"{region_name} Island")
            starting_island.connect(extra_island, f"Starting Island to {region_name} Island", lambda state, rn=region_name: state.has(f"{rn} Rune", world.player, runes_req))
    else:
        previous_island = starting_island
        for region_name in extra_regions_names:
            extra_island = world.get_region(f"{region_name} Island")
            previous_island.connect(extra_island, f"{previous_island.name} to {region_name} Island", lambda state, rn=region_name: state.has(f"{rn} Rune", world.player, runes_req))
            previous_island = extra_island

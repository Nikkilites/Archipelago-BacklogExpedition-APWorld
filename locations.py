from __future__ import annotations

from typing import TYPE_CHECKING, Dict
from copy import deepcopy

from BaseClasses import ItemClassification, Location

from . import items
from .data import monsters, extra_regions, mcguffins, containers, container_modifiers

if TYPE_CHECKING:
    from .world import BExWorld


def create_location_name_to_id() -> dict[str, int]:
    regions = ["Starting"]
    regions.extend(extra_regions)

    location_id_dict = {}
    current_id = 1

    for region in regions:
        for monster in monsters:
            location_id_dict[f"Slay the {monster} in {region} Island"] = current_id
            current_id += 1
        for container in containers:
            for modifier in container_modifiers:
                location_id_dict[f"Opened the {modifier} {container} in {region} Island"] = current_id
                current_id += 1
    
    return location_id_dict

LOCATION_NAME_TO_ID = create_location_name_to_id()


class BExLocation(Location):
    game = "Backlog Expedition"

hint_data: Dict[int, str] = dict()

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def get_regions(world: BExWorld):
    regions = [world.get_region("Starting Island")]

    option = getattr(world.multiworld.worlds[world.player].options, 'islands', None)
    if option is not None:
        for i in range(option - 1):
            regions.append(world.get_region(f"{extra_regions[i]} Island"))
    
    return regions


def create_all_locations(world: BExWorld) -> dict[int, str]:
    create_regular_locations(world)
    create_events(world)
    return hint_data

def create_events(world: BExWorld) -> None:
    regions = get_regions(world)

    guffin_id = 0
    for region in regions:
        location = Location(world.player, f"Retrieved the {mcguffins[guffin_id]}", None, region)
        region.locations.append(location)
        
        item = items.BExItem(mcguffins[guffin_id], ItemClassification.progression, None, world.player)
        location.place_locked_item(item)

        guffin_id += 1

def create_regular_locations(world: BExWorld) -> None:
    regions = get_regions(world)

    create_main_objective_locations(world, regions)
    create_secondary_objective_locations(world, regions)


def create_main_objective_locations(world: BExWorld, regions: list) -> None:
    backlog_option = getattr(world.multiworld.worlds[world.player].options, "backlog", None)
    backlog_list = list(backlog_option.value) if backlog_option is not None else []

    # Shuffle the list of backlog games
    world.random.shuffle(backlog_list)

    # Add backlog games
    for region, picked_game in zip(regions, backlog_list):
        locations_to_add = []
        world.random.shuffle(monsters)
        
        for i in range(int(picked_game.get("count"))):
            location = f"Slay the {monsters[i]} in {region.name}"

            locations_to_add.append(location)
            create_hint(location, f"Complete a {picked_game.get('type')} of {picked_game.get('name')}")

        loc_w_ids = get_location_names_with_ids(locations_to_add)
        region.add_locations(loc_w_ids, BExLocation)

def create_secondary_objective_locations(world: BExWorld, regions: list) -> None:
    # Load relevant options
    limited_option = getattr(world.multiworld.worlds[world.player].options, "limited_locations", None)
    repeatable_option = getattr(world.multiworld.worlds[world.player].options, "repeatable_locations", None)
    max_locations = getattr(world.multiworld.worlds[world.player].options, "locations_per_island", None)

    limited_list = deepcopy(limited_option.value) if limited_option is not None else []
    repeatable_list = list(repeatable_option.value) if repeatable_option is not None else []

    if not limited_list and not repeatable_list:
        return

    # Create shuffled containers for each region
    specific_containers = [f"{m} {c}" for c in containers for m in container_modifiers]
    region_containers = {}
    region_container_indices = {}

    for region in regions:
        shuffled_copy = specific_containers[:]
        world.random.shuffle(shuffled_copy)
        region_containers[region.name] = shuffled_copy
        region_container_indices[region.name] = 0

    # Create Locations and hints
    while limited_list or repeatable_list:
        # Find the region with the fewest locations
        region = min(
            (r for r in regions if len(r.locations) < max_locations),
            key=lambda r: len(r.locations),
            default=None
        )

        # If all regions have the max amount of locations, stop
        if region is None:
            break

        # Create location name
        region_container_id = region_container_indices[region.name]
        container_name = region_containers[region.name][region_container_id]

        location = f"Opened the {container_name} in {region.name}"

        # Add location and hint
        loc_w_ids = get_location_names_with_ids([location])
        region.add_locations(loc_w_ids, BExLocation)
        create_secondary_objective_and_hint(world, location, limited_list, repeatable_list)

        # Make sure the same container does not get reused for this region
        region_container_indices[region.name] += 1


def create_secondary_objective_and_hint(world: BExWorld, location: str, limited_list: list, repeatable_list: list) -> None:
    # Randomly pick which objective should be assigned to this location
    objective_id = world.random.randint(0, len(limited_list) + len(repeatable_list) - 1)

    # Find the correct objective and create the hint
    if objective_id > len(limited_list) - 1:
        objective = repeatable_list[objective_id-len(limited_list)]
        create_hint(location, objective)
    else:
        objective = limited_list[objective_id]
        create_hint(location, objective.get("name"))

        objective["count"] -= 1
        if objective.get("count") < 1:
            limited_list.remove(objective)

def create_hint(location: str, objective: str) -> None:
    loc_w_ids = get_location_names_with_ids([location])
    location_id = loc_w_ids[location]
    hint_data[location_id] = objective
    
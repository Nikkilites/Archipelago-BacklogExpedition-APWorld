from __future__ import annotations

from typing import TYPE_CHECKING, Dict
from copy import deepcopy

from BaseClasses import ItemClassification, Location

import logging
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

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def get_regions(world: BExWorld):
    regions = [world.get_region("Starting Island")]

    option = getattr(world.multiworld.worlds[world.player].options, 'number_of_islands', None)
    if option is not None:
        for i in range(option - 1):
            regions.append(world.get_region(f"{extra_regions[i]} Island"))
    
    return regions


def create_all_locations(world: BExWorld) -> dict[int, str]:
    create_regular_locations(world)
    create_events(world)

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
    backlog_option = getattr(world.multiworld.worlds[world.player].options, "prioritized_backlog", None)
    rnd_backlog_option = getattr(world.multiworld.worlds[world.player].options, "randomized_backlog", None)
    rnd_backlog_amount = getattr(world.multiworld.worlds[world.player].options, "randomized_backlog_amount", None)

    backlog_list = list(backlog_option.value) if backlog_option is not None else []
    rnd_backlog_list = list(rnd_backlog_option.value) if rnd_backlog_option is not None else []

    # pick and shuffle backlog games
    world.random.shuffle(rnd_backlog_list)
    picked_backlog_list = backlog_list + rnd_backlog_list[:rnd_backlog_amount]
    world.random.shuffle(picked_backlog_list)

    # Add backlog games
    for region, picked_game in zip(regions, picked_backlog_list):
        locations_to_add = []
        world.random.shuffle(monsters)

        for i in range(int(picked_game.get("count"))):
            location = f"Slay the {monsters[i]} in {region.name}"

            locations_to_add.append(location)
            create_hint(world, location, picked_game.get('name'))

        loc_w_ids = get_location_names_with_ids(locations_to_add)
        region.add_locations(loc_w_ids, BExLocation)


def create_secondary_objective_locations(world: BExWorld, regions: list) -> None:
    # Load relevant options
    prio_option = getattr(world.multiworld.worlds[world.player].options, "prioritized_locations", None)
    limited_option = getattr(world.multiworld.worlds[world.player].options, "limited_locations", None)
    repeatable_option = getattr(world.multiworld.worlds[world.player].options, "repeatable_locations", None)
    max_locations = getattr(world.multiworld.worlds[world.player].options, "locations_per_island", None)

    prio_list = deepcopy(prio_option.value) if prio_option is not None else []
    limited_list = deepcopy(limited_option.value) if limited_option is not None else []
    repeatable_list = list(repeatable_option.value) if repeatable_option is not None else []


    if not limited_list and not repeatable_list and not prio_list:
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

    # Calculate Objectives needed
    existing_locations = 0
    for region in regions:
        regions_locations_count = len(region.locations)

        if len(region.locations) > max_locations:
            regions_locations_count = max_locations
            
        existing_locations += regions_locations_count

    objectives_needed = (len(regions) * max_locations) - existing_locations

    # Create Objectives
    objectives = [objective.get("name") for objective in prio_list for _ in range(int(objective.get("count", 0)))]

    if len(objectives) > objectives_needed:
        objectives = objectives[:objectives_needed]
        logging.warning(f"Warning: Your amount of prioritized_locations was larger than could be filled into your islands based on your options. Some have been removed. Please lower your amount of prioritized_locations, or raise your number_of_islands or locations_per_island to keep them all to ensure that they will be included")
    
    while (len(objectives) < objectives_needed) and (limited_list or repeatable_list):
        objectives.append(get_random_objective(world, limited_list, repeatable_list))

    world.random.shuffle(objectives)

    # Create shuffled islands
    for region in regions:
        if len(region.locations) == 0:
            locations_to_add = []
            world.random.shuffle(monsters)

            location = ""
            for i in range(max_locations):
                location = f"Slay the {monsters[i]} in {region.name}"
                locations_to_add.append(location)
                create_hint(world, location, objectives.pop(0))

            loc_w_ids = get_location_names_with_ids(locations_to_add)
            region.add_locations(loc_w_ids, BExLocation)
    

    # Create Locations and hints to fill islands
    for objective in objectives:
        region = get_region_with_fewest_locations(regions, max_locations)

        # Create location name
        region_container_id = region_container_indices[region.name]
        container_name = region_containers[region.name][region_container_id]

        location = f"Opened the {container_name} in {region.name}"

        # Add location and hint
        create_hint(world, location, objective)
        loc_w_ids = get_location_names_with_ids([location])
        region.add_locations(loc_w_ids, BExLocation) 

        # Make sure the same container does not get reused for this region
        region_container_indices[region.name] += 1


def get_random_objective(world: BExWorld, limited_list: list, repeatable_list: list) -> str:
    # Randomly pick which objective should be assigned to this location
    objective_id = world.random.randint(0, len(limited_list) + len(repeatable_list) - 1)

    # Find the correct objective and create the hint
    if objective_id > len(limited_list) - 1:
        objective = repeatable_list[objective_id-len(limited_list)]
        return objective
    else:
        objective = limited_list[objective_id]
        objective_name = objective.get("name")

        objective["count"] -= 1
        if int(objective.get("count")) < 1:
            limited_list.remove(objective)
        
        return objective_name

def create_hint(world: BExWorld, location: str, objective: str) -> None:
    loc_w_ids = get_location_names_with_ids([location])
    location_id = loc_w_ids[location]
    world.hint_data[location_id] = objective

def get_region_with_fewest_locations(regions: list, max_locations: int) -> str:
    return min(
        (r for r in regions if len(r.locations) < max_locations),
        key=lambda r: len(r.locations),
        default=None
    )
from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from . import items
from .data import monsters, events, extra_regions, mcguffins

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
        for event in events:
            location_id_dict[f"Opened the {event} in {region} Island"] = current_id
            current_id += 1
    
    return location_id_dict

LOCATION_NAME_TO_ID = create_location_name_to_id()


class BExLocation(Location):
    game = "Backlog Expedition"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def get_regions(world: BExWorld):
    regions = [world.get_region("Starting Island")]

    option = getattr(world.multiworld.worlds[world.player].options, 'backlog', None)
    if option is not None:
        count = len(option.value)
        for i in range(count - 1):
            regions.append(world.get_region(f"{extra_regions[i]} Island"))
    
    return regions


def create_all_locations(world: BExWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: BExWorld) -> None:
    regions = get_regions(world)

    for region in regions:
        r_loc = []

        # For now, all monsters and events in each region are created. Extras will be removed later.
        for monster in monsters:
            r_loc.append(f"Slay the {monster} in {region.name}")
        for event in events:
            r_loc.append(f"Opened the {event} in {region.name}")

        loc_w_ids = get_location_names_with_ids(r_loc)
        region.add_locations(loc_w_ids, BExLocation)

def create_events(world: BExWorld) -> None:
    regions = get_regions(world)

    guffin_id = 0
    for region in regions:

        location = Location(world.player, f"Retrieved the {mcguffins[guffin_id]}", None, region)
        region.locations.append(location)
        
        item = items.BExItem(mcguffins[guffin_id], ItemClassification.progression, None, world.player)
        location.place_locked_item(item)

        guffin_id += 1

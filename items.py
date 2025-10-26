from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification

from .data import extra_regions, fillers

if TYPE_CHECKING:
    from .world import BExWorld


def create_item_name_to_id() -> dict[str, int]:
    item_id_dict = {}
    current_id = 1

    for filler in fillers:
        item_id_dict[filler] = current_id
        current_id += 1
    for region in extra_regions:
        item_id_dict[f"{region} Rune"] = current_id
        current_id += 1
   
    return item_id_dict

ITEM_NAME_TO_ID = create_item_name_to_id()

ITEM_ID_TO_NAME = {v: k for k, v in ITEM_NAME_TO_ID.items()}


def create_item_classification() -> dict[str, ItemClassification]:
    item_classification_dict = {}

    for filler in fillers:
        item_classification_dict[filler] = ItemClassification.filler
    for region in extra_regions:
        item_classification_dict[f"{region} Rune"] = ItemClassification.progression
   
    return item_classification_dict

DEFAULT_ITEM_CLASSIFICATIONS = create_item_classification()


class BExItem(Item):
    game = "Backlog Expedition"


def get_random_filler_item_name(world: BExWorld) -> str:
    return ITEM_ID_TO_NAME.get(world.random.randint(1, len(fillers)))

def create_item_with_correct_classification(world: BExWorld, name: str) -> BExItem:
    return BExItem(name, DEFAULT_ITEM_CLASSIFICATIONS[name], ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: BExWorld) -> None:
    itempool = []

    for region in extra_regions:
        itempool.append(world.create_item(f"{region} Rune"))

    number_of_items = len(itempool)
    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

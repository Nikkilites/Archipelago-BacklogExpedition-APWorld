from collections.abc import Mapping
from typing import Any, Dict

from worlds.AutoWorld import World

from . import items, locations, options, regions, rules, web_world

class BExWorld(World):
    """
    Backlog Expedition is a meta game where a viking sets out on an expedition to an archipelago.
    In order to slay monsters and open chests to grab their loot,
    the player has to complete objectives in their backlog of games/movies/series etc. 
    """

    game = "Backlog Expedition"

    web = web_world.BExWebWorld()

    options_dataclass = options.BExOptions
    options: options.BExOptions

    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = items.ITEM_NAME_TO_ID

    origin_region_name = "Starting Island"

    hint_data: Dict[int, str] = dict()

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        self.hint_data = locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.BExItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        return self.options.as_dict(
            "locations_per_island", "beaten_to_goal", "backlog", "limited_locations", "repeatable_locations"
        )
    
    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        hint_data[self.player] = self.hint_data
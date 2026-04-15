import logging
from Options import OptionError
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hint_data: Dict[int, str] = {}

    def generate_early(self) -> None:
        islands = self.options.number_of_islands
        prio_len = len(self.options.prioritized_backlog.value)
        rand_len = len(self.options.randomized_backlog.value)

        # Throw exception if number_of_islands is too small to hold amount of games in prioritized_backlog
        if islands < prio_len:
            raise OptionError(
                "Error: Your number_of_islands is smaller than required for your amount of prioritized backlog games. "
                "Please check your YAML, and increase your number of islands or select fewer prioritized backlog games"
            )

        # Ensure there are enough empty islands to hold selected amount of randomized games defined by randomized_backlog_amount
        if islands < prio_len + self.options.randomized_backlog_amount:
            new_amount = islands - prio_len
            self.options.randomized_backlog_amount.value = new_amount
            logging.warning(
                "Warning: Your selected number_of_islands was smaller than required for selected backlog games. "
                f"randomized_backlog_amount was set to {new_amount}. Please check your YAML."
            )
        
        # Ensure randomized_backlog_amount is not higher than amount of games in randomized_backlog
        if self.options.randomized_backlog_amount > rand_len:
            self.options.randomized_backlog_amount.value = rand_len
            logging.warning(
                "Warning: Your selected randomized_backlog_amount was higher than the amount of games in your randomized_backlog. "
                f"randomized_backlog_amount was set to {rand_len}. Please check your YAML."
            )

        # Ensure backlog games do not have more than 20 locations each
        backlog = self.options.prioritized_backlog.value + self.options.randomized_backlog.value
        for game in backlog:
            count = game.get("count", 0)
            if count > 20:
                game["count"] = 20
                logging.warning(
                    f'Warning: Your backlog game {game.get("name")} had more locations than 20. '
                    'Number was therefore lowered to 20. Please check your YAML.'
                )

        # Ensure beaten_to_goal is not higher than number_of_islands
        if self.options.beaten_to_goal > islands:
            self.options.beaten_to_goal.value = islands.value
            logging.warning(
                f"Warning: Your beaten_to_goal was higher than your number_of_islands. "
                "Number was therefore lowered. Please check your YAML and lower your beaten_to_goal to be less than or equal to number_of_islands."
            )
        
        # Warning for having too many prioritized locations than what is able to be filled happens in locations.py
        
    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self) -> None:
        items.create_all_items(self)

    def create_item(self, name: str) -> items.BExItem:
        return items.create_item_with_correct_classification(self, name)

    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    def fill_slot_data(self) -> Mapping[str, Any]:
        slot_data = self.options.as_dict("beaten_to_goal", "runes_required")
        slot_data["hint_data"] = self.hint_data
        return slot_data
    
    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        hint_data[self.player] = self.hint_data
from dataclasses import dataclass
from schema import Schema, And

from Options import OptionGroup, PerGameCommonOptions, Range, OptionList


class PrioritizedBacklog(OptionList):
    """
    Games that will be your goal on an island.
    These games will always be included, and generate as many locations as defined here.
    Maximum of 20 games allowed, with a maximum of 20 locations per game.
    """

    display_name = "Prioritized Backlog"
    default = [
        {"name": "Complete an area of Hollow Knight", "count": 12},
        {"name": "Complete a chapter of Celeste", "count": 9},
    ]

    schema = Schema([
        {
            "name": And(str, len),
            "count": And(int, lambda x: x > 0),
        }
    ])

class RandomizedBacklog(OptionList):
    """
    Games that will be your goal on an island.
    These will will be randomly picked, based on your "Randomized Backlog Amount" option, and will generate as many locations as defined here.
    You can put an unlimited amount of games here, with a maximum of 20 locations per game.
    """

    display_name = "Randomized Backlog"
    default = [
        {"name": "Finish a kingdom in Super Mario Odyssey", "count": 15},
        {"name": "Beat a boss in Cuphead", "count": 19},
    ]

    schema = Schema([
        {
            "name": And(str, len),
            "count": And(int, lambda x: x > 0),
        }
    ])

class PrioritizedLocations(OptionList):
    """
    Objectives that will be used to fill up islands.
    These only exist a limited amount of times, and will be prioritized over other locations (Except Backlog locations).
    """

    display_name = "Prioritized Locations"
    default = [
        {"name": "Play a level of Train Valley", "count": 10},
        {"name": "Find a shiny Pikachu in Pokemon Sword", "count": 1},
    ]

    schema = Schema([
        {
            "name": And(str, len),
            "count": And(int, lambda x: x > 0),
        }
    ])

class LimitedLocations(OptionList):
    """
    Objectives that will be used to fill up islands.
    These only exist a limited amount of times, but are not guaranteed to exist.
    """

    display_name = "Limited Locations"
    default = [
        {"name": "Play a day of Stardew Valley", "count": 10},
        {"name": "Find a shiny Eevee in Pokemon Violet", "count": 1},
        {"name": "Try a new game", "count": 1},
    ]

    schema = Schema([
        {
            "name": And(str, len),
            "count": And(int, lambda x: x > 0),
        }
    ])

class RepeatableLocations(OptionList):
    """
    Objectives that will be used to fill up islands.
    These will be repeated as many times as needed to fill up islands.
    """

    display_name = "Repeatable Locations"
    default = ["Complete a run of Vampire Survivors", "Gain an Achievement in Cult of the Lamb", "Obtain a shiny pokemon"]

class TreasuresToGoal(Range):
    """
    How many Treasures you need to find to Goal.
    On each island you will find a treasure, so this number can only go as high as your "Number Of Islands" option.
    A maximum of 20, and minimum of 1.
    """

    display_name = "Treasures To Goal"

    range_start = 1
    range_end = 20
    default = 3

class  RandomizedBacklogAmount(Range):
    """
    How many random backlog games your world will have, in addition to your prioritized backlog games.
    This number cannot go higher than the amount of games in your "Randomized Backlog" option
    A maximum of 20.
    """

    display_name = "Randomized Backlog Amount"

    range_start = 0
    range_end = 20
    default = 1

class  NumberOfIslands(Range):
    """
    How many Islands your world will have.
    Make sure that this number is either equal to or higher than the amount of games in your "Prioritized Backlog" option + your "Randomized Backlog Amount" option.
    An Island that is not filled with a Backlog Game will instead become a medley island, filled with random objectives from the other location lists.
    A maximum of 20, and minimum of 1.
    """

    display_name = "Number Of Islands"

    range_start = 1
    range_end = 20
    default = 4

class  LocationsPerIsland(Range):
    """
    How many Locations each island should try to be filled with.
    If no repeatable locations are added, generation will fill up as much as possible.
    Locations needed for games put in any of the Backlog options are guaranteed to exist though.
    A maximum of 20.
    """

    display_name = "Locations Per Island"

    range_start = 0
    range_end = 20
    default = 10

class  RunesRequired(Range):
    """
    How many Runes each island will require to be unlocked.
    A maximum of 5.
    """

    display_name = "Runes Required"

    range_start = 1
    range_end = 5
    default = 2


@dataclass
class BExOptions(PerGameCommonOptions):
    number_of_islands: NumberOfIslands
    locations_per_island: LocationsPerIsland
    beaten_to_goal: TreasuresToGoal
    randomized_backlog_amount: RandomizedBacklogAmount
    prioritized_backlog: PrioritizedBacklog
    randomized_backlog: RandomizedBacklog
    prioritized_locations: PrioritizedLocations
    limited_locations: LimitedLocations
    repeatable_locations: RepeatableLocations
    runes_required: RunesRequired


option_groups = [
    OptionGroup(
        "Game Options",
        [NumberOfIslands, LocationsPerIsland, TreasuresToGoal, RandomizedBacklogAmount, RunesRequired],
    ),
    OptionGroup(
        "Game Additions",
        [PrioritizedBacklog, RandomizedBacklog, PrioritizedLocations, LimitedLocations, RepeatableLocations],
    ),
]

from dataclasses import dataclass
from schema import Schema, And

from Options import OptionGroup, PerGameCommonOptions, Range, OptionList


class Backlog(OptionList):
    """
    Games that will be beat in their entirety on the islands.
    These will always be included, and generate as many checks as selected.
    Maximum of 20 games allowed, with a maximum of 20 parts per game.
    """

    display_name = "Backlog"
    default = [
        {"name": "Hollow Knight", "type": "Area", "count": 12},
        {"name": "Celeste", "type": "chapter", "count": 9},
        {"name": "Dredge", "type": "Part", "count": 20},
    ]

    schema = Schema([
        {
            "name": And(str, len),
            "type": And(str, len),
            "count": And(int, lambda x: x > 0),
        }
    ])

class PrioritizedLocations(OptionList):
    """
    Objectives that will be used to fill up islands.
    These only exist a limited amount of times, and will be prioritized over other locations (Except Backlog).
    """

    display_name = "Limited Locations"
    default = [
        {"name": "Play a level of Train Valley", "count": 10},
        {"name": "Shinyhunt a Pikachu", "count": 1},
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
        {"name": "Play a level of Train Valley", "count": 10},
        {"name": "Shinyhunt a Pikachu", "count": 1},
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
    default = ["Do a run of Vampire Survivors", "Gain an Achievement in Vampire Survivors", "Obtain a shiny pokemon"]

class TreasuresToGoal(Range):
    """
    How many Treasures you need to find to Goal.
    It can only go as high as the Max Number Of Islands.
    """

    display_name = "Treasures To Goal"

    range_start = 1
    range_end = 20
    default = 10

class  MaxNumberOfIslands(Range):
    """
    How many Islands your world will have.
    An Island that cannot be filled with a Backlog Game will instead be filled with random objectives from the other lists
    A maximum of 20, and minimum of 1.
    """

    display_name = "Max Number Of Islands"

    range_start = 1
    range_end = 20
    default = 20

class  MaxLocationsPerIsland(Range):
    """
    How many Locations each island should try to be filled with.
    If no repeatable locations are added, generation will fill up as much as possible.
    Games put in Backlog are guaranteed to exist though.
    A maximum of 20.
    """

    display_name = "Max Locations Per Island"

    range_start = 0
    range_end = 20
    default = 20


@dataclass
class BExOptions(PerGameCommonOptions):
    islands: MaxNumberOfIslands
    locations_per_island: MaxLocationsPerIsland
    beaten_to_goal: TreasuresToGoal
    backlog: Backlog
    prioritized_locations: PrioritizedLocations
    limited_locations: LimitedLocations
    repeatable_locations: RepeatableLocations


option_groups = [
    OptionGroup(
        "Game Options",
        [MaxNumberOfIslands, MaxLocationsPerIsland, TreasuresToGoal],
    ),
    OptionGroup(
        "Game Additions",
        [Backlog, PrioritizedLocations, LimitedLocations, RepeatableLocations],
    ),
]

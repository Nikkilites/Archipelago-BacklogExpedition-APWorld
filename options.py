from dataclasses import dataclass
from schema import Schema, And

from Options import OptionGroup, PerGameCommonOptions, Range, OptionDict, OptionList


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

class LimitedLocations(OptionList):
    """
    Games that will be used to fill up islands with extra things to do alongside the game you want to beat.
    These only exist a limited amount of times, but are not guaranteed to exist.
    """

    display_name = "Limited Locations"
    default = [
        {"locationName": "Play a level of Train Valley", "count": 10},
        {"locationName": "Shinyhunt a Pikachu", "count": 1},
    ]

    schema = Schema([
        {
            "locationName": And(str, len),
            "count": And(int, lambda x: x > 0),
        }
    ])

class RepeatableLocations(OptionList):
    """
    Games that will be used to fill up islands with extra things to do alongside the game you want to beat.
    These will be repeated as many times as needed to fill up islands.
    """

    display_name = "Repeatable Locations"
    default = ["Do a run of Vampire Survivors", "Gain an Achievement in Vampire Survivors", "Obtain a shiny pokemon"]


class  MaxLocationsPerIsland(Range):
    """
    How many Locations each island should try to be filled with.
    If no repeatable locations are added, generation will fill up as much as possible
    A maximum of 20.
    """

    display_name = "Max Locations Per Island"

    range_start = 0
    range_end = 20
    default = 20

class  BacklogBeatenToGoal(Range):
    """
    How many Backlog Games you need to Beat to Goal.
    It can only go as high as the amount of Backlog Games added.
    """

    display_name = "Backlog Games Beaten To Goal"

    range_start = 1
    range_end = 20
    default = 10

@dataclass
class BExOptions(PerGameCommonOptions):
    locations_per_island: MaxLocationsPerIsland
    beaten_to_goal: BacklogBeatenToGoal
    backlog: Backlog
    limited_locations: LimitedLocations
    repeatable_locations: RepeatableLocations


option_groups = [
    OptionGroup(
        "Game Options",
        [MaxLocationsPerIsland, BacklogBeatenToGoal],
    ),
    OptionGroup(
        "Game Additions",
        [Backlog, LimitedLocations, RepeatableLocations],
    ),
]

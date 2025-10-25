from BaseClasses import Tutorial

from worlds.AutoWorld import WebWorld

from .options import option_groups


class BExWebWorld(WebWorld):
    game = "Backlog Expedition"
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Backlog Expedition for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Nikkilite"],
    )

    tutorials = [setup_en]

    option_groups = option_groups

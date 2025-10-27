import json
from pathlib import Path

# Import the data.py variables
from data import extra_regions, monsters, container_modifiers, containers, fillers, mcguffins

# Prepare dictionary in the same structure as you want in JSON
data_dict = {
    "extra_regions": extra_regions,
    "monsters": monsters,
    "container_modifiers": container_modifiers,
    "containers": containers,
    "fillers": fillers,
    "mcguffins": mcguffins
}

# Output path (same folder as this script)
output_file = Path(__file__).parent / "data.json"

# Write JSON with indentation
with output_file.open("w", encoding="utf-8") as f:
    json.dump(data_dict, f, indent=2, ensure_ascii=False)

print(f"JSON file created at {output_file}")
import sys
import json
import argparse
from typing import Optional


ADJACENT = (
    ("Frozen Cabins", "Dark Forest"),
    ("Frozen Cabins", "Moon Temple"),
    ("Frozen Cabins", "Colosseum"),
    ("Dark Forest", "Factory"),
    ("Dark Forest", "Defiled Cathedral"),
    ("Factory", "Vaal Pyramid"),
    ("Factory", "Laboratory"),
    ("Vaal Pyramid", "Vaults of Atziri"),
    ("Vaal Pyramid", "Shrine"),
    ("Defiled Cathedral", "Moon Temple"),
    ("Defiled Cathedral", "Atoll"),
    ("Defiled Cathedral", "Laboratory"),
    ("Laboratory", "Shrine"),
    ("Laboratory", "Crimson Township"),
    ("Moon Temple", "The Twilight Temple"),
    ("Moon Temple", "Cells"),
    ("Colosseum", "Terrace"),
    ("Crimson Township", "Plateau"),
    ("Crimson Township", "Spider Forest"),
    ("Crimson Township", "Atoll"),
    ("Atoll", "Mud Geyser"),
    ("Atoll", "Maelström of Chaos"),
    ("Atoll", "Cells"),
    ("Terrace", "Crimson Temple"),
    ("Crimson Temple", "Cells"),
    ("Crimson Temple", "Park"),
    ("Cells", "Chateau"),
    ("Park", "Chateau"),
    ("Park", "Phantasmagoria"),
    ("Park", "Thicket"),
    ("Phantasmagoria", "Coral Ruins"),
    ("Phantasmagoria", "Wharf"),
    ("Phantasmagoria", "Waterways"),
    ("Thicket", "Waterways"),
    ("Thicket", "Strand"),
    ("Strand", "Whakawairua Tuahu"),
    ("Strand", "Carcass"),
    ("Carcass", "Waterways"),
    ("Carcass", "Museum"),
    ("Carcass", "Overgrown Ruin"),
    ("Overgrown Ruin", "Excavation"),
    ("Bramble Valley", "Caldera"),
    ("Bramble Valley", "Bone Crypt"),
    ("Bone Crypt", "Primordial Pool"),
    ("Bone Crypt", "Dungeon"),
    ("Bone Crypt", "Olmec's Sanctum"),
    ("Dungeon", "Crater"),
    ("Dungeon", "Temple"),
    ("Temple", "Poorjoy's Asylum"),
    ("Temple", "Lava Chamber"),
    ("Mausoleum", "Lava Chamber"),
    ("Mausoleum", "Jungle Valley"),
    ("Mausoleum", "Maze"),
    ("Mausoleum", "Ancient City"),
    ("Jungle Valley", "Acid Caverns"),
    ("Jungle Valley", "Fungal Hollow"),
    ("Fungal Hollow", "Maze"),
    ("Fungal Hollow", "Wasteland"),
    ("Fungal Hollow", "Arachnid Tomb"),
    ("Arachnid Tomb", "Arachnid Nest"),
    ("Arachnid Tomb", "Wharf"),
    ("Arachnid Nest", "Wasteland"),
    ("Arachnid Nest", "Barrows"),
    ("Arachnid Nest", "Overgrown Shrine"),
    ("Wharf", "Shore"),
    ("Shore", "Acid Caverns"),
    ("Shore", "Mao Kun"),
    ("Shore", "Caldera"),
    ("Shore", "Museum"),
    ("Shore", "Waterways"),
    ("Museum", "The Putrid Cloister"),
    ("Museum", "Excavation"),
    ("Excavation", "Caldera"),
    ("Caldera", "Primordial Pool"),
    ("Primordial Pool", "Acid Caverns"),
    ("Primordial Pool", "Crater"),
)
COLORS = (
    "38;5;242",  # 0, gray
    "38;5;111",  # 1, blue
    "38;5;76",   # 2, green
    "38;5;166",  # 3, orange
    "38;5;178",  # 4, gold
)


class Map:

    def __init__(self, name: str, tier: int, have: bool) -> None:
        self.name = name
        self.tier = tier
        self.have = have
        self.adjacent = set()

    @property
    def undiscovered(self) -> int:
        """
        How many undiscovered maps are adjacent to this map.
        """
        return sum([not m.have for m in self.adjacent])


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """Read and parse arguments."""

    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        type=str,
        help="Path to file with input data. Default: None.",
        required=True,
        default=None,
    )

    return parser.parse_args(args)


def read_input(fn: str) -> dict:
    with open(fn) as f:
        return json.load(f)


def main():
    opts = parse_args()
    maps = read_input(opts.input)

    maps_by_name = {}
    maps_by_tier = {i: [] for i in range(1, 17)}
    for which, have in (("have_maps", True), ("dont_have_maps", False)):
        tiers = maps.get(which)
        for tier, map_list in tiers.items():
            for map_name in map_list:
                atlas_map = Map(map_name, int(tier), have)
                maps_by_name[atlas_map.name] = atlas_map
                maps_by_tier[atlas_map.tier].append(atlas_map)

    for adjacent in ADJACENT:
        map_a, map_b = [maps_by_name[x] for x in adjacent]
        map_a.adjacent.add(map_b)
        map_b.adjacent.add(map_a)

    for tier in sorted(maps_by_tier.keys()):
        line = f"Tier {tier:2d}: "
        map_strings = []
        for atlas_map in maps_by_tier.get(tier):
            u = atlas_map.undiscovered
            color = COLORS[u]

            if u:
                string = f"\033[{color}m{atlas_map.name} ({u})\033[0m"
            else:
                string = f"\033[{color}m{atlas_map.name}\033[0m"

            map_strings.append(string)

        line += " - ".join(map_strings)

        print(line)


if __name__ == "__main__":
    main()

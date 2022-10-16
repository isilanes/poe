import sys
import json
import argparse
from typing import Optional, Union


COLORS = {
    "links": (
        "38;5;242",  # gray
        "38;5;111",  # 1, blue
        "38;5;76",   # 2, green
        "38;5;166",  # 3, orange
        "38;5;178",  # 4, gold
        "38;5;129",  # 5
        "38;5;142",  # 6
    ),
    "highlight": "48;5;11",  # yellow background
}


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
        "--league",
        type=str,
        help="Path to file with map progress data. Default: required.",
        required=True,
    )
    parser.add_argument(
        "--atlas",
        type=str,
        help="Path to file with Atlas data. Default: required.",
        required=True,
    )
    parser.add_argument(
        "--select",
        type=str,
        help="Highlight selected map. Default: do not.",
        default=None,
    )

    return parser.parse_args(args)


def read_input(fn: str) -> Union[dict, list]:
    with open(fn) as f:
        return json.load(f)


def main():
    opts = parse_args()
    maps = read_input(opts.league)
    atlas = read_input(opts.atlas)

    maps_by_name = {}
    maps_by_tier = {i: [] for i in range(1, 17)}
    for which, have in (("have_maps", True), ("dont_have_maps", False)):
        tiers = maps.get(which)
        for tier, map_list in tiers.items():
            for map_name in map_list:
                atlas_map = Map(map_name, int(tier), have)
                maps_by_name[atlas_map.name] = atlas_map
                maps_by_tier[atlas_map.tier].append(atlas_map)

    for adjacent in atlas:
        map_a, map_b = [maps_by_name[x] for x in adjacent]
        map_a.adjacent.add(map_b)
        map_b.adjacent.add(map_a)

    for tier in sorted(maps_by_tier.keys()):
        line = f"Tier {tier:2d}: "
        map_strings = []
        for atlas_map in maps_by_tier.get(tier):
            u = atlas_map.undiscovered
            link_color = COLORS.get("links")[u]
            if opts.select and opts.select.lower() in atlas_map.name.lower():
                link_color += ";" + COLORS.get("highlight")

            name = atlas_map.name
            if not atlas_map.have:
                name = f"[{name}]"

            string = f"\033[{link_color}m{name}\033[0m"

            map_strings.append(string)

        line += " - ".join(map_strings)

        print(line)


if __name__ == "__main__":
    main()

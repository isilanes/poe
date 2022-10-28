import os
import sys
import json
import argparse
from typing import Optional, Union


DIR = os.path.dirname(os.path.abspath(__file__))
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
    "undiscovered": "31;48;5;15",  # red on white
}


class Map:

    def __init__(self, name: str, tier: int, have: bool = False) -> None:
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


def read_config(name: str) -> Union[dict, list]:
    fn = os.path.join(DIR, "config", f"{name}.json")

    return read_input(fn)


def main():
    opts = parse_args()
    maps = read_config(opts.league)

    # Read map configuration from Atlas JSON:
    atlas = read_config(f"atlas_{opts.atlas}")
    maps_by_name = {}
    maps_by_tier = {}
    for map_name, map_info in atlas.items():
        tier = map_info.get("tier")
        adjacent_map_names = map_info.get("adjacent")
        this_map = Map(map_name, tier)

        if tier not in maps_by_tier:
            maps_by_tier[tier] = []
        maps_by_tier[tier].append(this_map)
        maps_by_name[map_name] = this_map

        for other_name in adjacent_map_names:
            if other_name not in maps_by_name:
                continue
            other_map = maps_by_name[other_name]
            this_map.adjacent.add(other_map)
            other_map.adjacent.add(this_map)  # should be unnecessary

    # Read maps that I have:
    for which, have in (("have_maps", True), ("dont_have_maps", False)):
        tiers = maps.get(which)
        for tier, map_list in tiers.items():
            for map_name in map_list:
                this_map = maps_by_name[map_name]
                this_map.have = have

    for tier in sorted(maps_by_tier.keys()):
        line = f"Tier {tier:2d}: "
        map_strings = []
        for atlas_map in maps_by_tier.get(tier):
            u = atlas_map.undiscovered
            link_color = COLORS.get("links")[u]
            if opts.select and opts.select.lower() in atlas_map.name.lower():
                link_color += ";" + COLORS.get("highlight")

            if not atlas_map.have:
                link_color = COLORS.get("undiscovered")

            string = f"\033[{link_color}m{atlas_map.name}\033[0m"

            map_strings.append(string)

        line += " - ".join(map_strings)

        print(line)


if __name__ == "__main__":
    main()

import os
import sys
import json
import argparse
from typing import Optional, Union, Tuple

from PyInquirer import prompt


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
    "in_questions": "38;5;178",  # gold
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
    parser.add_argument(
        "--add",
        action="store_true",
        help="Add a Map. Default: print existing Maps.",
        default=False,
    )

    return parser.parse_args(args)


def read_input(fn: str) -> Union[dict, list]:
    with open(fn) as f:
        return json.load(f)


def read_config(name: str) -> Tuple[str, Union[dict, list]]:
    fn = os.path.join(DIR, "config", f"{name}.json")

    return fn, read_input(fn)


def build_atlas(atlas: dict) -> Tuple:
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

    return maps_by_name, maps_by_tier


def read_maps_i_have(maps: dict, maps_by_name: dict) -> None:
    for which, have in (("have_maps", True), ("dont_have_maps", False)):
        tiers = maps.get(which)
        for tier, map_list in tiers.items():
            for map_name in map_list:
                this_map = maps_by_name[map_name]
                this_map.have = have


def print_maps(opts, maps_by_tier: dict) -> None:
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


def add_map(maps: dict, maps_path: str, atlas: dict, atlas_path: str) -> None:
    atlas_map = get_atlas_map(atlas)
    add_map_to_map_list(atlas_map, maps, maps_path)
    add_map_to_atlas(atlas_map, atlas, atlas_path)


def add_map_to_map_list(atlas_map: Map, maps: dict, maps_path: str) -> None:
    which = "dont_have_maps"
    if atlas_map.have:
        which = "have_maps"

    for which, keep in (("have_maps", atlas_map.have), ("dont_have_maps", not atlas_map.have)):
        mw = maps[which]
        t = str(atlas_map.tier)

        if t not in mw:
            mw[t] = []

        mwt = mw[t]

        if keep and atlas_map.name not in mwt:
            mwt.append(atlas_map.name)

        if not keep and atlas_map.name in mwt:
            mwt.remove(atlas_map.name)

    with open(maps_path, "w") as f:
        json.dump(maps, f, ensure_ascii=False, indent=4)


def add_map_to_atlas(atlas_map: Map, atlas: dict, atlas_path: str) -> None:
    atlas[atlas_map.name] = {
        "tier": atlas_map.tier,
        "adjacent": list(atlas_map.adjacent),
    }

    with open(atlas_path, "w") as f:
        json.dump(atlas, f, ensure_ascii=False, indent=4)


def get_atlas_map(atlas: dict) -> Map:
    questions = [
        {
            "type": "input",
            "name": "map_name",
            "message": "Map name:"
        },
        {
            "type": "input",
            "name": "map_tier",
            "message": "Map tier:",
            "default": "",
            "validate": lambda i: isinstance(int(i), int),
        },
        {
            "type": "confirm",
            "name": "have",
            "message": "Completed?:",
        }
    ]
    answers = prompt(questions)

    atlas_map = Map(
        name=answers.get("map_name"),
        tier=int(answers.get("map_tier")),
        have=bool(answers.get("have")),
    )

    add_more = True
    already_adjacent = atlas.get(atlas_map.name, {}).get("adjacent", [])
    if already_adjacent:
        map_list = [f"[{n}]" for n in already_adjacent]
        msg = f"{atlas_map.name} already has these adjacent maps: {', '.join(map_list)}\n"
        msg += "Do you want to add another one?:"
        questions = [
            {
                "type": "confirm",
                "name": "add_more",
                "default": False,
                "message": msg,
            },
        ]
        answers = prompt(questions)
        add_more = answers.get("add_more")

    if not add_more:
        atlas_map.adjacent = list(sorted(set(already_adjacent)))
        return atlas_map

    questions = [
        {
            "type": "input",
            "name": "adjacent",
            "message": "Introduce map adjacent to it:",
        },
    ]

    adjacent_maps = already_adjacent
    go_on = True
    while go_on:
        answers = prompt(questions)
        adjacent = answers.get("adjacent")
        if not adjacent:
            break

        adjacent_maps.append(adjacent)

    if adjacent_maps:
        atlas_map.adjacent = tuple(sorted(set(adjacent_maps)))

    return atlas_map


def main():
    opts = parse_args()
    maps_path, maps = read_config(opts.league)
    atlas_path, atlas = read_config(f"atlas_{opts.atlas}")

    maps_by_name, maps_by_tier = build_atlas(atlas)
    read_maps_i_have(maps, maps_by_name)

    if opts.add:
        add_map(maps, maps_path, atlas, atlas_path)
    else:
        print_maps(opts, maps_by_tier)


if __name__ == "__main__":
    main()

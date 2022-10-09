HAVE_MAPS = (
    # Name, Tier
    ("Frozen Cabins", 1),
    ("Overgrown Ruin", 1),
    ("Strand", 1),
    ("Terrace", 1),

    ("Bramble Valley", 2),
    ("Colosseum", 2),
    ("Crimson Temple", 2),
    ("Dark Forest", 2),
    ("Excavation", 2),
    ("Moon Temple", 2),

    ("Caldera", 3),
    ("Cells", 3),
    ("Defiled Cathedral", 3),
    ("Factory", 3),
    ("Museum", 3),
    ("Park", 3),

    ("Atoll", 4),
    ("Dungeon", 4),
    ("Laboratory", 4),
    ("Phantasmagoria", 4),
    ("Primordial Pool", 4),
    ("Shore", 4),
    ("Vaal Pyramid", 4),
    ("Maelström of Chaos", 4),

    ("Acid Caverns", 5),
    ("Crimson Township", 5),
    ("Temple", 5),
    ("Wharf", 5),

    ("Arachnid Tomb", 6),
    ("Jungle Valley", 6),

    ("Arachnid Nest", 7),
    ("Fungal Hollow", 7),
    ("Mausoleum", 7),
)
DONT_HAVE_MAPS = (
    ("Whakawairua Tuahu", 1),

    ("Carcass", 2),
    ("Thicket", 2),
    ("The Twilight Temple", 2),

    ("Bone Crypt", 3),
    ("Waterways", 3),
    ("Olmec's Sanctum", 3),
    ("The Putrid Cloister", 3),

    ("Chateau", 4),
    ("Vaults of Atziri", 4),
    ("Mao Kun", 4),

    ("Coral Ruins", 5),
    ("Crater", 5),
    ("Mud Geyser", 5),
    ("Shrine", 5),
    ("Poorjoy's Asylum", 5),

    ("Dry Sea", 6),
    ("Lava Chamber", 6),
    ("Overgrown Shrine", 6),
    ("Plateau", 6),
    ("Spider Forest", 6),

    ("Colonnade", 7),
    ("Lair", 7),
    ("Necropolis", 7),
    ("Summit", 7),

    ("Ancient City", 8),
    ("Barrows", 8),
    ("Bog", 8),
    ("Canyon", 8),
    ("Ghetto", 8),
    ("Maze", 8),
    ("Wasteland", 8),
)
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
COLORS = [
    "38;5;242",  # 0, gray
    "38;5;111",  # 1, blue
    "38;5;76",   # 2, green
    "38;5;166",  # 3, orange
    "38;5;178",  # 4, gold
]


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


def main():
    maps_by_name = {}
    maps_by_tier = {i: [] for i in range(1, 17)}
    for map_list, have in ((HAVE_MAPS, True), (DONT_HAVE_MAPS, False)):
        for data in map_list:
            atlas_map = Map(*data, have)
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

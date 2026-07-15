from dataclasses import dataclass, field

@dataclass
class Loot:

    coins: list = field(default_factory=list)

    gems: list = field(default_factory=list)

    art_objects: list = field(default_factory=list)

    mundane_items: list = field(default_factory=list)

    magic_items: list = field(default_factory=list)
from dataclasses import dataclass


@dataclass
class Item:
    name: str

    category: str
    subcategory: str

    rarity: str

    requires_attunement: bool

    appearance: str

    description: str

    effect: str

    limitations: str

    value: str
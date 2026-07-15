from dataclasses import dataclass, field

@dataclass
class TableItem:

    roll: str

    text: str

@dataclass
class Table:

    name: str

    dice: str

    group: str = ""

    items: list[TableItem] = field(default_factory=list)
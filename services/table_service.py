import json
import random
import re
from pathlib import Path

from models.table import Table, TableItem


class TableService:

    def __init__(self):

        self.tables = []

        tables_path = (
            Path(__file__).parents[1]
            / "knowledge"
            / "tables"
        )

        self.load_tables(tables_path)

    def load_tables(self, folder):

        if not folder.exists():
            return

        for file in folder.glob("*.json"):

            try:

                with open(file, encoding="utf-8") as f:
                    data = json.load(f)

                items = []

                for item in data.get("items", []):
                    items.append(

                        TableItem(

                            roll=str(
                                item.get("roll", "")
                            ),

                            text=item.get(
                                "text",
                                ""
                            ).replace("\n", "<br>")

                        )

                    )

                self.tables.append(
                    Table(
                        name=data.get("name", file.stem),
                        dice=data.get("dice", ""),
                        group=data.get("group", ""),
                        items=items
                    )
                )

            except Exception as e:

                print(f"Ошибка загрузки {file.name}")
                print(e)

    def get_tables(self):

        return sorted(
            self.tables,
            key=lambda x: x.name.lower()
        )

    def search(self, text):

        text = text.lower()

        return [
            table
            for table in self.tables
            if text in table.name.lower()
        ]

    def get(self, name):

        for table in self.tables:

            if table.name == name:
                return table

        return None

    def parse_dice(self, dice):

        if not dice:
            return None

        match = re.search(r"(\d+)", dice)

        if not match:
            return None

        return int(match.group(1))

    def roll(self, table):

        sides = self.parse_dice(table.dice)

        if sides is None:
            return None

        return random.randint(1, sides)

    def match_roll(self, pattern, value):

        pattern = pattern.strip()

        if value is None:
            return False

        if not pattern:
            return False

        if "-" in pattern:

            try:

                left, right = pattern.split("-")

                return int(left) <= value <= int(right)

            except Exception:

                return False

        try:

            return int(pattern) == value

        except Exception:

            return False

    def find_result(self, table, roll):

        if not table.items:
            return None

        if roll is None:
            return random.choice(table.items)

        for item in table.items:

            if self.match_roll(item.roll, roll):
                return item

        return random.choice(table.items)

    def random_result(self, table_name):

        table = self.get(table_name)

        if table is None:
            return None

        roll = self.roll(table)

        item = self.find_result(table, roll)

        return {
            "table": table,
            "item": item,
            "roll": roll
        }
import json
import random
from pathlib import Path


class NameGenerator:

    def __init__(self):

        path = (
            Path(__file__)
            .resolve()
            .parent.parent
            / "knowledge"
            / "npc_database.json"
        )

        with open(path, "r", encoding="utf-8") as file:
            self.database = json.load(file)

    def generate(
        self,
        race: str,
        gender: str,
    ) -> str:

        if race not in self.database:
            return "Неизвестный"

        race_data = self.database[race]

        if gender == "Мужчина":
            names = race_data["male_names"]

        else:
            names = race_data["female_names"]

        return random.choice(names)

    def random_appearance(
        self,
        race: str,
    ):

        appearance = self.database[race]["appearance"]

        result = {}

        for key, values in appearance.items():
            result[key] = random.choice(values)

        return result


    def prompt(self, race: str):

        return self.database[race]["prompt"]
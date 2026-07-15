import json
import random
from pathlib import Path
from urllib.parse import quote

class ImageService:

    def __init__(self):

        database_path = (
            Path(__file__).parents[1]
            / "knowledge"
            / "data"
            / "npc_database.json"
        )

        with open(database_path, encoding="utf-8") as f:
            self.database = json.load(f)

        self.gender_translate = {
            "Мужчина": "male",
            "Женщина": "female",
        }

        self.class_translate = {
            "Воин": "fighter",
            "Волшебник": "wizard",
            "Чародей": "sorcerer",
            "Колдун": "warlock",
            "Жрец": "cleric",
            "Паладин": "paladin",
            "Следопыт": "ranger",
            "Плут": "rogue",
            "Бард": "bard",
            "Монах": "monk",
            "Друид": "druid",
            "Варвар": "barbarian",
            "Изобретатель": "artificer",
        }

        self.age_translate = {
            "Молодой": "young adult",
            "Взрослый": "adult",
            "Пожилой": "elderly",
        }


    def random_race_description(self, race):

        race_data = self.database.get(race)

        if race_data is None:
            return "", ""

        race_prompt = race_data["prompt"]

        appearance = []

        for values in race_data.get("appearance", {}).values():

            if values:
                appearance.append(random.choice(values))

        return race_prompt, appearance


    def build_prompt(self, npc):

        race_prompt, race_features = self.random_race_description(
            npc.race
        )

        gender = self.gender_translate.get(
            npc.gender,
            "male"
        )

        character_class = self.class_translate.get(
            npc.character_class,
            npc.character_class.lower()
        )

        age = self.age_translate.get(
            npc.age,
            "adult"
        )

        race_description = ", ".join(race_features)

        prompt = f"""
masterpiece,
best quality,
ultra detailed,
highly detailed,
fantasy illustration,
Dungeons and Dragons,
cinematic lighting,

{gender},
{age},

{race_prompt},

{character_class},

{race_description},

{npc.appearance},

beautiful fantasy character,

sharp focus,

portrait,

full face,

concept art,

realistic,

8k,

intricate details,

fantasy RPG,

official artwork
"""

        negative = """
worst quality,
low quality,
blurry,
pixelated,
deformed,
bad anatomy,
extra arms,
extra fingers,
extra legs,
mutated,
cropped,
text,
logo,
watermark,
duplicate,
ugly,
bad proportions,
"""

        prompt += f"\nNegative prompt: {negative}"

        return prompt

    def generate(self, npc):

        prompt = self.build_prompt(npc)

        seed = random.randint(
            1,
            999999999
        )

        url = (
            "https://image.pollinations.ai/prompt/"
            + quote(prompt)
            + f"?seed={seed}"
            + "&width=768"
            + "&height=1024"
            + "&nologo=true"
            + "&enhance=true"
        )

        return url
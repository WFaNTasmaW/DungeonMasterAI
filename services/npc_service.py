import json
import random
from pathlib import Path

from llm.client import LLMClient
from models.npc import NPC
from services.image_service import ImageService


class NPCService:

    def __init__(self):

        self.llm = LLMClient()
        self.image_service = ImageService()

        database_path = (
            Path(__file__).parents[1]
            /"knowledge"
            / "data"
            / "npc_database.json"
        )

        with open(database_path, encoding="utf-8") as f:
            self.database = json.load(f)

        self.classes = [
            "Воин",
            "Волшебник",
            "Чародей",
            "Колдун",
            "Жрец",
            "Паладин",
            "Следопыт",
            "Плут",
            "Бард",
            "Монах",
            "Друид",
            "Варвар",
            "Изобретатель",
        ]

        self.alignments = [
            "Законопослушный Добрый",
            "Нейтральный Добрый",
            "Хаотичный Добрый",
            "Законопослушный Нейтральный",
            "Истинно Нейтральный",
            "Хаотичный Нейтральный",
            "Законопослушный Злой",
            "Нейтральный Злой",
            "Хаотичный Злой",
        ]

        self.roles = [
            "Торговец",
            "Кузнец",
            "Стражник",
            "Алхимик",
            "Трактирщик",
            "Священник",
            "Охотник",
            "Наёмник",
            "Маг",
            "Рыбак",
            "Фермер",
            "Бандит",
        ]

        self.ages = [
            "Молодой",
            "Взрослый",
            "Пожилой",
        ]

        self.genders = [
            "Мужчина",
            "Женщина",
        ]

    # -----------------------------------------------------

    def randomize(
        self,
        race,
        character_class,
        gender,
        age,
        alignment,
        role,
    ):

        if race == "Любая":
            race = random.choice(
                list(self.database.keys())
            )

        if character_class == "Любой":
            character_class = random.choice(
                self.classes
            )

        if gender == "Любой":
            gender = random.choice(
                self.genders
            )

        if age == "Любой":
            age = random.choice(
                self.ages
            )

        if alignment == "Любое":
            alignment = random.choice(
                self.alignments
            )

        if role == "Любая":
            role = random.choice(
                self.roles
            )

        return (
            race,
            character_class,
            gender,
            age,
            alignment,
            role,
        )
    # -----------------------------------------------------

    def generate_name(
        self,
        race,
        gender,
    ):

        race_data = self.database[race]

        if gender == "Мужчина":
            return random.choice(
                race_data["male_names"]
            )

        return random.choice(
            race_data["female_names"]
        )
    # -----------------------------------------------------

    def generate_appearance(
        self,
        race,
    ):

        race_data = self.database[race]

        appearance = race_data.get("appearance", {})

        result = []

        for category, values in appearance.items():

            if not values:
                continue

            value = random.choice(values)

            if category == "skin":
                result.append(f"{value} кожа")

            elif category == "hair":
                result.append(f"{value} волосы")

            elif category == "eyes":
                result.append(f"{value} глаза")

            elif category == "horns":
                result.append(f"{value} рога")

            elif category == "tail":
                result.append(f"{value} хвост")

            elif category == "beard":
                result.append(f"{value} борода")

            elif category == "tattoos":
                result.append(value)

            elif category == "scars":
                result.append(value)

            elif category == "ears":
                result.append(f"{value} уши")

            else:
                result.append(value)

        return ", ".join(result)

        # -----------------------------------------------------

    def build_prompt(
            self,
            npc,
            features,
    ):

            return f"""
    Ты создаешь NPC для Dungeon Master.

    Верни ТОЛЬКО JSON.

    Не используй Markdown.

    Не добавляй пояснений.

    Имя уже выбрано.

    Раса уже выбрана.

    Класс уже выбран.

    Пол уже выбран.

    Возраст уже выбран.

    Мировоззрение уже выбрано.

    Роль уже выбрана.

    Внешность уже выбрана.

    Не меняй их.

    Персонаж

    Имя: {npc.name}

    Раса: {npc.race}

    Класс: {npc.character_class}

    Пол: {npc.gender}

    Возраст: {npc.age}

    Мировоззрение: {npc.alignment}

    Роль: {npc.role}

    Внешность:

    {npc.appearance}

    Дополнительные особенности:

    {features if features else "нет"}

    Придумай только:

    - personality
    - motivation
    - speech
    - inventory

    Верни JSON:

    {{
    "personality":"",
    "motivation":"",
    "speech":"",
    "inventory":[]
    }}
    """
    # -----------------------------------------------------

    def generate(
        self,
        race,
        character_class,
        gender,
        age,
        alignment,
        role,
        features,
    ):

        (
            race,
            character_class,
            gender,
            age,
            alignment,
            role,
        ) = self.randomize(
            race,
            character_class,
            gender,
            age,
            alignment,
            role,
        )

        name = self.generate_name(
            race,
            gender,
        )

        appearance = self.generate_appearance(
            race,
        )

        npc = NPC(
            name=name,
            race=race,
            character_class=character_class,
            gender=gender,
            age=age,
            alignment=alignment,
            role=role,
            personality="",
            motivation="",
            speech="",
            appearance=appearance,
            inventory=[],
        )

        prompt = self.build_prompt(
        npc,
        features,
        )

        response = self.llm.ask(prompt)

        response = response.strip()

        if response.startswith("```"):
            response = response.split("\n", 1)[1]
            response = response.rsplit("```", 1)[0]

        try:

            data = json.loads(response)

        except Exception:

            data = {
                "personality": "Спокойный и немногословный.",
                "motivation": "Заработать достаточно золота, чтобы исполнить свою мечту.",
                "speech": "Говорит размеренно, тщательно подбирая слова.",
                "inventory": [
                    "Нож",
                    "Кошель с монетами",
                    "Фляга",
                ]
            }

        npc.personality = data.get(
            "personality",
            npc.personality,
        )

        npc.motivation = data.get(
            "motivation",
            npc.motivation,
        )

        npc.speech = data.get(
            "speech",
            npc.speech,
        )

        inventory = data.get(
            "inventory",
            [],
        )

        if isinstance(inventory, str):

            inventory = [
                item.strip()
                for item in inventory.split(",")
                if item.strip()
            ]

        npc.inventory = inventory

        image = self.image_service.generate(
            npc
        )

        npc.image_path = image

        return npc, image

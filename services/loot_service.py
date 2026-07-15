import json
from llm.client import LLMClient
from pathlib import Path

from models.loot import Loot


class LootService:

    def __init__(self):

        self.llm = LLMClient()

        loot_path = (
            Path(__file__).parents[1]
            / "knowledge"
            / "loot"
        )

        self.mundane_items = self.load_json(
            loot_path / "mundane_items.json"
        )

        self.magic_items = self.load_json(
            loot_path / "magic_items.json"
        )

        self.gems = self.load_json(
            loot_path / "gems.json"
        )

        self.currencies = self.load_json(
            loot_path / "currencies.json"
        )

    def load_json(self, path):

        if not path.exists():
            return []

        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def random_from(self, data, count):

        import random

        if not data:
            return []

        count = min(count, len(data))

        return random.sample(data, count)

    # -----------------------------------------------------

    def random_coins(
            self,
            danger,
    ):

        import random

        coins = {}

        if danger == "1-4":

            cp = random.randint(50, 300)
            sp = random.randint(20, 120)
            gp = random.randint(5, 30)

            if cp:
                coins["ММ"] = cp

            if sp:
                coins["СМ"] = sp

            if gp:
                coins["ЗМ"] = gp

        elif danger == "5-10":

            sp = random.randint(100, 600)
            gp = random.randint(50, 250)

            if random.random() < 0.35:
                pp = random.randint(1, 10)
            else:
                pp = 0

            coins["СМ"] = sp
            coins["ЗМ"] = gp

            if pp:
                coins["ПМ"] = pp

        elif danger == "11-16":

            gp = random.randint(500, 3000)
            pp = random.randint(10, 80)

            coins["ЗМ"] = gp
            coins["ПМ"] = pp

        else:

            gp = random.randint(3000, 12000)
            pp = random.randint(100, 600)

            coins["ЗМ"] = gp
            coins["ПМ"] = pp

        return coins
    def default_distribution(
            self,
            danger,
    ):

        if danger == "1-4":
            return {
                "coins": True,
                "mundane_items": 2,
                "gems": 0,
                "magic_items": 0,
            }

        if danger == "5-10":
            return {
                "coins": True,
                "mundane_items": 3,
                "gems": 1,
                "magic_items": 0,
            }

        if danger == "11-16":
            return {
                "coins": True,
                "mundane_items": 3,
                "gems": 2,
                "magic_items": 1,
            }

        return {

            "coins": True,
            "mundane_items": 4,
            "gems": 4,
            "magic_items": 2,

        }

    def build_prompt(

            self,

            danger,

            features,

    ):

            return f"""
    Ты — опытный Dungeon Master D&D 5.5 (2024).

    Твоя задача — определить состав награды.

    НЕ придумывай предметы.

    НЕ придумывай названия.

    НЕ описывай сокровища.

    Тебе нужно только определить,
    сколько предметов каждой категории
    должно присутствовать в награде.

    Главное правило:

    Основной фактор — опасность приключения.

    Диапазоны опасности:

    1–4
    небольшие награды

    5–10
    умеренные награды

    11–16
    богатые награды

    17+
    легендарные награды

    Дополнительные пожелания могут изменить
    тип добычи, но НЕ должны значительно
    увеличивать её количество.

    Например:

    "логово дракона"

    ↓

    больше золота и драгоценностей

    "лаборатория алхимика"

    ↓

    больше магических предметов

    "храм"

    ↓

    меньше золота,
    больше реликвий

    Опасность:

    {danger}

    Дополнительные пожелания:

    {features if features else "нет"}

    Верни только JSON.

    {{
        "coins": true,
        "mundane_items": 0,
        "gems": 0,
        "magic_items": 0
    }}
    """

    def get_distribution(

            self,

            danger,

            features,

    ):

        prompt = self.build_prompt(
            danger,
            features,
        )

        try:

            data = self.llm.ask_json(prompt)

            if isinstance(data, str):
                data = json.loads(data)

            defaults = self.default_distribution(danger)

            result = {}

            result["coins"] = bool(
                data.get(
                    "coins",
                    defaults["coins"],
                )
            )

            result["mundane_items"] = min(
                max(
                    int(
                        data.get(
                            "mundane_items",
                            defaults["mundane_items"],
                        )
                    ),
                    0,
                ),
                defaults["mundane_items"] + 2,
            )

            result["gems"] = min(
                max(
                    int(
                        data.get(
                            "gems",
                            defaults["gems"],
                        )
                    ),
                    0,
                ),
                defaults["gems"] + 2,
            )

            result["magic_items"] = min(
                max(
                    int(
                        data.get(
                            "magic_items",
                            defaults["magic_items"],
                        )
                    ),
                    0,
                ),
                defaults["magic_items"] + 1,
            )

            return result

        except Exception:

            return self.default_distribution(
                danger
            )

    def generate(

            self,

            danger,

            features="",

    ):

        loot = Loot()

        distribution = self.get_distribution(

            danger,

            features,

        )


        if distribution.get("coins", True):
            coins = self.random_coins(danger)

            for coin_type, amount in coins.items():
                loot.coins.append(
                    f"{amount} {coin_type}"
                )


        loot.mundane_items = self.random_from(

            self.mundane_items,

            distribution.get(

                "mundane_items",

                0,

            ),

        )


        loot.gems = self.random_from(

            self.gems,

            distribution.get(

                "gems",

                0,

            ),

        )

        loot.magic_items = self.random_from(

            self.magic_items,

            distribution.get(

                "magic_items",

                0,

            ),

        )

        return loot
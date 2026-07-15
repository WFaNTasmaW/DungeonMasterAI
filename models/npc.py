from dataclasses import dataclass, field


@dataclass
class NPC:
    name: str

    race: str
    character_class: str

    gender: str
    age: str

    alignment: str
    role: str

    personality: str
    motivation: str
    speech: str

    appearance: str

    inventory: list[str] = field(default_factory=list)

    image_path: str = ""

    def to_dict(self):

        return {
            "name": self.name,
            "race": self.race,
            "character_class": self.character_class,
            "gender": self.gender,
            "age": self.age,
            "alignment": self.alignment,
            "role": self.role,
            "personality": self.personality,
            "motivation": self.motivation,
            "speech": self.speech,
            "appearance": self.appearance,
            "inventory": self.inventory,
            "image_path": self.image_path,
        }

    @classmethod
    def from_dict(cls, data):

        inventory = data.get("inventory", [])

        if isinstance(inventory, str):
            inventory = [
                item.strip()
                for item in inventory.split(",")
                if item.strip()
            ]

        return cls(
            name=data.get("name", "Безымянный"),

            race=data.get("race", "Человек"),
            character_class=data.get("class", data.get("character_class", "Воин")),

            gender=data.get("gender", "Мужчина"),
            age=data.get("age", "Взрослый"),

            alignment=data.get("alignment", "Истинно Нейтральный"),
            role=data.get("role", "Путешественник"),

            personality=data.get("personality", ""),
            motivation=data.get("motivation", ""),
            speech=data.get("speech", ""),
            appearance=data.get("appearance", ""),

            inventory=inventory,

            image_path=data.get("image_path", "")
        )
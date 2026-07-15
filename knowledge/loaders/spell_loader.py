from models.spell import Spell
from knowledge.loaders.base_loader import BaseLoader
from core.config import SPELLS_PATH


class SpellLoader(BaseLoader):

    def __init__(self):
        super().__init__(SPELLS_PATH)

    def load(self) -> list[Spell]:
        return [
            Spell.model_validate(item)
            for item in self.read()
        ]
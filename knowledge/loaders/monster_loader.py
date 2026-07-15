from core.config import MONSTERS_PATH
from knowledge.loaders.base_loader import BaseLoader
from models import Monster


class MonsterLoader(BaseLoader):

    def __init__(self):
        super().__init__(MONSTERS_PATH)

    def load(self) -> list[Monster]:

        return [
            Monster.model_validate(monster)
            for monster in self.read()
        ]
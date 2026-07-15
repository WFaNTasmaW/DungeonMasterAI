from models.character_class import CharacterClass
from knowledge.loaders.base_loader import BaseLoader
from core.config import CLASSES_PATH


class ClassLoader(BaseLoader):

    def __init__(self):
        super().__init__(CLASSES_PATH)

    def load(self) -> list[CharacterClass]:
        return [
            CharacterClass.model_validate(item)
            for item in self.read()
        ]
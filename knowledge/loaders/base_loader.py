from abc import ABC
from pathlib import Path
import json

class BaseLoader(ABC):

    def __init__(self, file_path: Path):
        self.file_path = file_path

    def read(self) -> list[dict]:

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"File not found: {self.file_path}"
            )

        with open(self.file_path, "r", encoding="utf-8") as file:
            return json.load(file)
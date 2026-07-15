from pymorphy3 import MorphAnalyzer

from knowledge.loaders import (
    MonsterLoader,
    SpellLoader,
    ClassLoader,
)


class DataFilter:

    def __init__(self):
        self.monsters = MonsterLoader().load()
        self.spells = SpellLoader().load()
        self.classes = ClassLoader().load()

        self.morph = MorphAnalyzer()

        self.synonyms = {
            "опасность": ["challenge_rating", "cr"],
            "броня": ["armor_class"],
            "кд": ["armor_class"],
            "хиты": ["hit_points"],
            "здоровье": ["hit_points"],
            "скорость": ["speed"],
            "язык": ["languages"],
            "языки": ["languages"],
            "урон": ["damage"],
        }

    def filter(self, query: str):

        words = self.prepare_words(query)

        results = []

        for obj in self.spells:
            score = self.score_object(obj, words)
            if score > 0:
                results.append((score, obj))

        for obj in self.monsters:
            score = self.score_object(obj, words)
            if score > 0:
                results.append((score, obj))

        for obj in self.classes:
            score = self.score_object(obj, words)
            if score > 0:
                results.append((score, obj))

        results.sort(key=lambda x: x[0], reverse=True)

        return [obj for _, obj in results[:5]]

    def prepare_words(self, query: str):

        stop_words = {
            "что",
            "как",
            "какой",
            "какая",
            "какие",
            "показать",
            "рассказать",
            "про",
            "для",
            "весь",
            "и",
            "или",
            "с",
            "на",
            "по",
            "о",
            "монстр",
            "заклинание",
            "класс",
        }

        words = []

        for word in self.normalize(query):

            if word in stop_words:
                continue

            words.append(word)

        expanded = []

        for word in words:
            expanded.append(word)

            if word in self.synonyms:
                expanded.extend(self.synonyms[word])

        return expanded

    def normalize(self, text: str):

        result = []

        for word in text.lower().split():

            word = word.strip(".,!?()[]{}:;\"'")

            if not word:
                continue

            normal = self.morph.parse(word)[0].normal_form

            result.append(normal)

        return result

    def score_object(self, obj, words):

        data = obj.model_dump()

        score = 0

        for field, value in data.items():

            if value is None:
                continue

            text_words = set(self.normalize(str(value)))

            for word in words:

                if word not in text_words:
                    continue

                if field == "name":
                    score += 20

                elif field == "name_en":
                    score += 15

                elif field in {
                    "type",
                    "school",
                    "level",
                    "classes",
                    "challenge_rating",
                    "cr",
                }:
                    score += 8

                else:
                    score += 2

        return score
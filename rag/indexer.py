from models import Monster, Spell, CharacterClass

class Indexer:
    @staticmethod
    def monster_to_document(monster: Monster) -> str:
        return f"""
Название: {monster.name}
Тип: {monster.type}
Размер: {monster.size}
Мировоззрение: {monster.alignment}
CR: {monster.challenge_rating}
HP: {monster.hit_points}
Описание:
{monster.description}
"""
    @staticmethod
    def spell_to_document(spell: Spell) -> str:
        return f"""
Название: {spell.name}
Уровень: {spell.level}
Школа: {spell.school}
Описание:
{spell.description}
"""
    @staticmethod
    @staticmethod
    def class_to_document(character_class: CharacterClass) -> str:
        return character_class.rag_text
from pydantic import BaseModel, ConfigDict
from typing import Dict, List


class Ability(BaseModel):
    model_config = ConfigDict(extra="ignore")

    value: str
    mod: str
    save: str


class MonsterAction(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    description: str


class Monster(BaseModel):
    model_config = ConfigDict(extra="ignore")

    # Общая информация
    url: str
    name: str
    name_en: str

    size: str
    type: str
    subtype: str
    alignment: str

    # Боевые характеристики
    armor_class: str
    initiative: str

    hit_points: str
    hit_points_average: int
    hit_points_formula: str

    speed: str

    # Характеристики
    abilities: Dict[str, Ability]

    # Дополнительная информация
    skills: str
    senses: str
    languages: str

    # Challenge Rating
    challenge_rating: str
    cr: float
    xp: int

    # Особенности
    traits: List[MonsterAction]
    actions: List[MonsterAction]
    bonus_actions: List[MonsterAction]
    reactions: List[MonsterAction]
    legendary_actions: List[MonsterAction]

    # Описание
    description: str

    # Отображение
    size_type_alignment: str
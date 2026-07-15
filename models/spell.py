from pydantic import BaseModel, ConfigDict


class Spell(BaseModel):
    model_config = ConfigDict(extra="ignore")

    url: str

    name: str

    level: str

    school: str

    casting_time: str

    range: str

    components: str

    duration: str

    description: str

    classes: str
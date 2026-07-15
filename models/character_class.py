from pydantic import BaseModel, ConfigDict, Field


class Subclass(BaseModel):
    model_config = ConfigDict(extra="ignore")

    name: str
    description: str
    features: list = Field(default_factory=list)


class CharacterClass(BaseModel):
    model_config = ConfigDict(extra="ignore")

    url: str
    name: str

    rag_text: str = ""

    subclasses: list[Subclass] = Field(default_factory=list)

    special_features: list = Field(default_factory=list)
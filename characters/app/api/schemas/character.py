from pydantic import BaseModel, Field, FilePath


class CharacterBase(BaseModel):
    name: str = Field(default="Mario")
    role: str = Field(default="Char")
    content: str = Field(default="")


class CharacterCreate(CharacterBase):
    image: FilePath


class CharacterUpdate(CharacterBase):
    pass


class CharacterInDBBase(CharacterBase):
    id: int | None = None

    class Config:
        orm_mode = True


class Character(CharacterInDBBase):
    pass


class CharacterInDB(CharacterInDBBase):
    pass

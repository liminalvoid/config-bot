from typing import Annotated

from sqlmodel import Field, SQLModel


class ConfigBase(SQLModel):
    name: str = Field(index=True)
    protocol: str = Field(index=True)
    user_id: int


class Config(ConfigBase, table=True):
    id: int = Field(default=None, primary_key=True)


class ConfigPublic(ConfigBase):
    id: int


class ConfigCreate(ConfigBase): ...


class ConfigUpdate(ConfigBase):
    name: str = ""

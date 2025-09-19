from typing import Annotated, List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

from .configs import Config


class UserBase(SQLModel):
    tg_id: int = Field(default=None, index=True)
    configs: List[Config]


class User(UserBase, table=True):
    id: int = Field(default=None, primary_key=True)


class UserPublic(UserBase):
    id: int


class UserCreate(UserBase): ...

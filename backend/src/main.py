from os import getenv
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import SQLModel
from dotenv import load_dotenv

from lib.dependencies import get_session
from lib.db import init_db
from routers import configs


load_dotenv()

DB_PROTOCOL = getenv("DB_PROTOCOL")
DB_USER = getenv("DB_USER")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
DB_NAME = getenv("DB_NAME")

db_url = f"{DB_PROTOCOL}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not database_exists(db_url):
        create_database(db_url)

    engine = init_db(db_url)

    SQLModel.metadata.create_all(engine)

    yield


origins = ["http://tg_bot"]

app = FastAPI(
    lifespan=lifespan,
    dependencies=[Depends(get_session)]
)

app.include_router(configs.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"root": True}

from sqlmodel import SQLModel, create_engine, Session


# TODO: Try to make this singleton or consider better option
engine = None


def init_db(connection_string: str):
    global engine

    engine = create_engine(connection_string)

    return engine


def get_session():
    if engine is None:
        raise RuntimeError("Database engine is not initialized. Call init_db() first.")

    with Session(engine) as session:
        yield session

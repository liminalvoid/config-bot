from fastapi import HTTPException, APIRouter
from sqlmodel import select

from models.configs import Config, ConfigPublic, ConfigCreate
from lib.dependencies import SessionDep


router = APIRouter(
    prefix="/configs",
    tags=["configs"],
    responses={404: {"description": "Not found"}}
)


@router.post("/", response_model=ConfigPublic)
async def create_configs(session: SessionDep, config: ConfigCreate) -> Config:
    db_config = Config.model_validate(config)

    session.add(db_config)
    session.commit()
    session.refresh(db_config)

    return db_config


@router.get("/", response_model=list[ConfigPublic])
async def read_configs(session: SessionDep):
    configs = session.exec(select(Config))._allrows()

    return configs


@router.get("/{config_id}", response_model=ConfigPublic)
async def read_config(config_id: int, session: SessionDep):
    config = session.get(Config, config_id)

    if not config:
        raise HTTPException(status_code=404, detail="Config not found")

    return config


@router.delete("/{config_id}")
async def delete_config(config_id: int, session: SessionDep):
    config = session.get(Config, config_id)

    if not config:
        raise HTTPException(status_code=404, detail="Config not found")

    session.delete(config)
    session.commit()

    return {"ok": True}

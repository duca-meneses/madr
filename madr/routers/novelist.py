from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select

from madr.data.models import Novelist
from madr.schemas.message import MessageSchema
from madr.schemas.novelist import (
    NovelistListAll,
    NovelistPublic,
    NovelistSchema,
    NovelistUpdate,
)
from madr.utils.dependencies import T_CurrentUser, T_Session
from madr.utils.sanitize import sanitize_data

router = APIRouter(prefix='/novelist', tags=['novelist'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=NovelistPublic
)
async def create_novelist(
    novelist: NovelistSchema, user: T_CurrentUser, session: T_Session
):
    db_novelist = await session.scalar(
        select(Novelist).where(Novelist.name == novelist.name)
    )

    if db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='novelist already on the MADR',
        )

    db_novelist = Novelist(name=sanitize_data(novelist.name))

    session.add(db_novelist)
    await session.commit()
    await session.refresh(db_novelist)

    return db_novelist


@router.get('/', status_code=HTTPStatus.OK, response_model=NovelistListAll)
async def list_novelist(
    session: T_Session,
    user: T_CurrentUser,
    name: str = Query(None),
    offset: int = Query(None),
    limit: int = Query(10),
):
    query = select(Novelist)
    if name:
        query = query.filter(Novelist.name.contains(name))

    novelists = await session.scalars(query.offset(offset).limit(limit))

    return {'novelists': novelists}


@router.get(
    '/{novelist_id}', status_code=HTTPStatus.OK, response_model=NovelistPublic
)
async def get_novelist_by_id(
    novelist_id: int, session: T_Session, user: T_CurrentUser
):
    db_novelist = await session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )

    if not db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Novelist not listed in MADR',
        )

    return db_novelist


@router.patch(
    '/{novelist_id}', status_code=HTTPStatus.OK, response_model=NovelistPublic
)
async def update_novelist(
    novelist_id: int,
    novelist: NovelistUpdate,
    session: T_Session,
    user: T_CurrentUser,
):
    db_novelist = await session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )

    if not db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Novelist not listed in MADR',
        )

    novelist_name = sanitize_data(novelist.name)

    db_novelist_name = await session.scalar(
        select(Novelist).where(Novelist.name == novelist_name)
    )
    if db_novelist_name:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='novelist already on the MADR',
        )

    db_novelist.name = novelist_name

    session.add(db_novelist)
    await session.commit()
    await session.refresh(db_novelist)

    return db_novelist


@router.delete(
    '/{novelist_id}', status_code=HTTPStatus.OK, response_model=MessageSchema
)
async def delete_novelist(
    novelist_id: int, session: T_Session, user: T_CurrentUser
):
    db_novelist = await session.scalar(
        select(Novelist).where(Novelist.id == novelist_id)
    )

    if not db_novelist:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Novelist not listed in MADR',
        )

    await session.delete(db_novelist)
    await session.commit()

    return {'message': 'Novelist deleted from MADR'}

from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    MessageSchema,
    PublicUserSchema,
    UserListSchema,
    UserSchema,
)

app = FastAPI(
    title='🚀 FAST API',
    version='0.1.0',
    description='✨ API FOR LEARNING FASTAPI ✨',
)

database = []


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
    tags=['Health'],
)
def read_root():
    return {'message': 'Hello World'}


@app.get(
    '/ping',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
    tags=['Health'],
)
def ping():
    return {'message': 'pong'}


@app.post(
    '/users',
    status_code=HTTPStatus.CREATED,
    response_model=PublicUserSchema,
    tags=['Users'],
)
def create_user(user: UserSchema, session: Session = Depends(get_session)):

    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get(
    '/users',
    status_code=HTTPStatus.OK,
    response_model=UserListSchema,
    tags=['Users'],
)
def resume_users(
    offset: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(offset).limit(limit)).all()
    return {'users': users}


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=PublicUserSchema,
    tags=['Users'],
)
def resume_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return db_user


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=PublicUserSchema,
    tags=['Users'],
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )
    try:
        db_user.username = user.username
        db_user.email = user.email
        db_user.password = user.password
        session.commit()
        session.refresh(db_user)
        return db_user
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or email already exists',
        )


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
    tags=['Users'],
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted successfully'}

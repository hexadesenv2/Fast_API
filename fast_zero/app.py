from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import (
    MessageSchema,
    PublicUserSchema,
    TokenSchema,
    UserListSchema,
    UserSchema,
)
from fast_zero.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
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
        username=user.username,
        password=get_password_hash(user.password),
        email=user.email,
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
    offset: int = 0,
    limit: int = 10,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    users = session.scalars(select(User).offset(offset).limit(limit)).all()
    return {'users': users}


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=PublicUserSchema,
    tags=['Users'],
)
def resume_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to view this user',
        )

    return current_user


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=PublicUserSchema,
    tags=['Users'],
)
def update_user(
    user_id: int,
    user: UserSchema,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to update this user',
        )

    try:
        current_user.username = user.username
        current_user.email = user.email
        current_user.password = get_password_hash(user.password)
        session.commit()
        session.refresh(current_user)
        return current_user
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
def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):

    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN,
            detail='You do not have permission to delete this user',
        )

    session.delete(current_user)
    session.commit()

    return {'message': 'User deleted successfully'}


@app.post('/token', response_model=TokenSchema, tags=['Authentication'])
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    db_user = session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect username or password',
        )

    access_token = create_access_token({'sub': db_user.username})

    return {'access_token': access_token, 'token_type': 'bearer'}

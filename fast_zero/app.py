from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import (
    Message,
    PublicUser,
    User,
    UserDB,
    UserListSchema,
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
    response_model=Message,
    tags=['Health'],
)
def read_root():
    return {'message': 'Hello World'}


@app.get(
    '/ping', status_code=HTTPStatus.OK, response_model=Message, tags=['Health']
)
def ping():
    return {'message': 'pong'}


@app.post(
    '/users',
    status_code=HTTPStatus.CREATED,
    response_model=PublicUser,
    tags=['Users'],
)
def create_user(user: User):
    user_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_id)
    return user_id


@app.get(
    '/users',
    status_code=HTTPStatus.OK,
    response_model=UserListSchema,
    tags=['Users'],
)
def resume_users():
    return {'users': database}


@app.get(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=PublicUser,
    tags=['Users'],
)
def resume_user(user_id: int):
    if (user_id < 1) or (user_id > len(database)):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    return database[user_id - 1]


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=PublicUser,
    tags=['Users'],
)
def update_user(user_id: int, user: User):
    updated_user = UserDB(**user.model_dump(), id=user_id)

    if (user_id < 1) or (user_id > len(database)):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    database[user_id - 1] = updated_user

    return updated_user


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.NO_CONTENT,
    response_model=None,
    tags=['Users'],
)
def delete_user(user_id: int):
    if (user_id < 1) or (user_id > len(database)):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    database.pop(user_id - 1)

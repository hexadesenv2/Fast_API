from http import HTTPStatus

from fastapi import FastAPI

from fast_zero.schemas import Message

app = FastAPI(title='🚀API', version='0.0.1')


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'Hello World'}


@app.get('/ping', status_code=HTTPStatus.OK, response_model=Message)
def ping():
    return {'message': 'pong'}

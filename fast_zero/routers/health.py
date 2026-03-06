from http import HTTPStatus

from fastapi import APIRouter

from fast_zero.schemas import MessageSchema

router = APIRouter(prefix='/health', tags=['❤️ Health'])


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=MessageSchema,
)
def read_root():
    return {'message': 'API working...'}

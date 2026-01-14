from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_read_root():
    # Arrange
    client = TestClient(app)
    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}

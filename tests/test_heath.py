from http import HTTPStatus


def test_read_root(client):  # Arrange
    # Act
    response = client.get('/health/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_ping(client):  # Arrange
    # Act
    response = client.get('/health/ping')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'pong'}

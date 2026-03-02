from http import HTTPStatus


def test_read_root(client):  # Arrange
    # Act
    response = client.get('/health/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'API working...'}

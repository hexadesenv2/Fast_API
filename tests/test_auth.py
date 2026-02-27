from http import HTTPStatus


def test_get_jwt(client, dummy_user):  # Arrange
    # Act
    response = client.post(
        '/auth/token',
        data={
            'username': dummy_user.username,
            'password': dummy_user.clean_password,
        },
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    token = response.json()
    assert token['token_type'] == 'bearer'
    assert 'access_token' in token


def test_get_jwt_no_user(client):  # Arrange
    # Act
    response = client.post(
        '/auth/token',
        data={
            'username': 'nonexistentuser',
            'password': 'Secret',
        },
    )
    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}


def test_get_jwt_wrong_password(client, dummy_user):  # Arrange
    # Act
    response = client.post(
        '/auth/token',
        data={
            'username': dummy_user.username,
            'password': 'wrongpassword',
        },
    )
    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}

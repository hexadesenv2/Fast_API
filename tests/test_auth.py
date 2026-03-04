from http import HTTPStatus

from freezegun import freeze_time


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
    assert token['token_type'] == 'Bearer'
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


def test_get_jwt_expired_token(client, dummy_user):  # Arrange
    # Act
    with freeze_time('2026-01-01 08:00:00'):
        response = client.post(
            '/auth/token',
            data={
                'username': dummy_user.username,
                'password': dummy_user.clean_password,
            },
        )

        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2026-01-01 12:01:00'):
        response = client.put(
            f'/users/{dummy_user.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'WrongDoe',
                'email': 'WrongDoe@example.com',
                'password': 'WrongDoeSecret',
            },
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


def test_refresh_token(client, token):  # Arrange
    # Act
    response = client.post(
        '/auth/refresh',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    data = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'Bearer'


def test_token_expired_dont_refresh(client, dummy_user):  # Arrange
    with freeze_time('2026-01-01 08:00:00'):
        response = client.post(
            '/auth/token',
            data={
                'username': dummy_user.username,
                'password': dummy_user.clean_password,
            },
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2026-01-01 12:01:00'):
        response = client.post(
            '/auth/refresh', headers={'Authorization': f'Bearer {token}'}
        )

        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}

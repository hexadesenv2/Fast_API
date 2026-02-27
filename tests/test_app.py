from http import HTTPStatus

from fast_zero.schemas import PublicUserSchema


def test_read_root(client):  # Arrange
    # Act
    response = client.get('/')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Hello World'}


def test_ping(client):  # Arrange
    # Act
    response = client.get('/ping')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'pong'}


def test_create_user(client):  # Arrange
    user_data = {
        'username': 'JhonDoe',
        'email': 'JhonDoe@example.com',
        'password': 'Secret',
    }
    # Act
    response = client.post('/users', json=user_data)
    # Assert
    assert response.status_code == HTTPStatus.CREATED
    response_data = response.json()
    assert response_data['id'] == 1
    assert response_data['username'] == user_data['username']
    assert response_data['email'] == user_data['email']


def test_create_user_with_existing_username(client, dummy_user):  # Arrange
    user_schema = PublicUserSchema.model_validate(dummy_user).model_dump()
    user_data = {
        'username': user_schema['username'],
        'email': 'another@example.com',
        'password': 'anotherSecret',
    }
    # Act
    response = client.post(
        '/users',
        json=user_data,
    )
    # Assert
    assert response.status_code == HTTPStatus.CONFLICT


def test_create_user_with_existing_email(client, dummy_user):  # Arrange
    user_schema = PublicUserSchema.model_validate(dummy_user).model_dump()
    user_data = {
        'username': 'AliceDoe',
        'email': user_schema['email'],
        'password': 'anotherSecret',
    }
    # Act
    response = client.post(
        '/users',
        json=user_data,
    )
    # Assert
    assert response.status_code == HTTPStatus.CONFLICT


def test_resume_users(client, dummy_user, token):  # Arrange
    user_schema = PublicUserSchema.model_validate(dummy_user).model_dump()
    # Act
    response = client.get(
        '/users', headers={'Authorization': f'Bearer {token}'}
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_resume_user(client, dummy_user, token):  # Arrange
    user_schema = PublicUserSchema.model_validate(dummy_user).model_dump()
    # Act
    response = client.get(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_resume_user_not_found(client, token):  # Arrange
    # Act
    response = client.get(
        '/users/999', headers={'Authorization': f'Bearer {token}'}
    )
    # Assert
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_update_user(client, dummy_user, token):  # Arrange
    user_data = {
        'username': 'JaneDoe',
        'email': 'JaneDoe@example.com',
        'password': 'NewSecret',
    }
    # Act
    response = client.put(
        '/users/1',
        json=user_data,
        headers={'Authorization': f'Bearer {token}'},
    )
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'JaneDoe',
        'email': 'JaneDoe@example.com',
    }


def test_update_integrity_violation(client, dummy_user, token):  # Arrange

    # Create another user to cause integrity violation
    client.post(
        '/users',
        json={
            'username': 'JaneDoe',
            'email': 'jane@example.com',
            'password': 'Secret',
        },
    )

    # Act
    response_update = client.put(
        f'/users/{dummy_user.id}',
        json={
            'username': 'JaneDoe',
            'email': 'JhonDoe@example.com',
            'password': 'Secret123',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or email already exists'
    }


def test_update_another_user(client, dummy_user, token):  # Arrange
    # Create another user
    client.post(
        '/users',
        json={
            'username': 'JaneDoe',
            'email': 'jane@example.com',
            'password': 'Secret',
        },
    )
    # Act
    response_update = client.put(
        '/users/2',
        json={
            'username': 'JoseyDoe',
            'email': 'JoseyDoe@example.com',
            'password': 'Josey123',
        },
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response_update.status_code == HTTPStatus.FORBIDDEN
    assert response_update.json() == {
        'detail': 'You do not have permission to update this user'
    }


def test_delete_user(client, dummy_user, token):  # Arrange
    # Act
    response = client.delete(
        '/users/1', headers={'Authorization': f'Bearer {token}'}
    )
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_delete_another_user(client, dummy_user, token):  # Arrange
    # Create another user
    client.post(
        '/users',
        json={
            'username': 'JaneDoe',
            'email': 'jane@example.com',
            'password': 'Secret',
        },
    )
    # Act
    response = client.delete(
        '/users/2', headers={'Authorization': f'Bearer {token}'}
    )
    # Assert
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {
        'detail': 'You do not have permission to delete this user'
    }


def test_get_jwt(client, dummy_user):  # Arrange
    # Act
    response = client.post(
        '/token',
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
        '/token',
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
        '/token',
        data={
            'username': dummy_user.username,
            'password': 'wrongpassword',
        },
    )
    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Incorrect username or password'}

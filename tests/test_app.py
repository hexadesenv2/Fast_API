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


def test_create_user_with_existing_username(client, default_user):  # Arrange
    user_schema = PublicUserSchema.model_validate(default_user).model_dump()
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


def test_create_user_with_existing_email(client, default_user):  # Arrange
    user_schema = PublicUserSchema.model_validate(default_user).model_dump()
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


def test_resume_users(client):  # Arrange
    # Act
    response = client.get('/users')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_resume_users_with_user(client, default_user):  # Arrange
    user_schema = PublicUserSchema.model_validate(default_user).model_dump()
    # Act
    response = client.get('/users')

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_resume_user(client, default_user):  # Arrange
    user_schema = PublicUserSchema.model_validate(default_user).model_dump()
    # Act
    response = client.get('/users/1')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_resume_user_not_found(client):  # Arrange
    # Act
    response = client.get('/users/999')
    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client, default_user):  # Arrange
    user_data = {
        'username': 'JaneDoe',
        'email': 'JaneDoe@example.com',
        'password': 'NewSecret',
    }
    # Act
    response = client.put('/users/1', json=user_data)
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'JaneDoe',
        'email': 'JaneDoe@example.com',
    }


def test_update_user_not_found(client):  # Arrange
    user_data = {
        'username': 'NoUser',
        'email': 'NoUser@example.com',
        'password': 'Secret',
    }
    # Act
    response = client.put('/users/999', json=user_data)
    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_integrity_violation(client, default_user):  # Arrange

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
        f'/users/{default_user.id}',
        json={
            'username': 'JaneDoe',
            'email': 'JhonDoe@example.com',
            'password': 'Secret123',
        },
    )

    # Assert
    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        'detail': 'Username or email already exists'
    }


def test_delete_user(client, default_user):  # Arrange
    # Act
    response = client.delete('/users/1')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted successfully'}


def test_delete_user_not_found(client):  # Arrange
    # Act
    response = client.delete('/users/999')
    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND

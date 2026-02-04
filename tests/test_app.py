from http import HTTPStatus


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


def test_resume_users(client):  # Arrange
    # Act
    response = client.get('/users')

    # Assert
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    response_data == {
        'users': [
            {'id': 1, 'username': 'JhonDoe', 'email': 'JhonDoe@example.com'}
        ]
    }


def test_resume_user(client):  # Arrange
    # Act
    response = client.get('/users/1')
    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'JhonDoe',
        'email': 'JhonDoe@example.com',
    }


def test_resume_user_not_found(client):  # Arrange
    # Act
    response = client.get('/users/999')
    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_user(client):  # Arrange
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


def test_delete_user(client):  # Arrange
    # Act
    response = client.delete('/users/1')
    # Assert
    assert response.status_code == HTTPStatus.NO_CONTENT


def test_delete_user_not_found(client):  # Arrange
    # Act
    response = client.delete('/users/999')
    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND

from http import HTTPStatus

from jwt import decode

from fast_zero.security import ALGORITHM, SECRET_KEY, create_access_token


def test_create_jwt():
    # Arrange
    clain = {'test': 'test'}
    token = create_access_token(clain)
    # Act
    decoded = decode(token, SECRET_KEY, algorithms=ALGORITHM)
    # Assert
    assert decoded['test'] == clain['test']
    assert 'exp' in decoded


def test_jwt_invalid(client):  # Arrange
    # Act
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer invalidtoken'}
    )
    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_credentials_exception_on_get_user_but_doesnt_have_subject(
    client,
):  # Arrange
    clain = {'no-sub': 'nosubject'}
    token = create_access_token(clain)
    # Act
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_credentials_exception_on_get_user_but_doesnt_exists(
    client,
):  # Arrange
    clain = {'sub': 'nonexistentuser'}
    token = create_access_token(clain)
    # Act
    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
    # Assert
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}

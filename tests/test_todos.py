from http import HTTPStatus

import factory
import factory.fuzzy
import pytest

from fast_zero.models import Todo, ToDoState


class ToDoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(ToDoState)
    user_id = 1


def test_create_todo(client, token):  # Arrange

    # Act
    response = client.post(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test ToDo',
            'description': 'Test ToDo Description',
            'state': 'draft',
        },
    )
    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'id': 1,
        'title': 'Test ToDo',
        'description': 'Test ToDo Description',
        'state': 'draft',
    }


@pytest.mark.asyncio
async def test_resume_todos_should_return_5_todos(
    session, client, dummy_user, token
):  # Arrange
    expected_todos = 5
    session.add_all(ToDoFactory.create_batch(5, user_id=dummy_user.id))
    await session.commit()

    # Act
    response = client.get(
        '/todos',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_resume_todos_pagination_should_return_2_todos(
    session, client, dummy_user, token
):  # Arrange
    expected_todos = 2
    session.add_all(ToDoFactory.create_batch(5, user_id=dummy_user.id))
    await session.commit()

    # Act
    response = client.get(
        'todos/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_resume_todos_filter_title_should_return_5_todos(
    session, client, dummy_user, token
):  # Arrange
    expected_todos = 5
    session.add_all(
        ToDoFactory.create_batch(5, user_id=dummy_user.id, title='Test Todo 1')
    )
    await session.commit()

    # Act
    response = client.get(
        'todos/?title=Test Todo 1',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_resume_todos_filter_description_should_return_5_todos(
    session, client, dummy_user, token
):  # Arrange
    expected_todos = 5
    session.add_all(
        ToDoFactory.create_batch(
            5, user_id=dummy_user.id, description='Description todo 1'
        )
    )
    await session.commit()

    # Act
    response = client.get(
        'todos/?description=Desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_resume_todos_filter_state_should_return_5_todos(
    session, client, dummy_user, token
):  # Arrange
    expected_todos = 5
    session.add_all(
        ToDoFactory.create_batch(
            5, user_id=dummy_user.id, state=ToDoState.todo
        )
    )
    await session.commit()

    # Act
    response = client.get(
        'todos/?state=todo',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['todos']) == expected_todos


@pytest.mark.asyncio
async def test_delete_todo(session, client, dummy_user, token):  # Arrange
    todo = ToDoFactory(user_id=dummy_user.id)
    session.add(todo)
    await session.commit()

    # Act
    response = client.delete(
        f'/todos/{todo.id}', headers={'Authorization': f'Bearer {token}'}
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Task has been deleted successfully'}


@pytest.mark.asyncio
async def test_delete_todo_not_found(client, token):  # Arrange

    # Act
    response = client.delete(
        '/todos/999', headers={'Authorization': f'Bearer {token}'}
    )
    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_delete_other_user_todo(
    session, client, token, other_dummy_user
):  # Arrange
    todo_uther_user = ToDoFactory(user_id=other_dummy_user.id)
    session.add(todo_uther_user)
    await session.commit()

    # Act
    response = client.delete(
        f'/todos/{todo_uther_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


def test_patch_todo_error(client, token):  # Arrange

    # Act
    response = client.patch(
        '/todos/999',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Task not found'}


@pytest.mark.asyncio
async def test_patch_todo(session, client, dummy_user, token):  # Arrange
    todo = ToDoFactory(user_id=dummy_user.id)

    session.add(todo)
    await session.commit()

    # Act
    response = client.patch(
        f'/todos/{todo.id}',
        json={'title': 'Test Title To do'},
        headers={'Authorization': f'Bearer {token}'},
    )

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json()['title'] == 'Test Title To do'

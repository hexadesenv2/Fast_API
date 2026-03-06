from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.models import Todo, ToDoState, User


@pytest.mark.asyncio
async def test_user_model(session: AsyncSession, mock_db_time):  # Arrange
    # Act
    with mock_db_time(model=User) as time:
        new_user = User(
            username='JhonDoe',
            email='JhonDoe@example.com',
            password='SecretKey',
        )

        session.add(new_user)
        await session.commit()

        user = await session.scalar(
            select(User).where(User.username == 'JhonDoe')
        )
        # Assert
        assert asdict(user) == {
            'id': 1,
            'username': 'JhonDoe',
            'email': 'JhonDoe@example.com',
            'password': 'SecretKey',
            'created_at': time,
            'updated_at': time,
            'todos': [],
        }


@pytest.mark.asyncio
async def test_todo_model(
    session: AsyncSession, mock_db_time, dummy_user
):  # Arrange
    # Act
    with mock_db_time(model=Todo) as time:
        new_todo = Todo(
            title='Todo title',
            description='Todo description',
            state=ToDoState.todo,
            user_id=dummy_user.id,
        )

        session.add(new_todo)
        await session.commit()

        todo = await session.scalar(
            select(Todo).where(
                Todo.user_id == dummy_user.id, Todo.state == ToDoState.todo
            )
        )
        # Assert
        assert asdict(todo) == {
            'id': 1,
            'title': 'Todo title',
            'description': 'Todo description',
            'state': ToDoState.todo,
            'user_id': dummy_user.id,
            'created_at': time,
            'updated_at': time,
        }

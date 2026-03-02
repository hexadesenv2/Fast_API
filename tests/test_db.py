from dataclasses import asdict

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fast_zero.models import User


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
        }

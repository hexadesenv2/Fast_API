from dataclasses import asdict

from sqlalchemy import select

from fast_zero.models import User


def test_user_model(session, mock_db_time):

    with mock_db_time(model=User) as time:
        new_user = User(
            username='JhonDoe',
            email='JhonDoe@example.com',
            password='SecretKey',
        )

        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'JhonDoe'))

        assert asdict(user) == {
            'id': 1,
            'username': 'JhonDoe',
            'email': 'JhonDoe@example.com',
            'password': 'SecretKey',
            'created_at': time,
            'updated_at': time,
        }

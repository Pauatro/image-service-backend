from users.services.schemas import CreateUser
from users.services.users import create_user
from users.services.authentication import get_password_hash
from users.services.exceptions import UserAlreadyExistsException

mock_users = [
    {
        "username": "username",
        "hashed_password": get_password_hash("password"),
    },
]


def seed_users_table():
    for user in mock_users:
        try:
            create_user(CreateUser(**user))
        except UserAlreadyExistsException:
            continue

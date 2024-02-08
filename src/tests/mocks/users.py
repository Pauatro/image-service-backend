import uuid
from datetime import datetime
from users.data.models import UserModel
from users.services.authentication import get_password_hash


def get_mock_user(username: str = "username", password: str = "password"):
    return UserModel(
        username=username,
        hashed_password=get_password_hash(password),
        id=uuid.uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

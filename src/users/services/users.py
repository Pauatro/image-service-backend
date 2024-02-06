from sqlalchemy.orm import Session
from sqlalchemy import select
from shared.database import get_db_session
from shared.logging import get_logger, Logger
from users.data.models import UserModel
from users.services.schemas import User, CreateUser
from users.services.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    IncorrectUsernameOrPasswordException,
)
from users.services.authentication import verify_password


def get_user_by_username(
    username: str, session: Session = get_db_session(), logger: Logger = get_logger()
) -> User:
    try:
        statement = select(UserModel).where(UserModel.username == username)
        user = session.execute(statement).first()
        if not user:
            logger.error(f"User with username {username} was not found")
            raise UserNotFoundException()
        else:
            logger.info(f"Found user {user[0].username} with id {user[0].id}")
            return User.model_validate(user[0])
    except Exception as error:
        logger.error(error)


def create_user(
    user: CreateUser, session: Session = get_db_session(), logger: Logger = get_logger()
):
    try:
        existing_user = get_user_by_username(user.username, session, logger)
        if existing_user:
            logger.error(
                f"Failed to create user with username {user.username} because it already exists"
            )
            raise UserAlreadyExistsException()
    except UserNotFoundException:
        new_user = UserModel(**user.model_dump())
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        logger.info(f"Created user {new_user.username} with id {new_user.id}")
        return new_user
    except Exception as error:
        logger.error(error)


def authenticate_user(user: User, password: str, logger: Logger = get_logger()):
    try:
        if not verify_password(password, user.hashed_password):
            logger.info(f"Password authentication for user {user.id} failed")
            raise IncorrectUsernameOrPasswordException()
        logger.info(f"User {user.id} was successfully authenticated")
        return user
    except UserNotFoundException:
        raise IncorrectUsernameOrPasswordException()

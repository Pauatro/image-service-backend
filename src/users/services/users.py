from sqlalchemy import select
import jwt
from datetime import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from shared.database import get_db_session
from shared.logging import get_logger
from users.data.models import UserModel
from users.services.schemas import User, CreateUser
from users.services.exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
    IncorrectUsernameOrPasswordException,
)
from users.endpoints.exceptions import (
    InvalidTokenHttpException,
    ExpiredTokenHttpException,
    UserNotFoundHttpException,
)
from users.services.authentication import verify_password, decode_access_token
from users.services.schemas import TokenPayload, User


def get_user_by_username(
    username: str, session=get_db_session(), logger=get_logger()
) -> User:
    try:
        statement = select(UserModel).where(UserModel.username == username)
        user = session.execute(statement).first()
    except Exception as error:
        logger.error(error)
        raise Exception(error)

    if not user:
        logger.warning(f"User with username {username} was not found")
        raise UserNotFoundException()
    else:
        logger.info(f"Found user {user[0].username} with id {user[0].id}")
        return User.model_validate(user[0])


def create_user(user: CreateUser, session=get_db_session(), logger=get_logger()):
    try:
        existing_user = get_user_by_username(user.username, session, logger)
        if existing_user:
            logger.warning(
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
    except UserAlreadyExistsException:
        raise UserAlreadyExistsException()
    except Exception as error:
        logger.error(error)
        raise Exception(error)


def authenticate_user(user: User, password: str, logger=get_logger()):
    try:
        if not verify_password(password, user.hashed_password):
            logger.info(f"Password authentication for user {user.id} failed")
            raise IncorrectUsernameOrPasswordException()
        logger.info(f"User {user.id} was successfully authenticated")
        return user
    except UserNotFoundException:
        raise IncorrectUsernameOrPasswordException()


reusable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")


async def get_current_user(
    token: str = Depends(reusable_oauth), logger=Depends(get_logger)
) -> User:
    try:
        payload = decode_access_token(token)
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            logger.warning("Expired bearer token")
            raise ExpiredTokenHttpException()
    except (jwt.PyJWTError, ValidationError):
        logger.warning("Missing or invalid bearer token")
        raise InvalidTokenHttpException()

    try:
        user = get_user_by_username(token_data.sub)
    except UserNotFoundException:
        logger.info("User in bearer token was not found")
        raise UserNotFoundHttpException()

    logger.info("User authenticated through bearer token")
    return user

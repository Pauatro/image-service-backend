from passlib.context import CryptContext
import jwt
import time
from shared.settings import Settings

app_settings = Settings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(
        to_encode, app_settings.jwt_secret_key, algorithm=app_settings.jwt_algorithm
    )
    return encoded_jwt


def get_token_expiration_time(expires_delta_seconds: int):
    return round(time.time()) + expires_delta_seconds

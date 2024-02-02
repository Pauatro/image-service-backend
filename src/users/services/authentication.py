from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from users.services.users import get_user_by_username
from users.services.exceptions import UserNotFoundException, IncorrectUsernameOrPasswordException

SECRET_KEY = "574387fbcb3fbf0c0e58c893f3a5fe40f6b244480137993adb8a1024f74ade5e"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    try: 
        user = get_user_by_username(username)
        if not verify_password(password, user.hashed_password):
            raise IncorrectUsernameOrPasswordException()
        return user
    except UserNotFoundException:
        raise IncorrectUsernameOrPasswordException()
    

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
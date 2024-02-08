from fastapi import APIRouter
from users.endpoints.exceptions import IncorrectUsernameOrPasswordHttpException
from shared.endpoints.exceptions import InternalServerHttpException
from users.services.exceptions import (
    IncorrectUsernameOrPasswordException,
    UserNotFoundException,
)
from users.services.users import get_user_by_username, authenticate_user
from users.services.authentication import create_access_token, get_token_expiration_time
from users.endpoints.schemas import LoginRequestBody, LoginResponseBody
from shared.settings import Settings

router = APIRouter()
app_settings = Settings()


@router.post("/login")
async def login(form_data: LoginRequestBody) -> LoginResponseBody:
    try:
        user = get_user_by_username(form_data.username)
        authenticate_user(user, form_data.password)
        access_token_expires = get_token_expiration_time(
            app_settings.access_token_expire_seconds
        )
        access_token = create_access_token(
            data={
                "sub": user.username,
                "exp": access_token_expires,
            }
        )

        return LoginResponseBody(
            access_token=access_token, expiration_time=access_token_expires
        )
    except UserNotFoundException:
        raise IncorrectUsernameOrPasswordHttpException()
    except IncorrectUsernameOrPasswordException:
        raise IncorrectUsernameOrPasswordHttpException()
    except:
        raise InternalServerHttpException()

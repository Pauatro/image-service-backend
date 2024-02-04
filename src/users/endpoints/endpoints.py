from fastapi import APIRouter
from users.endpoints.exceptions import IncorrectUsernameOrPasswordHttpException
from shared.endpoints.exceptions import InternalServerHttpException
from users.services.exceptions import IncorrectUsernameOrPasswordException
from users.services.authentication import authenticate_user, create_access_token, get_token_expiration_time
from users.endpoints.schemas import LoginRequestBody, LoginResponseBody
from shared.settings import Settings

router = APIRouter()
app_settings = Settings() 

@router.post("/login")
async def login_for_access_token(
    form_data:  LoginRequestBody
) -> LoginResponseBody:
    try:
        user = authenticate_user(form_data.username, form_data.password)
        access_token_expires = get_token_expiration_time(app_settings.access_token_expire_seconds)
        access_token = create_access_token(data={"sub": user.username})

        return LoginResponseBody(access_token=access_token, expiration_time=access_token_expires)
    except IncorrectUsernameOrPasswordException:
        raise IncorrectUsernameOrPasswordHttpException()
    except:
        raise InternalServerHttpException()
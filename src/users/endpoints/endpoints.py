from users.endpoints.exceptions import IncorrectUsernameOrPasswordHttpException, InternalServerHttpException
from users.services.exceptions import IncorrectUsernameOrPasswordException
from fastapi import APIRouter
from users.services.schemas import AccessToken
from users.services.authentication import authenticate_user, create_access_token
from users.endpoints.schemas import LoginRequestBody
from datetime import timedelta

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()
    
@router.post("/login")
async def login_for_access_token(
    form_data:  LoginRequestBody
) -> AccessToken:
    try:
        user = authenticate_user(form_data.username, form_data.password)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return AccessToken(access_token=access_token, token_type="bearer")
    except IncorrectUsernameOrPasswordException:
        raise IncorrectUsernameOrPasswordHttpException()
    except:
        raise InternalServerHttpException()
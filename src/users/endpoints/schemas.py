from pydantic import BaseModel


class LoginRequestBody(BaseModel):
    username: str
    password: str


class LoginResponseBody(BaseModel):
    access_token: str
    expiration_time: int

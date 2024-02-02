from pydantic import BaseModel

class LoginRequestBody(BaseModel):
    username: str
    password: str
from pydantic import BaseModel, UUID4
from datetime import datetime


class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: UUID4
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateUser(UserBase):
    hashed_password: str


class PostUser(UserBase):
    password: str

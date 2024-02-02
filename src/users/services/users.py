from sqlalchemy.orm import Session
from sqlalchemy import select
from pydantic.type_adapter import TypeAdapter
from shared.database import get_db_session
from users.data.models import UserModel
from users.services.schemas import User, CreateUser
from users.services.exceptions import UserNotFoundException, UserAlreadyExistsException

def get_user_by_username(username: str, session: Session = get_db_session()) -> User:
    statement = select(UserModel).where(UserModel.username == username)
    user = session.execute(statement).first()
    if not user:
        raise UserNotFoundException()
    else:
        return User.model_validate(user[0])
    
def create_user(user: CreateUser, session: Session = get_db_session()):
    try:
        existing_user = get_user_by_username(user.username)
        if existing_user:
            raise UserAlreadyExistsException()
    except UserNotFoundException:
        new_user = UserModel(**user.model_dump())
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        
        return new_user
  



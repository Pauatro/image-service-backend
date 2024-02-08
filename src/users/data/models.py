from shared.database import Base, UUID_Column
from sqlalchemy import Column, String, TIMESTAMP, text


class UserModel(Base):
    __tablename__ = "users"
    id = UUID_Column
    username = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    hashed_password = Column(String, nullable=False)

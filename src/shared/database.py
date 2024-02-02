from sqlalchemy import create_engine, Column, Uuid
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import uuid

DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/postgres'

engine = create_engine(DATABASE_URL)

SessionMakerInstance = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db_session():
    db_session = SessionMakerInstance()
    try:
        return db_session
    finally:
        db_session.close()

UUID_Column = Column(
        Uuid(as_uuid=True),
        default=uuid.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
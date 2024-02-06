from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from shared.settings import Settings
from users.endpoints import endpoints as users
from images.endpoints import endpoints as images
from shared.database import Base, engine
from users.data.mocks import seed_users_table

# setup loggers
logging.config.fileConfig("config/logging.conf", disable_existing_loggers=False)

## In a proper project this would be done using migrations, but works for this case
Base.metadata.create_all(engine)
seed_users_table()

app = FastAPI()
app_settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(images.router)

# TODO: add tests

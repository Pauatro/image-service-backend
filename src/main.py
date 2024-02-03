from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.settings import Settings
from users.endpoints import endpoints as users
from shared.database import Base, engine
from users.data.mocks import seed_users_table


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

# TODO: add logs
# TODO: add tests

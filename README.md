Hi! 

This is a small image service developed in python/FastAPI.

## Environment

I managed the local environment, dependencies and versions using [Poetry](https://python-poetry.org/docs/).

if you don't have poetry installed, you'll first need to install pipx if you don't have it:

```
pip3 install pipx
```

then you can install poetry:

```
pipx install poetry
```

Dependencies are specified in the pyproject.toml and the exact versions are in the poetry.lock. Dependencies should be installed using the command:

```
poetry install
```

Some environment vars need to be set in a .env to initialize the project locally.
Of course, usually these wouldn't be included in the project, but for the sake of being able to run the project without issues they're included here to generate your own .env in the root folder:

```
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="postgres"
POSTGRES_HOST="0.0.0.0"
POSTGRES_DB="postgres"
POSTGRES_PORT="5432"
LOGGER="root"
```

If you're running the project directly using docker-compose you won't need to do that since these env vars are also defined in the docker-compose file.

## Initialization

To run the backend in development mode, run the following command inside the src folder:

```
uvicorn main:app -p 8008 --reload
```

The app will run on port 8008.

## Running the Dockerized version

Everything is set up to run the app using docker and docker-compose.
Since there's two separate repos (frontend and backend), the image for the frontend needs to be generated first. To do that, run the following command in the root folder of the frontend project:

```
docker build . -t image-service-frontend
```

Then you can just run the docker compose in this project to have everything up and running:

```
docker compose up -d
```

## Documentation

Once run locally, API documentation is automatically generated [here](http://localhost:8008/docs)

## Logging in

The test user has the following credentials:
- Username: username
- Pwd: password

## Tests

Tests need to be run from the src folder, otherwise the images tests will fail to find the mock db. You just need to run the command:

```
pytest
```
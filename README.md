Hi! 

This is a small image service developed in python/FastAPI.

## Environment

I managed the local environment, dependencies and versions using [Poetry](https://python-poetry.org/docs/).

if you don't have poetry installed, you'll first need to install pipx if you don't have it:

```pip3 install pipx```

then you can install poetry:

```pipx install poetry```

dependencies are specified in the pyproject.toml and the exact versions are in the poetry.lock. Dependencies should be installed using the command:

```poetry install```


## Initialization

To run the backend in development mode, run the following command inside the src folder:

```uvicorn main:app --reload```

The app will run on port 8000.

## Documentation

Once run locally, API documentation is automatically generated [here](http://localhost:8000/docs)

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
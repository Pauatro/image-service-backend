FROM python:3.8.10

WORKDIR /src/

# https://docs.python.org/3/using/cmdline.html#envvar-PYTHONDONTWRITEBYTECODE
# Prevents Python from writing .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1

# ensures that the python output is sent straight to terminal (e.g. your container log)
# without being first buffered and that you can see the output of your application
# in real time. Equivalent to python -u: https://docs.python.org/3/using/cmdline.html#cmdoption-u
ENV PYTHONUNBUFFERED 1
ENV ENVIRONMENT prod
ENV TESTING 0

# Install Poetry
RUN curl -sSL https://install.python-poetry.org/ | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock /src/

RUN bash -c "poetry install --no-root"

ADD src /src/src

ENV PYTHONPATH=/src
ENV PORT=${PORT:-8000}
ENV APP_MODULE=${APP_MODULE:-"main:src"}
ENV HOST=${HOST:-0.0.0.0}

EXPOSE ${PORT}

WORKDIR /src/src

CMD uvicorn ${APP_MODULE} --host ${HOST} --port ${PORT}

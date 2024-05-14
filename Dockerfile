FROM python:3.11-buster

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.4.2 \
    POETRY_VIRTUALENVS_CREATE="false"

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock docker-entrypoint.sh ./
RUN poetry install --no-interaction --no-ansi --no-dev

COPY . /app

EXPOSE 8787

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
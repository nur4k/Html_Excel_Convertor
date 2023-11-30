FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - && \
    mv /etc/poetry/bin/poetry /usr/local/bin/poetry

COPY . .

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-dev --no-interaction --no-ansi

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/:$PYTHONPATH"

RUN mkdir -p media

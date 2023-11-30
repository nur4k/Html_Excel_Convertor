# FROM python:3.11-slim as builder
# WORKDIR /app
# ## Install poetry
# RUN apt-get update && apt-get install -y curl
# RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
# ENV PATH=$PATH:/etc/poetry/bin

# ##
# ADD ./poetry.lock ./pyproject.toml ./
# RUN poetry config virtualenvs.in-project true
# RUN poetry install --only main

# FROM python:3.11-slim
# WORKDIR /app
# ENV PATH=/app/.venv/bin:$PATH PYTHONPATH=$PYTHONPATH:/app/
# COPY --from=builder /app/.venv .venv
# COPY . .
# RUN python3 manage.py collectstatic --settings core.settings_test
# ENTRYPOINT ["gunicorn", "core.wsgi", "--bind", "0.0.0.0:8000", "--workers", "4", "--threads", "4"]

FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 - && \
    mv /etc/poetry/bin/poetry /usr/local/bin/poetry

COPY . .

RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/:$PYTHONPATH"

RUN mkdir -p media

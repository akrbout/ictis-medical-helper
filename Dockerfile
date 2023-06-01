FROM python:3.10.6-alpine3.16

RUN pip3 install -U pip poetry

WORKDIR /app/

COPY poetry.lock /app
COPY pyproject.toml /app

RUN poetry config virtualenvs.in-project true
RUN poetry install --no-root

COPY ./ /app

CMD ["poetry", "run", "python", "./src/main.py"]
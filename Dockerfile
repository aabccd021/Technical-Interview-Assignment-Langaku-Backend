FROM python:3.12-slim

WORKDIR /code

RUN pip install uv

COPY . .

RUN uv sync --all-groups

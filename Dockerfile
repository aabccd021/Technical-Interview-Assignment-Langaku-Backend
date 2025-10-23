FROM python:3.12-slim

WORKDIR /code

RUN pip install uv

COPY . .

RUN uv sync --all-groups

EXPOSE 8000

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]

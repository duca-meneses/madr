FROM python:3.12-slim
ENV POETRY_VIRTUAL_CREATE=false

WORKDIR app/
COPY . .

RUN pip install poetry

RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi

EXPOSE 8000
CMD poetry run fastapi run madr/app.py --host 0.0.0.0
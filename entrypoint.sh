#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicializa a aplicação
poetry run fastapi run madr/app.py --host 0.0.0.0
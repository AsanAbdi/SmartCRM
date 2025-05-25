#!/usr/bin/env bash
set -e

# Выполняем миграции
alembic upgrade head

# Запускаем приложение
exec uvicorn core.main:app --host 0.0.0.0 --port 8000
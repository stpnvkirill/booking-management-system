# Этап 1: сборка
FROM ghcr.io/astral-sh/uv:python3.14-alpine AS builder

ARG PIP_NO_CACHE_DIR=1
ARG PYTHONDONTWRITEBYTECODE=1
ARG PYTHONUNBUFFERED=1

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1

WORKDIR /app

# Копируем только необходимое для установки зависимостей
COPY pyproject.toml uv.lock ./

# Устанавливаем production зависимости
RUN uv sync --frozen --no-dev --no-editable

# Этап 2: рантайм
FROM python:3.14-alpine

WORKDIR /app

# Копируем установленные зависимости
COPY --from=builder /app/.venv .venv

# Копируем исходный код
COPY . .

# Добавляем .venv/bin в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Удаляем ненужные файлы
RUN find /app/.venv -type f -name '*.pyc' -delete && \
    find /app/.venv -type d -name '__pycache__' -delete && \
    find /app/.venv -type f -name '*.so' -exec strip {} \; 2>/dev/null || true

# Non-root пользователь
RUN adduser -D -u 1000 appuser
USER appuser

ENTRYPOINT ["python", "-m", "uvicorn", "main:app"]

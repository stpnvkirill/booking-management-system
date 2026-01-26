FROM python:3.14-alpine

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk add --no-cache \
    ca-certificates \
    build-base \
    rust \
    cargo

COPY telegram_alert.py /app/telegram_alert.py

RUN pip install --no-cache-dir \
    fastapi==0.128.0 \
    uvicorn==0.40.0 \
    httpx==0.27.0 \
    "pydantic>=2.0.0,<3.0.0"

EXPOSE 8080

CMD ["uvicorn", "telegram_alert:app", "--host", "0.0.0.0", "--port", "8080"]


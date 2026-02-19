FROM python:3.12-slim AS builder

WORKDIR /install

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

COPY app/requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

FROM python:3.12-slim AS runtime

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends libpq5 netcat-openbsd && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
COPY app/requirements.txt .
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

COPY app /app
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]

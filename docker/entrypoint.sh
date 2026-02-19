#!/bin/sh
set -e

echo "Aguardando banco em ${POSTGRES_HOST}:${POSTGRES_PORT}..."
until nc -z "$POSTGRES_HOST" "$POSTGRES_PORT"; do
  sleep 1
done

echo "Aplicando migrations..."
python manage.py migrate --noinput

echo "Coletando estáticos..."
python manage.py collectstatic --noinput

exec "$@"

#!/usr/bin/env bash
set -o errexit

echo "Instalando dependencias de Python..."
pip install -r requirements.txt

echo "Entrando al frontend..."
cd frontend

echo "Instalando dependencias del frontend..."
pnpm install --frozen-lockfile

echo "Construyendo frontend..."
pnpm run build

echo "Volviendo a la raíz..."
cd ..

echo "Iniciando servidor Django..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 300
#!/bin/sh
set -e

echo "⏳ Ждём базу данных..."
python manage.py wait_for_db 2>/dev/null || sleep 5

echo "🔄 Применяем миграции..."
python manage.py migrate --noinput --settings=config.settings.production

echo "📦 Собираем статику..."
python manage.py collectstatic --noinput --settings=config.settings.production

echo "🚀 Запускаем Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
